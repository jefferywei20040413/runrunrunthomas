import pygame
import random
import sys

# --- 1. 初始化 Pygame ---
pygame.init()

# --- 2. 游戏常量设置 ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BOARD_SIZE = 12 # 游戏板格子数量

TILE_SIZE = 80 # 每个格子的大小
PLAYER_SIZE = 30 # 玩家棋子大小



# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0) # 游戏板背景色
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

# 字体设置
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# --- 3. 游戏板格子定义 ---
# 每个格子是一个字典，包含类型、名称、位置、属性拥有者等
# 简化版，位置将在布局时动态计算
BOARD = []

# 定义格子类型常量
TILE_TYPE_START = "START"
TILE_TYPE_PROPERTY = "PROPERTY"
TILE_TYPE_CHANCE = "CHANCE"
TILE_TYPE_JAIL = "JAIL"

# 初始化游戏板格子
for i in range(BOARD_SIZE):
    tile = {
        "id": i,
        "rect": None, # 矩形区域，用于绘制和点击
        "owner": None, # 属性拥有者 (None, player_id)
        "price": 0,    # 购买价格
        "rent": 0,     # 租金
        "name": f"Tile {i}",
        "type": TILE_TYPE_PROPERTY
    }

    if i == 0:
        tile["type"] = TILE_TYPE_START
        tile["name"] = "起点"
    elif i == 3:
        tile["type"] = TILE_TYPE_CHANCE
        tile["name"] = "机会"
    elif i == 6:
        tile["type"] = TILE_TYPE_JAIL
        tile["name"] = "监狱"
    elif i == 9:
        tile["type"] = TILE_TYPE_CHANCE
        tile["name"] = "命运"
    else:
        tile["price"] = (i + 1) * 50 # 示例价格
        tile["rent"] = (i + 1) * 10  # 示例租金
        tile["name"] = f"地产 {i}"

    BOARD.append(tile)

# --- 4. 玩家类定义 ---
class Player:
    def __init__(self, id, color, start_money=1500):
        self.id = id
        self.color = color
        self.money = start_money
        self.position = 0 # 当前所在格子索引
        self.properties = [] # 拥有的地产ID列表

    def move(self, steps):
        old_position = self.position
        self.position = (self.position + steps) % BOARD_SIZE
        # 如果路过或到达起点，增加金钱
        if self.position < old_position: # 说明绕了一圈
            self.money += 200 # 路过起点奖励
        elif self.position == 0 and old_position != 0: # 如果正好停在起点
             self.money += 200 # 停在起点奖励

    def add_money(self, amount):
        self.money += amount

    def deduct_money(self, amount):
        self.money -= amount

    def buy_property(self, tile_id, price):
        if self.money >= price:
            self.deduct_money(price)
            self.properties.append(tile_id)
            BOARD[tile_id]["owner"] = self.id
            return True
        return False

# --- 5. 游戏逻辑函数 ---

def roll_dice():
    """模拟掷骰子，返回1到6的随机数"""
    return random.randint(1, 6)

def handle_land_on_tile(player, tile_id, current_player_index, players):
    """处理玩家落在某个格子上的逻辑"""
    tile = BOARD[tile_id]
    global game_message # 声明全局变量以修改

    game_message = f"玩家 {player.id + 1} 落在 '{tile['name']}'"

    if tile["type"] == TILE_TYPE_START:
        game_message += ", 获得 $200。"
        # 停在起点额外奖励，路过已在move()中处理
        # player.add_money(200)

    elif tile["type"] == TILE_TYPE_PROPERTY:
        if tile["owner"] is None: # 无主之地
            # 玩家可以选择购买
            game_message += f", 无主地，价格 ${tile['price']}。点击 '购买' 或 '跳过'。"
            return "DECISION_NEEDED" # 需要玩家做决定
        elif tile["owner"] == player.id: # 自己的地
            game_message += ", 这是你的地。"
        else: # 别人的地，付租金
            owner_player = players[tile["owner"]]
            rent = tile["rent"]
            if player.money >= rent:
                player.deduct_money(rent)
                owner_player.add_money(rent)
                game_message += f", 支付玩家 {owner_player.id + 1} 租金 ${rent}。"
            else:
                game_message += f", 破产了！需要支付玩家 {owner_player.id + 1} 租金 ${rent}，但钱不够！"
                # 这里可以添加破产逻辑，简化版暂时只提示
                end_game(f"玩家 {player.id + 1} 破产了！")
                return "GAME_OVER"

    elif tile["type"] == TILE_TYPE_CHANCE:
        # 随机事件
        event_money = random.choice([-100, 50, 200, -50])
        player.add_money(event_money)
        game_message += f", 触发事件！{'获得' if event_money >= 0 else '失去'} ${abs(event_money)}。"

    elif tile["type"] == TILE_TYPE_JAIL:
        game_message += ", 路过监狱，没事。" # 简化版不设惩罚

    return "ACTION_DONE" # 动作完成，可以进入下一回合

