# MLflow Deployment

This directory contains the MLflow deployment configuration using the community-charts/mlflow Helm chart.

## Components

- **namespace.yaml**: Creates the mlflow namespace
- **repository.yaml**: Configures the community-charts Helm repository
- **secrets.yaml**: Database credentials for connecting to PostgreSQL
- **secrets.yaml.template**: Template for creating the secrets file
- **release.yaml**: HelmRelease configuration for MLflow
- **mlflow-loadbalancer.yaml**: LoadBalancer service for external access
- **kustomization.yaml**: Kustomize configuration

## Configuration

### Database Connection
MLflow is configured to use the existing PostgreSQL deployment in the `postgres` namespace. The connection details are:
- Host: `postgres-postgresql.postgres.svc.cluster.local`
- Port: 5432
- Database: `mlflow`
- Username: `mlflow`
- Password: Stored in the `mlflow-credentials` secret

### Prerequisites
1. PostgreSQL must be running in the `postgres` namespace
2. You need to create the `mlflow` database and user in PostgreSQL
3. Update the `secrets.yaml` file with the correct credentials

### Creating the MLflow Database
Connect to your PostgreSQL instance and run:
```sql
CREATE DATABASE mlflow;
CREATE USER mlflow WITH PASSWORD 'your-password-here';
GRANT ALL PRIVILEGES ON DATABASE mlflow TO mlflow;
```

### Accessing MLflow
MLflow will be accessible via:
- Internal: `mlflow.mlflow.svc.cluster.local:5000`
- External: Through the LoadBalancer service (check `kubectl get svc -n mlflow`)

### Security
- The deployment runs as non-root user (UID 1000)
- ReadOnlyRootFilesystem is set to false as MLflow needs write access for some operations
- Resource limits are configured to prevent resource exhaustion

### Customization
You can modify the `release.yaml` file to:
- Enable authentication
- Configure S3/GCS/Azure blob storage for artifacts
- Enable ingress for custom domain access
- Adjust resource limits
- Configure autoscaling
