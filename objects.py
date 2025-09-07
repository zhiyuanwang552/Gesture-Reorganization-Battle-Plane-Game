import pygame as pg
class player_plane:
    def __init__(self,x_cord,y_cord,plane_height):
        self.x = x_cord
        self.y = y_cord
        self.health = 100
        self.state = "alive"
        self.plane_height = plane_height
        self.x_flame = int(x_cord * 0.95)
        self.y_flame = int((2 * y_cord + plane_height) / 2.07)
        self.flame_index = 0
    
    def move(self,dx,direction,screen_height):
        if direction == "up":
            if(self.y - dx > 0):
                self.y -= dx
                self.y_flame -= dx
        elif direction == "down":
            if(self.y + dx < screen_height - self.plane_height):
                self.y += dx
                self.y_flame += dx

    def draw(self,screen,img,flame_img):
        screen.blit(flame_img,(self.x_flame,self.y_flame))
        screen.blit(img,(self.x,self.y))
        self.flame_index += 1
        if(self.flame_index == 7):
            self.flame_index = 0
        
    
    def hit(self,dmg):
        self.health -= dmg
        if self.health <= 0:
            self.state = "dead"

class bullet:
    def __init__(self,x_cord,y_cord):
        self.x = x_cord
        self.y = y_cord
        self.bullet_index = 0

    def move(self,dx):
        self.x += dx

    def draw(self,screen,img):
        screen.blit(img,(self.x,self.y))
        self.bullet_index += 1
        if(self.bullet_index == 8):
            self.bullet_index = 0

    def hit(self,obj_x,obj_y,obj_width,obj_height,dmg):
        if obj_x < self.x < obj_x + obj_width and obj_y < self.y < obj_y + obj_height:
            return dmg
        return 0
    
class asteroids:
    def __init__(self,x_cord,y_cord,asteroid_height,asteroid_width,id,speed,health):
        self.x = x_cord
        self.y = y_cord
        self.asteroid_height = asteroid_height
        self.asteroid_width = asteroid_width
        self.speed = speed
        self.state = "alive"
        self.id = id
        self.health = health
    
    def move(self):
        self.x -= self.speed

    def draw(self,screen,img):
        screen.blit(img,(self.x,self.y))
    
    def hit(self,dmg):
        self.health -= dmg
        if self.health <= 0:
            self.state = "destroyed"
