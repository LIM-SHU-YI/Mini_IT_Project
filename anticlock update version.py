import pygame
import math

# Game window
WIDTH, HEIGHT = 1280, 760
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drag and click the clock hand")

# Color of clock
White = (255,255,255)
Black = (0,0,0)

# Clock Size and Position
Position = (WIDTH//2, HEIGHT//2)
Size = 150

# Hand's Initial Position
hour_angle = -math.pi/2
minute_angle = -math.pi/2

# Track dragged hand
drag_hour = False
drag_min = False

#Draw clock
def clock (hour_angle, minute_angle):
    screen.fill(Black)

    pygame.draw.circle(screen, White, Position, Size, 2)

    #hour hand position 
    hour_x = Position[0] + int(Size * 0.6 * math.cos(hour_angle))
    hour_y = Position[1] + int(Size * 0.6 * math.sin(hour_angle))
    pygame.draw.line(screen, White, Position, (hour_x, hour_y),6)

    #minute hand position
    minute_x = Position[0] + int(Size * 0.9 * math.cos(minute_angle))
    minute_y = Position[1] + int(Size * 0.9 * math.sin(minute_angle))
    pygame.draw.line(screen, White, Position, (minute_x, minute_y),4)

# Click and Drag Run Progress
run = True

while run:
    #whatever pygame receive 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # mouse been clicked
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            hour_x = Position[0] + int(Size * 0.6 * math.cos(hour_angle))
            hour_y = Position[1] + int(Size * 0.6 * math.sin(hour_angle))
            if math.sqrt((mouse_x-hour_x)** 2 + (mouse_y - hour_y)**2)< 15:
                drag_hour = True

            minute_x = Position[0] + int(Size * 0.9 * math.cos(minute_angle))
            minute_y = Position[1] + int(Size * 0.9 * math.sin(minute_angle))
            if math.sqrt((mouse_x-minute_x)** 2 + (mouse_y - minute_y)**2)< 15:
                drag_min = True

        elif event.type == pygame.MOUSEBUTTONUP:
            drag_hour = False
            drag_min = False

    if drag_hour or drag_min:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.atan2(mouse_y - Position[1], mouse_x - Position[0])
        
        if drag_hour:
            hour_angle = angle
        
        if drag_min:
            minute_angle = angle

    clock(hour_angle, minute_angle)
    pygame.display.flip()

pygame.quit()
