#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# Visualizes the enhanced nmap results

# Copyright (c) 2015	NorthernSec
# Copyright (c)	2015	Pieter-Jan Moreels
# This software is licensed under the Original BSD License

# Imports
import os
import sys
runpath=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runpath, '..'))

try:
  from jinja2 import Environment, FileSystemLoader
  from weasyprint import HTML
except:
  sys.exit("Dependencies missing!")

from lib.Toolkit import make_dict, toHuman, fromEpoch

# Variables
env = Environment(loader=FileSystemLoader(os.path.join(runpath, '.')))
template = env.get_template("templates/pdf.html")
stylesheets = os.path.join(runpath, "static/css/pdf.css")

def pdfify(enhanced, output):
  enhanced["scan"]["time"] = fromEpoch(enhanced["scan"]["time"])
  enhanced["enhanced"]["time"] = fromEpoch(enhanced["enhanced"]["time"])
  appendixes=[]
  
  appendix = 1
  for system in enhanced["systems"]:
    if "cpes" in system:
      for cpe in system["cpes"]:
        cpe["cpe"] = toHuman(cpe["cpe"])
        if "cves" in cpe and len(cpe["cves"])!=0:
          appendixes.append(cpe["cves"])
          cpe.pop("cves")
          cpe["appendix"]=appendix
          appendix += 1
    for service in system["services"]:
      service["banner"]=product(service["banner"])
      if "cves" in service and len(service["cves"])!=0:
        appendixes.append(service["cves"])
        service["appendix"] = appendix
        appendix += 1
      if "cves" in service: service.pop("cves")

  enhanced["appendixes"]=appendixes
  html_out = template.render(enhanced)
  HTML(string=html_out).write_pdf(output, stylesheets=[stylesheets])

def product(banner):
  if banner:
    r=make_dict(banner)
    return r['product'] if 'product' in r else 'unknown'
  else:
    return "unknown"
