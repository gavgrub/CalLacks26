import pygame
import math
import numpy as np
from src.ui.components import Text, Image, Slider

BG_TOP = (139, 0, 0)
BG_BOTTOM = (60, 0, 0)

UILIGHT = (255, 180, 180)
UIDARK = (180, 50, 50)
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
        HEIGHT = self.sm.HEIGHT

        # Generate the backgrouund image
        self.background = self.gradient(WIDTH, HEIGHT, BG_TOP, BG_BOTTOM, angle=45)
        
        noteSize = int(WIDTH * 0.75)
        
        albumArt = Image(self.am.image("album"))
        albumArt.build((noteSize, noteSize))
        
        self.title = Text("Song 2", int(UISIZE * 6), WHITE, align="left")
        self.title.build(self.am)
        
        self.artist = Text("A cool guy", int(UISIZE * 4), UILIGHT, align="left")
        self.artist.build(self.am)

        self.timeBar = Slider(noteSize, int(UISIZE * 4), UIDARK, UILIGHT)
        self.timeBar.build()

        self.timeLeft = Text("Time 1", int(UISIZE * 3), UILIGHT, align="left")
        self.timeLeft.build(self.am)
        
        self.timeRight = Text("Time 2", int(UISIZE * 3), UILIGHT, align="right")
        self.timeRight.build(self.am)
        
        soundBar = Slider(int(noteSize * 0.8), int(UISIZE * 4), UIDARK, UILIGHT)
        soundBar.build()

        muteImg = Image(self.am.image("mute"))
        muteImg.build((int(UISIZE * 4), int(UISIZE * 4)))
        
        volumeImg = Image(self.am.image("volume"))
        volumeImg.build((int(UISIZE * 4), int(UISIZE * 4)))

        x = WIDTH / 2 - noteSize / 2
        y = WIDTH / 2 + noteSize / 2 + UISIZE * 6
        
        albumArt.x, albumArt.y = x, x
        
        self.title.x, self.title.y = x, y
        
        y += UISIZE * 8
        self.artist.x, self.artist.y = x, y
        
        y += UISIZE * 9
        self.timeBar.x, self.timeBar.y = x, y
        
        y += UISIZE * 7
        self.timeLeft.x, self.timeLeft.y = x, y
        self.timeRight.x, self.timeRight.y = x + noteSize, y
        
        y += UISIZE * 7
        soundBar.x, soundBar.y = (WIDTH / 2 - soundBar.width / 2), y
        muteImg.x, muteImg.y = x, y
        volumeImg.x, volumeImg.y = (x + noteSize - volumeImg.surface.get_width()), y

        self.elements.extend([albumArt, self.title, self.artist, self.timeBar, self.timeLeft, self.timeRight, soundBar, muteImg, volumeImg])

    def gradient(self, width, height, color1, color2, angle=45):
        surf = pygame.Surface((width, height))
        angle_rad = math.radians(angle)
        dir_x = math.cos(angle_rad)
        dir_y = math.sin(angle_rad)

        corners = [(0, 0), (width, 0), (0, height), (width, height)]
        projections = [x * dir_x + y * dir_y for x, y in corners]
        min_p = min(projections)
        max_p = max(projections)
        diff_p = max_p - min_p if max_p != min_p else 1

        # Use numpy for performance
        x = np.linspace(0, width, width, endpoint=False)
        y = np.linspace(0, height, height, endpoint=False)
        xv, yv = np.meshgrid(x, y)
        
        proj = xv * dir_x + yv * dir_y
        t = (proj - min_p) / diff_p
        t = np.clip(t, 0, 1)

        r = (color1[0] + (color2[0] - color1[0]) * t).astype(np.uint8)
        g = (color1[1] + (color2[1] - color1[1]) * t).astype(np.uint8)
        b = (color1[2] + (color2[2] - color1[2]) * t).astype(np.uint8)

        rgb = np.stack((r, g, b), axis=-1)
        pygame.surfarray.blit_array(surf, rgb.swapaxes(0, 1))
        return surf

    def draw(self):
        screen = self.sm.screen
        screen.blit(self.background, (0, 0))
        
        # Use the generic draw method from the Element class
        for element in self.elements:
            element.draw(screen)