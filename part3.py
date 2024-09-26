import pygame
import common
from clock import clock_main_loop


# settings for the window of the game
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load("asset/image/gameicon.png")
pygame.display.set_caption("Memories")
pygame.display.set_icon(icon)

# Load images
p1_a = pygame.image.load("asset/image/part3/1.png")
p1_b = pygame.image.load("asset/image/part3/2.png")
p1_c = pygame.image.load("asset/image/part3/3.png")
p1_d = pygame.image.load("asset/image/part3/4.png")
p1_e = pygame.image.load("asset/image/part3/4b.png")
p1_f = pygame.image.load("asset/image/part3/5.png")


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


def display_text_centered(screen, text, font, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    screen.blit(text_surface, text_rect)

def text_slide_sequence():
    font = pygame.font.Font("kitasset/part2/font.ttf", 41) 
    text_slides = [
        "Guided by Death, ",
        "Hachi found its owner at the station in the other world.",
        "Hachi fulfilled its final wish.",
        "Their souls ascended, reunited for eternity.",
        "Though Death had witnessed countless farewells and sorrow,",
        "This journey made him reflect on life's meaning and the power of love.",
        "As Hachi and its owner vanished into the light, the street grew still.",
        "A cardboard box on the street gently swayed in the breeze,",
        "Bringing this story to a quiet, tender close."
    ]
    
    slide_duration = 3000
    
    for text in text_slides:
        start_time = pygame.time.get_ticks()
        while common.running:
            screen.fill((0, 0, 0)) 
            display_text_centered(screen, text, font, (255, 255, 255))  # Display the text
            pygame.display.flip()

            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - start_time

            if elapsed_time >= slide_duration:
                break  

def first_scene():
    clock = pygame.time.Clock()
    common.running = True
    scenes = [
        {"image": p1_a, "fade_in": 1000, "display": 1000, "fade_out": 1000},
        {"image": p1_b, "fade_in": 1000, "display": 1000, "fade_out": 1000},
        {"image": p1_c, "fade_in": 1000, "display": 1000, "fade_out": 1000},
        {"image": p1_d, "fade_in": 1000, "display": 1000, "fade_out": 1000},
        {"image": p1_e, "fade_in": 1000, "display": 1000, "fade_out": 1000},
        {"image": p1_f, "fade_in": 1000, "display": 1000, "fade_out": 1000}  
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

    if common.running:
        text_slide_sequence()

        # if index == 2:  #dic start from 0
        #     clock_main_loop()  # Call minigame here
        #     # The code will return here after the minigame finishes
        #     if not common.running:
        #         break

    # if common.running:
    #     from love import love_interaction
    #     love_interaction()

    pygame.quit()


# # ONLY FOR DEBUGG!!! DO NOT RUN THIS WHEN RUN FROM MAINNNN!!!
# while common.running:
#     first_scene()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             common.running = False
#             break