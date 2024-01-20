import pygame
import random

#Digunakan untuk membuat salinan yang tidak terikat.
from copy import deepcopy

#Choice digunakan untuk mengembalikan elemen acak dari sebuah list
#Randrange digunakan untuk mengembalikan angka acak dari sebuah rentang angka.
from random import choice, randrange


#Konstanta untuk ukuran layar game.
W, H = 10, 19

#Konstanta untuk ukuran santun blok.
TILE = 40

#Konstanta untuk ukuran layar game.
GAME_RES = W * TILE, H * TILE

#Konstanta untuk ukuran layar window.
RES = 700, 780

#Konstanta untuk frame rate game.
FPS = 60

#Inisialisasi Pygame.
pygame.init()
pygame.mixer.init()

#Membuat audio.
sound_move = pygame.mixer.Sound('C:\\Users\\ASUS\\Desktop\\PyGame\\FILE PENTING\\Python-Tetris-master\\audio\\Tetris-Audio.wav')

#Membuat window game.
sc = pygame.display.set_mode(RES)

#Membuat surface untuk game.
game_sc = pygame.Surface(GAME_RES)

#Membuat clock untuk mengatur frame rate game.
clock = pygame.time.Clock()

#Membuat list yang berisi objek rect untuk setiap blok pada grid.
grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

#Membuat list yang berisi bentuk-bentuk blok yang tersedia   .         
figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]


#Membuat list yang berisi objek-objek rect untuk setiap blok pada setiap bentuk.
figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for i in range(W)] for j in range(H)]

#Set kecepatan animasi game over
anim_count, anim_speed, anim_limit = 0, 60, 2000

#Membuat gambar background
bg = pygame.image.load('img/gam5.jpeg').convert()

#Membuat gambar background game.
game_bg = pygame.image.load('img/gam5.jpeg').convert()

#Membuat font.
main_font = pygame.font.Font('font/LimeBlossomCaps.ttf', 57)
font = pygame.font.Font('font/HelloSummerPersonalUse.ttf', 45)

#warna-warna pada font. 
title_tetris = main_font.render('TETRIS', True, pygame.Color('darkorange'))
title_score = font.render('score:', True, pygame.Color('green'))
title_record = font.render('record:', True, pygame.Color('purple'))

#Membuat warna yang dihasilkan selalu berbeda setiap kali fungsi tersebut dipanggil. 
get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))

#Membuat copyan blok dan di salin dengan copyan yang acak
figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()

#Membuat score secara otomatis dengan mengunakan hitungan komputer.
score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}


#Digunakan untuk memeriksa variable yang di wakilkan oleh figure itu melebihi batas atau tidak.
def check_borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True

#Digunakan untuk membaca nilai record tertinggi yang tersimpan.
def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')

#Digunakan untuk menyimpan nilai tertinggi ke file record.
#Fungsi ini menerima dua parameter, yaitu record dan score, yang masing-masing merupakan nilai record tertinggi sebelumnya dan skor saat ini.
def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))

while True:
    sound_move.play()
    record = get_record()
    dx, rotate = 0, False
    sc.blit(bg, (0, 0))
    sc.blit(game_sc, (20, 20))
    game_sc.blit(game_bg, (0, 0))
    
    # Delay for full lines
    for i in range(lines):
        pygame.time.wait(200)
        
    # Control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_UP:
                rotate = True


    # Move x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break
        
    # Move y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                anim_limit = 2000
                break
            
    # Rotate
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break
            
    # Check lines
    line, lines = H - 1, 0
    for row in range(H - 1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
        else:
            anim_speed += 3
            lines += 1
            
    # Komputer score
    score += scores[lines]
    
    # Membuat kotak
    [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]

    # Draw figure
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(game_sc, color, figure_rect)

        
    # Draw field
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(game_sc, col, figure_rect)
                
    # Draw next figure
    for i in range(4):
        figure_rect.x = next_figure[i].x * TILE + 380
        figure_rect.y = next_figure[i].y * TILE + 185
        pygame.draw.rect(sc, next_color, figure_rect)

        
    # Membuat ukuran font, letak posisi pada font dan warna pada font.
    sc.blit(title_tetris, (400, 10))
    sc.blit(title_score, (535, 550))
    sc.blit(font.render(str(score), True, pygame.Color('white')), (550, 630))
    sc.blit(title_record, (525, 400))
    sc.blit(font.render(record, True, pygame.Color('gold')), (550, 490))
    
    # Game over
    for i in range(W):
        if field[0][i]:
            set_record(record, score)
            field = [[0 for i in range(W)] for i in range(H)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            for i_rect in grid:
                pygame.draw.rect(game_sc, get_color(), i_rect)
                sc.blit(game_sc, (20, 20))
                pygame.display.flip()
                clock.tick(200)

    pygame.display.flip()
    clock.tick(FPS)

   
