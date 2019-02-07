#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, James Vo, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse


def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        code = data.split()[1]
        return(int(code))

    def get_headers(self,data):
        return None

    def get_body(self, data):
        body = data.split("\r\n\r\n")[1]
        return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    # python3 httpclient.py GET http://google.com
    def GET(self, url, args=None):
        if "http" in url or "https" in url:
            parse = urllib.parse.urlparse(url)
        else:
            url = "http://" + url
            parse = urllib.parse.urlparse(url)

        host = parse.hostname
        path = parse.path
        port = parse.port

        if not path:
            path = "/"

        if not port:
            port = 80

        request_line = "GET " + path + " HTTP/1.1\r\n"
        host_line = "Host: " + host + "\r\n"
        ua_line = "User-Agent: jv\r\n"
        accept_line = "Accept: */*\r\n"
        close_line = "Connection: close\r\n\r\n"

        headers = request_line + host_line + ua_line + accept_line + close_line
        # print(headers)
        self.connect(host, port)
        self.sendall(headers)

        returned = self.recvall(self.socket)

        code = self.get_code(returned)
        body = self.get_body(returned)

        print(body)
        self.close()

        return HTTPResponse(code, body)

    # python3 httpclient.py POST http://google.com
    def POST(self, url, args=None):
        if "http" in url or "https" in url:
            parse = urllib.parse.urlparse(url)
        else:
            url = "http://" + url
            parse = urllib.parse.urlparse(url)

        host = parse.hostname
        path = parse.path
        port = parse.port
        # content_length = 0

        if not path:
            path = "/"
        if not port:
            port = 80
        if args:
            arg = urllib.parse.urlencode(args)
            content_length = len(arg)
        else:
            arg = ""
            content_length = 0
        
        request_line = "POST " + path + " HTTP/1.1\r\n"
        host_line = "Host: " + host + "\r\n"
        accept_line = "Accept: */*\r\n"
        ct_line = "Content-Type: application/x-www-form-urlencoded\r\n"
        cl_line = "Content-Length: " + str(content_length) + "\r\n"
        close_line = "Connection: close\r\n\r\n"

        headers = request_line + host_line + accept_line + ct_line + cl_line + close_line + arg
        # print(headers)
        self.connect(host, port)
        self.sendall(headers)
        
        returned = self.recvall(self.socket)

        code = self.get_code(returned)
        body = self.get_body(returned)

        print(body)
        self.close()

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
