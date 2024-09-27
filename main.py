import pygame
from button import Button
import common
import logging

# Clear the log file at the start
open('error_log.txt', 'w').close()

# Configure logging
logging.basicConfig(
    filename='error_log.txt',  # Log file to store messages
    level=logging.ERROR,        # Log only error messages and above
    format='%(asctime)s - %(levelname)s - %(message)s'  # Format of log messages
)

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

def main_interface():
    # print menu background and game tittle
    screen.blit(menu_background, (0, 0))
    screen.blit(Mshadow, Mshadow_rect)
    screen.blit(Memories, Memories_rect)

    # show on screen buttons cannot use blit
    play.update(screen)
    credit.update(screen)
    quit.update(screen)

    if common.music_button.visible:
        common.music_button.update(screen)
    if common.mute_button.visible:
        common.mute_button.update(screen)

# main loop of the game
clock = pygame.time.Clock()
FPS = 60  # Set desired frame rate

try:
    while common.running:
        clock.tick(FPS)  # Limit the frame rate
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common.running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if common.current_scene == "main_menu":
                    if play.checkforinput(pygame.mouse.get_pos()):
                        common.click.play()
                        pygame.time.delay(250)
                        common.current_scene = "first_scene"
                    elif credit.checkforinput(pygame.mouse.get_pos()):
                        common.click.play()
                        pygame.time.delay(250)
                        common.current_scene = "credit"
                    elif quit.checkforinput(pygame.mouse.get_pos()):
                        common.click.play()
                        pygame.time.delay(250)
                        common.running = False
                        break
                
                if common.music_button.visible and common.music_button.checkforinput(pygame.mouse.get_pos()):
                    common.click.play()
                    common.music_on_off()
                elif common.mute_button.visible and common.mute_button.checkforinput(pygame.mouse.get_pos()):
                    common.click.play()
                    common.music_on_off()

        # Update and draw the current scene
        if common.current_scene == "main_menu":
            main_interface()
        elif common.current_scene == "first_scene":
            from part1 import first_scene
            first_scene()
        elif common.current_scene == "credit":
            from credit import credits
            credits(event)

        pygame.display.flip()

except Exception as e:
    # Log the exception with traceback
    logging.error("An exception occurred", exc_info=True)
    print("Oops! Something went wrong. Please check error_log.txt for details.")
finally:
    pygame.quit()