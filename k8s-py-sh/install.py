import subprocess

def run_command(cmd):
    """Run a command and print its result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Command succeeded: {cmd}")
    else:
        print(f"Command failed: {cmd}\nError: {result.stderr}")
    return result

def configure_kernel_modules():
    """Load kernel modules and configure sysctl settings for Kubernetes."""
    run_command("sudo modprobe overlay")
    run_command("sudo modprobe br_netfilter")
    
    # Write kernel modules to configuration file
    with open("/etc/modules-load.d/containerd.conf", "w") as f:
        f.write("overlay\nbr_netfilter")
    
    # Configure sysctl settings
    sysctl_conf = """
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
"""
    with open("/etc/sysctl.d/kubernetes.conf", "w") as f:
        f.write(sysctl_conf)
    
    run_command("sudo sysctl --system")

def install_containerd():
    """Install and configure containerd."""
    run_command("sudo apt-get update")
    run_command("sudo apt-get install -y containerd")
    run_command("sudo mkdir -p /etc/containerd")
    run_command("sudo containerd config default | sudo tee /etc/containerd/config.toml > /dev/null")
    run_command("sudo sed -i '/\\[plugins.\"io.containerd.grpc.v1.cri\".containerd.runtimes.runc.options\\]/,/}/s/SystemdCgroup =.*/SystemdCgroup = true/' /etc/containerd/config.toml")

def install_kubernetes_tools(install_kubectl=True):
    """Install Kubernetes tools."""
    run_command("sudo apt-get update")
    run_command("sudo apt-get install -y apt-transport-https ca-certificates curl gpg")
    run_command("curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.31/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg")
    run_command("echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.31/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list")

    run_command("sudo apt-get update")
    run_command("sudo apt-get install -y kubelet kubeadm")
    
    if install_kubectl:
        run_command("sudo apt-get install -y kubectl")
    
    run_command("sudo apt-mark hold kubelet kubeadm kubectl")
    run_command("sudo systemctl enable kubelet")

def disable_swap():
    """Disable swap."""
    run_command("sudo swapoff -a")
    run_command("sudo sed -i '/ swap / s/^(.*)$/#\\1/g' /etc/fstab")

def configure_hosts():
    """Add server IP and apisrv.example.com to /etc/hosts."""
    apiserver_ip = input("Please enter the IP address for apisrv.example.com: ")
    with open("/etc/hosts", "a") as f:
        f.write(f"{apiserver_ip} apisrv.example.com\n")

def setup_master_node():
    """Configure this node as the Kubernetes master."""
    run_command("sudo hostnamectl set-hostname 'master'")
    install_kubernetes_tools(install_kubectl=True)
    run_command("sudo kubeadm config images pull")
    
    # Run kubeadm init and save output
    run_command("sudo kubeadm init --control-plane-endpoint 'apisrv.example.com:8443' --upload-certs --pod-network-cidr=10.244.0.0/16 | tee ~/kubeadm_init_output.txt")
    
    # Install Flannel network plugin
    run_command("kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml")
    
    # Configure kubectl access
    run_command("mkdir -p $HOME/.kube")
    run_command("sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config")
    run_command("sudo chown $(id -u):$(id -g) $HOME/.kube/config")
    
    print("Master node is configured and Flannel is installed.")

def setup_worker_node():
    """Configure this node as a Kubernetes worker."""
    run_command("sudo hostnamectl set-hostname 'worker'")
    install_kubernetes_tools(install_kubectl=False)
    
    token = input("Please enter the kubeadm join token: ")
    ca_cert_hash = input("Please enter the discovery-token-ca-cert-hash: ")
    run_command(f"sudo kubeadm join apisrv.example.com:8443 --token {token} --discovery-token-ca-cert-hash sha256:{ca_cert_hash}")
    print("Worker node is configured and joined to the cluster.")

def setup_control_plane_node():
    """Configure this node as an additional Kubernetes control plane."""
    run_command("sudo hostnamectl set-hostname 'control-plane'")
    install_kubernetes_tools(install_kubectl=False)
    
    token = input("Please enter the kubeadm join token: ")
    ca_cert_hash = input("Please enter the discovery-token-ca-cert-hash: ")
    certificate_key = input("Please enter the certificate key: ")
    run_command(f"sudo kubeadm join apisrv.example.com:8443 --token {token} --discovery-token-ca-cert-hash sha256:{ca_cert_hash} --control-plane --certificate-key {certificate_key}")
    print("Control plane node is configured and joined to the cluster.")

def main():
    configure_kernel_modules()
    install_containerd()
    disable_swap()
    configure_hosts()
    
    # Prompt user to configure master, worker, or control plane node
    node_type = input("If this node is a master, press 1. If it's a worker, press 2. If it's a control plane node, press 3: ")
    
    if node_type == "1":
        setup_master_node()
    elif node_type == "2":
        setup_worker_node()
    elif node_type == "3":
        setup_control_plane_node()
    else:
        print("Invalid input. Please enter 1 for master, 2 for worker, or 3 for control plane.")

if __name__ == "__main__":
    main()

