import pygame
import random
from button import Button
from common import text_with_shadow, normal_text, cutedisplay

# Initialize Pygame
pygame.init()

# Set up the display
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load("asset/image/gameicon.png")
pygame.display.set_caption("Memories")
pygame.display.set_icon(icon)

# Load images
background = pygame.image.load("Photo used/Button/game background.png")
hug_img = pygame.image.load("Photo used/Button/Hug.png")
angry_img = pygame.image.load("Photo used/Button/Angry.png")
food_img = pygame.image.load("Photo used/Button/Food.png")
play_img = pygame.image.load("Photo used/Button/Play.png")
me_img = pygame.image.load("Photo used/Button/Me.png")
dad_img = pygame.image.load("Photo used/Button/Dad.png")

# Create buttons
buttons = {
    "Hug": Button(387, 560, image=hug_img),
    "Angry": Button(643, 563, image=angry_img),
    "Food": Button(391, 378, image=food_img),
    "Play": Button(865, 545, image=play_img),
    "Me": Button(857, 376, image=me_img),
    "Dad": Button(640, 378, image=dad_img)
}

# Game variables
words = ["Hug", "Angry", "Food", "Play", "Me", "Dad", "Hug Me", "Me Angry", "Dad Play", "Dad Food"]
current_word = ""
correct_answers = 0
wrong_answers = 0
total_questions = 5
game_over = False
clicked_sequence = []

# Main game loop
running = True
clock = pygame.time.Clock()

def display_result(result):
    screen.fill((255, 255, 255))
    result_text = normal_text(result, cutedisplay(50), (0, 0, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(*result_text)
    pygame.display.flip()
    pygame.time.wait(2000)

def new_question():
    global current_word, clicked_sequence
    if words:
        current_word = random.choice(words)
        words.remove(current_word)
        clicked_sequence = []
    else:
        game_over = True

# Start with a question
new_question()

while running:
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_pos = pygame.mouse.get_pos()
            for word, button in buttons.items():
                if button.checkforinput(mouse_pos):
                    clicked_sequence.append(word)
                    
                    if " " in current_word:
                        expected_sequence = current_word.split()
                        if len(clicked_sequence) == len(expected_sequence):
                            if clicked_sequence == expected_sequence:
                                correct_answers += 1
                                display_result("Correct!")
                            else:
                                wrong_answers += 1
                                display_result("Wrong!")
                            new_question()
                    else:
                        if clicked_sequence[0] == current_word:
                            correct_answers += 1
                            display_result("Correct!")
                        else:
                            wrong_answers += 1
                            display_result("Wrong!")
                        new_question()
                    
                    if correct_answers + wrong_answers >= total_questions or wrong_answers >= 3:
                        game_over = True

    if not game_over:
        # Display current word or sentence
        if current_word:
            word_text = normal_text(current_word, cutedisplay(40), (0, 0, 0), (SCREEN_WIDTH // 2, 200))
            screen.blit(*word_text)
        
        # Draw buttons
        for button in buttons.values():
            button.update(screen)
    else:
        # Game over screen
        screen.fill((255, 255, 255))
        if wrong_answers >= 3:
            message = "You did not learn how to use the button"
        else:
            message = "You know how to use the button already"
        
        game_over_text = normal_text(message, cutedisplay(40), (0, 0, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(*game_over_text)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

