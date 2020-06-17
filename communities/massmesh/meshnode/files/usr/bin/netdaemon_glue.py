#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os.path, json, socket

import subprocess
from subprocess import check_output
import multiprocessing

import netdaemon_endpoints

from wsgiref.simple_server import make_server
from wsgiref import simple_server, util

from wsgiref.simple_server import WSGIRequestHandler, WSGIServer
from wsgiref.simple_server import make_server
import socket

class wsgi():

    def server_init(self):

      self.host = "::"
      server_cls  = WSGIServer

      if ':' in self.host:
        if getattr(server_cls, 'address_family') == socket.AF_INET:
          class server_cls(server_cls):
            address_family = socket.AF_INET6

      self.port = 1617
      server = make_server(self.host, self.port, netdaemon_endpoints.application, server_cls)
      self.server_process = multiprocessing.Process(target=server.serve_forever)
      self.server_process.daemon=False
      self.server_process.start()

    def setUp(self):
      try:
        self.server_init()
      except socket.error:
        print('wsgi: error: server socket error / socket not available')
        self.tearDown()

    def tearDown(self):
        if hasattr(self, 'server_process'):
          self.server_process.terminate()
          self.server_process.join()
          del(self.server_process)
# <!-- end of wsgi -->

