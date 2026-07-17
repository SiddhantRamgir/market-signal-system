param(
    [Parameter(Mandatory = $true)]
    [string]$GitHubUsername,

    [string]$ImageTag = "v0.4.0",

    [string]$ResourceGroup = "rg-market-signal-lab",

    [string]$Location = "northeurope",

    [string]$ContainerAppName = "ca-market-signal-dashboard",

    [string]$EnvironmentName = "cae-market-signal-lab"
)

$ErrorActionPreference = "Stop"

$ImageName = "ghcr.io/$($GitHubUsername.ToLower())/market-signal-system:$ImageTag"

Write-Host "Using image: $ImageName"
Write-Host "Resource group: $ResourceGroup"
Write-Host "Location: $Location"

Write-Host "Creating resource group if it does not exist..."
az group create `
    --name $ResourceGroup `
    --location $Location `
    --output table

Write-Host "Deploying Azure Container App..."
az containerapp up `
    --name $ContainerAppName `
    --resource-group $ResourceGroup `
    --location $Location `
    --environment $EnvironmentName `
    --image $ImageName `
    --target-port 8501 `
    --ingress external `
    --env-vars `
        APP_ENV=azure-lab `
        LOG_LEVEL=INFO `
        DEFAULT_PERIOD=5d `
        DEFAULT_INTERVAL=1m `
        DEFAULT_TIMEFRAME=15min

Write-Host "Fetching application URL..."
$Fqdn = az containerapp show `
    --name $ContainerAppName `
    --resource-group $ResourceGroup `
    --query "properties.configuration.ingress.fqdn" `
    --output tsv

Write-Host ""
Write-Host "Deployment complete."
Write-Host "Dashboard URL: https://$Fqdn"