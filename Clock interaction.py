import pygame
import math

# Initialize pygame
pygame.init()

# Game window
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drag and click the clock hand")

# Colors
WHITE = (255, 255, 255)

# Clock Size and Position
POSITION = (WIDTH // 2, HEIGHT * 3 // 4)  # Moved down
SIZE = 150

# Hand's Initial Position
hour_angle = 0
minute_angle = 0

# Track dragged hand and rotations
drag_min = False
anticlockwise_rotations = 0
hour_rotations = 0

# Font for clock numbers and messages
font = pygame.font.Font(None, 24)
message_font = pygame.font.Font(None, 36)

# Load background images
background = pygame.image.load("Photo used/Clock/dog die.png")  # Make sure to have this image in your directory
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
next_scene = pygame.image.load("Photo used/Clock/first met.png")  # Make sure to have this image in your directory
next_scene = pygame.transform.scale(next_scene, (WIDTH, HEIGHT))

current_background = background

# Draw clock
def clock(hour_angle, minute_angle):
    screen.blit(current_background, (0, 0))

    # Draw clock circle
    pygame.draw.circle(screen, WHITE, POSITION, SIZE, 2)

    # Draw clock numbers
    for i in range(1, 13):
        angle = math.radians(i * 30 - 90)  # -90 to start at 12 o'clock
        x = POSITION[0] + int((SIZE - 20) * math.cos(angle))
        y = POSITION[1] + int((SIZE - 20) * math.sin(angle))
        number = font.render(str(i), True, WHITE)
        number_rect = number.get_rect(center=(x, y))
        screen.blit(number, number_rect)

    # Hour hand position
    hour_x = POSITION[0] + int(SIZE * 0.5 * math.sin(hour_angle))
    hour_y = POSITION[1] - int(SIZE * 0.5 * math.cos(hour_angle))
    pygame.draw.line(screen, WHITE, POSITION, (hour_x, hour_y), 4)

    # Minute hand position
    minute_x = POSITION[0] + int(SIZE * 0.7 * math.sin(minute_angle))
    minute_y = POSITION[1] - int(SIZE * 0.7 * math.cos(minute_angle))
    pygame.draw.line(screen, WHITE, POSITION, (minute_x, minute_y), 2)

# Check rotation conditions
def check_rotation_conditions():
    global anticlockwise_rotations, hour_angle, minute_angle
    if anticlockwise_rotations >= 12 and abs(hour_angle) % (2 * math.pi) < 0.1 and (minute_angle % (2 * math.pi)) < 0.1:
        return True
    return False

# Click and Drag
run = True
clockwise_message = ""
clockwise_rotation_started = False
game_over = False

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            minute_x = POSITION[0] + int(SIZE * 0.7 * math.sin(minute_angle))
            minute_y = POSITION[1] - int(SIZE * 0.7 * math.cos(minute_angle))
            if math.sqrt((mouse_x-minute_x)**2 + (mouse_y - minute_y)**2) < 15 and not game_over:
                drag_min = True
                clockwise_rotation_started = False

        elif event.type == pygame.MOUSEBUTTONUP:
            drag_min = False

    if drag_min and not game_over:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.atan2(mouse_x - POSITION[0], -(mouse_y - POSITION[1]))

        old_minute_angle = minute_angle
        minute_angle = angle
        # Calculate the change in minutes
        delta_minutes = ((minute_angle - old_minute_angle) / (2 * math.pi)) * 60
        if delta_minutes < -30:  # Crossed 12 o'clock clockwise
            delta_minutes += 60
        elif delta_minutes > 30:  # Crossed 12 o'clock counterclockwise
            delta_minutes -= 60
        
        # Update hour angle based on change in minutes
        hour_angle += (delta_minutes / 60) * (math.pi / 6)
        hour_angle %= 2 * math.pi

        # Check for anticlockwise rotation
        if delta_minutes < 0:
            anticlockwise_rotations += abs(delta_minutes) / 60
            if anticlockwise_rotations >= 12:
                hour_rotations = anticlockwise_rotations / 12

        # Check if rotation conditions are met
        if check_rotation_conditions():
            current_background = next_scene
            game_over = True

    clock(hour_angle, minute_angle)

    # Display clockwise rotation message
    if clockwise_rotation_started and clockwise_message:
        message_surface = message_font.render(clockwise_message, True, WHITE)
        message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(message_surface, message_rect)

    pygame.display.flip()

pygame.quit()