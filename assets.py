# assets.py
import pygame
import os
from settings import * # 匯入顏色設定以繪製幾何圖形

class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.bgm_path = 'assets/audio/bgm.mp3'

        # 定義圖片路徑
        self.image_paths = {
            'player_idle': 'assets/player/p1_stand.png',
            'player_walk': 'assets/player/p1_walk.png',
            'player_jump': 'assets/player/p1_jump.png',
            'grass': 'assets/tiles/grass.png',
            'dirt': 'assets/tiles/dirt.png',
            'brick': 'assets/tiles/brick.png',
            'castle': 'assets/tiles/castle.png',
            'spike': 'assets/hazards/spike.png',
            'spike_ball': 'assets/hazards/spike_ball.png',
            'bomb_idle': 'assets/hazards/bomb.png',
            'bomb_explode': 'assets/hazards/explosion.png',
            'coin': 'assets/items/coin.png',
            'door_closed': 'assets/items/door_closed.png',
            'door_open': 'assets/items/door_open.png',
            'spring': 'assets/items/spring.png',
            'portal': 'assets/items/portal.png',
            'menu_bg': 'assets/ui/bg_menu.png',
        }

        self.sound_paths = {
            'jump': 'assets/audio/sfx_jump.ogg',
            'spring': 'assets/audio/sfx_jump-high.ogg',
            'coin': 'assets/audio/sfx_coin.ogg',
            'hurt': 'assets/audio/sfx_hurt.ogg',
            'portal': 'assets/audio/sfx_magic.ogg',
            'select': 'assets/audio/sfx_select.ogg',
            'trap': 'assets/audio/sfx_throw.ogg',
            'open': 'assets/audio/sfx_disappear.ogg',
            'win': 'assets/audio/sfx_gem.ogg',
            'explode': 'assets/audio/sfx_explode.ogg',
        }
        self.load_sounds()

    def load_sounds(self):
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()
            except:
                return
        for name, path in self.sound_paths.items():
            if os.path.exists(path):
                try:
                    sound = pygame.mixer.Sound(path)
                    sound.set_volume(0.4)
                    self.sounds[name] = sound
                except:
                    pass

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()

    def get_image(self, key, size=None):
        cache_key = f"{key}_{size}"
        if cache_key in self.images:
            return self.images[cache_key]

        image = None
        path = self.image_paths.get(key, "")

        # 1. 嘗試讀取圖片檔案
        if os.path.exists(path):
            try:
                raw_img = pygame.image.load(path).convert_alpha()
                if size:
                    image = pygame.transform.scale(raw_img, size)
                else:
                    image = raw_img
            except:
                pass

        # 2. 程式繪圖 fallback (這段邏輯保持不變，為了簡潔我只列出部分結構)
        if image is None:
            w, h = size if size else (40, 40)
            image = pygame.Surface((w, h), pygame.SRCALPHA)

            # --- 繪圖邏輯 (與原程式相同) ---
            if 'player' in key:
                pygame.draw.rect(image, COLOR_PLAYER, (0, 0, w, h), border_radius=8)
                pygame.draw.rect(image, WHITE, (5, 8, 8, 8))
                pygame.draw.rect(image, WHITE, (w - 13, 8, 8, 8))
            elif key in ['grass', 'dirt', 'brick', 'castle']:
                color = COLOR_PLATFORM_GRASS
                if 'dirt' in key: color = COLOR_PLATFORM_DIRT
                elif 'brick' in key or 'castle' in key: color = COLOR_PLATFORM_BRICK
                image.fill(color)
                pygame.draw.rect(image, WHITE, (0, 0, w, h), 2)
            elif 'spike' in key:
                if 'ball' in key:
                    pygame.draw.circle(image, COLOR_SPIKE, (w // 2, h // 2), w // 2)
                    pygame.draw.circle(image, (255, 100, 100), (w // 2 - 5, h // 2 - 5), 5)
                else:
                    points = [(0, h), (w // 2, 0), (w, h)]
                    pygame.draw.polygon(image, COLOR_SPIKE, points)
            elif 'bomb' in key:
                if 'explode' in key:
                    pygame.draw.circle(image, COLOR_BOMB_EXPLODE, (w // 2, h // 2), w // 2)
                    pygame.draw.circle(image, (241, 196, 15), (w // 2, h // 2), w // 3)
                else:
                    pygame.draw.circle(image, COLOR_BOMB_IDLE, (w // 2, h - 5), w // 2 - 5)
                    pygame.draw.line(image, (50, 50, 50), (w // 2, h // 2), (w // 2, 0), 3)
                    pygame.draw.circle(image, (200, 50, 50), (w // 2, 2), 3)
            elif 'coin' in key:
                pygame.draw.circle(image, COLOR_COIN, (w // 2, h // 2), w // 2)
                pygame.draw.circle(image, (255, 240, 100), (w // 2, h // 2), w // 3)
            elif 'spring' in key:
                pygame.draw.rect(image, COLOR_SPRING, (0, h // 2, w, h // 2))
            elif 'door' in key:
                pygame.draw.rect(image, COLOR_DOOR, (0, 0, w, h), border_radius=5)
                if 'open' in key:
                    pygame.draw.rect(image, (50, 50, 50), (5, 5, w - 10, h - 5))
            elif 'portal' in key:
                pygame.draw.ellipse(image, COLOR_PORTAL, (0, 0, w, h))
                pygame.draw.ellipse(image, WHITE, (10, 10, w - 20, h - 20), 2)
            # assets.py 內的 get_image Fallback 部分
            elif 'grass_' in key:
                image.fill(COLOR_PLATFORM_GRASS)
                if 'left' in key:
                    pygame.draw.line(image, WHITE, (0, 0), (0, h), 5)  # 左邊畫一條線示意
                elif 'right' in key:
                    pygame.draw.line(image, WHITE, (w, 0), (w, h), 5)  # 右邊畫一條線示意
                pygame.draw.rect(image, (100, 150, 50), (0, 0, w, 10))  # 頂部深色草
            else:
                image.fill((150, 150, 150))
            # ---------------------------

        self.images[cache_key] = image
        return image

    def play_music(self):
        if os.path.exists(self.bgm_path):
            try:
                pygame.mixer.music.load(self.bgm_path)
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
            except:
                pass

# 建立全域實例供其他模組引用
asset_manager = AssetManager()