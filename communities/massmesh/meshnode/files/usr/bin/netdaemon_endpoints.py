#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cgi
import json
import os
import re
import sys
import subprocess
from subprocess import check_output
import multiprocessing
import socket

from mm_cli import util

import csv
import netaddr
import random
import string
import urllib

def log(s):
  print('[ℕ𝕖𝕥𝔻𝕒𝕖𝕞𝕠𝕟] %s' % str(s))

try:
  from __main__ import FILTER_TOGGLE_ALLOW, \
                       FILTER_TOGGLE_DENY, \
                       FILTER_ALLOW, \
                       FILTER_DENY, \
                       REGISTRATION_TOGGLE, \
                       REGISTRATION_NO_BORDERS, \
                       REGISTERED_WAITLIST, \
                       LEASE_CLIENT_MAX, \
                       LEASE_CLIENT_EXPIRE
except Exception as e:
  log('Endpoints: Error: Config environment at __main__ ' + str(e))
  sys.exit()



## globals

ND_MVP_DB='/tmp/netdaemon.csv'
ND_MVP_DB_COLUMNS = [
  'network_long',
  'network_cidr',
  'public_enckey',
  'status_blob',
  'ident_blob',
]

ND_SCRIPT_YGG_UCI  = '/usr/bin/ygguci'
ND_SCRIPT_CJD_UCI  = '/usr/bin/cjdnsconf'
ND_SCRIPT_MESHCTL  = '/usr/bin/meshctl'

BIN_YGGDRASIL = '/usr/sbin/yggdrasil'
BIN_YGGDR_CTL = '/usr/sbin/yggdrasilctl'

class NDExec(object):

  def __init__(self, ref_arg=False):

    required_args = [ ]

    try:

      if not ref_arg:
        raise ValueError('Error: NDExec(object) Missing Args')

      for var in required_args:
        if not ref_arg[var]:
          raise ValueError(var)
        else:
          setattr(self, var, ref_arg[var])

    except ValueError as e:
      self.insane = ValueError(e)
  # <!-- __init__ -->


  def file_exists(self, path_filename):
    return (os.path.isfile(path_filename))

  def nd_run_script(self, nd_script=False):
      try:

        if hasattr(self, 'insane'):
          raise self.insane

        try:
          out = check_output(nd_script, stderr=subprocess.STDOUT)
          data = json.loads(out)
          return([ json.dumps(data).encode("utf-8") ])
        except Exception as e:
          return([ json.dumps({'error': str(e)}).encode("utf-8") ])

      except OSError:
        return False
  # <!-- end nd_run_script -->
# <!-- end of NDExec -->



## sanity

def sanitize_path(path):
  newpath = path.split("/")
  newpath = filter(lambda x: x != "", newpath)
  return "/" + "/".join(newpath)

def bad_request(start_response, obj):
  start_response("400 Bad Request", [("content-type", "application/json; charset=utf-8")])
  return json.dumps(obj)


## endpoint functions

def getself(start_response):
  start_response("200 OK", [("content-type", "application/json; charset=utf-8")])
  v = [ "/usr/sbin/yggdrasilctl", "-v", "-json", "getself" ]
  r = NDExec({'courie': 'params'})
  return r.nd_run_script(v)
# <!-- end getself -->


def ping_pong(start_response, data):
  start_response("200 OK", [("content-type", "application/json; charset=utf-8")])
  return [ json.dumps(data).encode("utf-8") ]
# <!-- end ping_pong -->




## main application (routes)

