import pygame

X = 75
Y = 75 * 1.5
FPS = 60
CAPTION = "Music Player"

class ScreenManager:
    def __init__(self, size):
        self.fps = FPS
        self.currentScreen = None
        self.resize(size)
        pygame.display.set_caption(CAPTION)

    def resize(self, size):
        self.SIZE = size
        self.WIDTH = int(X * size)
        self.HEIGHT = int(Y * size)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        if self.currentScreen:
            self.currentScreen.build()

    def setScreen(self, screen):
        self.currentScreen = screen

    def draw(self):
        if self.currentScreen:
            self.currentScreen.draw()
        pygame.display.flip()

    def handleEvent(self, event):
        pass