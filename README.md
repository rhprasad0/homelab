# Here be my Kubernetes homelab repo
![K8s Meme](welcome.png)

### GenAI statement
Anthropic's Claude model has written the vast majority of the code in this repo. Any documentation it wrote will be left intact. It knows a lot more about this stuff than I do! Vibe coding is cool, I guess.

### Set up
The Kubernetes cluster itself is comprised of 2x HP EliteDesk thin clients running k3s on Ubuntu Server in a single server-agent configuration. A k3s agent was spun up on a PC with an NVIDIA RTX 3090 so that the cluster has a GPU avaialbe for AI tasking.

A Synology NAS is also attached to the cluster for shared storage. The aformentioned hardware sits behind a router so as to segregate it from the rest of the LAN.

#### Hardware Overview

| Component | Model/Type | Role | OS | Special Features |
|-----------|------------|------|----|--------------------|
| HP EliteDesk (1) | HP EliteDesk thin client | k3s server | Ubuntu Server | Primary control plane |
| HP EliteDesk (2) | HP EliteDesk thin client | k3s agent | Ubuntu Server | Worker node |
| GPU Node | PC with NVIDIA RTX 3090 | k3s agent | Ubuntu Desktop | AI/ML workloads |
| Storage | Synology NAS | Network storage | - | Shared cluster storage |
| Network | Router | Network isolation | - | Segregates cluster from main LAN |  

GitOps is practiced via Flux so that all cluster configuration is done declaratively instead of running individual commands.

### CI/CD demonstration
The cronjob.yaml file in `dev/airthings` references the [airthings-pg repo](https://github.com/rhprasad0/airthings-pg), which is a demonstration of a CI/CD pipeline. Pushes to the main branch in that repo are automatically deployed to the cluster.

### Security
The cluster is sitting behind a double NAT set up which isolates it from the rest of the network. This was a breaking change!

Kubernetes Sealed Secrets is being used to encrypt credentials prior to being committed to this public repo. 

Claude Security Review is being tested on this repo. I wonder what suggestions it will have for us.

Tailscale is up and running on the cluster with an exit node configured so as to act as a pseudo VPN. Saves money if a VPN service is needed for security reasons while on the go.

### MLOps demonstration with MLFlow
We are working on setting up Jupyter and MLFlow and getting practice tracking training runs and deploying models to Kubernetes from the MLFlow model registry.

### Model Context Protocol Demonstration
We are deploying an LLM to the cluster via Ollama and attempting to chat with our Postgres instance using MCP. Eventually, we would also like to be able to chat with the deployed model discussed above.