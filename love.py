import pygame
from button import Button
import part2
import part2b

def love_interaction():
    import sys
    import pygame
    import time
    
    pygame.init()

    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    icon = pygame.image.load("asset/image/gameicon.png")
    pygame.display.set_caption("Memories")
    pygame.display.set_icon(icon)

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
    bar_x = 110
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

    font = pygame.font.Font(None, 36) 
    instruction_text = ""
    start_time = pygame.time.get_ticks()  
    time_limit = 20000  

    return_img = pygame.image.load("asset/image/return.png")
    return_button = Button(50, 50, image=return_img, scale=0.27)    
  
    game_he = False  
    game_won = False
    running = True    
    elapsed_time = 0

    while running:
        screen.blit(background, (0, 0))

        current_time = pygame.time.get_ticks()
        remaining_time = max(0, (time_limit - (current_time - start_time)) // 1000)

        if remaining_time <= 0:
            game_he = True  
            elapsed_time = time_limit

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                running = False  

            if game_he:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if return_button.checkforinput(pygame.mouse.get_pos()):
                        running = False 
                        if elapsed_time <= time_limit:
                            part2b.second_b()
                        else:
                            part2.second_a()
            
            if not game_he:
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

                screen.blit(images[current_image_index], image_positions[current_image_index])

            if progress >= 100:
                elapsed_time = pygame.time.get_ticks() - start_time 
                game_won = True
                game_he = True 


        # screen.blit(images[current_image_index], image_positions[current_image_index])

        if not game_he:
            pygame.draw.rect(screen, (198, 184, 219), (105, 45, 310, 50), 2) 
            pygame.draw.rect(screen, (204, 255, 255), (bar_x, bar_y, (progress / 100) * bar_width, bar_height)) 
            screen.blit(images[current_image_index], image_positions[current_image_index])

            heart_count = int(progress / 10) 
            for i in range(heart_count):
                screen.blit(heart_image, (bar_x + 10 + i * 30, bar_y + 5))

            timer_text = font.render(f"Time: {remaining_time} sec", True, (255, 0, 0))  
            screen.blit(timer_text, (105, 120))

            text_surface = font.render(instruction_text, True, (153, 153, 255)) 
            screen.blit(text_surface, (40, 670)) 
            
        else:
            screen.fill((0, 0, 0)) 
            message_font = pygame.font.Font(None, 54)

            if progress >= 100:
                message_text1 = message_font.render("You have showered your dog with boundless care,", True, (255, 255, 255))
                message_text2 = message_font.render("making it blissful.", True, (255, 255, 255))
            else:
                message_text1 = message_font.render("You did not pet your dog enough.", True, (255, 255, 255))
                message_text2 = message_font.render("It is not very close to you and probably couldn't remember your face.", True, (255, 255, 255))

            message_rect1 = message_text1.get_rect(center=(1280 // 2, (720 // 2) - 30)) 
            message_rect2 = message_text2.get_rect(center=(1280 // 2, (720 // 2) + 30))

            screen.blit(message_text1, message_rect1)
            screen.blit(message_text2, message_rect2)

            return_button.update(screen)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.checkforinput(pygame.mouse.get_pos()):
                    running = False

        pygame.display.flip()

    return


#debug
# running=True
# while running:
#     love_interaction()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#             break