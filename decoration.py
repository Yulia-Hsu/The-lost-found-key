# sprites/decoration.py
import pygame

class Decoration(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((100, 50), pygame.SRCALPHA)
        c = (255, 255, 255, 150)
        pygame.draw.circle(self.image, c, (30, 30), 25)
        pygame.draw.circle(self.image, c, (70, 30), 30)
        pygame.draw.circle(self.image, c, (50, 20), 25)
        self.rect = self.image.get_rect(topleft=(x, y))