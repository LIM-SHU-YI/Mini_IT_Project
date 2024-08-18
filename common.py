import pygame
from button import Button

pygame.init()

current_scene = "main_menu"
running = True


# Fonts
def storytella(size):
    return pygame.font.Font("asset/font/Storytella.otf", size)

def monera(size):
    return pygame.font.Font("asset/font/Monera Calm.otf", size)

def playfair(size):
    return pygame.font.Font("asset/font/PlayfairDisplaySC-Regular.ttf", size)

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
    
# clicking sound effect
click = pygame.mixer.Sound("asset/songs/click.mp3")