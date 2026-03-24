import pygame
import os

# Handles playing music
class SongHandler:
    def __init__(self, path, musicScreen):

        # Text information related to the song
        self.path = path
        self.filename = os.path.basename(path)
        self.name, _ = os.path.splitext(self.filename)
        if " - " in self.name:
            parts = self.name.split(" - ", 1)
            self.artist = parts[0]
            self.title = parts[1]
        else:
            self.artist = "Unknown Artist"
            self.title = self.name

        # Scalar information related to the song
        self.duration = self.getDuration()

        # Store the time components on the UI
        self.musicScreen = musicScreen

        # Play the song
        self.restart()

    # Get duration of song
    def getDuration(self):
        tempSound = pygame.mixer.Sound(self.path)
        return tempSound.get_length()
    
    # Get number of seconds
    def getSeconds(self):
        return pygame.mixer.music.get_pos() / 1000.0
    
    # Get number of seconds left
    def getRemainingSeconds(self):
        remaining = self.duration - self.getSeconds()
        return max(0, remaining)
    
    # Format seconds into MM:SS string
    def formatTime(self, seconds):
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"
    
    # Gets percentage of how far along the song is
    def getPercentage(self):
        if self.duration > 0:
            return self.getSeconds() / self.duration
        return 0

    # Restart the song
    def restart(self):
        pygame.mixer.music.load(str(self.path))
        pygame.mixer.music.play(loops=0, start=0.0)

    # Update components related to the song
    def update(self):
        title = self.musicScreen.title
        artist = self.musicScreen.artist
        timeBar = self.musicScreen.timeBar
        timeLeft = self.musicScreen.timeLeft
        timeRight = self.musicScreen.timeRight

        title.setText(self.title)
        artist.setText(self.artist)
        timeBar.setProgress(self.getPercentage())
        timeLeft.setText(self.formatTime(self.getSeconds()))
        timeRight.setText(f"-{self.formatTime(self.getRemainingSeconds())}")