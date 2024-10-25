import os

def run_command(cmd):
    """Run a shell command and handle its success or failure."""
    print(f"Running: {cmd}")
    result = os.system(cmd)
    if result == 0:
        print(f"Command succeeded: {cmd}")
    else:
        print(f"Command failed: {cmd}")

def configure_kernel_modules():
    """Load required kernel modules and configure sysctl settings for Kubernetes."""
    run_command("sudo modprobe overlay")
    run_command("sudo modprobe br_netfilter")

    with open("/etc/modules-load.d/containerd.conf", "w") as f:
        f.write("overlay\nbr_netfilter\n")

    with open("/etc/sysctl.d/kubernetes.conf", "w") as f:
        f.write("net.bridge.bridge-nf-call-ip6tables = 1\n")
        f.write("net.bridge.bridge-nf-call-iptables = 1\n")
        f.write("net.ipv4.ip_forward = 1\n")

    run_command("sudo sysctl --system")

def install_containerd():
    """Install and configure containerd."""
    run_command("sudo dnf install -y yum-utils")
    run_command("sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo")
    run_command("sudo dnf install -y containerd.io")
    run_command("sudo mkdir -p /etc/containerd")
    run_command("containerd config default | sudo tee /etc/containerd/config.toml")
    run_command("sudo sed -i '/SystemdCgroup = false/c\\SystemdCgroup = true' /etc/containerd/config.toml")
    run_command("sudo systemctl restart containerd")
    run_command("sudo systemctl enable containerd")

def install_kubernetes_tools(install_kubectl):
    """Install Kubernetes tools: kubelet, kubeadm, and optionally kubectl."""
    run_command("sudo dnf install -y curl")
    run_command("sudo dnf install -y kubelet kubeadm")
    if install_kubectl:
        run_command("sudo dnf install -y kubectl")
    run_command("sudo systemctl enable --now kubelet")

def disable_swap():
    """Disable swap for Kubernetes compatibility."""
    run_command("sudo swapoff -a")
    run_command("sudo sed -i '/ swap / s/^/#/' /etc/fstab")

def configure_hosts():
    """Ask for and configure the API server address in /etc/hosts."""
    apiserver_ip = input("Enter the IP address for your API server: ")
    with open("/etc/hosts", "a") as f:
        f.write(f"{apiserver_ip} apisrv.moradi.com\n")

def setup_master_node():
    """Configure the node as a Kubernetes master."""
    install_kubernetes_tools(install_kubectl=True)
    run_command("sudo kubeadm init --control-plane-endpoint 'apisrv.moradi.com:6443' --upload-certs --pod-network-cidr=10.244.0.0/16")
    run_command("mkdir -p $HOME/.kube && sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config")
    run_command("kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml")

def setup_worker_node():
    """Configure the node as a Kubernetes worker."""
    install_kubernetes_tools(install_kubectl=False)
    token = input("Enter kubeadm join token: ")
    ca_cert_hash = input("Enter discovery-token-ca-cert-hash: ")
    run_command(f"sudo kubeadm join apisrv.moradi.com:6443 --token {token} --discovery-token-ca-cert-hash sha256:{ca_cert_hash}")

def setup_control_plane_node():
    """Configure the node as an additional control plane."""
    install_kubernetes_tools(install_kubectl=False)
    token = input("Enter kubeadm join token: ")
    ca_cert_hash = input("Enter discovery-token-ca-cert-hash: ")
    cert_key = input("Enter certificate key: ")
    run_command(f"sudo kubeadm join apisrv.moradi.com:6443 --token {token} --discovery-token-ca-cert-hash sha256:{ca_cert_hash} --control-plane --certificate-key {cert_key}")

def main():
    configure_kernel_modules()
    install_containerd()
    disable_swap()
    configure_hosts()

    node_type = input("Choose node type: 1 for master, 2 for worker, 3 for control plane: ")
    if node_type == "1":
        setup_master_node()
    elif node_type == "2":
        setup_worker_node()
    elif node_type == "3":
        setup_control_plane_node()
    else:
        print("Invalid input. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
