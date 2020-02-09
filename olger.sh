#!/usr/bin/env bash

if [ $# == 0 ]; then
    echo "Usage: $0 ip-range report_name"
    echo "* param1 example: 192.168.0.1-255"
    echo "* param2 example: home"
fi
#scan with nmap an save the results
nmap -sV -A $1 -oX data/nmap$2.xml

#convert the results to json
python3 ./bin/converter.py data/nmap$2.xml data/nmap$2.xml.json
#process the data to a json d3 graph
python olger_lib.py data/nmap$2.xml.json > reports/report$2.txt
#execute the web visualizer server
cd web
python3 -m http.server
