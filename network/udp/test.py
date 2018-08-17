'''
tcp 是建立可靠的连接，并且同心双方可以以流的方式发送数据
相对于tcp， udp是面向无连接的协议
使用udp协议时，不需要建立连接，只需要知道对方IP和端口号，就可以发送数据，但是能不能到达不可知
udp常用于广播
'''

import socket
import time

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.connect(('', 8080))

while True:
    udp.send('...'.encode('utf-8'))
    time.sleep(2)
