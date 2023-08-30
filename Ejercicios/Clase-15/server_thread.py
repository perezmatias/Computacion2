#!/usr/bin/python3
import socket, os, threading

def th_server(sock):
    print("Launching")
    while True:
        msg = sock.recv(1024)
        if msg.decode() == '\r\n':
            pass
        else:
            data = msg.decode()
            print("Received: %s" % data)
            if data == "exit\r\n":
                response = "\nAdiós\r\n".encode("utf-8")
                sock.send(response)
                print("The client closed the connection.\r\n")
                sock.close()
                break
            else:
                msg = data.upper() + "\r\n"
                sock.send(msg.encode("utf-8"))

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = ""
port = 50001

serversocket.bind((host, port))
serversocket.listen(5)

while True:
    clientsocket,addr = serversocket.accept()
    print("Got a connection from %s" % str(addr))
    msg = 'Thank for connecting'+ "\r\n"
    clientsocket.send(msg.encode('ascii'))
    th = threading.Thread(target=th_server, args=(clientsocket,))
    th.start()