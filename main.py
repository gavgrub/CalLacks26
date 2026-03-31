import os
import warnings
import subprocess
import pygame
import sys
import argparse
import threading
import queue

from src.ui.screenManager import ScreenManager
from src.ui.assetManager import AssetManager
from src.ui.musicPlayerScreen import MusicPlayerScreen
from src.controllers.songHandler import SongHandler

chessProcess = None
messageQueue = queue.Queue()

def outputReader(proc):
    """This runs in the background and fills the queue."""
    for line in iter(proc.stdout.readline, ""):
        if line:
            messageQueue.put(line.strip())

def getArgs():
    parser = argparse.ArgumentParser(description="A music player with a surprise.")
    parser.add_argument("path", help="Path to the .mp3 or .wav file")
    parser.add_argument("-n", action="store_true", help="Disable the 'surprise' feature")
    return parser.parse_args()

def openChessWindow(var_name):
    global chessProcess
    if chessProcess is not None and chessProcess.poll() is None:
        return
    chessProcess = subprocess.Popen(
        [sys.executable, "src/ui/chessWindow.py", str(var_name)],
        stdout=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    thread = threading.Thread(target=outputReader, args=(chessProcess,), daemon=True)
    thread.start()

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
    
    # Setup UI functionality
    if args.n:
        musicScreen.setCommand("soundBar", music.setVolume)
        musicScreen.setCommand("timeBar", music.setTime)
        musicScreen.setCommand("albumArt", music.toggle)
    else:
        musicScreen.setCommand("soundBar", lambda p : openChessWindow("VOLUME"))
        musicScreen.setCommand("timeBar", lambda p : openChessWindow("TIME"))
        musicScreen.setCommand("albumArt", lambda p : openChessWindow("PAUSE"))

    # Cleanup bridge file from previous run
    if os.path.exists("bridge.txt"):
        os.remove("bridge.txt")

    while True:
        clock.tick(sm.fps)

        # Read information
        try:
            while not messageQueue.empty():
                msg = messageQueue.get_nowait()
                if ":" in msg:
                    prefix, value = msg.split(":", 1)
                    val = float(value)

                    if prefix == "VOLUME":
                        music.setVolume(val)
                    elif prefix == "TIME":
                        music.setTime(val)
                    elif prefix == "PAUSE":
                        music.setPause(val)
        except (queue.Empty, ValueError):
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