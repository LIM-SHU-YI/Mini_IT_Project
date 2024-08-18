import pygame
import os
import random

pygame.init()
os.environ['centered'] = '1'

# screen
screenwidth = 1280
screenheight = 720
screen = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption("Puzzle")
fpsclock = pygame.time.Clock()

# screen colors
white = (255, 250, 250)
black = (0, 0, 0)

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
        image = pygame.image.load('gameasset/1.png')
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
            for tile in self.tiles:
                if tile.rect.collidepoint(interaction.pos):
                    tile.drag = True
                    tile.dragstart = interaction.pos
                    tile.originalrect = tile.rect.copy()
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

gridsize = (5, 5)
tilesize = (puzzlewidth // gridsize[0], puzzleheight // gridsize[1])
program = puzzle(gridsize, tilesize, puzzlearea)

# Load original image
originalimage = pygame.image.load('gameasset/1.png')
originalimage = pygame.transform.scale(originalimage, (screenwidth - puzzlewidth, puzzleheight))

# Main Game Loop
running = True
puzzlesolve = False

while running:
    for interaction in pygame.event.get():
        if interaction.type == pygame.QUIT:
            running = False
        elif interaction.type == pygame.KEYDOWN:
            if interaction.key == pygame.K_r:
                program.resetpuzzle()

        program.mouseinteraction(interaction)

    if not puzzlesolve and program.checkpuzzlesolved():
        puzzlesolve = True
        print("Congratulations! You have completed the puzzle!")

    screen.fill(white)
    program.draw(screen)
    screen.blit(originalimage, (puzzlewidth, puzzley))

    if puzzlesolve:
        font = pygame.font.Font('gameasset/font.ttf', 55)
        text = font.render("Congratulations! You have completed the puzzle!", True, white)
        textrect = text.get_rect(center=(screenwidth // 2, screenheight // 2))

        framepad = 20
        framerect = textrect.inflate(framepad * 2, framepad * 2)
        pygame.draw.rect(screen, black, framerect)
        screen.blit(text, textrect)

    pygame.display.flip()
    fpsclock.tick(60)

pygame.quit()
