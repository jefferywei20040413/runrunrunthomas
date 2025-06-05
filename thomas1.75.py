import pygame
import sys
import os
import random
import math

# --- 初始化 Pygame ---
pygame.init()

# --- 游戏常量 ---

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
            {"type": "goomba", "x": 700, "y": SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT},
            {"type": "goomba", "x": 1100, "y": SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT},
            {"type": "goomba", "x": 1500, "y": SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT},
            {"type": "goomba", "x": 1900, "y": SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT},
            {"type": "goomba", "x": 2300, "y": SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT},
            {"type": "koopa", "x": 1300, "y": SCREEN_HEIGHT - 350},
            {"type": "koopa", "x": 2000, "y": SCREEN_HEIGHT - 350},
            {"type": "boss", "x": 2600, "y": SCREEN_HEIGHT - GROUND_HEIGHT - 64}  # BossEnemy
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
        self.width = 48
        self.height = 64
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
    message = f"You Win! Level: {current_level + 1} Score: {player_score}" if game_win else f"Game Over Level: {current_level + 1} Score: {player_score}"
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
    global mario, all_sprites, enemies, platforms, fireballs, powerups, enemies_total_count, player_score, mario_lives, game_win, game_over, achievements, camera, current_level, MAP_WIDTH, particles, boss_bullets,iceballs

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
    all_sprites.add(fireballs, boss_bullets,particles,iceballs)

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
pygame.mixer.music.set_volume(0.8) # 设置音量为 30%

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
                enemy.update(platforms)
        fireballs.update(platforms)
        iceballs.update(platforms)  # <--- 新增：更新冰球精灵组
        boss_bullets.update()
        powerups.update()
        particles.update()

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

        # 冰球与敌人的碰撞 <--- 新增！
        for iceball in iceballs:
            if not iceball.alive:
                continue
            collided_enemies_with_iceball = pygame.sprite.spritecollide(iceball, enemies, False,
                                                                                pygame.sprite.collide_mask)
            for enemy in collided_enemies_with_iceball:
                if enemy.alive and not enemy.is_frozen:  # 只冰冻未被冰冻的敌人
                    enemy.get_hit_by_ice_ball()  # 敌人进入冰冻状态
                    iceball.alive = False  # 冰球击中后消失
                    # iceball.explosion_timer = iceball.EXPLOSION_DURATION # 如果有爆炸动画

                    break  # 冰球只击中一个敌人就消失
        # 遍历所有冰冻敌人，检查它们是否互相碰撞，或者被玛丽奥推动
        for frozen_enemy_a in enemies:
            if frozen_enemy_a.alive and frozen_enemy_a.is_frozen:
                # 检查是否被玛丽奥推动 (像踢龟壳一样)
                # 这需要一个单独的玛丽奥踢动逻辑，或在玛丽奥的碰撞检测中实现
                # 示例：如果玛丽奥在冰冻敌人旁边按下踢动键
                # if mario.rect.colliderect(frozen_enemy_a.rect) and keys[pygame.K_LSHIFT]: # 假设左Shift是踢动键
                #    direction = 1 if mario.rect.centerx < frozen_enemy_a.rect.centerx else -1
                #    frozen_enemy_a.push(direction)

                # 冰冻敌人之间的碰撞（被推动的冰块击中另一个敌人）
                # 可以使用 spritecollideany 提高效率
                hit_others = pygame.sprite.spritecollide(frozen_enemy_a, enemies, False, pygame.sprite.collide_mask)
                for frozen_enemy_b in hit_others:
                    if frozen_enemy_a != frozen_enemy_b and frozen_enemy_a.vel_x != 0: # 确保是移动中的冰块
                        if frozen_enemy_b.alive and not frozen_enemy_b.is_frozen:
                            # 移动的冰块击中普通敌人，冰冻它
                            frozen_enemy_b.get_hit_by_ice_ball()
                            print(f"Frozen {frozen_enemy_a.enemy_type} hit and froze {frozen_enemy_b.enemy_type}!")
                        elif frozen_enemy_b.alive and frozen_enemy_b.is_frozen and frozen_enemy_b.vel_x == 0:
                            # 移动的冰块击中静止的冰块，推动静止的冰块
                            frozen_enemy_b.push(frozen_enemy_a.vel_x / abs(frozen_enemy_a.vel_x))
                            print(f"Frozen {frozen_enemy_a.enemy_type} pushed frozen {frozen_enemy_b.enemy_type}!")
                        # 移动中的冰块在击中后可能会停止或反弹
                        frozen_enemy_a.vel_x = 0 # 简单停止

                # 冰冻敌人与平台的碰撞（确保冰块不会穿透平台）
                for platform in platforms:
                    if frozen_enemy_a.rect.colliderect(platform.rect):
                        if frozen_enemy_a.vel_x > 0 and frozen_enemy_a.rect.right > platform.rect.left and frozen_enemy_a.rect.left < platform.rect.left:
                            frozen_enemy_a.rect.right = platform.rect.left
                            frozen_enemy_a.vel_x = 0 # 撞墙停止
                        elif frozen_enemy_a.vel_x < 0 and frozen_enemy_a.rect.left < platform.rect.right and frozen_enemy_a.rect.right > platform.rect.right:
                            frozen_enemy_a.rect.left = platform.rect.right
                            frozen_enemy_a.vel_x = 0 # 撞墙停止
                        # 检查是否掉落到地面
                        if frozen_enemy_a.vel_y > 0 and frozen_enemy_a.rect.bottom >= platform.rect.top:
                            frozen_enemy_a.rect.bottom = platform.rect.top
                            frozen_enemy_a.vel_y = 0
                            frozen_enemy_a.on_ground = True # 冰块可以停留在地面

                # 冰块坠落深渊的处理
                if frozen_enemy_a.rect.top > SCREEN_HEIGHT + 50: # 掉出屏幕底部
                    frozen_enemy_a.kill() # 销毁冰块
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