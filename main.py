import pygame
import math
import random

pygame.init()

"""
Setting
"""
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Uncle cs Covid-19')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

"""
UNCLE
"""
# 1 - player - uncle.png

psize = 128

pimg = pygame.image.load('uncle.png')
px = 100  # start X
py = HEIGHT - psize  # start Y
pxchange = 0


def player(x, y):
    screen.blit(pimg, (x, y))


"""
ENEMY
"""
# 2 - enemy - virus.png

esize = 64

eimg = pygame.image.load('virus.png')
ex = 50
ey = 0
eychange = 1


def enemy(x, y):
    screen.blit(eimg, (x, y))


"""
MASK
"""
# 3 - mask - mask.png
msize = 32
mimg = pygame.image.load('mask.png')
mx = 100
my = HEIGHT - psize
mychange = 1
mstate = 'ready'


def fire_mask(x, y):
    global mstate
    mstate = 'fire'
    screen.blit(mimg, (x, y))


"""
COLLISION
"""


def is_conllision(ecx, ecy, mcx, mcy):
    # เช็คการชน
    distance = math.sqrt(math.pow(ecx - mcx, 2) + math.pow(ecy - mcy, 2))
    print(distance)
    if distance < 48:
        return True
    else:
        return False


"""
GAME LOOP
"""
running = True

clock = pygame.time.Clock()
FPS = 60
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pxchange = -10
            if event.key == pygame.K_RIGHT:
                pxchange = 10

            if event.key == pygame.K_SPACE:
                if mstate == 'ready':
                    mx = px + 100  # ขยับไปทีมือ
                    fire_mask(mx, my)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                pxchange = 0
    """
    RUN PLAYER 
    """
    player(px, py)

    if px <= 0:
        px = 0
        px += pxchange
    elif px >= WIDTH - psize:
        px = WIDTH - psize
        px += pxchange
    else:
        px += pxchange

    """
    RUN ENEMY
    """
    enemy(ex, ey)
    ey += eychange

    """
    FIRE MASK
    """
    if mstate == 'fire':
        fire_mask(mx, my)
        my = my - mychange
    # เช็คว่าชนยัง
    if my <= 0:
        my = HEIGHT - psize
        mstate = 'ready'
    # เช็คว่าชนหรือไม่
    collision = is_conllision(ex, ey, mx, my)
    if collision:
        my = HEIGHT - psize
        mstate = 'ready'
        ey = 0
        ex = random.randint(0. WIDTH - esize)
        # สุ่มตำแหน่ง ความกว้างหน้าจอ - ขนาด virus

    pygame.display.update()
    screen.fill((0, 0, 0))
    clock.tick(FPS)
