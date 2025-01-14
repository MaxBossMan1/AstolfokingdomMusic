# Discord Music Bot

A feature-rich Discord music bot with playlist support, Spotify integration, and queue management using slash commands.

## Features

- Play music from YouTube URLs or search queries
- Spotify track and playlist support
- Custom playlist creation and management
- Queue management with detailed information
- Rich embeds for better visualization
- Slash commands for easier interaction

## Prerequisites

- Python 3.8 or higher
- Lavalink server (for music playback)
- Discord Bot Token
- Spotify Developer credentials

## Setup

### Prerequisites

1. Install Python 3.8+ (Python 3.12 recommended):
   - Windows: [Python.org](https://www.python.org/downloads/)
   - Linux: `sudo apt install python3.12` (Ubuntu/Debian)
   - macOS: `brew install python@3.12` (with Homebrew)

2. Install Java 17 or newer:
   - Windows: [Adoptium](https://adoptium.net/)
   - Linux: `sudo apt install openjdk-17-jre` (Ubuntu/Debian)
   - macOS: `brew install openjdk@17` (with Homebrew)

3. Install Visual Studio Build Tools (Windows only):
   - Download and install [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - During installation, select "Desktop development with C++"

### Automatic Setup

#### Windows
1. Run `setup.bat`
2. Edit `config.json` with your Discord and Spotify tokens
3. Run `start.bat` to start both Lavalink and the bot

#### Linux/macOS
1. Run `chmod +x setup.sh start.sh`
2. Run `./setup.sh`
3. Edit `config.json` with your Discord and Spotify tokens
4. Run `./start.sh` to start both Lavalink and the bot

### Manual Setup

If you prefer to set up everything manually:

1. Install Python dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

2. Set up configuration:
   - Copy `config.json.example` to `config.json`
   - Fill in your Discord and Spotify credentials

3. Set up Lavalink:
   - Download [Lavalink.jar](https://github.com/lavalink-devs/Lavalink/releases)
   - Place it in the `lavalink` directory
   - The `application.yml` file is already configured

4. Start Lavalink:
   ```bash
   cd lavalink
   java -jar Lavalink.jar
   ```

5. In a new terminal, start the bot:
   ```bash
   python bot.py
   ```

## Commands

### Music Playback
- `/join` - Join your voice channel
- `/play <query/url>` - Play a song or add it to queue
- `/skip` - Skip current song
- `/queue` - Show current queue with details
- `/clear` - Clear the queue
- `/leave` - Leave voice channel
- `/nowplaying` - Show details about the current track

### Playlist Management
- `/createplaylist <name>` - Create a new empty playlist
- `/addtoplaylist <playlist_name> <query>` - Add a song to a playlist
- `/removefromplaylist <playlist_name> <index>` - Remove a song from a playlist
- `/playplaylist <name>` - Play a saved playlist
- `/listplaylists` - Show all saved playlists with their contents
- `/deleteplaylist <name>` - Delete a playlist

## Spotify Integration

The bot supports:
- Playing individual Spotify tracks
- Loading entire Spotify playlists
- Converting Spotify content to playable YouTube tracks

## Features in Detail

1. Queue Management:
   - Shows currently playing track
   - Displays up to 10 upcoming tracks
   - Shows total queue duration
   - Indicates total number of tracks

2. Playlist System:
   - Create multiple playlists
   - Add individual songs to playlists
   - Remove songs from playlists
   - View playlist contents
   - Play entire playlists

3. Rich Embeds:
   - Detailed track information
   - Queue visualization
   - Playlist contents display
   - Now playing information