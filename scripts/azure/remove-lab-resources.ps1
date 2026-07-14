param(
    [string]$ResourceGroup = "rg-market-signal-lab"
)

$ErrorActionPreference = "Stop"

Write-Host "This will delete the entire Azure resource group: $ResourceGroup"
Write-Host "All resources inside it will be removed."

$Confirmation = Read-Host "Type DELETE to continue"

if ($Confirmation -ne "DELETE") {
    Write-Host "Deletion cancelled."
    exit 0
}

az group delete `
    --name $ResourceGroup `
    --yes `
    --no-wait

Write-Host "Delete request submitted for resource group: $ResourceGroup"
Write-Host "Check Azure Portal to confirm removal."