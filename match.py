import pygame
import sys
import common
from button import Button
from drag_game import DragGame
from emotion_game import EmotionGame

# Define screen size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Memories")
icon = pygame.image.load("asset/image/gameicon.png")
pygame.display.set_icon(icon)

# Images
interface_bg = pygame.image.load("Photo used/Match/interfaceview.png")
kidsinter_img = pygame.image.load("Photo used/Match/kidsinter.png")
kids_img = pygame.image.load("Photo used/Match/kids.png")
boyfriendinter_img = pygame.image.load("Photo used/Match/boyfriendinter.png")
boyfriend_img = pygame.image.load("Photo used/Match/boyfriend.png")
dogownerinter_img = pygame.image.load("Photo used/Match/dogownerinter.png")
dogowner_img = pygame.image.load("Photo used/Match/dogowner.png")

# Gallery buttons
kidsinter_btn = Button(260, 245, image=kidsinter_img)
boyfriendinter_btn = Button(646, 236, image=boyfriendinter_img)
dogownerinter_btn = Button(1040, 236, image=dogownerinter_img)

back_btn = Button(50, 50, text_input="BACK", font=common.arcade(30), base_color="Black", hovering_color="Gray")

# Game states
MAIN_MENU, KIDS_VIEW, BOYFRIEND_VIEW, DOGOWNER_VIEW, DRAG_GAME, EMOTION_GAME, FINAL_RESULT = range(7)

current_state = MAIN_MENU

# Initialize games
drag_game = DragGame(screen)
emotion_game = EmotionGame(screen)

def draw_main_menu():
    screen.blit(interface_bg, (0, 0))
    if not drag_game.all_items_placed:
        drag_game.start_btn.update(screen)
    kidsinter_btn.update(screen)
    boyfriendinter_btn.update(screen)
    dogownerinter_btn.update(screen)
    if drag_game.all_items_placed:
        emotion_game.draw_emotion_buttons(screen)

def draw_view(image):
    screen.blit(image, (0, 0))
    back_btn.update(screen)

def draw_final_result():
    screen.fill((255, 255, 255))
    result_text, result_rect = common.normal_text("You already learn human emotion", common.arcade(50), (0, 0, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(result_text, result_rect)
    back_btn.update(screen)

def match_main():
    global current_state

    clock = pygame.time.Clock()
    running = True

    while running:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_state == MAIN_MENU:
                    if drag_game.start_btn.checkforinput(event.pos) and not drag_game.all_items_placed:
                        current_state = DRAG_GAME
                        drag_game.reset()
                    elif kidsinter_btn.checkforinput(event.pos):
                        current_state = KIDS_VIEW
                    elif boyfriendinter_btn.checkforinput(event.pos):
                        current_state = BOYFRIEND_VIEW
                    elif dogownerinter_btn.checkforinput(event.pos):
                        current_state = DOGOWNER_VIEW
                    elif drag_game.all_items_placed:
                        emotion_clicked = emotion_game.check_emotion_button_click(event.pos)
                        if emotion_clicked:
                            current_state = EMOTION_GAME
                            emotion_game.reset()
                elif current_state in [KIDS_VIEW, BOYFRIEND_VIEW, DOGOWNER_VIEW]:
                    if back_btn.checkforinput(event.pos):
                        current_state = MAIN_MENU

        if current_state == MAIN_MENU:
            draw_main_menu()
        elif current_state == KIDS_VIEW:
            draw_view(kids_img)
        elif current_state == BOYFRIEND_VIEW:
            draw_view(boyfriend_img)
        elif current_state == DOGOWNER_VIEW:
            draw_view(dogowner_img)
        elif current_state == DRAG_GAME:
            drag_game_result = drag_game.update(event_list)
            if drag_game_result == "MAIN_MENU":
                current_state = MAIN_MENU
        elif current_state == EMOTION_GAME:
            emotion_game_result = emotion_game.update(event_list)
            if emotion_game_result == "MAIN_MENU":
                current_state = MAIN_MENU
            elif emotion_game_result == "FINAL_RESULT":
                current_state = FINAL_RESULT
        elif current_state == FINAL_RESULT:
            draw_final_result()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    import sys
    sys.exit()

if __name__ == "__main__":
    match_main()