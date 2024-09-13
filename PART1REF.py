# As a reference only, old and new codes


import pygame
import common
from diary import diary

# settings for the window of the game
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load("asset/image/gameicon.png")
pygame.display.set_caption("Memories")
pygame.display.set_icon(icon)

# Load images
p1_a = pygame.image.load("asset/image/dogbox.png")
p1_b = pygame.image.load("asset/image/dogndead.png")
p1_c = pygame.image.load("asset/image/olddog.png")
p1_d = pygame.image.load("asset/image/youngdog.png")
p1_e = pygame.image.load("asset/image/handndog.png")
p1_f = pygame.image.load("asset/image/grpimg.png")

# Group A and B definitions
# group_A = [(p1_a, 1), (p1_b, 1), (p1_c, 1)]  # (image, display time in secs)
# group_B = [(p1_d, 1), (p1_e, 1), (p1_f, 1)]

# def display_group(group):
#     start_time = pygame.time.get_ticks()  # get initial time
#     for img, duration in group:
#         while True:
#             current_time = pygame.time.get_ticks()  # get current time
#             elapsed_time = (current_time - start_time) / 1000  # Calculate elapsed time in seconds
#             screen.blit(img, (0, 0))
            
#             # music button update(show on screen)
#             if common.music_button.visible:
#                 common.music_button.update(screen)
#             if common.mute_button.visible:
#                 common.mute_button.update(screen)

#             pygame.display.flip()

#             # Event handling for quit and music toggling
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     common.running = False
#                     return None
#                 if event.type == pygame.MOUSEBUTTONDOWN:
#                     if common.music_button.visible and common.music_button.checkforinput(pygame.mouse.get_pos()):
#                         common.click.play()
#                         common.music_on_off()
#                     elif common.mute_button.visible and common.mute_button.checkforinput(pygame.mouse.get_pos()):
#                         common.click.play()
#                         common.music_on_off()

#             if elapsed_time >= duration:  # Check if the display time has passed
#                 start_time = current_time  # Reset the start time for the next image
#                 break  # Move to the next image

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


# def first_scene():
#     clock = pygame.time.Clock()
#     common.running = True
#     while common.running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 common.running = False
#                 return

#         common.fade_in(screen, p1_a, duration=1000)
#         # screen.blit(p1_a, (0,0))
#         # updatem()
#         pygame.display.flip()

#         start_time = pygame.time.get_ticks()
#         while common.running:
#             screen.blit(p1_a, (0,0))
#             # if onoffm():
#             #     return
#             onoffm()
#             updatem()
#             pygame.display.flip()
            
#             current_time = pygame.time.get_ticks()
#             elapsed_time = current_time - start_time
#             if elapsed_time >= 2000:
#                 common.fade_out(screen, p1_a, duration=1000)
#                 break

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     common.running = False
#                     return

#             pygame.time.wait(100)

#         common.fade_in(screen, p1_b, duration=2000)
#         pygame.display.flip()

#         start_time = pygame.time.get_ticks()
#         while common.running:
#             # if onoffm():
#             #     return
#             screen.blit(p1_b, (0,0))
#             onoffm()
#             updatem()
            
#             current_time = pygame.time.get_ticks()
#             elapsed_time = current_time - start_time
#             if elapsed_time >= 2000:
#                 common.fade_out(screen, p1_b, duration=1000)
#                 break

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     common.running = False
#                     return

#             pygame.time.wait(100)

#         common.fade_in(screen, p1_c, duration=2000)
#         pygame.display.flip()

#         start_time = pygame.time.get_ticks()
#         while common.running:
#             # if onoffm():
#             #     return
#             screen.blit(p1_c, (0,0))
#             onoffm()
#             updatem()
            
#             current_time = pygame.time.get_ticks()
#             elapsed_time = current_time - start_time
#             if elapsed_time >= 2000:
#                 common.fade_out(screen, p1_c, duration=1000)
#                 break

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     common.running = False
#                     return

#             pygame.time.wait(100)

#         common.fade_in(screen, p1_d, duration=2000)
#         pygame.display.flip()

#         start_time = pygame.time.get_ticks()
#         while common.running:
#             # if onoffm():
#             #     return
#             screen.blit(p1_d, (0,0))
#             onoffm()
#             updatem()
            
#             current_time = pygame.time.get_ticks()
#             elapsed_time = current_time - start_time
#             if elapsed_time >= 2000:
#                 common.fade_out(screen, p1_d, duration=1000)
#                 break

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     common.running = False
#                     return

#             pygame.time.wait(100)

#         common.fade_in(screen, p1_e, duration=2000)
#         pygame.display.flip()

#         start_time = pygame.time.get_ticks()
#         while common.running:
#             # if onoffm():
#             #     return
#             screen.blit(p1_e, (0,0))
#             onoffm()
#             updatem()
            
#             current_time = pygame.time.get_ticks()
#             elapsed_time = current_time - start_time
#             if elapsed_time >= 2000:
#                 common.fade_out(screen, p1_e, duration=1000)
#                 break

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     common.running = False
#                     return

#             pygame.time.wait(100)

#         common.fade_in(screen, p1_f, duration=2000)
#         pygame.display.flip()

#         start_time = pygame.time.get_ticks()
#         while common.running:
#             # if onoffm():
#             #     return
#             screen.blit(p1_f, (0,0))
#             onoffm()
#             updatem()
            
#             current_time = pygame.time.get_ticks()
#             elapsed_time = current_time - start_time
#             if elapsed_time >= 2000:
#                 common.fade_out(screen, p1_f, duration=1000)
#                 break

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     common.running = False
#                     return

#             pygame.time.wait(100)


#         updatem()

#         common.current_scene = "second_a"
#         from part2 import second_a
#         second_a()


#     pygame.quit()

def first_scene():
    clock = pygame.time.Clock()
    common.running = True
    scenes = [
        {"image": p1_a, "fade_in": 1000, "display": 2000, "fade_out": 1000},
        {"image": p1_b, "fade_in": 2000, "display": 2000, "fade_out": 1000},
        {"image": p1_c, "fade_in": 2000, "display": 2000, "fade_out": 1000},
        {"image": p1_d, "fade_in": 2000, "display": 2000, "fade_out": 1000},
        {"image": p1_e, "fade_in": 2000, "display": 2000, "fade_out": 1000},
        {"image": p1_f, "fade_in": 2000, "display": 2000, "fade_out": 1000}
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

        if index == 2:  #dic start from 0
            diary()  # Call minigame here
            # The code will return here after the minigame finishes
            if not common.running:
                break

    if common.running:
        common.current_scene = "second_a"
        from part2 import second_a
        second_a()

    pygame.quit()



# # ONLY FOR DEBUGG!!! DO NOT RUN THIS WHEN RUN FROM MAINNNN!!!
# while common.running:
#     first_scene()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             common.running = False
#             break