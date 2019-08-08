import socket

def Main():
    host = "127.0.0.1"
    port = 5000
    s = socket.socket()
    s.bind((host, port))
    s.listen(1) # queue length for connection requests = 1
    connection, addr = s.accept() # connection acceptance
    print "Connection from: " + str(addr)
    while True:
        data = connection.recv(1024) # 1024 bytes
        if not data: # look for non-data packet (e.g. tcp fin)
            print "Connection terminated"
            break
        print "Data = " + str(data)
        data = str(data).upper()
        print "Sending: " + str(data)
        connection.send(data)
    connection.close()

if __name__ == '__main__':
    Main()
