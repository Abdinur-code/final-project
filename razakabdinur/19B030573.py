import pika
import json
import sys
import pygame
from threading import Thread
import random
from enum import Enum
from uuid import uuid4
from uuid import UUID
import uuid
def generateUUID():
    return str(uuid4())
size_x=1000
size_y=800
white=(255, 210, 155)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
black=(0, 50, 50)
gray=(50, 50, 50)
yellow=(255, 255, 0)
pygame.init()
width = 800
height = 600
IP = '34.254.177.17'
PORT = 5672
VIRTUAL_HOST = 'dar-tanks'
USERNAME = 'dar-tanks'
PASSWORD = '5orPLExUYnyVYZg48caMpX'
moi_tank=pygame.image.load("C:\\Users\\abdi\\Desktop\\last\\tankr.png")
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Т А Н К И   Г Р Я З И   Н Е   Б О Я Т С Я')
font = pygame.font.SysFont('Times new roman', 28)
gameIcon = pygame.image.load('champion1.png')
pygame.display.set_icon(gameIcon)
def singleplayer():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    fon = pygame.mixer.Sound('C:\\Users\\abdi\Desktop\\last\\background.wav')
    shoot = pygame.mixer.Sound('C:\\Users\\abdi\Desktop\\last\\fire.wav')
    collission = pygame.mixer.Sound('C:\\Users\\abdi\Desktop\\last\\collision.wav')
    brick=pygame.image.load('C:\\Users\\abdi\Desktop\\last\\wall.png')
    boom=pygame.mixer.Sound('C:\\Users\\abdi\Desktop\\last\\boom.wav')
    granade1=pygame.image.load('C:\\Users\\abdi\Desktop\\last\\granade123.png')
    tank1_sprites=[pygame.image.load('C:\\Users\\abdi\Desktop\\last\\tanku.png'),
                    pygame.image.load('C:\\Users\\abdi\Desktop\\last\\tankl.png'),
                    pygame.image.load('C:\\Users\\abdi\Desktop\\last\\tankd.png'),
                    pygame.image.load('C:\\Users\\abdi\Desktop\\last\\tankr.png')]
    tank2_sprites=[pygame.image.load('C:\\Users\\abdi\Desktop\\last\\tankuu.png'),
                    pygame.image.load('C:\\Users\\abdi\Desktop\\last\\tankll.png'),
                    pygame.image.load('C:\\Users\\abdi\Desktop\\last\\tankdd.png'),
                    pygame.image.load('C:\\Users\\abdi\Desktop\\last\\tankrr.png')]
    tt1 = True
    tt2 = True
    class GRD:
        def __init__(self, x,y):
            self.x = x
            self.y = y
            self.color = red
        def draw(self):
            screen.blit(granade1,(self.x,self.y))
    class Bullets:
        def __init__(self, x, y, speedx, speedy):
            self.x = x
            self.y = y
            self.speedx = speedx
            self.speedy = speedy
            self.shot = False
        def draw(self):
            pygame.draw.circle(screen, red, (self.x, self.y),8)
        def move(self):
            if self.shot == True:
                self.x += self.speedx
                self.y += self.speedy
            self.draw()
    class Direction(Enum):
        UP = 1
        DOWN = 2
        LEFT = 3
        RIGHT = 4
    class Tank:
        def __init__(self, x, y, speed, color, d_right=pygame.K_RIGHT, d_left=pygame.K_LEFT, d_up=pygame.K_UP, d_down=pygame.K_DOWN):
            self.x = x
            self.y = y
            self.speed = speed
            self.color = color
            self.width = 40
            self.direction = Direction.RIGHT
            self.KEY = {d_right: Direction.RIGHT, d_left: Direction.LEFT,
                        d_up: Direction.UP, d_down: Direction.DOWN}
        def draw_tank2(self):
            if self.direction== Direction.UP:
                screen.blit(tank2_sprites[0],(self.x,self.y))
            elif self.direction==Direction.LEFT:
                screen.blit(tank2_sprites[1],(self.x,self.y))
            elif self.direction==Direction.DOWN:
                screen.blit(tank2_sprites[2],(self.x,self.y))
            elif self.direction==Direction.RIGHT:
                screen.blit(tank2_sprites[3],(self.x,self.y))

        def draw_tank1(self):
            if self.direction == Direction.UP:
                screen.blit(tank1_sprites[0],(self.x,self.y))
            elif self.direction ==Direction.LEFT:
                screen.blit(tank1_sprites[1],(self.x,self.y))
            elif self.direction == Direction.DOWN:
                screen.blit(tank1_sprites[2],(self.x,self.y))
            elif self.direction == Direction.RIGHT:
                screen.blit(tank1_sprites[3],(self.x,self.y))
        

        def change_direction(self, direction):
            self.direction = direction

        def move_tank2(self):
            if self.direction == Direction.LEFT:
                self.x -= self.speed
            if self.direction == Direction.RIGHT:
                self.x += self.speed
            if self.direction == Direction.UP:
                self.y -= self.speed
            if self.direction == Direction.DOWN:
                self.y += self.speed
            if(self.x < 0):self.x = 800
            if(self.x > 800): self.x = 0
            if(self.y < 0): self.y = 550
            if(self.y > 550): self.y = 0
            self.draw_tank2()
        def move_tank1(self):
            if self.direction == Direction.LEFT:
                self.x -= self.speed
            if self.direction == Direction.RIGHT:
                self.x += self.speed
            if self.direction == Direction.UP:
                self.y -= self.speed
            if self.direction == Direction.DOWN:
                self.y += self.speed
            
            if(self.x < 0):self.x = 800
            if(self.x > 800): self.x = 0
            if(self.y < 0): self.y = 550
            if(self.y > 550): self.y = 0
            self.draw_tank1() 
        def granaderes(self,newpos_x,newpos_y):
            self.newpos_x=random.randint(0,800)
            self.newpos_y=random.randint(0,600)
    class Wall:
        def __init__(self,x,y):
            self.x=x
            self.y=y
        def draw(self):
            self.rect=pygame.Rect(self.x,self.y,40,40)
            screen.blit(brick,(self.x,self.y))
    life1 = 3
    life2 = 3
    mainloop = True
    fr1 = GRD(40,40)
    a=random.randint(20,250)
    b=random.randint(20,250)
    wall=Wall(a,b) 

    wall2=Wall(a+110,b+120)

    wall3=Wall(a+57,b+30)

    wall4=Wall(a+143,b+20)

    wall5=Wall(a+34,b+450)

    wall6=Wall(a+404,b+231)

    wall7=Wall(a+140,b+100)

    wall8=Wall(a+103,b+243)

    wall9=Wall(a+45,b+40)

    wall10=Wall(a+76,b+40)

    wall11=Wall(a+330,b+120)

    wall12=Wall(a+150,b+324)

    wall13=Wall(a+20,b+351)

    wall14=Wall(a+20,b+80)

    wall15=Wall(a+16,b+110)

    wall16=Wall(a+160,b+230)

    wall18=Wall(a+530,b+290)

    wall19=Wall(a+186,b+133)

    wall20=Wall(a+157,b+430)

    tank1 = Tank(300, 300, 1, (225, 0, 0))
    tank2 = Tank(100, 100, 1, (225, 0,0), pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)
    fr1 = GRD(40,40)

    tanks = [tank1, tank2]
    bullet1 = Bullets(831, 560, 0, 0)
    bullet2 = Bullets(831, 560, 0, 0)

    pp1=False
    pp2=False
    FPS = 60
    clock = pygame.time.Clock ()
    fon.play(1)

    playtime=0

    while mainloop:
        mill = clock.tick(FPS)
        playtime+=mill

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
                
                for tank in tanks:
                    if event.key in tank.KEY.keys():
                        tank.change_direction(tank.KEY[event.key])

                if event.key == pygame.K_RETURN and bullet1.shot == False:
                    
                    shoot.play()
                    bullet1.shot = True
                    if tank1.direction == Direction.LEFT:
                        bullet1.x = tank1.x - 20
                        bullet1.y = tank1.y + 20
                        bullet1.speedx = -10
                        bullet1.speedy = 0
                    if tank1.direction == Direction.RIGHT:
                        bullet1.x = tank1.x + 60
                        bullet1.y = tank1.y + 20
                        bullet1.speedx = 10
                        bullet1.speedy = 0
                    if tank1.direction == Direction.UP:
                        bullet1.x = tank1.x + 20
                        bullet1.y = tank1.y - 20
                        bullet1.speedx = 0
                        bullet1.speedy = -10
                    if tank1.direction == Direction.DOWN:
                        bullet1.x = tank1.x + 20
                        bullet1.y = tank1.y + 60
                        bullet1.speedx = 0
                        bullet1.speedy = 10

                if event.key == pygame.K_SPACE and bullet2.shot == False:
                    
                    shoot.play()
                    bullet2.shot = True
                    bullet2.x = tank2.x
                    bullet2.y = tank2.y
                    if tank2.direction == Direction.LEFT:
                        bullet2.x = tank2.x - 20
                        bullet2.y = tank2.y + 20
                        bullet2.speedx = -10
                        bullet2.speedy = 0 
                    if tank2.direction == Direction.RIGHT:
                        bullet2.x = tank2.x + 60
                        bullet2.y = tank2.y + 20
                        bullet2.speedx = 10
                        bullet2.speedy = 0
                    if tank2.direction == Direction.UP:
                        bullet2.x = tank2.x + 20
                        bullet2.y = tank2.y - 20
                        bullet2.speedx = 0
                        bullet2.speedy = -10
                    if tank2.direction == Direction.DOWN:
                        bullet2.x = tank2.x + 20
                        bullet2.y = tank2.y + 60
                        bullet2.speedx = 0
                        bullet2.speedy = 10
        if bullet1.x < 0 or bullet1.x > 821 or bullet1.y < 0 or bullet1.y > 550:
            bullet1.shot = False
        if bullet2.x < 0 or bullet2.x > 821 or bullet2.y < 0 or bullet2.y > 550:
            bullet2.shot = False

        if bullet1.x in range(tank2.x, tank2.x + 40) and bullet1.y in range(tank2.y, tank2.y + 40):
            
            collission.play()
            bullet1.shot = False
            bullet1.x = 810
            bullet1.y = 610
            life1 -= 1
            tt1 = True
        
        if bullet2.x in range(tank1.x, tank1.x + 40) and bullet2.y in range(tank1.y, tank1.y + 40):
            
            collission.play()
            bullet2.shot = False
            bullet2.x = 810
            bullet2.y = 610
            life2 -=1 
            tt2 = True
        if fr1.x in range(tank1.x, tank1.x+40) and fr1.y in range(tank1.y, tank1.y + 40):

            tank1.speed= 2

            fr1.x=random.randint(500,500)
            fr1.y = random.randint(500,500)
        if bullet1.x in range(wall.x,wall.x+30) and bullet1.y in range(wall.y,wall.y+30):
            wall.x=1000
            wall.y=1000
            boom.play()
        if bullet1.x in range(wall2.x,wall2.x+30) and bullet1.y in range(wall2.y,wall2.y+30):    
            wall2.x=1000
            wall2.y=1000
            boom.play()
        if bullet1.x in range(wall3.x,wall3.x+30) and bullet1.y in range(wall3.y,wall3.y+30):    
            wall3.x=1000
            wall3.y=1000
            boom.play()
        if bullet1.x in range(wall4.x,wall4.x+30) and bullet1.y in range(wall4.y,wall4.y+30):    
            wall4.x=1000
            wall4.y=1000
            boom.play()
        if bullet1.x in range(wall5.x,wall5.x+30) and bullet1.y in range(wall5.y,wall5.y+30):
            wall5.x=1000
            wall5.y=1000
            boom.play()
        if bullet1.x in range(wall6.x,wall6.x+30) and bullet1.y in range(wall6.y,wall6.y+30):    
            wall6.x=1000
            wall6.y=1000
            boom.play()
        if bullet1.x in range(wall7.x,wall7.x+30) and bullet1.y in range(wall7.y,wall7.y+30):    
            wall7.x=1000
            wall7.y=1000
            boom.play()
        if bullet1.x in range(wall8.x,wall8.x+30) and bullet1.y in range(wall8.y,wall8.y+30):    
            wall8.x=1000
            wall8.y=1000
            boom.play()  
        #
        if bullet1.x in range(wall9.x,wall9.x+30) and bullet1.y in range(wall9.y,wall9.y+30):
            wall9.x=1000
            wall9.y=1000
            boom.play()
        if bullet1.x in range(wall10.x,wall10.x+30) and bullet1.y in range(wall10.y,wall10.y+30):    
            wall10.x=1000
            wall10.y=1000
            boom.play()
        if bullet1.x in range(wall11.x,wall11.x+30) and bullet1.y in range(wall11.y,wall11.y+30):    
            wall11.x=1000
            wall11.y=1000
            boom.play()
        if bullet1.x in range(wall12.x,wall12.x+30) and bullet1.y in range(wall12.y,wall12.y+30):    
            wall12.x=1000
            wall12.y=1000
            boom.play()
        if bullet1.x in range(wall13.x,wall13.x+30) and bullet1.y in range(wall13.y,wall13.y+30):
            wall13.x=1000
            wall13.y=1000
            boom.play()
        if bullet1.x in range(wall14.x,wall14.x+30) and bullet1.y in range(wall14.y,wall14.y+30):    
            wall14.x=1000
            wall14.y=1000
            boom.play()
        if bullet1.x in range(wall15.x,wall15.x+30) and bullet1.y in range(wall15.y,wall15.y+30):    
            wall15.x=1000
            wall15.y=1000
            boom.play()
        if bullet1.x in range(wall16.x,wall16.x+30) and bullet1.y in range(wall16.y,wall16.y+30):    
            wall16.x=1000
            wall16.y=1000
            boom.play()
        if bullet1.x in range(wall18.x,wall18.x+30) and bullet1.y in range(wall18.y,wall18.y+30):
            wall18.x=1000
            wall18.y=1000
            boom.play()
        if bullet1.x in range(wall19.x,wall19.x+30) and bullet1.y in range(wall19.y,wall19.y+30):    
            wall19.x=1000
            wall19.y=1000
            boom.play()
        if bullet1.x in range(wall20.x,wall20.x+30) and bullet1.y in range(wall20.y,wall20.y+30):    
            wall20.x=1000
            wall20.y=1000
            boom.play()#score
        if bullet2.x in range(wall.x,wall.x+30) and bullet2.y in range(wall.y,wall.y+30):
            wall.x=1000
            wall.y=1000
            boom.play()
        if bullet2.x in range(wall2.x,wall2.x+30) and bullet2.y in range(wall2.y,wall2.y+30):
            wall2.x=1000
            wall2.y=1000
            boom.play()
        if bullet2.x in range(wall3.x,wall3.x+30) and bullet2.y in range(wall3.y,wall3.y+30):    
            wall3.x=1000
            wall3.y=1000
            boom.play()
        if bullet2.x in range(wall4.x,wall4.x+30) and bullet2.y in range(wall4.y,wall4.y+30):    
            wall4.x=1000
            wall4.y=1000
            boom.play() 
        #
        if bullet2.x in range(wall5.x,wall5.x+30) and bullet2.y in range(wall5.y,wall5.y+30):
            wall5.x=1000
            wall5.y=1000
            boom.play()
        if bullet2.x in range(wall6.x,wall6.x+30) and bullet2.y in range(wall6.y,wall6.y+30):    
            wall6.x=1000
            wall6.y=1000
            boom.play()
        if bullet2.x in range(wall7.x,wall7.x+30) and bullet2.y in range(wall7.y,wall7.y+30):    
            wall7.x=1000
            wall7.y=1000
            boom.play()
        if bullet2.x in range(wall8.x,wall8.x+30) and bullet2.y in range(wall8.y,wall8.y+30):    
            wall8.x=1000
            wall8.y=1000
            boom.play()  
        #
        if bullet2.x in range(wall9.x,wall9.x+30) and bullet2.y in range(wall9.y,wall9.y+30):
            wall9.x=1000
            wall9.y=1000
            boom.play()
        if bullet2.x in range(wall10.x,wall10.x+30) and bullet2.y in range(wall10.y,wall10.y+30):    
            wall10.x=1000
            wall10.y=1000
            boom.play()
        if bullet2.x in range(wall11.x,wall11.x+30) and bullet2.y in range(wall11.y,wall11.y+30):    
            wall11.x=1000
            wall11.y=1000
            boom.play()
        if bullet2.x in range(wall12.x,wall12.x+30) and bullet2.y in range(wall12.y,wall12.y+30):    
            wall12.x=1000
            wall12.y=1000
            boom.play()
        if bullet2.x in range(wall13.x,wall13.x+30) and bullet2.y in range(wall13.y,wall13.y+30):
            wall13.x=1000
            wall13.y=1000
            boom.play()
        if bullet2.x in range(wall14.x,wall14.x+30) and bullet2.y in range(wall14.y,wall14.y+30):    
            wall14.x=1000
            wall14.y=1000
            boom.play()
        if bullet2.x in range(wall15.x,wall15.x+30) and bullet2.y in range(wall15.y,wall15.y+30):    
            wall15.x=1000
            wall15.y=1000
            boom.play()
        if bullet2.x in range(wall16.x,wall16.x+30) and bullet2.y in range(wall16.y,wall16.y+30):    
            wall16.x=1000
            wall16.y=1000
            boom.play()  
        if bullet2.x in range(wall18.x,wall18.x+30) and bullet2.y in range(wall18.y,wall18.y+30):
            wall18.x=1000
            wall18.y=1000
            boom.play()
        if bullet2.x in range(wall19.x,wall19.x+30) and bullet2.y in range(wall19.y,wall19.y+30):    
            wall19.x=1000
            wall19.y=1000
            boom.play()
        if bullet2.x in range(wall20.x,wall20.x+30) and bullet2.y in range(wall20.y,wall20.y+30):    
            wall20.x=1000
            wall20.y=1000
            boom.play()
        if fr1.x in range(tank2.x, tank2.x+30) and fr1.y in range(tank2.y, tank2.y + 30):
            tank2.speed= 2 
            fr1.x=random.randint(0,500)
            fr1.y = random.randint(0,500)
        if wall.x in range(tank1.x,tank1.x+30) and wall.y in range(tank1.y,tank1.y+30):
            pp1=True
            boom.play()
            wall.x=a
            wall.y=b
            

        if wall.x in range(tank2.x,tank2.x+30) and wall.y in range(tank2.y,tank2.y+30):
            pp2=True
            boom.play()
            wall.x=a
            wall.y=b
            

        if wall2.x in range(tank1.x,tank1.x+30) and wall2.y in range(tank1.y,tank1.y+30):
            pp1=True
            boom.play()
            wall2.x=a
            wall2.y=b
        
        if wall2.x in range(tank2.x,tank2.x+30) and wall2.y in range(tank2.y,tank2.y+30):
            pp2=True
            boom.play()
            wall2.x=a
            wall2.y=b
        

        if wall3.x in range(tank1.x,tank1.x+30) and wall3.y in range(tank1.y,tank1.y+30):
            pp1=True
            boom.play()
            wall3.x=a
            wall3.y=b
            
        if wall3.x in range(tank2.x,tank2.x+30) and wall3.y in range(tank2.y,tank2.y+30):
            pp2=True
            boom.play()
            wall3.x=a
            wall3.y=b

        if wall4.x in range(tank1.x,tank1.x+30) and wall4.y in range(tank1.y,tank1.y+30):
            pp1=True
            boom.play()
            wall4.x=a
            wall4.y=b
            

        if wall4.x in range(tank2.x,tank2.x+30) and wall4.y in range(tank2.y,tank2.y+30):
            pp2=True
            boom.play()
            wall4.x=a
            wall4.y=b

        if wall5.x in range(tank1.x,tank1.x+30) and wall5.y in range(tank1.y,tank1.y+30):
            pp1=True
            boom.play()
            wall5.x=a
            wall5.y=b
            

        if wall5.x in range(tank2.x,tank2.x+30) and wall5.y in range(tank2.y,tank2.y+30):
            pp2=True
            boom.play()
            wall5.x=a
            wall5.y=b

        if wall6.x in range(tank1.x,tank1.x+30) and wall6.y in range(tank1.y,tank1.y+30):
            pp1=True
            boom.play()
            wall6.x=a
            wall6.y=b
            

        if wall6.x in range(tank2.x,tank2.x+30) and wall6.y in range(tank2.y,tank2.y+30):
            pp2=True
            boom.play()
            wall6.x=a
            wall6.y=b
            

        if wall7.x in range(tank1.x,tank1.x+30) and wall7.y in range(tank1.y,tank1.y+30):
            pp1=True
            boom.play()
            wall7.x=a
            wall7.y=b
        
        if wall7.x in range(tank2.x,tank2.x+30) and wall7.y in range(tank2.y,tank2.y+30):
            pp2=True
            boom.play()
            wall7.x=a
            wall7.y=b
        

        if wall8.x in range(tank1.x,tank1.x+30) and wall8.y in range(tank1.y,tank1.y+30):
            pp1=True
            boom.play()
            wall8.x=a
            wall8.y=b
            
        if wall8.x in range(tank2.x,tank2.x+30) and wall8.y in range(tank2.y,tank2.y+30):
            pp2=True
            boom.play()
            wall8.x=a
            wall8.y=b

        if wall9.x in range(tank1.x,tank1.x+30) and wall9.y in range(tank1.y,tank1.y+30):
            pp1=True
            boom.play()
            wall9.x=a
            wall9.y=b
            

        if wall9.x in range(tank2.x,tank2.x+30) and wall9.y in range(tank2.y,tank2.y+30):
            pp2=True
            boom.play()
            wall9.x=a
            wall9.y=b

        if wall10.x in range(tank1.x,tank1.x+30) and wall10.y in range(tank1.y,tank1.y+30):
            pp1=True
            boom.play()
            wall10.x=a
            wall10.y=b
            

        if wall10.x in range(tank2.x,tank2.x+30) and wall10.y in range(tank2.y,tank2.y+30):
            pp2=True
            boom.play()
            wall10.x=a
            wall10.y=b 
        #
        if wall11.x in range(tank1.x,tank1.x+30) and wall11.y in range(tank1.y,tank1.y+30):
            pp1=True
            boom.play()
            wall11.x=a
            wall11.y=b
            

        if wall11.x in range(tank2.x,tank2.x+30) and wall11.y in range(tank2.y,tank2.y+30):
            pp2=True
            boom.play()
            wall11.x=a
            wall11.y=b
            

        if wall12.x in range(tank1.x,tank1.x+30) and wall12.y in range(tank1.y,tank1.y+30):
            pp1=True
            boom.play()
            wall12.x=a
            wall12.y=b
        
        if wall12.x in range(tank2.x,tank2.x+30) and wall12.y in range(tank2.y,tank2.y+30):
            pp2=True
            boom.play()
            wall12.x=a
            wall12.y=b
        

        if wall13.x in range(tank1.x,tank1.x+30) and wall13.y in range(tank1.y,tank1.y+30):
            pp1=True
            boom.play()
            wall13.x=a
            wall13.y=b
            
        if wall13.x in range(tank2.x,tank2.x+30) and wall13.y in range(tank2.y,tank2.y+30):
            pp2=True
            boom.play()
            wall13.x=a
            wall13.y=b

        if wall14.x in range(tank1.x,tank1.x+30) and wall14.y in range(tank1.y,tank1.y+30):
            pp1=True
            boom.play()
            wall14.x=a
            wall14.y=b
            

        if wall14.x in range(tank2.x,tank2.x+30) and wall14.y in range(tank2.y,tank2.y+30):
            pp2=True
            boom.play()
            wall14.x=a
            wall14.y=b

        if wall15.x in range(tank1.x,tank1.x+30) and wall15.y in range(tank1.y,tank1.y+30):
            pp1=True
            boom.play()
            wall15.x=a
            wall15.y=b
            

        if wall15.x in range(tank2.x,tank2.x+30) and wall15.y in range(tank2.y,tank2.y+30):
            pp2=True
            boom.play()
            wall15.x=a
            wall15.y=b
        #
        if wall16.x in range(tank1.x,tank1.x+30) and wall16.y in range(tank1.y,tank1.y+30):
            pp1=True
            boom.play()
            wall16.x=a
            wall16.y=b
            

        if wall16.x in range(tank2.x,tank2.x+30) and wall16.y in range(tank2.y,tank2.y+30):
            pp2=True
            boom.play()
            wall16.x=a
            wall16.y=b
        if wall18.x in range(tank1.x,tank1.x+30) and wall18.y in range(tank1.y,tank1.y+30):
            pp1=True
            boom.play()
            wall18.x=a
            wall18.y=b
            
        if wall18.x in range(tank2.x,tank2.x+30) and wall18.y in range(tank2.y,tank2.y+30):
            pp2=True
            boom.play()
            wall18.x=a
            wall18.y=b

        if wall19.x in range(tank1.x,tank1.x+30) and wall19.y in range(tank1.y,tank1.y+30):
            pp1=True
            boom.play()
            wall19.x=a
            wall19.y=b
            

        if wall19.x in range(tank2.x,tank2.x+30) and wall19.y in range(tank2.y,tank2.y+30):
            pp2=True
            boom.play()
            wall19.x=a
            wall19.y=b

        if wall20.x in range(tank1.x,tank1.x+30) and wall20.y in range(tank1.y,tank1.y+30):
            pp1=True
            boom.play()
            wall20.x=a
            wall20.y=b
            

        if wall20.x in range(tank2.x,tank2.x+30) and wall20.y in range(tank2.y,tank2.y+30):
            pp2=True
            boom.play()
            wall20.x=a
            wall20.y=b
        #life
        if tt1 == True:
            font = pygame.font.SysFont(None,40)
            score_1 = font.render("white: " + str(life1), True, white)
            tt1 = False
        
        if tt2 == True:
            font = pygame.font.SysFont(None,40)
            score_2 = font.render("green: " + str(life2), True, green)
            tt2 = False
        
        if pp1==True:
            life1=life1-1
            tt1=True
            pp1=False
        if pp2==True:
            life2=life2-1
            tt2=True
            pp2=False
        screen.fill((0,125,255 ))
        screen.blit(score_1, (30, 10))
        screen.blit(score_2, (550, 10))
        tank1.move_tank1()
        tank2.move_tank2()
        bullet1.move()
        bullet2.move()

        tank1.granaderes(random.randint(100,700),random.randint(50,500))
        tank2.granaderes(random.randint(100,700),random.randint(50,500))

        fr1.draw()

        wall.draw()

        wall2.draw()
        
        wall3.draw()
        
        wall4.draw()
        
        wall5.draw()

        wall6.draw()
        
        wall7.draw()
        
        wall8.draw()
        
        wall9.draw()
        
        wall10.draw()

        wall11.draw()
        
        wall12.draw()
        
        wall13.draw()
        
        wall14.draw()
        
        wall15.draw()

        wall16.draw()
    
        wall18.draw()
        
        wall19.draw()
        
        wall20.draw()
        if life1 <= 0 :
            fon.stop()
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 800, 600))
            font = pygame.font.SysFont(None, 64)
            text_3 = font.render('W I N', True, (255, 255, 0))
            text_2 = font.render('W H I T E', True, white)
            screen.blit(text_2, (350, 200))
            screen.blit(text_3, (350, 280))
        if life2 <= 0 :
            fon.stop()
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 800, 600))
            font = pygame.font.SysFont('Times new roman', 64)
            text_3 = font.render('W I N', True, (255, 255, 0))
            text_1 = font.render('G R E E N', True, green)
            screen.blit(text_1, (340, 200))
            screen.blit(text_3, (350, 280))        
        pygame.display.flip()  
    pygame.quit()  
