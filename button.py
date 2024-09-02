import sys
import pygame

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Love Button Interaction")

images = [
    pygame.transform.scale(pygame.image.load("love button/dog_i.png"), (1280, 720)), 
    pygame.transform.scale(pygame.image.load("love button/dog_ii.png"), (1280, 720)), 
    pygame.transform.scale(pygame.image.load("love button/dog_iii.png"), (1280, 720))
]
current_image_index = 0

progress = 0
max_progress = 30 
bar_width = 300
bar_height = 20
bar_x = 300
bar_y = 100

interaction_area = pygame.Rect(300, 250, 400, 200)

last_mouse_x = None
direction = None
strokes = 0
#count the num within interact area

running = True

while running:
    screen.fill((255, 255, 255))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Mouse movement detection
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            
            # "Colli" check the mouse is in the interaction area
            if interaction_area.collidepoint(mouse_x, mouse_y):
                if last_mouse_x is not None:
                    if mouse_x > last_mouse_x and direction != "right":
                        direction = "right"
                        strokes += 1
                    elif mouse_x < last_mouse_x and direction != "left":
                        direction = "left"
                        strokes += 1
                    
                    progress = (strokes / max_progress) * 100
                    
                    if progress >= 66:
                        current_image_index = 2
                    elif progress >= 33:
                        current_image_index = 1

                last_mouse_x = mouse_x
            else:
                last_mouse_x = None
                direction = None

        if progress >= 100:
            running = False 

    screen.blit(images[current_image_index], (0, 0))

#bar column
    pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 2)  # Bar outline
    pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, (progress / 100) * bar_width, bar_height))  # Progress fill

#red red column
    pygame.draw.rect(screen, (255, 0, 0, 100), interaction_area, 2)  # Red rectangle for the interaction area
    
    pygame.display.flip()

pygame.quit()
