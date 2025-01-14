import discord
from discord import app_commands
from discord.ext import commands
import wavelink
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import asyncio
import json
from typing import Optional, List
import datetime

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

DISCORD_TOKEN = config['DISCORD_TOKEN']
SPOTIFY_CLIENT_ID = config['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = config['SPOTIFY_CLIENT_SECRET']
LAVALINK_CONFIG = config['LAVALINK']

class MusicBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        self.playlists = {}
        self.load_playlists()
        
        self.spotify = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET
            )
        )

    def load_playlists(self):
        try:
            with open('playlists.json', 'r') as f:
                self.playlists = json.load(f)
        except FileNotFoundError:
            self.playlists = {}

    def save_playlists(self):
        with open('playlists.json', 'w') as f:
            json.dump(self.playlists, f, indent=2)

    async def setup_hook(self):
        node = wavelink.Node(
            uri=f"http://{LAVALINK_CONFIG['host']}:{LAVALINK_CONFIG['port']}", 
            password=LAVALINK_CONFIG['password']
        )
        await wavelink.NodePool.connect(client=self, nodes=[node])
        await self.tree.sync()

class Music(commands.Cog):
    def __init__(self, bot: MusicBot):
        self.bot = bot
        self.queue = {}
        self.now_playing = {}

    def get_queue(self, guild_id: int) -> list:
        if guild_id not in self.queue:
            self.queue[guild_id] = []
        return self.queue[guild_id]

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        if not player.guild:
            return

        guild_id = player.guild.id
        queue = self.get_queue(guild_id)
        
        if guild_id in self.now_playing:
            del self.now_playing[guild_id]
            
        if queue:
            next_track = queue.pop(0)
            await player.play(next_track)
            self.now_playing[guild_id] = next_track
        else:
            await player.disconnect()

    async def process_spotify_track(self, track_url: str) -> Optional[wavelink.Track]:
        try:
            track_id = track_url.split('/')[-1].split('?')[0]
            track_info = self.bot.spotify.track(track_id)
            search_query = f"{track_info['name']} {' '.join(artist['name'] for artist in track_info['artists'])}"
            tracks = await wavelink.YouTubeTrack.search(search_query)
            return tracks[0] if tracks else None
        except Exception as e:
            print(f"Error processing Spotify track: {e}")
            return None

    async def process_spotify_playlist(self, playlist_url: str) -> list:
        try:
            playlist_id = playlist_url.split('/')[-1].split('?')[0]
            results = self.bot.spotify.playlist_tracks(playlist_id)
            tracks = []
            
            for item in results['items']:
                track = item['track']
                search_query = f"{track['name']} {' '.join(artist['name'] for artist in track['artists'])}"
                found_tracks = await wavelink.YouTubeTrack.search(search_query)
                if found_tracks:
                    tracks.append(found_tracks[0])
            
            return tracks
        except Exception as e:
            print(f"Error processing Spotify playlist: {e}")
            return []

    @app_commands.command(name="join", description="Join your voice channel")
    async def join(self, interaction: discord.Interaction):
        if not interaction.user.voice:
            await interaction.response.send_message("You need to be in a voice channel!", ephemeral=True)
            return
        
        if not interaction.guild.voice_client:
            await interaction.user.voice.channel.connect(cls=wavelink.Player)
        elif interaction.guild.voice_client.channel != interaction.user.voice.channel:
            await interaction.guild.voice_client.move_to(interaction.user.voice.channel)
        
        await interaction.response.send_message(f"Joined {interaction.user.voice.channel.mention}")

    @app_commands.command(name="play", description="Play a song or add it to queue")
    @app_commands.describe(query="Song URL or search query")
    async def play(self, interaction: discord.Interaction, query: str):
        if not interaction.guild.voice_client:
            if not interaction.user.voice:
                await interaction.response.send_message("You need to be in a voice channel!", ephemeral=True)
                return
            await interaction.user.voice.channel.connect(cls=wavelink.Player)

        await interaction.response.defer()

        if 'spotify.com/track' in query:
            track = await self.process_spotify_track(query)
            if not track:
                await interaction.followup.send("Could not process Spotify track!")
                return
        elif 'spotify.com/playlist' in query:
            await interaction.followup.send("Processing Spotify playlist... This might take a while.")
            tracks = await self.process_spotify_playlist(query)
            if not tracks:
                await interaction.followup.send("Could not process Spotify playlist!")
                return
            
            queue = self.get_queue(interaction.guild_id)
            queue.extend(tracks)
            
            if not interaction.guild.voice_client.is_playing():
                track = queue.pop(0)
                await interaction.guild.voice_client.play(track)
                self.now_playing[interaction.guild_id] = track
            
            await interaction.followup.send(f"Added {len(tracks)} tracks from Spotify playlist to the queue!")
            return
        else:
            tracks = await wavelink.YouTubeTrack.search(query)
            if not tracks:
                await interaction.followup.send("No tracks found!")
                return
            track = tracks[0]

        queue = self.get_queue(interaction.guild_id)
        
        if interaction.guild.voice_client.is_playing():
            queue.append(track)
            await interaction.followup.send(f"Added to queue: {track.title}")
        else:
            await interaction.guild.voice_client.play(track)
            self.now_playing[interaction.guild_id] = track
            await interaction.followup.send(f"Now playing: {track.title}")

    @app_commands.command(name="skip", description="Skip the current song")
    async def skip(self, interaction: discord.Interaction):
        if not interaction.guild.voice_client or not interaction.guild.voice_client.is_playing():
            await interaction.response.send_message("Nothing is playing!", ephemeral=True)
            return

        await interaction.guild.voice_client.stop()
        await interaction.response.send_message("Skipped current track!")

    @app_commands.command(name="queue", description="Show the current queue")
    async def queue(self, interaction: discord.Interaction):
        queue = self.get_queue(interaction.guild_id)
        
        embed = discord.Embed(title="Music Queue", color=discord.Color.blue())
        
        if interaction.guild_id in self.now_playing:
            current_track = self.now_playing[interaction.guild_id]
            embed.add_field(
                name="Now Playing",
                value=f"🎵 {current_track.title}",
                inline=False
            )

        if not queue:
            embed.add_field(name="Queue", value="Queue is empty!", inline=False)
        else:
            queue_text = ""
            for i, track in enumerate(queue[:10], 1):
                queue_text += f"{i}. {track.title}\n"
            
            if len(queue) > 10:
                queue_text += f"\n... and {len(queue) - 10} more tracks"
            
            embed.add_field(name="Queue", value=queue_text, inline=False)
            
        total_duration = sum(track.duration for track in queue)
        embed.add_field(
            name="Queue Info",
            value=f"Total tracks: {len(queue)}\nTotal duration: {str(datetime.timedelta(seconds=total_duration))}",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="clear", description="Clear the queue")
    async def clear(self, interaction: discord.Interaction):
        self.queue[interaction.guild_id] = []
        await interaction.response.send_message("Queue cleared!")

    @app_commands.command(name="leave", description="Leave the voice channel")
    async def leave(self, interaction: discord.Interaction):
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()
            if interaction.guild_id in self.now_playing:
                del self.now_playing[interaction.guild_id]
            await interaction.response.send_message("Disconnected from voice channel!")
        else:
            await interaction.response.send_message("I'm not in a voice channel!", ephemeral=True)

    @app_commands.command(name="createplaylist", description="Create a new playlist")
    @app_commands.describe(name="Name of the playlist")
    async def createplaylist(self, interaction: discord.Interaction, name: str):
        if name in self.bot.playlists:
            await interaction.response.send_message("A playlist with this name already exists!", ephemeral=True)
            return

        self.bot.playlists[name] = []
        self.bot.save_playlists()
        await interaction.response.send_message(f"Created empty playlist '{name}'!")

    @app_commands.command(name="addtoplaylist", description="Add a song to a playlist")
    @app_commands.describe(
        playlist_name="Name of the playlist",
        query="Song URL or search query"
    )
    async def addtoplaylist(self, interaction: discord.Interaction, playlist_name: str, query: str):
        if playlist_name not in self.bot.playlists:
            await interaction.response.send_message("Playlist not found!", ephemeral=True)
            return

        await interaction.response.defer()

        if 'spotify.com/track' in query:
            track = await self.process_spotify_track(query)
            if not track:
                await interaction.followup.send("Could not process Spotify track!")
                return
        else:
            tracks = await wavelink.YouTubeTrack.search(query)
            if not tracks:
                await interaction.followup.send("No tracks found!")
                return
            track = tracks[0]

        track_data = {'title': track.title, 'uri': track.uri}
        self.bot.playlists[playlist_name].append(track_data)
        self.bot.save_playlists()
        
        await interaction.followup.send(f"Added '{track.title}' to playlist '{playlist_name}'!")

    @app_commands.command(name="removefromplaylist", description="Remove a song from a playlist")
    @app_commands.describe(
        playlist_name="Name of the playlist",
        index="Song number in the playlist (starting from 1)"
    )
    async def removefromplaylist(self, interaction: discord.Interaction, playlist_name: str, index: int):
        if playlist_name not in self.bot.playlists:
            await interaction.response.send_message("Playlist not found!", ephemeral=True)
            return

        playlist = self.bot.playlists[playlist_name]
        if not 1 <= index <= len(playlist):
            await interaction.response.send_message("Invalid song number!", ephemeral=True)
            return

        removed_track = playlist.pop(index - 1)
        self.bot.save_playlists()
        
        await interaction.response.send_message(
            f"Removed '{removed_track['title']}' from playlist '{playlist_name}'!"
        )

    @app_commands.command(name="playplaylist", description="Play a saved playlist")
    @app_commands.describe(name="Name of the playlist")
    async def playplaylist(self, interaction: discord.Interaction, name: str):
        if name not in self.bot.playlists:
            await interaction.response.send_message("Playlist not found!", ephemeral=True)
            return

        if not interaction.guild.voice_client:
            if not interaction.user.voice:
                await interaction.response.send_message("You need to be in a voice channel!", ephemeral=True)
                return
            await interaction.user.voice.channel.connect(cls=wavelink.Player)

        await interaction.response.defer()

        playlist = self.bot.playlists[name]
        queue = self.get_queue(interaction.guild_id)

        for track_data in playlist:
            track = await wavelink.YouTubeTrack.search(track_data['uri'])
            if track:
                queue.append(track[0])

        if not interaction.guild.voice_client.is_playing() and queue:
            track = queue.pop(0)
            await interaction.guild.voice_client.play(track)
            self.now_playing[interaction.guild_id] = track

        await interaction.followup.send(f"Added {len(playlist)} tracks from playlist '{name}' to the queue!")

    @app_commands.command(name="listplaylists", description="Show all saved playlists")
    async def listplaylists(self, interaction: discord.Interaction):
        if not self.bot.playlists:
            await interaction.response.send_message("No playlists available!")
            return

        embed = discord.Embed(title="Available Playlists", color=discord.Color.blue())
        
        for name, tracks in self.bot.playlists.items():
            track_list = "\n".join(f"{i+1}. {track['title']}" for i, track in enumerate(tracks[:5]))
            if len(tracks) > 5:
                track_list += f"\n... and {len(tracks) - 5} more tracks"
            
            if track_list:
                embed.add_field(
                    name=f"{name} ({len(tracks)} tracks)",
                    value=track_list,
                    inline=False
                )
            else:
                embed.add_field(
                    name=f"{name}",
                    value="Empty playlist",
                    inline=False
                )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="deleteplaylist", description="Delete a playlist")
    @app_commands.describe(name="Name of the playlist")
    async def deleteplaylist(self, interaction: discord.Interaction, name: str):
        if name not in self.bot.playlists:
            await interaction.response.send_message("Playlist not found!", ephemeral=True)
            return

        del self.bot.playlists[name]
        self.bot.save_playlists()
        await interaction.response.send_message(f"Deleted playlist '{name}'!")

    @app_commands.command(name="nowplaying", description="Show the currently playing song")
    async def nowplaying(self, interaction: discord.Interaction):
        if interaction.guild_id not in self.now_playing:
            await interaction.response.send_message("Nothing is playing!", ephemeral=True)
            return

        track = self.now_playing[interaction.guild_id]
        embed = discord.Embed(title="Now Playing", color=discord.Color.blue())
        embed.add_field(name="Title", value=track.title, inline=False)
        embed.add_field(
            name="Duration",
            value=str(datetime.timedelta(seconds=track.duration)),
            inline=True
        )
        embed.add_field(name="URL", value=track.uri, inline=True)
        
        await interaction.response.send_message(embed=embed)

async def main():
    bot = MusicBot()
    async with bot:
        await bot.add_cog(Music(bot))
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())