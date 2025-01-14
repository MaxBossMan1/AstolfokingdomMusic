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

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your Discord bot token and Spotify credentials

3. Set up Lavalink:
   - Download the latest Lavalink.jar
   - Create an application.yml file for Lavalink configuration
   - Run Lavalink server: `java -jar Lavalink.jar`

4. Run the bot:
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