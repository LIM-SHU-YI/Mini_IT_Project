import pygame
from button import Button
import common

pygame.init()

# settings for the window of the game
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load("asset/image/gameicon.png")
pygame.display.set_caption("Memories")
pygame.display.set_icon(icon)

menu_background = pygame.image.load("asset/image/start.png")
# game tittle
(Mshadow, Mshadow_rect), (Memories, Memories_rect) = common.text_with_shadow("Memories", common.storytella(180), "Black", "White", (630, 145))

# buttons for main interface
play = Button(1070, 330, text_input="Play", font=common.cutedisplay(45), base_color="White", hovering_color="Grey", shadow_offset=(4, 4))
credit = Button(1070, 410, text_input="Credit", font=common.cutedisplay(45), base_color="White", hovering_color="Grey", shadow_offset=(4, 4))
quit = Button(1070, 495, text_input="Quit", font=common.cutedisplay(45), base_color="White", hovering_color="Grey", shadow_offset=(4, 4))

def main_interface(event):
    # print menu background and game tittle
    screen.blit(menu_background, (0, 0))
    screen.blit(Mshadow, Mshadow_rect)
    screen.blit(Memories, Memories_rect)

    if event.type == pygame.MOUSEBUTTONDOWN:
        if play.checkforinput(pygame.mouse.get_pos()):
            common.click.play()
            # added time delay so click sfx can play before executing the next command
            pygame.time.delay(250)
            # Game first scene not done yet below will be try and prerun codes that are not related to the final game
            common.current_scene = "first_scene"

        elif credit.checkforinput(pygame.mouse.get_pos()):
            common.click.play()
            pygame.time.delay(250)
            common.current_scene = "credit"

        elif quit.checkforinput(pygame.mouse.get_pos()):
            common.click.play()
            pygame.time.delay(250)
            common.running = False  # if False then program closes
            return      # returning to main loop
        
        if common.music_button.visible and common.music_button.checkforinput(pygame.mouse.get_pos()):
            common.click.play()
            common.music_on_off()
        elif common.mute_button.visible and common.mute_button.checkforinput(pygame.mouse.get_pos()):
            common.click.play()
            common.music_on_off()

    # show on screen buttons cannot use blit
    play.update(screen)
    credit.update(screen)
    quit.update(screen)

    if common.music_button.visible:
        common.music_button.update(screen)
    if common.mute_button.visible:
        common.mute_button.update(screen)

    pygame.display.flip()


# main loop of the game
while common.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            common.running = False
            break

        if common.current_scene == "main_menu":
            main_interface(event)

        elif common.current_scene == "first_scene":
            from second import first_scene
            first_scene(event)

        elif common.current_scene == "credit":
            from credit import credits
            credits(event)

    pygame.display.flip()

pygame.quit()