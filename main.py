import os
import warnings
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
warnings.filterwarnings("ignore", category=UserWarning, module='pygame.pkgdata')

import pygame
import sys

from src.ui.screenManager import ScreenManager
from src.ui.assetManager import AssetManager
from src.ui.musicPlayerScreen import MusicPlayerScreen

from src.controllers.songHandler import SongHandler

def main():
    # Error handling, make sure that the music player has a song
    if not (len(sys.argv) == 2):
        print("Program requires a song to play")
        sys.exit()
    songPath = sys.argv[1]
    if not (songPath.lower().endswith(".mp3") or songPath.lower().endswith(".wav")):
        print("Files must be formatted as either .mp3 or .wav")
        sys.exit()

    pygame.init()
    pygame.mixer.init()

    clock = pygame.time.Clock()

    sm = ScreenManager(6) 
    am = AssetManager()
    
    # Initialize the screen and set it in the manager
    musicScreen = MusicPlayerScreen(am, sm)
    sm.setScreen(musicScreen)

    # Setup the music manager
    music = SongHandler(os.path.abspath(songPath), musicScreen)

    while True:
        clock.tick(sm.fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                sm.resize(event.w / 75)

            sm.handleEvent(event)

        # Update music
        music.update()

        # Draw to screen
        sm.draw()

if __name__ == "__main__":
    main()