# Cypher - Social Media Phishing Page Generator

## Requirements

### System Requirements
1. Python 3.8 or higher
2. Node.js (for localtunnel option)
3. Cloudflared (for Cloudflare tunnel option)

### Installation Steps

1. **Install Python Dependencies:**
```bash
pip install -r requirements.txt
```

2. **Install Cloudflared (Recommended Method):**
```bash
# Download the package
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb

# Install it
sudo dpkg -i cloudflared.deb
```

3. **Install Node.js (Alternative Method):**
```bash
# Using apt (Debian/Ubuntu/Kali)
sudo apt update
sudo apt install nodejs npm -y

# Verify installation
node --version
npm --version
```

### Directory Structure
```
project/
├── main.py
├── requirements.txt
├── README.md
└── web/
    ├── instagram/
    ├── snapchat/
    ├── facebook/
    └── linkedin/
```

## Usage

1. Run the script:
```bash
python3 main.py
```

2. Select your target platform from the menu:
   - Instagram
   - Snapchat
   - Facebook
   - LinkedIn

3. The script will:
   - Start a local server
   - Create a secure tunnel
   - Generate a public URL
   - Monitor for incoming credentials

4. Press Ctrl+C to stop the server

## Troubleshooting

1. **Port Issues:**
   - The script uses random ports between 8000-9000
   - If you get a port error, try running the script again

2. **Tunnel Issues:**
   - Make sure you have an active internet connection
   - Check if cloudflared/Node.js is installed correctly
   - Try restarting the script

3. **Permission Issues:**
   - Run with sudo if you get permission errors
   - Make sure all directories are accessible

## Note
This tool is for educational purposes only. Use responsibly and legally. 