<#
    .SYNOPSIS
        This Script runs on master head node start, it is used in the ARM template to store the storage account name, key etc.
        It saves the result to local disk and restarts the main nodeJS controller process running on the VM.
#>

Param (
    [Parameter(Mandatory=$true)]
    [String]$storageAccountName,
    [Parameter(Mandatory=$true)]
    [String]$resourceGroup,
    [Parameter(Mandatory=$true)]
    [String]$subscriptionID,
    [Parameter(Mandatory=$true)]
    [String]$enableSSL,
    [Parameter(Mandatory=$true)]
    [String]$certFile,
    [Parameter(Mandatory=$true)]
    [String]$privateKeyFile,
    [Parameter(Mandatory=$true)]
    [String]$fqdn
)

$myObj = New-Object System.Object

$myObj | Add-Member -type NoteProperty -name storageAccountName -value $storageAccountName
$myObj | Add-Member -type NoteProperty -name resourceGroup -value $resourceGroup
$myObj | Add-Member -type NoteProperty -name subscriptionID -value $subscriptionID
$myObj | Add-Member -type NoteProperty -name enableSSL -value $enableSSL
$myObj | Add-Member -type NoteProperty -name certFile -value $certFile
$myObj | Add-Member -type NoteProperty -name privateKeyFile -value $privateKeyFile
$myObj | Add-Member -type NoteProperty -name fqdn -value $fqdn

$Utf8NoBomEncoding = New-Object System.Text.UTF8Encoding $False

$myContent = $myObj | ConvertTo-Json -Depth 100 
$myPath = "c:\\MathWorks\\controller\\config\\dynamicOptions.json"
[System.IO.File]::WriteAllLines($myPath, $myContent, $Utf8NoBomEncoding)

# stop windows services from using port 80
net stop http /y

# Start the main service that performs bootstrapping and attaching the file share
Start-Process -FilePath "node" -ArgumentList("c:\\MathWorks\\controller\\index.js")