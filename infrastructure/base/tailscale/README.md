# Tailscale Operator Setup

This directory contains the Kubernetes manifests for deploying the Tailscale operator using Flux CD.

## Overview

The Tailscale operator allows you to:
- Create Tailscale exit nodes and subnet routers
- Expose Kubernetes services via Tailscale
- Manage Tailscale resources declaratively

## Prerequisites

1. **Tailscale Account**: You need a Tailscale account and admin access
2. **OAuth Application**: Create an OAuth application in your Tailscale admin console

## Setup Instructions

### 1. Create OAuth Application

1. Go to [Tailscale Admin Console](https://login.tailscale.com/admin/settings/oauth)
2. Click "Generate OAuth Client"
3. Select the following scopes:
   - `devices:write` - Required for creating devices
   - `devices:read` - Required for reading device information
   - `routes:write` - Required if you plan to use subnet routing
   - `routes:read` - Required if you plan to use subnet routing
4. Copy both the generated client ID and client secret

### 2. Create the OAuth Secret

Before deploying, create the OAuth secret in your cluster with both credentials:

```bash
kubectl create namespace tailscale
kubectl create secret generic operator-oauth \
  --namespace tailscale \
  --from-literal=client_id=YOUR_CLIENT_ID_HERE \
  --from-literal=client_secret=YOUR_CLIENT_SECRET_HERE
```

### 3. Deploy via Flux

The operator will be automatically deployed when Flux reconciles the changes:

```bash
# Force reconciliation if needed
flux reconcile kustomization infrastructure-dev
```

### 4. Verify Installation

```bash
# Check if the operator is running
kubectl get pods -n tailscale

# Check the operator logs
kubectl logs -n tailscale deployment/tailscale-operator
```

## Usage Examples

### Expose a Service via Tailscale

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  annotations:
    tailscale.com/expose: "true"
    tailscale.com/hostname: "my-service"
spec:
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: my-app
```

### Create a Subnet Router

```yaml
apiVersion: tailscale.com/v1alpha1
kind: Connector
metadata:
  name: sample-connector
spec:
  subnetRouter:
    advertiseRoutes:
    - "10.0.0.0/8"
```

### Create an Exit Node

```yaml
apiVersion: tailscale.com/v1alpha1
kind: Connector
metadata:
  name: exit-node
spec:
  exitNode: true
```

## Configuration

The operator configuration can be customized in the `release.yaml` file. Key configuration options include:

- **Resources**: CPU and memory limits/requests
- **Security Context**: Pod and container security settings
- **Node Selector**: Control which nodes the operator runs on
- **Tolerations**: Allow scheduling on tainted nodes

## Troubleshooting

### Common Issues

1. **OAuth Secret Missing**: Ensure the `operator-oauth` secret exists in the `tailscale` namespace
2. **RBAC Errors**: The operator needs cluster-admin permissions to manage Tailscale resources
3. **Network Policies**: Ensure the operator can reach the Tailscale API (443/tcp)

### Useful Commands

```bash
# Check operator status
kubectl get deployment -n tailscale tailscale-operator

# View operator logs
kubectl logs -n tailscale deployment/tailscale-operator -f

# List Tailscale resources
kubectl get connectors -A
kubectl get services -A -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.annotations.tailscale\.com/expose}{"\n"}{end}'
```

## Resources

- [Tailscale Kubernetes Operator Documentation](https://tailscale.com/kb/1236/kubernetes-operator)
- [Tailscale Helm Chart](https://github.com/tailscale/tailscale/tree/main/cmd/k8s-operator/deploy/chart)
- [OAuth Application Setup](https://tailscale.com/kb/1215/oauth-clients)
