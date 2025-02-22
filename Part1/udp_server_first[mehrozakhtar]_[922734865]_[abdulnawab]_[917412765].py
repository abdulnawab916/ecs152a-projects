import socket
import time

# INITIALIZATION--
UDP_IP = "127.0.0.1"
UDP_PORT = 2000  # Random Port
BUFFER_SIZE = 4096  # Adjustable buffer size

# Timer to calculate throughput
start_time = 0.0
end_time = 0.0

# Store received data
total_data = bytearray()

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Loop to receive data
while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)  # Receive data from client
    
    # Start the timer when first data chunk arrives
    if start_time == 0.0:
        start_time = time.time()

    # Check if it's the stop signal
    if data.decode(errors="ignore") == "STOP":
        break

    # Append received data
    total_data.extend(data)

    print(f"Received message: {data[:50].decode(errors='ignore')}... from {addr}")
# End the timer after receiving all data
end_time = time.time()

# Avoid division by zero if no data was received
if start_time == end_time:
    throughput = 0.0
else:
    throughput = (len(total_data) / 1000) / (end_time - start_time) # KB/s

print(f"Throughput: {throughput:.2f} KB/s")

# Send the throughput back to the client (converted to bytes)
sock.sendto(str(throughput).encode(), addr)

# Close the socket
sock.close()

# --- RESOURCES / REFERENCES ---
# [1] Python Docs: socket — Low-level networking interface
#     - https://docs.python.org/3/library/socket.html
#     - Used to understand socket creation, recvfrom(), and sendto()
# 
# [2] Bytearray Methods - Official Python Docs
#     - https://docs.python.org/3/library/functions.html#bytearray
#     - Learned about bytearray.extend() instead of append() for handling received data.
#
# [3] Avoiding decode() errors in networking applications:
#     - StackOverflow discussion on handling binary data safely in sockets
#     - https://stackoverflow.com/questions/44024900
#     - Used `decode(errors="ignore")` to avoid crashing on non-text data.
#
# [4] Calculating Throughput Formula:
#     - General formula: Data Size (KB) / Time Taken (s)
#     - Referenced networking throughput calculation principles.
