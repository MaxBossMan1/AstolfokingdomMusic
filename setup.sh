#!/bin/bash

echo "Setting up Discord Music Bot..."

# Check if Python 3.11 is installed
if ! command -v python3.11 &> /dev/null; then
    echo "Python 3.11 is not installed! Please install Python 3.11"
    exit 1
fi

# Check if Java is installed
if ! command -v java &> /dev/null; then
    echo "Java is not installed! Please install Java 17 or newer"
    exit 1
fi

# Create directories
mkdir -p lavalink logs

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.11 -m venv venv
fi

# Download Lavalink if not exists
if [ ! -f "lavalink/Lavalink.jar" ]; then
    echo "Downloading Lavalink..."
    curl -L "https://github.com/lavalink-devs/Lavalink/releases/download/3.7.11/Lavalink.jar" -o "lavalink/Lavalink.jar"
fi

# Activate virtual environment and install dependencies
echo "Installing Python dependencies..."
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
deactivate

# Create config.json if it doesn't exist
if [ ! -f "config.json" ]; then
    echo "Creating config.json..."
    cp config.json.example config.json
    echo "Please edit config.json with your Discord and Spotify tokens"
fi

# Make start script executable
chmod +x start.sh

echo "Setup completed successfully!"
echo
echo "To start the bot:"
echo "1. Edit config.json with your tokens"
echo "2. Run ./start.sh"
echo