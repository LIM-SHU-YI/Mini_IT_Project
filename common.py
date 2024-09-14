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


#WIP below not the fully function ver
def slide_in(screen, image, direction="left", duration=2000):
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    if direction == "left":
        start_x = -SCREEN_WIDTH
        end_x = 0
        start_y = 0
        end_y = 0
    elif direction == "right":
        start_x = SCREEN_WIDTH
        end_x = 0
        start_y = 0
        end_y = 0
    elif direction == "up":
        start_y = -SCREEN_HEIGHT
        end_y = 0
        start_x = 0
        end_x = 0
    elif direction == "down":
        start_y = SCREEN_HEIGHT
        end_y = 0
        start_x = 0
        end_x = 0

    while True:
        delta_time = clock.tick(60)  # Get the time between frames, and limit FPS to 60
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common.running = False
                return  # Quit the game immediately
            
        # Calculate how far we are in the animation (as a percentage)
        progress = min(elapsed_time / duration, 1)  # Ensure it never goes above 1 (100%)

        # Calculate current position based on progress
        current_x = start_x + (end_x - start_x) * progress
        current_y = start_y + (end_y - start_y) * progress

        # Fill the screen and blit the image in its new position
        screen.fill((0, 0, 0))  # Clear the screen (or draw your background)
        screen.blit(image, (current_x, current_y))

        pygame.display.update()

        # End the loop when the progress reaches 100%
        if progress >= 1:
            break
        clock.tick(60)

def wipe_in(screen, image, direction="left", duration=2000):
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    # Variables for wipe effect based on direction
    if direction == "left":
        rect_width, rect_height = 0, SCREEN_HEIGHT
        max_width = SCREEN_WIDTH
        max_height = SCREEN_HEIGHT
    elif direction == "right":
        rect_width, rect_height = 0, SCREEN_HEIGHT
        max_width = SCREEN_WIDTH
        max_height = SCREEN_HEIGHT
    elif direction == "up":
        rect_width, rect_height = SCREEN_WIDTH, 0
        max_width = SCREEN_WIDTH
        max_height = SCREEN_HEIGHT
    elif direction == "down":
        rect_width, rect_height = SCREEN_WIDTH, 0
        max_width = SCREEN_WIDTH
        max_height = SCREEN_HEIGHT

    running = True
    while running:
        delta_time = clock.tick(60)
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common.running = False
                return

        # Calculate the progress of the wipe effect
        progress = min(elapsed_time / duration, 1)

        if direction == "left":
            rect_width = int(max_width * progress)
        elif direction == "right":
            rect_width = int(max_width * progress)
            x_offset = SCREEN_WIDTH - rect_width
        elif direction == "up":
            rect_height = int(max_height * progress)
        elif direction == "down":
            rect_height = int(max_height * progress)
            y_offset = SCREEN_HEIGHT - rect_height

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the image progressively based on the direction
        if direction == "left":
            screen.blit(image, (0, 0), (0, 0, rect_width, SCREEN_HEIGHT))
        elif direction == "right":
            screen.blit(image, (x_offset, 0), (x_offset, 0, rect_width, SCREEN_HEIGHT))
        elif direction == "up":
            screen.blit(image, (0, 0), (0, 0, SCREEN_WIDTH, rect_height))
        elif direction == "down":
            screen.blit(image, (0, y_offset), (0, y_offset, SCREEN_WIDTH, rect_height))

        pygame.display.update()

        # Exit when the wipe is complete
        if progress >= 1:
            break




def zoom_in(screen, image, duration=2000):
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time

        if elapsed_time >= duration:
            break

        scale_factor = elapsed_time / duration
        new_width = int(SCREEN_WIDTH * scale_factor)
        new_height = int(SCREEN_HEIGHT * scale_factor)
        scaled_image = pygame.transform.scale(image, (new_width, new_height))

        # Blit the scaled image at the center
        x = (SCREEN_WIDTH - new_width) // 2
        y = (SCREEN_HEIGHT - new_height) // 2
        screen.blit(scaled_image, (x, y))

        pygame.display.update()
        clock.tick(60)  # Cap at 60 FPS

