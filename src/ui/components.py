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
    def __init__(self, width, height, background, fill):
        super().__init__(0, 0)
        self.width = width
        self.height = height
        self.bg_color = background
        self.fill_color = fill
        self.progress = 0.0
        self.bg_surface = None
        self.fill_surface = None

    def build(self):
        self.bg_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.bg_surface, self.bg_color, (0, 0, self.width, self.height), border_radius=int(self.height / 2))
        
        self.fill_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.fill_surface, self.fill_color, (0, 0, self.width, self.height), border_radius=int(self.height / 2))

    def resize(self, new_width, new_height):
        self.width = new_width
        self.height = new_height
        self.build()

    def setProgress(self, value):
        self.progress = max(0.0, min(1.0, value))

    def draw(self, screen):
        if self.bg_surface:
            screen.blit(self.bg_surface, (self.x, self.y))
        
        if self.fill_surface and self.progress > 0:
            fillWidth = int(self.width * self.progress)
            screen.blit(self.fill_surface, (self.x, self.y), (0, 0, fillWidth, self.height))