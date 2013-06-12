#!/usr/bin/python

# simple HTTP server reporting its port number in responses to
# GET. Can be used for example to verify load balancing.
# 
# Spawn of 5 of them on 9001-5:
# for i in {1..5}; do ./port_report_http.py 900${i} &; done

import sys
import mimetypes
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

port = int(sys.argv[1])

class PortReportHandler(SimpleHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        ctype = mimetypes.types_map['.txt']
        self.send_header('Content-type', ctype)
        resp = str(self.server.server_port) + "\n"
        self.send_header('Content-Length', len(resp))
        self.end_headers()
        self.wfile.write(resp)
     
HandlerClass = PortReportHandler
ServerClass  = BaseHTTPServer.HTTPServer
Protocol     = "HTTP/1.0"

port = int(sys.argv[1])
server_address = ('0.0.0.0', port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)

sa = httpd.socket.getsockname()
print "Serving HTTP on", sa[0], "port", sa[1], "..."
httpd.serve_forever()
