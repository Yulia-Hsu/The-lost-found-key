# sprites/platforms.py
import pygame
from settings import *
from assets import asset_manager

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, img_key='grass', is_fake=False):
        super().__init__()
        self.is_fake = is_fake
        self.image = pygame.Surface((w, h))
        tile = asset_manager.get_image(img_key, (TILE_SIZE, TILE_SIZE))
        for i in range(0, w, TILE_SIZE):
            for j in range(0, h, TILE_SIZE):
                self.image.blit(tile, (i, j), (0, 0, min(TILE_SIZE, w - i), min(TILE_SIZE, h - j)))
        if is_fake:
            self.image.fill(COLOR_PLATFORM_FAKE)
            self.image.set_alpha(200)
        self.rect = self.image.get_rect(topleft=(x, y))

class MovingPlatform(Platform):
    def __init__(self, x, y, w, h, img_key, dist, speed):
        super().__init__(x, y, w, h, img_key)
        self.dist = dist
        self.start_x = x
        self.change_x = speed

    def update(self):
        self.rect.x += self.change_x
        if abs(self.rect.x - self.start_x) > self.dist:
            self.change_x *= -1