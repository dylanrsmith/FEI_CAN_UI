# import socket
# import json
# import os

# val1 = 1.1
# val2 = 2.2
# val3 = 3.3

# """ Check Seat Status """
# send_msg_string = {"cmd": "Test", "type": "type", "spn": "542", "val1": val1, "val2": val2, "val3": val1}

# send_msg = json.dumps(send_msg_string)  # Convert Dictionary to json string

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a socket object

# host = ''  # get server/host machine IP
# port = 8888  # get server/host machine Port

# print("Connecting to the server... \n")

# #s.connect((host,port))

# print("Connected to the server \n")

# print("Send the string to the server: ", send_msg)
# s.send(send_msg.encode())  # Send message to server
# #os.exit()
# os.system("pkill -f TestClient.py") # Kill any process which uses TCP Socket Address = 8888
