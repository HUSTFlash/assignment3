import pygame
import random
import math

enemy_num = 10
enemy_size_min = 1
enemy_size_max = 5
screen_width = 1280
screen_height = 720

class Ball(object):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.status = True
        
class PlayerBall(Ball):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)
    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.x, self.y), self.size)
    def eat(self, target_ball):
        if self != target_ball and self.status and target_ball.status:
            if math.sqrt((self.x - target_ball.x)**2 + (self.y - target_ball.y)**2) <= self.size:
                target_ball.status = False
                self.size += target_ball.size

class EnemyBall(Ball):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)
    def draw(self, screen):
        pygame.draw.circle(screen, "yellow", (self.x, self.y), self.size)

def create_player_ball():
    initial_position_x = screen_width / 2
    initial_position_y = screen_height / 2
    player_initial_size = 10
    player_ball = PlayerBall(initial_position_x, initial_position_y, player_initial_size)
    return player_ball

def create_enemy_ball(balls):
    if len(balls) < enemy_num:
        enemy_position_x = random.randint(0, screen_width)
        enemy_position_y = random.randint(0, screen_height)
        enemy_size = random.randint(enemy_size_min, enemy_size_max)
        enemy_ball = EnemyBall(enemy_position_x, enemy_position_y, enemy_size)
        balls.append(enemy_ball)
        
def player_move(player_ball, speed):
    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
        if player_ball.y <= 0:
            player_ball.y = 0
        player_ball.y -= speed
    if key[pygame.K_DOWN]:
        if player_ball.y >= screen_height:
            player_ball.y = screen_height
        player_ball.y += speed
    if key[pygame.K_LEFT]:
        if player_ball.x <= 0:
            player_ball.x = 0
        player_ball.x -= speed
    if key[pygame.K_RIGHT]:
        if player_ball.x >= screen_width:
            player_ball.x = screen_width
        player_ball.x += speed
        
def player_eat(player_ball, balls):
    for ball in balls:
        player_ball.eat(ball)
        
def draw_screen(player_ball, balls, screen):
    screen.fill("black")
    if player_ball.status:
        player_ball.draw(screen)
    for ball in balls:
        if ball.status:
            ball.draw(screen)
    

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Eat Ball Game")
clock = pygame.time.Clock()
running = True
dt = clock.tick(60) / 1000
speed = 30 * dt
enemy_balls = []

player_ball = create_player_ball()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    create_enemy_ball(enemy_balls)
    draw_screen(player_ball, enemy_balls, screen)
    pygame.display.flip()
    player_move(player_ball, speed)
    player_eat(player_ball, enemy_balls)
    
pygame.quit()