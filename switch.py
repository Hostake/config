import telnetlib

# Define the switch's IP address and credentials
switch_ip = '192.168.1.1'
username = 'admin'
password = 'password'

# Define the file to save the configuration
config_file = 'switch_config.txt'

# Establish a Telnet connection to the switch
tn = telnetlib.Telnet(switch_ip)

# Login to the switch
tn.read_until(b'Username: ')
tn.write(username.encode() + b'\n')
tn.read_until(b'Password: ')
tn.write(password.encode() + b'\n')

# Enter enable mode (if required)
tn.write(b'enable\n')
tn.read_until(b'# ')

# Get the switch's configuration
tn.write(b'show running-config\n')
config = ''
while True:
    output = tn.read_until(b'# ', timeout=1).decode()
    config += output
    if '--More--' in output:
        tn.write(b' ')
    else:
        break

# Save the configuration to a file
with open(config_file, 'w') as f:
    f.write(config)

# Close the Telnet connection
tn.close()

print(f'Configuration saved to {config_file}')
