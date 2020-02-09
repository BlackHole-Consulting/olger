#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# Web component of CVE-Scan. Takes a list of scanned hosts as input and
# starts a web server to display this information in a graphical manner,
# enhancing it with information from the CVE-Search database and 
# ToolsWatch Default Password Enumeration (DPE) list.
#
# Copyright (c) 2015	NorthernSec
# Copyright (c)	2015	Pieter-Jan Moreels
# This software is licensed under the Original BSD License

# Imports

import os
_runpath=os.path.dirname(os.path.realpath(__file__))

import re
from urllib.request import urlopen
import urllib
try:
  from flask import Flask, render_template
except:
  sys.exit("Missing dependencies!")

import json

from lib.Toolkit import make_dict, toLocalTime, toHuman, fromEpoch
from lib.Config import Configuration

class WebDisplay():
  @classmethod
  def start(self,port=None,scan=None):
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    # functions
    

    # routes
    @app.route('/')
    def index():
      return render_template('index.html', scan=scan)

    @app.route('/cve/<cveid>')
    def cve(cveid):
      host,port=Configuration.getCVESearch()
      data = (urlopen('http://%s:%s/api/cve/%s'%(host,port,cveid)).read()).decode('utf8')
      cvejson=json.loads(str(data))
      if cvejson is {}:
        return page_not_found(404)
      return render_template('cve.html', cve=cvejson)

    # error handeling
    @app.errorhandler(404)
    def page_not_found(e):
      return render_template('404.html'), 404

    # filters
    @app.template_filter('product')
    def product(banner):
      if banner:
        r=make_dict(banner)
        return r['product'] if 'product' in r else 'unknown'
      else:
        return "unknown"
    @app.template_filter('toHuman')
    def humanify(cpe):
      return toHuman(cpe)

    @app.template_filter('currentTime')
    def currentTime(utc):
      return toLocalTime(utc)

    @app.template_filter('impact')
    def impact(string):
      if string.lower() == "none":       return "good"
      elif string.lower() == "partial":  return "medium"
      elif string.lower() == "complete": return "bad"

    @app.template_filter('vFeedName')
    def vFeedName(string):
      string=string.replace('map_','')
      string=string.replace('cve_','')
      return string.title()

    @app.template_filter('htmlEncode')
    def htmlEncode(string):
      return urllib.parse.quote_plus(string).lower()

    @app.template_filter('isURL')
    def isURL(string):
      urlTypes= [re.escape(x) for x in ['http://','https://', 'www.']]
      return re.match("^(" + "|".join(urlTypes) + ")", string)

    @app.template_filter('fromEpoch')
    def fromEpoch_filter(epoch):
      return fromEpoch(epoch)


    # debug filter
    @app.template_filter('type')
    def isType(var):
      return type(var)

    #start webserver
    host = Configuration.getFlaskHost()
    port = Configuration.getFlaskPort()
    debug = Configuration.getFlaskDebug()
    app.run(host=host, port=port, debug=debug)


