import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Running Race Mini-Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player settings
dogdog_width, dogdog_height = 40, 60
dogdog_x, dogdog_y = 50, HEIGHT - dogdog_height - 20
dogdog_speed =7  # Move speed per click

# Obstacle settings
obstacle_width, obstacle_height = 50, 50
obstacle_speed = 5
obstacles = []

# Generate obstacles
for obstacle in range(6):
    obstacle_x = random.randint(WIDTH // 2, WIDTH - obstacle_width)
    obstacle_y = random.randint(0, HEIGHT - obstacle_height)
    obstacles.append(pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height))

# Finish line
finishline = WIDTH - 100

# Font settings
font = pygame.font.SysFont(None, 48)

# Timer settings
time_limit = 25  # 10 seconds to reach the finish line
start_time = time.time()

# Load images
background_pic = pygame.image.load(r"c:\Users\User\Downloads\PYTHON\background.png")
background_pic = pygame.transform.scale(background_pic, (WIDTH, HEIGHT))  # Resize the image to match the screen dimensions
dogdog_pic = pygame.image.load(r"c:\Users\User\Downloads\PYTHON\dog.png")
dogdog_pic = pygame.transform.scale(dogdog_pic, (dogdog_width, dogdog_height))  # Resize the image to match player dimensions

# Game loop
running = True
dogdog_won = False

while running:
    # Draw background image instead of filling with color
    screen.blit(background_pic, (0, 0))

    # Calculate time left
    time_left = time_limit - (time.time() - start_time)
    if time_left <= 0:
        time_left = 0
        running = False

    # Check for events
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

    # Keep player within screen bounds
    dogdog_x = max(0, min(dogdog_x, WIDTH - dogdog_width))
    dogdog_y = max(0, min(dogdog_y, HEIGHT - dogdog_height))

    # Draw player
    dogdog_rect = pygame.Rect(dogdog_x, dogdog_y, dogdog_width, dogdog_height)
    screen.blit(dogdog_pic, dogdog_rect)

    # Move and draw obstacles
    for obstacle in obstacles:
        obstacle.x -= obstacle_speed
        if obstacle.x < -obstacle_width:
            obstacle.x = WIDTH
            obstacle.y = random.randint(0, HEIGHT - obstacle_height)
        pygame.draw.rect(screen, BLUE, obstacle)

    # Draw finish line
    pygame.draw.line(screen, BLACK, (finishline, 0), (finishline, HEIGHT), 5)

    # Draw timer
    timer_text = font.render(f"Time Left: {int(time_left)}s", True, BLACK)
    screen.blit(timer_text, (10, 10))

    # Check if player collides with an obstacle
    if any(obstacle.colliderect(dogdog_rect) for obstacle in obstacles):
        running = False  # End the game if collision occurs

    # Check if player reaches the finish line
    if dogdog_x + dogdog_width >= finishline:
        dogdog_win = True
        running = False

    # Update display
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(30)

# End game message
screen.blit(background_pic, (0, 0))
if dogdog_won:
    endtxt = font.render("You Win!", True, GREEN)
else:
    endtxt = font.render("Game Over", True, BLACK)

screen.blit(endtxt, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
pygame.display.flip()
pygame.time.wait(3000)


pygame.quit()
