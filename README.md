# Cypher - Social Media Phishing Page Generator

## Requirements
- Python 3.8+
- ngrok account (free)

## Installation
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install ngrok (if not installed)
# The script will handle this automatically on first run
```

## Usage
1. Run the script:
```bash
python3 main.py
```

2. Follow the prompts to:
   - Select target platform
   - Choose link generation method
   - Configure ngrok (auth token or custom domain)
   - Get your phishing URL

## Troubleshooting

1. **Port Issues:**
   - The script uses random ports between 8000-9000
   - If you get a port error, try running the script again

2. **Tunnel Issues:**
   - Make sure you have an active internet connection
   - Check if ngrok is installed correctly
   - Try restarting the script

3. **Permission Issues:**
   - Run with sudo if you get permission errors
   - Make sure all directories are accessible

## Note
This tool is for educational purposes only. Use responsibly and legally. 