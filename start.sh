#!/bin/bash

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found! Please run setup.sh first."
    exit 1
fi

# Start Lavalink in the background
cd lavalink
java -jar Lavalink.jar > lavalink.log 2>&1 &
LAVALINK_PID=$!
cd ..

# Wait for Lavalink to start
echo "Waiting for Lavalink to start..."
sleep 10

# Activate virtual environment and start the bot
echo "Starting the bot..."
source venv/bin/activate
python bot.py
deactivate

# Cleanup when the bot exits
kill $LAVALINK_PID
rm lavalink/lavalink.log