import pygame
import sys
import os
import random
import math

# --- 初始化 Pygame ---
pygame.init()

# --- 游戏常量 ---
# 游戏计时器变量
game_start_time = 0 # 游戏开始的时间点
game_duration = 0   # 游戏已经进行的持续时间 (秒)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAP_WIDTH = 2400  # 扩展地图宽度
FPS = 60
GAME_STATE_MENU = 0
GAME_STATE_PLAYING = 1
GAME_STATE_ACHIEVEMENTS = 2
GAME_STATE_GAME_OVER = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
MARIO_WIDTH = 32
MARIO_HEIGHT = 48
MARIO_SPEED = 5
JUMP_STRENGTH = -12
GRAVITY = 0.5
GOOMBA_WIDTH = 32
GOOMBA_HEIGHT = 32
GOOMBA_SPEED = 2
GOOMBA_COLOR = (150, 75, 0)
KOOPA_WIDTH = 40
KOOPA_HEIGHT = 50
KOOPA_COLOR = (0, 200, 0)
FIREBALL_WIDTH = 32
FIREBALL_HEIGHT = 32
GROUND_HEIGHT = 50
GROUND_COLOR = (139, 69, 19)
BOSS_MOVE_LEFT_LIMIT = 100
BOSS_MOVE_RIGHT_LIMIT = SCREEN_WIDTH - 100
BOSS_MOVE_TOP_LIMIT = 0
BOSS_MOVE_BOTTOM_LIMIT = SCREEN_HEIGHT - GROUND_HEIGHT - 100

TILE_SIZE = 20
# --- 关卡数据 ---
levels = [
    # 第一关（现有地图）
    {
        "map_width": 2400,
        "platforms": [
            {"x": 0, "y": SCREEN_HEIGHT - GROUND_HEIGHT, "width": 2400, "height": GROUND_HEIGHT},
            {"x": 200, "y": SCREEN_HEIGHT - 200, "width": 150, "height": 20},
            {"x": 400, "y": SCREEN_HEIGHT - 300, "width": 150, "height": 20},
            {"x": 600, "y": SCREEN_HEIGHT - 250, "width": 150, "height": 20},
            {"x": 900, "y": SCREEN_HEIGHT - 350, "width": 150, "height": 20},
            {"x": 1200, "y": SCREEN_HEIGHT - 200, "width": 150, "height": 20},
            {"x": 1500, "y": SCREEN_HEIGHT - 300, "width": 150, "height": 20},
            {"x": 1800, "y": SCREEN_HEIGHT - 250, "width": 150, "height": 20},
            {"x": 2100, "y": SCREEN_HEIGHT - 350, "width": 150, "height": 20},
        ],
        "enemies": [
            {"type": "goomba", "x": 300, "y": SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT},
            {"type": "goomba", "x": 700, "y": SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT},
            {"type": "goomba", "x": 1000, "y": SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT},
            {"type": "goomba", "x": 1400, "y": SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT},
            {"type": "goomba", "x": 2000, "y": SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT},
            {"type": "koopa", "x": 1200, "y": SCREEN_HEIGHT - 350},
            {"type": "koopa", "x": 1800, "y": SCREEN_HEIGHT - 350},
        ],
        "powerups": [
            {"type": "fire_flower", "x": 300, "y": SCREEN_HEIGHT - 350},
            {"type": "ice_flower", "x": 350, "y": SCREEN_HEIGHT - 400},
        ]
    },
    # 第二关（示例：更短地图，更多敌人）
    {
        "map_width": 2000,
        "platforms": [
            {"x": 0, "y": SCREEN_HEIGHT - GROUND_HEIGHT, "width": 2000, "height": GROUND_HEIGHT},
            {"x": 300, "y": SCREEN_HEIGHT - 250, "width": 200, "height": 20},
            {"x": 600, "y": SCREEN_HEIGHT - 350, "width": 200, "height": 20},
            {"x": 1000, "y": SCREEN_HEIGHT - 200, "width": 200, "height": 20},
            {"x": 1400, "y": SCREEN_HEIGHT - 300, "width": 200, "height": 20},
        ],
        "enemies": [
            {"type": "goomba", "x": 400, "y": SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT},
            {"type": "goomba", "x": 800, "y": SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT},
            {"type": "goomba", "x": 1200, "y": SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT},
            {"type": "koopa", "x": 600, "y": SCREEN_HEIGHT - 350},
            {"type": "koopa", "x": 1000, "y": SCREEN_HEIGHT - 350},
            {"type": "boss", "x": 1600, "y": SCREEN_HEIGHT - GROUND_HEIGHT - 64},  # BossEnemy
        ],
        "powerups": [
            {"type": "fire_flower", "x": 500, "y": SCREEN_HEIGHT - 350},
        ]
    },
    # 第三关（示例：更长地图，密集平台）
    {
        "map_width": 3000,
        "platforms": [
            {"x": 0, "y": SCREEN_HEIGHT - GROUND_HEIGHT, "width": 3000, "height": GROUND_HEIGHT},
            {"x": 200, "y": SCREEN_HEIGHT - 200, "width": 150, "height": 20},
            {"x": 500, "y": SCREEN_HEIGHT - 300, "width": 150, "height": 20},
            {"x": 800, "y": SCREEN_HEIGHT - 250, "width": 150, "height": 20},
            {"x": 1100, "y": SCREEN_HEIGHT - 350, "width": 150, "height": 20},
            {"x": 1400, "y": SCREEN_HEIGHT - 200, "width": 150, "height": 20},
            {"x": 1700, "y": SCREEN_HEIGHT - 300, "width": 150, "height": 20},
            {"x": 2000, "y": SCREEN_HEIGHT - 250, "width": 150, "height": 20},
            {"x": 2300, "y": SCREEN_HEIGHT - 350, "width": 150, "height": 20},
            {"x": 2600, "y": SCREEN_HEIGHT - 200, "width": 150, "height": 20},

        ],
        "enemies": [
            {"type": "goomba", "x": 300, "y": SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT},

            {"type": "goomba", "x": 1100, "y": SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT},
            {"type": "goomba", "x": 1500, "y": SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT},
            {"type": "goomba", "x": 1900, "y": SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT},
            {"type": "goomba", "x": 2300, "y": SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT},
            {"type": "koopa", "x": 1300, "y": SCREEN_HEIGHT - 350},
            {"type": "koopa", "x": 2000, "y": SCREEN_HEIGHT - 350},

            {"type": "mega_piranha_plant", "x": 600, "y": SCREEN_HEIGHT - GROUND_HEIGHT - 384}
        ],
        "powerups": [

            {"type": "fire_flower", "x": 1800, "y": SCREEN_HEIGHT - 350},
        ]
    }
]
current_level = 0  # 当前关卡索引（从0开始）

# --- 设置屏幕 ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RunRunThomas")

# --- 字体 ---
font = pygame.font.Font(None, 36)
TITLE_FONT_PATH = 'assets/fonts/Rolie Twily.otf'
TITLE_FONT_SIZE = 72  # 较大的字体大小
title_font = pygame.font.Font(TITLE_FONT_PATH, TITLE_FONT_SIZE)

# 字体设置 (用于显示计时器)
pygame.font.init() # 确保 Pygame 字体模块已初始化
font_path = "assets/fonts/Rolie Twily.otf" # 假设你有一个字体文件
# 如果没有，可以使用系统默认字体：pygame.font.SysFont('Arial', 24)
try:
    timer_font = pygame.font.Font(font_path, 50) # 字体文件和大小
except FileNotFoundError:
    print(f"Warning: Font file not found at {font_path}. Using default font.")
    timer_font = pygame.font.SysFont('Arial', 60) # 备用字体
timer_text_color = (255, 255, 255) # 白色

# 背景音乐加载
# 假设你的背景音乐文件在 'assets/sounds/' 文件夹下
BGM_PATH = 'assets/sounds/game_bgm.mp3' # 或 .ogg

# 加载音乐文件
pygame.mixer.music.load(BGM_PATH)


# --- 图片加载 ---
IMAGE_DIR = "images"
mario_images = {"stand": None, "walk": [None, None], "jump": None}
koopa_images = {"fly1": None, "fly2": None, "shell": None, "dead": None}
boss_images = {"fly1": None, "fly2": None}
goomba_image = None
goomba_dead_image = None
fireball_images = [None, None]
explosion_image = None
ground_image = None
menu_background_image = None
fire_flower_image = None
ice_flower_image = None

boss_images["fly1"] = pygame.transform.scale(
        pygame.image.load(os.path.join(IMAGE_DIR, "boss1.png")).convert_alpha(),
        (120, 120)
    )
boss_images["fly2"] = pygame.transform.scale(
        pygame.image.load(os.path.join(IMAGE_DIR, "boss2.png")).convert_alpha(),
        (120, 120)
    )

boss_bullet_image = pygame.transform.scale(
    pygame.image.load(os.path.join(IMAGE_DIR, "fireball.png")).convert_alpha(),
    (16, 16))  # 弹幕图片，16x16

