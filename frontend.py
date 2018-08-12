from concurrent import futures
import time
import grpc
import pr_pb2
import pr_pb2_grpc
import thread
import sys
import csv
from multiprocessing.dummy import Pool as ThreadPool 
import json
import socket
from pymongo import MongoClient

if len(sys.argv) < 2 : 
    print "ERROR : Enter the port for access point server...exiting"
    exit()
port = sys.argv[1]

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

CENTRAL_SERVER_IP = ""
THRESHOLD = 1
SELF_IP=[l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

def generateBackup(topic,lst) :
    for data in lst :
        yield pr_pb2.topicData(topic=topic,data=data)

def sendToFrontend(lst):
    request = lst[0]
    client_ip = lst[1]
    channel = grpc.insecure_channel(client_ip)
    stub = pr_pb2_grpc.PublishTopicStub(channel)
    response = stub.sendData(request)

def forwardBackupToClient(lst):
    requestList = lst[0]
    client_ip = lst[1]
    lst = []
    temp_topic = ""
    for request in requestList :
        lst.append(request.data)
        temp_topic = request.topic
    channel = grpc.insecure_channel(client_ip)
    stub = pr_pb2_grpc.PublishTopicStub(channel)
    response = stub.forwardBackup(generateBackup(temp_topic,lst))

def publishData(lst):
    request = lst[0]
    accesspoint = lst[1]
    channel = grpc.insecure_channel(accesspoint)
    stub = pr_pb2_grpc.PublishTopicStub(channel)
    response = stub.publish(pr_pb2.topicData(topic=request.topic, data=request.data))
    return response.ack

def register_ip():
    channel = grpc.insecure_channel(CENTRAL_SERVER_IP)
    stub = pr_pb2_grpc.PublishTopicStub(channel)
    response = stub.registerIp(pr_pb2.ips(ip = str(SELF_IP)+":"+str(port)))
    print "Ip added to central server..."

class AccessPoint(pr_pb2_grpc.PublishTopicServicer):
    def subscribeRequest(self, request, context):
        print "\nFRONTEND : new client subscriber ",request.client_ip," for topic",request.topic
        subType = ""
        if subscribers.find({"topic":request.topic}).count() > 0 :
            print "FRONTEND : Not the first client for topic ",request.topic
            subType = "old"
        else : 
            print "FRONTEND : First client for topic ",request.topic
            subType = "new"
        newSubscribers.insert_one({"topic":request.topic,"ip":request.client_ip})
        subscribers.insert_one({"topic":request.topic,"ip":request.client_ip})
        if subscribers.find({"topic":request.topic}).count() > THRESHOLD :
            channel = grpc.insecure_channel(CENTRAL_SERVER_IP)
            stub = pr_pb2_grpc.PublishTopicStub(channel)
            response = stub.replicaRequest(pr_pb2.topicSubscribe(topic=request.topic,client_ip=str(SELF_IP)+":"+port))

        channel = grpc.insecure_channel(CENTRAL_SERVER_IP)
        stub = pr_pb2_grpc.PublishTopicStub(channel)
        response = stub.subscribeRequestCentral(pr_pb2.topicDataType(topic=request.topic,client_ip=str(SELF_IP)+":"+str(port),type=subType))
        return pr_pb2.acknowledge(ack="temporary acknowledge")

    def unsubscribeRequest(self, request_iterator, context):
        topicList = []
        client_ip = ""
        for request in request_iterator :
            print "FRONTEND : Unsubscribe request from client",request.client_ip," for topic",request.topic
            client_ip = request.client_ip
            topicList.append(request.topic)
        for topic in topicList :
            subscribers.delete_one({"topic":topic,"ip":client_ip})
            count = subscribers.find({"topic":topic}).count() 
            if count <= THRESHOLD and count > 0 :
                channel = grpc.insecure_channel(CENTRAL_SERVER_IP)
                stub = pr_pb2_grpc.PublishTopicStub(channel)
                response = stub.deReplicaRequest(pr_pb2.topicSubscribe(topic=topic,client_ip=str(SELF_IP)+":"+port))
                if response.ack == "DONE" :
                    dataDump.delete_many({"topic":topic})
                    print "TOPIC_SERVER : Dereplicated for topic :",topic
            else :
                channel = grpc.insecure_channel(CENTRAL_SERVER_IP)
                stub = pr_pb2_grpc.PublishTopicStub(channel)
                response = stub.unsubscribeRequestCentral(pr_pb2.topicSubscribe(topic=topic,client_ip=str(SELF_IP)+":"+port))
        return pr_pb2.acknowledge(ack="done")

    def sendBackup(self, request_iterator, context):
        requestList = []
        topic = ""
        for request in request_iterator :
            requestList.append(request)
            topic = request.topic
        cursor = newSubscribers.find({"topic":topic})
        pool = ThreadPool(cursor.count()) 
        lst = []
        for document in cursor:
            lst.append([requestList,document["ip"]])
        results = pool.map(forwardBackupToClient, lst)
        newSubscribers.delete_many({"topic":topic})
        return pr_pb2.acknowledge(ack="complete data backup received and forwarded to resepective clients...")

    def sendData(self, request, context):
        cursor = subscribers.find({"topic":request.topic})
        pool = ThreadPool(cursor.count()) 
        lst = []
        for document in cursor:
            lst.append([[request],document["ip"]])
        results = pool.map(forwardBackupToClient, lst)
        return pr_pb2.acknowledge(ack="data sent to subscribed clients")

    def sendBackupRequest(self, request, context):
        cursor = dataDump.find({"topic":request.topic})
        lst = []
        for document in cursor:
            lst.append(document["data"])
        channel = grpc.insecure_channel(request.client_ip)
        stub = pr_pb2_grpc.PublishTopicStub(channel)
        response = stub.sendBackup(generateBackup(request.topic,lst))
        return pr_pb2.acknowledge(ack="data send to : "+request.client_ip+" complete...")

    def sendBackupRequestReplica(self, request, context):
        print "TOPIC_SERVER : Sending data backup for topic : "+request.topic+" to the new replica : "+request.client_ip
        cursor = dataDump.find({"topic":request.topic})
        lst = []
        for document in cursor:
            lst.append(document["data"])
        channel = grpc.insecure_channel(request.client_ip)
        stub = pr_pb2_grpc.PublishTopicStub(channel)
        response = stub.sendBackupReplica(generateBackup(request.topic,lst))
        return pr_pb2.acknowledge(ack="data send to : "+request.client_ip+" replica complete...")

    def sendBackupReplica(self, request_iterator, context):
        requestList = []
        for request in request_iterator :
            requestList.append(request)
        topic = ""
        for request in requestList :
            dataDump.insert_one({"topic":request.topic,"data":request.data})
            topic = request.topic
        print "Replication complete for topic : "+topic
        return pr_pb2.acknowledge(ack="complete data backup received by the replica...")

    def publishRequest(self, request, context):
        print "FRONTEND : Data received for topic : "+request.topic
        channel = grpc.insecure_channel(CENTRAL_SERVER_IP)
        stub = pr_pb2_grpc.PublishTopicStub(channel)
        responses = stub.giveIps(pr_pb2.topic(topic=request.topic))
        returned_ips =[]
        for response in responses :
            print("FRONTEND : Data to be sent to topic server IP: " + response.ip + " for topic: "+request.topic)
            returned_ips.append(response.ip)
        lst = []
        pool = ThreadPool(len(returned_ips)) 
        for returned_ip in returned_ips :
            lst.append([request,returned_ip])
        results = pool.map(publishData, lst)
        return pr_pb2.acknowledge(ack="Published in "+str(len(results))+" topic servers")

    def publish(self, request, context):
        print "TOPIC_SERVER : Data received for topic : "+request.topic
        dataDump.insert_one({"topic":request.topic,"data":request.data})
        channel = grpc.insecure_channel(CENTRAL_SERVER_IP)
        stub = pr_pb2_grpc.PublishTopicStub(channel)
        responses = stub.giveSubscriberIps(pr_pb2.topicSubscribe(topic=request.topic,client_ip=str(SELF_IP)+":"+port))
        ipList = []
        for response in responses :
            ipList.append(response.ip)
            print("TOPIC_SERVER : frontend subscriber IP received: " + response.ip +" for topic: "+request.topic)
        if ipList[0] == "none" :
            return pr_pb2.acknowledge(ack="No subscribers for this replica")
        pool = ThreadPool(len(ipList)) 
        lst = []
        for client_ip in ipList:
            lst.append([request,client_ip])
        results = pool.map(sendToFrontend, lst)
        return pr_pb2.acknowledge(ack="Data send to clients complete")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pr_pb2_grpc.add_PublishTopicServicer_to_server(AccessPoint(), server)
    server.add_insecure_port(str(SELF_IP)+':'+port)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    a = json.load(open("options","r"))
    CENTRAL_SERVER_IP = a["virtualServer"]
    register_ip()

    mongoClient = MongoClient("localhost", 27017)
    mongoClient.drop_database('Frontend'+port)
    db = mongoClient['Frontend'+port]
    dataDump = db["dataDump"]
    subscribers = db["subscribers"]
    newSubscribers = db["newSubscribers"]

    serve()