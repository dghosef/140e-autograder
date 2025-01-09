import socket

# Message config
sunet = 'dghosef'
repo = 'https://github.com/dghosef/cs140e-22win/'
lab = 'lab1'
# PLEASE DO NOT MODIFY BELOW THIS LINE
assert lab in ['lab1']
message = f"{sunet} {repo} {lab}"
assert ' ' not in sunet and ' ' not in repo and ' ' not in lab, "Invalid message format"
# ngrok public address and port
host = '0.tcp.us-cal-1.ngrok.io'  # Will change every lab I think
port = 13903  # Will change every lab I think

# Connect to the listener
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

client_socket.send(message.encode())
print("Message sent!")

client_socket.close()
