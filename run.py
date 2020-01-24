import sys, pygame, random
from pygame.locals import *
from pygame.sprite import *


class Snake(Sprite):
    global GRID
    global CARCASSPOS

    def __init__(self, color):
        Sprite.__init__(self)
        posx, posy = random.randint(3, GRIDWIDTH - 4), random.randint(3, GRIDHEIGHT - 4)
        self.pos = [[posx, posy]]
        GRID[posx][posy] = SNAKE
        self.direction = None
        self.canMove = True
        self.color = color
        self.speed = len(self.pos)
        left, top = leftTopCoordsOfBox(self.pos[0][0], self.pos[0][1])
        pygame.draw.rect(DISPLAYSURF, self.color, (left, top, BOXSIZE, BOXSIZE))
        pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE), MARGIN)

    def move(self):
        front = self.pos[-1].copy()
        increase = False
        for i in range(len(CARCASSPOS)):
            if self.pos[-1] == CARCASSPOS[i]:
                CARCASSPOS.pop(i)
                increase = True
                self.speed += .1
                break
        if not increase and self.pos[-1] == FOODPOS:
            newFood()
            increase = True
            self.speed += 1
        if not increase:
            if self.pos[-1] == POISPOS:
                newPoison()
                if len(self.pos) == 1:
                    self.die()
                    return None
                else:
                    end = self.pos.pop(0)
                    emptyGrid(*end)
                    left, top = leftTopCoordsOfBox(end[0], end[1])
                    pygame.draw.rect(DISPLAYSURF, BLACK, (left, top, BOXSIZE, BOXSIZE))
                    pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE), MARGIN)
                    self.speed -= 1
            elif SPEED is FAST and self.pos[-1] == FASTPOS:
                newFast()
                self.speed += 1
            elif SPEED is FAST and self.pos[-1] == SLOWPOS:
                newSlow()
                self.speed -= 1
        if not increase:
            end = self.pos.pop(0)
            emptyGrid(*end)
            left, top = leftTopCoordsOfBox(*end)
            pygame.draw.rect(DISPLAYSURF, BLACK, (left, top, BOXSIZE, BOXSIZE))
            pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE), MARGIN)

        if self.direction == LEFT:
            front[0] -= 1
        elif self.direction == RIGHT:
            front[0] += 1
        elif self.direction == UP:
            front[1] -= 1
        elif self.direction == DOWN:
            front[1] += 1

        self.pos.append(front)

        left, top = leftTopCoordsOfBox(*self.pos[-1])
        pygame.draw.rect(DISPLAYSURF, self.color, (left, top, BOXSIZE, BOXSIZE))
        pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE), MARGIN)

        dead = False
        if front[0] < 0 or GRIDWIDTH <= front[0] or front[1] < 0 or front[
            1] >= GRIDHEIGHT:
            self.pos.pop(-1)
            self.die()
            dead = True
        for x in range(len(GRID)):
            for y in range(len(GRID[x])):
                if GRID[x][y] is SNAKE and (x == front[0] and y == front[1]):
                    self.die()
                    dead = True
                    break
        if not dead:
            makeSnake(*front)

    def die(self):
        for i in range(len(self.pos)):
            left, top = leftTopCoordsOfBox(*self.pos[i])
            pygame.draw.rect(DISPLAYSURF, DRED, (left, top, BOXSIZE, BOXSIZE))
            pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE), MARGIN)
            GRID[self.pos[i][0]][self.pos[i][1]] = None
            CARCASSPOS.append(self.pos[i])
        self.pos = [[random.randint(3, GRIDWIDTH - 4), random.randint(3, GRIDHEIGHT - 4)]]
        self.direction = None
        self.speed = len(self.pos)
        left, top = leftTopCoordsOfBox(self.pos[0][0], self.pos[0][1])
        pygame.draw.rect(DISPLAYSURF, self.color, (left, top, BOXSIZE, BOXSIZE))
        pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE), MARGIN)



WINDOWWIDTH = 1500
WINDOWHEIGHT = 750
BOXSIZE = int(WINDOWWIDTH / 50)
MARGIN = 1
GRIDWIDTH = int(WINDOWWIDTH / BOXSIZE)
GRIDHEIGHT = int(WINDOWHEIGHT / BOXSIZE)

GRID = []
for i in range(GRIDWIDTH):
    column = [None] * GRIDHEIGHT
    GRID.append(column)

LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'

NORMAL = 'normal'
FAST = 'kachow'

SNAKE = 'snake'
FOOD = 'food'
POISON = 'poison'
SLOW = 'slow'
CARCASS = 'carcass'

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (255, 0, 255)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
LBLUE = (0, 255, 255)
RED = (255, 0, 0)
DRED = (150, 0, 0)
YELLOW = (255, 255, 0)


