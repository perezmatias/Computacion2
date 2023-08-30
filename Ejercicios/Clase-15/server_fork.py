#!/usr/bin/python3
import socket, os, sys
import signal

signal.signal(signal.SIGCHLD, signal.SIG_IGN)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#host = socket.gethostname()
host = ""
#port = int(sys.argv[1])
port = 50002

serversocket.bind((host, port))
serversocket.listen(5)

while True:
    clientsocket, addr = serversocket.accept()
    print("connection from %s" % str(addr))
    msg = "thanks for the connection"+ "\r\n"
    clientsocket.send(msg.encode('ascii'))
    try:
        child_pid = os.fork()
        if not child_pid:
            while True:
                msg = clientsocket.recv(1024)
                if not msg.decode():
                    break
                else:
                    data = msg.decode()
                    print("Received: %s" % data)
                    if data == "exit\r\n":
                        response = "\nAdiós\r\n".encode("utf-8")
                        clientsocket.send(response)
                        clientsocket.close()
                        print("The client %s closed the connection\r\n" % str(addr))
                        sys.exit(0)
                    else:
                        msg = data.upper()+"\r\n"
                        clientsocket.send(msg.encode("utf-8"))

    except BrokenPipeError:
        print("The client closed the connection.")

    clientsocket.close()