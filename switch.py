import socket

# Define the switch's IP address and credentials
switch_ip = '192.168.1.1'
username = 'admin'
password = 'password'

# Define the file to save the configuration
config_file = 'switch_config.txt'

# Establish a socket connection to the switch
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((switch_ip, 23))  # Telnet port is 23

# Login to the switch
sock.sendall(b'\n')  # Send a newline character to get the login prompt
data = ''
while 'Username:' not in data:
    chunk = sock.recv(1024)
    if chunk.startswith(b'\xff'):  # Handle Telnet commands
        # Ignore or handle the Telnet command
        continue
    data += chunk.decode('utf-8', errors='replace')  # Decode with error handling

sock.sendall(username.encode() + b'\n')
data = ''
while 'Password:' not in data:
    chunk = sock.recv(1024)
    if chunk.startswith(b'\xff'):  # Handle Telnet commands
        # Ignore or handle the Telnet command
        continue
    data += chunk.decode('utf-8', errors='replace')  # Decode with error handling

sock.sendall(password.encode() + b'\n')
data = ''
while '>' not in data and '#' not in data:
    chunk = sock.recv(1024)
    if chunk.startswith(b'\xff'):  # Handle Telnet commands
        # Ignore or handle the Telnet command
        continue
    data += chunk.decode('utf-8', errors='replace')  # Decode with error handling

# Enter enable mode (if required)
sock.sendall(b'enable\n')
data = ''
while '>' not in data and '#' not in data:
    chunk = sock.recv(1024)
    if chunk.startswith(b'\xff'):  # Handle Telnet commands
        # Ignore or handle the Telnet command
        continue
    data += chunk.decode('utf-8', errors='replace')  # Decode with error handling

# Get the switch's configuration
sock.sendall(b'show running-config\n')
config = ''
while True:
    chunk = sock.recv(1024)
    if chunk.startswith(b'\xff'):  # Handle Telnet commands
        # Ignore or handle the Telnet command
        continue
    output = chunk.decode('utf-8', errors='replace')  # Decode with error handling
    config += output
    if '--More--' in output:
        sock.sendall(b' ')
    else:
        break

# Save the configuration to a file
with open(config_file, 'w') as f:
    f.write(config)

# Close the socket connection
sock.close()

print(f'Configuration saved to {config_file}')

Найти еще
