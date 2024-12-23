# 🚀 Quick Start with PromQL
PromQL (Prometheus Query Language) is a powerful yet simple language designed to query and analyze the metrics collected by Prometheus. If you’re looking to dive deep into your system’s data or build impressive dashboards, PromQL is your go-to tool!

## 📌 Quick Examples:
### 1️⃣ Basic Metric Query:

```promql
node_cpu_seconds_total
```
- This displays the total CPU usage time (in seconds).

### 2️⃣ Calculate Rate:

```promql
rate(node_cpu_seconds_total[5m])
```
- Calculates the rate of CPU usage over the last 5 minutes — perfect for live monitoring!

### 3️⃣ Filter by Labels:

```promql
node_memory_MemFree_bytes{instance="192.168.49.2:30002"}
```
- Filters and shows free memory for a specific server.

### 4️⃣ Aggregate Across Metrics:

```promql
sum(rate(node_network_receive_bytes_total[5m]))
```
- Sums up the total network received bytes across all interfaces.

### 💡 Pro Tips for PromQL:
1. Use [ ] to specify time ranges like [5m], [1h], etc.
2. Leverage aggregation functions like sum, avg, max, and min.
3. Labels ({key="value"}) are your best friends for filtering data effectively.

### 🌟 Why Learn PromQL?
- Gain deep insights into your system’s behavior.
- Create robust dashboards in Grafana.
- Detect and debug issues faster than anyone else.

#### Thank you for your attention...
