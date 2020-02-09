#!/usr/bin/env python
#====================================================================================
#  OLGER NETWORK MAPPING AND VULNERABILITY SCANNER 
#====================================================================================
# MADE WITH D3.JS , KIBANA, ELASTICSEARCH,  GRAPH, GRAPHVIZ
#====================================================================================
# Authors Pedro El Banquero 
#====================================================================================


from datetime import datetime
from elasticsearch import Elasticsearch
import json
import time
import codecs
import struct
import locale
import glob
import sys
import getopt
import xml.etree.ElementTree as xml
import re
import os
import xmltodict
from collections import Counter
import json

import urllib
import argparse
import subprocess

def elkpush(indexdat,jsondat):

        es = Elasticsearch(
                ['host.domain'],
                scheme="https",
                verify_certs=False,
                http_auth=('elastic', 'auth-key'),
		port=9200
	)
	print(es.index(index=indexdat,doc_type="security_report", body=json.dumps(jsondat)))

port=""
nameport=""
version=""
product=""
cves=""
os2=""
address=""
timestamp=""
cpe=""
cvecount=0
inventory_by_product={}

def filter(ini_string):
    result = re.sub('[\W_]+', '', ini_string) 
    return result.strip(',.').lower()

def olger_parser():
    f = open(sys.argv[1])
    xml_content = f.read()
    print (xml_content)
    f.close()
    dat=(json.loads(xml_content))

    timestamp=datetime.fromtimestamp(float(dat["scan"]["time"]))
    print (timestamp)
    dateelastic=str(str(timestamp).split(" ")[0])+"T"+str(str(timestamp).split(" ")[1])+"Z"
    address=""
    plist=""
    cvelist={}
    graph={}
    nodes=[]
    links=[]
    id=0
    for x in dat["systems"]:
        if "up" in x["status"]:
            
            
            nodes.append({"id":str(id)+""+str(x["ip"]),"host":str(id)+""+str(x["ip"])})
            
            for e in x["services"]:
                if "open" in e["state"]: 
                    #print e

                    try:
                        product=e["banner"].split("product: ")[1]
                        try:
                            product = product.split("version: ")[0]
                        except:
                            pass
                        
                        try:
                            product = product.split("ostype: ")[0]
                        except:
                            pass

                        try:
                            product = product.split("hostname: ")[0]
                        except:
                            pass

                        product=product.strip()
                    except:
                        pass
                        product=""
                    
                    
                    try:
                        version=e["banner"].split("product: ")[1].split("version: ")[1]
                        try:
                            version = version.split("ostype: ")[0]
                        except:
                            pass
                        try:
                            version = version.split("hostname: ")[0]
                        except:
                            pass
                        try:
                            version = version.split("extrainfo: ")[0]
                        except:
                            pass

                        version = version.strip()
                    except:
                        pass
                        version=""
                    os2=""
                    try:
                        os2=e["banner"].split("ostype: ")[1]
                        try:
                            os2 = os.split("devicetype: ")[0]
                        except:
                            pass
                            os2=""
                    except:
                        pass
                        os2=""
                    
                    try:
                        cpe=e["cpe"]
                    except:
                        pass
                        cpe=""
                    cves=""
                    cvecount="0"
                    print(cpe)
                    #try:
                    cvelist=""
                    csv_content=""
                    cvecount=0
                    csv_content=""
                    f = open("cvedata.csv", "w")
                    f.write(str(""))
                    f.close()
                    if product !="" and version != "":
                        print("CHEKING CVES ...")

                        os.system("python3 cvedetails-lookup.py --csv cvedata.csv --product \""+product+"\" --version \""+version+"\"")
                        try:

                            os.system("python3 cvedetails-lookup.py --csv cvedata.csv --product \""+product+"\" --version \""+version+"\"")
                            f = open("cvedata.csv")
                            csv_content = f.read()
                            f.close()
                            cvecount=len(str(csv_content).split("\n"))
                            cvelist=""
                            for x2 in str(csv_content).split("\n"):


                                cvelist=x2.split(";")[0]+","+cvelist
                            print(cvelist)
                        except:
                            pass
                    



                    nodes = {v['id']:v for v in nodes}.values()
                    #uncomment this line to send data to elastic  
                    #toelastic={"customer":sys.argv[2],"timestamp":dateelastic,"address":x["ip"],"domains":"","lat":"","long":"","os":os,"port":str(e["port"]),"portname":str(e["name"]),"product":str(product),"version":str(version),"cpe":str(cpe),"cves":str(cvelist[product]),"cvecount":int(cvecount)}
                    if str(e["port"]) !="":
                        links.append({"source":str(id)+""+str(x["ip"]),"target":str(id)+""+str(e["port"]), "value":"port"})
                        
                        nodes.append({"id":str(id)+""+str(e["port"]),"host":str(id)+""+str(e["port"])})

                    if str(e["name"]) !="":

                        nodes.append({"id":str(id)+""+str(e["name"]),"host":str(e["name"])})

                        links.append({"source":str(id)+""+str(x["ip"]),"target":str(id)+""+str(e["name"]), "value":"portname"})

                    print "product : "+filter(str(product))
                    if str(product) !="":
                        print filter(str(product))

                        print str(x["ip"])
                        
                        nb=filter(str(product))
                        try:
                            inventory_by_product[nb][id]=str(x["ip"])
                        except:
                            inventory_by_product[nb]={}
                            inventory_by_product[nb][id]=str(x["ip"])
                            pass

                        nodes.append({"id":str(id)+""+str(product),"host":str(product)})
                        links.append({"source":str(id)+""+str(x["ip"]),"target":str(id)+""+str(product), "value":"product"})
                    if str(version) !="":
                        nodes.append({"id":str(id)+""+str(version),"host":str(version)})
                        links.append({"source":str(id)+""+str(version),"target":str(id)+""+str(version), "value":"version"})
                    if str(os2) !="":
                        nodes.append({"id":str(id)+""+str(os2),"host":str(os2)})
                        links.append({"source":str(id)+""+str(x["ip"]),"target":str(os2), "value":"OS"})
                    
                    if str(cvelist) !="":
                        try:
                            nodes.append({"id":str(id)+""+str(cvelist),"host":str(cvelist)})
                            links.append({"source":str(id)+""+str(x["ip"]),"target":str(id)+""+str(cvelist), "value":"cves"})
                        except:
                            pass
                    

                    #print(toelastic)
                    #send data to elastic
                    #print(elkpush("box_"+sys.argv[2],toelastic))
                    id=id+1
            graph={"nodes": nodes,"links":links}

 
    data_grouped=""
    i=0
    for a in inventory_by_product:
        print "\n"+a+"\n"
        data_grouped = data_grouped+"\n\n["+a+"]\n\n"
        for b in inventory_by_product[a]:
            print b
            data_grouped=data_grouped+"\n"+inventory_by_product[a][b]+"\n"
            i=i+1

    f = open("inventory", "w")
    f.write(str(data_grouped))
    f.close()
    with open("web/graphs/data.json", 'w') as outfile:
        json.dump(graph, outfile)

        

olger_parser()