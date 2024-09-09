import sys
import pygame
import time

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Love Button Interaction")

background = pygame.transform.scale(pygame.image.load("love button/pink_background.png"), (1280, 720))

images = [
    pygame.transform.scale(pygame.image.load("love button/dog_i.png"), (658, 643)), 
    pygame.transform.scale(pygame.image.load("love button/dog_ii.png"), (688, 680)), 
    pygame.transform.scale(pygame.image.load("love button/dog_iii.png"), (536, 625)), 
    pygame.transform.scale(pygame.image.load("love button/dog_iv.png"), (619, 623)),
    pygame.transform.scale(pygame.image.load("love button/dog_1.png"), (691, 641)), 
    pygame.transform.scale(pygame.image.load("love button/dog_2.png"), (438, 672))
]

current_image_index = 0

image_positions = [
    ((1280 - 658) // 2, (720 - 643) // 2),  
    ((1280 - 688) // 2, (720 - 730) // 2), 
    ((1280 - 536) // 2, (720 - 625) // 2), 
    ((1280 - 710) // 2, (720 - 623) // 2),
    ((1280 - 725) // 2, (720 - 645) // 2), 
    ((1280 - 285) // 2, (720 - 647) // 2)
]

masks = [pygame.mask.from_surface(image) for image in images]

progress = 0
max_progress = 30 
bar_width = 300
bar_height = 40
bar_x = 70
bar_y = 50

heart_image = pygame.transform.scale(pygame.image.load("love button/heart.png"), (30, 30))


stomach_area = pygame.Rect(610, 180, 280, 200)
head_area = pygame.Rect(630, 65, 190, 80)

last_mouse_x = None
direction = None
strokes = 0
mouse_press = False  
out_area = False 
running = True


while running:
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_press = True  
        
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_press = False  

        # Mouse movement detection
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            
            # Check if the mouse is within the interaction area
            mouse_in_interaction_area = stomach_area.collidepoint(mouse_x, mouse_y)
            
            if mouse_press:
                if not mouse_in_interaction_area:
                    out_area = True
                else:
                    out_area = False
                
                if out_area:
                    if progress < 50:
                        current_image_index = 4 
                    else:
                        current_image_index = 5  
                else:
                    local_mouse_x = mouse_x - image_positions[current_image_index][0]
                    local_mouse_y = mouse_y - image_positions[current_image_index][1]
                    
                    if 0 <= local_mouse_x < images[current_image_index].get_width() and \
                       0 <= local_mouse_y < images[current_image_index].get_height() and \
                       masks[current_image_index].get_at((local_mouse_x, local_mouse_y)):
                        
                        if last_mouse_x is not None:
                            if mouse_x > last_mouse_x and direction != "right":
                                direction = "right"
                                strokes += 1
                            elif mouse_x < last_mouse_x and direction != "left":
                                direction = "left"
                                strokes += 1
                        
                            progress = (strokes / max_progress) * 100
                            
                            if progress >= 50:
                                if strokes % 2 == 1:
                                    current_image_index = 2 
                                else:
                                    current_image_index = 3  
                                    stomach_area = head_area
                            else:
                                if strokes % 2 == 1:
                                    current_image_index = 0  
                                else:
                                    current_image_index = 1  
                                    stomach_area = pygame.Rect(610, 180, 280, 200)

                        last_mouse_x = mouse_x
            else:
                last_mouse_x = None
                direction = None

        if progress >= 100:
            running = False 

    screen.blit(images[current_image_index], image_positions[current_image_index])

    # Progress bar
    pygame.draw.rect(screen, (0, 0, 0), (65, 45, 310, 50), 2) 
    pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, (progress / 100) * bar_width, bar_height)) 

    heart_count = int(progress / 10) 
    for i in range(heart_count):
        screen.blit(heart_image, (bar_x + 10 + i * 30, bar_y + 5))

    # Interaction area
    pygame.draw.rect(screen, (120, 0, 0, 80), stomach_area, 2)
    
    pygame.display.flip()

pygame.quit()
