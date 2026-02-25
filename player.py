# sprites/player.py
import pygame
from settings import *
from assets import asset_manager

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = asset_manager.get_image('player_idle', PLAYER_SIZE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.change_x = 0
        self.change_y = 0
        self.jump_count = 0
        self.facing_right = True
        self.on_ground = False
        self.portal_cooldown = 0
        self.has_key = False

    def update(self, level_data):
        if self.portal_cooldown > 0: self.portal_cooldown -= 1

        # X 軸移動
        self.rect.x += self.change_x
        hits = pygame.sprite.spritecollide(self, level_data.platforms, False)
        for block in hits:
            if not getattr(block, 'is_fake', False):
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                elif self.change_x < 0:
                    self.rect.left = block.rect.right

        # Y 軸移動 (重力)
        self.change_y += GRAVITY
        self.rect.y += self.change_y
        self.on_ground = False
        hits = pygame.sprite.spritecollide(self, level_data.platforms, False)
        for block in hits:
            if not getattr(block, 'is_fake', False):
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                    self.change_y = 0
                    self.jump_count = 0
                    self.on_ground = True
                    # 跟隨移動平台
                    if hasattr(block, 'change_x'):
                        self.rect.x += block.change_x
                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom
                    self.change_y = 0

        # 邊界檢查
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH

        # 更新動畫圖片
        key = 'player_jump' if not self.on_ground else ('player_walk' if self.change_x != 0 else 'player_idle')
        img = asset_manager.get_image(key, PLAYER_SIZE)
        if not self.facing_right: img = pygame.transform.flip(img, True, False)
        self.image = img

        if self.rect.top > SCREEN_HEIGHT: return "DEAD"
        return "ALIVE"

    def jump(self):
        if self.jump_count < 2:
            self.change_y = JUMP_POWER
            self.jump_count += 1
            asset_manager.play_sound('jump')

    def go_left(self):
        self.change_x = -MOVE_SPEED
        self.facing_right = False

    def go_right(self):
        self.change_x = MOVE_SPEED
        self.facing_right = True

    def stop(self):
        self.change_x = 0
