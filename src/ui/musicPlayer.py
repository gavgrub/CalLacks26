import pygame
from src.ui.components import Text, Image, Slider

BACKGROUND = (112, 62, 69)
UILIGHT = (231, 181, 189)
UIDARK = (157, 119, 132)
WHITE = (255, 255, 255)

class MusicPlayerScreen:
    def __init__(self, am, sm):
        self.am = am
        self.sm = sm
        self.elements = []
        self.build()

    def build(self):
        self.elements = []
        UISIZE = self.sm.SIZE
        WIDTH = self.sm.WIDTH
        
        noteSize = int(WIDTH * 0.75)
        
        albumArt = Image(self.am.image("play"))
        albumArt.build((noteSize, noteSize))
        
        title = Text("Song 2", int(UISIZE * 6), WHITE, align="left")
        title.build(self.am)
        
        artist = Text("A cool guy", int(UISIZE * 4), UILIGHT, align="left")
        artist.build(self.am)

        timeBar = Slider(noteSize, int(UISIZE * 4), UIDARK)
        timeBar.build()

        timeLeft = Text("Time 1", int(UISIZE * 4), UILIGHT, align="left")
        timeLeft.build(self.am)
        
        timeRight = Text("Time 2", int(UISIZE * 4), UILIGHT, align="right")
        timeRight.build(self.am)
        
        soundBar = Slider(int(noteSize * 0.8), int(UISIZE * 4), UIDARK)
        soundBar.build()

        muteImg = Image(self.am.image("mute"))
        muteImg.build((int(UISIZE * 4), int(UISIZE * 4)))
        
        volumeImg = Image(self.am.image("volume"))
        volumeImg.build((int(UISIZE * 4), int(UISIZE * 4)))

        x = WIDTH / 2 - noteSize / 2
        y = WIDTH / 2 + noteSize / 2 + UISIZE * 6
        
        albumArt.x, albumArt.y = x, x
        
        title.x, title.y = x, y
        
        y += UISIZE * 8
        artist.x, artist.y = x, y
        
        y += UISIZE * 9
        timeBar.x, timeBar.y = x, y
        
        y += UISIZE * 7
        timeLeft.x, timeLeft.y = x, y
        timeRight.x, timeRight.y = x + noteSize, y
        
        y += UISIZE * 7
        soundBar.x, soundBar.y = (WIDTH / 2 - soundBar.width / 2), y
        muteImg.x, muteImg.y = x, y
        volumeImg.x, volumeImg.y = (x + noteSize - volumeImg.surface.get_width()), y

        self.elements.extend([albumArt, title, artist, timeBar, timeLeft, timeRight, soundBar, muteImg, volumeImg])

    def draw(self):
        screen = self.sm.screen
        screen.fill(BACKGROUND)
        
        # Use the generic draw method from the Element class
        for element in self.elements:
            element.draw(screen)