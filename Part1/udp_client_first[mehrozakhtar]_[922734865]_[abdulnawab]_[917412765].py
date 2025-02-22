import socket
import sys

# INITIALIZATION --
UDP_IP = "127.0.0.1"
UDP_PORT = 2000  
BUFFER_SIZE = 4096  # Size of each chunk

# Ensure correct number of arguments
if len(sys.argv) != 2:
    print("Usage: python implement_client.py (the MB you want to send)")
    sys.exit(1)

# Convert MB input to bytes
mb = int(sys.argv[1])  # Convert user input to an integer
bytes_to_send = b"a" * (mb * 1024 * 1024)  # Creates a payload of 'a' bytes

# Create UDP Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Preparing to send {mb} MB of data to {UDP_IP}:{UDP_PORT}")

# Send data in chunks
for i in range(0, len(bytes_to_send), BUFFER_SIZE):
    chunk = bytes_to_send[i : i + BUFFER_SIZE]  # Extract chunk
    sock.sendto(chunk, (UDP_IP, UDP_PORT))  # Send chunk to server

# Send stop signal to indicate end of transmission
sock.sendto(b"STOP", (UDP_IP, UDP_PORT))  

print("Data transmission complete. Waiting for throughput response...")

# Receive throughput response from server
data, _ = sock.recvfrom(1024)  # Receive up to 1 KB (enough for throughput message)
print(f"Server response: {data.decode()} KB/s")

# Close socket
sock.close()

# --- RESOURCES / REFERENCES ---
# [1] Python Docs: socket — Low-level networking interface
#     - https://docs.python.org/3/library/socket.html
#     - Used to understand socket creation, sendto(), and recvfrom().
# 
# [2] Handling Large Byte Arrays in Python:
#     - https://docs.python.org/3/library/stdtypes.html#bytes
#     - Used `b"a" * size` to generate byte payloads efficiently.
#
# [3] Networking Best Practices:
#     - Chunked data sending approach inspired by real-world UDP implementation guides.
#     - Ensured `BUFFER_SIZE` handling avoids overloading network.
#
# [4] Python Command-Line Arguments:
#     - https://docs.python.org/3/library/sys.html
#     - Used `sys.argv` to take input from the command line properly.