try:
    mario_images["stand"] = pygame.transform.scale(
        pygame.image.load(os.path.join(IMAGE_DIR, "mario_stand-removebg-preview.png")).convert_alpha(), (MARIO_WIDTH, MARIO_HEIGHT))
    mario_images["walk"] = [
        pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DIR, "mario_walk1-removebg-preview.png")).convert_alpha(),
                               (MARIO_WIDTH, MARIO_HEIGHT)),
        pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DIR, "mario_walk2-removebg-preview.png")).convert_alpha(),
                               (MARIO_WIDTH, MARIO_HEIGHT))
    ]
    mario_images["jump"] = pygame.transform.scale(
        pygame.image.load(os.path.join(IMAGE_DIR, "mario_jump-removebg-preview.png")).convert_alpha(), (MARIO_WIDTH, MARIO_HEIGHT))

    menu_background_image = pygame.transform.scale(pygame.image.load(
        os.path.join(IMAGE_DIR, "dead-cells-launching-on-pc-and-console-next-month_rtu4.png")).convert(),
                                                   (SCREEN_WIDTH, SCREEN_HEIGHT))
    ground_image = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DIR, "ground.png")).convert(),
                                          (TILE_SIZE, TILE_SIZE))
    goomba_image = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DIR, "goomba-removebg-preview.png")).convert_alpha(),
                                          (GOOMBA_WIDTH, GOOMBA_HEIGHT))
    goomba_dead_image = pygame.transform.scale(
        pygame.image.load(os.path.join(IMAGE_DIR, "goomba_dead-removebg-preview.png")).convert_alpha(),
        (GOOMBA_WIDTH, GOOMBA_HEIGHT // 2))
    fireball_images = [
        pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DIR, "fireball.png")).convert_alpha(),
                               (FIREBALL_WIDTH, FIREBALL_HEIGHT)),
        pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DIR, "huojingling.png")).convert_alpha(),
                               (FIREBALL_WIDTH, FIREBALL_HEIGHT))
    ]
    explosion_image = pygame.transform.scale(
        pygame.image.load(os.path.join(IMAGE_DIR, "explosion-removebg-preview.png")).convert_alpha(), (64, 64))
    fire_flower_image = pygame.transform.scale(
        pygame.image.load(os.path.join(IMAGE_DIR, "huojingling.png")).convert_alpha(), (32, 32))
    ice_flower_image = pygame.transform.scale(
        pygame.image.load(os.path.join(IMAGE_DIR, "xuehua.png")).convert_alpha(), (32, 32))
    koopa_images["fly1"] = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DIR, "ufo-removebg-preview.png")).convert_alpha(),
                                                  (KOOPA_WIDTH, KOOPA_HEIGHT))
    koopa_images["fly2"] = pygame.transform.scale(
        pygame.image.load(os.path.join(IMAGE_DIR, "ufo2-removebg-preview.png")).convert_alpha(), (KOOPA_WIDTH, KOOPA_HEIGHT))
    koopa_images["shell"] = pygame.transform.scale(
        pygame.image.load(os.path.join(IMAGE_DIR, "ufo-removebg-preview.png")).convert_alpha(), (KOOPA_WIDTH, KOOPA_HEIGHT // 2))
    koopa_images["dead"] = pygame.transform.scale(
        pygame.image.load(os.path.join(IMAGE_DIR, "explosion-removebg-preview.png")).convert_alpha(), (64, 64))
    print("图片加载成功！")
except pygame.error as e:
    print(f"警告：图片加载失败：{e}。将使用纯色矩形代替。")
    if not os.path.exists(IMAGE_DIR):
        print(f"请创建 'images' 文件夹，并放入所需图片。")

# --- 全局变量 ---
enemies_total_count = 0
player_score = 0
mario_lives = 3
game_state = GAME_STATE_MENU
game_win = False
game_over = False
achievements = {
    "FIRST_GOOMBA_KILL": {"name": "First Blood", "unlocked": False, "description": "Kill one Goomba"},
    "ALL_ENEMIES_CLEARED": {"name": "Scavenger", "unlocked": False, "description": "Kill all enemies"},
    "KOOPA_KILLER": {"name": "Hunter", "unlocked": False, "description": "Kill Koopa"},
    "BOSS_SLAYER": {"name": "Boss Slayer", "unlocked": False, "description": "Defeat the Boss Enemy"}
}

boss_group = pygame.sprite.Group()

# --- 摄像机类 ---
class Camera:
    def __init__(self, width, height):  # 修正：添加 width 和 height 参数
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.lerp_factor = 0.2  # 平滑因子，快速跟随

    def apply(self, entity):
        return entity.rect.move(-self.camera.x, 0)  # 只在X轴移动，Y轴固定

    def update(self, target):
        # 计算目标X位置，使玛丽奥在屏幕中央
        target_x = target.rect.centerx - (SCREEN_WIDTH // 2)
        # 限制摄像机边界：0 到 map_width - SCREEN_WIDTH
        target_camera_x = max(0, min(self.width - SCREEN_WIDTH, target_x))
        # 平滑过渡
        self.camera.x += (target_camera_x - self.camera.x) * self.lerp_factor
        # 确保最终位置在边界内
        self.camera.x = max(0, min(self.width - SCREEN_WIDTH, self.camera.x))

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 165, 0))  # 橙黄色，火焰色
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = 30  # 存活30帧（0.5秒，FPS=60）
        self.alpha = 255  # 初始透明度

    def update(self):

        self.timer -= 1
        # 闪烁：透明度正弦变化（周期10帧）
        self.alpha = int(255 * (1 - self.timer / 30) * (0.5 + 0.5 * math.sin(self.timer * 2 * math.pi / 10)))
        self.alpha = max(0, min(255, self.alpha))  # 限制0-255
        # 缩小：大小从5到3
        self.size = max(3, 5 * self.timer / 30)
        self.image = pygame.Surface((int(self.size), int(self.size)), pygame.SRCALPHA)
        self.image.fill((255, 165, 0))
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(center=self.rect.center)  # 保持中心
        if self.timer <= 0:
            self.kill()


# --- 火球类 ---
class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, fireball_images, explosion_image):
        super().__init__()
        self.particle_timer = 0  # 控制粒子生成频率
        self.width = FIREBALL_WIDTH
        self.height = FIREBALL_HEIGHT
        self.animation_frames = []
        if fireball_images and all(fireball_images):
            for img in fireball_images:
                self.animation_frames.append(img)
        else:
            self.animation_frames.append(pygame.Surface((self.width, self.height)))
            self.animation_frames[0].fill((255, 100, 0))
            self.animation_frames.append(pygame.Surface((self.width, self.height)))
            self.animation_frames[1].fill((255, 150, 0))
        self.explosion_image = explosion_image if explosion_image else pygame.Surface((self.width, self.height))
        if not explosion_image:
            self.explosion_image.fill((255, 0, 0))
        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 8 * direction
        self.vel_y = 0
        self.GRAVITY = 0.3
        self.bounce_count = 0
        self.MAX_BOUNCES = 2
        self.alive = True
        self.animation_frame = 0
        self.animation_speed = 5
        self.explosion_timer = 0
        self.EXPLOSION_DURATION = 20

    def update(self, platforms):

        if not self.alive:
            if self.explosion_timer > 0:
                self.explosion_timer -= 1
                self.image = self.explosion_image
                if self.explosion_timer <= 0:
                    self.kill()
            return
        self.rect.x += self.speed
        self.vel_y += self.GRAVITY
        self.rect.y += self.vel_y
        on_ground = False
        # 生成粒子（每3帧）
        self.particle_timer += 1
        if self.particle_timer >= 3:
            particle_x = self.rect.centerx + random.randint(-2, 2)
            particle_y = self.rect.centery + random.randint(-2, 2)
            particle = Particle(particle_x, particle_y)
            all_sprites.add(particle)
            particles.add(particle)
            self.particle_timer = 0
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0 and self.rect.bottom <= platform.rect.top + abs(self.vel_y) + 1:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = -self.vel_y * 0.7
                    self.bounce_count += 1
                    on_ground = True
                    if self.bounce_count >= self.MAX_BOUNCES or abs(self.vel_y) < 1:
                        self.alive = False
                        self.explosion_timer = self.EXPLOSION_DURATION
                        break
                elif self.vel_y < 0 and self.rect.top >= platform.rect.bottom - abs(self.vel_y) - 1:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
                    self.alive = False
                    self.explosion_timer = self.EXPLOSION_DURATION
                    break
                elif self.rect.right > platform.rect.left and self.rect.left < platform.rect.right:
                    self.alive = False
                    self.explosion_timer = self.EXPLOSION_DURATION
                    break
        if self.rect.left < 0 or self.rect.right > MAP_WIDTH or self.rect.top > SCREEN_HEIGHT:
            self.alive = False
            self.explosion_timer = self.EXPLOSION_DURATION
        if self.alive:
            self.animation_frame = (self.animation_frame + 1) % (len(self.animation_frames) * self.animation_speed)
            self.image = self.animation_frames[self.animation_frame // self.animation_speed]




class IceBall(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.bounce_count = 0
        self.MAX_BOUNCES = 2
        self.alive = True
        self.animation_frame = 0
        self.animation_speed = 5
        self.explosion_timer = 0
        self.EXPLOSION_DURATION = 20
        self.width = 16
        self.height = 16
        self.image = pygame.transform.scale(pygame.image.load('images/xueqiu.png').convert_alpha(),
                                            (self.width, self.height))
        self.rect = self.image.get_rect(center=(x, y))

        self.vel_x = direction * 5  # 冰球速度
        self.vel_y = 0
        self.gravity = 0.03  # 冰球也会受重力影响，但可以比火球轻
        self.alive = True
        self.hit_enemy = False  # 标记是否击中敌人

        self.animation_timer = 0
        self.animation_speed = 5  # 动画速度 (如果冰球有动画)
        # 如果冰球有爆炸动画，也可以加载
        # self.explosion_images = [
        #     pygame.image.load('assets/images/ice_explosion_1.png').convert_alpha(),
        #     pygame.image.load('assets/images/ice_explosion_2.png').convert_alpha(),
        # ]
        # self.explosion_timer = 0
        # self.EXPLOSION_DURATION = 15 # 爆炸持续时间

    def update(self, platforms):
        if not self.alive:
            # 如果有爆炸动画，在这里处理
            # if self.explosion_timer > 0:
            #     self.explosion_timer -= 1
            #     # 切换爆炸动画帧
            #     self.image = self.explosion_images[self.explosion_timer // (self.EXPLOSION_DURATION // len(self.explosion_images))]
            #     if self.explosion_timer <= 0:
            #         self.kill()
            # else:
            #     self.kill() # 销毁
            return

        self.rect.x += self.vel_x
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0 and self.rect.bottom <= platform.rect.top + abs(self.vel_y) + 1:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = -self.vel_y * 0.7
                    self.bounce_count += 1
                    on_ground = True
                    if self.bounce_count >= self.MAX_BOUNCES or abs(self.vel_y) < 1:
                        self.alive = False
                        self.explosion_timer = self.EXPLOSION_DURATION
                        break
                elif self.vel_y < 0 and self.rect.top >= platform.rect.bottom - abs(self.vel_y) - 1:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
                    self.alive = False
                    self.explosion_timer = self.EXPLOSION_DURATION
                    break
                elif self.rect.right > platform.rect.left and self.rect.left < platform.rect.right:
                    self.alive = False
                    self.explosion_timer = self.EXPLOSION_DURATION
                    break
        # 动画更新 (如果冰球有行走动画)
        # self.animation_timer += 1
        # if self.animation_timer >= self.animation_speed:
        #     self.animation_timer = 0
        #     # 切换动画帧，根据方向翻转图片
        #     # self.image = self.images[current_frame_index]
        #     # if self.vel_x < 0: self.image = pygame.transform.flip(self.image, True, False)

        # 屏幕边界检查，防止飞出屏幕
        if self.rect.right < 0 or self.rect.left > MAP_WIDTH or self.rect.top > SCREEN_HEIGHT:
            self.kill()


# --- 玛丽奥类 ---
class Mario(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.show_fireball_tip = False  # <--- 新增：是否显示火球提示
        self.width = MARIO_WIDTH
        self.height = MARIO_HEIGHT
        self.image_dict = mario_images
        self.image = self.image_dict["stand"] if self.image_dict["stand"] else pygame.Surface((self.width, self.height))
        if not self.image_dict["stand"]:
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.walking = False
        self.walk_frame = 0
        self.walk_timer = 0
        self.walk_animation_speed = 5
        self.jump_count = 0
        self.max_jumps = 2
        self.lives = 3
        self.invincible = False
        self.invincible_timer = 0
        self.INVINCIBLE_DURATION = 90
        self.alive = True
        self.game_over = False
        self.has_fireball_power = False
        self.fireball_cooldown = 0
        self.FIREBALL_COOLDOWN_DURATION = 30
        self.facing_right = True

        self.has_ice_power = False  # <--- 新增：冰球能力
        self.iceball_cooldown = 0  # <--- 新增：冰球冷却时间变量
        self.ICEBALL_COOLDOWN_DURATION = 30  # <--- 新增：冰球冷却时间常数，可以与 FIREBALL_COOLDOWN_DURATION 相同或不同

        self.powerup_timer = 0  # <--- 新增：道具能力计时器（统一管理火球/冰球能力持续时间）
        self.POWERUP_DURATION = 3600  # 道具持续时间（例如：60秒 * 60帧/秒 = 3600帧）


    def update(self, platforms):
        keys = pygame.key.get_pressed()

        # Ice Ball logic (now uses K_c)
        if keys[pygame.K_c] :  # <--- CHANGED: Now checks for K_c
            if self.has_ice_power:
                # Assuming all_sprites and iceballs are globally accessible
                self.shoot_iceball(all_sprites, iceballs)

        self.rect.x += self.vel_x
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0 and self.rect.bottom <= platform.rect.top + abs(self.vel_y) + 5:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    self.jump_count = 0
                elif self.vel_y < 0 and self.rect.top >= platform.rect.bottom - abs(self.vel_y) - 1:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
        if self.rect.bottom > SCREEN_HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
            self.vel_y = 0
            if not self.on_ground:
                self.on_ground = True
                self.jump_count = 0
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > MAP_WIDTH:
            self.rect.right = MAP_WIDTH
        if self.fireball_cooldown > 0:
            self.fireball_cooldown -= 1




        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
            self.image.set_alpha(100 if self.invincible_timer % 10 < 5 else 255)
        else:
            self.image.set_alpha(255)
        if not self.on_ground:
            self.image = self.image_dict["jump"] if self.image_dict["jump"] else pygame.Surface(
                (self.width, self.height))
            if not self.image_dict["jump"]:
                self.image.fill((0, 0, 255))
        elif self.walking:
            self.walk_timer += 1
            if self.walk_timer >= self.walk_animation_speed:
                self.walk_frame = (self.walk_frame + 1) % len(self.image_dict["walk"])
                self.walk_timer = 0
            self.image = self.image_dict["walk"][self.walk_frame] if self.image_dict["walk"][
                self.walk_frame] else pygame.Surface((self.width, self.height))
            if not self.image_dict["walk"][self.walk_frame]:
                self.image.fill((255, 165, 0))
        else:
            self.image = self.image_dict["stand"] if self.image_dict["stand"] else pygame.Surface(
                (self.width, self.height))
            if not self.image_dict["stand"]:
                self.image.fill((255, 0, 0))
        if not self.facing_right and self.image:
            self.image = pygame.transform.flip(self.image, True, False)

    def shoot_fireball(self, all_sprites, fireballs_group, fireball_images, explosion_image):
        if self.has_fireball_power and self.fireball_cooldown <= 0:
            fireball_direction = 1 if self.facing_right else -1
            fireball_x = self.rect.centerx + (self.rect.width // 2) * fireball_direction
            fireball_y = self.rect.centery
            fireball = Fireball(fireball_x, fireball_y, fireball_direction, fireball_images, explosion_image)
            all_sprites.add(fireball)
            fireballs_group.add(fireball)
            self.fireball_cooldown = self.FIREBALL_COOLDOWN_DURATION

    def shoot_iceball(self, all_sprites_group, iceballs_group):
        if self.has_ice_power :
            iceball_direction = 1 if self.facing_right else -1
            iceball_x = self.rect.centerx + (self.rect.width // 2) * iceball_direction
            iceball_y = self.rect.centery
            # IceBall 类应自行加载图片
            iceball = IceBall(iceball_x, iceball_y, iceball_direction)
            all_sprites_group.add(iceball)
            iceballs_group.add(iceball)


    # --- 结束新增 ---

    def jump(self):
        if self.on_ground or self.jump_count < self.max_jumps:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
            self.jump_count += 1

    def move_left(self):
        self.vel_x = -MARIO_SPEED
        self.walking = True
        self.facing_right = False

    def move_right(self):
        self.vel_x = MARIO_SPEED
        self.walking = True
        self.facing_right = True

    def stop_move(self):
        self.vel_x = 0
        self.walking = False

    def take_damage(self):
        if not self.invincible:
            self.lives -= 1
            print(f"Mario 受到伤害！剩余生命：{self.lives}")
            if self.lives <= 0:
                self.alive = False
                self.game_over = True
            else:
                self.invincible = True
                self.invincible_timer = self.INVINCIBLE_DURATION


# --- 道具类 ---
class FireFlower(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.width = 32
        self.height = 32
        self.image = pygame.transform.scale(image, (self.width, self.height)) if image else pygame.Surface(
            (self.width, self.height))
        if not image:
            self.image.fill((255, 215, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.alive = True

    def apply_effect(self, mario):
        if self.alive:
            mario.has_fireball_power = True
            print("Mario 获得火球能力！")
            mario.show_fireball_tip = True  # <--- 激活提示显示
            self.alive = False
            self.kill()
class IceFlower(pygame.sprite.Sprite):
    def __init__(self, x, y,image):
        super().__init__()
        # 加载冰花图片
        self.image = pygame.transform.scale(pygame.image.load('images/xuehua.png').convert_alpha(), (32, 32))
        self.rect = self.image.get_rect(topleft=(x, y))

    def apply_effect(self, mario):
        mario.has_ice_power = True # 赋予马里奥冰球能力

        mario.powerup_timer = 3600 # 冰球能力持续时间 (例如 1分钟 = 60帧/秒 * 60秒)
        print("Mario gained Ice Power!")
        self.kill() # 道具使用后销毁


# --- 平台类 ---
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=None):
        super().__init__()
        self.image = pygame.Surface((width, height))
        if ground_image:
            self.image = pygame.transform.scale(ground_image, (width, height))
        else:
            self.image.fill(color if color else GROUND_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# --- Goomba 类 ---
class Goomba(pygame.sprite.Sprite):
    def __init__(self, x, y, active_image, dead_image):
        super().__init__()
        self.is_frozen = False  # <--- 新增：是否被冰冻
        self.frozen_timer = 0
        self.FROZEN_DURATION = 300  # 冰冻持续时间 (5 秒)
        self.original_image = None  # 用于存储原始图像，以便冰冻恢复
        self.width = GOOMBA_WIDTH
        self.height = GOOMBA_HEIGHT
        self.image_active = active_image
        self.image_dead = dead_image
        self.image = self.image_active if self.image_active else pygame.Surface((self.width, self.height))
        if not self.image_active:
            self.image.fill(GOOMBA_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.start_x = x
        self.walk_range = 80
        self.speed = GOOMBA_SPEED
        self.direction = 1
        self.alive = True
        self.squashed = False
        self.squash_timer = 0
        self.SQUASH_DURATION = 60
        self.vel_y = 0
        self.on_ground = False

    def update(self, platforms):
        if self.is_frozen:  # <--- 新增：如果被冰冻
            self.frozen_timer -= 1
            if self.frozen_timer <= 0:
                self.unfreeze()  # 解冻
            # 冰冻状态下不执行移动、攻击或动画
            return
        if not self.alive:
            if self.squashed:
                self.squash_timer += 1
                if self.squash_timer >= self.SQUASH_DURATION:
                    self.kill()
            return
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        self.rect.y += self.vel_y
        self.on_ground = False
        for platform in platforms:
            temp_rect = self.rect.copy()
            temp_rect.y += self.vel_y
            if temp_rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            return
        self.rect.x += self.direction * self.speed
        if self.direction == 1 and self.rect.x >= self.start_x + self.walk_range:
            self.direction = -1
        elif self.direction == -1 and self.rect.x <= self.start_x - self.walk_range:
            self.direction = 1
        if self.image_active:
            self.image = self.image_active
        else:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(GOOMBA_COLOR)

    def freeze(self):  # <--- 新增：被冰冻的方法
        if not self.is_frozen:
            self.is_frozen = True
            self.frozen_timer = self.FROZEN_DURATION
            # 保存当前图片，以便解冻后恢复
            self.original_image = self.image.copy()  # 或者保存动画帧列表
            # 切换到冰冻图片
            self.image = pygame.transform.scale(
                pygame.image.load(f'images/xueren.png').convert_alpha(),
                (self.width, self.height))
            self.vel_x = 0  # 冰冻时停止移动
            self.vel_y = 0  # 冰冻时停止下落
            self.gravity = 0  # 冰冻时不受重力影响 (变成漂浮的冰块)


    def unfreeze(self):  # <--- 新增：解冻方法
        self.is_frozen = False
        self.frozen_timer = 0
        if self.original_image:
            self.image = self.original_image  # 恢复原始图片
        # 恢复移动和重力
        self.vel_x = 1 if self.rect.x % 2 == 0 else -1  # 简单恢复移动方向
        self.gravity = 0.5  # 恢复重力


    def get_hit_by_ice_ball(self):  # <--- 新增：被冰球击中时的处理
        self.freeze()

    def push(self, direction_x):  # <--- 新增：被推动的方法 (像龟壳)
        if self.is_frozen:
            self.vel_x = direction_x * 4  # 被推动的速度
            self.vel_y = 0  # 推动时可能漂浮
            print(f"{self.enemy_type} (frozen) is being pushed!")

    def squash(self):
        global enemies_total_count, player_score, achievements
        if self.alive and not self.squashed:
            print(f"Goomba {self.rect.x, self.rect.y} 被踩扁了！")
            self.squashed = True
            self.alive = False
            self.squash_timer = 0
            enemies_total_count -= 1
            player_score += 100
            if not achievements["FIRST_GOOMBA_KILL"]["unlocked"]:
                achievements["FIRST_GOOMBA_KILL"]["unlocked"] = True
                print("成就解锁：初次击杀！")
            if self.image_dead:
                self.rect = self.image_dead.get_rect(midbottom=self.rect.midbottom)
                self.image = self.image_dead
            else:
                self.image = pygame.Surface((self.width, self.height // 2))
                self.image.fill((100, 100, 100))
                self.rect.height = self.height // 2
                self.rect.y += self.height // 2
            print(f"当前剩余可击败敌人数量: {enemies_total_count}, 当前分数: {player_score}")

    def hit_mario(self, mario):
        if self.alive and not self.squashed:
            mario.take_damage()


# --- Koopa 类 ---
class Koopa(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.is_frozen = False  # <--- 新增：是否被冰冻
        self.frozen_timer = 0
        self.FROZEN_DURATION = 300  # 冰冻持续时间 (5 秒)
        self.original_image = None  # 用于存储原始图像，以便冰冻恢复
        self.width = KOOPA_WIDTH
        self.height = KOOPA_HEIGHT
        self.images = koopa_images
        self.animation_frames = []
        if self.images.get("fly1"):
            self.animation_frames.append(self.images["fly1"])
        if self.images.get("fly2"):
            self.animation_frames.append(self.images["fly2"])
        self.image_dead = self.images.get("dead")
        if self.animation_frames:
            self.current_image = self.animation_frames[0]
        else:
            self.current_image = pygame.Surface((self.width, self.height))
            self.current_image.fill(KOOPA_COLOR)
        self.image = self.current_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.start_y = y
        self.flight_range_y = 60
        self.speed = 1.5
        self.direction = 1
        self.alive = True
        self.hit_by_fireball = False
        self.death_timer = 0
        self.DEATH_DURATION = 60
        self.animation_frame = 0
        self.animation_speed = 10

    def update(self, platforms=None):
        if self.is_frozen:  # <--- 新增：如果被冰冻
            self.frozen_timer -= 1
            if self.frozen_timer <= 0:
                self.unfreeze()  # 解冻
            # 冰冻状态下不执行移动、攻击或动画
            return
        if not self.alive:
            if self.hit_by_fireball:
                self.death_timer += 1
                if self.death_timer >= self.DEATH_DURATION:
                    self.kill()
            return
        self.rect.y += self.direction * self.speed
        if self.direction == 1 and self.rect.y >= self.start_y + self.flight_range_y:
            self.direction = -1
        elif self.direction == -1 and self.rect.y <= self.start_y - self.flight_range_y:
            self.direction = 1
        if self.alive and self.animation_frames:
            self.animation_frame = (self.animation_frame + 1)
            if self.animation_frame >= self.animation_speed * len(self.animation_frames):
                self.animation_frame = 0
            self.current_image = self.animation_frames[self.animation_frame // self.animation_speed]
            self.image = self.current_image
        elif not self.alive and self.image_dead:
            self.image = self.image_dead
        else:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(KOOPA_COLOR if self.alive else (100, 100, 100))

    def hit_mario(self, mario):
        if self.alive:
            mario.take_damage()

    def freeze(self):  # <--- 新增：被冰冻的方法
        if not self.is_frozen:
            self.is_frozen = True
            self.frozen_timer = self.FROZEN_DURATION
            # 保存当前图片，以便解冻后恢复
            self.original_image = self.image.copy()  # 或者保存动画帧列表
            # 切换到冰冻图片
            self.image = pygame.transform.scale(
                pygame.image.load(f'images/xueren.png').convert_alpha(),
                (self.width, self.height))
            self.vel_x = 0  # 冰冻时停止移动
            self.vel_y = 0  # 冰冻时停止下落
            self.gravity = 0  # 冰冻时不受重力影响 (变成漂浮的冰块)


    def unfreeze(self):  # <--- 新增：解冻方法
        self.is_frozen = False
        self.frozen_timer = 0
        if self.original_image:
            self.image = self.original_image  # 恢复原始图片
        # 恢复移动和重力
        self.vel_x = 1 if self.rect.x % 2 == 0 else -1  # 简单恢复移动方向
        self.gravity = 0.5  # 恢复重力


    def get_hit_by_ice_ball(self):  # <--- 新增：被冰球击中时的处理
        self.freeze()

    def push(self, direction_x):  # <--- 新增：被推动的方法 (像龟壳)
        if self.is_frozen:
            self.vel_x = direction_x * 4  # 被推动的速度
            self.vel_y = 0  # 推动时可能漂浮
            print(f"{self.enemy_type} (frozen) is being pushed!")

    def squash_by_fireball(self):
        global enemies_total_count, player_score, achievements
        if self.alive and not self.hit_by_fireball:
            print(f"Koopa {self.rect.x, self.rect.y} 被火球击败！")
            self.alive = False
            self.hit_by_fireball = True
            self.death_timer = 0
            enemies_total_count -= 1
            player_score += 200
            if not achievements["KOOPA_KILLER"]["unlocked"]:
                achievements["KOOPA_KILLER"]["unlocked"] = True
                print("成就解锁：飞行克星！")
            if self.image_dead:
                self.rect = self.image_dead.get_rect(midbottom=self.rect.midbottom)
                self.image = self.image_dead
            else:
                self.image = pygame.Surface((self.width, self.height))
                self.image.fill((100, 100, 100))
            print(f"当前剩余可击败敌人数量: {enemies_total_count}, 当前分数: {player_score}")
class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, image):
        super().__init__()
        self.is_frozen = False  # <--- 新增：是否被冰冻
        self.frozen_timer = 0
        self.FROZEN_DURATION = 300  # 冰冻持续时间 (5 秒)
        self.original_image = None  # 用于存储原始图像，以便冰冻恢复
        self.image = image if image else pygame.Surface((16, 16))
        if not image:
            self.image.fill((255, 100, 100))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.alive = True

    def update(self):
        if not self.alive:
            return
        self.rect.x += self.speed
        if self.rect.left < 0 or self.rect.right > MAP_WIDTH or self.rect.top > SCREEN_HEIGHT:
            self.kill()
class BossEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, images, bullet_image):
        super().__init__()
        self.is_frozen = False  # <--- 新增：是否被冰冻
        self.frozen_timer = 0
        self.FROZEN_DURATION = 300  # 冰冻持续时间 (5 秒)
        self.original_image = None  # 用于存储原始图像，以便冰冻恢复

        self.images = images  # 使用 koopa_images 的 fly1 和 fly2
        self.animation_frames = []
        if self.images.get("fly1"):
            self.animation_frames.append(self.images["fly1"])
        if self.images.get("fly2"):
            self.animation_frames.append(self.images["fly2"])
        if not self.animation_frames:
            self.animation_frames.append(pygame.Surface((self.width, self.height)))
            self.animation_frames[0].fill((200, 0, 0))  # 红色作为默认
        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.width = 48
        self.height = 64
        self.health = 3  # 三滴血
        self.alive = True
        self.speed = 1.2
        self.vel_y = 0
        self.on_ground = False
        self.animation_frame = 0
        self.animation_speed = 10
        self.bullet_timer = 0
        self.BULLET_INTERVAL = 120  # 每60帧发射弹幕
        self.bullet_image = bullet_image
        self.direction = 1  # 初始向右

    def update(self, platforms, mario, all_sprites, bullets_group):
        if self.is_frozen:  # <--- 新增：如果被冰冻
            self.frozen_timer -= 1
            if self.frozen_timer <= 0:
                self.unfreeze()  # 解冻
            # 冰冻状态下不执行移动、攻击或动画
            return
        if not self.alive:
            return
        # 重力与平台碰撞
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        self.rect.y += self.vel_y
        self.on_ground = False
        for platform in platforms:
            temp_rect = self.rect.copy()
            temp_rect.y += self.vel_y
            if temp_rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            return
        # 追踪玛丽奥
        if mario.rect.centerx > self.rect.centerx:
            self.rect.x += self.speed
            self.direction = 1
        elif mario.rect.centerx < self.rect.centerx:
            self.rect.x -= self.speed
            self.direction = -1
        # 发射弹幕
        self.bullet_timer += 1
        if self.bullet_timer >= self.BULLET_INTERVAL:
            self.bullet_timer = 0
            bullet = BossBullet(
                self.rect.centerx, self.rect.centery,
                6 if mario.rect.centerx > self.rect.centerx else -6,
                self.bullet_image
            )
            all_sprites.add(bullet)
            bullets_group.add(bullet)
        # 动画
        if self.animation_frames:
            self.animation_frame = (self.animation_frame + 1) % (len(self.animation_frames) * self.animation_speed)
            self.image = self.animation_frames[self.animation_frame // self.animation_speed]
        else:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((200, 0, 0))
        # 受伤效果：血量越低，透明度越低
        self.image.set_alpha(255 * self.health // 3)
        # 接触伤害
        if self.rect.colliderect(mario.rect) and mario.alive:
            mario.take_damage()

    def freeze(self):  # <--- 新增：被冰冻的方法
        if not self.is_frozen:
            self.is_frozen = True
            self.frozen_timer = self.FROZEN_DURATION
            # 保存当前图片，以便解冻后恢复
            self.original_image = self.image.copy()  # 或者保存动画帧列表
            # 切换到冰冻图片
            self.image = pygame.transform.scale(
                pygame.image.load(f'images/xueren.png').convert_alpha(),
                (self.width, self.height))
            self.vel_x = 0  # 冰冻时停止移动
            self.vel_y = 0  # 冰冻时停止下落
            self.gravity = 0  # 冰冻时不受重力影响 (变成漂浮的冰块)
            print(f"{self.enemy_type} is frozen!")

    def unfreeze(self):  # <--- 新增：解冻方法
        self.is_frozen = False
        self.frozen_timer = 0
        if self.original_image:
            self.image = self.original_image  # 恢复原始图片
        # 恢复移动和重力
        self.vel_x = 1 if self.rect.x % 2 == 0 else -1  # 简单恢复移动方向
        self.gravity = 0.5  # 恢复重力


    def get_hit_by_ice_ball(self):  # <--- 新增：被冰球击中时的处理
        self.freeze()

    def push(self, direction_x):  # <--- 新增：被推动的方法 (像龟壳)
        if self.is_frozen:
            self.vel_x = direction_x * 4  # 被推动的速度
            self.vel_y = 0  # 推动时可能漂浮


    def take_damage(self):
        global enemies_total_count, player_score, achievements
        if self.alive:
            self.health -= 1
            print(f"BossEnemy 受到伤害！剩余血量：{self.health}")
            if self.health <= 0:
                self.alive = False
                enemies_total_count -= 1
                player_score += 500
                if not achievements["BOSS_SLAYER"]["unlocked"]:
                    achievements["BOSS_SLAYER"]["unlocked"] = True
                    print("成就解锁：Boss 终结者！")
                self.kill()
                print(f"当前剩余可击败敌人数量: {enemies_total_count}, 当前分数: {player_score}")


class BossProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, vel_x, vel_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('images/fireball.png').convert_alpha(), (32, 32))
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.gravity = 0.2 # Boss 弹丸可以有轻微重力
        self.alive = True
        self.damage = 1 # 弹丸伤害

    def update(self, platforms):
        self.rect.x += self.vel_x
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # 碰撞平台则消失
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                self.alive = False
                # 生成爆炸粒子
                # for _ in range(5):
                #     particles.add(Particle(self.rect.centerx, self.rect.centery, (255, 100, 0)))
                break

        # 屏幕边界检查
        if self.rect.right < 0 or self.rect.left > MAP_WIDTH or \
           self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0:
            self.alive = False

        if not self.alive:
            self.kill()

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('images/spike.png').convert_alpha(), (48, 48))
        self.rect = self.image.get_rect(bottomleft=(x, y)) # 尖刺从地面冒出
        self.damage = 1
        self.lifetime = 180 # 尖刺存在时间 (3秒)

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
spikes_group = pygame.sprite.Group()
class MegaPiranhaPlant(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # 继承 Enemy 的基本属性，但可能需要调整以适应Boss的特殊性
        # Boss的尺寸可以根据你的图片来定
        super().__init__()
        self.width = 256
        self.height = 384
        self.max_health = 5
        self.health = self.max_health
        self.enemy_type = "mega_piranha_plant"
        self.alive = True

        # --- 添加动画相关的初始化属性 ---
        self.animation_frame = 0  # 当前动画帧的索引
        self.animation_timer = 0  # 用于控制动画播放速度的计时器
        self.current_animation = "idle"  # 初始动画状态

        # Boss 动画帧 (你需要准备这些图片)
        self.images = {
            "idle": [pygame.transform.scale(pygame.image.load(f'images/idle.png').convert_alpha(), (self.width, self.height)) ],
            "attack1_prepare": [pygame.transform.scale(pygame.image.load(f'images/attack1_prepare.png').convert_alpha(), (self.width, self.height)) ],
            "attack1_shoot": [pygame.transform.scale(pygame.image.load(f'images/attack1_shoot.png').convert_alpha(), (self.width, self.height)) ],
            "attack2_prepare": [pygame.transform.scale(pygame.image.load(f'images/attack2_prepare.png').convert_alpha(), (self.width, self.height)) ],
            "attack2_active": [pygame.transform.scale(pygame.image.load(f'images/attack2_shoot.png').convert_alpha(), (self.width, self.height)) ],
            "hurt": [pygame.transform.scale(pygame.image.load(f'images/boss1.png').convert_alpha(), (self.width, self.height)) ],
            "open_mouth": [pygame.transform.scale(pygame.image.load(f'images/open_mouth.png').convert_alpha(), (self.width, self.height))],
            "frozen": [pygame.transform.scale(pygame.image.load(f'images/frozen.png').convert_alpha(), (self.width, self.height))],
            "death": [pygame.transform.scale(pygame.image.load(f'images/death.png').convert_alpha(), (self.width, self.height)) ] # 死亡动画
        }
        self.current_animation = "idle"
        self.image = self.images[self.current_animation][0]
        self.rect = self.image.get_rect(topleft=(x, y))

        # Boss 状态机
        self.state = "idle" # "idle", "preparing_attack1", "attacking1", "preparing_attack2", "attacking2", "vulnerable", "hurt", "dying"
        self.state_timer = 0 # 用于控制状态持续时间

        self.move_state = "moving"  # 移动状态，可以是 "moving" 或 "idle_move"
        self.target_pos = None  # Boss 移动的目标位置 (x, y)
        self.move_speed = 2  # Boss 移动速度 (像素/帧)
        self.move_cooldown = 180  # 每次移动到目标后，等待多久再选择下一个目标 (帧数，3秒)
        self.move_cooldown_timer = self.move_cooldown

        # 攻击计时器和冷却
        self.attack_cooldown = 0
        self.ATTACK_COOLDOWN_DURATION = 120 # 攻击间隔 (2秒)
        self.VULNERABLE_DURATION = 90 # 弱点暴露时间 (1.5秒)
        self.HURT_DURATION = 60 # 受伤硬直时间 (1秒)
        self.DEATH_ANIMATION_DURATION = 120 # 死亡动画时间

        # 攻击特定参数
        self.projectile_speed = 4 # 攻击1的弹速
        self.spike_count = 5 # 攻击2的尖刺数量

        # 冰冻状态 (继承自 Enemy)
        self.is_frozen = False
        self.frozen_timer = 0
        self.FROZEN_DURATION = 15 # Boss 冰冻时间可以短一些 (3秒)
        self.original_image_state = "idle" # 记录冰冻前的动画状态

        # 碰撞体（Hitbox）调整：弱点
        # 默认碰撞体是整个矩形，但弱点可能只是矩形的一部分
        self.vulnerable_rect = None # 弱点碰撞体，只有在特定状态下才有效

        # 死亡逻辑
        self.is_dying = False

    def choose_new_target_pos(self):
        # 随机选择一个在定义区域内的目标位置
        # 注意：这里的随机位置是 Boss 的左上角，所以要考虑 Boss 的宽度和高度
        # 确保 Boss 不会移动到屏幕边缘以外
        target_x = random.randint(200, MAP_WIDTH - self.width-200)
        target_y = random.randint(BOSS_MOVE_TOP_LIMIT, BOSS_MOVE_BOTTOM_LIMIT - self.height)
        self.target_pos = (target_x, target_y)
        print(f"Boss chose new target: {self.target_pos}")
        self.move_state = "moving"  # 切换到移动状态


    def set_animation(self, anim_name):
        if self.current_animation != anim_name:
            self.current_animation = anim_name
            self.animation_frame = 0
            self.animation_timer = 0

    def update(self, platforms, mario, all_sprites_group, projectiles_group, particles_group,spikes_group):
        if not self.alive:
            if self.is_dying:
                self.state_timer -= 1
                self.animation_timer += 1
                if self.animation_timer >= 10: # 死亡动画帧速
                    self.animation_frame = (self.animation_frame + 1) % len(self.images["death"])
                    self.image = self.images["death"][self.animation_frame]
                    self.animation_timer = 0
                if self.state_timer <= 0:
                    self.kill() # 死亡动画结束后销毁
            return

        # 冰冻状态处理
        if self.is_frozen:
            self.frozen_timer -= 1
            if self.frozen_timer <= 0:
                self.unfreeze()
            # 冰冻状态下不执行其他逻辑
            self.set_animation("frozen") # 保持冰冻动画
            return

        # 受伤硬直状态
        if self.state == "hurt":
            self.state_timer -= 1
            self.set_animation("hurt")
            if self.state_timer <= 0:
                self.state = "idle" # 受伤硬直结束，回到待机
                self.attack_cooldown = self.ATTACK_COOLDOWN_DURATION // 2 # 受伤后缩短下次攻击间隔
            return

        # --- 移动逻辑 ---
        # 只有当 Boss 处于 "idle" 状态（不攻击、不受伤、不死亡）时才移动
        if self.state == "idle":
            if self.move_state == "moving":
                if self.target_pos is None:
                    # 如果没有目标，就选择一个。这通常在 Boss 刚开始移动时发生
                    self.choose_new_target_pos()

                # 计算 Boss 当前位置 (self.rect.x, self.rect.y) 到目标位置 (self.target_pos[0], self.target_pos[1]) 的向量
                # 使用 self.rect.centerx/centery 可能会更平滑，但如果目标是左上角，用 topleft 坐标更直接
                delta_x = self.target_pos[0] - self.rect.x
                delta_y = self.target_pos[1] - self.rect.y

                # 计算距离
                distance = math.sqrt(delta_x**2 + delta_y**2)

                # 判断是否已经到达目标附近
                if distance > self.move_speed: # 如果距离大于一步能移动的距离，继续移动
                    # 归一化方向向量 (将向量长度变为 1，只保留方向)
                    norm_x = delta_x / distance
                    norm_y = delta_y / distance

                    # 根据方向和速度移动 Boss
                    self.rect.x += norm_x * self.move_speed
                    self.rect.y += norm_y * self.move_speed
                    # 移动时可以播放待机动画或专门的移动动画
                    self.set_animation("idle") # 假设移动时也是 idle 动画
                else: # 已经到达或非常接近目标位置
                    self.rect.x = self.target_pos[0] # 精确设置到目标点，避免 overshoot
                    self.rect.y = self.target_pos[1]
                    self.target_pos = None # 清除目标
                    self.move_state = "idle_move" # 切换到移动冷却状态
                    self.move_cooldown_timer = self.move_cooldown # 重置冷却计时器
                    print("Boss reached target position.")

            elif self.move_state == "idle_move": # 移动冷却状态
                self.set_animation("idle") # 停在原地播放待机动画
                self.move_cooldown_timer -= 1
                if self.move_cooldown_timer <= 0:
                    self.choose_new_target_pos() # 冷却结束，选择下一个目标

        # --- 攻击状态机 (只有在空闲且攻击冷却结束时才选择攻击) ---
        # 确保只有在 Boss 不移动时才考虑攻击，或者移动时也可以攻击
        # 当前逻辑是 Boss 必须是 "idle" 状态（也就是非攻击、非受伤、非死亡）才能移动
        # 我们需要确保在 "idle" 状态下，攻击冷却优先于移动冷却触发
        if self.state == "idle" and self.attack_cooldown <= 0:
            self.choose_attack(mario) # 在非移动状态且冷却结束时选择攻击
        else: # 如果在攻击冷却中，就减少冷却时间
             self.attack_cooldown -= 1


        # 主要状态机逻辑
        if self.state == "idle":
            self.set_animation("idle")
            self.attack_cooldown -= 1
            if self.attack_cooldown <= 0:
                self.choose_attack(mario) # 选择一个攻击

        elif self.state == "preparing_attack1": # 攻击1准备 (喷吐弹丸)
            self.set_animation("attack1_prepare")
            self.state_timer -= 1
            if self.state_timer <= 0:
                self.attack1(mario, all_sprites_group, projectiles_group)
                self.state = "attacking1"
                self.state_timer = 30 # 攻击持续时间

        elif self.state == "attacking1":
            self.set_animation("attack1_shoot")
            self.state_timer -= 1
            if self.state_timer <= 0:
                self.state = "vulnerable" # 攻击后露出弱点
                self.state_timer = self.VULNERABLE_DURATION
                self.set_animation("open_mouth") # 弱点暴露动画

        elif self.state == "preparing_attack2": # 攻击2准备 (召唤尖刺)
            self.set_animation("attack2_prepare")
            self.state_timer -= 1
            if self.state_timer <= 0:
                self.attack2(all_sprites_group, platforms)
                self.state = "attacking2"
                self.state_timer = 60 # 尖刺存在时间

        elif self.state == "attacking2":
            self.set_animation("attack2_active")
            self.state_timer -= 1
            if self.state_timer <= 0:

                self.state = "vulnerable"
                self.state_timer = self.VULNERABLE_DURATION
                self.set_animation("open_mouth")

        elif self.state == "vulnerable": # 弱点暴露状态
            self.set_animation("open_mouth")
            self.state_timer -= 1
            # 更新弱点碰撞体位置 (假设弱点在嘴巴里)
            self.vulnerable_rect = pygame.Rect(self.rect.centerx - 20, self.rect.top + 50, 40, 40)
            if self.state_timer <= 0:
                self.state = "idle"
                self.attack_cooldown = self.ATTACK_COOLDOWN_DURATION
                self.vulnerable_rect = None # 弱点消失

        # 动画帧更新
        self.animation_timer += 1
        if self.animation_timer >= 10: # 动画速度
            self.animation_timer = 0
            # 确保当前动画有帧可播放
            if self.current_animation in self.images and self.images[self.current_animation]:
                self.animation_frame = (self.animation_frame + 1) % len(self.images[self.current_animation])
                self.image = self.images[self.current_animation][self.animation_frame]
            else:
                self.image = self.images["idle"][0] # 备用图像

        # Boss可能需要固定位置，不受重力影响
        # self.rect.x += self.vel_x # 如果Boss会移动
        # self.vel_y += self.gravity # 如果Boss会跳动或有重力
        # 确保Boss不会超出屏幕边界

    def choose_attack(self, mario):
        """根据策略选择下一次攻击"""
        # 可以根据马里奥的位置、Boss血量等因素决定
        choice = random.choice([1, 2, 3]) # 攻击1，攻击2，以及一个假动作/吸气攻击
        if choice == 1:
            self.state = "preparing_attack1"
            self.state_timer = 60 # 准备时间 (1秒)
        elif choice == 2:
            self.state = "preparing_attack2"
            self.state_timer = 90 # 准备时间 (1.5秒)
        elif choice == 3:
            # 可以是吸气攻击 (将马里奥拉向Boss)，或者只是一个短暂的咆哮，不发射任何东西
            # 这种攻击可以不直接造成伤害，但制造威胁或为下一次攻击做铺垫
            self.state = "preparing_attack1" # 或者新建一个 state，例如 "preparing_attack3"
            self.state_timer = 45 # 短暂准备时间
            print("Boss prepares a fakeout/roar attack!") # 实际实现可以有吸气效果
            # 攻击3的实际逻辑可以写在 attack3 方法中，或者直接在这里处理
            # 比如，如果攻击3是吸气，可以计算mario到boss的距离，并施加一个反方向的力
            delta_x = self.rect.centerx - mario.rect.centerx
            if abs(delta_x) < 200: # 在一定范围内
                mario.vel_x += 1 if delta_x > 0 else -1 # 简单示例，实际需要更精细控制

    # --- 攻击方式 1: 喷吐酸性弹丸 ---
    def attack1(self, mario, all_sprites_group, projectiles_group):
        print("Boss performs Attack 1: Spitting Projectiles!")
        # 朝向马里奥喷吐一个弹丸 (你可以创建 BossProjectile 类)
        # --- 弹幕配置 ---
        num_projectiles = 16  # 弹幕中火球的数量 (例如 8 个方向)
        base_speed = 6  # 火球的基础速度
        spread_angle_degrees = 360  # 分散角度，360 度表示全方位散射
        # 如果你想要一个更窄的扇形区域（例如向前 90 度），可以设置 spread_angle_degrees = 90
        # 并根据需要调整起始角度。

        # 计算弹丸发射位置 (从 Boss 嘴部)
        # 根据 Boss 的新高度调整 Y 坐标，使其更接近嘴巴位置
        start_x = self.rect.centerx
        start_y = self.rect.top + (self.height * 0.3)  # 大约 Boss 顶部向下 30% 的位置，作为嘴巴

        # --- 以圆形/分散模式发射弹丸 ---
        for i in range(num_projectiles):
            # 计算每个弹丸的角度 (均匀分布)
            angle = (i / num_projectiles) * spread_angle_degrees
            angle_radians = math.radians(angle)  # 转换为弧度，供数学函数使用

            # 根据角度和基础速度计算速度分量
            vel_x = base_speed * math.cos(angle_radians)
            vel_y = base_speed * math.sin(angle_radians)

            # 创建并添加 Boss 弹丸
            # 确保你的 BossProjectile 类接收 x, y, vel_x, vel_y
            boss_projectile = BossProjectile(start_x, start_y, vel_x, vel_y)
            all_sprites_group.add(boss_projectile)  # 添加到所有精灵组用于渲染
            boss_projectiles.add(boss_projectile)  # 添加到 Boss 弹丸组用于碰撞检测
            projectiles_group.add(boss_projectile)

    # --- 攻击方式 2: 召唤地面尖刺 ---
    def attack2(self, all_sprites_group, platforms):
        # 在地面随机位置生成一些尖刺
        spawn_area_left = self.rect.left - 100  # Boss 左右一定范围内
        spawn_area_right = self.rect.right + 100
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT  # 假设地面Y坐标

        # 确保生成范围在地图边界内，并防止无效范围
        left_bound = max(0, int(spawn_area_left))
        right_bound = min(MAP_WIDTH, int(spawn_area_right))
        if left_bound > right_bound:
            left_bound, right_bound = right_bound, left_bound  # 交换值，确保 left_bound <= right_bound
            print(f"Warning: Swapped spawn bounds in attack2: left={left_bound}, right={right_bound}")

        spike_positions = []
        for _ in range(self.spike_count):
            x = random.randint(left_bound, right_bound)
            spike_positions.append((x, ground_y))

        for pos_x, pos_y in spike_positions:
            spike = Spike(pos_x, pos_y)  # 创建尖刺
            all_sprites_group.add(spike)
            spikes_group.add(spike)

    # --- 攻击方式 3: (可选) 吸气或拍打 ---
    # 这里可以在 choose_attack 中选择，并根据 state 执行
    # 例如，如果 state 是 "attacking3"
    def attack3(self, mario):
         print("Boss performs Attack 3: Suction Pull!")
         # 简单的吸气效果：将马里奥拉向Boss
         pull_strength = 0.5
         if abs(self.rect.centerx - mario.rect.centerx) < 300: # 仅在范围内
             if mario.rect.centerx < self.rect.centerx:
                 mario.vel_x += pull_strength
             else:
                 mario.vel_x -= pull_strength
    #     # 可能伴随一个伤害区，如果马里奥离得太近

    def take_damage(self):
        """只有在脆弱状态下才能受到伤害"""
        if self.state == "vulnerable" and not self.is_frozen:
            self.health -= 1
            print(f"Boss hit! Health: {self.health}")
            self.state = "hurt"
            self.state_timer = self.HURT_DURATION
            self.attack_cooldown = self.ATTACK_COOLDOWN_DURATION // 2 # 受伤后重置攻击冷却
            if self.health <= 0:
                self.die()
        else:
            print("Boss is invincible!") # 非脆弱状态下免疫伤害

    def get_hit_by_ice_ball(self):
        """Boss 被冰球击中时的特殊处理"""
        if not self.is_frozen:
            self.freeze()
            self.original_image_state = self.current_animation # 记录冰冻前的动画
            self.state = "idle" # 冰冻时停止当前攻击模式

    def freeze(self):
        """冰冻 Boss"""
        if not self.is_frozen:
            self.is_frozen = True
            self.frozen_timer = self.FROZEN_DURATION
            # 保存当前图片，以便解冻后恢复
            self.original_image = self.image.copy()  # 或者保存动画帧列表
            # 切换到冰冻图片
            self.image = pygame.transform.scale(
                pygame.image.load(f'images/frozen.png').convert_alpha(),
                (self.width, self.height))
            self.vel_x = 0  # 冰冻时停止移动
            self.vel_y = 0  # 冰冻时停止下落
            self.gravity = 0  # 冰冻时不受重力影响 (变成漂浮的冰块)
            print(f"{self.enemy_type} is frozen!")


    def unfreeze(self):
        """解冻 Boss"""
        self.is_frozen = False
        self.frozen_timer = 0


        self.set_animation(self.original_image_state) # 恢复冰冻前的动画
        # Boss 解冻后可能有一个短暂的硬直或恢复动画
        self.attack_cooldown = self.ATTACK_COOLDOWN_DURATION // 4 # 解冻后立即准备攻击

    def die(self):
        global enemies_total_count, player_score
        print("Boss defeated!")
        self.alive = False
        self.is_dying = True
        self.state = "dying"
        self.state_timer = self.DEATH_ANIMATION_DURATION
        self.vel_x = 0 # 停止任何移动
        enemies_total_count -= 1  # 减少敌人计数
        player_score += 1000  # 与 BossEnemy 一致，给予 500 分
        if not achievements["BOSS_SLAYER"]["unlocked"]:
            achievements["BOSS_SLAYER"]["unlocked"] = True
            print("成就解锁：Boss 终结者！")

# --- 辅助函数 ---
def draw_text(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)


def draw_button(surface, rect, text, font, button_color, text_color):
    pygame.draw.rect(surface, button_color, rect)
    pygame.draw.rect(surface, BLACK, rect, 2)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)
    return rect


def draw_menu_screen():
    if menu_background_image:
        screen.blit(menu_background_image, (0, 0))
    else:
        screen.fill(SKY_BLUE)
    title_text = title_font.render("Run Run Thomas!", True, BLACK)  # 渲染游戏标题
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_text, title_rect)
    start_button_rect = draw_button(screen, pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50),
                                    "Start", font, (100, 200, 100), WHITE)
    achievements_button_rect = draw_button(screen,
                                           pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50),
                                           "Achievement", font, (100, 100, 200), WHITE)
    quit_button_rect = draw_button(screen, pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 90, 200, 50),
                                   "Exit", font, (200, 100, 100), WHITE)
    return start_button_rect, achievements_button_rect, quit_button_rect


def draw_achievements_screen():
    screen.fill(SKY_BLUE)
    draw_text(screen, "Achievement", font, BLACK, SCREEN_WIDTH // 2, 50)
    y_offset = 100
    for key, achievement in achievements.items():
        status = "Unlocked" if achievement["unlocked"] else "Locked"
        color = (0, 150, 0) if achievement["unlocked"] else (150, 0, 0)
        draw_text(screen, f"{achievement['name']}: {status}", font, color, SCREEN_WIDTH // 2, y_offset)
        draw_text(screen, f"  - {achievement['description']}", font, BLACK, SCREEN_WIDTH // 2, y_offset + 30)
        y_offset += 80
    back_button_rect = draw_button(screen, pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 70, 160, 40),
                                   "Return", font, (150, 150, 150), WHITE)
    return back_button_rect


def draw_game_over_screen(game_win, player_score):
    screen.fill(SKY_BLUE)
    message = f"You Win! Level: {current_level + 1} Score: {player_score} Time:{game_duration}" if game_win else f"Game Over Level: {current_level + 1} Score: {player_score}  Time:{game_duration}"
    color = (0, 150, 0) if game_win else (200, 0, 0)
    draw_text(screen, message, font, color, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
    restart_button_rect = draw_button(screen, pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50),
                                      "Restart Level", font, (100, 200, 100), WHITE)
    quit_button_rect = draw_button(screen, pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 90, 200, 50),
                                   "Exit", font, (200, 100, 100), WHITE)
    back_to_menu_button_rect = draw_button(screen,
                                           pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 160, 200, 50),
                                           "Menu", font, (150, 150, 150), WHITE)
    return restart_button_rect, quit_button_rect, back_to_menu_button_rect


def reset_game(level_index=0):
    global mario, all_sprites, enemies, platforms, fireballs, powerups, enemies_total_count, player_score, mario_lives, game_win, game_over, achievements, camera, current_level, MAP_WIDTH, particles, boss_bullets,iceballs,boss_projectiles,spikes_group

    # 设置当前关卡
    current_level = level_index
    level_data = levels[current_level]
    map_width = level_data["map_width"]
    MAP_WIDTH = level_data["map_width"]


    # 初始化精灵组
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    fireballs = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    boss_bullets = pygame.sprite.Group()
    particles = pygame.sprite.Group()
    iceballs = pygame.sprite.Group()
    boss_group = pygame.sprite.Group()
    boss_projectiles = pygame.sprite.Group()  # Boss 发射的弹丸
    spikes_group = pygame.sprite.Group()  # Boss 召唤的尖刺

    # 创建玛丽奥
    mario = Mario()
    all_sprites.add(mario)

    # 创建平台
    for plat_data in level_data["platforms"]:
        platform = Platform(
            plat_data["x"], plat_data["y"],
            plat_data["width"], plat_data["height"],
            (0, 100, 0) if plat_data["y"] < SCREEN_HEIGHT - GROUND_HEIGHT else GROUND_COLOR
        )
        platforms.add(platform)

    # 创建敌人
    killable_enemies_list = []
    for enemy_data in level_data["enemies"]:
        if enemy_data["type"] == "goomba":
            enemy = Goomba(
                enemy_data["x"], enemy_data["y"],
                goomba_image, goomba_dead_image
            )
        elif enemy_data["type"] == "koopa":
            enemy = Koopa(enemy_data["x"], enemy_data["y"])
        elif enemy_data["type"] == "boss":
            enemy = BossEnemy(
                enemy_data["x"], enemy_data["y"],
                boss_images, boss_bullet_image
            )
        elif enemy_data["type"] == "mega_piranha_plant":
            enemy = MegaPiranhaPlant(enemy_data["x"], enemy_data["y"],)
            boss_group.add(enemy)
        killable_enemies_list.append(enemy)
        enemies.add(enemy)
    all_sprites.add(enemies)

    # 创建道具
    for powerup_data in level_data["powerups"]:
        if powerup_data["type"] == "fire_flower":
            powerup = FireFlower(
                powerup_data["x"], powerup_data["y"],
                fire_flower_image
            )
            powerups.add(powerup)

        if powerup_data["type"] == "ice_flower":
            powerup = IceFlower(
                powerup_data["x"], powerup_data["y"],
                ice_flower_image
            )
            powerups.add(powerup)
    all_sprites.add(powerups)
    all_sprites.add(fireballs, boss_bullets,particles,iceballs,boss_projectiles)

    # 初始化全局变量
    enemies_total_count = len(killable_enemies_list)
    player_score = 0
    mario_lives = 3
    game_win = False
    game_over = False
    for key in achievements:
        achievements[key]["unlocked"] = False
    camera = Camera(map_width, SCREEN_HEIGHT)
    print(f"关卡 {current_level + 1} 已加载。地图宽度: {map_width}, 敌人总数: {enemies_total_count}")


# 播放背景音乐
pygame.mixer.music.play(-1) # -1 表示无限循环
pygame.mixer.music.set_volume(0.0) # 设置音量为 30%

# --- 主游戏循环 ---
clock = pygame.time.Clock()

reset_game()
running = True
start_button_rect = None
achievements_button_rect = None
quit_button_rect_menu = None
back_button_rect = None
restart_button_rect = None
back_to_menu_button_rect = None
quit_button_rect_game_over = None
if game_start_time == 0: # 确保只设置一次
    game_start_time = pygame.time.get_ticks()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == GAME_STATE_PLAYING:
                if event.key == pygame.K_LEFT:
                    mario.move_left()
                elif event.key == pygame.K_RIGHT:
                    mario.move_right()
                elif event.key == pygame.K_SPACE:
                    mario.jump()
                elif event.key == pygame.K_f:
                    mario.shoot_fireball(all_sprites, fireballs, fireball_images, explosion_image)
            elif game_state == GAME_STATE_GAME_OVER:
                if event.key == pygame.K_r:
                    reset_game()
                    game_state = GAME_STATE_PLAYING
                elif event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    game_state = GAME_STATE_MENU
            elif game_state == GAME_STATE_ACHIEVEMENTS:
                if event.key == pygame.K_ESCAPE:
                    game_state = GAME_STATE_MENU
        elif event.type == pygame.KEYUP:
            if game_state == GAME_STATE_PLAYING:
                if event.key == pygame.K_LEFT and mario.vel_x < 0:
                    mario.stop_move()
                elif event.key == pygame.K_RIGHT and mario.vel_x > 0:
                    mario.stop_move()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if game_state == GAME_STATE_MENU:
                if start_button_rect and start_button_rect.collidepoint(mouse_pos):
                    reset_game()
                    game_state = GAME_STATE_PLAYING
                elif achievements_button_rect and achievements_button_rect.collidepoint(mouse_pos):
                    game_state = GAME_STATE_ACHIEVEMENTS
                elif quit_button_rect_menu and quit_button_rect_menu.collidepoint(mouse_pos):
                    running = False
            elif game_state == GAME_STATE_GAME_OVER:
                if restart_button_rect and restart_button_rect.collidepoint(mouse_pos):
                    reset_game(current_level)  # 重启当前关卡
                    game_state = GAME_STATE_PLAYING
                elif back_to_menu_button_rect and back_to_menu_button_rect.collidepoint(mouse_pos):
                    game_state = GAME_STATE_MENU
                elif quit_button_rect_game_over and quit_button_rect_game_over.collidepoint(mouse_pos):
                    running = False
            elif game_state == GAME_STATE_ACHIEVEMENTS:
                if back_button_rect and back_button_rect.collidepoint(mouse_pos):
                    game_state = GAME_STATE_MENU

    screen.fill(SKY_BLUE)
    if game_state == GAME_STATE_PLAYING:
        if mario.alive:
            mario.update(platforms)
        camera.update(mario)

        for enemy in enemies:
            if isinstance(enemy, BossEnemy):
                enemy.update(platforms, mario, all_sprites, boss_bullets)
            else:
                if isinstance(enemy, MegaPiranhaPlant):
                    enemy.update(platforms, mario, all_sprites, boss_projectiles,particles,spikes_group)



                else:
                    enemy.update(platforms)
        fireballs.update(platforms)
        iceballs.update(platforms)  # <--- 新增：更新冰球精灵组
        boss_bullets.update()
        powerups.update()
        particles.update()
        boss_projectiles.update(platforms)  # 更新 Boss 弹丸
        spikes_group.update()  # 更新尖刺



        collided_powerups = pygame.sprite.spritecollide(mario, powerups, False)
        for powerup in collided_powerups:
            if isinstance(powerup, FireFlower) and powerup.alive:
                powerup.apply_effect(mario)
                powerup.kill()
            elif isinstance(powerup, IceFlower) and powerup.alive:
                powerup.apply_effect(mario)
                powerup.kill()

        if mario.show_fireball_tip:
            tip_message = "Power of fire ! Press F to witness"
            tip_text_surface = font.render(tip_message, True, BLACK)  # 使用通用字体渲染提示
            # 将提示放置在屏幕中央下方，不随摄像机滚动
            tip_text_rect = tip_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70))
            screen.blit(tip_text_surface, tip_text_rect)

        for fireball in fireballs:
            if not fireball.alive:
                continue
            collided_enemies = pygame.sprite.spritecollide(fireball, enemies, False)
            for enemy in collided_enemies:
                if enemy.alive:
                    if isinstance(enemy, Koopa):
                        enemy.squash_by_fireball()
                        fireball.alive = False
                        fireball.explosion_timer = fireball.EXPLOSION_DURATION
                        fireball.image = fireball.explosion_image
                    elif isinstance(enemy, Goomba):
                        enemy.squash()
                        fireball.alive = False
                        fireball.explosion_timer = fireball.EXPLOSION_DURATION
                        fireball.image = fireball.explosion_image
                    elif isinstance(enemy, BossEnemy):
                        enemy.take_damage()
                        fireball.alive = False
                        fireball.explosion_timer = fireball.EXPLOSION_DURATION
                        fireball.image = fireball.explosion_image
                    elif isinstance(enemy, MegaPiranhaPlant):

                        if not enemy.alive:
                                continue  # 如果 Boss 已经死亡，跳过

                            # 检查火球是否击中 Boss 的弱点（只有在脆弱状态下）
                            # `boss.vulnerable_rect` 只有在 Boss 处于 "vulnerable" 状态时才会被设置
                        if enemy.state == "vulnerable" and enemy.vulnerable_rect and fireball.rect.colliderect(
                                enemy.vulnerable_rect):
                            enemy.take_damage()  # Boss 受到伤害
                            fireball.kill()  # 火球击中后消失
                            print("Fireball hit Boss Weak Point!")
                            break  # 火球击中 Boss 弱点后通常就不再检查其他 Boss

        # 冰球与敌人的碰撞 <--- 新增！
        for iceball in iceballs:
            if not iceball.alive:
                continue
            for boss in boss_group:  # 遍历 Boss 组
                if not boss.alive:
                    continue  # 如果 Boss 已经死亡，跳过

                # 冰球击中未被冰冻的 Boss 时，使其进入冰冻状态
                # 注意：这里 Boss 主体碰撞即可，不需要瞄准弱点
                if not boss.is_frozen and iceball.rect.colliderect(boss.rect):
                    boss.get_hit_by_ice_ball()  # Boss 进入冰冻状态
                    iceball.kill()  # 冰球击中后消失
                    print("Ice Ball hit Boss and froze it!")
                    break  # 冰球击中 Boss 后通常就不再检查其他 Boss
            collided_enemies_with_iceball = pygame.sprite.spritecollide(iceball, enemies, False,
                                                                                pygame.sprite.collide_mask)
            for enemy in collided_enemies_with_iceball:
                if enemy.alive and not enemy.is_frozen:  # 只冰冻未被冰冻的敌人
                    enemy.get_hit_by_ice_ball()  # 敌人进入冰冻状态
                    iceball.alive = False  # 冰球击中后消失
                    # iceball.explosion_timer = iceball.EXPLOSION_DURATION # 如果有爆炸动画

                    break  # 冰球只击中一个敌人就消失
        # 遍历所有冰冻敌人，检查它们是否互相碰撞，或者被玛丽奥推动

        collided_enemies = pygame.sprite.spritecollide(mario, enemies, False)
        for bullet in boss_bullets:
            if bullet.alive and bullet.rect.colliderect(mario.rect) and mario.alive:
                mario.take_damage()
                bullet.kill()
        for enemy in collided_enemies:
            if mario.alive and enemy.alive:
                if isinstance(enemy, Goomba):
                    if mario.vel_y > 0 and mario.rect.bottom >= enemy.rect.top and mario.rect.bottom <= enemy.rect.top + 10:
                        enemy.squash()
                        mario.vel_y = JUMP_STRENGTH * 0.7
                    else:
                        enemy.hit_mario(mario)
                elif isinstance(enemy, Koopa):
                    enemy.hit_mario(mario)

        for projectile in boss_projectiles:
            # 检查弹丸是否存活，是否与 Mario 碰撞，以及 Mario 是否存活且非无敌
            if projectile.alive and projectile.rect.colliderect(mario.rect) and mario.alive and not mario.invincible:
                mario.take_damage()  # Mario 受到伤害
                projectile.kill()  # 弹丸击中 Mario 后消失
                print("Mario hit by Boss Projectile!")
        for spike in spikes_group:  # 遍历所有尖刺
            if mario.alive and not mario.invincible and mario.rect.colliderect(spike.rect):
                mario.take_damage()  # Mario 受到伤害
                # 尖刺通常不会因为击中 Mario 而消失，除非你设计成一次性陷阱
                print("Mario stepped on a Boss Spike!")




        if not mario.alive:
            game_win = False
            game_over = True
            game_state = GAME_STATE_GAME_OVER

        if enemies_total_count == 0:

            if not achievements["ALL_ENEMIES_CLEARED"]["unlocked"]:
                achievements["ALL_ENEMIES_CLEARED"]["unlocked"] = True
                print("成就解锁：清道夫！")
            # 检查是否还有下一关
            if current_level + 1 < len(levels):
                # 进入下一关
                current_level += 1
                reset_game(current_level)
                print(f"进入关卡 {current_level + 1}")
            else:
                # 所有关卡完成
                game_win = True
                game_over = True
                game_state = GAME_STATE_GAME_OVER

        current_time = pygame.time.get_ticks()
        # 计算游戏已经进行的持续时间 (秒)
        # 将毫秒转换为秒，并四舍五入或向下取整，取决于你希望的精度
        game_duration = (current_time - game_start_time) // 1000  # 向下取整到秒

        # 将秒数格式化为分钟:秒钟的字符串
        minutes = game_duration // 60
        seconds = game_duration % 60
        timer_display_text = f"Time: {minutes:02}:{seconds:02}"  # 例如: "Time: 01:35"

        # 渲染计时器文本
        timer_surface = timer_font.render(timer_display_text, True, timer_text_color)

        # 确定计时器文本显示位置
        # 通常在屏幕的左上角或右上角
        timer_rect = timer_surface.get_rect(topleft=(300, 10))  # 距离左上角 10 像素

        # 将计时器文本绘制到屏幕上
        screen.blit(timer_surface, timer_rect)

        for platform in platforms:
            screen.blit(platform.image, camera.apply(platform))
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))
        for bullet in boss_bullets:
            screen.blit(bullet.image, camera.apply(bullet))
        score_text = font.render(f"Score: {player_score}", True, BLACK)
        lives_text = font.render(f"Lives: {mario.lives}", True, BLACK)
        enemies_text = font.render(f"Enemies Left: {enemies_total_count}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))
        screen.blit(enemies_text, (10, 40))
        level_text = font.render(f"Level: {current_level + 1}", True, BLACK)
        screen.blit(level_text, (10, 70))
    elif game_state == GAME_STATE_MENU:
        start_button_rect, achievements_button_rect, quit_button_rect_menu = draw_menu_screen()
    elif game_state == GAME_STATE_ACHIEVEMENTS:
        back_button_rect = draw_achievements_screen()
    elif game_state == GAME_STATE_GAME_OVER:
        if game_win:
            mario.update(platforms)
        for platform in platforms:
            screen.blit(platform.image, camera.apply(platform))
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))
        restart_button_rect, quit_button_rect_game_over, back_to_menu_button_rect = draw_game_over_screen(game_win,
                                                                                                          player_score)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()