# Sealed Secrets

This directory contains the Flux configuration for installing [Sealed Secrets](https://sealed-secrets.netlify.app/) in your Kubernetes cluster.

## What is Sealed Secrets?

Sealed Secrets is a Kubernetes controller and tool for one-way encrypted Secrets. It allows you to store encrypted secrets in Git repositories and have them automatically decrypted by the controller when applied to the cluster.

## Installation

The Sealed Secrets controller will be automatically installed when you apply your Flux configuration. It includes:

- **Namespace**: `sealed-secrets`
- **Controller**: Deployed in the `sealed-secrets` namespace
- **RBAC**: Proper role-based access control
- **Monitoring**: Ready for Prometheus integration (disabled by default)

## Usage

### 1. Install the kubeseal CLI tool

You'll need the `kubeseal` command-line tool to create sealed secrets:

```bash
# On Linux
wget https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.5/kubeseal-0.24.5-linux-amd64.tar.gz
tar -xvzf kubeseal-0.24.5-linux-amd64.tar.gz kubeseal
sudo install -m 755 kubeseal /usr/local/bin/kubeseal

# Or using Homebrew (macOS/Linux)
brew install kubeseal
```

### 2. Create a sealed secret

```bash
# Create a regular Kubernetes secret (don't apply it!)
kubectl create secret generic mysecret --dry-run=client --from-literal=username=myuser --from-literal=password=mypassword -o yaml > mysecret.yaml

# Seal the secret
kubeseal -f mysecret.yaml -w mysealedsecret.yaml

# Clean up the unencrypted secret
rm mysecret.yaml

# Now you can safely commit mysealedsecret.yaml to Git
git add mysealedsecret.yaml
git commit -m "Add sealed secret"
```

### 3. Alternative: Create sealed secret directly

```bash
# Create sealed secret directly from command line
echo -n mypassword | kubectl create secret generic mysecret --dry-run=client --from-file=password=/dev/stdin -o yaml | kubeseal -w mysealedsecret.yaml
```

### 4. Apply the sealed secret

```bash
kubectl apply -f mysealedsecret.yaml
```

The Sealed Secrets controller will automatically decrypt the sealed secret and create the corresponding Kubernetes secret in your cluster.

## Security Notes

- The private key used for decryption is stored in the cluster and never leaves it
- Sealed secrets can only be decrypted by the specific cluster they were created for
- Sealed secrets are bound to the namespace they were created for (by default)
- You can safely store sealed secrets in Git repositories

## Monitoring

To enable Prometheus monitoring, edit `release.yaml` and set:

```yaml
values:
  metrics:
    serviceMonitor:
      enabled: true
```

## Troubleshooting

Check the controller logs:
```bash
kubectl logs -n sealed-secrets -l name=sealed-secrets-controller
```

Verify the controller is running:
```bash
kubectl get pods -n sealed-secrets
```
