#-*- coding:utf-8 -*-

from pywss import pywss
import thread

ws = pywss({
	"host": "",
	"port": 1234
	})

def test(ws):
	while True:
		ws.send("hello")
		print ws.data()

while ws.handshake():
	thread.start_new(test, (ws,))