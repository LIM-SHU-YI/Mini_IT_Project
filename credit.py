import pygame
from button import Button
import common

# settings for the window of the game
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load("asset/image/gameicon.png")
pygame.display.set_caption("Memories")
pygame.display.set_icon(icon)

credit_background = pygame.image.load("asset/image/creditimg.png")

# back to menu img and button
return_img = pygame.image.load("asset/image/return.png")
return_button = Button(50, 50, image=return_img, scale=0.27)


def credits(event):
    screen.blit(credit_background, (0, 0))
    if event.type == pygame.QUIT:
        common.running = False  # Quit the game
        return  # return to main loop
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        if return_button.checkforinput(pygame.mouse.get_pos()):
            common.click.play()
            pygame.time.delay(250)
            common.current_scene = "main_menu"  # Go back to main menu

            if common.music_button.visible and common.music_button.checkforinput(pygame.mouse.get_pos()):
                common.click.play()
                common.music_on_off()
            elif common.mute_button.visible and common.mute_button.checkforinput(pygame.mouse.get_pos()):
                common.click.play()
                common.music_on_off()

    return_button.update(screen)

    if common.music_button.visible:
        common.music_button.update(screen)
    if common.mute_button.visible:
        common.mute_button.update(screen)

    pygame.display.flip()



# # fast testrun
# common.running = True
# while common.running:
#     for event in pygame.event.get():
#         credits(event)

# pygame.quit()