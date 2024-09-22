import pygame

def running_race_game():  
    import pygame
    import sys
    import time
    import random

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

    dogdog_width, dogdog_height = 90, 80
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
    current_dog_pic = dogdog_pic1
    obstacle_pic = pygame.image.load("sayyunasset/running_race/obstacle_1.png")
    obstacle_pic = pygame.transform.scale(obstacle_pic, (obstacle_1280, obstacle_height))
    win_pic = pygame.image.load("sayyunasset/running_race/end_1.png")
    win_pic = pygame.transform.scale(win_pic, (1280, 720))
    lose_pic1 = pygame.image.load("sayyunasset/running_race/end_2.png")
    lose_pic1 = pygame.transform.scale(lose_pic1, (1280, 720))
    lose_pic2 = pygame.image.load("sayyunasset/running_race/end_3.png")
    lose_pic2 = pygame.transform.scale(lose_pic2, (1280, 720))

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
    for _ in range(15):
        last_x += random.randint(obstacle_spacing, obstacle_spacing * 2)
        obstacles.append(create_obstacle(last_x))

    finishline = 1280 - 100

    font = pygame.font.SysFont(None, 48)

    time_limit = 20  
    start_time = time.time()

    lives = 2
    running = True
    dogdog_win = False

    # Animation toggle
    frame_toggle = True

    while running and lives > 0:
        screen.blit(background_pic, (0, 0))

        time_left = time_limit - (time.time() - start_time)
        if time_left <= 0:
            time_left = 0
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    dogdog_x += dogdog_speed
                if event.key == pygame.K_LEFT:
                    dogdog_x -= dogdog_speed
                if event.key == pygame.K_UP:
                    dogdog_y -= dogdog_speed
                if event.key == pygame.K_DOWN:
                    dogdog_y += dogdog_speed

                if frame_toggle:
                    current_dog_pic = dogdog_pic2
                else:
                    current_dog_pic = dogdog_pic1
                frame_toggle = not frame_toggle

        dogdog_x = max(0, min(dogdog_x, 1280 - dogdog_width))
        dogdog_y = max(0, min(dogdog_y, 720 - dogdog_height))

        dogdog_rect = pygame.Rect(dogdog_x, dogdog_y, dogdog_width, dogdog_height)
        screen.blit(current_dog_pic, dogdog_rect.topleft)

        dogdog_mask = pygame.mask.from_surface(current_dog_pic)

        for obstacle in obstacles:
            obstacle.x -= obstacle_speed
            if obstacle.x < -obstacle_1280:
                obstacles.remove(obstacle)
                new_obstacle_x = 1280 + obstacle_1280
                obstacles.append(create_obstacle(new_obstacle_x))

            screen.blit(obstacle_pic, obstacle.topleft)

            obstacle_rect = pygame.Rect(obstacle.x, obstacle.y, obstacle_1280, obstacle_height)

            # Check for pixel-perfect collision
            offset = (obstacle_rect.x - dogdog_rect.x, obstacle_rect.y - dogdog_rect.y)
            if dogdog_mask.overlap(obstacle_mask, offset):
                lives -= 1 
                dogdog_x, dogdog_y = 50, 720 - dogdog_height - 20 
                obstacles.clear() 
                last_x = 1280
                for _ in range(15):
                    last_x += random.randint(obstacle_spacing, obstacle_spacing * 2)
                    obstacles.append(create_obstacle(last_x))
                start_time = time.time()


        pygame.draw.line(screen, BLACK, (finishline, 0), (finishline, 720), 5)

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
        screen.blit(win_pic,(0, 0))
        endtxt = font.render("You Win!", True, GREEN)
        screen.blit(endtxt, (1280 // 2 - 100, 720 // 2))

    else:
        screen.blit(lose_pic1, (0, 0))
        pygame.display.flip()
        pygame.time.delay(1000)
        screen.blit(lose_pic2, (0, 0))
        endtxt = font.render("YOU LOSE!", True, RED)
        screen.blit(endtxt, (1280 // 2 - 100, 720 // 2))

    pygame.display.flip()

    time.sleep(500)


#debug
# running=True
# while running:
#     running_race_game()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#             break

