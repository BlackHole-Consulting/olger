#Add a new Share on computer
$shareFolder = $args[0]
$useraccess = $args[1]
$sharePath = $args[2]

if (Test-Path "$sharePath\$shareFolder")
{
    Write-Host "The shared Folder Already Exist"
} 
else{
    Write-Host $folder
    New-SmbShare -Name $shareFolder -Path $sharePath -FullAccess $useraccess
}
    