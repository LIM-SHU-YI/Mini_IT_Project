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
firstimg = pygame.image.load("kitasset/part2/1.png")
secondimg = pygame.image.load("kitasset/part2/2.png")
blackscreen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
blackscreen.fill((0, 0, 0))

picb = pygame.transform.scale(picb, (96, 113))

boneb_1 = Button(195,355, image=boneb)
bookb_1 = Button(982,408, image=bookb)
picb_1 = Button(640,290, image=picb)
firstimg = pygame.transform.scale(firstimg, (SCREEN_WIDTH, SCREEN_HEIGHT))
secondimg = pygame.transform.scale(secondimg, (SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

completed_games = {
    "diary": False,
    "puzzle": False,
    "bone": False
}

font = pygame.font.Font("kitasset/part2/font.ttf", 30)

storytext1= (
    "July 13th\n"
    "The owner left early for a business trip, \nthe door closing softly behind them.\n\n "
    "The dogs sat by the door, eyes filled with hope,\nwaiting for their return.\n\n"
    "Days passed, and they stayed at the door,\nlistening for footsteps that never came. "
    "Each evening, bathed in the golden light of sunset,\n they remained there ears perked,\n"
    "hearts waiting hoping that any moment,\nthe door would open again.\n\n"
    "But the owner never came back."
)

storytext2 = (
    "After six long months of waiting, \nHachi could no longer endure the loneliness.\n"
    "His owner hadn’t returned, \nand something deep inside told him it was time to act.\n\n"
    "Hachi stood up from his familiar spot at the station and made a bold choice\n"
    "he would find his owner himself. \nWith determination in his eyes and hope in his heart,\n"
    "Hachi set off on a journey into the unknown."
)

def fadeinout(screen,image,duration=1500,fadetype='in'):
    starttime=pygame.time.get.ticks()
    fadeduration=duration
    alpha=0 if fadetype =='in' else 255
    while True:
        elapsedtime=pygame.time.get_ticks()-starttime
        if elapsedtime >= fadeduration:
            break

        if fadetype=='in':
            alpha=min(255,(elapsedtime/fadeduration)*255)

        else:
            alpha=max(0,255-(elapsedtime/fadeduration)*255)
        
        image.set_alphha(alpha)
        screen.blit(image(0,0))
        pygame.display.flip()
        clock.tick(60)

def drawtext(screen,text,font,colour,x,y):
    lines=text.split('\n')
    for i,line in enumerate(lines):
        renderedtext=font.render(line,True,colour)
        screen.blit(renderedtext,(x,y+i*renderedtext.get_height()))

def displaystory():
    starttime=pygame.time.get_ticks()
    displayduration=20000

    while True:
        elapsedtime=pygame.time.get_ticks()-starttime
        screen.fill((0,0,0))
        drawtext(screen,storytext1,font,(255,255,255),50,50)
        pygame.display.flip()

        if elapsedtime >= displayduration:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common.running=False
                return
        clock.tick(60)
def displaystory2():
    starttime=pygame.time.get_ticks()
    displayduration=20000

    while True:
        elapsedtime=pygame.time.get_ticks()-starttime
        screen.fill((0,0,0))
        drawtext(screen,storytext2,font,(255,255,255),50,50)
        pygame.display.flip()

        if elapsedtime >= displayduration:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common.running=False
                return
        clock.tick(60)
def fadetransition(screen,img1,img2,duration=10000):
    starttime=pygame.time.get_ticks()
    fadeduration=duration
    while True:
        elapsedtime=pygame.time.get_ticks()-starttime
        alpha=(elapsedtime/fadeduration)*255
        img1copy=img1.copy()
        img2copy=img2.copy()
        img1copy.set_alpha(255-int(alpha))
        img2copy.set_alpha(int(alpha))
        screen.fill((0,0,0))
        screen.blit(img1copy,(0,0))
        screen.blit(img2copy,(0,0))
        pygame.display.flip()

        if elapsedtime >= fadeduration:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common.running=False
                return
        clock.tick(60)

def infront():
    displaystory()
    fadetransition(screen,firstimg,secondimg,duration=3000)
    displaystory2()

def checkmdone():
    return all(completed_games.values())

def run_minigames(minigame):
    if completed_games[minigame]:
        print(f"{minigame} is already completed. You cannot play it again.")
        return
    if minigame == "diary":
        diary()
        completed_games["diary"] = True
    if minigame == "puzzle":
        puzzle()
        completed_games["puzzle"] = True
    if minigame == "bone":
        bone()
        completed_games["bone"] = True

    if checkmdone():
        bags()      # call bag.py when all games are done

def bags():
    bag()

def kitinterface():
    infront()
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
                                # bonegame()
                                run_minigames("bone")

                            if bookb_1.checkforinput(pygame.mouse.get_pos()):
                                common.click.play()
                                # book()
                                run_minigames("diary")

                            if picb_1.checkforinput(pygame.mouse.get_pos()):
                                common.click.play()
                                # puzz()
                                run_minigames("puzzle")

                        if common.music_button.visible and common.music_button.checkforinput(pygame.mouse.get_pos()):
                            common.click.play()
                            common.music_on_off()
                        elif common.mute_button.visible and common.mute_button.checkforinput(pygame.mouse.get_pos()):
                            common.click.play()
                            common.music_on_off()

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