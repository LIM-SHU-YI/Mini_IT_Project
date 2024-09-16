import pygame

def love_interaction():
    import sys
    import pygame
    import time

    pygame.init()

    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Love Button Interaction")

    background = pygame.transform.scale(pygame.image.load("sayyunasset/love_button/pink_background.png"), (1280, 720))

    images = [
        pygame.transform.scale(pygame.image.load("sayyunasset/love_button/dog_i.png"), (658, 643)), 
        pygame.transform.scale(pygame.image.load("sayyunasset/love_button/dog_ii.png"), (688, 680)), 
        pygame.transform.scale(pygame.image.load("sayyunasset/love_button/dog_iii.png"), (536, 625)), 
        pygame.transform.scale(pygame.image.load("sayyunasset/love_button/dog_iv.png"), (619, 623)),
        pygame.transform.scale(pygame.image.load("sayyunasset/love_button/dog_v.png"), (660, 498)), 
        pygame.transform.scale(pygame.image.load("sayyunasset/love_button/dog_vi.png"), (581, 497)),
        pygame.transform.scale(pygame.image.load("sayyunasset/love_button/dog_1.png"), (691, 641)), 
        pygame.transform.scale(pygame.image.load("sayyunasset/love_button/dog_2.png"), (438, 672)),
        pygame.transform.scale(pygame.image.load("sayyunasset/love_button/dog_3.png"), (586, 494))
    ]

    current_image_index = 0

    image_positions = [
        ((1280 - 658) // 2, (720 - 643) // 2),  
        ((1280 - 688) // 2, (720 - 730) // 2), 
        ((1280 - 536) // 2, (720 - 625) // 2), 
        ((1280 - 710) // 2, (720 - 623) // 2),
        ((1280 - 700) // 2, (720 - 533) // 2), 
        ((1280 - 550) // 2, (720 - 533) // 2),
        ((1280 - 725) // 2, (720 - 645) // 2), 
        ((1280 - 285) // 2, (720 - 647) // 2),
        ((1280 -548) // 2, (720 - 533) // 2)
    ]

    masks = [pygame.mask.from_surface(image) for image in images]

    progress = 0
    max_progress = 60 
    bar_width = 300
    bar_height = 40
    bar_x = 70
    bar_y = 50

    heart_image = pygame.transform.scale(pygame.image.load("sayyunasset/love_button/heart.png"), (30, 30))

    stomach_area = pygame.Rect(610, 180, 280, 200)
    head_area = pygame.Rect(630, 65, 190, 80)
    tail_area = pygame.Rect(330, 160, 180, 170)

    last_mouse_x = None
    direction = None
    strokes = 0
    mouse_press = False  
    out_area = False 
    running = True

    font = pygame.font.Font(None, 36) 
    instruction_text = ""

    while running:
        screen.blit(background, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_press = True  
            
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_press = False  

            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos

                if progress < 33:
                    interaction_area = stomach_area
                    instruction_text = "Stroke the dog's stomach"
                elif progress < 66:
                    interaction_area = head_area
                    instruction_text = "Stroke the dog's head"
                else:
                    interaction_area = tail_area
                    instruction_text = "Stroke the dog's tail"

                # Check if the mouse is within the interaction area
                mouse_in_interaction_area = interaction_area.collidepoint(mouse_x, mouse_y)   

                if mouse_press:
                    if not mouse_in_interaction_area:
                        out_area = True
                    else:
                        out_area = False
                    
                    if progress < 33:
                        if out_area:
                            current_image_index = 6
                        else:
                            current_image_index = 0 if strokes % 4 == 0 else 1
                    elif progress < 66:
                        if out_area:
                            current_image_index = 7  
                        else:
                            current_image_index = 2 if strokes % 4 == 0 else 3
                    else:
                        if out_area:
                            current_image_index = 8 
                        else:
                            current_image_index = 4 if strokes % 4 == 0 else 5      
                    
                    if mouse_in_interaction_area and last_mouse_x is not None:
                        if mouse_x > last_mouse_x and direction != "right":
                            direction = "right"
                            strokes += 1
                        elif mouse_x < last_mouse_x and direction != "left":
                            direction = "left"
                            strokes += 1
                    
                    progress = (strokes / max_progress) * 100

                    last_mouse_x = mouse_x
                else:
                    last_mouse_x = None
                    direction = None

            if progress >= 100:
                running = False 

        screen.blit(images[current_image_index], image_positions[current_image_index])

        # Progress bar
        pygame.draw.rect(screen, (198, 184, 219), (65, 45, 310, 50), 2) 
        pygame.draw.rect(screen, (204, 255, 255), (bar_x, bar_y, (progress / 100) * bar_width, bar_height)) 

        heart_count = int(progress / 10) 
        for i in range(heart_count):
            screen.blit(heart_image, (bar_x + 10 + i * 30, bar_y + 5))

        text_surface = font.render(instruction_text, True, (153, 153, 255)) 
        screen.blit(text_surface, (40, 670)) 
        
        pygame.display.flip()

    screen.fill((0, 0, 0)) 
    message_font = pygame.font.Font(None, 54) 
    message_text = message_font.render("You have shower your dog with boundless care, making it blissful.", True, (255, 255, 255))  
    message_rect = message_text.get_rect(center=(1280 // 2, 720 // 2))  
    screen.blit(message_text, message_rect)
    pygame.display.flip()

    time.sleep(3)


    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False

    pygame.quit()


#debug
# running=True
# while running:
#     love_interaction()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#             break