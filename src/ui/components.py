import pygame
import os

# Base element
class Element:
    def __init__(self, x, y, action=None):
        self.x = x
        self.y = y
        self.action = action
        self.rect = pygame.Rect(x, y, 0, 0)

    def execute(self, *args):
        if self.action is not None:
            self.action(*args)

    def isHovered(self, mousePos):
        return self.rect.collidepoint(mousePos)

    def draw(self, screen):
        pass

    def resize(self, scale):
        pass

# Text element
class Text(Element):
    def __init__(self, text, size, color, align="left", action=None):
        super().__init__(0, 0, action)
        self.text = text
        self.size = size
        self.color = color
        self.align = align
        self.uiRef = None
        self.surface = None

    def build(self, ui):
        self.uiRef = ui
        font = ui.getFont(self.size)
        self.surface = font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect()

    def draw(self, screen):
        if self.surface is None:
            return
            
        if self.align == "left":
            self.rect.topleft = (self.x, self.y)
        elif self.align == "right":
            self.rect.topright = (self.x, self.y)
            
        screen.blit(self.surface, self.rect)

    def setText(self, newText):
        if self.text != newText:
            self.text = newText
            if self.uiRef:
                self.build(self.uiRef)

# Image element
class Image(Element):
    def __init__(self, img, action=None):
        super().__init__(0, 0, action)
        self.raw = img
        self.surface = None

    def build(self, size):
        self.surface = pygame.transform.scale(self.raw, size)
        self.rect = self.surface.get_rect()

    def draw(self, screen):
        if self.surface:
            self.rect.topleft = (self.x, self.y)
            screen.blit(self.surface, self.rect)

# Slider element
class Slider(Element):
    def __init__(self, width, height, background, fill, action=None):
        super().__init__(0, 0, action)
        self.width = width
        self.height = height
        self.bgColor = background
        self.fillColor = fill
        self.progress = 0.0
        self.bgSurface = None
        self.fillSurface = None
        self.rect = pygame.Rect(0, 0, width, height)

    def build(self):
        self.bgSurface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.bgSurface, self.bgColor, (0, 0, self.width, self.height), border_radius=int(self.height / 2))
        
        self.fillSurface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.fillSurface, self.fillColor, (0, 0, self.width, self.height), border_radius=int(self.height / 2))
        self.rect.size = (self.width, self.height)

    def resize(self, newWidth, newHeight):
        self.width = newWidth
        self.height = newHeight
        self.build()

    def setProgress(self, value):
        self.progress = max(0.0, min(1.0, value))

    def handleClick(self, mousePos):
        if self.isHovered(mousePos):
            relativeX = mousePos[0] - self.x
            newProgress = relativeX / self.width
            self.setProgress(newProgress)
            self.execute(newProgress)
            return True
        return False

    def draw(self, screen):
        if self.bgSurface is None:
            self.build()
            
        self.rect.topleft = (self.x, self.y)
        screen.blit(self.bgSurface, self.rect)
        
        if self.fillSurface and self.progress > 0:
            fillWidth = int(self.width * self.progress)
            screen.blit(self.fillSurface, (self.x, self.y), (0, 0, fillWidth, self.height))