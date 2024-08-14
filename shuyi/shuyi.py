import pygame

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1280, 768))
pygame.display.set_caption("Simulator Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)

# Load the button image and get its rect
menu_button_image = pygame.image.load("menu_button.png")  # Replace with your image path
menu_button_rect = menu_button_image.get_rect()
menu_button_image = pygame.transform.scale(menu_button_image, (241, 240))
menu_button_rect.topleft = (519.5, 264)  # Set the position (top-left corner)


# Game variables
menu_open = False

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the menu button is clicked
            if menu_button_rect.collidepoint(event.pos):
                menu_open = not menu_open
    
    # Clear screen
    screen.fill(WHITE)
    
    # Draw the button image at the specified position
    screen.blit(menu_button_image, menu_button_rect.topleft)

    # If the menu is open, draw the hovering menu
    if menu_open:
        pygame.draw.rect(screen, BLACK, (250, 150, 300, 300))
        pygame.draw.rect(screen, GREY, (260, 160, 280, 280))

        # Draw some options on the menu
        font = pygame.font.Font(None, 36)
        option1_text = font.render("Option 1", True, WHITE)
        option2_text = font.render("Option 2", True, WHITE)
        screen.blit(option1_text, (300, 200))
        screen.blit(option2_text, (300, 250))

    # Update display
    pygame.display.flip()

pygame.quit()
