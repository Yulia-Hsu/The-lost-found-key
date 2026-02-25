# sprites/items.py
import pygame
from settings import *
from assets import asset_manager

class Spring(pygame.sprite.Sprite):
    def __init__(self, x, y, fake=False):
        super().__init__()
        self.fake = fake
        self.image = asset_manager.get_image('spring', (40, 30))
        self.rect = self.image.get_rect(topleft=(x, y))

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = asset_manager.get_image('portal', (40, 60))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.target_pos = (target_x, target_y)

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = asset_manager.get_image('coin', (50, 50))
        self.rect = self.image.get_rect(center=(x, y))

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image_closed = asset_manager.get_image('door_closed', (50, 80))
        self.image_open = asset_manager.get_image('door_open', (50, 80))
        self.image = self.image_closed
        self.rect = self.image.get_rect(bottomleft=(x, y))

    def open(self):
        if self.image != self.image_open:
            self.image = self.image_open
            asset_manager.play_sound('open')