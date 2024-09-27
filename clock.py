import pygame
import math
import common
from button import Button

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load("asset/image/gameicon.png")
pygame.display.set_caption("Memories")
pygame.display.set_icon(icon)

background = pygame.image.load("Photo used/Clock/dog die.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
dog_old = pygame.image.load("Photo used/Clock/dog old.png")
dog_old = pygame.transform.scale(dog_old, (SCREEN_WIDTH, SCREEN_HEIGHT))
first_met = pygame.image.load("Photo used/Clock/first met.png")
first_met = pygame.transform.scale(first_met, (SCREEN_WIDTH, SCREEN_HEIGHT))
clockbg = pygame.image.load("Photo used/Clock/clocks.png")
clockbg = pygame.transform.scale(clockbg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Clock parameters
CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4)
RADIUS = 150
hour_angle = 0
minute_angle = 0

# Game state
clock_stopped = False
current_background = background
zoom_factor = 1.0
message = ""
show_message = False
message_timer = 0
 
fonts = common.arcade(36)
font = common.cutedisplay(46)
return_img = pygame.image.load("asset/image/return.png")
return_button = Button(50, 50, image=return_img, scale=0.27)
game_completed = False

def updatem():
    if common.music_button.visible:
        common.music_button.update(screen)
    if common.mute_button.visible:
        common.mute_button.update(screen)

    pygame.display.flip()

# Get bg colour of initial photo
bg_colour = background.get_at((0, 0))

def draw_scene(surface, hour_angle, minute_angle, zoom_factor, draw_clock=True):
    surface.fill(bg_colour)
    
    # Draw the zoom 
    zoomed_width = int(SCREEN_WIDTH * zoom_factor)
    zoomed_height = int(SCREEN_HEIGHT * zoom_factor)
    
    zoomed_background = pygame.transform.scale(current_background, (zoomed_width, zoomed_height))
    
    #Position blit zoom
    x_offset = (zoomed_width - SCREEN_WIDTH) // 2
    y_offset = (zoomed_height - SCREEN_HEIGHT) // 2
    
    surface.blit(zoomed_background, (-x_offset, -y_offset))

    #Draw the clock
    if draw_clock:
        pygame.draw.circle(surface, (255, 255, 255), CENTER, RADIUS, 2)

        for i in range(1, 13):
            angle = math.radians(i * 30 - 90)
            x = CENTER[0] + int((RADIUS - 20) * math.cos(angle))
            y = CENTER[1] + int((RADIUS - 20) * math.sin(angle))
            number = fonts.render(str(i), True, (255, 255, 255))
            number_rect = number.get_rect(center=(x, y))
            surface.blit(number, number_rect)

        hour_x = CENTER[0] + int(RADIUS * 0.5 * math.sin(hour_angle))
        hour_y = CENTER[1] - int(RADIUS * 0.5 * math.cos(hour_angle))
        pygame.draw.line(surface, (255, 255, 255), CENTER, (hour_x, hour_y), 4)

        minute_x = CENTER[0] + int(RADIUS * 0.7 * math.sin(minute_angle))
        minute_y = CENTER[1] - int(RADIUS * 0.7 * math.cos(minute_angle))
        pygame.draw.line(surface, (255, 255, 255), CENTER, (minute_x, minute_y), 2)
        updatem()
        pygame.display.flip()

def check_hour_hand_position(cumulative_angle):
    full_rotations = abs(cumulative_angle) // (2 * math.pi)
    if full_rotations >= 1:
        if cumulative_angle > 0:
            return "clockwise"
        else:
            return "anticlockwise"
    return None

def clock_main_loop():
    global hour_angle, minute_angle, clock_stopped, current_background, zoom_factor, message, show_message, message_timer, game_completed

    drag_min = False
    last_angle = 0
    cumulative_angle = 0
    initial_zoom = 1.0

    game_is_done = False
    fade = False

    running = True
    while running:
        if not fade:
            common.fade_in(screen, clockbg, duration=1000)
            fade = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if common.music_button.visible and common.music_button.checkforinput(pygame.mouse.get_pos()):
                    common.click.play()
                    common.music_on_off()
                elif common.mute_button.visible and common.mute_button.checkforinput(pygame.mouse.get_pos()):
                    common.click.play()
                    common.music_on_off()
            if event.type == pygame.MOUSEBUTTONDOWN and not clock_stopped:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                minute_x = CENTER[0] + int(RADIUS * 0.7 * math.sin(minute_angle))
                minute_y = CENTER[1] - int(RADIUS * 0.7 * math.cos(minute_angle))
                if math.sqrt((mouse_x-minute_x)**2 + (mouse_y-minute_y)**2) < 15:
                    drag_min = True
                    last_angle = minute_angle
                    initial_zoom = zoom_factor
            elif event.type == pygame.MOUSEBUTTONUP:
                drag_min = False

        if drag_min and not clock_stopped:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            new_angle = math.atan2(mouse_x - CENTER[0], -(mouse_y - CENTER[1]))
            
            delta_angle = new_angle - last_angle
            if delta_angle > math.pi:
                delta_angle -= 2 * math.pi
            elif delta_angle < -math.pi:
                delta_angle += 2 * math.pi
            
            minute_angle = new_angle
            hour_angle += delta_angle / 12
            cumulative_angle += delta_angle / 12
            last_angle = new_angle
            
            # Update zoom based on direction
            # Clockwise
            if cumulative_angle > 0:  
                target_zoom = max(initial_zoom - (cumulative_angle / (2 * math.pi) * 0.25), 0.75)
            # Anticlockwise
            else:  
                target_zoom = min(initial_zoom + (abs(cumulative_angle) / (2 * math.pi) * 0.5), 1.5)
            
            zoom_factor += (target_zoom - zoom_factor) * 0.1  
            
            rotation_result = check_hour_hand_position(cumulative_angle)
            if rotation_result == "clockwise":
                message = "The dog did not become younger and it die soon"
                show_message = True
                message_timer = pygame.time.get_ticks()
            elif rotation_result == "anticlockwise":
                message = "The dog back to the day it met its owner"
                show_message = True
                message_timer = pygame.time.get_ticks()

        screen.fill((0, 0, 0))  
        
        if show_message:
            screen.fill((0, 0, 0))
            message_surface = font.render(message, True, (255, 255, 255))
            message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(message_surface, message_rect)
            
            if pygame.time.get_ticks() - message_timer > 2000:
                show_message = False
                if message == "The dog did not become younger and it die soon":
                    current_background = dog_old
                    updatem()
                    pygame.display.flip()
                elif message == "The dog back to the day it met its owner":
                    # current_background = first_met
                    show_message = True
                    screen.fill((0, 0, 0))
                    message_surface = font.render(message, True, (255, 255, 255))
                    message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    screen.blit(message_surface, message_rect)
                    return_button.update(screen)
                    updatem()
                    pygame.display.flip()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if return_button.checkforinput(pygame.mouse.get_pos()):
                            common.click.play()
                            game_is_done = True
                clock_stopped = True
                zoom_factor = 1.0
                hour_angle = 0
                minute_angle = 0
                cumulative_angle = 0
        else:
            draw_scene(screen, hour_angle, minute_angle, zoom_factor, not clock_stopped)
            updatem()
            pygame.display.flip()

        if game_is_done:
            game_completed = True
            return
        # added
        pygame.display.flip()

    pygame.quit()


# clock_main_loop()