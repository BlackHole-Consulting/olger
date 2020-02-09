#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# Terminal component of CVE-Scan. Takes a list of scanned hosts as
# input and uses the terminal to displays this information in a
# graphical manner, enhancing it with information from the CVE-Search
# database and ToolsWatch Default Password Enumeration (DPE) list.
#
# Copyright (c) 2016    NorthernSec
# Copyright (c) 2016    Pieter-Jan Moreels
# This software is licensed under the Original BSD Licence

# Imports
import os
runpath = os.path.dirname(os.path.realpath(__file__))

import copy
import re
import specter
from lib.Toolkit import make_dict, splitByLength, fromEpoch

class TermDisplay():
  @classmethod
  def start(self, scan=None):
    systems = scan['systems'] if scan and 'systems' in scan else None
    colors = {'vulnerable': ('red', 'black', False)}
    screen = specter.Specter(markupSet=colors)

    # Functions
    def product(banner):
      if banner:
        r=make_dict(banner)
        return r['product']
      else:
        return 'Unknown'


    def getSystemInfo(s):
      cpes    =s['cpes']      if 'cpes'       in s else ['Not Detected']
      mac     =s['mac']       if s['mac']          else 'Unknown'
      marked  ='vulnerable'   if 'cves' in cpes[0] else 'normal'
      hosts   =s['hostnames'] if 'hostnames'  in s else ['None']
      services=s['services']  if 'services'   in s else [_NoServ]
      serv    =services[0]

      cont=[        {'tn':'i',
                     'tc':[{'t': 'IP',           'm': 'title'},
                           {'t': s['ip']                     } ]},
                    {'tn':'i',
                     'tc':[{'t': 'MAC',          'm': 'title'},
                           {'t': mac                         } ]},
                    {'tn':'i',
                     'tc':[{'t': 'Status',       'm': 'title'},
                           {'t': s['status']                 } ]},
                    {'tn':'i',
                     'tc':[{'t': 'CPEs',         'm': 'title'},
                           {'t': cpes[0]['cpe'], 'm': marked } ]}]
      for cpe in cpes[1:]:
        marked='vulnerable' if 'cves' in cpe else 'normal'
        cont.append({'tn':'i',
                     'tc':[{'t': ' '                         },
                           {'t': cpes[0]['cpe'], 'm':marked  } ]})
      cont.append(  {'tn':'i',
                     'tc':[{'t': 'Vendor',       'm': 'title'},
                           {'t': s['vendor']                 } ]})
      cont.append(  {'tn':'i',
                     'tc':[{'t': 'Hostnames',    'm': 'title'},
                           {'t': hosts[0]                    } ]})
      for host in hosts[1:]:
        cont.append({'tn':'i',
                     'tc':[{'t': ' ',            'm': 'title'},
                           {'t': host                        } ]})
      cont.append(  {'tn':'i',
                     'tc':[{'t': 'Distance',     'm': 'title'},
                           {'t': s['distance']               } ]})
      ser='%s (%s/%s) is %s'%(serv['name'],serv['port'],serv['protocol'],serv['state'])
      marked='vulnerable' if len(serv['cves'])>0 else 'normal'
      cont.extend( [{'tn':'i',
                     'tc':[{'t': 'Services',     'm': 'title'},
                           {'t': ser,            'm':marked  } ]},
                    {'tn':'i',
                     'tc':[{'t': ' ',            'm': 'title'},
                           {'t': ' > %s'%product(serv['banner']),
                                                 'm': marked } ]},
                    {'tn':'i',
                     'tc':[{'t': ' ',            'm': 'title'},
                           {'t': ' > %s'%serv['cpe'],
                                                 'm':marked  } ]} ])

      for serv in services[1:]:
        marked='vulnerable' if len(serv['cves'])>0 else 'normal'
        ser='%s (%s/%s) is %s'%(serv['name'],serv['port'],serv['protocol'],serv['state'])
        cont.extend([{'tn':'i',
                      'tc':[{'t': ' '                        },
                            {'t': ser,           'm':marked  } ]},
                     {'tn':'i',
                      'tc':[{'t': ' '                        },
                            {'t': ' > %s'%product(serv['banner']),
                                                 'm':marked  } ]},
                    {'tn':'i',
                     'tc':[{'t': ' '                         },
                           {'t': ' > %s'%serv['cpe'],
                                                 'm':marked  } ]} ])
      return cont

    def cvesForcpe(line,sys,args=None):
      if type(line) == dict:
        if 'tc' in line: line = line['tc'][1]
        if 't'  in line: line = line['t']
      if type(line) is not str: line = str(line)

      # Clean out collumns
      if line.startswith("CPEs"):     line = line[4:].strip()
      if line.startswith("Services"): line = line[8:].strip()
      # reset variables
      service=None
      cves=None
      # make sure we're dealing with strings
      line=str(line)
      # handle args if present, else use current line
      if args:
        line=str(args[0])
      else:
        if line.strip().startswith('> '): # We're either working by cpe or product
          line=line.strip('> ')
        elif line.startswith('cpe:'):     # We're working by cpe
          pass
        else:                             # We're working by port
          line=rePortLine.search(line)
          if line: line=line.group()[1:-5]
          else:    return
      # see if we match on port
      if rePort.match(line):
        for s in sys['services']:
          if str(s['port'])==line:
            service=s;
            cves=s['cves']
            break
      # see if we match on cpe
      elif reCPE.match(line):
        for s in sys['services']:
          if str(s['cpe'])==line:
            service=s;
            cves=s['cves']
            break
        if not service:
          for c in sys['cpes']:
            if c['cpe']==line:cves=c['cves'];break
      # see if we match on product name
      else:
        for s in sys['services']:
          if product(s['banner'])==line:
            service=s;
            cves=s['cves']
            break
      if cves:
        cveList(cves,service)

    # Windows
    def splash():
      x, y = screen.getMaxXY()
      if y<10:raise("Please make sure your terminal has at least 10 rows")
      screen.splash(tSplash)

    def help():
      screen.scroll(tHelp, footer=tDefFoot, nav=extendedNav)

    def info():
      text=[{'t': "Scan", 'm': "title"},
            {'t': "  Date: %s"%fromEpoch(scan['scan']['time'])},
            {'t': "  Type: %s"%scan['scan']['type']},
            {'t': "Enhancement", 'm': "title"},
            {'t': "  Date: %s"%fromEpoch(scan['enhanced']['time'])}]
      screen.scroll(text, footer=tDefFoot, nav=extendedNav)

    def cveList(cves, service=None):
      navSet=copy.deepcopy(extendedNav)
      navSet['enter'] = ['o']
      text=[]
      for cve in cves:
        C = cve[_I][_IC][0] if _I in cve and _IC in cve[_I] else "?"
        I = cve[_I][_II][0] if _I in cve and _II in cve[_I] else "?"
        A = cve[_I][_IA][0] if _I in cve and _IA in cve[_I] else "?"
        V = cve[_A][_AV][0] if _A in cve and _AV in cve[_A] else "?"
        Co= cve[_A][_AC][0] if _A in cve and _AC in cve[_A] else "?"
        text.append({'t': "%s - %s%s%s - %s %s"%(cve['id'], C, I, A, V, Co),
                     'a': cveDetails, 'p': cve})
      screen.scroll(text,header=tServiceHead,footer=tServiceFoot,
                    cursor=True, nav=navSet)

    def cveDetails(cve):
      maxx, maxy = screen.getMaxXY()
      summary=splitByLength(cve['summary'],maxx-18)

      text=      ["CVE id    %s"%cve['id']]
      text.append("Summary   %s"%summary[0])
      for i, x in enumerate(summary[1:]):
        text.append("          %s"%summary[i+1])
      text.append(" ")
      text.append("CVSS      Base:             %s"%(cve['cvss']))
      text.append("          Exploitability:   %s"%(cve['exploitCVSS'] if 'exploitCVSS' in cve else ' -'))
      text.append("          Impact:           %s"%(cve['impactCVSS']  if 'impactCVSS'  in cve else ' -'))
      text.append(" ")
      text.append("Access    Vector:           %s"%cve['access']['vector'])
      text.append("          Complexity:       %s"%cve['access']['complexity'])
      text.append("          Authentication:   %s"%cve['access']['authentication'])
      text.append(" ")
      text.append("Impact    Confidentiality:  %s"%cve['impact']['confidentiality'])
      text.append("          Integrity:        %s"%cve['impact']['integrity'])
      text.append("          Availability:     %s"%cve['impact']['availability'])
      screen.scroll(text, footer=tDefFoot, nav=extendedNav)

    def home():
      index = 0
      lineNr = 0
      while True:
        system = systems[index]
        content = getSystemInfo(system)
        foot=copy.deepcopy(tNavFoot)
        foot[1]=foot[1]%(index+1,len(systems))
        key, lineNr = screen.scroll(content, footer=foot, cursor=lineNr,
                                    blocking=False, functions=keyFuncts,
                                    nav=sysNav)
        if   key in ['n']:
          index+=1
          if index>=len(systems):index=0
        elif key in ['p']:
          index-=1
          if index<0:index=len(systems)-1
        elif key in ['o']:
          cvesForcpe(content[lineNr], system)
        elif key in ['c']:
          parts = screen.userInput("Enter your command").lower().split()
          if parts:
            command = parts[0]
            args    = parts[1:]
            if   command in ['h', 'help']: help()
            elif command in ['c', 'cve' ]:
              line = content[lineNr]
              if type(line) == dict and 't' in line: line=line['t']
              if type(line) == str: cvesForcpe(line,system,args)
            elif command in ['i', 'info']: info()
            else: screen.popup(tInvalidCommand)
        elif key in ['q', chr(specter.KEY_ESC)]:
          break


    tSplash=[{'t': " _____ _   _ _____      _____                 ", 'm': 'header'},
             {'t': "/  __ \ | | |  ___|    /  ___|                ", 'm': 'header'},
             {'t': "| /  \/ | | | |__ _____\ `--.  ___ __ _ _ __  ", 'm': 'header'},
             {'t': "| |   | | | |  __|_____|`--. \/ __/ _` | '_ \ ", 'm': 'header'},
             {'t': "| \__/\ \_/ / |___     /\__/ / (_| (_| | | | |", 'm': 'header'},
             {'t': " \____/\___/\____/     \____/ \___\__,_|_| |_|", 'm': 'header'},
             {'t': "                            (c) NorthernSec   ", 'm': 'header'},
             {'t': "             [Press the any key]              ", 'm': 'title'}]

    tNavFoot=["(u)p   | (n)ext    | (p)revious | (q)uit |",
              "(d)own | (j)ump to | (c)ommand  | (o)pen | [%s/%s]"]

    tServiceHead=['CVE           - CIA - Vector Complexity']

    tServiceFoot=['Vector:     N(etwork) - A(djecent network) - L(ocal)',
                  'CIA Impact: L(ow)     - M(edium)           - H(igh)',
                  'Press Enter or o for more info']

    tHelp=[{'t': '----------', 'm': 'title'},
           {'t': '|  HELP  |', 'm': 'title'},
           {'t': '----------', 'm': 'title'},
           {'t': ' '},
           {'t':'Navigating','m': 'title'},
           {'t':' * You can navigate through the scanned systems with p and n, or the left and right arrow key'},
           {'t':' * You can scroll through the current system with u and d, or the up and down arrow key'},
           {'t':' * You can jump directly to a scanned system by entering the page number with j, and entering the page number.'},
           {'t':' '},
           {'t':'Commands','m': 'title'},
           {'t':'By pressing c, you can enter commands:'},
           {'t':'  h/help                  - Displays this menu'},
           {'t':'  c/cve [port/cpe/banner] - If found, displays CVEs of the current line, or service with the parameter'},
           {'t':'  i/info                  - Display info of the scan'}]
    tDefFoot=[" - press q or ESC to return to the previous page-"]

    tInvalidCommand = [{'t': 'Invalid command', 'm': 'title'}]

    extendedNav={'esc': ["q"], 'up':["u"], 'down':["d"]}
    sysNav={'esc': ["q"], 'up':["u"], 'down':["d"], 'left':["p"], 'right':["n"]}
    keyFuncts={'i': info, 'h': help}

    rePort=re.compile('^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$')
    reCPE=re.compile('^((%s|%s)[aoh]:.*)$'%(re.escape('cpe:/'),re.escape('cpe:2.3:')))
    rePortLine=re.compile('\\([0-9]*/(tcp|udp)\\)')
    _I ="impact"
    _IC="confidentiality"
    _II="integrity"
    _IA="availability"
    _A ="access"
    _AV="vector"
    _AC="complexity"

    _NoServ="No services found"
    try:
      splash()
      home()
      screen.stop()
    except Exception as ex:
      screen.stop()
      raise(ex)
