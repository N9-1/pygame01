import pygame

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
pxchange = 1

def player(x, y):
    screen.blit(pimg, (x, y))


"""
ENEMY
"""

"""
MASK
"""

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
    # จุดเริ่มต้น
    player(px, py)
    if px <= 0:
        pxchange = 1
        px += pxchange
    elif px >= WIDTH - psize:
        pxchange = -1
        px += pxchange
    else:
        px += pxchange
    px += 1
    pygame.display.update()
    clock.tick(FPS)