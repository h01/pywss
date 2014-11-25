Pywss:Python websocket Server
====
简介
---
	pywss是Python websocket server的简称。顾名思义，就是python写的websocket服务端。
用法
----
### 导入模块
```python
from pywss import pywss
```
### 初始化
```python
ws = pywss({
	"host": "",		// 绑定的IP，可留空
	"port": 1234	// 监听的端口
})
```
### 监听握手数据并建立连接通信
```python
while ws.handshake():
	while True:
		ws.send("hello")
		print ws.data()
```
### 如果要多线程连接多个客户端（一般情况都这样），则放入多线程即可
```python
def test(ws):
	while True:
		ws.send("hello")
		print ws.data()

while ws.handshake():
	thread.start_new(test, (ws,))
```
	demo可参考test.py和client.html
