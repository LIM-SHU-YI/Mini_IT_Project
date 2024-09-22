import pygame
import common
from button import Button
from p2interact import p2int

# settings for the window of the game
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load("asset/image/gameicon.png")
pygame.display.set_caption("Memories")
pygame.display.set_icon(icon)


# Load images
heart = pygame.image.load("asset/image/part2b/1h.png")
heart2 = pygame.image.load("asset/image/part2b/2h.png")
heart3 = pygame.image.load("asset/image/part2b/3h.png")
heart4 = pygame.image.load("asset/image/part2b/4h.png")
wait = pygame.image.load("asset/image/part2b/wait.png")
bath = pygame.image.load("asset/image/part2b/bath.png")
shower = pygame.image.load("asset/image/part2b/shower.png")
blowdry = pygame.image.load("asset/image/part2b/blowdry.png")
interface = pygame.image.load("asset/image/part2b/int.png")
livingroom = pygame.image.load("asset/image/part2b/livingroom.png")
redempty = pygame.image.load("asset/image/part2b/redempty.png")
redfull = pygame.image.load("asset/image/part2b/redfull.png")
redpour = pygame.image.load("asset/image/part2b/redpour.png")
blueempty = pygame.image.load("asset/image/part2b/blueempty.png")
bluewater = pygame.image.load("asset/image/part2b/bluewater.png")
water = pygame.image.load("asset/image/part2b/water.png")
toy = pygame.image.load("asset/image/part2b/toy.png")
dogfood = pygame.image.load("asset/image/part2b/dogfood.png")
bone = pygame.image.load("asset/image/part2b/bone.png")
lroom = pygame.image.load("asset/image/part2b/living.png")
lpic = pygame.image.load("asset/image/part2b/pic.png")
blur = pygame.image.load("asset/image/part2b/livingblur.png")
bowl = pygame.image.load("asset/image/part2b/bowl.png")
img1 = pygame.image.load("asset/image/part2b/img1.png")
img2 = pygame.image.load("asset/image/part2b/img2.png")
img3 = pygame.image.load("asset/image/part2b/img3.png")
img1_1 = pygame.image.load("asset/image/part2b/imgonec.png")
img2_2 = pygame.image.load("asset/image/part2b/imgtwo.png")
img3_3 = pygame.image.load("asset/image/part2b/imgthree.png")
bowls = pygame.image.load("asset/image/part2b/bowls.png")

# img1_1 = pygame.transform.scale(img1_1, (1071, 602))
img1_1 = pygame.transform.scale(img1_1, (400, 400))
img1_1pos = img1_1.get_rect(center=(640,360))
img2_2pos = img2_2.get_rect(center=(640,360))
img3_3pos = img3_3.get_rect(center=(640,360))

return_img = pygame.image.load("asset/image/return.png")
return_button = Button(50, 50, image=return_img, scale=0.27)    

b_bowl = Button(1170,655, image=bowl)
b_img1 = Button(230,70, image=img1)
b_img2= Button(460,36, image=img2)
b_img3 = Button(610, 119, image=img3)

border_width = 15

def onoffm():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            common.running = False
            return True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if common.music_button.visible and common.music_button.checkforinput(pygame.mouse.get_pos()):
                common.click.play()
                common.music_on_off()
                return False
            elif common.mute_button.visible and common.mute_button.checkforinput(pygame.mouse.get_pos()):
                common.click.play()
                common.music_on_off()
                return False
    return False

def updatem():
    if common.music_button.visible:
        common.music_button.update(screen)
    if common.mute_button.visible:
        common.mute_button.update(screen)

    pygame.display.flip()
