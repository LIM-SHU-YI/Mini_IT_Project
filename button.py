import sys
import pygame

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Pet Interaction Game")

# Load images
images = [
    pygame.image.load("love button/dog_i.png"), 
    pygame.image.load("love button/dog_ii.png"), 
    pygame.image.load("love button/dog_iii.png")
]
current_image_index = 0

# Progress bar setup
progress = 0
max_progress = 30  # 10 strokes for each stage
bar_width = 400
bar_height = 30
bar_x = 200
bar_y = 50

# Define the interaction area (x, y, width, height)
interaction_area = pygame.Rect(200, 150, 400, 200)

# Variables to track mouse movement direction
last_mouse_x = None
direction = None
strokes = 0

# Game loop
running = True

while running:
    screen.fill((255, 255, 255))  # Fill the background with white
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Mouse movement detection
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            
            # Check if the mouse is within the interaction area
            if interaction_area.collidepoint(mouse_x, mouse_y):
                if last_mouse_x is not None:
                    if mouse_x > last_mouse_x and direction != "right":
                        direction = "right"
                        strokes += 1
                    elif mouse_x < last_mouse_x and direction != "left":
                        direction = "left"
                        strokes += 1
                    
                    # Update progress based on strokes
                    progress = (strokes / max_progress) * 100
                    
                    # Update the current image based on progress
                    if progress >= 66.6666:
                        current_image_index = 2
                    elif progress >= 33.3333:
                        current_image_index = 1

                last_mouse_x = mouse_x
            else:
                # Reset direction when out of interaction area
                last_mouse_x = None
                direction = None

        # Check if progress reaches 100%
        if progress >= 100:
            running = False  # Exit the game loop

    # Draw the current image
    screen.blit(images[current_image_index], (200, 150))

    # Draw progress bar
    pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 2)  # Bar outline
    pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, (progress / 100) * bar_width, bar_height))  # Progress fill

    # Draw interaction area for debugging (optional)
    pygame.draw.rect(screen, (255, 0, 0, 100), interaction_area, 2)  # Red rectangle for the interaction area
    
    pygame.display.flip()

# Quit Pygame
pygame.quit()
