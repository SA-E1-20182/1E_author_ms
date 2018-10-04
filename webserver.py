import socket
import time
import pymongo
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = ""
hostPort = 8000

mydbclient = pymongo.MongoClient("mongodb://localhost:27017/")
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
            
        #elif(self.path == "/addProject"):
            

        #elif(self.path == "/removeProject"):

        else:
            self.send_response(404, "Not found")
            self.end_headers()
        
        

myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
	myServer.serve_forever()
except KeyboardInterrupt:
	pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
