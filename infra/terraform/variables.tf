variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "larvixon-patients"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "West Europe"
}

variable "image_name" {
  description = "Name of the container image"
  type        = string
  default     = "patients-service"
}

variable "image_tag" {
  description = "Tag of the container image"
  type        = string
  default     = "latest"
}

variable "container_cpu" {
  description = "CPU allocation for the container"
  type        = number
  default     = 0.25
}

variable "container_memory" {
  description = "Memory allocation for the container"
  type        = string
  default     = "0.5Gi"
}

variable "min_replicas" {
  description = "Minimum number of container replicas"
  type        = number
  default     = 0
}

variable "max_replicas" {
  description = "Maximum number of container replicas"
  type        = number
  default     = 3
}

locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
    Service     = "patients-service"
  }
}
