# settings.py

# --- 視窗設定 ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "The lost earth keys"
HIGHSCORE_FILE = "data/highscores.json"

# --- 顏色定義 (莫蘭迪色系 - 優雅沈穩) ---
WHITE = (255, 250, 240)      # 稍微帶點米白，不刺眼
GRAY = (128, 128, 128)
TEXT_COLOR = (72, 85, 99)    # 深岩灰色，比純黑柔和

# 背景色
BG_COLOR_DAY = (229, 227, 218)   # 燕麥奶色
BG_COLOR_NIGHT = (67, 83, 99)    # 莫蘭迪深藍灰

# --- 物件配色 ---
# 平台
COLOR_PLATFORM_GRASS = (149, 165, 149)  # 鼠尾草綠
COLOR_PLATFORM_DIRT = (189, 174, 152)   # 奶茶棕
COLOR_PLATFORM_BRICK = (163, 174, 186)  # 霧霾藍灰
COLOR_PLATFORM_FAKE = (119, 110, 101)   # 深褐灰

# 互動物件
COLOR_SPIKE = (194, 124, 136)   # 豆沙紅 (不刺眼的紅色)
COLOR_COIN = (217, 196, 136)    # 復古金
COLOR_DOOR = (126, 148, 134)    # 灰綠色
COLOR_SPRING = (214, 166, 128)  # 髒橘色
COLOR_PLAYER = (115, 139, 158)  # 霧藍色
COLOR_PORTAL = (166, 149, 171)  # 芋泥紫
COLOR_MENU_BTN = (149, 165, 166) # 混凝土灰藍
COLOR_BEST_SCORE = (189, 174, 152)

# 炸彈顏色
COLOR_BOMB_IDLE = (52, 73, 94)      # 深青灰
COLOR_BOMB_EXPLODE = (200, 100, 100) # 柔和紅

# --- 物理與遊戲參數 ---
GRAVITY = 0.8
JUMP_POWER = -17
MOVE_SPEED = 6
BOUNCE_POWER = -24
PLAYER_SIZE = (60, 65)
TILE_SIZE = 80