import pygame
import sys
import os
import time
import json

# 如果是打包後執行檔, 切換工作目錄到解壓後的暫存路徑
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

from settings import *
from assets import asset_manager as assets

# 匯入我們拆分好的類別
from sprites.items import Coin, Door, Spring, Portal
from sprites.player import Player
from sprites.platforms import Platform, MovingPlatform
from sprites.hazards import Bomb, Hazard, Trigger
from sprites.decoration import Decoration


# --- 關卡設定 ---
class Level:
    def __init__(self):
        self.platforms = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        self.springs = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.triggers = pygame.sprite.Group()
        self.decorations = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.door = None
        self.player_start = (50, 500)
        self.name = ""

    def load(self, level_id):
        self.platforms.empty()
        self.hazards.empty()
        self.springs.empty()
        self.portals.empty()
        self.coins.empty()
        self.triggers.empty()
        self.decorations.empty()
        self.bombs.empty()

        self.platforms.add(Platform(-20, 0, 20, SCREEN_HEIGHT, 'brick'))
        self.platforms.add(Platform(SCREEN_WIDTH, 0, 20, SCREEN_HEIGHT, 'brick'))

        self.decorations.add(Decoration(100, 100))
        self.decorations.add(Decoration(600, 150))
        self.decorations.add(Decoration(350, 80))

        if level_id == 1:
            self.name = "Tutorial"
            self.player_start = (50, 480)
            self.platforms.add(Platform(0, 550, 800, 50, 'grass'))
            self.platforms.add(Platform(200, 450, 100, 20, 'grass'))
            self.platforms.add(Platform(400, 350, 100, 20, 'grass'))
            self.platforms.add(Platform(600, 250, 200, 20, 'grass'))
            self.hazards.add(Hazard(320, 530, 60, 20))
            self.springs.add(Spring(500, 520))
            self.coins.add(Coin(700, 200))
            self.door = Door(750, 550)

        elif level_id == 2:
            self.name = "The Floor is Lava"
            self.player_start = (30, 100)
            self.platforms.add(Platform(0, 150, 100, 20, 'brick'))
            self.hazards.add(Hazard(0, 580, 800, 20))
            self.platforms.add(Platform(0, 595, 800, 5, 'brick'))
            self.springs.add(Spring(150, 500))
            self.springs.add(Spring(300, 350))
            self.springs.add(Spring(450, 500))
            self.springs.add(Spring(600, 350))
            self.platforms.add(Platform(700, 200, 100, 20, 'brick'))
            self.coins.add(Coin(620, 100))
            self.door = Door(750, 200)

        elif level_id == 3:
            self.name = "Portal Logic"
            self.player_start = (50, 500)
            self.platforms.add(Platform(0, 550, 800, 50, 'castle'))
            self.platforms.add(Platform(250, 0, 20, 450, 'castle'))
            self.platforms.add(Platform(550, 150, 20, 450, 'castle'))
            self.platforms.add(Platform(0, 400, 100, 20, 'castle'))
            self.hazards.add(Hazard(270, 530, 280, 20))
            self.platforms.add(Platform(350, 300, 100, 20, 'castle'))
            self.platforms.add(Platform(570, 200, 100, 20, 'castle'))
            self.portals.add(Portal(50, 340, 600, 450))
            self.portals.add(Portal(400, 240, 700, 100))
            self.portals.add(Portal(700, 500, 380, 250))
            self.coins.add(Coin(650, 400))
            self.door = Door(620, 200)

        elif level_id == 4:
            self.name = "The Troll"
            self.player_start = (50, 500)
            self.platforms.add(Platform(0, 550, 150, 50, 'dirt'))
            self.platforms.add(Platform(650, 550, 150, 50, 'dirt'))
            self.platforms.add(Platform(150, 550, 500, 50, 'dirt', is_fake=True))
            self.hazards.add(Hazard(150, 580, 500, 20))
            self.platforms.add(Platform(80, 400, 80, 20, 'dirt'))

            self.bombs.add(Bomb(80, 400))

            self.platforms.add(Platform(200, 450, 50, 20, 'box'))
            self.platforms.add(Platform(300, 350, 50, 20, 'box'))
            self.platforms.add(Platform(400, 250, 50, 20, 'box'))
            self.platforms.add(Platform(550, 300, 100, 20, 'dirt'))

            trap_enemy = Hazard(425, 0, 40, 40, invisible=True, moving_type='falling', active=False)
            self.hazards.add(trap_enemy)

            trigger_zone = Trigger(415, 200, 50, 100, [trap_enemy])
            self.triggers.add(trigger_zone)

            self.hazards.add(Hazard(600, 50, 40, 40, invisible=True, moving_type='falling'))

            self.coins.add(Coin(425, 230))
            self.door = Door(750, 550)

        elif level_id == 5:
            self.name = "FINAL EXAM"
            self.player_start = (50, 500)
            self.platforms.add(Platform(0, 550, 150, 50, 'castle'))
            self.hazards.add(Hazard(150, 590, 650, 10))

            mp1 = MovingPlatform(200, 450, 80, 20, 'castle', 150, 3)
            self.platforms.add(mp1)
            mp2 = MovingPlatform(400, 300, 80, 20, 'castle', 150, 5)
            self.platforms.add(mp2)

            self.springs.add(Spring(50, 350))
            self.platforms.add(Platform(600, 200, 100, 20, 'castle'))

            bird1 = Hazard(200, 150, 30, 30, moving_type='horizontal', speed=3, dist=150)
            bird2 = Hazard(450, 80, 30, 30, moving_type='horizontal', speed=4, dist=150)
            self.hazards.add(bird1)
            self.hazards.add(bird2)

            self.portals.add(Portal(650, 150, 100, 100))
            self.coins.add(Coin(750, 100))
            self.platforms.add(Platform(700, 250, 100, 20, 'castle'))
            self.door = Door(750, 250)


