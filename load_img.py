import pygame as pg
def load_arrows():
    up_arrow = pg.image.load("lib/bg_pics/arrow_up.png")
    down_arrow = pg.image.load("lib/bg_pics/arrow_down.png")
    boarder = pg.image.load("lib/bg_pics/board.png")
    boarder_bg = pg.image.load("lib/bg_pics/board_bg.png")
    return up_arrow, down_arrow, boarder, boarder_bg

def load_bg(bg_list,screen_width, screen_height):
    for i in range(1,6):
        img = pg.transform.scale(pg.image.load(f"lib/background/bg-{i}.png"),(screen_width, screen_height)).convert_alpha()
        bg_list.append(img)
    return bg_list

def load_plane(screen_width,screen_height):
    plane_img = pg.image.load("lib/plane/plane.png")
    plane_img = pg.transform.scale(plane_img, (screen_width, screen_height))
    return plane_img

def load_flame(plane_width,plane_height):
    flame_imgs = []
    for i in range(1,8):
        img = pg.image.load(f"lib/plane/flame/flame ({i}).png")
        img = pg.transform.flip(img, True, False)
        img = pg.transform.scale(img, (int(plane_width/2.3), int(plane_height/3)))
        flame_imgs.append(img)
    return flame_imgs

def load_bullet(screen_width,screen_height):
    bullet_list = []
    for i in range(1,9):
        img = pg.image.load(f"lib/plane/bullet/bullet ({i}).png")
        img = pg.transform.scale(img, (int(screen_width/30), int(screen_height/25)))
        bullet_list.append(img)
    return bullet_list

def load_asteroids(asteroid_height,asteroid_width):
    asteroid_imgs = []
    for i in range(1,4):
        img = pg.image.load(f"lib/asteroids/asteroid ({i}).png")
        img = pg.transform.scale(img, (asteroid_width, asteroid_height))
        asteroid_imgs.append(img)
    return asteroid_imgs

def load_explosion(explosion_height,explosion_width):
    explosion_imgs = []
    for i in range(1,21):
        img = pg.image.load(f"lib/destroy/{i}.png")
        img = pg.transform.scale(img, (explosion_width, explosion_height))
        explosion_imgs.append(img)
    return explosion_imgs

def load_health_bar(health_width,health_height):
    health_bar = []
    for i in range(1,8):
        img = pg.image.load(f"lib/health/health ({i}).png")
        img = pg.transform.scale(img, (int(health_width), int(health_height)))
        health_bar.append(img)
    return health_bar