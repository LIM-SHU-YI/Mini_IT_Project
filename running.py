import pygame

def running_race_game():
    import pygame
    import sys
    import time
    import random
    from button import Button
    import part3
    import common
    pygame.init()

    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    icon = pygame.image.load("asset/image/gameicon.png")
    pygame.display.set_caption("Memories")
    pygame.display.set_icon(icon)

    WHITE = (255, 255, 255)
    BROWN = (140, 107, 88)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)

    dogdog_width, dogdog_height = 100, 80
    dogdog_x, dogdog_y = 50, 720 - dogdog_height - 20
    dogdog_speed = 25 

    obstacle_1280, obstacle_height = 120, 80
    obstacle_speed = 8
    obstacle_spacing = 65 
    vertical_spacing = 125
    obstacles = []

    background_pic = pygame.image.load("sayyunasset/running_race/riverbackground.png")
    background_pic = pygame.transform.scale(background_pic, (1280, 720))
    dogdog_pic1 = pygame.image.load("sayyunasset/running_race/dog_1.png")
    dogdog_pic1 = pygame.transform.scale(dogdog_pic1, (dogdog_width, dogdog_height))
    dogdog_pic2 = pygame.image.load("sayyunasset/running_race/dog_2.png")
    dogdog_pic2 = pygame.transform.scale(dogdog_pic2, (dogdog_width, dogdog_height))
    dogdogswim_pic1 = pygame.image.load("sayyunasset/running_race/dogswim_1.png")
    dogdogswim_pic1 = pygame.transform.scale(dogdogswim_pic1, (dogdog_width, dogdog_height))
    dogdogswim_pic2 = pygame.image.load("sayyunasset/running_race/dogswim_2.png")
    dogdogswim_pic2 = pygame.transform.scale(dogdogswim_pic2, (dogdog_width, dogdog_height))
    current_dog_pic = dogdog_pic1
    obstacle_pic = pygame.image.load("sayyunasset/running_race/obstacleswim.png")
    obstacle_pic = pygame.transform.scale(obstacle_pic, (obstacle_1280, obstacle_height))
    win_pic = pygame.image.load("sayyunasset/running_race/end_1.png")
    win_pic = pygame.transform.scale(win_pic, (1280, 720))
    lose_pic1 = pygame.image.load("sayyunasset/running_race/end_2.png")
    lose_pic1 = pygame.transform.scale(lose_pic1, (1280, 720))
    lose_pic2 = pygame.image.load("sayyunasset/running_race/end_3.png")
    lose_pic2 = pygame.transform.scale(lose_pic2, (1280, 720))
    return_img = pygame.image.load("asset/image/return.png")
    return_button = Button(50, 50, image=return_img, scale=0.27)

    dogdog_mask = pygame.mask.from_surface(current_dog_pic)
    obstacle_mask = pygame.mask.from_surface(obstacle_pic)

    # Initialize the first obstacle
    def create_obstacle(x):
        while True:
            obstacle_y = random.randint(0, 720 - obstacle_height)
            if not obstacles or abs(obstacle_y - obstacles[-1].y) > vertical_spacing:
                break
        return pygame.Rect(x, obstacle_y, obstacle_1280, obstacle_height)
   
    # Generate initial obstacles
    last_x = 1280
    for _ in range(12):
        last_x += random.randint(obstacle_spacing, obstacle_spacing * 2)
        obstacles.append(create_obstacle(last_x))

    finishline = 1280 - 110
    left_line_x = 150

    font = pygame.font.SysFont(None, 48)

    time_limit = 20  
    start_time = time.time()

    lives = 3
    running = True
    dogdog_win = False

    # Animation toggle
    frame_toggle = True

    no_return = False


    while running and lives > 0:
        screen.blit(background_pic, (0, 0))

        time_left = time_limit - (time.time() - start_time)
        if time_left <= 0:
            time_left = 0
            lives -= 1 
            dogdog_x, dogdog_y = 50, 720 - dogdog_height - 20 
            obstacles.clear() 
            last_x = 1280
            for _ in range(12):
                last_x += random.randint(obstacle_spacing, obstacle_spacing * 2)
                obstacles.append(create_obstacle(last_x))
            start_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    dogdog_x += dogdog_speed
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    dogdog_x -= dogdog_speed
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    dogdog_y -= dogdog_speed
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    dogdog_y += dogdog_speed

                if dogdog_x < left_line_x:
                    if frame_toggle:
                        current_dog_pic = dogdog_pic1 
                    else:
                        current_dog_pic = dogdog_pic2
                else:
                    if frame_toggle:
                        current_dog_pic = dogdogswim_pic1
                    else:
                        current_dog_pic = dogdogswim_pic2

                frame_toggle = not frame_toggle

        dogdog_x = max(0, min(dogdog_x, 1280 - dogdog_width))
        dogdog_y = max(0, min(dogdog_y, 720 - dogdog_height))

        dogdog_rect = pygame.Rect(dogdog_x, dogdog_y, dogdog_width, dogdog_height)
        screen.blit(current_dog_pic, dogdog_rect.topleft)

        dogdog_mask = pygame.mask.from_surface(current_dog_pic)

        # pygame.draw.line(screen, (255, 255, 255), (left_line_x, 0), (left_line_x, SCREEN_HEIGHT), 5)

        for obstacle in obstacles:
            obstacle.x -= obstacle_speed
            if obstacle.x <= left_line_x:
                obstacles.remove(obstacle)
                new_obstacle_x = finishline
                obstacles.append(create_obstacle(new_obstacle_x))

            screen.blit(obstacle_pic, obstacle.topleft)

            obstacle_rect = pygame.Rect(obstacle.x, obstacle.y, obstacle_1280, obstacle_height)

            # Check for pixel-perfect collision
            offset = (obstacle_rect.x - dogdog_rect.x, obstacle_rect.y - dogdog_rect.y)
            if dogdog_mask.overlap(obstacle_mask, offset):
                lives -= 1 
                dogdog_x, dogdog_y = 50, 720 - dogdog_height - 20 
                obstacles.clear() 
                last_x = finishline
                for _ in range(12):
                    last_x += random.randint(obstacle_spacing, obstacle_spacing * 2)
                    obstacles.append(create_obstacle(last_x))
                start_time = time.time()

        # pygame.draw.line(screen, BLACK, (finishline, 0), (finishline, 720), 5)

        timer_text = font.render(f"Time Left: {int(time_left)}s", True, BROWN)
        lives_text = font.render(f"Lives: {lives}", True, BROWN)
        screen.blit(timer_text, (10, 10))
        screen.blit(lives_text, (10, 50))

        if dogdog_x + dogdog_width >= finishline:
            dogdog_win = True
            running = False

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    screen.blit(background_pic, (0, 0))
    if dogdog_win:
        no_return = False
        screen.blit(win_pic, (0, 0))
        common.sopro.play()
        endtxt = font.render("You Win!", True, GREEN)
        return_button.update(screen)
        pygame.display.flip()

    else:
        no_return = True
        common.hahaha.play()
        screen.blit(lose_pic1, (0, 0))
        pygame.display.flip()
        pygame.time.delay(1000)
        screen.blit(lose_pic2, (0, 0))
        endtxt = font.render("YOU LOSE!", True, RED)

    screen.blit(endtxt, (1280 // 2 - 100, 720 // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        if no_return:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if return_button.checkforinput(event.pos):
                            part3.first_scene()
                            waiting = False

    pygame.quit()
    sys.exit()


# Debug
# running = True
# while running:
#     running_race_game()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#             break