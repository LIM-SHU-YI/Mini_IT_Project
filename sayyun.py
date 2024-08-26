import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Running Race Mini-Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

dogdog_width, dogdog_height = 90, 80
dogdog_x, dogdog_y = 50, HEIGHT - dogdog_height - 20
dogdog_speed = 25 

obstacle_width, obstacle_height = 120, 80
obstacle_speed = 8
obstacle_spacing = 65 
vertical_spacing = 115
obstacles = []

background_pic = pygame.image.load("running_race/riverbackground.png")
background_pic = pygame.transform.scale(background_pic, (WIDTH, HEIGHT))
dogdog_pic1 = pygame.image.load("running_race/dog_1.png")
dogdog_pic1 = pygame.transform.scale(dogdog_pic1, (dogdog_width, dogdog_height))
dogdog_pic2 = pygame.image.load("running_race/dog_2.png")
dogdog_pic2 = pygame.transform.scale(dogdog_pic2, (dogdog_width, dogdog_height))
current_dog_pic = dogdog_pic1
obstacle_pic = pygame.image.load("running_race/obstacle_1.png")
obstacle_pic = pygame.transform.scale(obstacle_pic, (obstacle_width, obstacle_height))

# Initialize the first obstacle
def create_obstacle(x):
    while True:
        obstacle_y = random.randint(0, HEIGHT - obstacle_height)
        if not obstacles or abs(obstacle_y - obstacles[-1].y) > vertical_spacing:
            break
    return pygame.Rect(x, obstacle_y, obstacle_width, obstacle_height)

# Generate initial obstacles
last_x = WIDTH
for _ in range(15):
    last_x += random.randint(obstacle_spacing, obstacle_spacing * 2)
    obstacles.append(create_obstacle(last_x))

finishline = WIDTH - 100

font = pygame.font.SysFont(None, 48)

time_limit = 20  # 25 seconds to reach the finish line
start_time = time.time()

# Game loop
running = True
dogdog_win = False

# Animation toggle
frame_toggle = True

while running:
    screen.blit(background_pic, (0, 0))

    time_left = time_limit - (time.time() - start_time)
    if time_left <= 0:
        time_left = 0
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                dogdog_x += dogdog_speed
            if event.key == pygame.K_LEFT:
                dogdog_x -= dogdog_speed
            if event.key == pygame.K_UP:
                dogdog_y -= dogdog_speed
            if event.key == pygame.K_DOWN:
                dogdog_y += dogdog_speed

            if frame_toggle:
                current_dog_pic = dogdog_pic2
            else:
                current_dog_pic = dogdog_pic1
            frame_toggle = not frame_toggle

    dogdog_x = max(0, min(dogdog_x, WIDTH - dogdog_width))
    dogdog_y = max(0, min(dogdog_y, HEIGHT - dogdog_height))

    dogdog_rect = pygame.Rect(dogdog_x, dogdog_y, dogdog_width, dogdog_height)
    screen.blit(current_dog_pic, dogdog_rect.topleft)

    for obstacle in obstacles:
        obstacle.x -= obstacle_speed
        if obstacle.x < -obstacle_width:
            obstacles.remove(obstacle)
            new_obstacle_x = WIDTH + obstacle_width
            obstacles.append(create_obstacle(new_obstacle_x))

        screen.blit(obstacle_pic, obstacle.topleft)

    pygame.draw.line(screen, BLACK, (finishline, 0), (finishline, HEIGHT), 5)

    timer_text = font.render(f"Time Left: {int(time_left)}s", True, BLACK)
    screen.blit(timer_text, (10, 10))

    if any(obstacle.colliderect(dogdog_rect) for obstacle in obstacles):
        running = False

    if dogdog_x + dogdog_width >= finishline:
        dogdog_win = True
        running = False

    pygame.display.flip()
    pygame.time.Clock().tick(30)

screen.blit(background_pic, (0, 0))
if dogdog_win:
    endtxt = font.render("You Win!", True, GREEN)
else:
    endtxt = font.render("Game Over", True, BLACK)

screen.blit(endtxt, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
