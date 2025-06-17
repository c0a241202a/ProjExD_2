import os
import random
import sys
import time
import pygame as pg

WIDTH, HEIGHT = 1100, 650
DELTA = {  # 移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def get_kk_img(sum_mv: tuple[int, int], base_img: pg.Surface) -> pg.Surface:
    kk_imgs = {
        (0, 0): base_img,
        (+5, 0): pg.transform.flip(base_img, True, False),  # 左
        (+5, -5): pg.transform.rotozoom(pg.transform.flip(base_img, True, False), 45, 1.0),  # 左下
        (0, +5): pg.transform.rotozoom(base_img, 90, 1.0),  # 下
        (-5, +5): pg.transform.rotozoom(base_img, 45, 1.0),  # 右下
        (-5, 0): base_img,  # 右
        (-5, -5): pg.transform.rotozoom(base_img, -45, 1.0),  # 右上
        (0, -5): pg.transform.rotozoom(base_img, -90, 1.0),  # 上
        (+5, +5): pg.transform.rotozoom(pg.transform.flip(base_img, True, False), -45, 1.0),  # 左上
    }
    return kk_imgs.get(tuple(sum_mv), base_img)


def make_accel_bombs():
    bb_accs = [a for a in range(1, 11)]
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs

def show_game_over(screen, kk_dead_img):
    blackout = pg.Surface((WIDTH, HEIGHT))
    blackout.set_alpha(128)
    blackout.fill((0, 0, 0))

    font = pg.font.SysFont(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))

    kk_img = pg.transform.rotozoom(kk_dead_img, 0, 0.8)
    left_rect = kk_img.get_rect(center=(text_rect.left - 80, HEIGHT//2))
    right_rect = kk_img.get_rect(center=(text_rect.right + 80, HEIGHT//2))

    screen.blit(blackout, (0, 0))
    screen.blit(kk_img, left_rect)
    screen.blit(kk_img, right_rect)
    screen.blit(text, text_rect)
    pg.display.update()
    time.sleep(5)

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bb_imgs, bb_accs = make_accel_bombs()
    kk_dead_img = pg.image.load("fig/8.png")
    bg_img = pg.image.load("fig/pg_bg.jpg")
    base_kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_img = base_kk_img
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        if kk_rct.colliderect(bb_rct):
            show_game_over(screen, kk_dead_img)
            return

        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        kk_img = get_kk_img(tuple(sum_mv), base_kk_img)
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(kk_img, kk_rct)

        idx = min(tmr // 500, 9)
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]
        bb_img = bb_imgs[idx]
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
