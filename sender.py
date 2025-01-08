import socket

# Message config
sunet = 'dghosef'
repo = 'https://github.com/dghosef/test2'
lab = 'test'
# PLEASE DO NOT MODIFY BELOW THIS LINE
message = f"{sunet} {repo} {lab}"
assert ' ' not in sunet and ' ' not in repo and ' ' not in lab, "Invalid message format"
# ngrok public address and port
host = '0.tcp.us-cal-1.ngrok.io'  # Will change every lab I think
port = 10066  # Will change every lab I think

# Connect to the listener
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

client_socket.send(message.encode())
print("Message sent!")

client_socket.close()