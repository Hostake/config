import telnetlib
import os
import schedule
import time
import telebot

# Define the switches and their credentials
switches = [
    {"ip": "192.168.1.1", "username": "admin", "password": "password"},
    {"ip": "192.168.1.2", "username": "admin", "password": "password"},
    # Add more switches as needed
]

# Define the server and its credentials
server_ip = "192.168.1.100"
server_username = "username"
server_password = "password"

# Create a directory to store the backups
backup_dir = "/backups/switch_configs"
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

def backup_switches():
    try:
        # Connect to each switch and backup its configuration
        for switch in switches:
            tn = telnetlib.Telnet(switch["ip"])
            tn.read_until(b"Username: ")
            tn.write(switch["username"].encode("ascii") + b"\n")
            tn.read_until(b"Password: ")
            tn.write(switch["password"].encode("ascii") + b"\n")

            # Run the command to backup the configuration
            tn.write(b"show running-config\n")
            config = tn.read_until(b"#").decode("utf-8")

            # Save the configuration to a file
            filename = f"{switch['ip']}_config.txt"
            with open(os.path.join(backup_dir, filename), "w") as f:
                f.write(config)

            # Close the Telnet connection
            tn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    # Create a Telegram bot
    bot_token = "YOUR_BOT_TOKEN"
    bot = telebot.TeleBot(bot_token)

    @bot.message_handler(commands=["start"])
    def start(message):
        bot.send_message(message.chat.id, "Welcome to the switch backup bot!")

    @bot.message_handler(commands=["backup_now"])
    def backup_now(message):
        if backup_switches():
            bot.send_message(message.chat.id, "Backup completed successfully!")
        else:
            bot.send_message(message.chat.id, "Backup failed. Check the error message above.")

    @bot.message_handler(commands=["schedule_backup"])
    def schedule_backup(message):
        try:
            schedule.every(7).days.at("02:00").do(backup_switches)  # Run every Sunday at 2am
            bot.send_message(message.chat.id, "Backup scheduled to run every Sunday at 2am.")
        except Exception as e:
            bot.send_message(message.chat.id, text=f"Error: {e}")

    @bot.message_handler(commands=["disable_backup"])
    def disable_backup(message):
        try:
            schedule.clear("backup_switches")  # Clear the scheduled task
            bot.send_message(message.chat.id, "Automatic backup disabled.")
        except Exception as e:
            bot.send_message(message.chat.id, text=f"Error: {e}")

    bot.infinity_polling()

if __name__ == "__main__":
    main()
