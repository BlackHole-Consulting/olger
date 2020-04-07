$nombre = $args[0]
$apellido = $args[1]
$email = $args[2]
$user = $args[3]
$pass = $args[4]
$ou = $args[5]
$eid = $args[6]
$company = 'example.org'

if ([bool] (Get-ADUser -Filter { SamAccountName -eq $user })) {
    Write-Host "The user already exist"
}
else {
    New-ADUser -Name $nombre -Surname $apellido -EmailAddress $email -Path $ou -Company $company -EmployeeID $eid -AccountPassword $pass -ChangePasswordAtLogon -Enabled -KerberosEncriptionType AES256    
}
