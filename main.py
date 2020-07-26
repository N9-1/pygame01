import pygame
import math
import random
import csv

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
pspeed = 0


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
allenemy = 3

for i in range(allenemy):
    exlist.append(random.randint(50, WIDTH - esize))
    eylist.append(random.randint(0, 100))
    # ey_change_list.append(random.randint(1, 2))  # สุ่มความเร็ว enemy
    ey_change_list.append(1)  # เพิ่มความเร็วหลังจากยิงโดน
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

    if distance < (esize / 2) + (msize / 2):
        # ระยะที่ชนกัน
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
SCORE HIGHEST
"""
highest_score = 0
fontscore = pygame.font.Font('angsana.ttc', 30)

def read_highestscore():
    global highest_score
    with open(r'score.csv') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            if row:
                highest_score = int(row[0])


read_highestscore()

def highest():
    scoretext = fontscore.render(f'คะแนนสูงสุด {highest_score}', True, (0, 255, 0))
    screen.blit(scoretext, (30, 70))


"""
APPLE
"""
asize = 64

aimg = pygame.image.load('apple.png')
ax = 50
ay = 0
aychange = 1


def apple(x, y):
    screen.blit(aimg, (x, y))



"""
STATS
"""
hsize = 32
himg = pygame.image.load('heart.png')
hx = WIDTH - hsize
hy = 0
allheart = 3


def heart(x, y):
    screen.blit(himg, (x, y))


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
        gameoversound.play(1)
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
                pxchange = -10 - pspeed
            if event.key == pygame.K_RIGHT:
                pxchange = 10 + pspeed

            if event.key == pygame.K_SPACE:
                if mstate == 'ready':
                    firesound.play()
                    mx = px + 100  # ขยับไปทีมือ
                    fire_mask(mx, my)
            if event.key == pygame.K_n:
                gameover = False
                playsound = False
                allscore = 0
                allheart = 3
                hx2 = hx - hsize
                hx3 = hx2 - hsize
                hx = WIDTH - hsize
                pygame.mixer.music.play(-1)
                read_highestscore()
                # reset enemy speed
                for j in range(0, 3):
                    ey_change_list[j] = 1
                # reset enemy
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
    APPLE DROP
    """
    apple(ax, ay)
    ay += aychange
    applecollisionmulit = is_conllision(ax, ay, mx, my)
    if applecollisionmulit:
        ay = 0
        ax = random.randint(50, WIDTH - esize)
        pspeed += 20
    # ชนพื้น
    if ay == HEIGHT:
        ay = 0
        ax = random.randint(50, WIDTH - asize)


    """
    RUN MULTI ENEMY
    """
    damage = 0
    for i in range(allenemy):
        # เพิ่ม enemy speed
        if eylist[i] > HEIGHT - esize and gameover == False:
            eylist[i] = 0
            allheart -= 1
            #print(allheart)
            if allheart <= 0:
                if allscore > highest_score:
                    with open('score.csv', mode='w') as csv_file:
                        score_writer = csv.writer(csv_file)
                        score_writer.writerow([allscore])
                game_over()
                pygame.mixer.music.stop()
                for i in range(allenemy):
                    eylist[i] = 1000

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

        #print(allheart)

        hx2 = hx - hsize
        hy2 = 0
        hx3 = hx2 - hsize
        hy3 = 0
        if allheart <= 1:
            hx2 = -1000
        if allheart <= 2:
            hx3 = -1000
        if allheart == 0:
            hx = -1000
        heart(hx, hy)
        heart(hx2, hy2)
        heart(hx3, hy3)
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
    highest()
    pygame.display.update()
    screen.fill((0, 0, 0))
    clock.tick(FPS)