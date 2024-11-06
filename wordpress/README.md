# Using Kubernetes Secrets for MySQL Password Management 🔒

![1](https://github.com/user-attachments/assets/58745fb2-80b1-4860-b512-ea7dd6c70037)


**In this setup, we leverage Kubernetes Secrets to securely store the MySQL root password, avoiding plain text exposure in configuration files. Kubernetes Secrets are a secure way to handle sensitive data like passwords, API keys, and other confidential information in your cluster.**

## Step-by-Step Guide

### 1. Create a Secret in Kubernetes

Start by creating a Secret in Kubernetes to securely hold the MySQL root password. This can be done with a YAML file or directly via the `kubectl` command.

**Example command:**
```bash
kubectl create secret generic mysql-pass --from-literal=password=YOUR_PASSWORD_HERE
```
### In this example:
- mysql-pass is the name of the Secret.
- password is the key that holds the actual MySQL root password.

### 2. Using the Secret in a Deployment
To ensure that MySQL accesses the password from the Secret, reference it in the Deployment configuration under the environment variables.

Example configuration in mysql-deployment.yaml:

```yaml
env:
  - name: MYSQL_ROOT_PASSWORD
    valueFrom:
      secretKeyRef:
        name: mysql-pass
        key: password
```
Here, the MYSQL_ROOT_PASSWORD environment variable in the MySQL Pod will take its value from the mysql-pass Secret.

## Best Practices for Secrets Avoid Plain Text Exposure:
- Always use Secrets for sensitive data to avoid putting passwords or other confidential information directly in YAML files.
- RBAC for Secrets: Ensure only authorized users have access to Secrets by setting up Role-Based Access Control (RBAC).
- Encrypt at Rest: If your Kubernetes distribution supports it, enable encryption of Secrets at rest.

## Commands Summary
### Create a Secret:
```bash
Copy code
kubectl create secret generic <secret-name> --from-literal=<key>=<value>
```
### View Secret Metadata (without exposing sensitive data):
```bash
Copy code
kubectl get secret <secret-name> -o yaml
```
### Delete a Secret:
```bash
Copy code
kubectl delete secret <secret-name>
```
## Why Use Kubernetes Secrets?
Using Kubernetes Secrets improves security by allowing you to:

- Avoid hard-coding sensitive information in application configurations.
- Control access to sensitive information through Kubernetes RBAC.
- Securely manage the lifecycle of confidential data within the cluster.

### Technologies Used
- Kubernetes Secrets: For managing sensitive data.
- Kubernetes RBAC: (Optional) To control access to Secrets.
