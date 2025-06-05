import pygame
import sys
import math  # Particle 类中用到了 math.sin

# --- 常量定义 (简化版) ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)  # 用于测试提示


# --- Particle 类 (使用你提供的代码，稍作改进确保透明度支持) ---
class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # 确保 Surface 支持透明度 (SRCALPHA)
        self.image = pygame.Surface((5, 5), pygame.SRCALPHA)
        self.image.fill(ORANGE)  # 橙黄色，火焰色
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = 60  # 存活时间改为 60 帧（1 秒）
        self.initial_timer = self.timer  # 记录初始计时器
        self.alpha = 255  # 初始透明度

    def update(self):
        self.timer -= 1

        # 确保粒子在消失前有视觉变化
        # 简单的线性淡出效果
        fade_progress = 1 - (self.timer / self.initial_timer)
        self.alpha = int(255 * (1 - fade_progress))
        self.alpha = max(0, min(255, self.alpha))  # 限制在 0-255

        # 缩小效果 (从 5 到 1)
        self.size = max(1, 5 * (self.timer / self.initial_timer))

        # 重新创建 Surface 以应用新的大小和透明度
        old_center = self.rect.center
        self.image = pygame.Surface((int(self.size), int(self.size)), pygame.SRCALPHA)
        self.image.fill(ORANGE)
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(center=old_center)

        if self.timer <= 0:
            self.kill()  # 计时器归零后，从所有精灵组中移除


# --- Pygame 初始化 ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Particle Timer Test")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)  # 用于显示提示信息

# --- 精灵组 ---
all_particles = pygame.sprite.Group()

# --- 游戏循环 ---
running = True
spawn_timer = 0  # 用于控制粒子生成频率

print("按 'S' 键生成粒子。粒子会在 1 秒后消失。")
print("观察右下角的 'Particles:' 计数，看粒子是否正确消失。")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                # 按 'S' 键在鼠标位置生成一个粒子
                mouse_x, mouse_y = pygame.mouse.get_pos()
                new_particle = Particle(mouse_x, mouse_y)
                all_particles.add(new_particle)
                print(f"新粒子生成于: ({mouse_x}, {mouse_y})")

    # --- 更新 ---
    all_particles.update()  # 调用所有粒子的 update() 方法

    # --- 绘制 ---
    screen.fill(WHITE)  # 填充背景
    all_particles.draw(screen)  # 绘制所有粒子

    # --- 显示粒子数量 (用于调试) ---
    particle_count_text = font.render(f"Particles: {len(all_particles)}", True, GREEN)
    screen.blit(particle_count_text, (SCREEN_WIDTH - particle_count_text.get_width() - 10,
                                      SCREEN_HEIGHT - particle_count_text.get_height() - 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()