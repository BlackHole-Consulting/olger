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

import argparse
import json

visuals={'web':  {'import': 'from lib.WebDisplay import WebDisplay',
                  'exec':   'WebDisplay.start(scan=data)'},
         'term': {'import': 'from lib.TermDisplay import TermDisplay',
                  'exec':   'TermDisplay.start(scan=data)'},
         'pdf':  {'import': 'from lib.PDFParser import pdfify',
                  'exec':   'pdfify(data, args.p)'}                  }

def filtersFromArgs(args):
  # populate filters
  filters={'access':[],'impact':[]}
  if args.fL:  filters['access'].append('LOCAL')
  if args.fAN: filters['access'].append('ADJECENT_NETWORK')
  if args.fN:  filters['access'].append('NETWORK')
  if args.fC:  filters['impact'].append('confidentiality')
  if args.fI:  filters['impact'].append('integrity')
  if args.fA:  filters['impact'].append('availability')
  return filters

def filter(vulns, exploitsOnly=False, filters={}):
  if 'access' in filters and len(filters['access'])!=0:  # access filters
    vulns=[x for x in vulns if 'access' in x and x['access']['vector'] in filters['access']]
  if 'impact' in filters and len(filters['impact'])!=0:  # impact filters
    for fil in filters['impact']: vulns=[x for x in vulns if  'impact' in x and x['impact'][fil] !='NONE']
  # exploits only
  if exploitsOnly: vulns=[x for x in vulns if ('map_cve_exploitdb' in x or 'map_cve_msf' in x)]
  return vulns

def displayTypeFromArgs(args):
  if args.t:   return "term"
  elif args.p: return "pdf"
  else:        return "web"

def visualize(data, exploitOnly=False, filters={}, display="web"):
  # do the filtering on the data
  for system in data['systems']:
    if 'cpes' in system:
      for cpe in system['cpes']:
        cpe['cves']=filter(cpe['cves'], exploitOnly, filters)
    for service in system['services']:
      if "cves" in service:
        service['cves']=filter(service['cves'], exploitOnly, filters)
  # display using the correct method
  try:
    if not display in visuals.keys():
      sys.exit("Could not visualize: Unknown display (%s)"%display)
    # try to import requirements
    try:
      exec(visuals[display]['import'])
    except:
      sys.exit("Could not visualize due to missing dependencies")
    exec(visuals[display]['exec'])
  except KeyboardInterrupt:
    pass

if __name__ == '__main__':
  # argument parser
  description='''Visualizes the enhanced nmap results'''
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('-t',  action='store_true', help='Use terminal GUI')
  parser.add_argument('-p',  metavar='location',  help='Parse to PDF to location')
  parser.add_argument('-fE', action='store_true', help='Filter: Exploit scripts/frameworks available')
  parser.add_argument('-fN', action='store_true', help='Filter: Exploitable via network')
  parser.add_argument('-fL', action='store_true', help='Filter: Exploitable locally')
  parser.add_argument('-fAN',action='store_true', help='Filter: Exploitable via adjecent network')
  parser.add_argument('-fC', action='store_true', help='Filter: Impacts Confidentiality')
  parser.add_argument('-fI', action='store_true', help='Filter: Impacts Integrity')
  parser.add_argument('-fA', action='store_true', help='Filter: Impacts Availability')
  parser.add_argument('inp', metavar='input',     help='output file from analyzer' )
  args = parser.parse_args()

  # intakes
  try:
    syslist=json.loads(open(args.inp).read())
  except:
    sys.exit("Invalid JSon format!")

  filters = filtersFromArgs(args)
  display = displayTypeFromArgs(args)
  visualize(syslist, args.fE, filters, display)
