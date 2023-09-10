import os
import sys
import socket
import logging
import threading
import keyboard
import random
from colorama import init, Fore, Back, Style

# Set the console title to the name of the executable
exe_name = os.path.basename(sys.argv[0])
os.system(f'title {exe_name}')


init(autoreset=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ping_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # Set a timeout of 1 second for the connection attempt
        s.connect((ip, port))
        s.close()
        return True
    except (socket.timeout, TimeoutError):  # Catch both socket.timeout and TimeoutError
        logging.warning(f"Timeout while trying to connect to {ip} on port {port}")
        return False
    except Exception as e:
        logging.error(f"Error while trying to connect to {ip} on port {port}: {e}")
        return False

def send_packet(ip, port, size, timeout=1):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.sendall(b"X" * size)
        s.close()
        return True
    except:
        return False

def ping_target(target, start_port, end_port):
    for port in range(start_port, end_port):
        if exit_signal:  # Check if the exit_signal is set
            break
        if ping_port(target, port):
            logging.info(f"Port {port} is open on {target}")
        else:
            logging.info(f"Port {port} is closed on {target}")

def apply_random_color(text):
    colors = [
        '\033[91m',  # RED
        '\033[92m',  # GREEN
        '\033[93m',  # YELLOW
        '\033[94m',  # BLUE
        '\033[95m',  # PURPLE
        '\033[96m',  # CYAN
        '\033[97m',  # WHITE
    ]
    return random.choice(colors) + text + '\033[0m'  # Reset color at the end

def main():
    global exit_signal
    exit_signal = False  # Used to signal the threads to stop
    while True:  # Main menu loop
        print(apply_random_color("""
   _____    ____    _____    _____   __     __  _____                   _         
  / ____|  / __ \  |  __ \  |  __ \  \ \   / / |  __ \                 | |        
 | (___   | |  | | | |__) | | |__) |  \ \_/ /  | |__) |   ___    _ __  | |_   ___ 
  \___ \  | |  | | |  _  /  |  _  /    \   /   |  ___/   / _ \  | '__| | __| / __|
  ____) | | |__| | | | \ \  | | \ \     | |    | |      | (_) | | |    | |_  \__ \
      
 |_____/   \____/  |_|  \_\ |_|  \_\    |_|    |_|       \___/  |_|     \__| |___/                     

"""                             ))

        print(apply_random_color("1. IP address"))
        print(apply_random_color("2. Domain"))
        print(apply_random_color("3. About"))
        print(apply_random_color("4. Exit"))
        choice = input("Enter your choice: ")
        target = input()


        if choice in ["1", "2"]:
            target = input(apply_random_color("Enter the IP address: " if choice == "1" else "Enter the domain: "))
            print(apply_random_color("\nStarting the operation. Press 'q' to kill the process...\n"))
            target = input()

            num_threads = 10  # Number of threads to use
            ports_per_thread = 65536 // num_threads
            threads = []

            # Start the pinging process in multiple threads
            for i in range(num_threads):
                start_port = i * ports_per_thread
                end_port = (i+1) * ports_per_thread
                t = threading.Thread(target=ping_target, args=(target, start_port, end_port))
                threads.append(t)
                t.start()

            # Monitor for user input in the main thread
            while True:
                if keyboard.is_pressed('q'):
                    exit_signal = True
                    for t in threads:
                        t.join()  # Wait for all the pinging threads to finish
                    break

        elif choice == "3":
            print(apply_random_color("""
About the DDOS Testing Tool:

Author: Ashton Kinnell
Version: 1.0

Description:
This tool is designed to ping an IP address or domain on all ports to test the resilience and performance of your network. It's intended for educational and SOC purposes only. Unauthorized and illegal use is strictly prohibited.

Instructions:

1. Start the tool and you'll be presented with the main menu.

2. Choose one of the following options:
   - IP address: Select this option if you want to test a specific IP address.
   - Domain: Select this option if you want to test a specific domain name.

3. After selecting an option, you'll be prompted to enter the IP address or domain name you wish to test.

4. The tool will start the pinging operation. It will attempt to connect to all ports (from 1 to 65535) on the specified target.

5. To stop the operation at any time, simply press the 'q' key on your keyboard. The tool will gracefully stop all ongoing operations and return you to the main menu.

6. If you want to learn more about the tool or need a refresher on how to use it, select the "About" option from the main menu.

7. To exit the tool, select the "Exit" option from the main menu.

Note:
- Always ensure you have the necessary permissions to test the target IP or domain.
- Continuous or aggressive use of this tool on a target may lead to its unavailability or other unintended consequences. Use responsibly and monitor the target's performance and health during testing.

Disclaimer:
This tool is for educational and SOC purposes only. Do not use this tool on any network that you do not own or have explicit permission to test. Unauthorized use is illegal and strictly prohibited.
"""))
            input(apply_random_color("Press Enter to return to the main menu..."))  # Wait for user input before returning to the main menu
            target = input()

        elif choice == "4":
            break # Exit the main menu
            target = input()

        else:
            print(apply_random_color("Invalid choice!"))
            target = input()
    
    


                
if __name__ == "__main__":
    main()
