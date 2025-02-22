# PROXY CODE
# FROM TEMPLATE
# https://www.bomberbot.com/proxy/building-a-tcp-proxy-server-in-python-a-comprehensive-guide/
#
import socket, json
import sys

# Addresses
proxy_host = "127.0.0.1"
proxy_port = 9000

blocked_ips = {"127.0.0.4", "127.0.1.4"} # Examples

# PROXY, handle stuff from client
def handle_client(client_socket):
    # Receive data from client
    data = client_socket.recv(4096).decode()

    # Parse JSON data from the client
    # What we need to do?
    # Get the server_ip, server_port, and message from the json data
        # Because we need to send it to server through this proxy
    jsonDATA = json.loads(data) # Load the data
    server_ip = jsonDATA['server_ip']
    server_port = jsonDATA['server_port']
    message = jsonDATA['message']

    # Print the JSON data request
    print(f"\n✅[PROXY] Received from CLIENT: {jsonDATA}")

    # ERROR: Check Blocked IP's. If IP is blocked, return error message to the client
    if server_ip in blocked_ips:
        error = json.dumps({"error": "Blocked IP"})

        # Send to client about blocked IP
        client_socket.sendall(error.encode())
        client_socket.close()
        return


    # SERVER ---------
    # Add proxy IP to the json data to send
    jsonDATA["proxy_ip"] = proxy_host
    jsonDATA["proxy_port"] = proxy_port

    # Forward to server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((server_ip, server_port))
    server_socket.sendall(json.dumps(jsonDATA).encode())
    print(f"[PROXY] Forwarded to SERVER: {jsonDATA}")

    # Receive from server
    server_response = server_socket.recv(4096).decode()
    print(f"[PROXY] Received from SERVER: {server_response}")

    # CLIENT ---------
    # Forward to client
    client_socket.sendall(server_response.encode())
    print(f"[PROXY] Forwarded to CLIENT: {server_response}")

    # ----------------
    # Close all the sockets
    server_socket.close()
    client_socket.close()

# MAIN METHOD
# Using the proxy template as a guide
def main():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((proxy_host, proxy_port))
    proxy_socket.listen(5)
    print(f"[PROXY] LISTENING on {proxy_host}:{proxy_port}")

    # If press ctrl+c, make sure it stops the program?

    # Always on
    while True:
        client_socket, addr = proxy_socket.accept()
        handle_client(client_socket)



if __name__ == '__main__':
    main()

#
# RESOURCES
"""
1. Example of creating TCP Client and server proxy, PROXY TEMPLATE
https://www.bomberbot.com/proxy/building-a-tcp-proxy-server-in-python-a-comprehensive-guide/
 - 

"""