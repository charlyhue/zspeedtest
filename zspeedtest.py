#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import time
import SimpleHTTPServer # importe un ensemble d'instructions pour servir les requêtes http.
import SocketServer     # importe un ensemble d'instructions pour connecter le programme.
import sys
import os.path
import subprocess
from datetime import datetime
import time
import argparse

parser = argparse.ArgumentParser(description="Web speedtes graphs")
parser.add_argument('-p', '--port', type=int, help='Web UI port', default=8080)
parser.add_argument('-w', '--wait', type=int, help='Time between speedtests in seconds', default=600)

args = parser.parse_args()


csvFile="stats.csv"


running = True

def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True, 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

def check_speedtest():
	if not cmd_exists("speedtest-cli"):
		sys.exit("Missing speedtest-cli")

	if not cmd_exists("speedtest-csv") :
		sys.exit("Missing speedtest-csv")

def setup():
	if not os.path.isfile(csvFile):
		os.system("speedtest-csv --header --sep ',' > " + csvFile)
	

def speedtest():
	while running:
		os.system("speedtest-csv --sep ',' >> " + csvFile)
		a = datetime.now()
		while (datetime.now() - a).seconds < args.wait:
			if not running:
				break
			else:
				time.sleep(1)

def webServer():
	Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
	httpd = SocketServer.TCPServer(("", args.port), Handler)
	print "serving at port", args.port, "with speedtest delay as ", args.wait, "seconds"
	httpd.serve_forever()


try:
	check_speedtest()
	setup()
	t1 = threading.Thread(target=speedtest)
	t1.start()
	webServer()
except KeyboardInterrupt:
	running = False
	print "Waiting for current speedtest"
	t1.join()