def main():
    global DISPLAYSURF, SNAKE1, SNAKE2, FOODPOS, POISPOS, FASTPOS, SLOWPOS, SPEED, NUMPLAYER, CARCASSPOS
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), RESIZABLE)
    pygame.display.set_caption('Snake')

    DISPLAYSURF.fill(BLACK)
    font = pygame.font.SysFont('Comic Sans', 75)
    text = font.render('Should the speed remain constant or get faster?', 1, WHITE)
    text_rect = text.get_rect(center=(750, 50))
    DISPLAYSURF.blit(text, text_rect)

    normfont = pygame.font.SysFont('Comic Sans', 100)
    normtext = normfont.render('Constant Speed', 1, WHITE)
    normtext_rect = normtext.get_rect(center=(750, 250))
    DISPLAYSURF.blit(normtext, normtext_rect)

    fastfont = pygame.font.SysFont('Comic Sans', 100)
    fasttext = fastfont.render('Big Boy Speed', 1, WHITE)
    fasttext_rect = fasttext.get_rect(center=(750, 600))
    DISPLAYSURF.blit(fasttext, fasttext_rect)

    pygame.display.update()

    noClick = True
    while noClick:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                if normtext_rect.collidepoint(pygame.mouse.get_pos()):
                    SPEED = NORMAL
                    noClick = False
                elif fasttext_rect.collidepoint(pygame.mouse.get_pos()):
                    SPEED = FAST
                    noClick = False

    DISPLAYSURF.fill(BLACK)
    numfont = pygame.font.SysFont('Comic Sans', 100)
    numtext = numfont.render('How many players?', 1, WHITE)
    numtext_rect = numtext.get_rect(center=(750, 50))
    DISPLAYSURF.blit(numtext, numtext_rect)

    onefont = pygame.font.SysFont('Comic Sans', 100)
    onetext = onefont.render('Onnnnnnnnnnnnnnnnnnnnnne', 1, WHITE)
    onetext_rect = onetext.get_rect(center=(750, 250))
    DISPLAYSURF.blit(onetext, onetext_rect)

    twofont = pygame.font.SysFont('Comic Sans', 100)
    twotext = twofont.render('Twwwwwwwwwwwwwwwwo', 1, WHITE)
    twotext_rect = twotext.get_rect(center=(750, 600))
    DISPLAYSURF.blit(twotext, twotext_rect)

    pygame.display.update()

    noClick = True
    while noClick:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                if onetext_rect.collidepoint(pygame.mouse.get_pos()):
                    NUMPLAYER = 1
                    noClick = False
                elif twotext_rect.collidepoint(pygame.mouse.get_pos()):
                    NUMPLAYER = 2
                    noClick = False

    drawScreen()
    SNAKE1 = Snake(BLUE)
    if NUMPLAYER >= 2:
        SNAKE2 = Snake(YELLOW)
    FOODPOS = [random.randint(0, GRIDWIDTH), random.randint(0, GRIDHEIGHT)]
    newFood()
    POISPOS = [random.randint(0, GRIDWIDTH), random.randint(0, GRIDHEIGHT)]
    newPoison()
    if SPEED is FAST:
        FASTPOS = [random.randint(0, GRIDWIDTH), random.randint(0, GRIDHEIGHT)]
        newFast()
        SLOWPOS = [random.randint(0, GRIDWIDTH), random.randint(0, GRIDHEIGHT)]
        newSlow()

    CARCASSPOS = []

    time = pygame.time.get_ticks()
    time2 = pygame.time.get_ticks()
    t = 0
    t2 = 0
    while True:
        dt = pygame.time.get_ticks() - time
        time = pygame.time.get_ticks()
        dt2 = pygame.time.get_ticks() - time2
        time2 = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                print("Resize")
                # tempSurf = DISPLAYSURF.copy()
                w = min(event.w, event.h)
                pygame.display.set_mode((w, int(w/2)), RESIZABLE)
            elif event.type == KEYDOWN:
                if event.key == K_LEFT and not SNAKE1.direction == RIGHT:
                    SNAKE1.direction = LEFT
                    SNAKE1.move()
                    t = 0
                elif event.key == K_RIGHT and not SNAKE1.direction == LEFT:
                    SNAKE1.direction = RIGHT
                    SNAKE1.move()
                    t = 0
                elif event.key == K_UP and not SNAKE1.direction == DOWN:
                    SNAKE1.direction = UP
                    SNAKE1.move()
                    t = 0
                elif event.key == K_DOWN and not SNAKE1.direction == UP:
                    SNAKE1.direction = DOWN
                    SNAKE1.move()
                    t = 0

                if NUMPLAYER >= 2:
                    if event.key == K_a and not SNAKE2.direction == RIGHT:
                        SNAKE2.direction = LEFT
                        SNAKE2.move()
                        t2 = 0
                    elif event.key == K_d and not SNAKE2.direction == LEFT:
                        SNAKE2.direction = RIGHT
                        SNAKE2.move()
                        t2 = 0
                    elif event.key == K_w and not SNAKE2.direction == DOWN:
                        SNAKE2.direction = UP
                        SNAKE2.move()
                        t2 = 0
                    elif event.key == K_s and not SNAKE2.direction == UP:
                        SNAKE2.direction = DOWN
                        SNAKE2.move()
                        t2 = 0
        if SNAKE1.direction:
            t += dt
            if SPEED == NORMAL:
                while t >= 150:
                    t -= 150
                    SNAKE1.move()
            elif SPEED == FAST:
                while t >= 200 * pow(.9, SNAKE1.speed - 1):
                    t -= 200 * pow(.9, SNAKE1.speed - 1)
                    SNAKE1.move()

        if NUMPLAYER >= 2 and SNAKE2.direction:
            t2 += dt2
            if SPEED == NORMAL:
                while t2 >= 200:
                    t2 -= 200
                    SNAKE2.move()
            elif SPEED == FAST:
                while t2 >= 200 * pow(.9, SNAKE2.speed - 1):
                    t2 -= 200 * pow(.9, SNAKE2.speed - 1)
                    SNAKE2.move()
        pygame.display.update()


