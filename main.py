import os
import warnings
import subprocess
import pygame
import sys
import argparse

from src.ui.screenManager import ScreenManager
from src.ui.assetManager import AssetManager
from src.ui.musicPlayerScreen import MusicPlayerScreen
from src.controllers.songHandler import SongHandler

chessProcess = None

def getArgs():
    parser = argparse.ArgumentParser(description="A music player with a surprise.")
    parser.add_argument("path", help="Path to the .mp3 or .wav file")
    parser.add_argument("-n", action="store_true", help="Disable the 'surprise' feature")
    return parser.parse_args()

def openChessWindow(*args):
    global chessProcess

    if chessProcess is not None and chessProcess.poll() is None:
        return

    try:
        chessProcess = subprocess.Popen([sys.executable, "src/ui/chessWindow.py"])
    except Exception:
        pass

def main():
    args = getArgs()
    songPath = args.path

    # Validation logic
    if not songPath.lower().endswith((".mp3", ".wav")):
        print("Error: Unsupported file format. Please use .mp3 or .wav")
        sys.exit(1)

    if not os.path.exists(songPath):
        print(f"Error: The file '{songPath}' could not be found.")
        sys.exit(1)

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

    # Setup buttons on the ui
    musicScreen.setCommand("albumArt", music.toggle)
    musicScreen.setCommand("timeBar", music.setTime)
    
    # Soundbar functionality
    if args.n:
        musicScreen.setCommand("soundBar", music.setVolume)
    else:
        musicScreen.setCommand("soundBar", openChessWindow)

    # Cleanup bridge file from previous run
    if os.path.exists("bridge.txt"):
        os.remove("bridge.txt")

    while True:
        clock.tick(sm.fps)

        # Read volume from chess window
        try:
            if os.path.exists("bridge.txt"):
                with open("bridge.txt", "r") as f:
                    content = f.read().strip()
                    if content:
                        newVol = float(content)
                        music.setVolume(newVol)
        except (ValueError, IOError):
            pass

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Cleanup bridge file on exit
                if os.path.exists("bridge.txt"):
                    os.remove("bridge.txt")
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.VIDEORESIZE:
                sm.resize(event.w / 75)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    music.toggle()

            sm.handleEvents(event)

        # Update / draw
        music.update()
        sm.draw()

if __name__ == "__main__":
    main()