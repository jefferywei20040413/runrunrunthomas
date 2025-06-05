import pygame
import sys
import os

# --- 1. 初始化 Pygame ---
pygame.init()

# --- 2. 游戏常量设置 ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60 # 帧率
# 游戏状态
GAME_STATE_MENU = 0       # 新增：主菜单界面
GAME_STATE_PLAYING = 1    # 游戏进行中
GAME_STATE_ACHIEVEMENTS = 2 # 新增：成就界面
GAME_STATE_GAME_OVER = 3  # 游戏结束界面

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235) # 天空蓝

# 角色属性
MARIO_WIDTH = 32
MARIO_HEIGHT = 48
MARIO_SPEED = 5 # 水平移动速度
JUMP_STRENGTH = -12 # 跳跃力度 (负值向上)
GRAVITY = 0.5 # 重力加速度
GOOMBA_WIDTH = 32
GOOMBA_HEIGHT = 32
GOOMBA_SPEED = 2 # Goomba 的水平移动速度
GOOMBA_COLOR = (150, 75, 0) # 棕色（备用颜色）
KOOPA_WIDTH = 40
KOOPA_HEIGHT = 50
# 全局变量：存活敌人总数 (默认为 0，在实例化敌人后更新)
enemies_total_count = 0 # <--- 新增这行
game_state = GAME_STATE_MENU # <--- 将初始状态设置为菜单
# 游戏分数和生命值
player_score = 0
mario_lives = 3 # 初始生命值
# 成就系统 (简化版)
achievements = {
    "FIRST_GOOMBA_KILL": {"name": "First Blood", "unlocked": False, "description": "Kill one Goomba"},
    "ALL_ENEMIES_CLEARED": {"name": "Scavenger", "unlocked": False, "description": "Kill all enemies"},
    "KOOPA_KILLER": { # 新增成就
        "name": "Hunter",
        "description": "Kill Koopa",
        "unlocked": False
    }
}
# 地面属性
GROUND_HEIGHT = 50 # 地面厚度
GROUND_COLOR = (139, 69, 19) # 棕色

# 通关平台属性 (新增)
EXIT_PLATFORM_X = 650
EXIT_PLATFORM_Y = SCREEN_HEIGHT - 250 # 放置在一个空中平台的高度
EXIT_PLATFORM_WIDTH = 100
EXIT_PLATFORM_HEIGHT = 20
EXIT_PLATFORM_COLOR = (0, 100, 0) # 深绿色，用于区分

# --- 3. 设置屏幕 / 窗口 ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Super Mario Clone")

# --- 4. 字体设置 (可选) ---
font = pygame.font.Font(None, 36)

# --- 5. 加载图片资源 ---
# 图片路径定义
IMAGE_DIR = os.path.join(os.path.dirname(__file__), "images") # 假设图片放在脚本同级目录的 'images' 文件夹里

# 尝试加载图片，如果失败则使用纯色矩形代替

goomba_image = None
goomba_dead_image = None
mario_images = {
    "stand": None,
    "walk": [],
    "jump": None
}

# 新增：Koopa 图片变量
koopa_images = {
    "fly1": None,
    "fly2": None, # 用于飞行动画
    "shell": None, # 缩壳状态
    "dead": None
}
ground_image = None

