import pygame, random
from datetime import datetime
import json

pygame.init()
W, H = 400, 300
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 24)
big_font = pygame.font.SysFont(None, 36)

player_name = ""
input_active = True
game_over = False
score = 0

def save_history(name, score):
    try:
        with open("history.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []   # ถ้าไฟล์ยังไม่มี → สร้าง list ใหม่

    data.append({
        "เวลา": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ชื่อ": name,
        "คะแนน": score
    })

    with open("history.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def draw_name_input():
    screen.fill((0, 0, 0))
    title = font.render("Enter your name:", True, (255, 255, 255))
    name_text = font.render(player_name, True, (0, 255, 0))
    screen.blit(title, (W//2 - title.get_width()//2, 90))
    screen.blit(name_text, (W//2 - name_text.get_width()//2, 130))
    pygame.display.update()

def draw_score():
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

def draw_game_over():
    screen.fill((0, 0, 0))

    over = big_font.render("GAME OVER!", True, (255, 0, 0))
    sc = font.render(f"Your score: {score}", True, (255, 255, 255))
    screen.blit(over, (W//2 - over.get_width()//2, 50))
    screen.blit(sc, (W//2 - sc.get_width()//2, 90))

    restart_btn = pygame.Rect(110, 140, 180, 35)
    exit_btn = pygame.Rect(110, 190, 180, 35)

    pygame.draw.rect(screen, (0, 150, 0), restart_btn)
    pygame.draw.rect(screen, (150, 0, 0), exit_btn)

    r_text = font.render("Restart", True, (255, 255, 255))
    e_text = font.render("Exit", True, (255, 255, 255))

    screen.blit(r_text, (restart_btn.centerx - r_text.get_width()//2,
                          restart_btn.centery - r_text.get_height()//2))
    screen.blit(e_text, (exit_btn.centerx - e_text.get_width()//2,
                          exit_btn.centery - e_text.get_height()//2))

    pygame.display.update()
    return restart_btn, exit_btn

class Snake:
    def __init__(self):
        self.body = [[100, 50]]
        self.dx, self.dy = 10, 0

    def move(self):
        head = [self.body[0][0] + self.dx, self.body[0][1] + self.dy]
        self.body.insert(0, head)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def draw(self):
        for b in self.body:
            pygame.draw.rect(screen, (0, 255, 0), (*b, 10, 10))

class Food:
    def __init__(self):
        self.x = random.randrange(0, W, 10)
        self.y = random.randrange(0, H, 10)

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 10, 10))

snake = Snake()
food = Food()

run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

        if input_active:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and player_name != "":
                    input_active = False
                elif e.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    if len(player_name) < 10:
                        player_name += e.unicode

        elif game_over:
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                restart_btn, exit_btn = draw_game_over()

                if restart_btn.collidepoint(mx, my):
                    snake = Snake()
                    food = Food()
                    score = 0
                    game_over = False

                if exit_btn.collidepoint(mx, my):
                    run = False

        else:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:  snake.dx, snake.dy = -10, 0
                if e.key == pygame.K_RIGHT: snake.dx, snake.dy = 10, 0
                if e.key == pygame.K_UP:    snake.dx, snake.dy = 0, -10
                if e.key == pygame.K_DOWN:  snake.dx, snake.dy = 0, 10

    if input_active:
        draw_name_input()
        continue

    if game_over:
        draw_game_over()
        continue

    snake.move()

    if snake.body[0] == [food.x, food.y]:
        snake.grow()
        food = Food()
        score += 1

    if snake.body[0][0] < 0 or snake.body[0][0] >= W or \
       snake.body[0][1] < 0 or snake.body[0][1] >= H:
        save_history(player_name, score)
        game_over = True

    screen.fill((0, 0, 0))
    snake.draw()
    food.draw()
    draw_score()
    pygame.display.update()
    clock.tick(10)

pygame.quit()
