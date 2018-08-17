###服务器
```python
import socket

udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udpServer.bind(('127.0.0.1', 8080))

while True:
    data, addr = udpServer.recvfrom(1024)
    print('客户端：', data.decode('utf-8'))
    info = input('请输入要发送的数据：')
    udpServer.sendto(info.encode('utf-8'), addr)
```

###客户端
```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    data = input('请输入要发送的数据：')
    client.sendto(data.encode('utf-8'), ('127.0.0.1', 8080))
    info = client.recv(1024).decode('utf-8')
    print('服务器：', info)
```