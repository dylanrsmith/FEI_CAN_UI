# """ Multithreaded server Receives,and send data to and from clients in JSON format """
# import os
# import socket
# import threading
# import json
# import subprocess

# # Not compatible with Windows
# # os.system("kill $(lsof -t -i:8888)") # Kill any process which uses TCP Socket Address = 8888

# IP = ""
# port = 8888

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket Object
# print("Socket Successfully  Created")
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s.bind(("", port))  # Bind socket to a IP, and Port
# # print("Server running on %s" %(IP))
# # print("Socket binded to %s" %(port))
# # s.listen(20)
# print("Socket is in listening mode")


# class socketHandler(threading.Thread):
#     def __init__(self, clientAddress, clientsocket, io_obj):
#         threading.Thread.__init__(self)
#         self.class_socket = clientsocket
#         self.class_adress = clientAddress
#         self._running = True
#         self.io_obj = io_obj

#     def run(self):
#         rcv_msg = self.class_socket.recv(1024)  # Receive 1024 Bytes
#         msg = rcv_msg.decode()  # Convert received byte into json string
#         rcv_dict = json.loads(msg)  # Convert received json string into dictionary
#         # print("Received Message  :\n",rcv_dict)

#         if rcv_dict["cmd"] == "setio":
#             print("setio : \n", rcv_dict)
#             self.io_obj.data_from_pytest_to_board(
#                 SPN=int(rcv_dict["spn"]), val=int(rcv_dict["val1"])
#             )
#             # print ("Connection to {} closed".format(self.class_adress))
#             self.class_socket.close()  # Close Connection

#         elif rcv_dict["cmd"] == "getio":
#             print("getio : \n", rcv_dict)
#             msg = self.io_obj.data_to_pytest_from_board(SPN=int(rcv_dict["spn"]))
#             print("\n Response to getio : \n", msg)
#             self.class_socket.send(msg)
#             # print ("Connection to {} closed".format(self.class_adress))
#             self.class_socket.close()  # Close Connection
#         elif rcv_dict["cmd"] == "Test":
#             print("Socket communication Tested and Working")


# class socket_py:
#     def __init__(self, io):
#         self.io_obj = io
#         self.TestFlag = 0
#         if self.TestFlag == 0:
#             # subprocess.Popen(['sys.executable','/home/pi/Desktop/Bench_Code/TestClient.py'],shell=True)
#             os.system("python3 TestClient.py")
#             self.TestFlag = 1

#     def accept_socket(self):
#         clientsocket, clientAddress = s.accept()  # Accept Connection from client
#         # print("Got Connection from {}".format(clientAddress))
#         Server_Class_Thread = socketHandler(
#             clientAddress, clientsocket, self.io_obj
#         )  # Create Thread
#         Server_Class_Thread.start()  # Start Thread
#         threading.Timer(1, self.accept_socket).start()
