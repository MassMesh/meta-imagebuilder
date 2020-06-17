#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys, os, socket

import locale
locale.setlocale(locale.LC_ALL, '')

import netdaemon_glue
import json
## globals

FILTER_TOGGLE_ALLOW     = os.environ.get('FILTER_TOGGLE_ALLOW', False)
FILTER_TOGGLE_DENY      = os.environ.get('FILTER_TOGGLE_DENY', False)
FILTER_ALLOW            = os.environ.get('FILTER_ALLOW', [])
FILTER_DENY             = os.environ.get('FILTER_DENY', [])
REGISTRATION_TOGGLE     = os.environ.get('REGISTRATION_TOGGLE', False)
REGISTRATION_NO_BORDERS = os.environ.get('REGISTRATION_NO_BORDERS', True)
REGISTERED_WAITLIST     = os.environ.get('REGISTERED_WAITLIST', [])
LEASE_CLIENT_MAX        = os.environ.get('LEASE_CLIENT_MAX', 10)
LEASE_CLIENT_EXPIRE     = os.environ.get('LEASE_CLIENT_EXPIRE', 240)

APP_BASEDIR     = os.getcwd()
THIS_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
LOGO = '-=[ 𝕄𝕄 ℕ𝕖𝕥𝔻𝕒𝕖𝕞𝕠𝕟 ]=-'

def log(s):
  print('[ℕ𝕖𝕥𝔻𝕒𝕖𝕞𝕠𝕟] %s' % str(s))

def main():
  print(LOGO)
  log("Web Server Gateway Interface: " + wsgi_server.host + ":" + str(wsgi_server.port))

  try:
    netdaemon_cfgfile = '/usr/etc/netdaemon.ini'
    with open(netdaemon_cfgfile) as file_descriptor:
      exec(file_descriptor.read())
    log('NetDaemon: Config: Imported from ' + netdaemon_cfgfile)

  except (Exception) as e:
    log('NetDaemon: Config: Warning: ' + str(e))

  pass

wsgi_server = netdaemon_glue.wsgi()
wsgi_server.setUp()

if __name__ == '__main__':
  try:
    main()
  except SystemExit:
    pass
  except:
    print ('Fatal Error -- ' + traceback.format_exec())
