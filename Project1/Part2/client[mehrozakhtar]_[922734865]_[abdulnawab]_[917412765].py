# CLIENT
#
import socket, json
import sys

# Proxy addresses
proxy_ip = "127.0.0.1"
proxy_port = 9000 # Proxy is port 9000
msg = "" # Initialize the message you want to send over

# ERROR CHECKING: Check if the user input is a 4 character string
if len(sys.argv) == 2 and len(sys.argv[1]) == 4:
    # Parse the argument message
    msg = sys.argv[1]
else:
    print("[CLIENT] Usage: python impl_client.py (4 char string)")
    sys.exit(1)

# Create TCP client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Try Catch here to handle connection errors
try:
    # CONNECT to PROXY
    client_socket.connect((proxy_ip, proxy_port))

    # Make the JSON request format
    # This is the destination server
    data = {
        "server_ip": '127.0.0.1',
        "server_port": 7000,
        "message": msg
    }

    # SEND JSON message TO PROXY
    # Need to encode the data to send it over, 
    # We're basically getting the data DICT and converting it to json format
    # Then, encode to bytes and SEND
    sendresponse = json.dumps(data)
    client_socket.sendall(sendresponse.encode())
    print(f"\n[CLIENT] Sending response: {sendresponse}")

    # RECEIVE response from PROXY
    response = client_socket.recv(4096).decode()
    print(f"\n✅[CLIENT] Received from PROXY: {response}")

# Close
finally:
    # CLOSE, END CONNECTION
    client_socket.close()

#
# RESOURCES
"""
1. Example of creating TCP Client and server proxy
https://www.bomberbot.com/proxy/building-a-tcp-proxy-server-in-python-a-comprehensive-guide/

2. Socket documentation
https://docs.python.org/3/library/socket.html
- SERVER:
 - socket.listen(n)	                || n clients maximum in queue)
 - socket.accept()	                || accept connection
 - socket.recv(1024)	            || receive data (1024 bytes each time)
 - socket.sendall(data.encode())    || send the encoded data

 3. JSON documentation
 https://www.w3schools.com/python/ref_string_encode.asp
 - json.dumps(data)                 || convert dictionary to JSON
    - Default goes to UTF-8
    - 'utf-8' is more safe b/c we are talking to different machines
    - known as a best practice

"""
