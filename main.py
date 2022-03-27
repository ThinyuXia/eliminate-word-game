import sys
import time
import pygame
from pygame.locals import *
import words

BORDERWIDTH = 4  # 游戏区边框宽度
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'
WINDOWWIDTH = BOXSIZE * (BOARDWIDTH + 5)
WINDOWHEIGHT = BOXSIZE * BOARDHEIGHT

MOVESIZEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1
XMARGIN = int((WINDOWWIDTH - BOARDHEIGHT * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK = (0, 0, 0)
RED = (155, 0, 0)
GREEN = (0, 155, 0)
BLUE = (0, 0, 155)
YELLOW = (155, 155, 0)
BORDERCOLOR = BLUE
BGCOLOR = BLACK


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('汉字大作战')
    font1 = pygame.font.SysFont('SimHei', 24)  # 黑体24
    font2 = pygame.font.Font(None, 72)  # GAME OVER 的字体
    font_pos_x = BOARDWIDTH * BOXSIZE + 10  # 右侧信息显示区域字体位置的X坐标
    gameover_size = font2.size('GAME OVER')
    font1_height = int(font1.size('得分')[1])
    cur_block = None  # 当前下落方块
    next_block = None  # 下一个方块
    cur_pos_x, cur_pos_y = 0, 0

    game_area = None  # 整个游戏区域
    game_area_img = {} # 对应game_area区域的图片
    game_over = True
    start = False  # 是否开始，当start = True，game_over = True 时，才显示 GAME OVER
    score = 0  # 得分
    orispeed = 0.5  # 原始速度
    speed = orispeed  # 当前速度
    pause = False  # 暂停
    last_drop_time = None  # 上次下落时间
    last_press_time = None  # 上次按键时间
    cur_block = words.get_block()

    def _dock():
        nonlocal cur_block, next_block, game_area, game_area_img, cur_pos_x, cur_pos_y, game_over, score, speed
        cur_block = words.get_block()
        cur_pos_x, cur_pos_y = (BOARDWIDTH - cur_block.end_pos.X - 1) // 2, -1 - cur_block.end_pos.Y



    def _judge(pos_x, pos_y, block):
        if pos_x < 0 or pos_x >= BOARDWIDTH or pos_x + block.end_pos.X - block.start_pos.X >= BOARDWIDTH: #判断左右横移越界情况
            return False
        if pos_y == BOARDHEIGHT - 1:
            game_area_img[pos_x , pos_y - (block.end_pos.Y - block.start_pos.Y)] = block  #存当前block左上角坐标以及block，用于后续绘制
            for i in range(pos_y - (block.end_pos.Y - block.start_pos.Y),pos_y + 1):
                for j in range(pos_x,pos_x + block.end_pos.X - block.start_pos.X + 1):
                    game_area[i][j] = 'O'
            _dock()
        else:
            for i in range(pos_x,pos_x + block.end_pos.X - block.start_pos.X + 1):
                if game_area[pos_y + 1][i] == 'O':
                    # print(game_area[pos_y + 1][pos_x:(block.end_pos.X - block.start_pos.X + 1)])
                    # sys.exit()
                    game_area_img[pos_x, pos_y - (block.end_pos.Y - block.start_pos.Y)] = block  # 存当前block左上角坐标以及block，用于后续绘制
                    for i in range(pos_y - (block.end_pos.Y - block.start_pos.Y),pos_y + 1):
                        for j in range(pos_x,pos_x + block.end_pos.X - block.start_pos.X + 1):
                            game_area[i][j] = 'O'
                    _dock()
        return True

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if game_over:
                        start = True
                        game_over = False
                        score = 0
                        last_drop_time = time.time()
                        last_press_time = time.time()
                        game_area = [['.'] * BOARDWIDTH for _ in range(BOARDHEIGHT)]
                        game_area_img = {}
                        cur_block = words.get_block()
                        next_block = words.get_block()
                        cur_pos_x, cur_pos_y = (BOARDWIDTH - cur_block.end_pos.X - 1) // 2, -1 - cur_block.end_pos.Y
                if event.key == pygame.K_UP:
                    if 0 <= cur_pos_x <= BOARDWIDTH - (cur_block.end_pos.Y - cur_block.start_pos.Y) - 1:
                        _next_block = words.get_next_block(cur_block)
                        cur_block = _next_block
                if event.key == pygame.K_LEFT:
                    if not game_over and not pause and _judge(cur_pos_x - 1, cur_pos_y, cur_block):
                        if time.time() - last_press_time > 0.1:
                            last_press_time = time.time()
                            cur_pos_x -= 1
                if event.key == pygame.K_RIGHT:
                    if not game_over and not pause and _judge(cur_pos_x + 1, cur_pos_y, cur_block):
                        if time.time() - last_press_time > 0.1:
                            last_press_time = time.time()
                            cur_pos_x += 1
                if event.key == pygame.K_DOWN:
                    if not game_over and not pause and _judge(cur_pos_x, cur_pos_y + 1, cur_block):
                        if time.time() - last_press_time > 0.1:
                            last_press_time = time.time()
                            cur_pos_y += 1

        if not game_over:  # 控制block自动下落速度
            cur_drop_time = time.time()
            if cur_drop_time - last_drop_time > speed:
                if not pause:
                    if not _judge(cur_pos_x, cur_pos_y + 1, cur_block):  # 判断到底没
                        _dock()
                    else:
                        last_drop_time = cur_drop_time
                        cur_pos_y += 1

        else:
            if start:
                print_text(screen, font2,
                           (WINDOWWIDTH - gameover_size[0]) // 2, (WINDOWHEIGHT - gameover_size[1]) // 2,
                           'GAME OVER', RED)

        _draw_background(screen)
        _draw_gridlines(screen)
        _draw_block(screen, cur_pos_x * BOXSIZE, cur_pos_y * BOXSIZE, cur_block)
        _draw_info(screen, font1, font_pos_x, font1_height, score)
        _draw_game_area(screen,game_area_img)
        print(game_area)
        pygame.display.flip()


# 画背景
def _draw_background(screen):
    # 填充背景色
    screen.fill(GRAY)
    # 画游戏区域分隔线
    pygame.draw.line(screen, BLUE,
                     (BOXSIZE * BOARDWIDTH + BORDERWIDTH // 2, 0),
                     (BOXSIZE * BOARDWIDTH + BORDERWIDTH // 2, WINDOWHEIGHT), BORDERWIDTH)


# 画单个方块
def _draw_block(screen, pos_x, pos_y, block):
    image = pygame.image.load(block.image)
    screen.blit(pygame.transform.scale(image, (
    (block.end_pos.X - block.start_pos.X + 1) * BOXSIZE, (block.end_pos.Y - block.start_pos.Y + 1) * BOXSIZE)),
                (pos_x, pos_y))

# 画已经落下的方块
def _draw_game_area(screen,game_area_img):
    for key,value in game_area_img.items():
        _draw_block(screen,key[0] * BOXSIZE,key[1]  * BOXSIZE,value)


# 画网格线
def _draw_gridlines(screen):
    # 画网格线 竖线
    for x in range(BOARDWIDTH):
        pygame.draw.line(screen, BLACK, (x * BOXSIZE, 0), (x * BOXSIZE, WINDOWHEIGHT), 1)
    # 画网格线 横线
    for y in range(BOARDHEIGHT):
        pygame.draw.line(screen, BLACK, (0, y * BOXSIZE), (BOARDWIDTH * BOXSIZE, y * BOXSIZE), 1)


def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))


# 画得分等信息
def _draw_info(screen, font, pos_x, font_height, score):
    print_text(screen, font, pos_x, 10, f'score: ')
    print_text(screen, font, pos_x, 10 + font_height + 6, f'{score}')
    print_text(screen, font, pos_x, 20 + (font_height + 6) * 2, f'speed: ')
    print_text(screen, font, pos_x, 20 + (font_height + 6) * 3, f'{score // 10000}')
    print_text(screen, font, pos_x, 30 + (font_height + 6) * 4, f'next:')


if __name__ == '__main__':
    main()
