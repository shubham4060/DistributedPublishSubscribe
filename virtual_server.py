from concurrent import futures
import time
import json
import grpc
import pr_pb2
import pr_pb2_grpc
import thread
import random
import sys
import socket
from pymongo import MongoClient
import time

MASTER_IP = ""
BACKUP_IP = ""

if len(sys.argv) < 2 :
  print "ERROR : Enter the port for access point server...exiting"
  exit()
port = sys.argv[1]


_ONE_DAY_IN_SECONDS = 60 * 60 * 24
SELF_IP=[l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

stub = ""
stub1 = ""

TIMEOUT = 3

def Forward(request,i):
  global stub
  global stub1
  retries=0

  while(True):
    if retries >=3 :
      toggle_backup()
      retries = 0
    try:
      if i == 0:
        response=stub.unsubscribeRequestCentral(request, timeout = 10)
        return response
      elif i == 1:
        response=stub.deReplicaRequest(request, timeout = 10)
        return response
      elif i == 3:
        response=stub.replicaRequest(request, timeout = 10)
        return response
      elif i == 4:
        response=stub.subscribeRequestCentral(request, timeout = 10)
        return response
      elif i == 7:
        response=stub.getFrontIp(request, timeout = 10)
        return response
      elif i == 8:
        response=stub.registerIp(request, timeout = 10)
        return response

    except Exception as e:
      retries+=1
      print "master not reachable, retry :", retries
      time.sleep(TIMEOUT)

def toggle_backup():
  global stub
  global stub1

  a = json.load(open("options","r"))
  temp = a["centralServer"]
  a["centralServer"] = a["centralServerBackup"]
  a["centralServerBackup"] = temp
  json.dump(a,open("options","w"))
  print "Master is down toggled to Backup"
  response = stub1.upgradeBackup(pr_pb2.empty())
  c=stub
  stub=stub1
  stub1=c



class VirtualServer(pr_pb2_grpc.PublishTopicServicer):

  def getMasterIp(self, request, context):
    a = json.load(open("options","r"))
    return pr_pb2.ips(ip=a["centralServer"])

  def getBackupIp(self, request, context):
    a = json.load(open("options","r"))
    return pr_pb2.ips(ip=a["centralServerBackup"])

  def unsubscribeRequestCentral(self, request, context):
    response=Forward(request,0)
    return response

  def deReplicaRequest(self, request, context):
    response=Forward(request,1)
    return response

  def querryTopics(self, request, context):
    retries=0
    global stub
    global stub1
    while(True):
      if retries >=3 :
        toggle_backup()
        retries = 0
      try :
        responses=stub.querryTopics(request, timeout = 10)
        for response in responses :
          yield response
        return
      except Exception as e:
        retries+=1
        print "master not reachable, retry :", retries
        time.sleep(TIMEOUT)

  def replicaRequest(self, request, context):
    response=Forward(request,3)
    return response

  def subscribeRequestCentral(self, request, context):
    response=Forward(request,4)
    return response

  def giveSubscriberIps(self, request, context):
    retries=0
    global stub
    global stub1
    while(True):
      if retries >=3 :
        toggle_backup()
        retries = 0
      try :
        responses=stub.giveSubscriberIps(request, timeout = 10)
        for response in responses :
          yield response
        return
      except Exception as e:
        retries+=1
        print "master not reachable, retry :", retries
        time.sleep(TIMEOUT)

  def giveIps(self, request, context):
    retries=0
    global stub
    global stub1
    while(True):
      if retries >=3 :
        toggle_backup()
        retries = 0
      try :
        responses=stub.giveIps(request, timeout = 10)
        for response in responses :
          yield response
        return
      except Exception as e:
        retries+=1
        print "master not reachable, retry :", retries
        time.sleep(TIMEOUT)

  def getFrontIp(self, request, context) :
    response=Forward(request,7)
    return response

  def registerIp(self, request, context) :
    response=Forward(request,8)
    return response


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  pr_pb2_grpc.add_PublishTopicServicer_to_server(VirtualServer(), server)
  server.add_insecure_port(str(SELF_IP)+":"+port)
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  c=json.load(open('options','r'))
  MASTER_IP=c["centralServer"]
  BACKUP_IP=c["centralServerBackup"]

  channel = grpc.insecure_channel(MASTER_IP)
  stub = pr_pb2_grpc.PublishTopicStub(channel)

  channel1 = grpc.insecure_channel(BACKUP_IP)
  stub1 = pr_pb2_grpc.PublishTopicStub(channel1)

  print "Virtual server up..."

  serve()
