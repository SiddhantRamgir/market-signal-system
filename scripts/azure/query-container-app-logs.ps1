param(
    [string]$ResourceGroup = "rg-market-signal-lab",
    [int]$Hours = 1
)

$ErrorActionPreference = "Stop"

$WorkspaceId = az monitor log-analytics workspace list `
    --resource-group $ResourceGroup `
    --query "[0].customerId" `
    --output tsv

if (-not $WorkspaceId) {
    throw "No Log Analytics workspace found in resource group $ResourceGroup"
}

Write-Host "Workspace ID: $WorkspaceId"
Write-Host ""

Write-Host "Latest container logs:"
az monitor log-analytics query `
    --workspace $WorkspaceId `
    --analytics-query "union isfuzzy=true ContainerAppConsoleLogs, ContainerAppConsoleLogs_CL | where TimeGenerated > ago(${Hours}h) | order by TimeGenerated desc | take 20" `
    --output table

Write-Host ""
Write-Host "Recent error logs:"
az monitor log-analytics query `
    --workspace $WorkspaceId `
    --analytics-query "union isfuzzy=true ContainerAppConsoleLogs, ContainerAppConsoleLogs_CL | where TimeGenerated > ago(${Hours}h) | where Log_s has 'ERROR' or Log_s has 'Exception' or Log_s has '""level"":""ERROR""' | order by TimeGenerated desc | take 20" `
    --output table