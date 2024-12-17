# Server Automation with Ansible and Docker
This repository contains an Ansible Playbook designed for automated deployment of Docker and running a containerized Nginx web server. This setup showcases the power of automation and provides a practical guide for managing infrastructure with Ansible.

### Features
- 🚀 Automated Docker Installation: Ensures Docker is installed and configured on all target servers.
- 🐳 Docker SDK Setup: Configures Python Docker SDK for smooth Docker container management.
- 📦 Nginx Container Deployment: Pulls the latest Nginx image from ArvanCloud and runs it seamlessly.
- 🔄 Idempotent Playbook: Ensures repeatability without causing configuration drift.
  
### Files
- ansible-playbook.yml: Main playbook for setting up Docker and deploying the Nginx container.

## Setup and Usage
### Prerequisites
1. Servers: Ensure you have SSH access to your servers.
2. Python: Python 3.x should be installed on the Ansible control node.
3. Ansible: Install Ansible on the control node. Use pip install ansible.

## Usage Steps
1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```
2. Define Target Servers
  Update the hosts file with your server IPs or hostnames.

3. Run the Playbook
  Execute the playbook using:
```bash
ansible-playbook -i hosts ansible-playbook.yml
```
4. Verify Deployment
  Access the deployed Nginx container via http://<server-ip>.

### Project Diagram
Below is the architecture of the automation:
The diagram shows the control node managing multiple servers for deploying Docker and running Nginx containers.

## Challenges and Goals
### Goals:
1. Streamline Docker and container deployment across multiple servers.
2. Simplify repetitive tasks with idempotent Ansible playbooks.
### Challenges:
- Setting up the Docker SDK dynamically for Python.
- Troubleshooting permission issues during automated container deployment.

## Next Steps
- Add support for custom images and environments.
- Extend the playbook to include monitoring tools like Prometheus and Grafana.
- Enable container orchestration with Kubernetes in future iterations.

## Contributing
We welcome contributions!
Feel free to fork the repo, make changes, and submit a pull request.

