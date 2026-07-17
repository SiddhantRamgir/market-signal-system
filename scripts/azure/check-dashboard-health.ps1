param(
    [string]$ResourceGroup = "rg-market-signal-lab",
    [string]$ContainerAppName = "ca-market-signal-dashboard"
)

$ErrorActionPreference = "Stop"

$Fqdn = az containerapp show `
    --name $ContainerAppName `
    --resource-group $ResourceGroup `
    --query "properties.configuration.ingress.fqdn" `
    --output tsv

if (-not $Fqdn) {
    throw "Could not find FQDN for $ContainerAppName"
}

$HealthUrl = "https://$Fqdn/_stcore/health"

Write-Host "Checking health endpoint:"
Write-Host $HealthUrl

try {
    $Response = Invoke-WebRequest `
        -Uri $HealthUrl `
        -TimeoutSec 10 `
        -UseBasicParsing

    if ($Response.StatusCode -eq 200 -and $Response.Content -match "ok") {
        Write-Host "HEALTHY"
        exit 0
    }

    Write-Host "UNHEALTHY: Unexpected response"
    Write-Host "Status code: $($Response.StatusCode)"
    Write-Host "Content: $($Response.Content)"
    exit 1
}
catch {
    Write-Host "UNHEALTHY: $($_.Exception.Message)"
    exit 1
}