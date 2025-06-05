import pygame
import sys
import os

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

# --- 设置屏幕 ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RunRunThomas")

# --- 字体 ---
font = pygame.font.Font(None, 36)
TITLE_FONT_PATH = 'assets/fonts/Rolie Twily.otf'
TITLE_FONT_SIZE = 72  # 较大的字体大小
title_font = pygame.font.Font(TITLE_FONT_PATH, TITLE_FONT_SIZE)

# --- 图片加载 ---
IMAGE_DIR = "images"
mario_images = {"stand": None, "walk": [None, None], "jump": None, "victory": [None, None]}
koopa_images = {"fly1": None, "fly2": None, "shell": None, "dead": None}
goomba_image = None
goomba_dead_image = None
fireball_images = [None, None]
explosion_image = None
ground_image = None
menu_background_image = None
fire_flower_image = None

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
    mario_images["victory"] = [
        pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DIR, "mario_victory1.png")).convert_alpha(),
                               (MARIO_WIDTH, MARIO_HEIGHT)),
        pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DIR, "mario_victory1.png")).convert_alpha(),
                               (MARIO_WIDTH, MARIO_HEIGHT))
    ]
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
        pygame.image.load(os.path.join(IMAGE_DIR, "explosion-removebg-preview.png")).convert_alpha(), (FIREBALL_WIDTH, FIREBALL_HEIGHT))
    fire_flower_image = pygame.transform.scale(
        pygame.image.load(os.path.join(IMAGE_DIR, "huojingling.png")).convert_alpha(), (32, 32))
    koopa_images["fly1"] = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DIR, "ufo-removebg-preview.png")).convert_alpha(),
                                                  (KOOPA_WIDTH, KOOPA_HEIGHT))
    koopa_images["fly2"] = pygame.transform.scale(
        pygame.image.load(os.path.join(IMAGE_DIR, "ufo2-removebg-preview.png")).convert_alpha(), (KOOPA_WIDTH, KOOPA_HEIGHT))
    koopa_images["shell"] = pygame.transform.scale(
        pygame.image.load(os.path.join(IMAGE_DIR, "ufo-removebg-preview.png")).convert_alpha(), (KOOPA_WIDTH, KOOPA_HEIGHT // 2))
    koopa_images["dead"] = pygame.transform.scale(
        pygame.image.load(os.path.join(IMAGE_DIR, "explosion-removebg-preview.png")).convert_alpha(), (KOOPA_WIDTH, KOOPA_HEIGHT))
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
    "KOOPA_KILLER": {"name": "Hunter", "unlocked": False, "description": "Kill Koopa"}
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
        # 计算摄像机的目标X坐标（负值，向右移动显示地图右边）
        target_camera_x = target_x
        # 限制摄像机边界：左端 camera.x=0，右端 camera.x=-(MAP_WIDTH-SCREEN_WIDTH)
        target_camera_x = min(self.width - SCREEN_WIDTH, max(0, target_camera_x))
        # 平滑过渡到目标位置
        self.camera.x += (target_camera_x - self.camera.x) * self.lerp_factor
        # 确保最终位置在边界内

        target_camera_x = min(self.width - SCREEN_WIDTH, max(0, target_camera_x))


# --- 火球类 ---
class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, fireball_images, explosion_image):
        super().__init__()
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
        self.victory = False
        self.victory_frame = 0
        self.victory_timer = 0
        self.victory_animation_speed = 10

    def update(self, platforms):
        if self.victory:
            self.victory_timer += 1
            if self.victory_timer >= self.victory_animation_speed:
                self.victory_frame = (self.victory_frame + 1) % len(self.image_dict["victory"])
                self.victory_timer = 0
            self.image = self.image_dict["victory"][self.victory_frame] if self.image_dict["victory"][
                self.victory_frame] else pygame.Surface((self.width, self.height))
            if not self.image_dict["victory"][self.victory_frame]:
                self.image.fill((0, 255, 255))
            return
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
    message = f"You Win Score: {player_score}" if game_win else f"Game Over Score: {player_score}"
    color = (0, 150, 0) if game_win else (200, 0, 0)
    draw_text(screen, message, font, color, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
    restart_button_rect = draw_button(screen, pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50),
                                      "Again", font, (100, 200, 100), WHITE)
    quit_button_rect = draw_button(screen, pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 90, 200, 50),
                                   "Exit", font, (200, 100, 100), WHITE)
    back_to_menu_button_rect = draw_button(screen,
                                           pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 160, 200, 50),
                                           "Menu", font, (150, 150, 150), WHITE)
    return restart_button_rect, quit_button_rect, back_to_menu_button_rect


