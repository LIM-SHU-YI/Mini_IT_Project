import pygame
import sys

# code by chatgpt for me to check the coordinates for imgs

# Initialize pygame
pygame.init()

# Set up the screen dimensions
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mouse Coordinate Capture")

livingroom = pygame.image.load("asset/image/part2a/livingroom.png")
interface = pygame.image.load("asset/image/part2a/int.png")
ref = pygame.image.load("asset/image/part2a/ref.png")
credit = pygame.image.load("asset/image/creditimg.png")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            # Get the mouse coordinates
            mouse_x, mouse_y = pygame.mouse.get_pos()
            print(f"Mouse coordinates: ({mouse_x}, {mouse_y})")
    
    # Fill the screen with a black color
    screen.blit(credit, (0,0))
    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
