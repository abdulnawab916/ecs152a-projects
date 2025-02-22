3# Importing the needed libraries
import socket
import time

# Server Constants
UDP_IP = "127.0.0.1"
UDP_PORT = 2000
BUFFER_SIZE = 2048
END_MARKER = b"STOP"

# Create and bind UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"UDP server listening on {UDP_IP}:{UDP_PORT}")

# Initialize variables
total_bytes = 0
start_time = 0.0
client_addr = None

# Start receiving data
while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)

    # Store client address
    # If no client address, then assign the client address
    # To what was recieved
    if client_addr is None:
        client_addr = addr
    
    # Start timer on first packet
    if start_time == 0.0:
        start_time = time.time()

    # Check for the stop marker to end the transmission
    # When stop marker is seen, then we break out of the
    # while-loop
    if data == END_MARKER:
        break

    # Increment received byte count each time
    # we recieve data
    total_bytes += len(data)

# Capture the timestamp when the last packet was received
end_time = time.time()

# Duration calculation, if start time is 0 or less, then we return 0
duration = end_time - start_time if start_time > 0 else 0

# Calculate throughput (KB/s), return '0' if the timer didn't start
# or if there was some error [such as a negative time, which can't exist]
# 0 will be the return value in both of these cases
throughput_kb_s = (total_bytes / 1000) / duration if duration > 0 else 0

# Print statistics, AI made this a bit prettier
print("\n========= FINAL STATISTICS [SERVER SIDE] =========")
print(f"Client IP: {client_addr[0]}")
print(f"Server IP: {UDP_IP}")
print(f"Timestamp (Start of Reception): {start_time:.6f} seconds")
print(f"Timestamp (End of Reception): {end_time:.6f} seconds")
print(f"Total Data Received: {total_bytes} bytes")
print(f"Elapsed Time: {duration:.6f} seconds")
print(f"Throughput: {throughput_kb_s:.2f} KB/s")
print("======================================\n")

# Convert data to strings before sending
throughput_message = f"{throughput_kb_s:.2f}".encode()
bytes_received_message = f"{total_bytes}".encode()
timestamp_message = f"{end_time}".encode()

# Send each piece of data separately
sock.sendto(throughput_message, client_addr)
sock.sendto(bytes_received_message, client_addr)
sock.sendto(timestamp_message, client_addr)

# Clean up resources assoc. with the socket
sock.close()
