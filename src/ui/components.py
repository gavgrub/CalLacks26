import pygame

# Base element
class Element:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pass

    def resize(self, scale):
        pass

# Text element
class Text(Element):
    def __init__(self, text, size, color, align="left"):
        super().__init__(0, 0)
        self.text = text
        self.size = size
        self.color = color
        self.align = align

    def build(self, ui):
        font = ui.getFont(self.size)
        self.surface = font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect()
        self.uiRef = ui

    def draw(self, screen):
        rect = self.rect.copy()

        if self.align == "left":
            rect.topleft = (self.x, self.y)
        elif self.align == "right":
            rect.topright = (self.x, self.y)

        screen.blit(self.surface, rect)

    def setText(self, newText):
        if self.text != newText:
            self.text = newText
            self.build(self.uiRef)

# Image element
class Image(Element):
    def __init__(self, img):
        super().__init__(0, 0)
        self.raw = img

    def build(self, size):
        self.surface = pygame.transform.scale(self.raw, size)

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))

# Slider element
class Slider(Element):
    def __init__(self, width, height, color):
        super().__init__(0, 0)
        self.width = width
        self.height = height
        self.color = color

    def build(self):
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.surface, self.color, (0, 0, self.width, self.height), border_radius=20)

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))