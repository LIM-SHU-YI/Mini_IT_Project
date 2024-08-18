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

sec_background = pygame.image.load("asset/image/test.jpg")

testing = Button(650,430,text_input="Deep Memories", font=common.monera(80), base_color="black",hovering_color="grey", shadow_on=False)


def first_scene(event):

    screen.blit(sec_background, (0,0))
    
    
    if event.type == pygame.QUIT:
        common.running = False  # Quit the game
        return  # return to main loop
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        if testing.checkforinput(pygame.mouse.get_pos()):
            common.click.play()

        if common.music_button.visible and common.music_button.checkforinput(pygame.mouse.get_pos()):
            common.click.play()
            common.music_on_off()
        elif common.mute_button.visible and common.mute_button.checkforinput(pygame.mouse.get_pos()):
            common.click.play()
            common.music_on_off()

    
    testing.update(screen)

    if common.music_button.visible:
        common.music_button.update(screen)
    if common.mute_button.visible:
        common.mute_button.update(screen)

    pygame.display.flip()


# # fast testrun
# common.running = True
# while common.running:
#     for event in pygame.event.get():
#         first_scene(event)

# pygame.quit()