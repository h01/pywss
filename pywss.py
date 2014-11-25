#-*- coding:utf-8 -*-
'''
	@name		Python WebSocket Server
	@blog		https://ursb.org
	@github		https://github.com/h01/pywss
	@update		2014/10/30
	@author		Holger
	@version	1.0
'''
import socket, re
from base64  import b64encode
from hashlib import sha1

class pywss:
	def __init__(self, obj):
		self.host = obj['host']
		self.port = obj['port']
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((self.host, self.port))
		self.sock.listen(0)
	def getValue(self, key, data):
		try:
			tmp = re.findall("%s: ([\w\S]*)"%key, data)
			return tmp[0]
		except:
			return ""
	def handshake(self):
		self.client, self.info = self.sock.accept()
		data = self.client.recv(1024)
		try:
			key = self.getValue("Sec-WebSocket-Key", data)
			key = b64encode(sha1(key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").digest())
			ori = self.getValue("Origin", data)
			wss = "ws://%s/"%self.getValue("Host", data)
			self.client.send("HTTP/1.1 101 Web Socket Protocol Handshake\r\nUpgrade: webSocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: %s\r\nSec-WebSocket-Origin: %s\r\nSec-WebSocket-Location: %s\r\n\r\n"%(key, ori, wss))
			return True
		except Exception, ex:
			print ex
			return False
	def send(self, data):
		temp = "\x81"
		leng = len(data)
		if leng < 125:
			temp += chr(leng)
		else:
			temp += chr(126)
			temp += chr(leng >> 8)
			temp += chr(leng & 0xFF)
		temp += data
		self.client.send(temp)
	def data(self):
		temp = self.client.recv(1024)
		if not len(temp):
			return False
		else:
			leng = ord(temp[1]) & 127
			if leng == 126:
				masks = temp[4:8]
				datas = temp[8:]
			elif leng == 127:
				masks = temp[10:14]
				datas = temp[14:]
			else:
				masks = temp[2:6]
				datas = temp[6:]
		temp = ""
		for i in range(len(datas)):
			temp += chr(ord(datas[i]) ^ ord(masks[i % 4]))
		return temp