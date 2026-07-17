param(
    [string]$ResourceGroup = "rg-market-signal-lab",
    [string]$AlertName = "alert-market-signal-resource-health",
    [string]$ActionGroupName = "ag-market-signal-lab"
)

$ErrorActionPreference = "Stop"

$ContainerAppId = az containerapp show `
    --name ca-market-signal-dashboard `
    --resource-group $ResourceGroup `
    --query id `
    --output tsv

$ActionGroupId = az monitor action-group show `
    --name $ActionGroupName `
    --resource-group $ResourceGroup `
    --query id `
    --output tsv

if (-not $ContainerAppId) {
    throw "Container App not found."
}

if (-not $ActionGroupId) {
    throw "Action group not found."
}

Write-Host "Container App:"
Write-Host $ContainerAppId

Write-Host "Action group:"
Write-Host $ActionGroupId

az monitor activity-log alert create `
    --name $AlertName `
    --resource-group $ResourceGroup `
    --scope $ContainerAppId `
    --condition "category=ResourceHealth" `
    --action-group $ActionGroupId `
    --description "Alert on Container App resource health events." `
    --output table