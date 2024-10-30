# Kubernetes Firewall Configuration on Ubuntu

**Hey! One key thing to keep in mind when setting up Kubernetes is security. It's important to follow organizational policies while ensuring Kubernetes functions smoothly. Here’s a firewall configuration I put together to help with that!**

![1](https://github.com/user-attachments/assets/8e738865-0bb7-49a4-bd3e-1aec63ba84dc)

In Ubuntu, you can configure the firewall with `ufw` (Uncomplicated Firewall) to open the necessary ports for Kubernetes components.

## Required Ports

### Master Node
- **TCP 6443**: Kubernetes API server
- **TCP 2379-2380**: etcd (for multi-control-plane clusters)
- **TCP 10250**: kubelet API
- **TCP 10251**: kube-scheduler
- **TCP 10252**: kube-controller-manager

### Worker Nodes
- **TCP 10250**: kubelet API
- **TCP 30000-32767**: NodePort range (default for services)

## Firewall Configuration Commands

To open these ports, use the following `ufw` commands:

```bash
# For Master Node:
sudo ufw allow 6443/tcp
sudo ufw allow 2379:2380/tcp
sudo ufw allow 10250/tcp
sudo ufw allow 10251/tcp
sudo ufw allow 10252/tcp

# For Worker Node:
sudo ufw allow 10250/tcp
sudo ufw allow 30000:32767/tcp

# Enable UFW (if it’s not enabled yet):
sudo ufw enable

