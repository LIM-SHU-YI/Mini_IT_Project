import pygame
def bone():
    import pygame
    import sys
    import random
    from button import Button
    import common

    pygame.init()

    fpsclock = pygame.time.Clock()
    width=1280
    height=720
    screen=pygame.display.set_mode((width,height))
    pygame.display.set_caption("Memories")

    white=(255,255,255)
    black=(0,0,0)
    grey=(64,64,64)

    image=["kitasset/boneimg/1.png", "kitasset/boneimg/2.png", "kitasset/boneimg/3.png"]
    scenes=[pygame.image.load(image).convert()for image in image]
    currentscene=0
    scenes=[pygame.transform.scale(scene,(width,height))for scene in scenes]

    buttonimg="kitasset/boneimg/4.png"
    buttonsize=(120,120)
    button=pygame.image.load(buttonimg).convert_alpha()
    button=pygame.transform.scale(button,buttonsize)
    
    return_img = pygame.image.load("asset/image/return.png")
    return_button = Button(50, 50, image=return_img, scale=0.27)   
    game_is_done = False            #added to return back to threeinter
    wingame = False            #added to check game win or no


    fontttf="kitasset/boneimg/font.ttf"
    fontsize=72
    font=pygame.font.Font(fontttf,fontsize)

    smallsize=36
    small=pygame.font.Font(fontttf,smallsize)

    starttime=pygame.time.get_ticks()
    timelimit=1*60*1000+1*1000
    # timelimit=10*1000     # change time when use for debug


    hitcircle=[]
    spawninterval=700
    lastspawntime=starttime
    shrinkduration=700

    score=0

    def randomposition():
        x=random.randint(0,width-buttonsize[0])
        y=random.randint(0,height-buttonsize[1])
        return x,y
    def spawnhitcircle():
        buttonx, buttony = randomposition()
        buttonrect = pygame.Rect(buttonx, buttony, *buttonsize)
        buttoncenter = buttonrect.center
        radius = max(buttonsize)
        detectradius = radius
        hitcircle.append({
            'rect': buttonrect,
            'center': buttoncenter,
            'spawntime': pygame.time.get_ticks(),
            'clicked': False,
            'radius': radius,
            'detectradius': detectradius
        })

    running=True
    gameover=False

    while running:
        currenttime=pygame.time.get_ticks()
        elapsedtime=currenttime-starttime
        remainingtime=timelimit-elapsedtime
        

        if not gameover:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running=False
                    pygame.quit()
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    if common.music_button.visible and common.music_button.checkforinput(pygame.mouse.get_pos()):
                        common.click.play()
                        common.music_on_off()
                    elif common.mute_button.visible and common.mute_button.checkforinput(pygame.mouse.get_pos()):
                        common.click.play()
                        common.music_on_off()

                    for circle in hitcircle:
                        if not circle['clicked']:
                            distance = (event.pos[0] - circle['center'][0]) ** 2 + (event.pos[1] - circle['center'][1]) ** 2
                            if distance <= circle['detectradius'] ** 2:
                                circle["clicked"]=True
                                clicktime=pygame.time.get_ticks()
                                timediff=clicktime-circle['spawntime']

                                if abs(timediff)<= 100:
                                    score+=300
                                elif abs (timediff)<+ 200:
                                    score+= 100
                                elif abs(timediff)<= 300:
                                    score +=50
                                else:
                                    score+=10

                                if score>= 40 and score%40 ==0:
                                # if score>= 10 and score%10 ==0:           # change clicks when debug time to switch scenes
                                    if currentscene < len(scenes)-1:
                                        currentscene += 1
                                    else:
                                        gameover=True
            if currenttime-lastspawntime>=spawninterval and not gameover:
                spawnhitcircle()
                lastspawntime=currenttime
        
            screen.blit(scenes[currentscene],(0,0))

            for circle in hitcircle:
                if not circle['clicked']:
                    spawntimediff=currenttime-circle['spawntime']
                    shrinkradius=max(10,circle['radius']-spawntimediff//10)

                    if spawntimediff>= shrinkduration:
                        circle['clicked']=True
                    else:
                        pygame.draw.circle(screen,grey,circle['center'],shrinkradius,3)
                        buttonrect=button.get_rect(center=circle['center'])
                        screen.blit(button,buttonrect.topleft)


            (clicksha, clicksha_rect), (click, click_rect) = common.text_with_shadow("Click the circles in time!", common.cutedisplay(50), "Black", "White", (640, 50), shadow_offset=(4, 5))
            screen.blit(clicksha, clicksha_rect)
            screen.blit(click, click_rect)
            
            minutes=remainingtime//60000
            seconds=(remainingtime%60000)//1000
            (timesha, timesha_rect), (time, time_rect) = common.text_with_shadow(f"Time: {minutes:01}:{seconds:02}", common.cutedisplay(36), "Black", "White", (1185, 120), shadow_offset=(4, 5))
            screen.blit(timesha, timesha_rect)
            screen.blit(time, time_rect)

            if common.music_button.visible:
                common.music_button.update(screen)
            if common.mute_button.visible:
                common.mute_button.update(screen)


            if remainingtime <= 0 or gameover:
                gameover = True
            pygame.display.flip()


        else:
            screen.fill(black)
            if score>=120:
            # if score>=10:            # change total score when debug
                result= "You found your favourite bone!"
                wingame = True

            else:
                result= "You lost your bone!"
                wingame = False
            
            if wingame:
                resultrender=font.render(result,True,(white))
                screen.blit(resultrender,((width-resultrender.get_width())//2,(height-resultrender.get_height())//2))
                return_button.update(screen)
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if return_button.checkforinput(pygame.mouse.get_pos()):
                                common.click.play()
                                game_is_done = True
            else:
                resultrender=font.render(result,True,(white))
                screen.blit(resultrender,((width-resultrender.get_width())//2,(height-resultrender.get_height())//2))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
        
        pygame.display.flip()
        fpsclock.tick(60)


        if game_is_done: 
            return


# debug
# running=True
# while running:
#     bone()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#             break