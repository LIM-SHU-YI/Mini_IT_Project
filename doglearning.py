import pygame
import random
import os
from button import Button
from common import text_with_shadow, normal_text, cutedisplay
import common
import threeinter

pygame.init()


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load("asset/image/gameicon.png")
pygame.display.set_caption("Memories")
pygame.display.set_icon(icon)


background = pygame.image.load("Photo used/Button/gamebackground.png")
hug_img = pygame.image.load("Photo used/Button/Hug.png")
angry_img = pygame.image.load("Photo used/Button/Angry.png")
food_img = pygame.image.load("Photo used/Button/Food.png")
play_img = pygame.image.load("Photo used/Button/Play.png")
me_img = pygame.image.load("Photo used/Button/Me.png")
dad_img = pygame.image.load("Photo used/Button/Dad.png")
replay_img = pygame.image.load("Photo used/Button/replay.png")


buttons = {
    "Hug": Button(387, 560, image=hug_img, visible=False),
    "Angry": Button(643, 563, image=angry_img, visible=False),
    "Food": Button(391, 378, image=food_img, visible=False),
    "Play": Button(865, 545, image=play_img, visible=False),
    "Me": Button(857, 376, image=me_img, visible=False),
    "Dad": Button(640, 378, image=dad_img, visible=False)
    
}

replay_button = Button(580, 180, image=replay_img, visible=True)


words = ["Hug", "Angry", "Food", "Play", "Me", "Dad", "Hug Me", "Me Angry", "Dad Play", "Dad Food"]
current_word = ""
correct_answers = 0
wrong_answers = 0
total_questions = 5
game_over = False
clicked_sequence = []
replay_count = 3
audio_playing = False
buttons_visible = False
delay = None

font = cutedisplay(40)

audio_files = {word: pygame.mixer.Sound(f"Audio Used/{word.replace(' ', '_').lower()}.wav") for word in words}

def drawtext(screen, text, font, colour, x, y):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        rendered_text = font.render(line, True, colour)
        screen.blit(rendered_text, (x, y + i * rendered_text.get_height()))

def display_result(result):
    screen.fill((255, 255, 255))
    result_text = normal_text(result, cutedisplay(50), (0, 0, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(*result_text)
    pygame.display.flip()
    pygame.time.wait(2000)

def new_question():
    global current_word, clicked_sequence, audio_playing, buttons_visible
    if words:
        current_word = random.choice(words)
        words.remove(current_word)
        clicked_sequence = []
        audio_playing = False
        buttons_visible = False
        for button in buttons.values():
            button.visible = False
    else:
        global game_over
        game_over = True

def play_audio():
    global audio_playing
    if current_word in audio_files:
        audio_files[current_word].play()
        audio_playing = True
    else:
        print(f"Warning: No audio file for '{current_word}'")
        audio_playing = False

def show_buttons():
    global buttons_visible
    for button in buttons.values():
        button.visible = True
    buttons_visible = True

def handle_button_click(word):
    global correct_answers, wrong_answers, game_over
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

def draw_game():
    global delay, font
    screen.blit(background, (0, 0))
    
    if not game_over:
        for button in buttons.values():
            if button.visible:
                button.update(screen)
        
        #Continue draw the replay button
        replay_button.update(screen)
        replay_text = normal_text(f"x{replay_count}", cutedisplay(80), (0, 0, 0), (730,180))
        screen.blit(*replay_text)
    else:
        screen.fill((255, 255, 255))
        if wrong_answers >= 3:
            message = (
                        "\n\n"
                        "Bad Ending:\n\n"
                        "Hachi did not learn how to use the button\n"
                        "and could not communicate with its owner.\n\n" 
                        "Its owner throw it away.")
            drawtext(screen,message,font,(0, 0, 0), 50, 50)
            pygame.display.flip()
        else:
            message = "Hachi learned how to use the button!"
            if delay is None:
                delay = pygame.time.get_ticks()
            drawtext(screen,message,font,(0, 0, 0), 320, 360)
            pygame.display.flip()

        if delay:
            current_time = pygame.time.get_ticks()
            if current_time - delay >= 1500:
                threeinter.kitinterface()
                delay = None  # Reset delay to avoid repeated calls

def doglearning_main_game_loop():
    global running, replay_count, buttons_visible, audio_playing, delay
    
    new_question()
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                common.click.play()
                mouse_pos = pygame.mouse.get_pos()
                
                if replay_button.checkforinput(mouse_pos) and replay_count > 0:
                    play_audio()
                    replay_count -= 1
                    buttons_visible = False
                    for button in buttons.values():
                        button.visible = False
                
                if buttons_visible:
                    for word, button in buttons.items():
                        if button.checkforinput(mouse_pos) and button.visible:
                            handle_button_click(word)
        
        if not game_over:
            if not audio_playing:
                play_audio()
            elif not pygame.mixer.get_busy() and not buttons_visible:
                show_buttons()
        
        draw_game()
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()


doglearning_main_game_loop()