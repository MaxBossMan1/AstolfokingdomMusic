@echo off
setlocal enabledelayedexpansion

:: Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found! Please run setup.bat first.
    pause
    exit /b 1
)

:: Start Lavalink in a new window
start "Lavalink Server" cmd /c "cd lavalink && java -jar Lavalink.jar"

:: Wait for Lavalink to start
echo Waiting for Lavalink to start...
timeout /t 10 /nobreak

:: Activate virtual environment and start the bot
echo Starting the bot...
call venv\Scripts\activate.bat
python bot.py
deactivate

pause