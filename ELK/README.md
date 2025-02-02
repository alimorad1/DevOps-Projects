# ELK Stack on Kubernetes
![image](https://github.com/user-attachments/assets/5903c09b-1709-448a-a15a-c7840ace1144)

This repository contains the configuration and setup for deploying the ELK Stack (Elasticsearch, Logstash, and Kibana) on a Kubernetes cluster. This setup aims to provide a fully functional logging and monitoring system within a production-like environment, suitable for handling logs and metrics in real-world use cases.

## Components
- Elasticsearch: A distributed, RESTful search and analytics engine for storing and querying logs and data.
- Logstash: A data processing pipeline that ingests, transforms, and sends logs to Elasticsearch.
- Kibana: A data visualization platform that works with Elasticsearch to provide real-time dashboards and insights from log data.

## Requirements
- A Kubernetes cluster (could be managed or self-hosted).
- kubectl: A command-line tool for interacting with Kubernetes clusters.
- Helm (optional): A package manager for Kubernetes, which simplifies deployment and management of ELK components.

## Setup
### 1. Deploy Elasticsearch
To deploy Elasticsearch on your Kubernetes cluster:

```bash
helm repo add elastic https://helm.elastic.co
helm install elasticsearch elastic/elasticsearch
```
### 2. Deploy Logstash
To deploy Logstash:

```bash
helm install logstash elastic/logstash
```
### 3. Deploy Kibana
To deploy Kibana:

```bash
helm install kibana elastic/kibana
```
### 4. Verify Deployment
After the installation, check if the ELK components are running successfully:

```bash
kubectl get pods
```
### 5. Access Kibana
To access the Kibana dashboard, you can expose the service or use port-forwarding:

```bash
kubectl port-forward service/kibana 5601:5601
```
Then, open your browser and navigate to http://localhost:5601 to access the Kibana UI.

## Configuration
Configuration files for each ELK component are provided in this repository. You can customize settings such as Elasticsearch resource limits, Logstash pipeline configurations, and Kibana dashboards by modifying the values.yaml or respective configuration files.
### Example configuration for Logstash:
```yaml
input {
  file {
    path => "/var/log/**/*.log"
    type => "syslog"
  }
}
```
### Example configuration for Elasticsearch:
```yaml
cluster:
  name: "my-cluster"
  node:
    name: "elasticsearch-node-1"
```

## Usage
- Kibana: Use Kibana to create dashboards and visualize logs stored in Elasticsearch.
- Logstash: Configure Logstash pipelines to collect logs from various sources (e.g., system logs, application logs) and send them to Elasticsearch.
- Elasticsearch: Store logs and use powerful search capabilities to analyze log data in real-time.

## Contributing
Feel free to fork this repository, submit issues, or open pull requests. Contributions to improve the setup or add additional features are welcome!

## License
This project is licensed under the MIT License.
