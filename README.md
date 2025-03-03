# Cypher - Social Media Phishing Page Generator

A powerful tool for generating phishing pages for various social media platforms with Discord webhook integration.

## Requirements
- Python 3.8 or higher
- ngrok account (free)
- Discord account (for webhook)

## Installation

1. Clone or download this repository
2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Setup Steps

### 1. Discord Webhook Setup
1. Open Discord
2. Go to Server Settings
3. Select Integrations
4. Click "Create Webhook"
5. Give it a name (e.g., "Cypher")
6. Copy the Webhook URL
7. The URL format should be: `https://discord.com/api/webhooks/...`

### 2. Ngrok Setup
1. Go to https://ngrok.com
2. Sign up for a free account
3. Get your auth token from: https://dashboard.ngrok.com/get-started/your-authtoken
4. The tool will automatically configure ngrok on first run

## Usage

1. Run the tool:
```bash
python3 main.py
```

2. First-time setup:
   - Enter your Discord webhook URL when prompted
   - The URL will be saved for future use

3. Main Menu Options:
   - [1] Instagram
   - [2] Snapchat
   - [3] Facebook
   - [4] LinkedIn
   - [5] Exit

4. Link Generation Options:
   - [1] Ngrok (Public URL)
   - [2] Localhost (Local Network)
   - [3] Back

## Features

- Beautiful ASCII art interface
- Multiple platform support
- Discord webhook integration
- Automatic ngrok setup
- Local network support
- Persistent webhook storage
- Cross-platform compatibility

## Troubleshooting

1. **Webhook Issues:**
   - Make sure your Discord webhook URL is valid
   - Check if you have proper permissions in Discord
   - Try creating a new webhook

2. **Ngrok Issues:**
   - Verify your ngrok auth token
   - Check your internet connection
   - Make sure no other ngrok instances are running
   - Try running with sudo: `sudo python3 main.py`

3. **Port Issues:**
   - The tool uses random ports between 8000-9000
   - If you get a port error, try running the tool again
   - Make sure no other services are using the ports

4. **Permission Issues:**
   - Run with sudo if you get permission errors
   - Make sure all directories are accessible
   - Check file permissions

## Note
This tool is for educational purposes only. Use responsibly and legally. 