# """ Multithreaded server Receives,and send data to and from clients in JSON format """
# from IOCtrl import *
#
# import socket
# import threading
# import json
#
# IP = ''
# port = 8888
# connection_acknowledgement = "Yor are now connected to the server ! Please Send data."
# data_acknowledgement = "Looping back Received data:\t"
#
# class socketHandler(threading.Thread):
#     io_obj = IOCtrl()
#     def __init__(self,clientAddress,clientsocket):
#         threading.Thread.__init__(self)
#         self.class_socket = clientsocket
#         self.class_adress = clientAddress
#         self._running = True
#     def run(self):
#         rcv_msg = self.class_socket.recv(1024)                          # Receive 1024 Bytes
#         print(rcv_msg)
#         msg = rcv_msg.decode()                                          # Convert received byte into json string
#         rcv_dict = json.loads(msg)                                      # Convert received json string into dictionary
#
#         if rcv_dict['cmd'] == "setio":
#             print(rcv_dict)
#             self.io_obj.data_from_pytest_to_board(SPN=int(rcv_dict['spn']),val=int(rcv_dict['val1']))
#             # print ("Connection to {} closed".format(self.class_adress))
#             self.class_socket.close()   # Close Connection
#
#         elif rcv_dict['cmd'] == "getio":
#             msg = self.io_obj.data_to_pytest_from_board(SPN=int(rcv_dict['spn']))
#             self.class_socket.send(msg)                # Loop back received json string
#             # print ("Connection to {} closed".format(self.class_adress))
#             self.class_socket.close()   # Close Connection
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Socket Object
# print("Socket Successfully  Created")
# s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# s.bind(('',port)) # Bind socket to a IP, and Port
# print("Server running on %s" %(IP))
# print("Socket binded to %s" %(port))
# s.listen(10)
# print("Socket is in listening mode")
#
# while True:
#     clientsocket,clientAddress = s.accept() # Accept Connection from client
#     print("Got Connection from {}".format(clientAddress))
#     Server_Class_Thread = socketHandler(clientAddress,clientsocket) # Create Thread
#     Server_Class_Thread.start() # Start Thread

# old test code

""" Multithreaded server Receives,and send data to and from clients in JSON format """
# from IOCtrl import *
# from global_defines import *
# from UserInterface.parse_excel import *
#
# import os
# import socket
# import threading
# import json
#
# os.system("kill $(lsof -t -i:8888)") # Kill process which uses TCP Socket Address = 8888
#
# gd_obj = global_defines()
# io_obj = IOCtrl(gd_obj)
# pe     = parse_excel(gd_obj)
#
# IP = ''
# port = 8888
# connection_acknowledgement = "Yor are now connected to the server ! Please Send data."
# data_acknowledgement = "Looping back Received data:\t"
#
# class socketHandler(threading.Thread):
#
#     def __init__(self,clientAddress,clientsocket):
#         threading.Thread.__init__(self)
#         self.class_socket = clientsocket
#         self.class_adress = clientAddress
#         self._running = True
#     def run(self):
#         rcv_msg = self.class_socket.recv(1024)                          # Receive 1024 Bytes
#         msg = rcv_msg.decode()                                          # Convert received byte into json string
#         rcv_dict = json.loads(msg)                                      # Convert received json string into dictionary
#
#         if rcv_dict['cmd'] == "setio":
#             print("setio : ",rcv_dict)
#             self.io_obj.data_from_pytest_to_board(SPN=int(rcv_dict['spn']),val=int(rcv_dict['val1']))
#             #print ("Connection to {} closed".format(self.class_adress))
#             #self.class_socket.close()   # Close Connection
#
#         elif rcv_dict['cmd'] == "getio":
#             print("getio : ",rcv_dict)
#             #msg = json.dumps(rcv_dict)
#             #self.class_socket.send(msg.encode())                # Loop back received json string
#             #msg = self.IOCtrl.data_to_pytest_from_board(SPN=int(rcv_dict['spn']))
#             #self.class_socket.send(msg)                # Loop back received json string
#             # print ("Connection to {} closed".format(self.class_adress))
#             self.class_socket.close()   # Close Connection
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Socket Object
# print("Socket Successfully  Created")
# s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# s.bind(('',port)) # Bind socket to a IP, and Port
# print("Server running on %s" %(IP))
# print("Socket binded to %s" %(port))
# s.listen(10)
# print("Socket is in listening mode")
#
# while True:
#     clientsocket,clientAddress = s.accept() # Accept Connection from client
#     print("Got Connection from {}".format(clientAddress))
#     Server_Class_Thread = socketHandler(clientAddress,clientsocket) # Create Thread
#     Server_Class_Thread.start() # Start Thread

""" Multithreaded server Receives,and send data to and from clients in JSON format """
from IOCtrl import *
from global_defines import *
from UserInterface.parse_excel import *

import os
import socket
import threading
import json

os.system(
    "kill $(lsof -t -i:8888)"
)  # Kill process which uses TCP Socket Address = 8888

gd_obj = global_defines()
pe = parse_excel(gd_obj)
pe.parse_excel()
io_obj = IOCtrl(gd_obj)
print("Type Dict: \t", gd_obj.type_dict)

IP = ""
port = 8888
connection_acknowledgement = "Yor are now connected to the server ! Please Send data."
data_acknowledgement = "Looping back Received data:\t"


class socketHandler(threading.Thread):
    def __init__(self, clientAddress, clientsocket, io_obj):
        threading.Thread.__init__(self)
        self.class_socket = clientsocket
        self.class_adress = clientAddress
        self._running = True
        self.io_obj = io_obj

    def run(self):
        rcv_msg = self.class_socket.recv(1024)  # Receive 1024 Bytes
        msg = rcv_msg.decode()  # Convert received byte into json string
        rcv_dict = json.loads(msg)  # Convert received json string into dictionary

        if rcv_dict["cmd"] == "setio":
            print("setio : ", rcv_dict)
            self.io_obj.data_from_pytest_to_board(
                SPN=int(rcv_dict["spn"]), val=int(rcv_dict["val1"])
            )
            print("Connection to {} closed".format(self.class_adress))
            self.class_socket.close()  # Close Connection

        elif rcv_dict["cmd"] == "getio":
            print("getio : ", rcv_dict)
            ##msg = json.dumps(rcv_dict)
            ##self.class_socket.send(msg.encode())                # Loop back received json string
            msg = self.io_obj.data_to_pytest_from_board(SPN=int(rcv_dict["spn"]))
            print("Response to getio : \n", msg)
            self.class_socket.send(msg)  # Loop back received json string
            print("Connection to {} closed".format(self.class_adress))
            self.class_socket.close()  # Close Connection


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket Object
print("Socket Successfully  Created")
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", port))  # Bind socket to a IP, and Port
print("Server running on %s" % (IP))
print("Socket binded to %s" % (port))
s.listen(10)
print("Socket is in listening mode")

while True:
    clientsocket, clientAddress = s.accept()  # Accept Connection from client
    print("Got Connection from {}".format(clientAddress))
    Server_Class_Thread = socketHandler(
        clientAddress, clientsocket, io_obj
    )  # Create Thread
    Server_Class_Thread.start()  # Start Thread