def newFood():
    global FOODPOS
    FOODPOS = [random.randint(0, GRIDWIDTH - 1), random.randint(0, GRIDHEIGHT - 1)]
    good = False
    while good:
        if GRID[FOODPOS[0]][FOODPOS[1]] is SNAKE or FOODPOS == POISPOS or FOODPOS == FASTPOS or FOODPOS == SLOWPOS:
            FOODPOS = [random.randint(0, GRIDWIDTH - 1), random.randint(0, GRIDHEIGHT - 1)]
        else:
            good = True

    left, top = leftTopCoordsOfBox(*FOODPOS)
    pygame.draw.rect(DISPLAYSURF, LBLUE, (left, top, BOXSIZE, BOXSIZE))


def newPoison():
    global POISPOS
    POISPOS = [random.randint(0, GRIDWIDTH - 1), random.randint(0, GRIDHEIGHT - 1)]
    good = False
    while good:
        if GRID[POISPOS[0]][POISPOS[1]] is SNAKE or POISPOS == FOODPOS or POISPOS == FASTPOS or POISPOS == SLOWPOS:
            POISPOS = [random.randint(0, GRIDWIDTH - 1), random.randint(0, GRIDHEIGHT - 1)]
        else:
            good = True

    left, top = leftTopCoordsOfBox(*POISPOS)
    pygame.draw.rect(DISPLAYSURF, PURPLE, (left, top, BOXSIZE, BOXSIZE))


def newFast():
    global FASTPOS
    FASTPOS = [random.randint(0, GRIDWIDTH - 1), random.randint(0, GRIDHEIGHT - 1)]
    good = False
    while good:
        if GRID[FASTPOS[0]][FASTPOS[1]] is SNAKE or FASTPOS == FOODPOS or FASTPOS == POISPOS or FASTPOS == SLOWPOS:
            FASTPOS = [random.randint(0, GRIDWIDTH - 1), random.randint(0, GRIDHEIGHT - 1)]
        else:
            good = True

    left, top = leftTopCoordsOfBox(*FASTPOS)
    pygame.draw.rect(DISPLAYSURF, GREEN, (left, top, BOXSIZE, BOXSIZE))


def newSlow():
    global SLOWPOS
    SLOWPOS = [random.randint(0, GRIDWIDTH - 1), random.randint(0, GRIDHEIGHT - 1)]
    good = False
    while good:
        if GRID[SLOWPOS[0]][SLOWPOS[1]] is SNAKE or SLOWPOS == FOODPOS or SLOWPOS == POISPOS or SLOWPOS == FASTPOS:
            SLOWPOS = [random.randint(0, GRIDWIDTH - 1), random.randint(0, GRIDHEIGHT - 1)]
        else:
            good = True

    left, top = leftTopCoordsOfBox(*SLOWPOS)
    pygame.draw.rect(DISPLAYSURF, RED, (left, top, BOXSIZE, BOXSIZE))


def emptyGrid(x, y):
    global GRID
    GRID[x][y] = None


def makeSnake(x, y):
    global GRID
    GRID[x][y] = SNAKE



def drawScreen():
    DISPLAYSURF.fill(BLACK)
    for x in range(GRIDWIDTH):
        for y in range(GRIDWIDTH):
            boxx, boxy = leftTopCoordsOfBox(x, y)
            pygame.draw.rect(DISPLAYSURF, WHITE, (boxx, boxy, BOXSIZE, BOXSIZE), MARGIN)


def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * BOXSIZE
    top = boxy * BOXSIZE
    return left, top


if __name__ == '__main__':
    main()