def application(env, start_response):
  method       = env["REQUEST_METHOD"].upper()
  page         = sanitize_path(env["PATH_INFO"])
  pathinfo     = env["PATH_INFO"]
  query_data   = env["QUERY_STRING"]
  query_string = env['QUERY_STRING']
  remote_addr  = env['REMOTE_ADDR']
  user_agent   = env['HTTP_USER_AGENT']

  try:
    request_body_size = int(env.get('CONTENT_LENGTH', 0))
  except (ValueError):
    request_body_size = 0

  request_body = env['wsgi.input'].read(request_body_size)

  try:
    user_venom = urllib.parse.parse_qs(request_body, encoding='utf-8')
    print('user_venom', user_venom)
    box_pub_key = user_venom.get(b'box_pub_key')[0].decode()
    print('box_pub_key:', box_pub_key)
  except:
    pass

  if (method == "POST"):

    if (page == "/wip_make_register"):

      ## Debug output if interested
      # print('query_data', query_data)
      # print('query_string', query_string)
      # print('method', method)
      # print('user_venom', user_venom)
      # print('box_pub_key', box_pub_key)

      return wip_make_register(start_response, remote_addr, box_pub_key)

  elif (method == "GET"):

    if (page == "/ping"):

      data = {
        'method': method,
        'page': page,
        'pathinfo': pathinfo,
        'query_string': query_string,
        'remote_addr': remote_addr,
        'user_agent': user_agent
      }

      return ping_pong(start_response, data)
    # /ping

    elif (page == "/getself"):
      return getself(start_response)

    elif (page == "/wip_make_pool_database"):
      return wip_make_pool_database(start_response)

    elif (page == "/wip_read_pool_file"):
      return wip_read_pool_file(start_response)

    elif (page == "/info"):
      return get_info(start_response)

    elif (page == "/wip_make_register"):
      return wip_get_register(start_response, remote_addr)

    elif (page == "/wip_get_register"):
      return wip_get_register(start_response)

    elif (page == "/exit"):
      ## Testing: Kills the server (when running in loop)
      os.popen('killall -9 python python3')

  # <!-- end GET method -->

  else:

    return bad_request(start_response, {'error': 'bad_request'})

# <!-- end application(env, start_response) -->

def verify_publickey(**kwargs):

  ## remote_addr: ip6 address assert(validate == bpk_lookup)
  if 'remote_addr' in kwargs:
    remote_addr = str(kwargs["remote_addr"])
    try:
      ygg_rtr_prefix="200::/8" # Routers
      ygg_sub_prefix="300::/8" # Advertised Prefix
      assert(netaddr.IPAddress(remote_addr) in netaddr.IPNetwork(ygg_rtr_prefix))
    except:
      return None
  else:
    # We optionally check box_pub_key matches a remote_addr
    remote_addr = None

  ## box_pub_key: may be user provided we assert yggrouter IP sanity
  if 'box_pub_key' in kwargs:
    try:
      box_pub_key = re.match('(^[a-z0-9]{64}$)', kwargs["box_pub_key"])[0]

      bpk_lookup = subprocess.check_output([ BIN_YGGDRASIL, "-address", "-useconf"],
        input=bytes(json.dumps({'EncryptionPublicKey': box_pub_key}), 'utf-8'))
      bpk_lookup = bpk_lookup.decode('utf-8').replace("\n", "")

      # Fully Qualified Public Key
      if (remote_addr) and (remote_addr == bpk_lookup):
        return bpk_lookup

      # Return a box_pub_key lookup
      elif not (remote_addr):
        return bpk_lookup

      # Zero Cools
      else:
        print('err: *!* FQPK Fail')
        return None
    except:
      return None
  else:
      # Missing public_key arg.
      return None

# end of verify_publickey(data)

