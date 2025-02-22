import socket
import sys
import time

# Global constants [these constants are the same
# across both the client and the server]
UDP_IP = "127.0.0.1"
UDP_PORT = 2000
BUFFER_SIZE = 2048

if len(sys.argv) != 2:
    # Usage instructions may vary ['python ...' vs. 'python3 ...']
    # The usage discrepancy is noted within the report
    print("Usage: python3 implement_client.py <MB_of_payload>")
    print("Example: python3 implement_client.py 25")
    sys.exit(1)

# Basic error-handling
try:
    mb_int = int(sys.argv[1])
    if mb_int < 25 or mb_int > 200:
        raise ValueError("Please enter a value between 25 and 200 MB.")
except ValueError:
    print("Error: Invalid input! Please provide a numeric value between 25 and 200 MB.\n")
    sys.exit(1)

bytes_to_send = mb_int * 1000000

# Generate payload of BUFFER_SIZE
data = b'A' * BUFFER_SIZE
total_chunks = bytes_to_send // BUFFER_SIZE

# Instantiating our socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Increase the UDP buffer size (Place this line RIGHT AFTER socket creation)
# This ensures for reliable data transfer, AI suggested addition
# Note: we kept losing packest, this addition of setting the sock opt
# fields assisted us in ensuring that we had a large enough buffer to keep 
# the payload from dropping before reaching the server-side
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 40 * 1024 * 1024)

# Get current timestamp before sending data
client_timestamp = time.time()

# Print client metadata
print("\n========= CLIENT METADATA =========")
print(f"Client IP: {UDP_IP}")
print(f"Client Port: {UDP_PORT}")
print(f"Timestamp (Start of Transmission): {client_timestamp:.6f} seconds\n")


print(f"\nSending data to server! Wait until the transmission is complete...")
# Start the timer
start_time = time.time()

# Send data in chunks
for _ in range(total_chunks):
    sock.sendto(data, (UDP_IP, UDP_PORT))
    time.sleep(.00001)

# Send remaining bytes
remainder = bytes_to_send % BUFFER_SIZE
if remainder:
    leftover_data = b'A' * remainder
    sock.sendto(leftover_data, (UDP_IP, UDP_PORT))

# Send STOP marker
sock.sendto(b"STOP", (UDP_IP, UDP_PORT))

# Stop the timer
end_time = time.time()

# Try receiving data from server
try:
   # Receive throughput data
   throughput_data, server_address = sock.recvfrom(1024)
   throughput = float(throughput_data.decode())  # Convert to float (KB/s)

   # Receive bytes received by the server
   bytes_received_data, _ = sock.recvfrom(1024)
   received_bytes = int(bytes_received_data.decode())  # Convert to int

   # Receive the server timestamp
   timestamp_data, _ = sock.recvfrom(1024)
   server_timestamp = float(timestamp_data.decode())  # Convert to float

   # Compute percentage of data successfully transmitted
   percentage_received = (received_bytes / bytes_to_send) * 100

   print("\n========= SERVER RESPONSE =========")
   print(f"Server IP: {server_address[0]}")
   print(f"Timestamp (Server Received Data): {server_timestamp:.6f} seconds")
   print(f"Throughput: {throughput:.2f} KB/s")
   print(f"Bytes Sent: {bytes_to_send} bytes")
   print(f"Bytes Received by Server: {received_bytes} bytes")
   print(f"Percentage of Data Received: {percentage_received:.2f}%\n")

except socket.timeout:
    print("\nERROR: SERVER UNABLE TO REACH THE CLIENT! \n")

# Clean up resources
sock.close()

# Print Final Statistics
print("\n========= FINAL STATISTICS [CLIENT SIDE] =========")
print(f"Client IP: {UDP_IP}")
print(f"Server IP: {server_address[0] if 'server_address' in locals() else 'Unknown'}")
print(f"Total Data Sent: {bytes_to_send / 1024} KB")
print(f"Elapsed Time: {end_time - start_time:.6f} seconds")
print("=====================================\n")
