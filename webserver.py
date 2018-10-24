import socket
import time
import pymongo
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "0.0.0.0"
hostPort = 7999

mydbclient = pymongo.MongoClient("mongodb://192.168.99.101:27018/")
mydb = mydbclient["author_db"]
authors = mydb["authors"]

class MyServer(BaseHTTPRequestHandler):
    def do_POST(self):
        print( "Incomming POST to host", self.path )
        
        if(self.path == "/create"):
            content_length = int(self.headers['Content-Length']) 
            post_data = json.loads(self.rfile.read(content_length))
            authors.insert_one(post_data)
            self.send_response(200, "OK")
            self.end_headers()

        elif(self.path == "/search"):
            content_length = int(self.headers['Content-Length']) 
            post_data = json.loads(self.rfile.read(content_length))
            searchResult = []
            for x in authors.find(post_data):
                searchResult.append(x)                
            self.send_response(200, "OK")
            self.send_header("result", searchResult)
            self.end_headers()

        elif(self.path == "/author"):
            content_length = int(self.headers['Content-Length']) 
            post_data = json.loads(self.rfile.read(content_length))
            searchResult = authors.find_one(post_data)
            self.send_response(200, "OK")
            self.send_header("author", searchResult)
            self.end_headers()

        else:
            self.send_response(404, "Not found")
            self.end_headers()
        
        

myServer = HTTPServer((hostName, hostPort), MyServer)
print("Webserver up and running at %s:%s" % (hostName, hostPort), time.asctime())

try:
	myServer.serve_forever()
except KeyboardInterrupt:
	pass

myServer.server_close()
print("Bye ", time.asctime())
