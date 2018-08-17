import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    data = input('请输入要发送的数据：')
    client.sendto(data.encode('utf-8'), ('127.0.0.1', 8080))
    info = client.recv(1024).decode('utf-8')
    print('服务器：', info)