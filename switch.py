import pexpect
import getpass

# Get the switch IP address and username from the user
switch_ip = input("Enter the switch IP address: ")
username = input("Enter the username: ")

# Get the password from the user without echoing
password = getpass.getpass("Enter the password: ")

# Establish a connection to the switch using pexpect
child = pexpect.spawn(f"telnet {switch_ip} 23")
child.expect("Username:")
child.sendline(username)
child.expect("Password:")
child.sendline(password)

# Wait for the switch to prompt for a command
child.expect("#")

# Send the command to show the running configuration
child.sendline("show running-config")

# Wait for the output
child.expect("#")

# Get the output and save it to a file
output = child.before.decode("utf-8")
with open("switch_config.txt", "w") as f:
    f.write(output)

print("Configuration saved to switch_config.txt")
