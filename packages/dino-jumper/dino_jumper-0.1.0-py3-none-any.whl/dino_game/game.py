import pygame
import random
import sys
import os

# 初始化Pygame
pygame.init()

# 设置窗口
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('小恐龙跳仙人掌')

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 游戏参数
GRAVITY = 0.8
JUMP_SPEED = -15
GROUND_HEIGHT = 350
MAX_JUMPS = 2  # 最大跳跃次数

# 设置字体
def get_font(size):
    # 尝试使用系统中文字体
    system_fonts = [
        "C:/Windows/Fonts/simhei.ttf",  # Windows 黑体
        "C:/Windows/Fonts/msyh.ttc",    # Windows 微软雅黑
        "/System/Library/Fonts/PingFang.ttc",  # macOS
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf"  # Linux
    ]
    
    for font_path in system_fonts:
        if os.path.exists(font_path):
            return pygame.font.Font(font_path, size)
    
    # 如果没有找到中文字体，使用默认字体
    return pygame.font.Font(None, size)

# 恐龙类
class Dino:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = 50
        self.y = GROUND_HEIGHT
        self.velocity = 0
        self.is_jumping = False
        self.jumps_remaining = MAX_JUMPS
        self.height = 50
        self.width = 30

    def jump(self):
        if self.jumps_remaining > 0:
            self.velocity = JUMP_SPEED
            self.is_jumping = True
            self.jumps_remaining -= 1

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

        if self.y >= GROUND_HEIGHT:
            self.y = GROUND_HEIGHT
            self.velocity = 0
            self.is_jumping = False
            self.jumps_remaining = MAX_JUMPS  # 落地时重置跳跃次数

    def draw(self, screen):
        # 绘制恐龙身体
        pygame.draw.rect(screen, BLACK, (self.x, self.y - self.height, self.width, self.height))
        # 绘制'dyx'标识
        font = get_font(24)
        text = font.render('dyx', True, BLACK)
        screen.blit(text, (self.x, self.y - self.height - 20))
        
        # 显示剩余跳跃次数
        jumps_text = font.render(f'跳跃: {self.jumps_remaining}', True, BLACK)
        screen.blit(jumps_text, (self.x, self.y - self.height - 40))

    def get_rect(self):
        return pygame.Rect(self.x, self.y - self.height, self.width, self.height)

# 仙人掌类
class Cactus:
    def __init__(self):
        self.characters = '典孝急乐蚌批赢麻'
        self.width = 20
        self.speed = 5
        self.reset()

    def reset(self):
        self.x = WINDOW_WIDTH + random.randint(100, 300)
        self.height = random.randint(30, 100)
        self.y = GROUND_HEIGHT - self.height
        self.char = random.choice(self.characters)

    def update(self):
        self.x -= self.speed
        if self.x < -self.width:
            self.reset()

    def draw(self, screen):
        font = get_font(self.height)
        text = font.render(self.char, True, BLACK)
        screen.blit(text, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

def show_game_over(score):
    font = get_font(74)
    text = font.render('游戏结束!', True, RED)
    text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 50))
    screen.blit(text, text_rect)
    
    score_font = get_font(48)
    score_text = score_font.render(f'最终分数: {score}', True, BLACK)
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 50))
    screen.blit(score_text, score_rect)
    
    pygame.display.flip()
    pygame.time.wait(2000)

def reset_game():
    dino = Dino()
    cacti = [Cactus() for _ in range(3)]
    score = 0
    game_over = False
    return dino, cacti, score, game_over

def run_game():
    clock = pygame.time.Clock()
    dino, cacti, score, game_over = reset_game()
    font = get_font(36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    dino.jump()
                elif event.key == pygame.K_r and game_over:
                    # 重新开始游戏
                    dino, cacti, score, game_over = reset_game()

        if not game_over:
            # 更新游戏状态
            dino.update()
            for cactus in cacti:
                cactus.update()
                # 检测碰撞
                if dino.get_rect().colliderect(cactus.get_rect()):
                    game_over = True
                    show_game_over(score)
                    break

            # 更新分数
            score += 1

            # 绘制
            screen.fill(WHITE)
            # 绘制地面
            pygame.draw.line(screen, BLACK, (0, GROUND_HEIGHT), (WINDOW_WIDTH, GROUND_HEIGHT), 2)
            dino.draw(screen)
            for cactus in cacti:
                cactus.draw(screen)
            
            # 显示分数
            score_text = font.render(f'分数: {score}', True, BLACK)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(60)
        else:
            # 显示重新开始提示
            restart_font = get_font(36)
            restart_text = restart_font.render('按 R 键重新开始', True, BLACK)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 100))
            screen.blit(restart_text, restart_rect)
            pygame.display.flip()

def main():
    run_game()

if __name__ == '__main__':
    main() 