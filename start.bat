@echo off
setlocal enabledelayedexpansion

:: Start Lavalink in a new window
start "Lavalink Server" cmd /c "cd lavalink && java -jar Lavalink.jar"

:: Wait for Lavalink to start
echo Waiting for Lavalink to start...
timeout /t 10 /nobreak

:: Start the bot
echo Starting the bot...
python bot.py

pause