def end_game(winner_msg):
    """游戏结束函数"""
    global running, game_message
    running = False
    game_message = f"游戏结束！{winner_msg}"
    print(game_message) # 打印到控制台

# --- 6. 游戏状态和变量 ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame 简化版大富翁")

players = [Player(0, BLUE), Player(1, RED)]
current_player_index = 0
dice_rolled = False
current_dice_value = 0
game_message = "玩家 1 请掷骰子！"
game_state = "ROLL_DICE" # ROLL_DICE, WAITING_FOR_ACTION, DECISION_NEEDED, GAME_OVER

# 按钮的矩形区域
roll_button_rect = pygame.Rect(SCREEN_WIDTH - 150, 50, 120, 50)
buy_button_rect = pygame.Rect(SCREEN_WIDTH - 150, 120, 120, 50)
skip_button_rect = pygame.Rect(SCREEN_WIDTH - 150, 190, 120, 50)
next_turn_button_rect = pygame.Rect(SCREEN_WIDTH - 150, 260, 120, 50) # 新增下一回合按钮

# --- 7. 布局计算 (将棋盘格子放置在屏幕上) ---
def calculate_board_layout():
    """计算每个格子的屏幕位置和矩形"""
    tiles_per_side = BOARD_SIZE // 4 # 每边3个格子
    # 底部一排 (从左到右)
    for i in range(tiles_per_side + 1): # 0, 1, 2, 3
        idx = i
        BOARD[idx]["rect"] = pygame.Rect(
            50 + i * TILE_SIZE, SCREEN_HEIGHT - 50 - TILE_SIZE, TILE_SIZE, TILE_SIZE
        )
    # 左边一列 (从下到上)
    for i in range(1, tiles_per_side + 1): # 4, 5, 6
        idx = tiles_per_side + i
        BOARD[idx]["rect"] = pygame.Rect(
            50, SCREEN_HEIGHT - 50 - TILE_SIZE - i * TILE_SIZE, TILE_SIZE, TILE_SIZE
        )
    # 顶部一排 (从左到右)
    for i in range(1, tiles_per_side + 1): # 7, 8, 9
        idx = tiles_per_side * 2 + i
        BOARD[idx]["rect"] = pygame.Rect(
            50 + i * TILE_SIZE, 50, TILE_SIZE, TILE_SIZE
        )
    # 右边一列 (从上到下)
    for i in range(1, tiles_per_side): # 10, 11
        idx = tiles_per_side * 3 + i
        BOARD[idx]["rect"] = pygame.Rect(
            SCREEN_WIDTH - 50 - TILE_SIZE, 50 + i * TILE_SIZE, TILE_SIZE, TILE_SIZE
        )

calculate_board_layout()

# --- 8. 游戏主循环 ---
running = True
clock = pygame.time.Clock()

