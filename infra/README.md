# Azure Deployment Guide - Terraform

Deploy the Larvixon Patients Service to Azure Container Apps.

## Prerequisites

* **Azure CLI** installed and logged in (`az login`).
* **Terraform** installed.
* **Docker** installed and running.
* **Registered Providers** (Run once per subscription):

    ```bash
    az provider register -n Microsoft.App
    az provider register -n Microsoft.OperationalInsights
    az provider register -n Microsoft.ContainerRegistry
    ```

## Quick Start (Local Build Method)

To avoid deployment errors, we follow a 3-step process: **Infrastructure (Base) -> Build Image -> Infrastructure (App)**.

### 1. Initialize & Configure

```bash
cd infra/terraform
terraform init
cp terraform.tfvars.example terraform.tfvars
# Update 'image_tag' in terraform.tfvars to match your local tag (e.g., "v1")
```

### 2. Create the Registry First

We need the registry to exist before we can push images to it.

```bash
terraform apply -target=azurerm_container_registry.main
```

### 3. Build & Push Image (Locally)

**Important:** We build locally to bypass Azure Free Tier restrictions on cloud builds.

```bash
# Variables
ACR_NAME="larvixonpatientsdevacr" # Check your terraform output or vars
TAG="v1"                          # Must match var.image_tag in terraform.tfvars

# Login & Push
az acr login --name $ACR_NAME
docker build -t $ACR_NAME.azurecr.io/patients-service:$TAG ../..
docker push $ACR_NAME.azurecr.io/patients-service:$TAG
```

### 4. Deploy the Service

Now that the image exists, deploy the Container App.

```bash
terraform apply
```

## CI/CD Secrets (GitHub Actions)

If connecting to GitHub Actions later, configure these secrets:
`AZURE_CREDENTIALS`, `ACR_LOGIN_SERVER`, `ACR_USERNAME`, `ACR_PASSWORD`, `AZURE_RESOURCE_GROUP`, `CONTAINER_APP_NAME`.
