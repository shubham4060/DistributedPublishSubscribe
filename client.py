from concurrent import futures
import time
import grpc
import pr_pb2
import pr_pb2_grpc
import thread
import sys
import json
import socket
from pymongo import MongoClient

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
CENTRAL_SERVER_IP = ""
ACCESS_POINT = ""
SELF_IP=[l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

if len(sys.argv) < 2 : 
	print "ERROR : Enter the port for access point server...exiting"
	exit()
port = sys.argv[1]
self_ip = str(SELF_IP)+":"+str(port)

class Client(pr_pb2_grpc.PublishTopicServicer):
	def forwardBackup(self, request_iterator, context):
		for request in request_iterator :
			print "\nReceived new data..."
			print request
			dataDump.insert_one({"topic":request.topic,"data":request.data})
		return pr_pb2.acknowledge(ack="Data received by the client...")

def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	pr_pb2_grpc.add_PublishTopicServicer_to_server(Client(), server)
	server.add_insecure_port(self_ip)
	server.start()
	try:
		while True:
			time.sleep(_ONE_DAY_IN_SECONDS)
	except KeyboardInterrupt:
		server.stop(0)

def subscribe_topic(topic,self_ip):
	if subscribedTopics.find({"topic":topic}).count() > 0 :
		print "Already subscribed to the topic :",topic
	else :
		channel = grpc.insecure_channel(ACCESS_POINT)
		stub = pr_pb2_grpc.PublishTopicStub(channel)
		response = stub.subscribeRequest(pr_pb2.topicSubscribe(topic=topic,client_ip=self_ip))
		subscribedTopics.insert_one({"topic":topic})

def push_topic(topic,data):
	channel = grpc.insecure_channel(ACCESS_POINT)
	stub = pr_pb2_grpc.PublishTopicStub(channel)
	response = stub.publishRequest(pr_pb2.topicData(topic=topic, data=data))
	print("Ack received: " + response.ack)

def get_front_ip():
	channel = grpc.insecure_channel(CENTRAL_SERVER_IP)
	stub = pr_pb2_grpc.PublishTopicStub(channel)
	response = stub.getFrontIp(pr_pb2.empty())
	print("Frontend server Ip alloted: " + response.ip)
	if response.ip == "NONE" :
		print "No frontend servers active ...extiting..."
		exit()
	return response.ip

def generateTopics(lst,client_ip):
	for topic in lst :
		yield pr_pb2.topicSubscribe(topic=topic,client_ip=client_ip)		

if __name__ == '__main__':
	thread.start_new_thread(serve,())

	mongoClient = MongoClient("localhost", 27017)
	mongoClient.drop_database('Client'+port)
	db = mongoClient['Client'+port]
	subscribedTopics = db["subscribedTopics"]
	dataDump = db["dataDump"]

	a = json.load(open("options","r"))
	CENTRAL_SERVER_IP = a["virtualServer"]
	ACCESS_POINT = get_front_ip()

	while (True) :

		print "Type 1 for publish\nType 2 for subscribe\nType 3 for unsubscribe\nType 4 for exit"
		response = raw_input()

		if response == "1" :
			print "Enter topic"
			topic = raw_input()

			print "Enter data"
			data = raw_input()

			push_topic(topic,data)

		elif response == "2" :
			channel = grpc.insecure_channel(CENTRAL_SERVER_IP)
			stub = pr_pb2_grpc.PublishTopicStub(channel)
			responses = stub.querryTopics(pr_pb2.empty())
			topicList = []
			i = 0
			for response in responses :
				i+=1
				topicList.append(response.topic)
			cursor = subscribedTopics.find({})
			subscribedTopicsList = []
			for document in cursor:
				subscribedTopicsList.append(document["topic"])
			newTopicList = list(set(topicList) - set(subscribedTopicsList))
			i=0
			for topic in newTopicList :
				print i,": ",topic
				i+=1

			if len(newTopicList) > 0 :	
				print "Select available unsubscribed topic from above choices :"
				selectedNumber = raw_input()
				try :
					if int(selectedNumber) < len(newTopicList) :
						subscribe_topic(newTopicList[int(selectedNumber)],self_ip)
					else :
						print "Invalid option selected ..."

				except :
					print "Invalid option selected ..."

			else :
				print "No new topics found ..."

		elif response == "3" :
			cursor = subscribedTopics.find({})
			lst = []
			i = 0
			for document in cursor:
				print i,": "+document["topic"] 
				i+=1
				lst.append(document["topic"])
			unsubscribeList = []
			if len(lst) > 0 :	
				print "Select topics from above choices, seperated by spaces:"
				selectedNumbers = raw_input().split()
				for selectedNumber in selectedNumbers :
					try :
						if int(selectedNumber) < len(lst) :
							unsubscribeList.append(str(lst[int(selectedNumber)]))
						else :
							print "Invalid options selected ..."
							unsubscribeList = []
							break

					except :
						unsubscribeList = []
						print "Invalid options selected ..."

			else :
				print "No topics subscribed to ..."
			if len(unsubscribeList) > 0 :
				channel = grpc.insecure_channel(ACCESS_POINT)
				stub = pr_pb2_grpc.PublishTopicStub(channel)
				response = stub.unsubscribeRequest(generateTopics(unsubscribeList,str(SELF_IP)+":"+port))
				for topic in unsubscribeList :
					subscribedTopics.delete_one({"topic":topic})
				print "unsubscribed from topics :",unsubscribeList

		elif response == "4" :
			cursor = subscribedTopics.find({})
			lst = []
			for document in cursor:
				lst.append(document["topic"])
			channel = grpc.insecure_channel(ACCESS_POINT)
			stub = pr_pb2_grpc.PublishTopicStub(channel)
			response = stub.unsubscribeRequest(generateTopics(lst,str(SELF_IP)+":"+port))
			mongoClient.drop_database('Client'+port)
			print "exiting now..."
			exit()

		else :
			print "Invalid option selected, try again..."