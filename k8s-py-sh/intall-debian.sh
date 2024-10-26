#!/bin/bash

run_command() {
    # Run a command and handle its output
    local cmd="$1"
    echo "Running: $cmd"
    eval "$cmd"
    if [ $? -eq 0 ]; then
        echo "Command succeeded: $cmd"
    else
        echo "Command failed: $cmd"
    fi
}

configure_kernel_modules() {
    # Load kernel modules and configure sysctl settings for Kubernetes
    run_command "sudo modprobe overlay"
    run_command "sudo modprobe br_netfilter"

    # Add modules to containerd config
    echo -e "overlay\nbr_netfilter" | sudo tee /etc/modules-load.d/containerd.conf

    # Configure sysctl settings
    cat <<EOF | sudo tee /etc/sysctl.d/kubernetes.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF

    # Apply sysctl settings
    run_command "sudo sysctl --system"
}

install_containerd() {
    # Install and configure containerd
    run_command "sudo apt-get update"
    run_command "sudo apt-get install -y containerd"
    
    sudo mkdir -p /etc/containerd
    run_command "sudo containerd config default | sudo tee /etc/containerd/config.toml"
    sudo sed -i "/\[plugins.\"io.containerd.grpc.v1.cri\".containerd.runtimes.runc.options\]/,/}/s/SystemdCgroup =.*/SystemdCgroup = true/" /etc/containerd/config.toml
}

install_kubernetes_tools() {
    # Install Kubernetes tools like kubelet, kubeadm, and optionally kubectl for the master
    local install_kubectl=$1
    run_command "sudo apt-get update"
    run_command "sudo apt-get install -y apt-transport-https ca-certificates curl gpg"
    run_command "curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.31/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg"
    echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.31/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list

    run_command "sudo apt-get update"
    run_command "sudo apt-get install -y kubelet kubeadm"
    
    if [ "$install_kubectl" = "true" ]; then
        run_command "sudo apt-get install -y kubectl"
    fi

    run_command "sudo apt-mark hold kubelet kubeadm kubectl"
    run_command "sudo systemctl enable kubelet"
}

disable_swap() {
    # Disable swap
    run_command "sudo swapoff -a"
    sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
}

configure_hosts() {
    # Prompt user to enter the server's IP address for apisrv.example.com
    read -p "Please enter the IP address for apisrv.example.com: " apiserver_ip

    # Add server's IP and domain name to /etc/hosts if not already present
    if ! grep -q "apisrv.example.com" /etc/hosts; then
        echo "$apiserver_ip apisrv.example.com" | sudo tee -a /etc/hosts
    fi
}

setup_master_node() {
    # Configure this node as the Kubernetes master
    sudo hostnamectl set-hostname 'master'
    install_kubernetes_tools true
    run_command "sudo kubeadm config images pull"

    # Run kubeadm init and save output
    sudo kubeadm init --control-plane-endpoint 'apisrv.example.com:8443' --upload-certs --pod-network-cidr=10.244.0.0/16 | tee ~/kubeadm_init_output.txt

    # Install Flannel network plugin
    kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

    # Configure kubectl access
    mkdir -p $HOME/.kube
    sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config

    echo "Master node is configured and Flannel is installed."
}

setup_worker_node() {
    # Configure this node as a Kubernetes worker
    sudo hostnamectl set-hostname 'worker'
    install_kubernetes_tools false

    # Get kubeadm join token and discovery cert hash from user
    read -p "Please enter the kubeadm join token: " token
    read -p "Please enter the discovery-token-ca-cert-hash: " ca_cert_hash

    # Join the worker node to the cluster
    sudo kubeadm join apisrv.example.com:8443 --token "$token" --discovery-token-ca-cert-hash sha256:"$ca_cert_hash"
    echo "Worker node is configured and joined to the cluster."
}

setup_control_plane_node() {
    # Configure this node as an additional Kubernetes control plane
    sudo hostnamectl set-hostname 'control-plane'
    install_kubernetes_tools false

    # Get kubeadm token, discovery cert hash, and certificate key from user
    read -p "Please enter the kubeadm join token: " token
    read -p "Please enter the discovery-token-ca-cert-hash: " ca_cert_hash
    read -p "Please enter the certificate key: " certificate_key

    # Join the control plane node to the cluster
    sudo kubeadm join apisrv.example.com:8443 --token "$token" --discovery-token-ca-cert-hash sha256:"$ca_cert_hash" --control-plane --certificate-key "$certificate_key"
    echo "Control plane node is configured and joined to the cluster."
}

main() {
    configure_kernel_modules
    install_containerd
    disable_swap
    configure_hosts

    # Prompt user to configure master, worker, or control plane node
    echo "If this node is a master, press 1. If it's a worker, press 2. If it's a control plane node, press 3: "
    read -r node_type

    case "$node_type" in
        1) setup_master_node ;;
        2) setup_worker_node ;;
        3) setup_control_plane_node ;;
        *) echo "Invalid input. Please enter 1 for master, 2 for worker, or 3 for control plane." ;;
    esac
}

main

