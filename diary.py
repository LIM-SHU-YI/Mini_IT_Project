import pygame
import math
import common
from button import Button

game_complete = False

def diary():
    global game_complete
    pygame.init()

    width,height=1280, 720
    screen=pygame.display.set_mode((width,height))
    pygame.display.set_caption("Memories")

    white=(255, 255, 255)
    black=(0, 0, 0)

    diaryimg=pygame.image.load("kitasset/diarypic/1.png")
    paperimg=pygame.image.load("kitasset/diarypic/2.png")
    backgroundimg=pygame.image.load("kitasset/diarypic/3.png")
    pencilimg=pygame.image.load("kitasset/diarypic/6.png")
    roombgd=pygame.image.load("kitasset/diarypic/4.png") 

    backgroundimg=pygame.transform.scale(backgroundimg,(600,500)) 
    paperimg=pygame.transform.scale(paperimg,(600,500)) 
    pencilimg=pygame.transform.scale(pencilimg,(50,50)) 

    return_img = pygame.image.load("asset/image/return.png")
    return_button = Button(50, 50, image=return_img, scale=0.27) 

    diaryrect=diaryimg.get_rect(center=(width//2,height//2))
    backgroundrect=backgroundimg.get_rect(center=diaryrect.center) 
    erasablearea=pygame.Rect(diaryrect.centerx-backgroundrect.width//2,diaryrect.top,backgroundrect.width,backgroundrect.height) 
    righterasablearea=pygame.Rect(erasablearea.right-erasablearea.width//2,erasablearea.top,erasablearea.width//2,erasablearea.height)  # Only right side is erasable
    pencilrect=pencilimg.get_rect()
    pencilrect.topleft=(100,100)

    # Variables
    scene=1
    erasablemask=paperimg.copy()  
    erasedarea=0
    showmsg=False
    showinstruction=True  
    fpsclock=pygame.time.Clock()

    # Fonts and text
    font=pygame.font.Font("kitasset/diarypic/font.ttf", 35)  
    msg="""5 May\n\nToday, I found out I'll be going to Kyoto for a business trip \n from 13 May to 25 July. 
    It's a great opportunity,\n but I'm really concerned about my dog. 
    I need to figure out how to make sure\n he's well cared for while I'm away. 
    The thought of leaving him behind is tough,\n but I have to find a good solution soon."""
    instruction="Use the pencil to find something"

    def checkerase(erasablearea, erasablemask):
        """ Calculate how much area is erased by checking pixel transparency using get_at """
        erasedarea=0
        totalarea=righterasablearea.width*righterasablearea.height
        
        for x in range(righterasablearea.width):
            for y in range(righterasablearea.height):
                localx=righterasablearea.x-erasablearea.x+x
                localy=righterasablearea.y-erasablearea.y+y
                if 0<=localx < erasablemask.get_width() and 0<= localy < erasablemask.get_height():
                    if erasablemask.get_at((localx, localy))[3]==0:
                        erasedarea+=1

        percenterased=(erasedarea/totalarea)*100
        # print(f"Erased Area:{percenterased}%") 
        return percenterased 

    def drawscene1():
        screen.blit(roombgd,(0, 0))
        screen.blit(diaryimg,diaryrect)

        if showinstruction:
            renderinstruction()

    def drawscene2():
        screen.blit(roombgd,(0,0))
        screen.blit(backgroundimg,backgroundrect.topleft) 
        screen.blit(erasablemask,backgroundrect.topleft)  
        screen.blit(pencilimg,pencilrect.topleft) 

        if showmsg:
            rendermsg()

    def rendermsg():
        screen.fill(black) 
        msglines=msg.split("\n")
        yoffset=100
        for line in msglines:
            msgsurface=font.render(line,True,white)
            screen.blit(msgsurface,(100,yoffset))
            yoffset+=50

    def renderinstruction():
        instructionsurface=font.render(instruction,True,black)
        screen.blit(instructionsurface,(width//2-instructionsurface.get_width()//2,50))

    def eraseline(startpos,endpos,brushsize=30):
        """ Erase along the line between start_pos and end_pos """
        distance=math.hypot(endpos[0]-startpos[0],endpos[1]-startpos[1])
        if distance==0:
            return

        for i in range(int(distance)):
            lerpx=int(startpos[0]+(endpos[0]-startpos[0])*i/distance)
            lerpy=int(startpos[1]+(endpos[1]-startpos[1])*i/distance)
            erase((lerpx,lerpy),brushsize)

    def erase(pencilpos,brushsize=30):
        """ Erase the area at the pencil position """
        if righterasablearea.collidepoint(pencilpos):
            pygame.draw.circle(erasablemask,(0, 0, 0, 0),(pencilpos[0]-backgroundrect.x,pencilpos[1]-backgroundrect.y),brushsize)


    def updatem():
        if common.music_button.visible:
            common.music_button.update(screen)
        if common.mute_button.visible:
            common.mute_button.update(screen)


    running=True
    pencilactive=False
    lastpos=None
    game_is_done = False

    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                pygame.quit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                mousepos=pygame.mouse.get_pos()
                if scene==1 and diaryrect.collidepoint(mousepos):
                    scene=2
                    showinstruction=False 
                if scene==2 and pencilrect.collidepoint(mousepos):
                    pencilactive=True
                    lastpos=mousepos

                if common.music_button.visible and common.music_button.checkforinput(pygame.mouse.get_pos()):
                    common.click.play()
                    common.music_on_off()
                elif common.mute_button.visible and common.mute_button.checkforinput(pygame.mouse.get_pos()):
                    common.click.play()
                    common.music_on_off()

                
            if event.type==pygame.MOUSEBUTTONUP:
                pencilactive=False
                lastpos=None


        if pencilactive:
            mousepos=pygame.mouse.get_pos()
            pencilrect.center=mousepos
            if lastpos:
                eraseline(lastpos,mousepos)
                lastpos=mousepos

        # draw scene
        if scene==1:
            drawscene1()  
        elif scene==2:
            drawscene2() 
            erasedarea=checkerase(erasablearea,erasablemask)
            if erasedarea>=83:
                showmsg=True
                # print("83% erased! Showing message...")  
        updatem()

        if showmsg:
            return_button.update(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if return_button.checkforinput(pygame.mouse.get_pos()):
                        common.click.play()
                        game_is_done = True
                    if common.music_button.visible and common.music_button.checkforinput(pygame.mouse.get_pos()):
                        common.click.play()
                        common.music_on_off()
                    elif common.mute_button.visible and common.mute_button.checkforinput(pygame.mouse.get_pos()):
                        common.click.play()
                        common.music_on_off()


        pygame.display.flip()  # Update display
        fpsclock.tick(60)  # Limit FPS

        if game_is_done:
            game_complete = True  # Mark the game as completed
            return
        
# debug
# running = True
# while running:
#     diary()

#     # Check if the game is complete
#     if game_complete:
#         running = False  

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#             break