def wip_make_register(start_response, remote_addr, box_pub_key):
  """
    Finds next available cloud prefix

    POST /register - Takes basic information and stores requester's node key for whitelisting

        200 - Registration accepted
        400 - Registration failed

  """

  ## Verify box_pub_key is valid with yggdrasil -address trick
  ## If remote_addr is supplied, validate box_pub_key matches remote_addr
  try:
    assert(verify_publickey(remote_addr=remote_addr, box_pub_key=box_pub_key))
  except:
    start_response("400 OK", [("content-type", "application/json; charset=utf-8")])
    return [ json.dumps({"public_encryption_key": "error"}).encode("utf-8") ]

  ## All networks in csv file
  subnets = list(map(lambda x: netaddr.IPNetwork(x['network_cidr']), wip_read_pool_file()))

  ## Filter Supernet (100.100.0.0/21) for /24 networks NOT in csv file
  suprnet = netaddr.IPNetwork('100.100.0.0/21').subnet(24)

  try:
    free_network = list(filter(lambda x: not x in subnets, suprnet))[0]

    ## Append the registration details and new 'free_network' to CSV
    with open(ND_MVP_DB, mode='a', encoding='UTF-8', newline='') as db:
      writer = csv.DictWriter(db, fieldnames=ND_MVP_DB_COLUMNS)

      ip_list   = list(free_network)
      broadcast = ip_list.pop(-1)
      gateway   = ip_list.pop(1)
      citizen   = ip_list.pop(1)
      poolsize  = len(ip_list)

      reqcloud  = 'cloud-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))


      network_cidr  = str(free_network)
      network_long  = str(netaddr.IPNetwork(gateway).value)
      prefix_length = netaddr.IPNetwork(network_cidr).prefixlen
      public_enckey = box_pub_key
      status_blob   = 'None'
      ident_blob    = {'cloud': reqcloud, 'remote_addr': remote_addr}

      data = [network_long, network_cidr, public_enckey, status_blob, ident_blob]
      data = dict(zip(ND_MVP_DB_COLUMNS, map(str, data)))
      print('writing data', str(data))
      writer.writerow(data)
    # <!-- end of CSV work -->
  except:
    start_response("400 OK", [("content-type", "application/json; charset=utf-8")])
    return [ json.dumps({ 'cloud_network': 'None'}).encode("utf-8") ]

  start_response("200 OK", [("content-type", "application/json; charset=utf-8")])

  util.addremotesubnet(citizen, box_pub_key)

  ip_addr_add = str(gateway) + "/" + str(prefix_length)
  util.addip(ip_addr_add, 'ygg0')

  return [ json.dumps({
    'remote_addr': remote_addr,     # 201:1dc6:90e4:1c1a:bba4:b5ba:82:1948
    'box_pub_key': box_pub_key,     # 6ac222cd81ef3446832b9aef2b0d2c8920ded440f68495a43544ecee99ad4045
    'prefix': str(free_network),    # 100.100.4.0/24
    'pfxlen': str(prefix_length),   # 24
    'gateway': str(gateway),        # 100.100.4.1
    'broadcast': str(network_cidr), # 100.100.4.0/24
    'poolsize': str(poolsize),      # 253
    'citizen': str(citizen)         # 100.100.4.2
  }).encode("utf-8") ]

# <!-- end wip_make_pool_db() -->

def wip_get_register(start_response):
  """
    GET /register - Shows the status of registration
        200 - Registration open
        202 - Registration pending approval
        201 - Registration successful / complete
        403 - Registration not allowed
  """

  start_response("200 OK", [("content-type", "application/json; charset=utf-8")])

  data = 'wip_get_register(!!)'
  return [ json.dumps(data).encode("utf-8") ]
# <!-- end wip_make_pool_db() -->

## Make Pool
def wip_make_pool_database(start_response):

  start_response("200 OK", [("content-type", "application/json; charset=utf-8")])

  ## 256 class-c networks (100.100.*.*)
  ip = netaddr.IPNetwork('100.100.0.0/16')

  ## 4 class-c networks (100.100.0-3.*)
  ip = netaddr.IPNetwork('100.100.0.0/22')


  ## Populates the CSV file (Mostly for testing)
  with open(ND_MVP_DB, mode='w', encoding='UTF-8', newline='') as db:
    writer = csv.DictWriter(db, fieldnames=ND_MVP_DB_COLUMNS)
    writer.writeheader()

    for network in list(ip.subnet(24)):

      ip_list   = list(network)

      broadcast = ip_list.pop(-1)
      gateway   = ip_list.pop(0)
      poolsize  = len(ip_list)
      reqcloud  = 'cloud-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))


      network_cidr  = str(network)
      network_long  = str(netaddr.IPNetwork(gateway).value)
      public_enckey = 'None'
      public_enckey =  ''.join(random.choices(string.ascii_lowercase + string.digits, k=64))
      status_blob   = {'status': 'disconnected', 'key': 'value'}
      status_blob   = 'None'
      ident_blob    = {'cloud': reqcloud}
      ident_blob    = 'None'

      data = [network_long, network_cidr, public_enckey, status_blob, ident_blob]
      data = dict(zip(ND_MVP_DB_COLUMNS, map(str, data)))

      writer.writerow(data)

    # <!-- end csv dataWrites -->
  # <!-- closed file descriptor -->

  data = wip_read_pool_file()
  return [ json.dumps(data).encode("utf-8") ]
