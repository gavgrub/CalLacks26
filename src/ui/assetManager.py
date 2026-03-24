import pygame
import os

class AssetManager:
    def __init__(self):
        self.font_cache = {}
        self.images = {}
        if not os.path.exists("assets/img"):
            os.makedirs("assets/img")
        self.loadImg()

    def loadImg(self, folder="assets/img"):
        for file in os.listdir(folder):
            if file.endswith(".png"):
                name = os.path.splitext(file)[0]
                full_path = os.path.join(folder, file)
                self.images[name] = pygame.image.load(full_path).convert_alpha()

    def image(self, name):
        return self.images.get(name, pygame.Surface((10, 10)))

    def getFont(self, size):
        size = int(size)
        if size not in self.font_cache:
            try:
                self.font_cache[size] = pygame.font.Font("assets/Sansation.ttf", size)
            except:
                self.font_cache[size] = pygame.font.SysFont("Arial", size)
        return self.font_cache[size]