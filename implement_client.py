import socket
import sys

# INTIIALIZE
# 127.0.0.0/8
UDP_IP = "127.0.0.1"
# Random Port
UDP_PORT = 2000 
# We can adjust this later
BUFFER_SIZE = 4096 

# Get the argument from the python argument
# Convert it to bytes to send

# EXAMPLE USAGE: python implement_client.py 100
if (len(sys.argv) != 2):
    print("Usage: python implement_client.py (the mb u wanna send)")
    sys.exit(1)

# Get the arguments
mb = sys.argv[1] # The user sends "25"

 # Convert the mb to bytes
bytes_to_send = mb * 1024 * 1024
print(bytes_to_send)

# PROBLEM: Convert this bytes_to_send to actual data payload
# What would 25 mb look like in bytes?
# 25 * 1024 * 1024 = 26214400 bytes = big number

# We make chunks of 4096 bytes for the data


# Send each chunk to the server


# Create the UDP Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("mb " + str(bytes_to_send))
print("bytes_to_send " + str(bytes_to_send))
print("Sending data to server")

# Send the data to the server
sock.sendto(bytes_to_send, (UDP_IP, UDP_PORT))
sock.sendto(b"STOP", (UDP_IP, UDP_PORT)) # End marker



# close the socket
sock.close()


