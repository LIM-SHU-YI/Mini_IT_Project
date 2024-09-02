import pygame
import common
from button import Button
from  p2interact import p2int

# settings for the window of the game
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load("asset/image/gameicon.png")
pygame.display.set_caption("Memories")
pygame.display.set_icon(icon)


# Load images
heart = pygame.image.load("asset/image/part2a/1h.png")
heart2 = pygame.image.load("asset/image/part2a/2h.png")
heart3 = pygame.image.load("asset/image/part2a/3h.png")
heart4 = pygame.image.load("asset/image/part2a/4h.png")
wait = pygame.image.load("asset/image/part2a/wait.png")
bath = pygame.image.load("asset/image/part2a/bath.png")
shower = pygame.image.load("asset/image/part2a/shower.png")
blowdry = pygame.image.load("asset/image/part2a/blowdry.png")
interface = pygame.image.load("asset/image/part2a/int.png")
livingroom = pygame.image.load("asset/image/part2a/livingroom.png")
redempty = pygame.image.load("asset/image/part2a/redempty.png")
redfull = pygame.image.load("asset/image/part2a/redfull.png")
redpour = pygame.image.load("asset/image/part2a/redpour.png")
blueempty = pygame.image.load("asset/image/part2a/blueempty.png")
bluewater = pygame.image.load("asset/image/part2a/bluewater.png")
water = pygame.image.load("asset/image/part2a/water.png")
toy = pygame.image.load("asset/image/part2a/toy.png")
dogfood = pygame.image.load("asset/image/part2a/dogfood.png")
bone = pygame.image.load("asset/image/part2a/bone.png")
lroom = pygame.image.load("asset/image/part2a/living.png")
lpic = pygame.image.load("asset/image/part2a/pic.png")
blur = pygame.image.load("asset/image/part2a/livingblur.png")
bowl = pygame.image.load("asset/image/part2a/bowl.png")
img1 = pygame.image.load("asset/image/part2a/img1.png")
img2 = pygame.image.load("asset/image/part2a/img2.png")
img3 = pygame.image.load("asset/image/part2a/img3.png")
img1_1 = pygame.image.load("asset/image/part2a/imgonec.png")
img2_2 = pygame.image.load("asset/image/part2a/imgtwo.png")
img3_3 = pygame.image.load("asset/image/part2a/imgthree.png")
bowls = pygame.image.load("asset/image/part2a/bowls.png")

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

group_A = [(wait, 1), (shower, 1), (bath, 1), (blowdry, 1)] 

def display_group(group):
    start_time = pygame.time.get_ticks()  # get initial time
    for img, duration in group:
        while True:
            current_time = pygame.time.get_ticks()  # get current time
            elapsed_time = (current_time - start_time) / 1000  # Calculate elapsed time in seconds
            screen.blit(img, (0, 0))
            
            # music button update(show on screen)
            if common.music_button.visible:
                common.music_button.update(screen)
            if common.mute_button.visible:
                common.mute_button.update(screen)

            pygame.display.flip()

            # Event handling for quit and music toggling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    common.running = False
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if common.music_button.visible and common.music_button.checkforinput(pygame.mouse.get_pos()):
                        common.click.play()
                        common.music_on_off()
                    elif common.mute_button.visible and common.mute_button.checkforinput(pygame.mouse.get_pos()):
                        common.click.play()
                        common.music_on_off()

            if elapsed_time >= duration:  # Check if the display time has passed
                start_time = current_time  # Reset the start time for the next image
                break  # Move to the next image


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

# —————————————————————————————————————Testing—————————————————————————————————————

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
            for img, duration in group_A:
                start_time = pygame.time.get_ticks()
                while True:
                    current_time = pygame.time.get_ticks()
                    elapsed_time = (current_time - start_time) / 1000
                    screen.blit(img, (0, 0))

                    if common.music_button.visible:
                        common.music_button.update(screen)
                    if common.mute_button.visible:
                        common.mute_button.update(screen)

                    pygame.display.flip()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            common.running = False
                            return None
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if common.music_button.visible and common.music_button.checkforinput(pygame.mouse.get_pos()):
                                common.click.play()
                                common.music_on_off()
                            elif common.mute_button.visible and common.mute_button.checkforinput(pygame.mouse.get_pos()):
                                common.click.play()
                                common.music_on_off()

                    if elapsed_time >= duration:
                        break

                    clock.tick(60)

            showlroom = True

        if showlroom:
            # common.running = True
            while common.running:
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
# while common.running:
#     second_a()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             common.running = False
#             break