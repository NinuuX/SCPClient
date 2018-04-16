#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

from sys import argv
from os import listdir
import paramiko
from scp import SCPClient

class colors:
	# class for colors
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def getAllFileList (file_ext):
	file_lst = []
	files = (file for file in listdir("./") if file.endswith(".%s"%(file_ext)))
	for file in files:
		file_lst.append(file)

	print(INFO + ", ".join(file_lst) + " IS ABOUT TO SEND!")
	return file_lst

def getArgvFileList ():
	# get list of argv if it's more than one argv -> ELSE return the argv[1]
	if len(argv) > 2:
		del argv[0]
		return argv
	else:
		return argv[1]

def createSSHClient():
	SERVER = "example.com"; PORT = "22"; USER = "NinuX"; PASSWORD= "github701"
	
	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(SERVER, PORT, USER, PASSWORD)
	return client


INFO = colors.OKGREEN + "[INFO]\t" + colors.ENDC
ERROR = colors.FAIL + "[ERR]\t" + colors.ENDC
PATH = "/var/www/html/"

try:
	ssh = createSSHClient() # create a SSH connection
	scp = SCPClient(ssh.get_transport()) # create SCP comminution

	files_lst = getArgvFileList()

	if ( len(files_lst) > 1 and type(files_lst) == list):
		scp.put( files_lst, recursive=True, remote_path=PATH)
		print(INFO + ", ".join(files_lst) + " IS ABOUT TO SEND!")

	else:
		scp.put( argv[1] if argv[1].split(".")[0] != "*" else getAllFileList(argv[1].split(".")[1]), # Check if it's a single file or 
			recursive=True,
			remote_path=PATH)


	print( INFO + " DONE!")	
	scp.close()
except:
	print(ERROR + "SOME ERROR HAS OCCUR")