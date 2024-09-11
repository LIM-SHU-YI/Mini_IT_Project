import pygame
import common
from button import Button
from bag import bag
from puzzle import puzzle
from bone import bone
from diary import diary

# settings for the window of the game
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load("asset/image/gameicon.png")
pygame.display.set_caption("Memories")
pygame.display.set_icon(icon)


# Load images
background = pygame.image.load("asset/image/interimg/background.png")
boneb = pygame.image.load("asset/image/interimg/boneb.png")
bookb = pygame.image.load("asset/image/interimg/bookb.png")
picb = pygame.image.load("asset/image/interimg/picbutton.png")

picb = pygame.transform.scale(picb, (96, 113))

boneb_1 = Button(195,355, image=boneb)
bookb_1 = Button(982,408, image=bookb)
picb_1 = Button(640,290, image=picb)

completed_games = {
    "diary": False,
    "puzzle": False,
    "bone": False
}

def book():
    diary()
    completed_games["diary"] = True

def puzz():

    puzzle()  # Play the puzzle game
    completed_games["puzzle"] = True

def bonegame():
    bone()
    completed_games["bone"] = True

def bags():
    bag()

def kitinterface():
    global game_completed
    game_completed =  False
    clock = pygame.time.Clock()
    common.running = True
    mainroom = True

    while common.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if common.music_button.visible and common.music_button.checkforinput(pygame.mouse.get_pos()):
                    common.click.play()
                    common.music_on_off()
                elif common.mute_button.visible and common.mute_button.checkforinput(pygame.mouse.get_pos()):
                    common.click.play()
                    common.music_on_off()

        if mainroom:
            # common.running = True
            while common.running:
                screen.blit(background, (0,0))
                boneb_1.update(screen)
                bookb_1.update(screen)
                picb_1.update(screen)

                if common.music_button.visible:
                    common.music_button.update(screen)  # Update music button
                if common.mute_button.visible:
                    common.mute_button.update(screen)

                pygame.display.flip()
                clock.tick(60)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        common.running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if boneb_1.checkforinput(pygame.mouse.get_pos()):
                                common.click.play()
                                bonegame()

                            if bookb_1.checkforinput(pygame.mouse.get_pos()):
                                common.click.play()
                                book()

                            if picb_1.checkforinput(pygame.mouse.get_pos()):
                                common.click.play()
                                puzz()

                        if common.music_button.visible and common.music_button.checkforinput(pygame.mouse.get_pos()):
                            common.click.play()
                            common.music_on_off()
                        elif common.mute_button.visible and common.mute_button.checkforinput(pygame.mouse.get_pos()):
                            common.click.play()
                            common.music_on_off()

                if completed_games["diary"] and completed_games["puzzle"] and completed_games["bone"]:
                    bags()              # call bag.py when all games are done

        if game_completed:
            break

    pygame.quit()

# ONLY FOR DEBUGG!!! DO NOT RUN THIS WHEN RUN FROM MAINNNN!!!
while common.running:
    kitinterface()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            common.running = False
            break