# --- 主程式控制 ---
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        assets.play_music()

        self.level_manager = Level()
        self.player = None
        self.current_level_num = 1
        self.state = "MENU"
        self.mode = "ALL"

        self.level_start_time = 0
        self.accumulated_time = 0
        self.level_records = {}

        self.highscores = self.load_highscores()

        self.level_buttons = []
        positions = [(150, 200), (400, 200), (650, 200), (275, 400), (525, 400)]
        for i, pos in enumerate(positions, 1):
            rect = pygame.Rect(0, 0, 160, 140)
            rect.center = pos
            self.level_buttons.append((i, rect))

        self.preview_images = {}
        self.load_previews()

    def load_previews(self):
        folder = "assets/previews"
        for i in range(1, 6):
            path = f"{folder}/level_{i}.png"
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.smoothscale(img, (180, 140))
                self.preview_images[i] = img

    def load_highscores(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        if os.path.exists(HIGHSCORE_FILE):
            try:
                with open(HIGHSCORE_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_highscores(self):
        with open(HIGHSCORE_FILE, 'w') as f:
            json.dump(self.highscores, f)

    def update_highscore(self, level, time_val):
        lvl_key = str(level)
        current_best = self.highscores.get(lvl_key, None)
        if time_val == "SKIP":
            return
        if current_best is None or current_best == "SKIP" or time_val < current_best:
            self.highscores[lvl_key] = time_val
            self.save_highscores()

    def reset_level(self, level_id, hard_reset=True):
        self.level_manager.load(level_id)
        self.player = Player(*self.level_manager.player_start)
        if hard_reset:
            self.accumulated_time = 0
        else:
            time_spent = time.time() - self.level_start_time
            self.accumulated_time += time_spent
        self.level_start_time = time.time()
        self.player.portal_cooldown = 0

    def draw_text(self, text, size, color, x, y, align="center"):
        font = pygame.font.Font(None, size)
        surf = font.render(str(text), True, color)
        rect = surf.get_rect()
        if align == "center":
            rect.center = (x, y)
        elif align == "left":
            rect.topleft = (x, y)
        elif align == "right":
            rect.topright = (x, y)
        self.screen.blit(surf, rect)

    def finish_level(self, skipped=False):
        current_run_time = time.time() - self.level_start_time
        total_level_time = round(self.accumulated_time + current_run_time, 2)

        if skipped:
            self.level_records[self.current_level_num] = "SKIP"
        else:
            self.level_records[self.current_level_num] = total_level_time
            assets.play_sound('win')
            self.update_highscore(self.current_level_num, total_level_time)

        if self.mode == "SINGLE":
            self.state = "WIN"
        else:
            if self.current_level_num < 5:
                self.state = "WIN"
            else:
                self.state = "GRADUATED"

    def next_level(self):
        if self.mode == "SINGLE":
            self.state = "LEVEL_SELECT"
        else:
            self.current_level_num += 1
            self.reset_level(self.current_level_num, hard_reset=True)
            self.state = "PLAYING"

    def draw_level_preview(self, lvl, rect):
        preview_rect = pygame.Rect(rect.x + 10, rect.y + 35, rect.width - 20, rect.height - 60)
        pygame.draw.rect(self.screen, (20, 20, 20), preview_rect)
        if lvl in self.preview_images:
            img = self.preview_images[lvl]
            display_img = pygame.transform.smoothscale(img, (preview_rect.width, preview_rect.height))
            self.screen.blit(display_img, preview_rect)
        else:
            pygame.draw.line(self.screen, (100, 100, 100), preview_rect.topleft, preview_rect.bottomright, 2)
            pygame.draw.line(self.screen, (100, 100, 100), preview_rect.topright, preview_rect.bottomleft, 2)
        pygame.draw.rect(self.screen, (200, 200, 200), preview_rect, 1)

    def run(self):
        running = True
        while running:
            # 1. 事件處理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.state == "MENU":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            assets.play_sound('select')
                            self.state = "MODE_SELECT"
                        elif event.key == pygame.K_ESCAPE:
                            running = False

                elif self.state == "MODE_SELECT":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            assets.play_sound('select')
                            self.mode = "ALL"
                            self.current_level_num = 1
                            self.level_records = {}
                            self.reset_level(1, hard_reset=True)
                            self.state = "PLAYING"
                        elif event.key == pygame.K_2:
                            assets.play_sound('select')
                            self.mode = "SINGLE"
                            self.state = "LEVEL_SELECT"
                        elif event.key == pygame.K_ESCAPE:
                            self.state = "MENU"

                elif self.state == "LEVEL_SELECT":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        for lvl, rect in self.level_buttons:
                            if rect.collidepoint(mx, my):
                                assets.play_sound('select')
                                self.current_level_num = lvl
                                self.level_records = {}
                                self.reset_level(lvl, hard_reset=True)
                                self.state = "PLAYING"
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = "MODE_SELECT"

                elif self.state == "PLAYING":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.player.go_left()
                        elif event.key == pygame.K_RIGHT:
                            self.player.go_right()
                        elif event.key == pygame.K_SPACE:
                            self.player.jump()
                        elif event.key == pygame.K_r:
                            self.reset_level(self.current_level_num, hard_reset=False)
                        elif event.key == pygame.K_ESCAPE:
                            self.state = "MENU"
                        elif event.key == pygame.K_F1:
                            self.finish_level(skipped=True)
                    if event.type == pygame.KEYUP:
                        if (event.key == pygame.K_LEFT and self.player.change_x < 0) or \
                                (event.key == pygame.K_RIGHT and self.player.change_x > 0):
                            self.player.stop()

                elif self.state in ["WIN", "GAMEOVER"]:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            assets.play_sound('select')
                            if self.state == "GAMEOVER":
                                self.reset_level(self.current_level_num, hard_reset=False)
                                self.state = "PLAYING"
                            else:  # WIN
                                self.next_level()
                        elif event.key == pygame.K_ESCAPE:
                            self.state = "MENU"

                elif self.state == "GRADUATED":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            assets.play_sound('select')
                            self.state = "MENU"
                        elif event.key == pygame.K_ESCAPE:
                            running = False

            # 2. 繪圖
            self.screen.fill(BG_COLOR_DAY)

            if self.state == "MENU":
                self.screen.blit(assets.get_image('menu_bg', (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
                s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                s.fill((48, 51, 107, 200))
                self.screen.blit(s, (0, 0))
                self.draw_text("The lost earth keys", 80, WHITE, 400, 150)
                self.draw_text("Press ENTER to Start", 40, WHITE, 400, 300)
                self.draw_text("Arrows: Move | Space: Jump | F1: Secret Skip", 24, WHITE, 400, 500)

            elif self.state == "MODE_SELECT":
                self.screen.fill(BG_COLOR_NIGHT)
                self.draw_text("Select Mode", 60, WHITE, 400, 150)
                self.draw_text("1. Full Course (All 5 Levels)", 40, WHITE, 400, 300)
                self.draw_text("2. Practice Single Level", 40, (180, 180, 180), 400, 400)
                self.draw_text("[ESC] Back", 30, WHITE, 100, 550)

            elif self.state == "LEVEL_SELECT":
                self.screen.fill(BG_COLOR_NIGHT)
                self.draw_text("Select Level", 50, WHITE, 400, 80)

                for lvl, rect in self.level_buttons:
                    pygame.draw.rect(self.screen, COLOR_MENU_BTN, rect, border_radius=10)
                    pygame.draw.rect(self.screen, WHITE, rect, 3, border_radius=10)
                    self.draw_text(f"Lv {lvl}", 28, TEXT_COLOR, rect.centerx, rect.y + 20)
                    self.draw_level_preview(lvl, rect)
                    best = self.highscores.get(str(lvl), "---")
                    bst_str = f"Best: {best}s" if isinstance(best, (int, float)) else "Best: ---"
                    self.draw_text(bst_str, 20, (50, 50, 50), rect.centerx, rect.bottom - 15)

                self.draw_text("[ESC] Back", 30, WHITE, 100, 550)

            elif self.state == "PLAYING":
                self.level_manager.decorations.draw(self.screen)
                if self.level_manager.door:
                    self.screen.blit(self.level_manager.door.image, self.level_manager.door.rect)
                for p in self.level_manager.platforms:
                    self.screen.blit(p.image, p.rect)
                    if isinstance(p, MovingPlatform): p.update()

                self.level_manager.hazards.update(self.player.rect)
                for h in self.level_manager.hazards:
                    self.screen.blit(h.image, h.rect)

                self.level_manager.bombs.update()
                for b in self.level_manager.bombs:
                    self.screen.blit(b.image, b.rect)

                self.level_manager.springs.draw(self.screen)
                self.level_manager.portals.draw(self.screen)
                self.level_manager.coins.draw(self.screen)
                for trigger in self.level_manager.triggers:
                    trigger.check_trigger(self.player.rect)

                status = self.player.update(self.level_manager)
                self.screen.blit(self.player.image, self.player.rect)

                if pygame.sprite.spritecollide(self.player, self.level_manager.coins, True):
                    assets.play_sound('coin')
                    self.player.has_key = True
                    self.level_manager.door.open()

                spring_hits = pygame.sprite.spritecollide(self.player, self.level_manager.springs, False)
                for spring in spring_hits:
                    if self.player.change_y > 0:
                        self.player.rect.bottom = spring.rect.top
                        self.player.change_y = BOUNCE_POWER
                        self.player.jump_count = 1
                        assets.play_sound('spring')

                portal_hits = pygame.sprite.spritecollide(self.player, self.level_manager.portals, False)
                if portal_hits and self.player.portal_cooldown == 0:
                    portal = portal_hits[0]
                    self.player.rect.topleft = portal.target_pos
                    self.player.portal_cooldown = 30
                    assets.play_sound('portal')

                if self.player.has_key and pygame.sprite.collide_rect(self.player, self.level_manager.door):
                    self.finish_level(skipped=False)

                bomb_hits = pygame.sprite.spritecollide(self.player, self.level_manager.bombs, False)
                for b in bomb_hits:
                    if b.state == "EXPLODE":
                        assets.play_sound('hurt')
                        self.state = "GAMEOVER"

                if status == "DEAD" or \
                        pygame.sprite.spritecollide(self.player, self.level_manager.hazards, False):
                    assets.play_sound('hurt')
                    self.state = "GAMEOVER"

            # --- WIN 狀態：顯示單關成績與該關最佳紀錄 ---
            elif self.state == "WIN":
                s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                s.fill((0, 0, 0, 150))
                self.screen.blit(s, (0, 0))
                self.draw_text("Level Passed!", 80, WHITE, 400, 180)

                # 取得當前時間
                cur_time = self.level_records.get(self.current_level_num, "---")
                # 取得歷史最佳
                best_time = self.highscores.get(str(self.current_level_num), "---")

                # 顯示兩行數據
                self.draw_text(f"Time: {cur_time}s", 50, WHITE, 400, 280)
                self.draw_text(f"Best: {best_time}s", 40, (255, 215, 0), 400, 340)  # 金色顯示最佳

                self.draw_text("[R] Next / [ESC] Menu", 30, WHITE, 400, 500)

            elif self.state == "GAMEOVER":
                s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                s.fill((50, 0, 0, 150))
                self.screen.blit(s, (0, 0))
                self.draw_text("WASTED", 100, (255, 50, 50), 400, 200)
                self.draw_text("Don't give up!", 40, WHITE, 400, 350)
                self.draw_text("[R] Retry / [ESC] Menu", 30, WHITE, 400, 500)

            # --- GRADUATED 狀態：全破後的計分板 ---
            elif self.state == "GRADUATED":
                self.screen.fill((189, 174, 152))
                self.draw_text("You found all the lost keys!", 40, (50, 50, 50), 400, 80)
                self.draw_text("Scoreboard", 40, (100, 100, 100), 400, 140)

                # 繪製表格標頭
                header_y = 190
                self.draw_text("Level", 30, (0, 0, 0), 250, header_y)
                self.draw_text("Current", 30, (0, 0, 0), 400, header_y)
                self.draw_text("Best", 30, (0, 0, 0), 550, header_y)

                # 畫線隔開
                pygame.draw.line(self.screen, (0, 0, 0), (200, 210), (600, 210), 2)

                y_offset = 230
                for lvl in range(1, 6):
                    # 當次成績
                    record = self.level_records.get(lvl, "---")
                    # 最佳成績
                    best = self.highscores.get(str(lvl), "---")

                    # 繪製每一列
                    self.draw_text(f"Lv {lvl}", 30, (50, 50, 50), 250, y_offset)
                    self.draw_text(f"{record}s", 30, (50, 50, 150), 400, y_offset)
                    self.draw_text(f"{best}s", 30, (150, 50, 50), 550, y_offset)

                    y_offset += 40

                self.draw_text("[R] Return to Menu", 30, (50, 50, 50), 400, 550)

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()