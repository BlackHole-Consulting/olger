#Install new Active Directory with DNS

$domain_name = args[0]

Install-WindowsFeature ADDomain-Services -IncludeManagementTools
Install-ADDSForest -DomainName $domain_name -InstallDns


#Si se instala un dns aparte escuchar peticiones solamente de cierta maquina
Add-WindowsFeature -Name DNS, RSAT-DNS-Server -IncludeAllSubFeature
$DnsObj = Get-DNSServerSetting -ComputerName $env:computername -All 
#sentencia de escucha en una dirección ip especifica
$DnsObj.ListeningIPAddress = @{$ipaddress}
Set-DnsServerSetting -InputObject $DnsObj

# Deshabilitar la recursión de los DNS
Set-DnsRecursion -ComputerName $env:computername -Enable $false
$SecDNS = "156.154.70.4"

Add-DnsForwarder -IPAddress $SecDNS -ComputerName $env:computername

#set records, only if there is AD setted up
#Add-DnsServerResourceRecordA -IPv4Address $ipaddress -Name "resource_name" -ZoneName $domain_name
#we can add more records changing the A in the end of the cmdlet
#Consutla de cmdlets  Get-Command -Module DnsServer -Name *ResourceRecord*