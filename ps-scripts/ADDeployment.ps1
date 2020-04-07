Import-Module ADDSDeployment
Install-ADDSForest -CreateDnsDelegation:$false -DatabasePath "C:\Windows\NTDS" -DomainMode "WinThreshold" -DomainName "vulnerable.local" -DomainNetbiosName "VULNERABLE" -LogPath "C:\Windows\NTDS" -NoRebootOnCompletion:$false -SysvolPath "C:\Windows\SYSVOL" -Force:$true

new-gpo -name "ScreenSaverTimeOut" -comment "1 hour"
Set-GPRegistryValue -Name "ScreenSaverTimeOut" -Key "HKCU\Software\Policies\Microsoft\Windows\Control Panel\Desktop" -ValueName ScreenSaveTimeOut -Type String -Value 900
New-GPLink -Name "ScreenSaverTimeOut" -Target "ou=people,dc=pagr,dc=inet"

#Cryptography Settings
#Desactivar SSLv2
New-Item 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Server' -Force
New-ItemProperty -path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Server' -name Enabled -value 0 -PropertyType DWORD

#Desactivar TLS 1.0
New-Item 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Server' -Force
New-ItemProperty -path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Server' -name Enabled -value 0 -PropertyType DWORD
New-ItemProperty -path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Server' -name DisabledByDefault -value 0 -PropertyType DWORD

#Desactivar SSLv3
New-Item 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Server' -Force
New-ItemProperty -path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Server' -name Enabled -value 0 -PropertyType DWORD

#Desactivar TLS 1.1
New-Item 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Server' -Force
New-ItemProperty -path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Server' -name DisabledByDefault -value 0 -PropertyType DWORD
New-ItemProperty -path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Server' -name Enabled -value 0 -PropertyType DWORD

#Habilitar TLS 1.2
New-Item 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Server' -Force
New-ItemProperty -path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Server' -name DisabledByDefault -value 0 -PropertyType DWORD
New-ItemProperty -path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Server' -name Enabled -value 1 -PropertyType DWORD

#Deshabilitar Hashes Debiles MD5 y SHA1
New-Item 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\MD5' -Force
New-ItemProperty -path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\MD5' -name Enabled -value 0 -PropertyType DWORD
New-Item 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\SHA' -Force
New-ItemProperty -path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\SHA' -name Enabled -value 0 -PropertyType DWORD

#Habilitar Hashes estandares SHA256, SHA384, SHA512
New-Item 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\SHA256' -Force
New-Item 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\SHA384' -Force
New-Item 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\SHA512' -Force
New-ItemProperty -path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\SHA256' -name Enabled -value 1 -PropertyType DWORD
New-ItemProperty -path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\SHA384' -name Enabled -value 1 -PropertyType DWORD
New-ItemProperty -path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\SHA512' -name Enabled -value 1 -PropertyType DWORD


#Configuraciones de Seguridad (hardening)
Set-ItemProperty -path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters" -name RequireSecuritySignature -value 1 -PropertyType DWORD
Set-ItemProperty -path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters" -name AllowGuestAuth -value 0 -PropertyValue DWORD
Set-ItemProperty -path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters" -name EnableSecuritySignature -value 1 -PropertyType DWORD
Set-ItemProperty -path "HKLM:\System\CurrentControlSet\Control\Lsa\LmCompatibilityLevel" -name LmCompatibilityLevel -value 5 -PropertyType DWORD

#Creacion de Shares
New-SmbShare -Name "VMSFiles" -Path "C:\ClusterStorage\Volume1\VMFiles" -ChangeAccess "Users" -FullAccess "Administrators"


#"\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\PolicyManager\default\LocalPoliciesSecurityOptions\NetworkSecurity_LANManagerAuthenticationLevel"
#"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\PolicyManager\default\LocalPoliciesSecurityOptions\Accounts_EnableGuestAccountStatus"
#"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\PolicyManager\default\LanmanWorkstation\EnableInsecureGuestLogons"
#"HKLM"