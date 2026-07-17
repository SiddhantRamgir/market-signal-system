param(
    [string]$ResourceGroup = "rg-market-signal-lab",
    [string]$ContainerAppName = "ca-market-signal-dashboard"
)

$ErrorActionPreference = "Stop"

Write-Host "Container App status:"
az containerapp show `
    --name $ContainerAppName `
    --resource-group $ResourceGroup `
    --query "{name:name, location:location, provisioningState:properties.provisioningState, fqdn:properties.configuration.ingress.fqdn}" `
    --output table

Write-Host ""
Write-Host "Revisions:"
az containerapp revision list `
    --name $ContainerAppName `
    --resource-group $ResourceGroup `
    --query "[].{name:name, active:properties.active, trafficWeight:properties.trafficWeight, createdTime:properties.createdTime}" `
    --output table