def multiplayer():
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))

    class TankRpcClient: 
        def __init__(self):
            self.connection  = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=IP,                                                
                    port=PORT,
                    virtual_host=VIRTUAL_HOST,
                    credentials=pika.PlainCredentials(
                        username=USERNAME,
                        password=PASSWORD
                    )
                )
            )
            self.channel = self.connection.channel()                      
            queue = self.channel.queue_declare(queue='',exclusive=True,auto_delete=True)  
            self.callback_queue = queue.method.queue 
            self.channel.queue_bind(exchange='X:routing.topic',queue=self.callback_queue)
            self.channel.basic_consume(queue=self.callback_queue,
                                    on_message_callback=self.on_response,
                                    auto_ack=True) 
            self.response= None    
            self.corr_id = None
            self.token = None
            self.tank_id = None
            self.room_id = None

        def on_response(self, ch, method, props, body):
            if self.corr_id == props.correlation_id:
                self.response = json.loads(body)
                print(self.response)

        def call(self, key, message={}):     
            self.response = None
            self.corr_id = str(uuid.uuid4())
            self.channel.basic_publish(
                exchange='X:routing.topic',
                routing_key=key,
                properties=pika.BasicProperties(
                    reply_to=self.callback_queue,
                    correlation_id=self.corr_id,
                ),
                body=json.dumps(message) 
            )
            while self.response is None:
                self.connection.process_data_events()

        def check_server_status(self): 
            self.call('tank.request.healthcheck')
            return self.response['status']== '200' 

        def obtain_token(self, room_id):
            message = {
                'roomId': room_id
            }
            self.call('tank.request.register', message)
            if 'token' in self.response:
                self.token = self.response['token']
                self.tank_id = self.response['tankId']
                self.room_id = self.response['roomId']
                return True
            return False

        def turn_tank(self, token, direction):
            message = {
                'token': token,
                'direction': direction
            }
            self.call('tank.request.turn', message)
        def fire_bullet(self,token):
            message={
                'token':token 
            }
            self.call("tank.request.fire",message)

    class TankConsumerClient(Thread):

        def __init__(self, room_id):
            super().__init__()
            self.connection  = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=IP,                                                
                    port=PORT,
                    virtual_host=VIRTUAL_HOST,
                    credentials=pika.PlainCredentials(
                        username=USERNAME,
                        password=PASSWORD
                    )
                )
            )
            self.channel = self.connection.channel()                      
            result = self.channel.queue_declare(queue='',exclusive=True,auto_delete=True)
            queue_name = result.method.queue
            self.channel.queue_bind(exchange='X:routing.topic',queue=queue_name,routing_key='event.state.'+room_id)
            self.channel.basic_consume(
                queue=queue_name,
                on_message_callback=self.on_response,
                auto_ack=True
            )
            self.response = None

        def on_response(self, ch, method, props, body):
            self.response = json.loads(body)
        def run(self):
            self.channel.start_consuming()
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    FIRE = 'LALT'

    CV = {
        pygame.K_UP: UP,
        pygame.K_LEFT: LEFT,
        pygame.K_DOWN: DOWN,
        pygame.K_RIGHT: RIGHT
    }
    AT_1 = {
        pygame.K_LALT : FIRE
    }
    tank1_sprites=[pygame.image.load('C:\\Users\\abdi\Desktop\\last\\tanku.png'),
                    pygame.image.load('C:\\Users\\abdi\Desktop\\last\\tankl.png'),
                    pygame.image.load('C:\\Users\\abdi\Desktop\\last\\tankd.png'),
                    pygame.image.load('C:\\Users\\abdi\Desktop\\last\\tankr.png')]
    tank2_sprites=[pygame.image.load('C:\\Users\\abdi\Desktop\\last\\tankuu.png'),
                    pygame.image.load('C:\\Users\\abdi\Desktop\\last\\tankll.png'),
                    pygame.image.load('C:\\Users\\abdi\Desktop\\last\\tankdd.png'),
                    pygame.image.load('C:\\Users\\abdi\Desktop\\last\\tankrr.png')]
    def draw_tank2(x,y,direction):
        if direction=="UP":
            screen.blit(tank2_sprites[0],(x,y))
        elif direction=="LEFT":
            screen.blit(tank2_sprites[1],(x,y))
        elif direction=="DOWN":
            screen.blit(tank2_sprites[2],(x,y))
        elif direction=="RIGHT":
            screen.blit(tank2_sprites[3],(x,y))
    def tank1(x, y,direction):
        if direction=="UP":
            screen.blit(tank1_sprites[0],(x,y))
        elif direction == "LEFT":
            screen.blit(tank1_sprites[1],(x,y))
        elif direction == "DOWN":
            screen.blit(tank1_sprites[2],(x,y))
        elif direction == "RIGHT":
            screen.blit(tank1_sprites[3],(x,y))
    def table(tank,mains):
        fd=font1.render('{0}: hp: {1}, score: {2}'.format(tank['id'],tank['health'],tank['score']),4,(255,0,0)) 
        screen.blit(fd,(400,90+(45*mains)))
    def draw_bullet(x,y,bul_width,bul_height,bul_direction):
        pygame.draw.rect(screen,(225,0,0),(x,y,bul_width,bul_height))
    def game_start():
        mainloop = True
        font = pygame.font.Font(None, 40) 
        while mainloop:
            screen.fill((0,0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mainloop = False
                    if event.key in CV:
                        client.turn_tank(client.token, CV[event.key])
                    if event.key in AT_1:
                        client.fire_bullet(client.token)
            try:
                remaining_time = event_client.response['remainingTime']
                
                text = font.render('Remaining Time: {}'.format(remaining_time), True, blue)
                           
                textRect = text.get_rect()
                
                textRect.center = (450, 30)
                
                screen.blit(text, textRect)
                
                hits = event_client.response['hits']
                
                bullets = event_client.response['gameField']['bullets']
                
                winners = event_client.response['winners']
                
                tanks = event_client.response['gameField']['tanks']
                
                for tank in tanks:
                    id=tank['id']
                    tank_x = tank['x']
                    tank_y = tank['y']
                    tank_width = tank['width']
                    tank_height = tank['height']
                    tank_direction = tank['direction']
                    tank_health=tank['health']
                    draw_tank2(tank_x, tank_y, tank_direction)
                    if client.tank_id==id:
                        tank1(tank_x,tank_y,tank_direction)
                for bullet in bullets:
                    bullet_x=bullet['x']
                    bullet_y=bullet['y']
                    bul_height=bullet['height']
                    bul_width=bullet['width']
                    bul_direction=bullet['direction']
                    draw_bullet(bullet_x,bullet_y,bul_width,bul_height,bul_direction)
                for tank in tanks:
                    for i in range(1,len(tanks)):
                        table(tank,i)
                
            
            except Exception as e:
                pass
            pygame.display.flip()
        client.connection.close()
        pygame.quit()


    client = TankRpcClient()
    client.check_server_status()
    client.obtain_token('room-1')
    event_client = TankConsumerClient('room-1')
    event_client.start()
    game_start()
    pygame.quit()   
def game_over():
    my_font = pygame.font.SysFont(None, 90)
    game_over_NG = my_font.render('N I C E  G A M E', True, red)
    game_over_r = game_over_NG.get_rect()
    game_over_r.midtop = (400, 200)
    screen.fill(black)
    screen.blit(game_over_NG, game_over_r)
    pygame.display.flip()
    pygame.quit()
    sys.exit()#rect
def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)
    return newText
def main_menu():
    font = None
    click = False
    uakyt = pygame.time.Clock()
    FPS = 60
    while True:
        ms = uakyt.tick(FPS)
        screen.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()
        #buttons
        button1 = pygame.Rect(270, 245, 460, 70)
        button2 = pygame.Rect(280, 325, 440, 70)
        button3 = pygame.Rect(150, 405, 700, 70)
        button4 = pygame.Rect(380, 485, 280, 70)
        #bool
        bt1 = False
        bt2 = False
        bt3 = False
        bt4 = False
        if button1.collidepoint((mx, my)):
            bt1 = True
            if click:
                singleplayer()

        if button2.collidepoint((mx, my)):
            bt2 = True
            if click:
                multiplayer()
            
        if button3.collidepoint((mx, my)):
            bt3 = True
            if click:
                multiplayer()

        if button4.collidepoint((mx, my)):
            bt4 = True
            if click:
                game_over()

        if bt1:
            pygame.draw.rect(screen, (255, 222,222), button1)
        else:
            pygame.draw.rect(screen, (200, 0, 0), button1)
        if bt2:
            pygame.draw.rect(screen, (255, 222, 222), button2)
        else:
            pygame.draw.rect(screen, (200, 0, 0), button2)
        if bt3:
            pygame.draw.rect(screen, (255, 222, 222), button3)
        else:
            pygame.draw.rect(screen, (200, 0, 0), button3)
        if bt4:
            pygame.draw.rect(screen, (255, 222, 222), button4)
        else:
            pygame.draw.rect(screen, (200, 0, 0), button4)
        my_font = pygame.font.SysFont(None, 90)
        single_player_text = text_format("Single Player", font, 75, blue) 
        multiplayer_text = text_format("Multiplayer", font, 75, blue)
        multi_player_ai_text = text_format("Multiplayer with AI" ,font, 75, blue)
        quit1_text = text_format("QUIT", font, 75, blue)

        singleplayer_rect = single_player_text.get_rect()
        multiplayer_rect = multiplayer_text.get_rect()
        multi_player_ai_rect = multi_player_ai_text.get_rect()
        quit1_rect = quit1_text.get_rect()

        screen.blit(single_player_text, (1000//2 - (singleplayer_rect[2]//2), 250))
        screen.blit(multiplayer_text, (1000//2 - (multiplayer_rect[2]//2), 330))
        screen.blit(multi_player_ai_text, (1000//2 - (multi_player_ai_rect[2]//2), 410))
        screen.blit(quit1_text,(1000//2 - (quit1_rect[2]//2), 490))
        pygame.display.update()

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
main_menu()
