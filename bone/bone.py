import pygame
def bone():
    import pygame
    import sys
    import random

    pygame.init()

    width=1280
    height=720
    screen=pygame.display.set_mode((width,height))
    pygame.display.set_caption("Bone Game")

    white=(255,255,255)
    black=(0,0,0)
    grey=(64,64,64)

    image=["bone/boneimg/1.png", "bone/boneimg/2.png", "bone/boneimg/3.png"]
    scenes=[pygame.image.load(image).convert()for image in image]
    currentscene=0
    scenes=[pygame.transform.scale(scene,(width,height))for scene in scenes]

    buttonimg="bone/boneimg/4.png"
    buttonsize=(120,120)
    button=pygame.image.load(buttonimg).convert_alpha()
    button=pygame.transform.scale(button,buttonsize)

    fontttf="bone/boneimg/font.ttf"
    fontsize=72
    font=pygame.font.Font(fontttf,fontsize)

    smallsize=36
    small=pygame.font.Font(fontttf,smallsize)

    starttime=pygame.time.get_ticks()
    timelimit=2*60*1000+30*1000

    hitcircle=[]
    spawninterval=2000
    lastspawntime=starttime
    shrinkduration=2000

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
        detectradius = radius // 2
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
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            elif event.type==pygame.MOUSEBUTTONDOWN:
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
                            if score>= 80 and score%80 ==0:
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

        caption=small.render("Click the circles in time!",True,white)
        screen.blit(caption,(width//2-caption.get_width()//2,20))
        
        minutes=remainingtime//60000
        seconds=(remainingtime%60000)//1000
        timer=small.render(f"Time:{minutes:01}:{seconds:02}",True,white)
        screen.blit(timer,(width-timer.get_width()-20,20))

        if remainingtime <= 0 or gameover:
            running=False
        pygame.display.flip()

    screen.fill(black)
    if score>=100:
        result= "You found your favourite bone!"
    else:
        result= "You lost your bone!"

    resultrender=font.render(result,True,(white))
    screen.blit(resultrender,((width-resultrender.get_width())//2,(height-resultrender.get_height())//2))
        
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

# debug\
# running=True
# while running:
#     bone()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#             break