# --- 重置游戏 ---
def reset_game():
    global mario, all_sprites, enemies, platforms, fireballs, powerups, enemies_total_count, player_score, mario_lives, game_win, game_over, achievements, camera
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    fireballs = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    mario = Mario()
    all_sprites.add(mario)
    platforms_list = [
        Platform(0, SCREEN_HEIGHT - GROUND_HEIGHT, MAP_WIDTH, GROUND_HEIGHT, GROUND_COLOR),
        Platform(200, SCREEN_HEIGHT - 200, 150, 20, (0, 100, 0)),
        Platform(400, SCREEN_HEIGHT - 300, 150, 20, (0, 100, 0)),
        Platform(600, SCREEN_HEIGHT - 250, 150, 20, (0, 100, 0)),
        Platform(900, SCREEN_HEIGHT - 350, 150, 20, (0, 100, 0)),
        Platform(1200, SCREEN_HEIGHT - 200, 150, 20, (0, 100, 0)),
        Platform(1500, SCREEN_HEIGHT - 300, 150, 20, (0, 100, 0)),
        Platform(1800, SCREEN_HEIGHT - 250, 150, 20, (0, 100, 0)),
        Platform(2100, SCREEN_HEIGHT - 350, 150, 20, (0, 100, 0)),
    ]
    for platform in platforms_list:
        platforms.add(platform)
    goomba1 = Goomba(300, SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT, goomba_image, goomba_dead_image)
    goomba2 = Goomba(700, SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT, goomba_image, goomba_dead_image)
    goomba3 = Goomba(1000, SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT, goomba_image, goomba_dead_image)
    goomba4 = Goomba(1400, SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT, goomba_image, goomba_dead_image)
    goomba5 = Goomba(2000, SCREEN_HEIGHT - GROUND_HEIGHT - GOOMBA_HEIGHT, goomba_image, goomba_dead_image)
    koopa1 = Koopa(1200, SCREEN_HEIGHT - 350)
    koopa2 = Koopa(1800, SCREEN_HEIGHT - 350)
    killable_enemies_list = [goomba1, goomba2, goomba3, goomba4, goomba5, koopa1, koopa2]
    enemies.add(*killable_enemies_list)
    all_sprites.add(enemies)
    fire_flower = FireFlower(300, SCREEN_HEIGHT - 350, fire_flower_image)
    powerups.add(fire_flower)
    all_sprites.add(powerups)
    all_sprites.add(fireballs)
    enemies_total_count = len(killable_enemies_list)
    player_score = 0
    mario_lives = 3
    game_win = False
    game_over = False
    for key in achievements:
        achievements[key]["unlocked"] = False
    camera = Camera(MAP_WIDTH, SCREEN_HEIGHT)
    print(f"游戏已重置。敌人总数: {enemies_total_count}")


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
                    reset_game()
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
        enemies.update(platforms)
        fireballs.update(platforms)
        powerups.update()
        collided_powerups = pygame.sprite.spritecollide(mario, powerups, False)
        for powerup in collided_powerups:
            if isinstance(powerup, FireFlower) and powerup.alive:
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
        collided_enemies = pygame.sprite.spritecollide(mario, enemies, False)
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
            game_win = True
            game_over = True
            game_state = GAME_STATE_GAME_OVER
            mario.victory = True
            if not achievements["ALL_ENEMIES_CLEARED"]["unlocked"]:
                achievements["ALL_ENEMIES_CLEARED"]["unlocked"] = True
                print("成就解锁：清道夫！")
        for platform in platforms:
            screen.blit(platform.image, camera.apply(platform))
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))
        score_text = font.render(f"Score: {player_score}", True, BLACK)
        lives_text = font.render(f"Lives: {mario.lives}", True, BLACK)
        enemies_text = font.render(f"Enemies Left: {enemies_total_count}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))
        screen.blit(enemies_text, (10, 40))
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