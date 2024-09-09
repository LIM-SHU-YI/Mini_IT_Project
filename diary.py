import pygame
game_completed = False

def diary():
    global game_completed
    import pygame
    import sys
    from button import Button
    import common

    pygame.init()

    screen=pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Memories")

    white=(255,255,255)
    black=(0,0,0)

    font=pygame.font.Font('diarypic/font.ttf',36)
    bgd=pygame.image.load('diarypic/3.png')
    bgd=pygame.transform.scale(bgd,(1280,720))

    diaryimg=pygame.image.load('diarypic/1.png')
    diaryimg=pygame.transform.scale(diaryimg,(400,400))
    diaryrect=diaryimg.get_rect(center=(640,360))

    first=pygame.image.load('diarypic/2.png')
    first=pygame.transform.scale(first,(1280,720))
    firstrect=first.get_rect(topleft=(0,0))

    return_img = pygame.image.load("asset/image/return.png")
    return_button = Button(50, 50, image=return_img, scale=0.27)   

    showdiary=True
    showfirst=False
    showmsg=False

    diarytext="""5May
    Today, I found out I'll be going to Kyoto \nfor a business trip from 13 May to 25 July. 
    It's a great opportunity, \nbut I'm really concerned about my dog. 
    I need to figure out how to make sure he's well cared for while I'm away. 
    The thought of leaving him behind is tough,\n but I have to find a good solution soon."""

    game_is_done = False

    def displaybgd():
        screen.blit(bgd,(0,0))

    def displaydiary():
        displaybgd()
        screen.blit(diaryimg,diaryrect.topleft)
        instruction=font.render("Click to continue",True,black)
        screen.blit(instruction,(640-instruction.get_width()//2,680))

    def displayfirst():
        displaybgd()
        screen.blit(first,firstrect.topleft)
        instruction=font.render("Click to continue",True,black)
        screen.blit(instruction,(640-instruction.get_width()//2,680))

    def displaymsg():
        screen.fill(black)
        lines=diarytext.split('\n')
        for i,line in enumerate(lines):
            text=font.render(line,True,white)
            screen.blit(text,(640-text.get_width()//2,200+i*40))

    while not game_completed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if showdiary and diaryrect.collidepoint(event.pos):
                    showdiary=False
                    showfirst=True
                elif showfirst and firstrect.collidepoint(event.pos):
                    showfirst=False
                    showmsg=True
        if showdiary:
            displaydiary()
        elif showfirst:
            displayfirst()
        elif showmsg:
            displaymsg()
            # game_is_done = True 
            return_button.update(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.checkforinput(pygame.mouse.get_pos()):
                    common.click.play()
                    game_is_done = True 
                
        pygame.display.flip()
        if game_is_done:  # This condition should be defined by your game logic
            game_completed = True
            break

# # debug
# running=True
# while running:
#     diary()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#             break
