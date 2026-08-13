output "resource_group_name" {
  description = "Resource group created by Terraform."
  value       = azurerm_resource_group.main.name
}

output "container_app_name" {
  description = "Container App name."
  value       = azurerm_container_app.dashboard.name
}

output "container_image" {
  description = "Container image deployed."
  value       = local.image_name
}

output "container_app_latest_revision_fqdn" {
  description = "Latest revision FQDN for the Container App."
  value       = azurerm_container_app.dashboard.latest_revision_fqdn
}