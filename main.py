import pygame

pygame.init()

"""
Setting
"""
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Uncle cs Covid-19')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

"""
UNCLE
"""
# 1 - player - uncle.png
pisize = 128

pimg = pygame.image.load('uncle.png')
px = 100  # start X
py = 600 - pisize  # start Y
pxchange = 1

def player(x, y):
    screen.blit(pimg, (x, y))


"""
UNCLE
"""

"""
UNCLE
"""

running = True

clock = pygame.time.Clock()
FPS = 30
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # จุดเริ่มต้น
    player(px, py)
    if px <= 0:
        pxchange = 1
        px += pxchange
    elif px >= 600:
        pxchange = -1
        px += pxchange
    px += 1
    pygame.display.update()
    clock.tick(FPS)