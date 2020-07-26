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

background = pygame.image.load('BG.jpg')
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
MULTI-ENEMY
"""
exlist = []
eylist = []
ey_change_list = []  # enemy speed
allenemy = 5

for i in range(allenemy):
    exlist.append(random.randint(50, WIDTH - esize))
    eylist.append(random.randint(0, 100))
    #ey_change_list.append(random.randint(1, 2))  # สุ่มความเร็ว enemy
    ey_change_list.append(1)
"""
MASK
"""
# 3 - mask - mask.png
msize = 32
mimg = pygame.image.load('mask.png')
mx = 100
my = HEIGHT - psize
mychange = 20
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
SCORE
"""
allscore = 0
font = pygame.font.Font('angsana.ttc', 50)


def showscore():
    score = font.render(f'คะแนน: {allscore} คะแนน', True, (255, 255, 255))
    screen.blit(score, (30, 30))

"""
SOUND
"""
pygame.mixer.music.load('oldvideogame.wav')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

firesound = pygame.mixer.Sound('whoosh.ogg')
esound = pygame.mixer.Sound('roblox_death_sound_effect.ogg')
gameoversound = pygame.mixer.Sound('Wasted_-Busted_-Mission-Failed-Sound-effects-with-text.ogg')
"""
GAME OVER
"""
fontover = pygame.font.Font('angsana.ttc', 80)
fontnew = pygame.font.Font('angsana.ttc', 20)
playsound = False
gameover = False
def game_over():
    global playsound
    global gameover
    if playsound == False:
        gameoversound.play()
        playsound = True
    if gameover == False:
        gameover = True

"""
GAME LOOP
"""
running = True

clock = pygame.time.Clock()
FPS = 60
while running:

    screen.blit(background, (0, 0))
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
                    firesound.play()
                    mx = px + 100  # ขยับไปทีมือ
                    fire_mask(mx, my)
            if event.key == pygame.K_n:
                gameover = False
                playsound = False
                allscore = 0
                pygame.mixer.music.play(-1)
                for i in range(allenemy):
                    eylist[i] = random.randint(0, 100)
                    exlist[i] = random.randint(50, WIDTH - psize)

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
    '''
    enemy(ex, ey)
    ey += eychange
    # ชนพื้น
    if ey == HEIGHT:
        ey = 0
        ex = random.randint(50, WIDTH - esize)
    '''

    """
    RUN MULTI ENEMY
    """
    for i in range(allenemy):
        # เพิ่ม enemy speed
        if eylist[i] > HEIGHT - esize and gameover == False:
            for i in range(allenemy):
                eylist[i] = 1000
            game_over()
            pygame.mixer.music.stop()
            break
        if gameover == True:
            overtext = fontover.render('GAME OVER', True, (255, 0, 0))
            screen.blit(overtext, (300, 300))
            overtext2 = fontnew.render('pass [N] new game', True, (255, 255, 255))
            screen.blit(overtext2, (350, 400))

        eylist[i] += ey_change_list[i]
        collisionmulit = is_conllision(exlist[i], eylist[i], mx, my)
        if collisionmulit:
            my = HEIGHT - psize
            mstate = 'ready'
            eylist[i] = 0
            exlist[i] = random.randint(50, WIDTH - esize)
            allscore += 1
            ey_change_list[i] += 1
            esound.play()

        enemy(exlist[i], eylist[i])

        # ชนพื้น
        '''
        if eylist[i] == HEIGHT:
            eylist[i] = 0
            exlist[i] = random.randint(50, WIDTH - esize)
        '''
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
        ex = random.randint(50, WIDTH - esize)
        allscore += 1
        # สุ่มตำแหน่ง ความกว้างหน้าจอ - ขนาด virus
    showscore()
    pygame.display.update()
    screen.fill((0, 0, 0))
    clock.tick(FPS)
