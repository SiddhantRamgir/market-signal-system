variable "resource_group_name" {
  description = "Name of the Azure resource group used for the lab."
  type        = string
  default     = "rg-market-signal-tf-lab"
}

variable "location" {
  description = "Azure region for the lab resources."
  type        = string
  default     = "northeurope"
}

variable "log_analytics_workspace_name" {
  description = "Name of the Log Analytics workspace."
  type        = string
  default     = "law-market-signal-tf-lab"
}

variable "container_app_environment_name" {
  description = "Name of the Azure Container Apps environment."
  type        = string
  default     = "cae-market-signal-tf-lab"
}

variable "container_app_name" {
  description = "Name of the Azure Container App."
  type        = string
  default     = "ca-market-signal-dashboard"
}

variable "github_username" {
  description = "GitHub username that owns the GHCR image."
  type        = string
}

variable "image_tag" {
  description = "Container image tag to deploy."
  type        = string
  default     = "v0.4.0"
}

variable "app_env" {
  description = "Application environment name."
  type        = string
  default     = "azure-terraform-lab"
}

variable "log_level" {
  description = "Application log level."
  type        = string
  default     = "INFO"
}

variable "default_period" {
  description = "Default yfinance data period."
  type        = string
  default     = "5d"
}

variable "default_interval" {
  description = "Default yfinance data interval."
  type        = string
  default     = "1m"
}

variable "default_timeframe" {
  description = "Default signal timeframe."
  type        = string
  default     = "15min"
}

variable "container_cpu" {
  description = "CPU allocation for the dashboard container."
  type        = number
  default     = 0.25
}

variable "container_memory" {
  description = "Memory allocation for the dashboard container."
  type        = string
  default     = "0.5Gi"
}

variable "tags" {
  description = "Common Azure resource tags."
  type        = map(string)

  default = {
    project     = "market-signal-system"
    environment = "lab"
    managed_by  = "terraform"
  }
}