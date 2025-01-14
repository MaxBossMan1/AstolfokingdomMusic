#!/bin/bash

# Start Lavalink in the background
cd lavalink
java -jar Lavalink.jar &
LAVALINK_PID=$!
cd ..

# Wait for Lavalink to start
echo "Waiting for Lavalink to start..."
sleep 10

# Start the bot
echo "Starting the bot..."
python3 bot.py

# Cleanup when the bot exits
kill $LAVALINK_PID