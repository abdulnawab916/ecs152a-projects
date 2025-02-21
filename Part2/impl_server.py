# SERVER
#
import socket, json

# Create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket to SERVER address and port
server_host = '127.0.0.1'
server_port = 7000
server_socket.bind((server_host, server_port))

# LISTEN
server_socket.listen(1)
print(f"SERVER: LISTENING on {server_host}:{server_port}")


# By going to the client, we'll be sending data to the proxy
 # client -> proxy -> server
 # server -> proxy -> client

# LOOP to accept incoming connections
# We need to make it work with json
while True:
    # Accept connection from a client
    # server_socket.accept() returns a tuple (client_socket, client_address)
    client_socket, client_address = server_socket.accept()
    print(f"SERVER: Connected socket {client_address}")
    
    # TRY / FINALLY
    try:
        # RECEIVE data from client
        data = client_socket.recv(4096).decode()
        print(f"SERVER: Received: {data}")

        # We need to parse the json data
        # Load it from the DATA
        request = json.loads(data)

        # Get from the message field in the json 
        msg = request['message']
        print(f"SERVER: The message from JSON: {msg}")

        # Extract message from JSON
        sendresponse = json.dumps({"message": msg})

        # SEND back the message to proxy
        client_socket.sendall(sendresponse.encode())
        print(f"SERVER: Sending response: {sendresponse}")

    finally:
        # Close connection
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


"""