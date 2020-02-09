## What olger does

Olger make a network scan parse the data ans send to elastic search, make a scan report in txt .

Local python webserver in localhost for graph visualization with D3.js .

Uses cvdetails.com to identiy Cyber Security Vulnerabilities .

Sends data to elastichsearch and visualizes data in kibana .

Search vulnerabilities in www.cvdetails.com

Cooming soon complete report in pdf and network diagram in pdf with vulnerability checks

## How

Runnig this is as easy as:

#### Nmap Your Target:
`
 ./olger.sh 192.168.0.1-255 name-mission

## How it looks

Explore the network with browser view and D3.js Graph

![image olger graph d3 js](olger.png)


Make a plain text report with cvdetails connection

![image olger report vulnerabilities CVE](report.png)


Send data to elastic search and import our Dashboard in KIBANA

![image olger relastic search and kibana](kibana.png)
