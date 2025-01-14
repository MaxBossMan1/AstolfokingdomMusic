@echo off
setlocal enabledelayedexpansion

:: Function to handle errors
:error
if %errorlevel% neq 0 (
    echo Error occurred! Error code: %errorlevel%
    pause
    exit /b %errorlevel%
)

:: Check requirements
if not exist "venv" (
    echo Virtual environment not found! Please run setup.bat first.
    pause
    exit /b 1
)

if not exist "lavalink\Lavalink.jar" (
    echo Lavalink.jar not found! Please run setup.bat first.
    pause
    exit /b 1
)

if not exist "lavalink\application.yml" (
    echo application.yml not found! Please run setup.bat first.
    pause
    exit /b 1
)

:: Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

:: Kill any existing Java processes (Lavalink)
taskkill /F /IM java.exe /FI "WINDOWTITLE eq Lavalink Server" >nul 2>&1

:: Start Lavalink in a new window with logging
echo Starting Lavalink server...
start "Lavalink Server" cmd /c "cd lavalink && java -jar Lavalink.jar > ..\logs\lavalink.log 2>&1"

:: Wait for Lavalink to start
echo Waiting for Lavalink to start...
timeout /t 10 /nobreak

:: Check if Lavalink started successfully
findstr /C:"Lavalink is ready to accept connections." ..\logs\lavalink.log >nul
if errorlevel 1 (
    echo Lavalink failed to start! Check logs\lavalink.log for details.
    pause
    exit /b 1
)

:: Activate virtual environment and start the bot
echo Starting the bot...
call venv\Scripts\activate.bat
python bot.py
call :error
deactivate

pause