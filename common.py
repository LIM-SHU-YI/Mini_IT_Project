import pygame
from button import Button
import common

pygame.init()

current_scene = "main_menu"
running = True

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Fonts
def storytella(size):
    return pygame.font.Font("asset/font/Storytella.otf", size)

def arcade(size):
    return pygame.font.Font("asset/font/arcadeclassic.ttf", size)

def cutedisplay(size):
    return pygame.font.Font("asset/font/cutedisplay.ttf", size)


def text_with_shadow(text, font, shadow_color, text_color, pos, shadow_offset=(7, 7)):
    # text shadow
    shadow_surface = font.render(text, True, shadow_color)
    shadow_rect = shadow_surface.get_rect(center=(pos[0] + shadow_offset[0], pos[1] + shadow_offset[1]))

    # main text
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=pos)

    return (shadow_surface, shadow_rect), (text_surface, text_rect)

def normal_text(text, font, text_color, pos):
    ntext = font.render(text, True, text_color)
    ntext_rect = ntext.get_rect(center=(pos[0], pos[1]))

    return (ntext, ntext_rect)


# Music img
music_img = pygame.image.load("asset/image/m.png")
mute_img = pygame.image.load("asset/image/mm.png")

bgm = pygame.mixer.music.load("asset/songs/bgm.mp3")
bgm = pygame.mixer.music.set_volume(0.2)
# Run the music at start
pygame.mixer.music.play(-1)

# Music button
music_button = Button(1230,50, image=music_img, scale=0.35)
mute_button = Button(1230,50, image=mute_img, scale=0.35, visible=False)

# Functions of music button, pygame.mixer.music.get_busy() checks music playing state, if playing=True otherwise False
def music_on_off():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        music_button.visible = False
        mute_button.visible = True
        return mute_button
    else:
        pygame.mixer.music.unpause()
        music_button.visible = True
        mute_button.visible = False
        return music_button
    
# sound effects
click = pygame.mixer.Sound("asset/songs/click.mp3")
huh = pygame.mixer.Sound("asset/songs/huh.mp3")
huh.set_volume(0.35)
hahaha = pygame.mixer.Sound("asset/songs/hahaha.mp3")
sopro = pygame.mixer.Sound("asset/songs/sopro.mp3")


def fade_in(screen, surface, duration=2000):
    clock = pygame.time.Clock()
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))
    
    start_time = pygame.time.get_ticks()  # Track the start time
    while True:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time

        # Calculate the alpha based on time elapsed
        progress = min(elapsed_time / duration, 1)  # Clamp the progress between 0 and 1
        alpha = int(255 * (1 - progress))  # Reverse alpha fade-in

        # Set the transparency and draw the image
        fade_surface.set_alpha(alpha)
        screen.blit(surface, (0, 0))  # draw image
        screen.blit(fade_surface, (0, 0))  # apply fade effect
        pygame.display.update()
        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common.running = False
                pygame.quit()

        # Exit when fade in is complete
        if progress >= 1:
            break
        
        clock.tick(60)

def fade_out(screen, surface, duration=2000):
    clock = pygame.time.Clock()
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))
    
    start_time = pygame.time.get_ticks()  # Track the start time
    while True:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time

        # Calculate the alpha based on time elapsed
        progress = min(elapsed_time / duration, 1)  # Clamp the progress between 0 and 1
        alpha = int(255 * progress)  # Fade-out

        # Set the transparency and draw the image
        fade_surface.set_alpha(alpha)
        screen.blit(surface, (0, 0))  # Draw the main image
        screen.blit(fade_surface, (0, 0))  # Apply the fade effect
        pygame.display.update()  # Update the display

        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common.running = False
                pygame.quit()

        # Exit the loop when fade-out is complete
        if progress >= 1:
            break

        clock.tick(60)  # Control frame rate

