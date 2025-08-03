# Here be my Kubernetes homelab repo
Very tinker, much learn

![K8s Meme](welcome.png)

The cluster itself is comprised of 2x HP EliteDesk thin clients running k3s on Ubuntu Server in a single server-agent configuration. a Synology NAS is also attached to the cluster for shared storage. GitOps is practiced via Flux so that all cluster configuration is done declaratively instead of running individual commands.  

Currently looking at spinning up a Spark cluster for MLOps related experiments.