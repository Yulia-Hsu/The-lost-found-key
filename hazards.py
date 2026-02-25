# sprites/hazards.py
import pygame
from settings import *
from assets import asset_manager

class Hazard(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, invisible=False, moving_type=None, active=True, speed=0, dist=0):
        super().__init__()
        self.invisible = invisible
        self.moving_type = moving_type
        self.active = active
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vy = 0
        self.vx = speed
        self.dist = dist
        self.start_x = x
        self.triggered = False

        if not invisible and active:
            self._draw_hazard(w, h)

    def _draw_hazard(self, w, h):
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        if self.moving_type == 'horizontal':
            img = asset_manager.get_image('spike_ball', (w, h))
            self.image.blit(img, (0, 0))
        else:
            tile = asset_manager.get_image('spike', (20, 20))
            for i in range(0, w, 20):
                self.image.blit(tile, (i, h - 20))

    def activate_trap(self):
        if not self.active or self.invisible:
            self.active = True
            self.invisible = False
            self.rect.width, self.rect.height = 40, 40
            self.image = asset_manager.get_image('spike_ball', (40, 40))
            if self.moving_type == 'falling':
                self.vy = 12
            if not self.triggered:
                asset_manager.play_sound('trap')
                self.triggered = True

    def update(self, player_rect):
        if not self.active: return

        if self.moving_type == 'falling':
            self.rect.y += self.vy
            if self.vy == 0 and not self.triggered and self.invisible:
                if abs(player_rect.centerx - self.rect.centerx) < 40 and player_rect.y > self.rect.y:
                    self.activate_trap()

        elif self.moving_type == 'horizontal':
            self.rect.x += self.vx
            if abs(self.rect.x - self.start_x) > self.dist:
                self.vx *= -1

class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.state = "COOLDOWN"
        self.timer = 0
        self.cooldown_time = 120
        self.explode_time = 60
        self.update_image()

    def update_image(self):
        if self.state == "COOLDOWN":
            self.image = asset_manager.get_image('bomb_idle', (40, 40))
            self.rect = self.image.get_rect(midbottom=(self.x, self.y))
        else:
            self.image = asset_manager.get_image('bomb_explode', (70, 70))
            self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def update(self):
        self.timer += 1
        if self.state == "COOLDOWN":
            if self.timer >= self.cooldown_time:
                self.state = "EXPLODE"
                self.timer = 0
                self.update_image()
                asset_manager.play_sound('trap')
        elif self.state == "EXPLODE":
            if self.timer >= self.explode_time:
                self.state = "COOLDOWN"
                self.timer = 0
                self.update_image()

class Trigger(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, target_hazards):
        super().__init__()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.target_hazards = target_hazards

    def check_trigger(self, player_rect):
        if self.rect.colliderect(player_rect):
            for hazard in self.target_hazards:
                hazard.activate_trap()
            self.kill()