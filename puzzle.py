import pygame
game_completed = False

def puzzle():   
    global game_completed
    import pygame
    import os
    import random
    from button import Button
    import common

    pygame.init()
    os.environ['centered'] = '1'

    # screen
    screenwidth = 1280
    screenheight = 720
    screen = pygame.display.set_mode((screenwidth, screenheight))
    pygame.display.set_caption("Memories")
    fpsclock = pygame.time.Clock()

    # screen colors
    white = (255, 250, 250)
    black = (0, 0, 0)
    gray = (128, 128, 128)

    return_img = pygame.image.load("asset/image/return.png")
    return_button = Button(50, 50, image=return_img, scale=0.27)   


    # Puzzle Pieces
    class puzzlepiece:
        def __init__(self, image, position, index):
            self.image = image
            self.rect = self.image.get_rect(topleft=position)
            self.originalposition = position
            self.index = index
            self.drag = False

    class puzzle:
        def __init__(self, gridsize, tilesize, puzzlearea):
            self.gridsize = gridsize
            self.tilesize = tilesize
            self.tiles = []
            self.puzzlearea = puzzlearea
            self.init_puzzle()

        def init_puzzle(self):
            image = pygame.image.load('kitasset/gameasset/1.png')
            scaledwidth = self.gridsize[0] * self.tilesize[0]
            scaledheight = self.gridsize[1] * self.tilesize[1]
            image = pygame.transform.scale(image, (scaledwidth, scaledheight))

            for row in range(self.gridsize[1]):
                for col in range(self.gridsize[0]):
                    x = self.puzzlearea.left + col * self.tilesize[0]
                    y = self.puzzlearea.top + row * self.tilesize[1]
                    tileimage = image.subsurface(pygame.Rect(col * self.tilesize[0], row * self.tilesize[1], self.tilesize[0], self.tilesize[1]))
                    tile = puzzlepiece(tileimage, (x, y), row * self.gridsize[0] + col)
                    self.tiles.append(tile)

            self.resetpuzzle()

        def resetpuzzle(self):
            position = [(tile.originalposition[0], tile.originalposition[1]) for tile in self.tiles]
            random.shuffle(position)
            for i, tile in enumerate(self.tiles):
                tile.rect.topleft = position[i]

        def draw(self, screen):
            pygame.draw.rect(screen, black, self.puzzlearea, 3)
            for row in range(self.gridsize[1] + 1):
                pygame.draw.line(screen, black, 
                                (self.puzzlearea.left, self.puzzlearea.top + row * self.tilesize[1]), 
                                (self.puzzlearea.right, self.puzzlearea.top + row * self.tilesize[1]), 2)
            for col in range(self.gridsize[0] + 1):
                pygame.draw.line(screen, black, 
                                (self.puzzlearea.left + col * self.tilesize[0], self.puzzlearea.top), 
                                (self.puzzlearea.left + col * self.tilesize[0], self.puzzlearea.bottom), 2)
            for tile in self.tiles:
                screen.blit(tile.image, tile.rect.topleft)

        def mouseinteraction(self, interaction):
            if interaction.type == pygame.MOUSEBUTTONDOWN:
                for i, tile in enumerate(self.tiles):
                    if tile.rect.collidepoint(interaction.pos):
                        tile.drag = True
                        tile.dragstart = interaction.pos
                        tile.originalrect = tile.rect.copy()
                        self.tiles.append(self.tiles.pop(i))
                        break
            elif interaction.type == pygame.MOUSEBUTTONUP:
                for tile in self.tiles:
                    if tile.drag:
                        tile.drag = False
                        self.snapgrid(tile)
            elif interaction.type == pygame.MOUSEMOTION:
                for tile in self.tiles:
                    if tile.drag:
                        newx = interaction.pos[0] - tile.rect.width // 2
                        newy = interaction.pos[1] - tile.rect.height // 2

                        newx = max(self.puzzlearea.left, min(newx, self.puzzlearea.right - tile.rect.width))
                        newy = max(self.puzzlearea.top, min(newy, self.puzzlearea.bottom - tile.rect.height))

                        tile.rect.topleft = (newx, newy)

        def snapgrid(self, tile):
            closestcol = round((tile.rect.x - self.puzzlearea.left) / self.tilesize[0])
            closestrow = round((tile.rect.y - self.puzzlearea.top) / self.tilesize[1])

            newx = self.puzzlearea.left + closestcol * self.tilesize[0]
            newy = self.puzzlearea.top + closestrow * self.tilesize[1]

            if 0 <= closestcol < self.gridsize[0] and 0 <= closestrow < self.gridsize[1]:
                targetpos = (newx, newy)
                for t in self.tiles:
                    if t.rect.topleft == targetpos and t != tile:
                        t.rect.topleft = tile.originalrect.topleft
                        break
                tile.rect.topleft = targetpos

        def checkpuzzlesolved(self):
            return all(tile.rect.topleft == tile.originalposition for tile in self.tiles)

    # Puzzle Area Setup
    puzzlewidth = 640
    puzzleheight = 640
    puzzlearea = pygame.Rect(0, 0, puzzlewidth, puzzleheight)
    puzzley = (screenheight - puzzleheight) // 2
    puzzlearea.top = puzzley

    # gridsize = (3, 3)           #change to more ez when debug
    gridsize = (5, 5)
    tilesize = (puzzlewidth // gridsize[0], puzzleheight // gridsize[1])
    program = puzzle(gridsize, tilesize, puzzlearea)

    # Load original image
    originalimage = pygame.image.load('kitasset/gameasset/1.png')
    originalimage = pygame.transform.scale(originalimage, (screenwidth - puzzlewidth, puzzleheight))

    # Main Game Loop
    running = True
    puzzlesolve = False
    gameover=False
    game_is_done = False
    wingame = False

    # timer
    starttime=pygame.time.get_ticks()
    timer=1*60*1000+46*1000
    # timer=5*1000 #change when use for debug
    

    # font
    large=pygame.font.Font ('kitasset/gameasset/font.ttf',60)
    small=pygame.font.Font ('kitasset/gameasset/font.ttf',40)

    while running:
        currenttime=pygame.time.get_ticks()
        timeleft=max(0,timer-(currenttime-starttime))
        minutes=timeleft//60000
        sec=(timeleft%60000)//1000

        for interaction in pygame.event.get():
            if interaction.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif interaction.type == pygame.KEYDOWN:
                if interaction.key == pygame.K_r:
                    program.resetpuzzle()
                    puzzlesolve=False
                    gameover=False
                    starttime=pygame.time.get_ticks()

            program.mouseinteraction(interaction)

            if interaction.type == pygame.MOUSEBUTTONDOWN:
                if common.music_button.visible and common.music_button.checkforinput(pygame.mouse.get_pos()):
                    common.click.play()
                    common.music_on_off()
                elif common.mute_button.visible and common.mute_button.checkforinput(pygame.mouse.get_pos()):
                    common.click.play()
                    common.music_on_off()


        if not puzzlesolve and program.checkpuzzlesolved():
            puzzlesolve = True
            gameover=True
            wingame = True
            finishcaption=("Congratulations! You have completed the puzzle!")
            

        if timeleft <= 0 and not puzzlesolve:
            gameover=True
            wingame = False
            finishcaption="You forgot your owner's face, huh?"

        screen.fill(white)
        program.draw(screen)
        screen.blit(originalimage, (puzzlewidth, puzzley))


        (timsha, timsha_rect), (tim, tim_rect) = common.text_with_shadow(f"{minutes:01}:{sec:02}", common.cutedisplay(40), "Black", "White", (1135, 70), shadow_offset=(4, 5))
        screen.blit(timsha, timsha_rect)
        screen.blit(tim, tim_rect)
        

        if common.music_button.visible:
            common.music_button.update(screen)
        if common.mute_button.visible:
            common.mute_button.update(screen)

        if gameover:
            if wingame:
                return_button.update(screen)
                pygame.draw.rect(screen,black,screen.get_rect())
                text=large.render(finishcaption,True,white)
                textrect=text.get_rect(center=(screenwidth//2,screenheight//2))
                screen.blit(text,textrect)
                return_button.update(screen)

                if interaction.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if interaction.type == pygame.MOUSEBUTTONDOWN:
                    if return_button.checkforinput(pygame.mouse.get_pos()):
                        common.click.play()
                        game_is_done = True

            else:
                pygame.draw.rect(screen,black,screen.get_rect())
                text=large.render(finishcaption,True,white)
                textrect=text.get_rect(center=(screenwidth//2,screenheight//2))
                screen.blit(text,textrect)

                if interaction.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                        
            pygame.display.flip()


        if game_is_done:
            game_completed = True
            return

        pygame.display.flip()
        fpsclock.tick(60)


# debug
# running=True
# while running:
#     puzzle()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#             break
