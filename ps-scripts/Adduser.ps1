$user = args[0]
if (Get-ADUser -Filter { SamAccountName -eq $user } | Select-Object -property Enabled) {
    Write-Host "User already disabled"
}
else {
    Diasable-ADAccount -Identity $user   
}