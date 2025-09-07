import mediapipe as mp
import os
import cv2
import pygame as pg
import numpy as np
import load_img as li
import objects as ob
import random
#obtain camera input
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if not ret:
    print("Failed to grab frame")
    exit()

relative_path = "gesture_recognizer.task"
model_path = os.path.abspath(relative_path)

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

def set_result(result, output_image: mp.Image, timestamp_ms: int):
    global gesture, gesture_confidence
    gesture = "None"
    gesture_confidence = 0.0
    if not result.gestures:
        return
    gesture = result.gestures[0][0].category_name
    gesture_confidence = result.gestures[0][0].score
    # print(f"Gesture: {gesture} ({gesture_confidence})")

def draw_bg(screen):
    for bg in bg_list:
        screen.blit(bg, (bg_img_x[bg_list.index(bg)], 0))
        screen.blit(bg, (bg_img_x[bg_list.index(bg)] + bg.get_width(), 0))

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=set_result)

with GestureRecognizer.create_from_options(options) as recognizer:
    running  = True
    scroll = 0
    clock = pg.time.Clock()
    FPS = 120
    #variables declaration
    gesture = "None"
    gesture_confidence = 0.0
    pg.init()
    pg_screen = pg.display.set_mode((1000, 600))
    screen_width, screen_height = pg_screen.get_size()
    #initialize images
    plane_img = li.load_plane(screen_width/10,screen_height/8)
    plane = ob.player_plane(int(screen_width/4.3 + int(screen_width/22+10)),int(screen_height/2),screen_height/8)
    up_arrow, down_arrow, board, board_bg = li.load_arrows()
    bg_list = []
    bg_list = li.load_bg(bg_list,screen_width,screen_height)
    bg = pg.transform.scale(bg_list[1], (screen_width - int(screen_width/4.3), screen_height))
    flame_imgs = li.load_flame(plane_img.get_width(),plane_img.get_height())
    scroll_speed = [5,7,9,11,13]
    bg_img_x = [0,0,0,0,0]
    bullet_img = li.load_bullet(screen_width,screen_height)
    asteroid_imgs = li.load_asteroids(int(screen_height/10),int(screen_width/10))
    explosion_imgs = li.load_explosion(int(screen_height/10),int(screen_width/10))
    health_bar = li.load_health_bar(int(screen_width/7),int(screen_height/23))

    #scale images
    up_arrow = pg.transform.scale(up_arrow, (int(screen_width/22), int(screen_height/13)))
    down_arrow = pg.transform.scale(down_arrow, (int(screen_width/22), int(screen_height/13)))
    down_clicked_arrow = pg.transform.scale(down_arrow, (int(screen_width/22+10), int(screen_height/13+5)))
    up_clicked_arrow = pg.transform.scale(up_arrow, (int(screen_width/22+10), int(screen_height/13+5)))
    board = pg.transform.scale(board, (int(screen_width/4.3), int(screen_height)))
    board_bg = pg.transform.scale(board_bg, (int(screen_width/4.3), int(screen_height)))
    #set image positions
    health_bar_x, health_bar_y = int((screen_width/4.3)/5), int(screen_height/2.7)

    boarder_out_x = int(screen_width/4.3)

    arrow_up_x = boarder_out_x
    arrrow_up_y = 5
    arrow_down_x = boarder_out_x
    arrow_down_y = int(screen_height/11)+10

    bullet_list = []
    bullet_time_counter = 0

    asteroid_spawn_counter = 0
    asteroid_list = []

    explosion_list = []
    while running:
        bullet_time_counter += 1
        asteroid_spawn_counter += 1
        if(asteroid_spawn_counter == 60):
            asteroid_spawn_counter = 0
            asteroid_list.append(ob.asteroids(screen_width, random.randint(0, screen_height - int(screen_height/10)), int(screen_height/10), int(screen_width/10), random.randint(1,3), random.randint(3,6), 30))
        if(bullet_time_counter == 13):
            bullet_time_counter = 0
            bullet_list.append(ob.bullet(plane.x + plane_img.get_width(), int(plane.y + plane_img.get_height()/2.8)))
        clock.tick(FPS)
        pg_screen.fill((0, 0, 0))
        #draw parrallax background
        draw_bg(pg_screen)
        for i in range(5):
            bg_img_x[i] -= scroll_speed[i]
            if(abs(bg_img_x[i]) > bg_list[i].get_width()):
                bg_img_x[i] += bg_list[i].get_width()
        #obtain camera frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        # Set desired resolution
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 220)   # width in pixels
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 140)  # height in pixels
        # Convert the BGR image to RGB before processing.
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        frame_timestamp_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))
        # recognize the gesture
        recognizer.recognize_async(mp_image, frame_timestamp_ms)
        
        #resizee the camera frame
        frame = cv2.resize(frame, (int((screen_width/4.3)-(screen_width/4.3)/3.5), int(((screen_width/4.3)-(screen_width/4.3)/3.5)*0.65)))
        frame = pg.surfarray.make_surface(np.rot90(frame))
        
        #display arrows based on gesture
        if(gesture == "Thumb_Up" and gesture_confidence > 0.6):
            pg_screen.blit(up_clicked_arrow, (arrow_up_x-5, arrrow_up_y))
            pg_screen.blit(down_arrow, (arrow_down_x, arrow_down_y))
            plane.move(5,"up",screen_height)
        elif(gesture == "Thumb_Down" and gesture_confidence > 0.6):
            pg_screen.blit(down_clicked_arrow, (arrow_down_x-5, arrow_down_y))
            pg_screen.blit(up_arrow, (arrow_up_x, arrrow_up_y))
            plane.move(5,"down",screen_height)
        else:
            pg_screen.blit(up_arrow, (arrow_up_x, arrrow_up_y))
            pg_screen.blit(down_arrow, (arrow_down_x, arrow_down_y))

        plane.draw(pg_screen,plane_img,flame_imgs[plane.flame_index])

        for b in bullet_list:
            if(b.x > screen_width):
                bullet_list.remove(b)
                continue
            b.draw(pg_screen,bullet_img[b.bullet_index])
            b.move(10)
        
        for a in asteroid_list:
            if(a.x < -a.asteroid_width):
                asteroid_list.remove(a)
                continue
            a.draw(pg_screen,asteroid_imgs[a.id - 1])
            a.move()
            dmg = 0
            for b in bullet_list:
                dmg += b.hit(a.x, a.y, a.asteroid_width, a.asteroid_height, 10)
            if(dmg > 0):
                a.hit(dmg)
                for b in bullet_list:
                    if (b.x > a.x and b.x < a.x + a.asteroid_width and b.y > a.y and b.y < a.y + a.asteroid_height):
                        bullet_list.remove(b)
                if a.state == "destroyed":
                    asteroid_list.remove(a)
                    #add destroyed animation here
                    explosion_list.append([0, a.x, a.y])
                    continue
            if(dmg == 0
               and plane.x < a.x + a.asteroid_width 
               and plane.x + plane_img.get_width() > a.x 
               and plane.y < a.y + a.asteroid_height 
               and plane.y + plane_img.get_height() > a.y):
                plane.hit(10)
                asteroid_list.remove(a)
                #add destroyed animation here
                print(f"Plane Health: {plane.health}")
                if(plane.state == "dead"):
                    print("Game Over")
                    running = False
                    break
    
        pg_screen.blit(board_bg, (0,0))
        pg_screen.blit(frame, (int((screen_width/4.3)/6.5), int(screen_height/7)))
        pg_screen.blit(board, (0,0))
        pg_screen.blit(health_bar[0],(health_bar_x, health_bar_y))
        pg_screen.blit(health_bar[plane.health_id], (health_bar_x, health_bar_y))
        
        for e in explosion_list:
            if e[0] < 20:
                pg_screen.blit(explosion_imgs[e[0]], (e[1], e[2]))
                e[0] += 1
            else:
                explosion_list.remove(e)
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False