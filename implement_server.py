import socket
import time

# INITIALIZATION--
# 127.0.0.0/8
UDP_IP = "127.0.0.1"
# Random Port
UDP_PORT = 2000 
# We can adjust this later
BUFFER_SIZE = 4096 

# Create the timer to calculate throughput
start_time = 0
end_time = 0

# Create a byte thingy to store all the data
total_data = bytearray()

# Create a value for the throughput
throughput = 0

# Create the UDP Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Loop to receive the expected number of data chunks
while True:
    # Receive the data from the client
    data, addr = sock.recvfrom(BUFFER_SIZE) # DATA [aaaa , (aaaaaa)]

    # Start the timer to calculate throughput
    if start_time == 0:
        start_time = time.time()

    # Append the data to the total_data
    total_data.append(data)
    # 00101000101010101010101

    print(f"Received message: {data.decode()} from {addr}")
    if data.decode() == "STOP": # Found the end marker!
        break 

# End the timer?
end_time = time.time()

# Calculate the throughput
# How do we do (total data)/(total time)?
throughput = ((len(total_data)) / 1000 ) / (end_time - start_time) # kilobytes / total time


print(throughput)


# Send the throughput back to the client
sock.sendto(throughput, addr)


# Close the socket
sock.close()