while running:
    # --- 事件处理 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if game_state == "ROLL_DICE":
                if roll_button_rect.collidepoint(mouse_pos):
                    current_dice_value = roll_dice()
                    players[current_player_index].move(current_dice_value)
                    game_message = f"玩家 {players[current_player_index].id + 1} 掷出 {current_dice_value} 点。"
                    # 处理落点逻辑
                    action_result = handle_land_on_tile(
                        players[current_player_index],
                        players[current_player_index].position,
                        current_player_index,
                        players
                    )
                    if action_result == "DECISION_NEEDED":
                        game_state = "DECISION_NEEDED"
                    elif action_result == "GAME_OVER":
                        game_state = "GAME_OVER"
                    else:
                        game_state = "WAITING_FOR_ACTION" # 等待点击下一回合

            elif game_state == "DECISION_NEEDED":
                if buy_button_rect.collidepoint(mouse_pos):
                    current_tile_id = players[current_player_index].position
                    tile = BOARD[current_tile_id]
                    if players[current_player_index].buy_property(tile["id"], tile["price"]):
                        game_message += f" 购买成功！"
                    else:
                        game_message += f" 购买失败！金钱不足。"
                    game_state = "WAITING_FOR_ACTION"

                elif skip_button_rect.collidepoint(mouse_pos):
                    game_message += f" 放弃购买。"
                    game_state = "WAITING_FOR_ACTION"

            elif game_state == "WAITING_FOR_ACTION":
                 if next_turn_button_rect.collidepoint(mouse_pos):
                    current_player_index = (current_player_index + 1) % len(players)
                    game_message = f"玩家 {players[current_player_index].id + 1} 请掷骰子！"
                    game_state = "ROLL_DICE"

    # --- 绘制 ---
    board_background_image = None
    original_board_image = pygame.image.load("16pic_8128697_b.jpg").convert()

    # 缩放棋盘图片到屏幕大小
    board_background_image = pygame.transform.scale(original_board_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    if board_background_image:  # 确保图片已成功加载
        screen.blit(board_background_image, (0, 0))
    else:
        # 如果背景图加载失败，可以回退到填充颜色
        screen.fill(GREEN)
    # 绘制格子
    for tile in BOARD:
        pygame.draw.rect(screen, GRAY, tile["rect"], 0) # 填充格子
        pygame.draw.rect(screen, BLACK, tile["rect"], 3) # 边框

        # 绘制格子名称
        name_text = small_font.render(tile["name"], True, BLACK)
        screen.blit(name_text, (tile["rect"].x + 5, tile["rect"].y + 5))

        # 绘制价格/租金 (如果适用)
        if tile["type"] == TILE_TYPE_PROPERTY:
            if tile["owner"] is None:
                price_text = small_font.render(f"${tile['price']}", True, BLACK)
                screen.blit(price_text, (tile["rect"].x + 5, tile["rect"].y + 25))
            else:
                owner_color = players[tile["owner"]].color
                pygame.draw.rect(screen, owner_color, (tile["rect"].x + 5, tile["rect"].y + 55, TILE_SIZE - 10, 20), 0)
                owner_text = small_font.render(f"P{tile['owner']+1}", True, WHITE)
                screen.blit(owner_text, (tile["rect"].x + 10, tile["rect"].y + 55))


    # 绘制玩家棋子
    # 加载图片
    player_images = []

    player_images.append(
        pygame.transform.scale(
            pygame.image.load("player1.png").convert_alpha(),  # 加载并优化
            (PLAYER_SIZE, PLAYER_SIZE)  # 缩放
        )
    )
    player_images.append(
        pygame.transform.scale(
            pygame.image.load("player2.png").convert_alpha(),  # 加载并优化
            (PLAYER_SIZE, PLAYER_SIZE)  # 缩放
        )
    )

    for player in players:
        tile_rect = BOARD[player.position]["rect"]
        # 在格子里稍微错开位置，避免重叠
        # Calculate position for the image
        # We want to center the image within the tile_rect, then potentially offset it for multiple players
        # Image top-left corner calculation:
        image_x = tile_rect.centerx - PLAYER_SIZE // 2 + (player.id * 10 - 5)
        image_y = tile_rect.centery - PLAYER_SIZE // 2

        # Draw the player image
        screen.blit(player_images[player.id], (image_x, image_y))


    # 绘制玩家信息
    for i, player in enumerate(players):
        player_info_text = font.render(f"玩家 {player.id + 1}: ${player.money}", True, player.color)
        screen.blit(player_info_text, (50, 10 + i * 40))

    # 绘制当前骰子点数
    dice_text = font.render(f"骰子: {current_dice_value}", True, BLACK)
    screen.blit(dice_text, (SCREEN_WIDTH - 200, 10))

    # 绘制游戏信息
    message_text = font.render(game_message, True, BLACK)
    screen.blit(message_text, (50, SCREEN_HEIGHT - 40))


    # 绘制按钮
    if game_state == "ROLL_DICE":
        pygame.draw.rect(screen, BLUE, roll_button_rect)
        roll_text = font.render("掷骰子", True, WHITE)
        text_rect = roll_text.get_rect(center=roll_button_rect.center)
        screen.blit(roll_text, text_rect)
    elif game_state == "DECISION_NEEDED":
        pygame.draw.rect(screen, BLUE, buy_button_rect)
        buy_text = font.render("购买", True, WHITE)
        text_rect_buy = buy_text.get_rect(center=buy_button_rect.center)
        screen.blit(buy_text, text_rect_buy)

        pygame.draw.rect(screen, RED, skip_button_rect)
        skip_text = font.render("跳过", True, WHITE)
        text_rect_skip = skip_text.get_rect(center=skip_button_rect.center)
        screen.blit(skip_text, text_rect_skip)
    elif game_state == "WAITING_FOR_ACTION":
        pygame.draw.rect(screen, BLUE, next_turn_button_rect)
        next_turn_text = font.render("下一回合", True, WHITE)
        text_rect_next_turn = next_turn_text.get_rect(center=next_turn_button_rect.center)
        screen.blit(next_turn_text, text_rect_next_turn)


    pygame.display.flip()
    clock.tick(60)

# --- 游戏退出 ---
pygame.quit()
sys.exit()