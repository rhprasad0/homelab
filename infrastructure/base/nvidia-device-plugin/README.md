# NVIDIA Device Plugin for Kubernetes

![NVIDIA](https://img.shields.io/badge/NVIDIA-GPU-green?style=flat-square&logo=nvidia)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Device%20Plugin-blue?style=flat-square&logo=kubernetes)
![Flux](https://img.shields.io/badge/Flux-GitOps-purple?style=flat-square&logo=flux)

The NVIDIA device plugin for Kubernetes enables GPU support in your K3s cluster, allowing workloads to request and use NVIDIA GPUs as schedulable resources.

## 📋 Overview

This deployment includes:
- **HelmRepository**: Points to the official NVIDIA Helm chart repository
- **HelmRelease**: Deploys the device plugin with sane defaults
- **Namespace**: Isolated `nvidia-device-plugin` namespace
- **Node Feature Discovery**: Automatic GPU node detection

## 🛠️ Prerequisites

### K3s Agent Configuration

> ⚠️ **Important**: The K3s agent requires specific configuration to work with NVIDIA GPUs.

#### 1. Operating System
- **Ubuntu 22.04 LTS** (recommended)
- NVIDIA drivers properly installed

#### 2. NVIDIA Container Runtime Setup

Follow the official K3s documentation for NVIDIA container runtime configuration:
- 📖 [K3s NVIDIA Container Runtime Guide](https://docs.k3s.io/advanced#nvidia-container-runtime)

#### 3. K3s Agent Service Configuration

Edit the K3s agent service to use NVIDIA as the default runtime:

```bash
sudo systemctl edit k3s-agent
```

Add the following configuration:

```ini
[Service]
ExecStart=
ExecStart=/usr/local/bin/k3s agent --default-runtime nvidia
```

**Reference**: [K3s Discussion #9705](https://github.com/k3s-io/k3s/discussions/9705#discussioncomment-9853943)

## 🚀 Deployment

This component is automatically deployed via Flux CD as part of the base infrastructure.

### Manual Deployment (if needed)

```bash
# Apply the entire nvidia-device-plugin directory
kubectl apply -k infrastructure/base/nvidia-device-plugin/

# Or apply individual components
kubectl apply -f infrastructure/base/nvidia-device-plugin/namespace.yaml
kubectl apply -f infrastructure/base/nvidia-device-plugin/repository.yaml
kubectl apply -f infrastructure/base/nvidia-device-plugin/release.yaml
```

## 🧪 Testing GPU Availability

Create a test pod to verify GPU detection:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-test-pod
spec:
  restartPolicy: Never
  containers:
    - name: cuda-container
      image: nvcr.io/nvidia/k8s/cuda-sample:vectoradd-cuda12.5.0
      resources:
        limits:
          nvidia.com/gpu: 1 # Request 1 GPU
  tolerations:
  - key: nvidia.com/gpu
    operator: Exists
    effect: NoSchedule
```

Apply and check the results:

```bash
kubectl apply -f gpu-test-pod.yaml
kubectl logs gpu-test-pod
```

## 🔍 Verification Commands

```bash
# Check if GPUs are detected as allocatable resources
kubectl get nodes -o json | jq '.items[].status.allocatable | select(."nvidia.com/gpu")'

# List all GPU-capable nodes
kubectl get nodes -l feature.node.kubernetes.io/pci-0300_10de.present=true

# Check device plugin status
kubectl get pods -n nvidia-device-plugin

# View device plugin logs
kubectl logs -n nvidia-device-plugin -l app.kubernetes.io/name=nvidia-device-plugin
```

## ⚙️ Configuration

The HelmRelease is configured with:
- **Version**: `0.17.0`
- **Node Feature Discovery**: Enabled for automatic GPU detection
- **Basic resource limits**: Conservative CPU/memory allocation
- **Time-slicing**: Disabled by default (can be enabled for GPU sharing)

### Customization

To modify the configuration, edit `release.yaml` and uncomment/modify the values section as needed.

## 🔧 Troubleshooting

### Common Issues

1. **GPUs not detected**:
   - Verify NVIDIA drivers are installed: `nvidia-smi`
   - Check K3s agent configuration includes `--default-runtime nvidia`
   - Ensure containerd is configured for NVIDIA runtime

2. **Device plugin crashlooping**:
   - Check node labels: `kubectl get nodes --show-labels`
   - Verify GPU nodes have proper taints/tolerations
   - Check device plugin logs for specific errors

3. **Pods can't schedule on GPU nodes**:
   - Verify resource requests: `nvidia.com/gpu: 1`
   - Check node affinity and tolerations
   - Ensure GPU nodes are not cordoned

### Useful Links

- 📚 [NVIDIA Device Plugin Documentation](https://github.com/NVIDIA/k8s-device-plugin)
- 🏗️ [K3s NVIDIA Setup Guide](https://docs.k3s.io/advanced#nvidia-container-runtime)
- 🔧 [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

---

*Part of the homelab infrastructure managed by Flux CD*

Ryan wrote a bit, but Claude wrote most of this and it could be wrong!