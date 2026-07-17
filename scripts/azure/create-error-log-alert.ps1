param(
    [string]$ResourceGroup = "rg-market-signal-lab",
    [string]$AlertName = "alert-market-signal-errors",
    [string]$ActionGroupName = "ag-market-signal-lab",
    [string]$Location = "northeurope"
)

$ErrorActionPreference = "Stop"

$WorkspaceResourceId = az monitor log-analytics workspace list `
    --resource-group $ResourceGroup `
    --query "[0].id" `
    --output tsv

$ActionGroupId = az monitor action-group show `
    --name $ActionGroupName `
    --resource-group $ResourceGroup `
    --query id `
    --output tsv

if ([string]::IsNullOrWhiteSpace($WorkspaceResourceId)) {
    throw "No Log Analytics workspace resource ID found."
}

if ([string]::IsNullOrWhiteSpace($ActionGroupId)) {
    throw "Action group not found."
}

$Query = "union isfuzzy=true ContainerAppConsoleLogs, ContainerAppConsoleLogs_CL | where TimeGenerated > ago(5m) | extend Message = strcat(tostring(column_ifexists('Log', '')), ' ', tostring(column_ifexists('Log_s', ''))) | where Message has 'ERROR' or Message has 'Exception' or Message has 'Traceback' or Message has 'Internal Server Error'"

Write-Host "Workspace:"
Write-Host $WorkspaceResourceId

Write-Host "Action group:"
Write-Host $ActionGroupId

Write-Host "Query:"
Write-Host $Query

Write-Host "Deleting old alert if it exists..."
az monitor scheduled-query delete `
    --name $AlertName `
    --resource-group $ResourceGroup `
    --yes 2>$null

Write-Host "Creating alert..."

az monitor scheduled-query create `
    --name $AlertName `
    --resource-group $ResourceGroup `
    --location $Location `
    --scopes $WorkspaceResourceId `
    --description "Alert when market signal app writes error logs." `
    --condition "count 'ErrorLogs' > 0" `
    --condition-query "ErrorLogs=$Query" `
    --evaluation-frequency 5m `
    --window-size 5m `
    --severity 2 `
    --action-groups $ActionGroupId `
    --auto-mitigate true `
    --output json