# <!-- end wip_make_pool_db() -->


## Read Pool file
def wip_read_pool_file():
  data = []
  with open(ND_MVP_DB, mode='r', encoding='UTF-8', newline='') as csv_file:
    for row in csv.DictReader(csv_file):
      data.append(row)
  return data
# <!-- end wip_read_pool_db() -->



def get_info(start_response):

  try:
    ygg_thisbox = util.Hemicarp(name="netdaemon", admin_endpoint="/var/run/yggdrasil.sock")
    data = {
      'ipv6': ygg_thisbox.ipv6,
      'build_version': ygg_thisbox.build_version,
      'coords': ygg_thisbox.coords,
      'box_pub_key': ygg_thisbox.box_pub_key,
      'subnet': ygg_thisbox.subnet,
      'getpeers': list(ygg_thisbox.getPeers()),
      'enableTunnel': ygg_thisbox.enableTunnel(),
    }
    start_response("200 OK", [("content-type", "application/json; charset=utf-8")])
  except:
    data = { 'error': True }
    start_response("500 OK", [("content-type", "application/json; charset=utf-8")])
  finally:
    return [ json.dumps(data).encode("utf-8") ]

# <!-- end get_info() -->


"""
  GET /info - Displays info
      Gatway owner name / email, etc
      Description - A message to the node user's UI
      Registration required (if AllowRegistration AND WhitelistEnabled)

  POST /register - Takes basic information and stores requester's node key for whitelisting
      200 - Registration accepted
      400 - Registration failed

  GET /register - Shows the status of registration
      200 - Registration open
      202 - Registration pending approval
      201 - Registration successful / complete
      403 - Registration not allowed

  POST /renew - takes the source IP and finds public key, finds a free or existing IP in ygg.conf and adds a remote subnet if not exists, returns json or plain text the assigned IP, save timestamp somewhere
      200 - lease exists or renewed, responds with lease IP
      401 - Needs to register first
      201 - Registration pending
      403 - On blacklist or not on whitelist, contact node owner
      503 - MaxClients reached try again later

  ## 1. add source subnets
    # yctl addlocalsubnet subnet=0.0.0.0/0
    # print('allowSource', ygg_thisbox.allowSource('0.0.0.0'))

    ## 2. enable tunnel routing
    # yctl settunnelrouting enabled=true
    # print('enableTunnel', ygg_thisbox.enableTunnel())

    ## 3. Add IP/Network to yggdrasil interface
    # ip addr add ${above_network_100.100.0.1/24} dev ygg0

    ## 4. Tell yggdrasil connectng peers IP/Network and PubKey
    # yctl addremotesubnet subnet=${above_network_fetch_100.100.0.10/32} box_pub_key=${above_pubkey_xxxxxx}
    # print('addRoute', ygg_thisbox.addRoute('100.64.0.10/32', 'ygg_thatbox.box_pub_key'))

    ## 5. Firewall Rules
    # ipt -t filter -A FORWARD     -i ${wan} -j ACCEPT # and not FROM bogons!
    # ipt -t filter -A FORWARD     -o ${wan} -j ACCEPT # and not TO bogons
    # ipt -t nat    -A POSTROUTING -o ${wan} -j MASQUERADE
    # echo 1 | tee /proc/sys/net/ipv4/ip_forward


"""