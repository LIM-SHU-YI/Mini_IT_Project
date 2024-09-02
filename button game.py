import pygame
import random
import sys
import time

pygame.init()

# Screen size
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Click correct button!")

# Fonts
font = pygame.font.Font(None, 74)

# Colors Used
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 128, 255)
BUTTON_HOVER = (0, 200, 255)

# List for Words and buttons
words = ["Hungry", "Thirsty", "Sleepy"]
buttons = []

# Create buttons
button_width, button_height = 400, 75
button_x = (screen_width - button_width) // 2
for i, word in enumerate(words):
    button_rect = pygame.Rect(button_x, 150 + i * 100, button_width, button_height)
    buttons.append((word, button_rect))

# Function to draw buttons
def draw_buttons():
    for word, rect in buttons:
        color = BUTTON_COLOR if not rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_HOVER
        pygame.draw.rect(screen, color, rect)
        text = font.render(word, True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

# Random sentence
remaining_words = words.copy()
current_word = random.choice(remaining_words)

# Game loop variables
running = True
show_feedback = False
feedback_text = ""
feedback_display_time = 1.0  # Time to show feedback in seconds
last_feedback_time = time.time()  # Initialize with current time

# Get random word and exclude the existing one
def get_random_word(exclude_word=None):
    if exclude_word:
        possible_words = [word for word in remaining_words if word != exclude_word]
    else:
        possible_words = remaining_words
    return random.choice(possible_words) if possible_words else None

# Game loop
while running:
    screen.fill(WHITE)
    
    # Feedback
    if show_feedback:
        feedback_display = font.render(feedback_text, True, BLACK)
        feedback_rect = feedback_display.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(feedback_display, feedback_rect)  # Draw it 

        # Check duration 
        if time.time() - last_feedback_time > feedback_display_time:
            show_feedback = False
            if feedback_text == "All Correct! Game Over!":
                running = False
            else:
                # Update current_word only after feedback is hidden
                current_word = get_random_word(exclude_word=None)
                # Ensure current_word is valid
                if current_word is None:
                    feedback_text = "All Correct! Game Over!"
                    show_feedback = True
                last_feedback_time = time.time()
    
    # Display back 
    else:
        text = font.render(current_word, True, BLACK)
        text_rect = text.get_rect(center=(screen_width // 2, 50))
        screen.blit(text, text_rect)

        draw_buttons()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not show_feedback:
            for word, rect in buttons:
                if rect.collidepoint(event.pos):
                    if word == current_word:
                        if current_word in remaining_words:
                            remaining_words.remove(current_word)
                        feedback_text = "Correct!"
                        show_feedback = True
                        last_feedback_time = time.time()
                        # Set current_word to a new random one
                        current_word = get_random_word(exclude_word=None)
                    else:
                        feedback_text = "Try again!"
                        show_feedback = True
                        last_feedback_time = time.time()
                        # Set current_word to a new random one different from the current one
                        current_word = get_random_word(exclude_word=current_word)

    pygame.display.flip()

pygame.quit()
sys.exit()








'''
Code use for reference
import pygame
import random
import sys

pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Click the Right Button!")

# Font setup
font = pygame.font.Font(None, 74)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 128, 255)
BUTTON_HOVER = (0, 200, 255)

# Words and buttons
words = ["Hungry", "Thirsty", "Sleepy"]
buttons = []

# Create buttons
for i, word in enumerate(words):
    button_rect = pygame.Rect(200, 150 + i * 100, 400, 75)
    buttons.append((word, button_rect))

# Function to draw buttons
def draw_buttons():
    for word, rect in buttons:
        color = BUTTON_COLOR if not rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_HOVER
        pygame.draw.rect(screen, color, rect)
        text = font.render(word, True, BLACK)
        screen.blit(text, (rect.x + 20, rect.y + 20))

# Random sentence
current_word = random.choice(words)

# Game loop
running = True
while running:
    screen.fill(WHITE)
    
    # Display the current sentence
    text = font.render(current_word, True, BLACK)
    screen.blit(text, (250, 50))
    
    # Draw buttons
    draw_buttons()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for word, rect in buttons:
                if rect.collidepoint(event.pos):
                    if word == current_word:
                        print("Correct!")
                        current_word = random.choice(words)
                    else:
                        print("Try again!")

    pygame.display.flip()

pygame.quit()
sys.exit() 
'''