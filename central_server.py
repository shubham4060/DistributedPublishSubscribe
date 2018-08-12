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
from datetime import datetime
import logging

if len(sys.argv) < 3 : 
    print "ERROR : Enter the port and type of server (0 for master, 1 for backup)...exiting"
    exit()

port = sys.argv[1]
IS_MASTER = False
IS_LOCKED = False
if sys.argv[2] == "0" :
    IS_MASTER = True
_ONE_DAY_IN_SECONDS = 60 * 60 * 24
SELF_IP=[l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
MAX_RETRIES = 2
centralServer = ""
backupCentralServer = ""

def print_status():
    if IS_MASTER :
        print "I am master..."
    else :
        print "I am backup..."

def two_phase_init(request):
    while(IS_LOCKED == True):
        pass
    channel = grpc.insecure_channel(backupCentralServer)
    stub = pr_pb2_grpc.PublishTopicStub(channel)
    retries = 2
    while (retries>0) :
        try:
            response = stub.commit_request(request)
            if response.ack=="OK":
                logging.info("%s:%s:COMPLETE",str(datetime.now()),request.filename)
                return "COMPLETE"
            else :
                return "ERROR"

        except Exception as e:
            retries -= 1
            if retries==0:
                logging.info("%s:%s:Backup down, performing transaction...",str(datetime.now()),request.filename)
                print "Backup down...performing transaction"
                return "ERROR"

def roll_back(request):
    print("Roll back ...")
    documents = pending_twoLevelDict.find({"action":"remove"})
    for document in documents :
        twoLevelDict.insert_one({"topic":document["topic"],"publisher":document["publisher"],"subscriber":document["subscriber"]})

    documents = pending_twoLevelDict.find({"action":"insert"})
    for document in documents :
        twoLevelDict.delete_one({"topic":document["topic"],"publisher":document["publisher"],"subscriber":document["subscriber"]})

    documents = pending_frontends.find({"action":"remove"})
    for document in documents :
        typ = document["type"]
        frontends.insert_one({"type":document["type"],typ:document[typ]})

    documents = pending_frontends.find({"action":"insert"})
    for document in documents :
        typ = document["type"]
        frontends.delete_one({"type":document["type"],typ:document[typ]})

    pending_frontends.drop()
    pending_twoLevelDict.drop()

class CentralServer(pr_pb2_grpc.PublishTopicServicer):

    def giveDataPhaseOne(self,request,context):
        IS_LOCKED = True
        print "Master is locked"
        data2return = {}
        frontends_data=[]
        twoLevelDict_data=[]
        cursor = frontends.find({})
        tempDir = {}
        for document in cursor:
            tempDir = document
            del tempDir["_id"]
            frontends_data.append(tempDir)
        cursor = twoLevelDict.find({})
        tempDir = {}
        for document in cursor:
            tempDir = document
            del tempDir["_id"]
            twoLevelDict_data.append(tempDir)
        data2return["frontend"]=frontends_data
        data2return["twoleveldict"]=twoLevelDict_data
        return pr_pb2.topic(topic=json.dumps(data2return))

    def giveDataPhaseTwo(self,response,context):
        IS_LOCKED = False
        print "Master is unlocked... Phase two completed"
        return pr_pb2.acknowledge(ack = "phase two completed")

    def upgradeBackup(self, request, context):
        global IS_MASTER
        global centralServer
        global backupCentralServer
        IS_MASTER=True
        print_status()
        centralServer, backupCentralServer = backupCentralServer, centralServer
        return pr_pb2.acknowledge(ack="backup successfully upgraded to master")

    def commit_request(self,request,context):
        if request.filename == "twoLevelDict":        
            if request.action == "remove" :
                if request.level == "3" : 
                    documents = twoLevelDict.find({"topic":request.data_1,"subscriber":request.data_3})
                    for document in documents:
                        pending_twoLevelDict.insert_one({"topic":document["topic"],"publisher":document["publisher"],"subscriber":document["subscriber"],"action":"remove"})
                    twoLevelDict.delete_one({"topic":request.data_1,"subscriber":request.data_3})
                    logging.info("%s:%s:REMOVE 3 %s %s %s",str(datetime.now()),request.filename,request.data_1,"NIL",request.data_3)
                    
                elif request.level == "2" :
                    documents = twoLevelDict.find({"topic":request.data_1,"publisher":request.data_2})
                    for document in documents:
                        pending_twoLevelDict.insert_one({"topic":document["topic"],"publisher":document["publisher"],"subscriber":document["subscriber"],"action":"remove"})
                    twoLevelDict.delete_many({"topic":request.data_1,"publisher":request.data_2})
                    logging.info("%s:%s:REMOVE 2 %s %s %s",str(datetime.now()),request.filename,request.data_1,request.data_2,"NIL")
                    
            elif request.action == "insert":
                if request.level == "3" :
                    twoLevelDict.insert_one({"topic":request.data_1,"publisher":request.data_2,"subscriber":request.data_3}) 
                    documents = twoLevelDict.find({"topic":request.data_1,"publisher":request.data_2,"subscriber":request.data_3})
                    for document in documents:
                        pending_twoLevelDict.insert_one({"topic":document["topic"],"publisher":document["publisher"],"subscriber":document["subscriber"],"action":"insert"})
                    logging.info("%s:%s:INSERT 3 %s %s %s",str(datetime.now()),request.filename,request.data_1,request.data_2,request.data_3)
                   
        elif request.filename == "frontends" :
            if request.action == "remove" :
                if request.level == "2" : 
                    if request.data_1 == "ip" :
                        pending_frontends.insert_one({"type":request.data_1,request.data_1:request.data_2,"action":"remove"})
                        frontends.delete_one({"type":request.data_1,request.data_1:request.data_2})
                        logging.info("%s:%s:REMOVE 2 %s %s %s",str(datetime.now()),request.filename,request.data_1,request.data_2,request.data_3)
                    else :
                        pending_frontends.insert_one({"type":request.data_1,request.data_1:int(request.data_2),"action":"remove"})
                        frontends.delete_one({"type":request.data_1,request.data_1:int(request.data_2)})
                        logging.info("%s:%s:REMOVE 2 %s %s %s",str(datetime.now()),request.filename,request.data_1,request.data_2,request.data_3)

            elif request.action == "insert" :
                if request.level == "2" : 
                    if request.data_1 == "ip" :
                        pending_frontends.insert_one({"type":request.data_1,request.data_1:request.data_2,"action":"insert"})
                        frontends.insert_one({"type":request.data_1,request.data_1:request.data_2})
                        logging.info("%s:%s:INSERT 2 %s %s %s",str(datetime.now()),request.filename,request.data_1,request.data_2,request.data_3)
                    else :
                        pending_frontends.insert_one({"type":request.data_1,request.data_1:int(request.data_2),"action":"insert"})
                        frontends.insert_one({"type":request.data_1,request.data_1:int(request.data_2)})
                        logging.info("%s:%s:INSERT 2 %s %s %s",str(datetime.now()),request.filename,request.data_1,request.data_2,request.data_3)
        
        channel = grpc.insecure_channel(centralServer)
        stub = pr_pb2_grpc.PublishTopicStub(channel)

        TIMEOUT = 3
        print str(TIMEOUT),"seconds to kill central server..."
        time.sleep(TIMEOUT)

        retries = 0
        while(True) :
            try :
                response = stub.commit_phase_two(request)
                if response.ack == "COMMIT":
                    pending_frontends.drop()
                    pending_twoLevelDict.drop()
                    logging.info("%s:%s:COMMIT",str(datetime.now()),request.filename)
                    return pr_pb2.acknowledge(ack="OK")
                else :
                    return pr_pb2.acknowledge(ack="ERROR")
            except :
                retries += 1
                if retries > MAX_RETRIES :
                    print "Central down..."
                    roll_back(request)
                    logging.info("%s:%s:ROLLBACK",str(datetime.now()),request.filename)
                    return pr_pb2.acknowledge(ack="ERROR")

    def commit_phase_two(self,request,context):
        if request.filename == "twoLevelDict":        
            if request.action == "remove" :
                if request.level == "3" : 
                    twoLevelDict.delete_one({"topic":request.data_1,"subscriber":request.data_3})
                    logging.info("%s:%s:REMOVE 3 %s %s %s",str(datetime.now()),request.filename,request.data_1,"NIL",request.data_3)
                    
                elif request.level == "2" :
                    twoLevelDict.delete_many({"topic":request.data_1,"publisher":request.data_2})
                    logging.info("%s:%s:REMOVE 2 %s %s %s",str(datetime.now()),request.filename,request.data_1,request.data_2,"NIL")
                    
            elif request.action == "insert":
                if request.level == "3" :
                    twoLevelDict.insert_one({"topic":request.data_1,"publisher":request.data_2,"subscriber":request.data_3}) 
                    logging.info("%s:%s:INSERT 3 %s %s %s",str(datetime.now()),request.filename,request.data_1,request.data_2,request.data_3)
                   
        elif request.filename == "frontends" :
            if request.action == "remove" :
                if request.level == "2" : 
                    if request.data_1 == "ip" :
                        frontends.delete_one({"type":request.data_1,request.data_1:request.data_2})
                        logging.info("%s:%s:REMOVE 2 %s %s %s",str(datetime.now()),request.filename,request.data_1,request.data_2,request.data_3)
                    else :
                        frontends.delete_one({"type":request.data_1,request.data_1:int(request.data_2)})
                        logging.info("%s:%s:REMOVE 2 %s %s %s",str(datetime.now()),request.filename,request.data_1,request.data_2,request.data_3)

            elif request.action == "insert" :
                if request.level == "2" : 
                    if request.data_1 == "ip" :
                        frontends.insert_one({"type":request.data_1,request.data_1:request.data_2})
                        logging.info("%s:%s:INSERT 2 %s %s %s",str(datetime.now()),request.filename,request.data_1,request.data_2,request.data_3)
                    else :
                        frontends.insert_one({"type":request.data_1,request.data_1:int(request.data_2)})
                        logging.info("%s:%s:INSERT 2 %s %s %s",str(datetime.now()),request.filename,request.data_1,request.data_2,request.data_3)
        
        logging.info("%s:%s:COMMIT",str(datetime.now()),request.filename)
        return pr_pb2.acknowledge(ack="COMMIT")

    def unsubscribeRequestCentral(self, request, context):
        print "unsubscribe request from access point",request.client_ip," for topic",request.topic
        if IS_MASTER:
            response = two_phase_init(pr_pb2.commit_req_data(action="remove",level="3",data_1 = request.topic,data_2="", data_3 = request.client_ip, filename = "twoLevelDict",function_name="unsubscribeRequestCentral"))
            if response == "ERROR" :
                twoLevelDict.delete_one({"topic":request.topic,"subscriber":request.client_ip})
        else :
            twoLevelDict.delete_one({"topic":request.topic,"subscriber":request.client_ip})
        return pr_pb2.acknowledge(ack="temporary acknowledge from central server")

    def deReplicaRequest(self, request, context):
        dct = {}
        cursor = twoLevelDict.find({"topic":request.topic})
        for document in cursor:
            if dct.has_key(document["publisher"]):
                pass
            else : dct[document["publisher"]] = []
            if document["subscriber"]!="NULL" :
                dct[document["publisher"]].append(document["subscriber"])
        if len(dct.keys()) == 1:
            return pr_pb2.acknowledge(ack="ERROR")
        extraSubscribers = dct[request.client_ip]
        if IS_MASTER:
            response = two_phase_init(pr_pb2.commit_req_data(action="remove",level="2",data_1 = request.topic,data_2=request.client_ip, data_3 = "", filename = "twoLevelDict",function_name="deReplicaRequest"))
            if response == "ERROR" :
                twoLevelDict.delete_many({"topic":request.topic,"publisher":request.client_ip})
        else :
            twoLevelDict.delete_many({"topic":request.topic,"publisher":request.client_ip})
        # twoLevelDict.delete_many({"topic":request.topic,"publisher":request.client_ip})
        del dct[request.client_ip]
        for subscriber in extraSubscribers :
            l = sys.maxsize
            tempIp = ""
            for ip in dct.keys():
                tempCursor = twoLevelDict.find({"topic":request.topic,"publisher":ip})
                if tempCursor.count() < l:
                    l = tempCursor.count()
                    tempIp = ip

            if IS_MASTER:
                response = two_phase_init(pr_pb2.commit_req_data(action="insert",level="3",data_1 = request.topic,data_2=tempIp, data_3 = subscriber, filename = "twoLevelDict",function_name="deReplicaRequest"))
                if response == "ERROR" :
                    twoLevelDict.insert_one({"topic":request.topic,"publisher":tempIp,"subscriber":subscriber})
            else :
                twoLevelDict.insert_one({"topic":request.topic,"publisher":tempIp,"subscriber":subscriber})
            # twoLevelDict.insert_one({"topic":request.topic,"publisher":tempIp,"subscriber":subscriber})
        print "Dereplication for topic server : "+request.client_ip+" started..."
        return pr_pb2.acknowledge(ack="DONE") 

    def querryTopics(self, request, context):
        cursor = twoLevelDict.find({"subscriber":"NULL"})
        for document in cursor :
            yield pr_pb2.topic(topic=document["topic"])

    def replicaRequest(self, request, context):
        document = twoLevelDict.find_one({"topic":request.topic,"subscriber":"NULL"})
        allotedServer = document["publisher"]
        if twoLevelDict.find({"topic":request.topic,"publisher":request.client_ip}).count() > 0 :
            return pr_pb2.acknowledge(ack="Requesting front end server already a replica for "+request.topic)
        if twoLevelDict.find({"topic":request.topic,"subscriber":request.client_ip}).count() > 0 :
            if IS_MASTER:
                response = two_phase_init(pr_pb2.commit_req_data(action="remove",level="3",data_1 = request.topic,data_2="", data_3 = request.client_ip, filename = "twoLevelDict",function_name="replicaRequest"))
                if response == "ERROR" :
                    twoLevelDict.delete_one({"topic":request.topic,"subscriber":request.client_ip})
            else :
                twoLevelDict.delete_one({"topic":request.topic,"subscriber":request.client_ip})
            # twoLevelDict.delete_one({"topic":request.topic,"subscriber":request.client_ip})

        if IS_MASTER:
            response = two_phase_init(pr_pb2.commit_req_data(action="insert",level="3",data_1 = request.topic,data_2=request.client_ip, data_3 = "NULL", filename = "twoLevelDict",function_name="replicaRequest"))
            if response == "ERROR" :
                twoLevelDict.insert_one({"topic":request.topic,"publisher":request.client_ip,"subscriber":"NULL"})
        else :
            twoLevelDict.insert_one({"topic":request.topic,"publisher":request.client_ip,"subscriber":"NULL"})
        # twoLevelDict.insert_one({"topic":request.topic,"publisher":request.client_ip,"subscriber":"NULL"})
        if IS_MASTER:
            response = two_phase_init(pr_pb2.commit_req_data(action="insert",level="3",data_1 = request.topic,data_2=request.client_ip, data_3 = request.client_ip, filename = "twoLevelDict",function_name="replicaRequest"))
            if response == "ERROR" :
                twoLevelDict.insert_one({"topic":request.topic,"publisher":request.client_ip,"subscriber":request.client_ip})
        else :
            twoLevelDict.insert_one({"topic":request.topic,"publisher":request.client_ip,"subscriber":request.client_ip})
        # twoLevelDict.insert_one({"topic":request.topic,"publisher":request.client_ip,"subscriber":request.client_ip})
        channel = grpc.insecure_channel(allotedServer)
        stub = pr_pb2_grpc.PublishTopicStub(channel)
        response = stub.sendBackupRequestReplica(pr_pb2.topicSubscribe(topic=request.topic, client_ip=request.client_ip))
        print "Replication for topic server : "+request.client_ip+" started..."
        return pr_pb2.acknowledge(ack="Requesting front end server "+request.client_ip+" made a replica of topic(backup sent) "+request.topic)

    def subscribeRequestCentral(self, request, context):
        print "Subscribe request from access point",request.client_ip," for topic",request.topic," of type :",request.type
        allotedServer = ""
        if request.type == "new" :
            if twoLevelDict.find({"topic":request.topic,"publisher":request.client_ip}).count() > 0:
                allotedServer = request.client_ip 
            else :
                l = sys.maxsize
                tempIp = ""
                cursor = twoLevelDict.find({"topic":request.topic,"subscriber":"NULL"})
                for document in cursor :
                    ip = document["publisher"]
                    if twoLevelDict.find({"topic":request.topic,"publisher":ip}).count() < l :
                        l=twoLevelDict.find({"topic":request.topic,"publisher":ip}).count()
                        tempIp = ip
                allotedServer = tempIp
            if IS_MASTER:
                response = two_phase_init(pr_pb2.commit_req_data(action="insert",level="3",data_1 = request.topic,data_2=allotedServer, data_3 = request.client_ip, filename = "twoLevelDict",function_name="subscribeRequestCentral"))
                if response == "ERROR" :
                    twoLevelDict.insert_one({"topic":request.topic,"publisher":allotedServer,"subscriber":request.client_ip})
            else :
                twoLevelDict.insert_one({"topic":request.topic,"publisher":allotedServer,"subscriber":request.client_ip})
            # twoLevelDict.insert_one({"topic":request.topic,"publisher":allotedServer,"subscriber":request.client_ip})

        else :
            document = twoLevelDict.find_one({"topic":request.topic,"subscriber":request.client_ip})
            allotedServer = document["publisher"]

        channel = grpc.insecure_channel(allotedServer)
        stub = pr_pb2_grpc.PublishTopicStub(channel)
        response = stub.sendBackupRequest(pr_pb2.topicSubscribe(topic=request.topic, client_ip=request.client_ip))
        print response.ack
        return pr_pb2.acknowledge(ack="temporary acknowledge from central server")

    def giveSubscriberIps(self, request, context):
        if twoLevelDict.find({"topic":request.topic,"publisher":request.client_ip}).count() == 1: 
            yield pr_pb2.ips(ip="none")
        else:
            cursor = twoLevelDict.find({"topic":request.topic,"publisher":request.client_ip})
            for document in cursor:
                if document["subscriber"]!="NULL" :
                    yield pr_pb2.ips(ip=document["subscriber"])

    def giveIps(self, request, context):
        cursor = twoLevelDict.find({"topic":request.topic,"subscriber":"NULL"})
        if cursor.count() > 0:
            for document in cursor :
                yield pr_pb2.ips(ip=document["publisher"])

        else : 
            cursor = frontends.find({"type":"ip"})
            lst = []
            for document in cursor :
                lst.append(document["ip"])
            ip = random.choice(lst)
            if IS_MASTER:
                response = two_phase_init(pr_pb2.commit_req_data(action="insert",level="3",data_1 = request.topic,data_2=ip, data_3 = "NULL", filename = "twoLevelDict",function_name="giveIps"))
                if response == "ERROR" :
                    twoLevelDict.insert_one({"topic":request.topic,"publisher":ip,"subscriber":"NULL"})
            else :
                twoLevelDict.insert_one({"topic":request.topic,"publisher":ip,"subscriber":"NULL"})
            # twoLevelDict.insert_one({"topic":request.topic,"publisher":ip,"subscriber":"NULL"})
            yield pr_pb2.ips(ip=ip)

    def getFrontIp(self, request, context) :
        # cursor = frontends.find({"type":"index"})
        # if cursor.count() == 0:
        #     return pr_pb2.ips(ip="NONE")
        # index = 0
        # for document in cursor :
        #     index = document["index"]
        # ipList = []
        # cursor = frontends.find({"type":"ip"})
        # for document in cursor :
        #     ipList.append(document["ip"])
        # m = ipList[index]
        # if index == len(ipList) - 1 and len(ipList)!=0 :
        #     if IS_MASTER:
        #         response = two_phase_init(pr_pb2.commit_req_data(action="remove",level="2",data_1 = "index",data_2=str(index), data_3 = "", filename = "frontends",function_name="getFrontIp"))
        #         if response == "ERROR" :
        #             frontends.delete_one({"type":"index","index":index})
        #     else :
        #         frontends.delete_one({"type":"index","index":index})
        #     # frontends.delete_one({"type":"index","index":index})
        #     if IS_MASTER:
        #         response = two_phase_init(pr_pb2.commit_req_data(action="insert",level="2",data_1 = "index",data_2="0", data_3 = "", filename = "frontends",function_name="getFrontIp"))
        #         if response == "ERROR" :
        #             frontends.insert_one({"type":"index","index":0})
        #     else :
        #         frontends.insert_one({"type":"index","index":0})
        #     # frontends.insert_one({"type":"index","index":0})
        # else :
        #     if IS_MASTER:
        #         response = two_phase_init(pr_pb2.commit_req_data(action="remove",level="2",data_1 = "index",data_2=str(index), data_3 = "", filename = "frontends",function_name="getFrontIp"))
        #         if response == "ERROR" :
        #             frontends.delete_one({"type":"index","index":index})
        #     else :
        #         frontends.delete_one({"type":"index","index":index})
        #     # frontends.delete_one({"type":"index","index":index})
        #     if IS_MASTER:
        #         response = two_phase_init(pr_pb2.commit_req_data(action="insert",level="2",data_1 = "index",data_2=str(index+1), data_3 = "", filename = "frontends",function_name="getFrontIp"))
        #         if response == "ERROR" :
        #             frontends.insert_one({"type":"index","index":index+1})
        #     else :
        #         frontends.insert_one({"type":"index","index":index+1})
        #     # frontends.insert_one({"type":"index","index":index+1})
        cursor = frontends.find({"type":"ip"})
        lst = []
        for document in cursor :
            lst.append(document["ip"])
        ip = random.choice(lst)
        return pr_pb2.ips(ip=ip)

    def registerIp(self, request, context) :
        if IS_MASTER:
            response = two_phase_init(pr_pb2.commit_req_data(action="insert",level="2",data_1 = "ip",data_2=request.ip, data_3 = "", filename = "frontends",function_name="getFrontIp"))
            if response == "ERROR" :
                frontends.insert_one({"type":"ip","ip":request.ip})
        else :
            frontends.insert_one({"type":"ip","ip":request.ip})
        # frontends.insert_one({"type":"ip","ip":request.ip})
        return pr_pb2.acknowledge(ack="Ip added...")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pr_pb2_grpc.add_PublishTopicServicer_to_server(CentralServer(), server)
    server.add_insecure_port(str(SELF_IP)+":"+port)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig(filename=port+'.log',format='%(message)s',filemode='w',level=logging.DEBUG)
    print SELF_IP

    selfIpDct = json.load(open("options","r"))
    virtualServer = selfIpDct["virtualServer"]
    centralServer = selfIpDct["centralServer"]
    backupCentralServer = selfIpDct["centralServerBackup"]
    channel = grpc.insecure_channel(virtualServer)
    stub = pr_pb2_grpc.PublishTopicStub(channel)
    try :
        centralServer = stub.getMasterIp(pr_pb2.empty()).ip
        backupCentralServer = stub.getBackupIp(pr_pb2.empty()).ip
        print backupCentralServer
    except :
        pass

    mongoClient = MongoClient("localhost", 27017)
    mongoClient.drop_database('CentralServer'+port)
    db = mongoClient['CentralServer'+port]
    frontends = db["frontends"]
    twoLevelDict = db["twoLevelDict"]
    pending_twoLevelDict = db["pending_twoLevelDict"]
    pending_frontends = db["pending_frontends"]
    
    print_status()

    if IS_MASTER == False : 
        channel = grpc.insecure_channel(centralServer)
        stub = pr_pb2_grpc.PublishTopicStub(channel)
        response=stub.giveDataPhaseOne(pr_pb2.empty())
        dataRecieved = json.loads(response.topic)
        for item in dataRecieved["frontend"]:
            frontends.insert(item)
        for item in dataRecieved["twoleveldict"]:
            twoLevelDict.insert(item)
        print "collections Updated in Backup... initiating Phase two"
        response = stub.giveDataPhaseTwo(pr_pb2.empty())
        print "Phase two complete"

    serve()