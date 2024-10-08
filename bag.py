import pygame
def bag():
    import pygame 
    import sys
    import common
    from button import Button
    from running import running_race_game

    pygame.init()

    width=1280
    height=720
    screen=pygame.display.set_mode((width,height))
    pygame.display.set_caption('Memories')

    Black=(0,0,0)
    White=(255,255,255)

    background=pygame.image.load('kitasset/bagasset/5.png')
    bag=pygame.image.load('kitasset/bagasset/1.png')
    item1=pygame.image.load('kitasset/bagasset/2.png')
    item2=pygame.image.load('kitasset/bagasset/3.png')
    item3=pygame.image.load('kitasset/bagasset/4.png')

    bag=pygame.transform.scale(bag,(450,300))
    item1=pygame.transform.scale(item1,(200,200))
    item2=pygame.transform.scale(item2,(300,200))
    item3=pygame.transform.scale(item3,(250,250))
    return_img = pygame.image.load("asset/image/return.png")
    return_button = Button(50, 50, image=return_img, scale=0.27)


    class item(pygame.sprite.Sprite):
        def __init__(self,image,pos,rectsize):
            super().__init__()
            self.image=image
            self.rect=self.image.get_rect(topleft=pos)
            self.transparent_rect=pygame.Rect(self.rect.x+10,self.rect.y +10,rectsize[0]-20,rectsize[1]-20)
            self.dragging=False

        def update(self):
            if self.dragging:
                mousex,mousey=pygame.mouse.get_pos()
                newx=min(max(mousex,self.rect.width//2),width-self.rect.width//2)
                newy=min(max(mousey,self.rect.height//2),height-self.rect.height//2)
                self.rect.center=(newx,newy)
                self.transparent_rect.center=self.rect.center

    item1=item(item1,(600,150),(1,1))
    item2=item(item2,(100,150),(1,1))
    item3=item(item3,(800,150),(1,1))
    items=pygame.sprite.Group(item1,item2,item3)

    bagrect=bag.get_rect(center=(width//2,height-150))
    smallbagrect=bagrect.inflate(-200,-150)
    smallbagrect.center=bagrect.center

    itemdragged=None

    font=pygame.font.Font('kitasset/bagasset/font.ttf',74)
    instructionfont=pygame.font.Font('kitasset/bagasset/font.ttf',50)

    running=True
    while running:
        screen.fill(Black)
        screen.blit(background,(0,0))

        instructiontext=instructionfont.render("Put all the items in the bag",True,Black)
        instructionrect=instructiontext.get_rect(center=(width//2,50))
        screen.blit(instructiontext,instructionrect)
        for item in items:
            screen.blit(item.image,item.rect)
        screen.blit(bag,bagrect.topleft)

        for item in items:
            if item.dragging:
                screen.blit(item.image,item.rect) 

        for interaction in pygame.event.get():
            if interaction.type==pygame.QUIT:
                running=False
            elif interaction.type==pygame.MOUSEBUTTONDOWN:
                if itemdragged is None:
                    for item in items:
                        if item.rect.collidepoint(interaction.pos):
                            item.dragging=True
                            itemdragged=item

                if common.music_button.visible and common.music_button.checkforinput(pygame.mouse.get_pos()):
                    common.click.play()
                    common.music_on_off()
                elif common.mute_button.visible and common.mute_button.checkforinput(pygame.mouse.get_pos()):
                    common.click.play()
                    common.music_on_off()

            elif interaction.type==pygame.MOUSEBUTTONUP:
                if itemdragged:
                    itemdragged.dragging=False
                    if itemdragged.transparent_rect.colliderect(smallbagrect):
                        itemdragged.kill()
                    itemdragged=None
        items.update()

        if len(items)==0:
            screen.fill(Black)
            captiontext=font.render("Lets's start our journey!",True,White)
            captionrect=captiontext.get_rect(center=(width//2,height//2))
            screen.blit(captiontext,captionrect)
            pygame.display.flip()
            stop_scene = True
            while stop_scene:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        stop_scene = False  # Allow the game to quit
                        running = False  # Signal to stop the main loop
                pygame.time.wait(1000)
                running_race_game()
                running=False

            # pygame.time.wait(3000)
            # running=False

        if common.music_button.visible:
            common.music_button.update(screen)
        if common.mute_button.visible:
            common.mute_button.update(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# debug
# running=True
# while running:
#     bag()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#             break
