import json
import os
import random
import pygame
import threading

# Initialize Pygame mixer
pygame.mixer.init()

# Load JSON config
def load_config():
    """Load the configuration from the JSON file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    return {}

# Save the json config changed
def save_config(config):
    """Save the configuration to the JSON file."""
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=4)

# Constants
CONFIG_FILE = "config.json"
MUSIC_FOLDER = "assets/audios"
config = load_config()
PLAYLIST_ACTIVATED = config.get("playlist_activate", True)
PLAYLIST_VOLUME = config.get("playlist_sound", 50) / 100.0

# Playlist class
class Playlist:
    def __init__(self, folder, volume):
        self.folder = folder
        self.volume = volume
        self.playlist = self.load_music_files()
        self.played_songs = []

    def load_music_files(self):
        """Load all MP3 files from the specified folder."""
        return [os.path.join(self.folder, file) for file in os.listdir(self.folder) if file.endswith(".mp3")]

    def shuffle_playlist(self):
        """Shuffle the playlist."""
        random.shuffle(self.playlist)

    def play_next_song(self):
        """Play the next song in the playlist."""
        if not self.playlist:
            print("No songs in the playlist.")
            return

        if not self.played_songs or len(self.played_songs) == len(self.playlist):
            # All songs have been played, reshuffle and reset played songs list
            self.shuffle_playlist()
            self.played_songs = []

        # Pick the next song that hasn't been played yet
        next_song = None
        for song in self.playlist:
            if song not in self.played_songs:
                next_song = song
                break

        if next_song:
            self.play_song(next_song)
            self.played_songs.append(next_song)

    def play_song(self, song_path):
        """Play the given MP3 file."""
        try:
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()
            print(f"Playing: {os.path.basename(song_path)}")
        except Exception as e:
            print(f"Error playing {song_path}: {e}")

    def check_end_and_play_next(self):
        """Check if the current song has ended and play the next one."""
        if not pygame.mixer.music.get_busy():
            self.play_next_song()

# Create and launch the playlist
def playlist_runner():
    global PLAYLIST_ACTIVATED
    playlist = Playlist(MUSIC_FOLDER, PLAYLIST_VOLUME)
    playlist.shuffle_playlist()
    playlist.play_next_song()

    # Main loop to keep the program running and checking if the song has ended
    while PLAYLIST_ACTIVATED:
        playlist.check_end_and_play_next()
        pygame.time.wait(1000)  # Wait 1 second before checking again
    
    pygame.mixer.music.stop()  # Stop the music immediately if PLAYLIST_ACTIVATED is False
    print("Playlist stopped.")

# Start the playlist
def start_playlist():
    if PLAYLIST_ACTIVATED:
        playlist_thread = threading.Thread(target=playlist_runner, daemon=True)
        playlist_thread.start()

# Stop the playlist
def stop_playlist():
    global PLAYLIST_ACTIVATED
    PLAYLIST_ACTIVATED = False

# Toggle the playlist on or off based on current state.
def toggle_playlist():
    global PLAYLIST_ACTIVATED
    PLAYLIST_ACTIVATED = not PLAYLIST_ACTIVATED
    
    # Update the config file
    config['playlist_activate'] = PLAYLIST_ACTIVATED
    save_config(config)
    
    if PLAYLIST_ACTIVATED:
        start_playlist()
    else:
        stop_playlist()

