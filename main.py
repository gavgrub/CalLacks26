import pygame
import sys

from src.ui.screenManager import ScreenManager
from src.ui.assetManager import AssetManager
from src.ui.musicPlayer import MusicPlayerScreen

def main():
    pygame.init()
    pygame.mixer.init()

    clock = pygame.time.Clock()

    sm = ScreenManager(6) 
    am = AssetManager()
    
    # Initialize the screen and set it in the manager
    musicScreen = MusicPlayerScreen(am, sm)
    sm.setScreen(musicScreen)

    while True:
        clock.tick(sm.fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                sm.resize(event.w / 75)

            sm.handleEvent(event)

        sm.draw()

if __name__ == "__main__":
    main()