def show_img1_1():
    clock = pygame.time.Clock()
    screen.blit(blur, (0,0))
    screen.blit(img1_1, img1_1pos)  # Display img1_1 on top of lpic
    pygame.draw.rect(screen, (0, 0, 0), (img1_1pos.x - border_width, img1_1pos.y - border_width, img1_1pos.width + 2 * border_width, img1_1pos.height + 2 * border_width), border_width)
    return_button.update(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common.running = False
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.checkforinput(pygame.mouse.get_pos()):
                    common.click.play()
                    return  # return to showlroom loop

        pygame.display.flip()
        clock.tick(60)  # Limit the frame rate to 60 FPS

def show_img2_2():
    clock = pygame.time.Clock()
    screen.blit(blur, (0,0))
    screen.blit(img2_2, img2_2pos)  # Display img1_1 on top of lpic
    pygame.draw.rect(screen, (0, 0, 0), (img2_2pos.x - border_width, img2_2pos.y - border_width, img2_2pos.width + 2 * border_width, img2_2pos.height + 2 * border_width), border_width)
    return_button.update(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common.running = False
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.checkforinput(pygame.mouse.get_pos()):
                    common.click.play()
                    return

        pygame.display.flip()
        clock.tick(60)

def show_img3_3():
    clock = pygame.time.Clock()
    screen.blit(blur, (0,0))
    screen.blit(img3_3, img3_3pos)  # Display img1_1 on top of lpic
    pygame.draw.rect(screen, (0, 0, 0), (img3_3pos.x - border_width, img3_3pos.y - border_width, img3_3pos.width + 2 * border_width, img3_3pos.height + 2 * border_width), border_width)
    return_button.update(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common.running = False
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.checkforinput(pygame.mouse.get_pos()):
                    common.click.play()
                    return

        pygame.display.flip()
        clock.tick(60)

def bowl_interact():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common.running = False
                return
                
        p2int()
        if not common.running:
            break

# ———————————————————————————————————————————————————————————————————————————————————————————

def second_a():
    clock = pygame.time.Clock()
    common.running = True
    showlroom = False

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

        if not showlroom:
            scenes = [
                    {"image": wait, "fade_in": 1000, "display": 1000, "fade_out": 1000},
                    {"image": shower, "fade_in": 1000, "display": 1000, "fade_out": 1000},
                    {"image": bath, "fade_in": 1000, "display": 1000, "fade_out": 1000},
                    {"image": blowdry, "fade_in": 1000, "display": 1000, "fade_out": 1000}
                ]
                
            for index, scene in enumerate(scenes):
                if not common.running:
                    break

                common.fade_in(screen, scene["image"], duration=scene["fade_in"])
                pygame.display.flip()

                start_time = pygame.time.get_ticks()
                while common.running:
                    screen.blit(scene["image"], (0,0))
                    onoffm()
                    updatem()
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            common.running = False
                            return
                    current_time = pygame.time.get_ticks()
                    elapsed_time = current_time - start_time
                    if elapsed_time >= scene["display"]:
                        common.fade_out(screen, scene["image"], duration=scene["fade_out"])
                        break

                    pygame.time.wait(100)

            showlroom = True

        if showlroom:
            fade = False
            # common.running = True
            while common.running:
                if not fade:
                    common.fade_in(screen, livingroom, duration=1000)
                    fade = True
                screen.blit(lpic, (0,0))
                b_bowl.update(screen)
                b_img1.update(screen)
                b_img2.update(screen)
                b_img3.update(screen)


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
                            if b_img1.checkforinput(pygame.mouse.get_pos()):
                                common.click.play()
                                show_img1_1()

                            if b_img2.checkforinput(pygame.mouse.get_pos()):
                                common.click.play()
                                show_img2_2()

                            if b_img3.checkforinput(pygame.mouse.get_pos()):
                                common.click.play()
                                show_img3_3()

                            if b_bowl.checkforinput(pygame.mouse.get_pos()):
                                common.click.play()
                                bowl_interact()


                        if common.music_button.visible and common.music_button.checkforinput(pygame.mouse.get_pos()):
                            common.click.play()
                            common.music_on_off()
                        elif common.mute_button.visible and common.mute_button.checkforinput(pygame.mouse.get_pos()):
                            common.click.play()
                            common.music_on_off()




# ONLY FOR DEBUGG!!! DO NOT RUN THIS WHEN RUN FROM MAINNNN!!!
while common.running:
    second_a()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            common.running = False
            break