try:
    # 玛丽图片
    mario_images["stand"] = pygame.image.load(os.path.join(IMAGE_DIR, "mario_stand.png")).convert_alpha()
    mario_images["stand"] = pygame.transform.scale(mario_images["stand"], (MARIO_WIDTH, MARIO_HEIGHT))

    mario_images["walk"].append(pygame.image.load(os.path.join(IMAGE_DIR, "mario_walk1.png")).convert_alpha())
    mario_images["walk"].append(pygame.image.load(os.path.join(IMAGE_DIR, "mario_walk2.png")).convert_alpha())
    mario_images["walk"][0] = pygame.transform.scale(mario_images["walk"][0], (MARIO_WIDTH, MARIO_HEIGHT))
    mario_images["walk"][1] = pygame.transform.scale(mario_images["walk"][1], (MARIO_WIDTH, MARIO_HEIGHT))

    mario_images["jump"] = pygame.image.load(os.path.join(IMAGE_DIR, "mario_jump.png")).convert_alpha()
    mario_images["jump"] = pygame.transform.scale(mario_images["jump"], (MARIO_WIDTH, MARIO_HEIGHT))

    # 加载菜单背景图片
    menu_background_image = pygame.image.load(os.path.join(IMAGE_DIR, "dead-cells-launching-on-pc-and-console-next-month_rtu4.png")).convert()
    # 将背景图片缩放到屏幕大小，确保它能覆盖整个菜单界面
    menu_background_image = pygame.transform.scale(menu_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # 地面图片
    TILE_SIZE = 20
    ground_image = pygame.image.load(os.path.join(IMAGE_DIR, "ground.png")).convert()
    ground_image = pygame.transform.scale(ground_image, (TILE_SIZE, TILE_SIZE)) # 假设地面块也有个TILE_SIZE

    # Goomba 图片
    active_image = pygame.image.load(os.path.join(IMAGE_DIR, "goomba.png")).convert_alpha()
    active_image = pygame.transform.scale(active_image, (GOOMBA_WIDTH, GOOMBA_HEIGHT))

    # 可选：死亡 Goomba 图片（踩扁后的效果）
    dead_image = pygame.image.load(os.path.join(IMAGE_DIR, "goomba_dead.png")).convert_alpha()
    dead_image = pygame.transform.scale(dead_image, (GOOMBA_WIDTH, GOOMBA_HEIGHT // 2))  # 高度减半模拟踩扁

    # 火球
    fireball_image = pygame.image.load(os.path.join(IMAGE_DIR, "fireball.png")).convert_alpha()
    FIRE_FLOWER_IMAGE = pygame.image.load(os.path.join(IMAGE_DIR, "huojingling.png")).convert_alpha()  # <--- 新增

    # --- 新增：加载 Koopa 图片 ---
    # 定义 Koopa 的宽度和高度，可以在常量部分定义
    KOOPA_WIDTH = 40
    KOOPA_HEIGHT = 50

    koopa_images["fly1"] = pygame.image.load(os.path.join(IMAGE_DIR, "ufo.png")).convert_alpha()
    koopa_images["fly1"] = pygame.transform.scale(koopa_images["fly1"], (KOOPA_WIDTH, KOOPA_HEIGHT))

    koopa_images["fly2"] = pygame.image.load(os.path.join(IMAGE_DIR, "ufo2.png")).convert_alpha()
    koopa_images["fly2"] = pygame.transform.scale(koopa_images["fly2"], (KOOPA_WIDTH, KOOPA_HEIGHT))

    koopa_images["shell"] = pygame.image.load(os.path.join(IMAGE_DIR, "ufo.png")).convert_alpha()
    koopa_images["shell"] = pygame.transform.scale(koopa_images["shell"], (KOOPA_WIDTH, KOOPA_HEIGHT // 2))  # 缩壳后高度变矮

    koopa_images["dead"] = pygame.image.load(os.path.join(IMAGE_DIR, "explosion.png")).convert_alpha()
    koopa_images["dead"] = pygame.transform.scale(koopa_images["dead"], (KOOPA_WIDTH, KOOPA_HEIGHT))


    print("图片加载成功！")

    print("图片加载成功！")
except pygame.error as e:
    print(f"警告：图片加载失败：{e}。将使用纯色矩形代替。")
    # 如果图片加载失败，则使用 None 或纯色 Surface
    mario_images["stand"] = None
    mario_images["walk"] = [None, None]
    mario_images["jump"] = None
    ground_image = None
    # 确保在图片加载失败时，这些变量也被设置为 None，避免后续使用时出错
    koopa_images["fly1"] = None
    koopa_images["fly2"] = None
    koopa_images["shell"] = None
    # 确保文件夹存在，即使图片不存在
    if not os.path.exists(IMAGE_DIR):
        print(f"请在脚本同级目录创建 'images' 文件夹，并放入以下图片：mario_stand.png, mario_walk1.png, mario_walk2.png, mario_jump.png, ground.png")


# --- 6. 游戏角色类定义 ---
# --- 新增：火球类定义 ---
class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, fireball_image):
        super().__init__()
        self.width = 32 # 火球宽度 (根据你的图片调整)
        self.height = 32 # 火球高度 (根据你的图片调整)

        self.image = pygame.transform.scale(fireball_image, (self.width, self.height)) if fireball_image else pygame.Surface((self.width, self.height))
        if not fireball_image:
            self.image.fill((255, 100, 0)) # 橙色作为备用

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 8 * direction # 火球速度，根据玛丽奥方向决定
        self.vel_y = 0 # 垂直速度，用于重力
        self.GRAVITY = 0.3 # 火球的重力 (可以比玛丽奥小，实现弹跳效果)
        self.bounce_count = 0 # 弹跳次数
        self.MAX_BOUNCES = 2 # 最大弹跳次数

        self.alive = True # 火球是否存活

    def update(self, platforms):
        if not self.alive:
            self.kill() # 如果不再存活，则移除
            return

        # 水平移动
        self.rect.x += self.speed

        # 垂直移动 (应用重力)
        self.vel_y += self.GRAVITY
        self.rect.y += self.vel_y

        # 碰撞检测与平台
        on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # 从上方下落碰撞到平台
                if self.vel_y > 0 and self.rect.bottom <= platform.rect.top + abs(self.vel_y) + 1:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = -self.vel_y * 0.7 # 弹跳效果，速度衰减
                    self.bounce_count += 1
                    on_ground = True
                    # 如果弹跳次数达到上限，或者速度过小，则销毁火球
                    if self.bounce_count >= self.MAX_BOUNCES or abs(self.vel_y) < 1:
                        self.alive = False
                        break
                # 从下方跳起碰撞到平台 (撞到头)
                elif self.vel_y < 0 and self.rect.top >= platform.rect.bottom - abs(self.vel_y) - 1:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0 # 停止垂直速度，并销毁
                    self.alive = False
                    break
                # 侧面碰撞
                elif self.rect.right > platform.rect.left and self.rect.left < platform.rect.right:
                    self.alive = False # 碰到侧面也销毁
                    break

        # 边界检测 (防止飞出屏幕)
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH or self.rect.top > SCREEN_HEIGHT:
            self.alive = False
class Mario(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = MARIO_WIDTH
        self.height = MARIO_HEIGHT
        self.image_dict = mario_images # 存储所有玛丽的图片

        # 初始图片
        if self.image_dict["stand"]:
            self.image = self.image_dict["stand"]
        else: # 备用纯色矩形
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((255, 0, 0)) # 红色方块

        self.rect = self.image.get_rect()
        self.rect.x = 100 # 初始X坐标
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height # 初始Y坐标 (站在地面上)

        self.vel_x = 0 # 水平速度
        self.vel_y = 0 # 垂直速度
        self.on_ground = False # 是否在地面上

        self.walking = False
        self.walk_frame = 0
        self.walk_timer = 0
        self.walk_animation_speed = 5 # 控制行走动画的速度

        # --- 二段跳相关属性 ---
        self.jump_count = 0  # 记录当前已跳跃次数
        self.max_jumps = 2   # 允许的最大跳跃次数 (2 表示二段跳)

        # --- 玛丽奥生命值与无敌系统 ---
        self.lives = 3 # 初始生命值
        self.invincible = False # 是否处于无敌状态
        self.invincible_timer = 0 # 无敌计时器
        self.INVINCIBLE_DURATION = 90 # 无敌持续帧数 (例如 1.5 秒 @ 60 FPS)
        self.alive = True # 玛丽奥是否存活 (用于判断游戏是否结束)
        self.game_over = False # 标记游戏是否结束 (当 lives <= 0 时设置为 True)

        self.has_fireball_power = False  # 是否拥有火球能力
        self.fireball_cooldown = 0  # 火球发射冷却时间
        self.FIREBALL_COOLDOWN_DURATION = 30  # 火球冷却持续帧数 (例如 0.5 秒 @ 60 FPS)
        self.facing_right = True

    def update(self, platforms):
        # --- 1. 水平移动 ---
        self.rect.x += self.vel_x

        # --- 2. 垂直移动 (重力与跳跃) ---
        self.vel_y += GRAVITY # 施加重力
        self.rect.y += self.vel_y

        # --- 3. 碰撞检测 (与平台) ---
        # 每次更新开始时，先假设不在地面上
        # 如果后续与平台碰撞并停留在上方，则会重新设置为 True
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # 从上方下落碰撞到平台
                # +1 容错值用于确保精准触碰
                if self.vel_y > 0 and self.rect.bottom <= platform.rect.top + abs(self.vel_y) + 1:
                    self.rect.bottom = platform.rect.top # 调整位置到平台顶部
                    self.vel_y = 0 # 停止垂直速度
                    self.on_ground = True # 标记为在地面上
                    self.jump_count = 0 # 关键：落地时重置跳跃次数
                # 从下方跳起碰撞到平台 (撞到头)
                elif self.vel_y < 0 and self.rect.top >= platform.rect.bottom - abs(self.vel_y) - 1:
                    self.rect.top = platform.rect.bottom # 调整位置到平台下方
                    self.vel_y = 0 # 停止垂直速度 (模拟撞头后下落)
                    # 撞到头不重置 jump_count，因为可能还需要二段跳

        # 防止掉出屏幕底部 (如果地面是特殊平台，且地面高度需要更明确的碰撞)
        # 假设地面也是一个特殊的平台，或者这里是防范掉到最底部的逻辑
        if self.rect.bottom > SCREEN_HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
            self.vel_y = 0
            # 只有当从空中落地到游戏底部时才重置 on_ground 和 jump_count
            if not self.on_ground: # 避免重复设置
                self.on_ground = True
                self.jump_count = 0 # 关键：落地时重置跳跃次数


        # 防止跑出屏幕左右边界
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # 更新火球冷却计时器
        if self.fireball_cooldown > 0:
            self.fireball_cooldown -= 1

        # --- 新增：无敌状态计时器和闪烁效果 ---
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
            # 简单的闪烁效果：每隔几帧改变图片透明度
            if self.invincible_timer % 10 < 5: # 每10帧闪烁一次，有5帧是半透明的
                self.image.set_alpha(100) # 半透明
            else:
                self.image.set_alpha(255) # 完全不透明
        else:
            self.image.set_alpha(255) # 确保非无敌状态下是完全不透明的

        # --- 4. 动画更新 ---
        # 只有在非无敌状态，或者在无敌状态但需要显示图像时才更新动画
        if not self.on_ground:
            # 跳跃动画 (当不在地面上时)
            if self.image_dict["jump"]:
                # 在无敌闪烁期间，可能不需要切换动画，或者动画保持跳跃姿态
                self.image = self.image_dict["jump"]
            else:
                self.image.fill((0, 0, 255)) # 蓝色方块 (备用)
        elif self.walking:
            # 行走动画 (在地面上且在移动时)
            self.walk_timer += 1
            if self.walk_timer >= self.walk_animation_speed:
                self.walk_frame = (self.walk_frame + 1) % len(self.image_dict["walk"])
                self.walk_timer = 0
            if self.image_dict["walk"][self.walk_frame]:
                self.image = self.image_dict["walk"][self.walk_frame]
            else:
                self.image.fill((255, 165, 0)) # 橙色方块 (备用)
        else:
            # 站立动画 (在地面上且不移动时)
            if self.image_dict["stand"]:
                self.image = self.image_dict["stand"]
            else:
                self.image.fill((255, 0, 0)) # 红色方块 (备用)


    def shoot_fireball(self, all_sprites, fireballs_group, fireball_image):
        if self.has_fireball_power and self.fireball_cooldown <= 0:
            # 确定火球的初始位置和方向
            # 玛丽奥面向的方向决定火球方向
            fireball_direction = 1 if self.vel_x >= 0 else -1 # 如果静止或向右，火球向右；否则向左
            if self.vel_x == 0: # 如果静止，根据当前显示图片（如果有方向性）或默认向右
                # 这需要你判断玛丽奥的当前朝向，例如根据最后一次移动方向
                # 假设你有一个属性 self.facing_right
                if hasattr(self, 'facing_right'): # 检查是否有这个属性
                    fireball_direction = 1 if self.facing_right else -1
                else: # 否则默认向右
                    fireball_direction = 1

            # 火球从玛丽奥中心略偏右/左的位置发射
            fireball_x = self.rect.centerx + (self.rect.width // 2) * fireball_direction
            fireball_y = self.rect.centery

            fireball = Fireball(fireball_x, fireball_y, fireball_direction, fireball_image)
            all_sprites.add(fireball)
            fireballs_group.add(fireball)
            self.fireball_cooldown = self.FIREBALL_COOLDOWN_DURATION # 设置冷却时间



    def jump(self):
        # 只有在地面上 (self.on_ground 为 True) 或者
        # 已跳跃次数 (self.jump_count) 小于允许的最大跳跃次数 (self.max_jumps) 时才能跳跃
        if self.on_ground or self.jump_count < self.max_jumps:
            self.vel_y = JUMP_STRENGTH # 施加向上的跳跃力
            self.on_ground = False       # 离开地面状态
            self.jump_count += 1         # 增加跳跃次数
            # 播放跳跃音效 (如果你的游戏有)

    def move_left(self):
        self.vel_x = -MARIO_SPEED
        self.walking = True
        self.facing_right = False  # 玛丽奥面向左

    def move_right(self):
        self.vel_x = MARIO_SPEED
        self.walking = True
        self.facing_right = True  # 玛丽奥面向右

    def stop_move(self):
        self.vel_x = 0
        self.walking = False

    def take_damage(self):
        # 只有不在无敌状态时才受伤害
        if not self.invincible:
            self.lives -= 1
            print(f"Mario 受到伤害！剩余生命：{self.lives}")
            if self.lives <= 0:
                self.alive = False # 玛丽奥死亡
                self.game_over = True # 标记游戏结束
                # 播放死亡音效或动画
            else:
                self.invincible = True
                self.invincible_timer = self.INVINCIBLE_DURATION
                # 播放受伤音效
# --- 道具类定义  ---
class FireFlower(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.width = 32 # 道具宽度
        self.height = 32 # 道具高度
        self.image = pygame.transform.scale(image, (self.width, self.height)) if image else pygame.Surface((self.width, self.height))
        if not image:
            self.image.fill((255, 0, 0)) # 红色作为备用

        self.rect = self.image.get_rect(topleft=(x, y))
        self.alive = True # 是否存在

    def update(self):
        # 道具通常不需要复杂的更新逻辑，除非它们会移动或有动画
        pass

    def apply_effect(self, mario):
        if self.alive:
            mario.has_fireball_power = True
            print("Mario 获得火球能力！")
            self.alive = False # 道具被吃掉，设置为不存活
            # 播放道具音效
            # pygame.mixer.Sound("assets/sounds/powerup.wav").play()

# --- 7. 平台类定义 (用于地面和更高层的平台) ---
class Platform(pygame.sprite.Sprite):
    # 确保 'color' 和 'is_exit_platform' 参数出现在 __init__ 的参数列表中
    def __init__(self, x, y, width, height, color=None, is_exit_platform=False):  # <--- 这一行是关键
        super().__init__()

        self.image = pygame.Surface((width, height))  # 先创建一个空白的 Surface

        if is_exit_platform:  # 如果是出口平台，强制使用传入的颜色
            self.image.fill(color if color else (0, 0, 255))  # 如果没传入颜色，就用蓝色作为默认的出口颜色
        elif ground_image:  # 如果有地面图片且不是出口平台，就使用地面图片
            self.image = pygame.transform.scale(ground_image, (width, height))
        else:  # 否则，使用默认地面颜色（或传入的普通平台颜色）
            self.image.fill(color if color else GROUND_COLOR)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# --- 7. 敌人角色类定义 ---
class Goomba(pygame.sprite.Sprite):
    # 将加载好的 Goomba 图片作为参数传入构造函数
    def __init__(self, x, y, active_image, dead_image):
        super().__init__()
        self.width = GOOMBA_WIDTH
        self.height = GOOMBA_HEIGHT

        # 直接存储传入的图片变量
        self.image_active = active_image
        self.image_dead = dead_image

        # 初始图片 (使用活着的图片)
        if self.image_active:
            self.image = self.image_active
        else: # 如果图片加载失败，使用纯色矩形作为备用
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((150, 75, 0)) # 棕色 (GOOMBA_COLOR)

        self.rect = self.image.get_rect(topleft=(x, y))

        self.start_x = x
        self.walk_range = 80 # 巡逻范围
        self.speed = GOOMBA_SPEED # 移动速度
        self.direction = 1 # 1 代表向右，-1 代表向左

        self.alive = True # Goomba 是否活着
        self.squashed = False # 是否被踩扁
        self.squash_timer = 0
        self.SQUASH_DURATION = 60 # 踩扁后存在的时间 (帧数)

        self.vel_y = 0 # 垂直速度（用于重力）
        self.on_ground = False # 是否在地面上

    def update(self, platforms):
        # 如果 Goomba 已经死亡（被踩扁），只更新计时器
        if not self.alive:
            if self.squashed:
                self.squash_timer += 1
                if self.squash_timer >= self.SQUASH_DURATION:
                    self.kill() # 从所有精灵组中移除
            return # 死亡的 Goomba 不再执行移动和碰撞检测

        # 1. 应用重力
        self.vel_y += GRAVITY
        # 限制最大下落速度，防止穿透平台
        if self.vel_y > 10:
            self.vel_y = 10
        self.rect.y += self.vel_y

        # 2. 垂直碰撞检测 (与平台)
        self.on_ground = False
        for platform in platforms:
            # 创建一个临时矩形来预测垂直移动后的位置
            temp_rect = self.rect.copy()
            temp_rect.y += self.vel_y

            if temp_rect.colliderect(platform.rect):
                if self.vel_y > 0: # 如果是向下移动（下落）
                    # 敌人底部接触平台顶部
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0: # 如果是向上移动（跳起，撞到平台底部）
                    # 敌人顶部接触平台底部
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0 # 停止上升

        # 防止敌人掉出屏幕底部（"深渊"）
        if self.rect.top > SCREEN_HEIGHT:
            self.kill() # 移除敌人，因为它掉出屏幕了
            return # 已经死亡，不再执行后续代码

        # 3. 水平移动
        self.rect.x += self.direction * self.speed

        # 4. 水平边界检测 (巡逻范围)
        if self.direction == 1 and self.rect.x >= self.start_x + self.walk_range:
            self.direction = -1
        elif self.direction == -1 and self.rect.x <= self.start_x - self.walk_range:
            self.direction = 1

        # 5. 动画更新 (Goomba 只有行走姿态，被踩后切换图片)
        # 保持显示活着的图片
        if self.image_active:
            self.image = self.image_active
        else: # 备用纯色矩形
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((150, 75, 0)) # 棕色

    def squash(self):
        # 被玛丽奥踩扁的逻辑
        global enemies_total_count, player_score, achievements # 声明全局变量

        if self.alive and not self.squashed: # 确保只处理一次
            print(f"Goomba {self.rect.x, self.rect.y} 被踩扁了！")
            self.squashed = True
            self.alive = False # 逻辑上不再活动
            self.squash_timer = 0 # 重置计时器

            enemies_total_count -= 1 # 减少可击败敌人计数
            player_score += 100

            # 解锁成就：初次击杀
            if not achievements["FIRST_GOOMBA_KILL"]["unlocked"]:
                achievements["FIRST_GOOMBA_KILL"]["unlocked"] = True
                print("成就解锁：初次击杀！")

            if self.image_dead: # 切换到死亡图片
                # 调整 rect 位置，因为图片高度变矮了
                self.rect = self.image_dead.get_rect(midbottom=self.rect.midbottom)
                self.image = self.image_dead
            else: # 如果死亡图片缺失，使用灰色方块
                self.image = pygame.Surface((self.width, self.height // 2))
                self.image.fill((100, 100, 100)) # 灰色方块
                self.rect.height = self.height // 2 # 视觉上高度减半
                self.rect.y += self.height // 2 # 调整位置，使其底部保持不变

            print(f"当前剩余可击败敌人数量: {enemies_total_count}, 当前分数: {player_score}")

    def hit_mario(self, mario):
        # 玛丽奥碰到 Goomba (如果 Goomba 活着且没被踩扁)
        if self.alive and not self.squashed:
            mario.take_damage() # Goomba 会调用 mario.take_damage()

class Koopa(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = KOOPA_WIDTH
        self.height = KOOPA_HEIGHT
        self.images = koopa_images # 传入 Koopa 的图片字典
        self.animation_frames = []
        if self.images and "fly1" in self.images and self.images["fly1"]:
            self.animation_frames.append(self.images["fly1"])
        if self.images and "fly2" in self.images and self.images["fly2"]:
            self.animation_frames.append(self.images["fly2"])
        # 新增一个死亡图片，如果 Koopa 有被火球击败的动画或图片
        self.image_dead = self.images.get("dead")  # 假设图片字典里有 "dead" 键

        if self.animation_frames:
            self.current_image = self.animation_frames[0]
        else: # 备用纯色矩形
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((0, 200, 0)) # 绿色 Koopa

        self.rect = (self.current_image if self.animation_frames else self.image).get_rect(topleft=(x, y))

        self.start_y = y # Koopa 飞行巡逻的起始 Y 坐标
        self.flight_range_y = 60 # 飞行范围，从起始点上下各延伸 60 像素
        self.speed = 1.5 # 飞行速度
        self.direction = 1 # 1 for down, -1 for up (初始向下)

        self.alive = True # Koopa 逻辑上总是活着，不会被“杀死” (默认不可击败)
        self.hit_by_fireball = False  # 新增：是否被火球击中
        self.death_timer = 0
        self.DEATH_DURATION = 60  # 死亡状态持续时间，然后移除
        self.animation_frame = 0
        self.animation_speed = 10 # 动画速度控制 (决定帧切换速度)

    def update(self, platforms=None): # 飞行敌人通常不直接与平台碰撞
        if not self.alive:
            # 如果是死亡状态，更新死亡计时器
            if self.hit_by_fireball:
                self.death_timer += 1
                if self.death_timer >= self.DEATH_DURATION:
                    self.kill() # 从所有精灵组中移除
            return # 死亡的 Koopa 不再执行移动和碰撞检测

        # 1. 垂直移动
        self.rect.y += self.direction * self.speed

        # 2. 边界检测 (飞行范围)
        if self.direction == 1 and self.rect.y >= self.start_y + self.flight_range_y:
            self.direction = -1
        elif self.direction == -1 and self.rect.y <= self.start_y - self.flight_range_y:
            self.direction = 1

        # 动画更新 (飞行动画，只有活着的时候才更新飞行姿态)

        if self.alive and self.animation_frames:
            self.animation_frame = (self.animation_frame + 1)
            if self.animation_frame >= self.animation_speed * len(self.animation_frames):
                self.animation_frame = 0
            self.current_image = self.animation_frames[self.animation_frame // self.animation_speed]
            self.image = self.current_image
        elif not self.alive and self.image_dead: # 死亡时显示死亡图片
            self.image = self.image_dead
        else:
            # 如果没有动画帧，使用备用图片
            self.image.fill((0, 200, 0) if self.alive else (100, 100, 100)) # 活着绿色，死了灰色


    def hit_mario(self, mario):
        # 玛丽奥碰到 Koopa
        if self.alive:
            mario.take_damage() # 玛丽奥掉血
            # Koopa 不会被踩死，也不会被移除
            # 可以在这里添加 Koopa 暂时停止移动或反弹的逻辑
            # self.direction *= -1 # 碰到玛丽奥后反向
    # 新增：被火球击败的方法
    def squash_by_fireball(self):
        global enemies_total_count, player_score, achievements # 声明全局变量
        if self.alive and not self.hit_by_fireball: # 确保只处理一次
            print(f"Koopa {self.rect.x, self.rect.y} 被火球击败！")
            self.alive = False
            self.hit_by_fireball = True
            self.death_timer = 0

            enemies_total_count -= 1 # 减少可击败敌人计数
            player_score += 200 # 击败 Koopa 的分数

            # 解锁成就：飞行克星
            if not achievements["KOOPA_KILLER"]["unlocked"]: # 假设你有一个新成就
                achievements["KOOPA_KILLER"]["unlocked"] = True
                print("成就解锁：飞行克星！")

            if self.image_dead: # 切换到死亡图片
                # 根据死亡图片调整 rect，如果死亡图片是扁平的
                # 这里假设死亡图片也是正常大小，或者需要类似 Goomba 的调整
                self.rect = self.image_dead.get_rect(midbottom=self.rect.midbottom) # 保持底部不变
                self.image = self.image_dead
            else: # 如果死亡图片缺失，使用灰色方块
                self.image = pygame.Surface((self.width, self.height)) # 保持大小不变
                self.image.fill((100, 100, 100)) # 灰色方块
            print(f"当前剩余可击败敌人数量: {enemies_total_count}, 当前分数: {player_score}")

# --- 8. 游戏对象实例化 ---
mario = Mario()
all_sprites = pygame.sprite.Group() # 所有精灵组
all_sprites.add(mario)

platforms = pygame.sprite.Group() # 平台组
# 添加主地面
platforms.add(Platform(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
# 添加一个空中平台 (方便测试跳跃和碰撞)
platforms.add(Platform(200, SCREEN_HEIGHT - 200, 150, 20))
# 平台 2: 在右边更高一点的平台
platforms.add(Platform(400, SCREEN_HEIGHT - 280, 100, 20))

# 平台 3: 更高一点的平台，可以尝试连续跳跃
platforms.add(Platform(550, SCREEN_HEIGHT - 380, 80, 20))

# 平台 4: 靠左边的一个矮平台
platforms.add(Platform(50, SCREEN_HEIGHT - 100, 70, 20))

# 平台 5: 一个小浮空平台，可以跳上去休息
platforms.add(Platform(650, SCREEN_HEIGHT - 150, 60, 20))

# 平台 6: 另一个平台，可以作为通往更高处的跳板
platforms.add(Platform(100, SCREEN_HEIGHT - 300, 90, 20))

# --- 新增：通关平台 ---
# 实例化通关平台，并添加到 platforms 组
exit_platform = Platform(EXIT_PLATFORM_X, EXIT_PLATFORM_Y, EXIT_PLATFORM_WIDTH, EXIT_PLATFORM_HEIGHT, EXIT_PLATFORM_COLOR, is_exit_platform=True) # 关键：is_exit_platform=True
platforms.add(exit_platform)

# --- 新增精灵组 ---
fireballs = pygame.sprite.Group() # 火球组
powerups = pygame.sprite.Group() # 道具组
# 添加一个火花道具到地图上
fire_flower1 = FireFlower(300, SCREEN_HEIGHT - 350, FIRE_FLOWER_IMAGE) # 放置在某个空中平台附近
powerups.add(fire_flower1)
# 敌人组
enemies = pygame.sprite.Group()
# --- 修正 Goomba 实例化：传入图片变量 active_image 和 dead_image ---
goomba1 = Goomba(400, SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT, active_image, dead_image) # 放置在地面上
goomba2 = Goomba(250, SCREEN_HEIGHT - 180 - GOOMBA_HEIGHT, active_image, dead_image) # 假设有个平台在 SCREEN_HEIGHT - 180
goomba3 = Goomba(680, SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT, active_image, dead_image) # 添加更多敌人

enemies.add(goomba1, goomba2, goomba3) # 将所有敌人添加到组中
all_sprites.add(enemies)
all_sprites.add(fireballs) # <--- 添加火球组
all_sprites.add(powerups) # <--- 添加道具组

# --- 新增：设置敌人总数 ---
enemies_total_count = len(enemies) # <--- 新增这行
print(f"游戏开始时敌人总数: {enemies_total_count}") # 调试信息
# --- 9. 游戏主循环 ---
clock = pygame.time.Clock()
running = True

# --- 游戏状态变量 (确保在循环外初始化一次) ---
game_over = False  # <--- 将这两行移到这里
game_win = False   # <--- 将这两行移到这里

# --- 绘制文本辅助函数 ---
def draw_text(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

# --- 绘制按钮辅助函数 ---
def draw_button(surface, rect, text, font, button_color, text_color):
    pygame.draw.rect(surface, button_color, rect)
    pygame.draw.rect(surface, BLACK, rect, 2) # 边框
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)
    return rect # 返回矩形以便点击检测

# --- 游戏状态绘制函数 ---

def draw_menu_screen():
    screen.blit(menu_background_image, (0, 0))
    draw_text(screen, "RunRunThomas", font, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

    # 绘制按钮
    start_button_rect = draw_button(screen, pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50),
                                    "Start", font, (100, 200, 100), WHITE) # 绿色按钮
    achievements_button_rect = draw_button(screen, pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50),
                                           "Achievement", font, (100, 100, 200), WHITE) # 蓝色按钮
    quit_button_rect = draw_button(screen, pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 90, 200, 50),
                                   "Exit", font, (200, 100, 100), WHITE) # 红色按钮

    # 返回按钮的矩形，以便在主循环中检测点击
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
                                   "Return", font, (150, 150, 150), WHITE) # 灰色按钮
    return back_button_rect

def draw_game_over_screen(game_win, player_score):
    screen.fill(SKY_BLUE)
    message = ""
    color = BLACK
    if game_win:
        message = f"You Win Score: {player_score}"
        color = (0, 150, 0)
    else:
        message = f"Game Over Score: {player_score}"
        color = (200, 0, 0)

    draw_text(screen, message, font, color, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)

    restart_button_rect = draw_button(screen, pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50),
                                      "Again", font, (100, 200, 100), WHITE)
    quit_button_rect = draw_button(screen, pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 90, 200, 50),
                                   "Exit", font, (200, 100, 100), WHITE)


    return restart_button_rect, quit_button_rect, back_to_menu_button_rect

# --- 辅助函数：重置游戏状态 ---
# 确保这个函数在 main loop 之前定义
def reset_game():
    global mario, platforms, enemies, exit_platform, enemies_total_count, player_score, mario_lives, game_win, game_over, all_sprites, achievements, fireballs, powerups

    # 清空所有精灵组
    all_sprites.empty()
    platforms.empty()
    enemies.empty()
    fireballs.empty()  # <--- 清空火球组
    powerups.empty()  # <--- 清空道具组

    # 重置玛丽
    mario = Mario()
    all_sprites.add(mario)

    # 重置平台 (重新创建所有平台)
    platforms.add(Platform(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
    platforms.add(Platform(200, SCREEN_HEIGHT - 200, 150, 20))
    platforms.add(Platform(400, SCREEN_HEIGHT - 280, 100, 20))
    platforms.add(Platform(550, SCREEN_HEIGHT - 380, 80, 20))
    platforms.add(Platform(50, SCREEN_HEIGHT - 100, 70, 20))
    platforms.add(Platform(650, SCREEN_HEIGHT - 150, 60, 20))
    platforms.add(Platform(100, SCREEN_HEIGHT - 300, 90, 20))
    exit_platform = Platform(EXIT_PLATFORM_X, EXIT_PLATFORM_Y, EXIT_PLATFORM_WIDTH, EXIT_PLATFORM_HEIGHT, EXIT_PLATFORM_COLOR, is_exit_platform=True)
    platforms.add(exit_platform)

    # --- 关键修正：在 reset_game() 中实例化 Goomba 时也传入图片 ---
    goomba1 = Goomba(400, SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT, active_image, dead_image)
    goomba2 = Goomba(250, SCREEN_HEIGHT - 180 - GOOMBA_HEIGHT, active_image, dead_image)
    goomba3 = Goomba(680, SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT, active_image, dead_image)
    koopa1 = Koopa(500, SCREEN_HEIGHT - 350)  # 飞行 Koopa

    # 这里的 enemies.list_of_killable_enemies 和 enemies.list_of_unkillable_enemies
    # 并不是 Sprite Group 的标准属性。
    # 更好的做法是在 reset_game() 内部根据敌人类型直接构建列表，
    # 或者如果需要在 enemies Sprite Group 内部进行分类，需要自定义 Sprite Group 类。
    # 目前我们直接用列表来计算 enemies_total_count 即可。
    killable_enemies_list = [goomba1, goomba2, goomba3,koopa1]  # 只记录 Goomba


    enemies.add(*killable_enemies_list)

    fire_flower1 = FireFlower(300, SCREEN_HEIGHT - 350, FIRE_FLOWER_IMAGE)
    powerups.add(fire_flower1)
    all_sprites.add(enemies)  # 将 enemies 组添加到 all_sprites
    all_sprites.add(fireballs)
    all_sprites.add(powerups)



    # --- 关键修改：设置敌人总数只计算可击败的 Goomba ---
    enemies_total_count = len(killable_enemies_list)
    print(f"游戏开始时可击败敌人总数: {enemies_total_count}")
    player_score = 0
    mario_lives = 3
    game_win = False
    game_over = False

    # 重置成就 (可选，根据你的游戏设计决定是否重置)
    for key in achievements:
        achievements[key]["unlocked"] = False # 每次新游戏都重置成就状态

    print(f"游戏已重置。初始敌人数量: {enemies_total_count}")


# --- 游戏主循环 ---
clock = pygame.time.Clock()
running = True

# 确保在主循环开始前，这些变量在全局范围可用
start_button_rect = None
achievements_button_rect = None
quit_button_rect_menu = None # <-- 将这个变量名改为 quit_button_rect_menu
back_button_rect = None
restart_button_rect = None
back_to_menu_button_rect = None
quit_button_rect_game_over = None


while running:
    # --- 事件处理 ---
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
                elif event.key == pygame.K_f:  # 新增：按 F 键发射火球
                    mario.shoot_fireball(all_sprites, fireballs, fireball_image)
            elif game_state == GAME_STATE_GAME_OVER:
                if event.key == pygame.K_r: # 按 R 键再来一局
                    reset_game()
                    game_state = GAME_STATE_PLAYING
                elif event.key == pygame.K_q: # 按 Q 键退出游戏
                    running = False
                elif event.key == pygame.K_ESCAPE: # 按 ESC 键返回主界面
                    game_state = GAME_STATE_MENU
            elif game_state == GAME_STATE_ACHIEVEMENTS:
                if event.key == pygame.K_ESCAPE: # 按 ESC 返回菜单
                    game_state = GAME_STATE_MENU

        elif event.type == pygame.KEYUP:
            if game_state == GAME_STATE_PLAYING:
                if event.key == pygame.K_LEFT and mario.vel_x < 0:
                    mario.stop_move()
                elif event.key == pygame.K_RIGHT and mario.vel_x > 0:
                    mario.stop_move()

        # 处理鼠标点击事件
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # 左键点击
                mouse_pos = event.pos

                if game_state == GAME_STATE_MENU:
                    # 确保按钮在检测点击前已经被绘制并返回了它们的 rect
                    # draw_menu_screen() 在此循环的下一部分被调用，所以我们依赖其返回值
                    if start_button_rect and start_button_rect.collidepoint(mouse_pos):
                        reset_game() # 开始新游戏前重置状态
                        game_state = GAME_STATE_PLAYING
                    elif achievements_button_rect and achievements_button_rect.collidepoint(mouse_pos):
                        game_state = GAME_STATE_ACHIEVEMENTS
                    elif quit_button_rect_menu and quit_button_rect_menu.collidepoint(mouse_pos):
                        running = False
                elif game_state == GAME_STATE_GAME_OVER:
                    # 确保按钮在检测点击前已经被绘制并返回了它们的 rect
                    if restart_button_rect and restart_button_rect.collidepoint(mouse_pos):
                        reset_game()
                        game_state = GAME_STATE_PLAYING
                    elif back_to_menu_button_rect and back_to_menu_button_rect.collidepoint(mouse_pos):
                        game_state = GAME_STATE_MENU
                    elif quit_button_rect_game_over and quit_button_rect_game_over.collidepoint(mouse_pos):
                        running = False
                elif game_state == GAME_STATE_ACHIEVEMENTS:
                    # 确保按钮在检测点击前已经被绘制并返回了它们的 rect
                    if back_button_rect and back_button_rect.collidepoint(mouse_pos):
                        game_state = GAME_STATE_MENU

    # --- 游戏状态逻辑分支 (更新和绘制) ---
    screen.fill(SKY_BLUE) # 每次循环开始时清空屏幕

    if game_state == GAME_STATE_PLAYING:
        enemies_text = font.render(f"Enemies Left: {enemies_total_count}", True, BLACK)
        screen.blit(enemies_text, (10, 40))


        # 游戏进行中，更新所有精灵和处理碰撞
        # 只有玛丽奥活着时才更新他的位置，否则保持死亡动画

        if mario.alive: # 判断玛丽奥是否存活
            mario.update(platforms)
        # 敌人始终更新，因为它们可能继续移动或执行死亡动画
        enemies.update(platforms) # 确保 enemies 组也传递 platforms 参数
        collided_powerups = pygame.sprite.spritecollide(mario, powerups, False)
        for powerup in collided_powerups:
            if isinstance(powerup, FireFlower) and powerup.alive:
                powerup.apply_effect(mario)  # 触发火花效果
                powerup.kill()  # 从精灵组中移除道具
        # 更新火球
        fireballs.update(platforms)

        # 新增：火球与敌人的碰撞检测
        for fireball in fireballs:
            if not fireball.alive:
                continue  # 跳过已销毁的火球
            collided_enemies = pygame.sprite.spritecollide(fireball, enemies, False)
            for enemy in collided_enemies:
                if enemy.alive:
                    if isinstance(enemy, Koopa):
                        enemy.squash_by_fireball()  # 火球击败 Koopa
                        fireball.alive = False  # 火球击中后销毁
                        fireball.kill()
                    elif isinstance(enemy, Goomba):
                        enemy.squash()  # 火球也可以击败 Goomba
                        fireball.alive = False
                        fireball.kill()

        # 玛丽奥与敌人的碰撞检测
        collided_enemies = pygame.sprite.spritecollide(mario, enemies, False) # 不自动移除，因为有些敌人可能不会被 kill
        for enemy in collided_enemies:
            # 只有当玛丽奥活着且敌人也活着时才处理碰撞
            if mario.alive and enemy.alive:
                if isinstance(enemy, Goomba): # 如果是 Goomba
                    # 检查是否从上方踩踏 (玛丽奥下降且底部在敌人顶部附近)
                    # mario.vel_y > 0 表示正在下落
                    # mario.rect.bottom >= enemy.rect.top 表示玛丽奥底部达到或超过敌人顶部
                    # mario.rect.bottom <= enemy.rect.top + 10 表示玛丽奥底部在敌人顶部10像素范围内 (容错值)
                    if mario.vel_y > 0 and mario.rect.bottom >= enemy.rect.top and mario.rect.bottom <= enemy.rect.top + 10:
                        enemy.squash() # 踩扁 Goomba，Goomba 内部会处理 alive = False 和 kill()
                        mario.vel_y = JUMP_STRENGTH * 0.7 # 玛丽奥反弹一下 (跳跃力度降低)
                    else:
                        # 玛丽奥被 Goomba 碰到 (非踩踏，例如侧面碰撞)
                        enemy.hit_mario(mario) # Goomba 会调用 mario.take_damage()
                elif isinstance(enemy, Koopa): # 如果是 Koopa
                    # Koopa 不能被踩死，玛丽奥碰到 Koopa 只会掉血
                    enemy.hit_mario(mario) # Koopa 会调用 mario.take_damage()


        # --- 游戏胜利/失败条件判断 ---
        # 确保 enemies_total_count 在 Goomba 被踩扁后立即减少
        all_enemies_defeated = (enemies_total_count == 0)
        on_exit_platform = False
        mario_rect = mario.rect
        exit_platform_rect = exit_platform.rect
        # 精确的脚部碰撞检测：创建一个玛丽奥脚部的小矩形
        mario_feet_rect = pygame.Rect(mario_rect.x, mario_rect.bottom - 5, mario_rect.width, 5) # 调整为玛丽奥底部5像素高

        if mario_feet_rect.colliderect(exit_platform_rect):
            # 确保玛丽奥是“站在”出口平台上的，而不是从侧面或下面碰到
            # mario.rect.bottom <= exit_platform_rect.top + 5: 玛丽奥底部在平台顶部5像素以内
            # mario.vel_y >= 0: 玛丽奥在静止或下落，表示可能“踩”在平台上
            if mario.rect.bottom <= exit_platform_rect.top + 5 and mario.vel_y >= 0:
                on_exit_platform = True


        # 游戏失败条件：玛丽奥生命值耗尽
        if not mario.alive: # mario.alive 为 False 说明生命值 <= 0
            game_win = False
            game_over = True
            game_state = GAME_STATE_GAME_OVER

        # 游戏胜利条件：所有可击败敌人被清除 且 玛丽奥站在出口平台
        #and on_exit_platform
        if all_enemies_defeated :
            game_win = True
            game_over = True
            game_state = GAME_STATE_GAME_OVER
            if not achievements["ALL_ENEMIES_CLEARED"]["unlocked"]:
                achievements["ALL_ENEMIES_CLEARED"]["unlocked"] = True
                print("成就解锁：清道夫！")

        # 绘制游戏元素
        platforms.draw(screen)
        all_sprites.draw(screen) # all_sprites 组包含 Mario 和所有 enemies

        # 绘制 UI (分数和生命值)
        score_text = font.render(f"Score: {player_score}", True, BLACK)
        lives_text = font.render(f"Lives: {mario.lives}", True, BLACK) # 从 mario 对象获取生命值
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))

    elif game_state == GAME_STATE_MENU:
        # 绘制主菜单，并获取按钮矩形，这些 rect 会在下一个鼠标事件循环中被使用
        start_button_rect, achievements_button_rect, quit_button_rect_menu = draw_menu_screen()

    elif game_state == GAME_STATE_ACHIEVEMENTS:
        # 绘制成就界面，并获取返回按钮矩形
        back_button_rect = draw_achievements_screen()

    elif game_state == GAME_STATE_GAME_OVER:
        # 绘制游戏结束界面，并获取按钮矩形
        # 这里需要确保 back_to_menu_button_rect 被定义，否则鼠标点击时可能出错
        restart_button_rect, quit_button_rect_game_over, back_to_menu_button_rect = draw_game_over_screen(game_win, player_score)


    # --- 更新屏幕显示 ---
    pygame.display.flip()

    # --- 控制帧率 ---
    clock.tick(FPS)

# --- 10. 退出 Pygame ---
pygame.quit()
sys.exit()