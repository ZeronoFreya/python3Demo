# Written by Vamei
print('localhost:8090/*.user.js')
import socket

# Address
HOST = ''
PORT = 8090

# Configure socket
s    = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

# infinite loop, server forever
while True:
    # 3: maximum number of requests waiting
    s.listen(3)
    conn, addr = s.accept()
    request    = conn.recv(1024).decode()
    method    = request.split(' ')[0]
    src            = request.split(' ')[1]
    # deal with GET method
    if method == 'GET':
        # ULR
        if src.endswith('.user.js'):
            with open( src.lstrip('/'), 'rb') as f:
                content = f.read()
                #print ('Connected by', addr)
                #print ('Request is:', request)
                conn.sendall(content)
    # close connection
    conn.close()