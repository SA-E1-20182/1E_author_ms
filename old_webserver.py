import socket
import time
import pymongo
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "0.0.0.0"
hostPort = 7999

#mydbclient = pymongo.MongoClient("mongodb://192.168.99.101:27018/")
mydbclient = pymongo.MongoClient("mongodb://localhost:27018/")

mydb = mydbclient["author_db"]
authors = mydb["authors"]

class MyServer(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) 
        post_data = json.loads(self.rfile.read(content_length))
        authors.insert_one(post_data)
        self.send_response(200, "OK")
        self.end_headers()

    def do_GET(self):
        url = self.path.split("/")
        searchResult = authors.find_one("'username':'"+url[2]+"'")
        self.send_header("author", searchResult)
        self.send_response(200, "OK")
        self.end_headers()

    def do_PUT(self):
        url = self.path.split("/author/addproject/")
        
        if(self.path == "/author/addproject/"):

            content_length = int(self.headers['Content-Length'])
            data = json.dumps(self.rfile.read(content_length))
            myquery = { "username": "" }
            newvalues = { "$push": { "projects":  ""} }
            self.send_response(200, "OK")
            self.end_headers()
        elif(self.path == "/author/dropproject"):
            self.send_response(200, "OK")
            self.end_headers()

    def do_DELETE(self):
        myquery = { "username": "Mountain 21" }
        self.send_response(200, "OK")
        self.end_headers()
            

myServer = HTTPServer((hostName, hostPort), MyServer)
print("Webserver up and running at %s:%s" % (hostName, hostPort), time.asctime())

try:
	myServer.serve_forever()
except KeyboardInterrupt:
	pass

myServer.server_close()
print("Bye ", time.asctime())
