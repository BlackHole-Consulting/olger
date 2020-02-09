#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# Converts the nmap xml file to the stripped down CVE-Search json
#  format

# Copyright (c) 2015	NorthernSec
# Copyright (c)	2015	Pieter-Jan Moreels
# This software is licensed under the Original BSD License

# Imports
import os
import sys
runpath=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runpath, '..'))

try:
  from libnmap.parser import NmapParser
except:
  sys.exit("Missing dependencies!")

import argparse

from lib.Toolkit import writeJson

def parseNMap(file=None, string=None):
  try:
    if file: report = NmapParser.parse_fromfile(file)
    elif string: report = NmapParser.parse_fromstring(string)
    else: raise(Exception)
  except:
    raise(Exception)
  systems = []
  for h in report.hosts:
    system = {'mac':h.mac, 'ip':h.address, 'status':h.status, 'hostnames': h.hostnames,
              'vendor':h.vendor, 'distance':h.distance}
    cpeList = []
    for c in h.os_match_probabilities():
      for x in c.get_cpe():
        cpeList.append(x)
    cpeList=list(set(cpeList))
    if len(cpeList)>0:
      system['cpes']=cpeList
    services = []
    for s in h.services:
      service={'port':s.port, 'banner':s.banner, 'protocol':s.protocol, 'name':s.service,
               'state':s.state, 'reason':s.reason}
      if s.cpelist:
        service['cpe'] = s.cpelist[0].cpestring
      services.append(service)
    system['services']=services
    systems.append(system)
  scan={"systems":systems, "scan": {"time": report.endtime, 
                                    "type": report._nmaprun["args"]}}
  return scan

if __name__ == '__main__':
  # argument parser
  description='''Converts the nmap xml file to the stripped down
                 CVE-Search json format'''
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('inp', metavar='input',  type=str, help='Input nmap xml file')
  parser.add_argument('out', metavar='output', type=str, help='Output file')
  args = parser.parse_args()

  # input
  try:
    syslist=parseNMap(file=args.inp)
  except:
    exit("Invalid Nmap xml!")
  writeJson(args.out, syslist)
