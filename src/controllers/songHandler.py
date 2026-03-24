import pygame
import os

# Handles playing music
class SongHandler:
    def __init__(self, path):
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