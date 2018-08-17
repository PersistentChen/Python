import socket

#  创建socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定ip端口
server.bind(('127.0.0.1', 8080))

# 监听
server.listen(5)
print('服务器启动成功...')
print('等待接收数据...')

# 等待连接
clientSocket, clientAddress = server.accept()
print('有客户端连入服务器...')

while True:
    # 接受收客户端数据
    data = clientSocket.recv(1024)
    print('收到数据：' + data.decode('utf-8'))
    sendData = input('请输入返回客户端的数据：')
    clientSocket.send(sendData.encode('utf-8'))
