@echo off
setlocal enabledelayedexpansion

echo Setting up Discord Music Bot...

:: Check if Python 3.11 is installed
py -3.11 --version > nul 2>&1
if errorlevel 1 (
    echo Python 3.11 is not installed! Please install Python 3.11 from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check if Java is installed
java -version > nul 2>&1
if errorlevel 1 (
    echo Java is not installed! Please install Java 17 or newer from https://adoptium.net/
    pause
    exit /b 1
)

:: Create directories
if not exist "lavalink" mkdir lavalink
if not exist "logs" mkdir logs
if not exist "venv" (
    echo Creating virtual environment...
    py -3.11 -m venv venv
)

:: Create plugins directory
if not exist "lavalink\plugins" mkdir lavalink\plugins

:: Download Lavalink if not exists
if not exist "lavalink\Lavalink.jar" (
    echo Downloading Lavalink...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/lavalink-devs/Lavalink/releases/download/3.7.11/Lavalink.jar' -OutFile 'lavalink\Lavalink.jar'"
)

:: Download YouTube plugin if not exists
if not exist "lavalink\plugins\lavalink-youtube-plugin.jar" (
    echo Downloading YouTube plugin...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/lavalink-devs/youtube-source/releases/download/1.0.0/lavalink-youtube-plugin-1.0.0.jar' -OutFile 'lavalink\plugins\lavalink-youtube-plugin.jar'"
)

:: Activate virtual environment and install dependencies
echo Installing Python dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
deactivate

:: Create config.json if it doesn't exist
if not exist "config.json" (
    echo Creating config.json...
    copy config.json.example config.json
    echo Please edit config.json with your Discord and Spotify tokens
)

echo Setup completed successfully!
echo.
echo To start the bot:
echo 1. Edit config.json with your tokens
echo 2. Run start.bat
echo.
pause