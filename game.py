#jesse mcdonald
#Controles, move with a and d, shoot by clicking on aliens.
#Aliens now target you
from __future__ import print_function,division
from pygame import *
from math import *
from random import *

true=True
false=False
init()
HEIGHT = 500 
WIDTH = 600
display.set_caption('Space Invaders')
screen = display.set_mode((WIDTH, HEIGHT))
tfont = font.Font(None, 36)

def sqr(x):
    return x*x
class Player:

    def __init__(self):
        self.sprite = image.load("ship.png")
        self.shieldS = image.load("shield.png")
        self.shieldR = self.shieldS.get_rect()
        self.spriteO=self.sprite
        self.rect = self.sprite.get_rect()
        self.pos=[350,HEIGHT-20]
        self.deathtime=100
        self.shield=False
    def update_and_display(self):
        self.deathtime-=1
        self.pos[0]%=WIDTH
        self.rect.centerx=self.pos[0]
        self.rect.centery=self.pos[1]
        self.shieldR.centerx=self.rect.centerx
        self.shieldR.centery=self.rect.centery
        screen.blit(self.sprite, self.rect)
        if self.shield==True:
            screen.blit(self.shieldS,self.shieldR)
class bullet:
    age=1000
    def __init__(self,pos,direction,team):
        self.pos=pos
        self.team=team
        self.vel=[sin(direction)*10,cos(direction)*10]
        self.age=50
        self.sprite = image.load("bullet.png")
        self.rect = self.sprite.get_rect()
        self.pos[0]%=WIDTH
        self.pos[1]%=HEIGHT
    def update(self):
        self.age-=1
        self.pos[0]+=self.vel[0]
        self.pos[1]+=self.vel[1]

        self.rect.centerx=self.pos[0]
        self.rect.centery=self.pos[1]
        self.rect.centerx%=WIDTH
        screen.blit(self.sprite, self.rect)
class Barrier:
    def __init__(self,x,y,):
        self.sprite = image.load("barrier1.png")
        self.rect = self.sprite.get_rect()
        self.pos=[x,y]
        self.health=10
        self.rect.centerx=self.pos[0]
        self.rect.centery=self.pos[1]  
    def update_and_display(self):
        screen.blit(self.sprite, self.rect)
    def hit(self):
        self.health-=1
        self.sprite = image.load(("barrier3.png","barrier3.png","barrier2.png","barrier1.png")[int(self.health/3)])
        self.rect = self.sprite.get_rect()
        self.rect.centerx=self.pos[0]
        self.rect.centery=self.pos[1] 
        if self.health<1:
            return True
        return False
bullets=[]
class Alien:
    def __init__(self, x,y,path,level):
        self.sprite = image.load(("Amother.png","Afighter.png","Aship.png")[level])
        self.rect = self.sprite.get_rect()
        self.points=(3-level)*10
        self.path=path
        self.pos=[x,y]
        self.starty=x
    def update_and_display(self):
        self.pos[1]+=.2
        x=self.pos[1]*2
        self.pos[0]=self.starty+eval(self.path)
        
        self.rect.centerx=self.pos[0]
        self.rect.centerx%=WIDTH
        self.rect.centery=self.pos[1]
        self.rect.centery%=HEIGHT-100   
        screen.blit(self .sprite, self.rect)
        
from time import sleep
player=Player()
FORWARD=False
LEFT=False
RIGHT=False
score=0
barriers=[Barrier(050,400),Barrier(150,400),Barrier(250,400),Barrier(350,400),Barrier(450,400),Barrier(550,400)]
aliens=[Alien(000,000,"x*10",0),Alien(100,000,"x*10.0",0),Alien(200,000,"x*10",0),Alien(300,000,"x*10",0),Alien(400,000,"x*10",0),Alien(500,000,"x*10",0),Alien(600,000,"x*10",0),Alien(000,50,"-x*10",0),Alien(100,50,"-x*10.0",0),Alien(200,50,"-x*10",0),Alien(300,50,"-x*10",0),Alien(400,50,"-x*10",0),Alien(500,50,"-x*10",0),Alien(600,50,"-x*10",0),Alien(000,100,"250*sin(x/40)",1),Alien(100,100,"250*sin(x/40)",1),Alien(200,100,"250*sin(x/40)",1),Alien(300,100,"250*sin(x/40)",1),Alien(400,100,"250*sin(x/40)",1),Alien(500,100,"250*sin(x/40)",1),Alien(600,100,"250*sin(x/40)",1),Alien(000,150,"250*sin(-x/40)",1),Alien(100,150,"250*sin(-x/40)",1),Alien(200,150,"250*sin(-x/40)",1),Alien(300,150,"250*sin(-x/40)",1),Alien(400,150,"250*sin(-x/40)",1),Alien(500,150,"250*sin(-x/40)",1),Alien(600,150,"250*sin(-x/40)",1),Alien(000,200,"1*sin(x/1)",2),Alien(100,200,"1*sin(x/1)",2),Alien(200,200,"1*sin(x/1)",2),Alien(300,200,"1*sin(x/1)",2),Alien(400,200,"1*sin(x/1)",2),Alien(500,200,"1*sin(x/1)",2),Alien(600,200,"1*sin(x/1)",2),Alien(000,250,"1*sin(-x/1)",2),Alien(100,250,"1*sin(-x/1)",2),Alien(200,250,"1*sin(-x/1)",2),Alien(300,250,"1*sin(-x/1)",2),Alien(400,250,"1*sin(-x/1)",2),Alien(500,250,"1*sin(-x/1)",2),Alien(600,250,"1*sin(-x/1)",2),]
def gameover(score):
    global WIDTH, HEIGHT
    while True:
        screen.fill((0,0,0))
        text = tfont.render("Game Over", 1, (255, 255, 255))
        textpos = text.get_rect()
        textpos.center=[WIDTH/2,HEIGHT/2]
        screen.blit(text, textpos)
        text = tfont.render("Your score was: "+str(score), 1, (255, 255, 255))
        textpos = text.get_rect()
        textpos.center=[WIDTH/2,HEIGHT/2+30]
        screen.blit(text, textpos)
        display.flip()
        sleep(0.01)
bDown=false
while True:
    mousepos=mouse.get_pos()
    angle=atan((mousepos[0]-player.pos[0])/(mousepos[1]-player.pos[1]))-pi
                
    #bullets.append(bullet([player.pos[0],player.pos[1]-10],angle,0))#debug lazer
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_a:
                LEFT=True
            if e.key == K_d:
                RIGHT=True
        if e.type == QUIT:
            from sys import exit
            exit()
        if e.type==KEYUP:
            if e.key ==K_w:
                FORWARD=False
            if e.key == K_a:
                LEFT=False
            if e.key == K_d:
                RIGHT=False
    if mouse.get_pressed()[0]& (not bDown):
                bDown=True
                mousepos=mouse.get_pos()
                bullets.append(bullet([player.pos[0],player.pos[1]],angle,0))
    if not mouse.get_pressed()[0]:
        bDown=false
    if LEFT:
        player.pos[0]-=3
    if RIGHT:
        player.pos[0]+=3
    screen.fill((0,0,0))
    player.update_and_display()
    for alien in aliens:
        alien.update_and_display()
    if (random()<.02):
        alien=choice(aliens)
        angle=atan((alien.pos[0]-player.pos[0])/(alien.pos[1]-player.pos[1]))   
        bullets.append(bullet([alien.pos[0],(alien.pos[1]%(HEIGHT-100))],0,1))
    for barrier in barriers:
        barrier.update_and_display();
    i=0
    if len(bullets)>0:
        i=0
        while i < len(bullets):
            j=0
            bulletflag=False
            while j <len(barriers):
                    if bullets[i].rect.colliderect(barriers[j]):
                        bulletflag=True
                        if barriers[j].hit():
                            barriers.remove(barriers[j])
                    j+=1
            if bullets[i].rect.colliderect(player.rect)&bullets[i].team==1:
                if player.shield:
                    bullletflag=True
                    player.shield=False
                    
                else:
                     gameover(score)
            j=0
            while j <len(aliens):
                    if bullets[i].rect.colliderect(aliens[j]):
                        if bullets[i].team==0:
                            bulletflag=True
                            score+=aliens[j].points
                            aliens.remove(aliens[j])
                    j+=1
            bullets[i].update()
            
            if bullets[i].age<0:
                bulletflag=True
            if bulletflag:
                bullets.remove(bullets[i])
            i+=1
    if len(aliens)<1:
        aliens=[Alien(000,000,"x*10",0),Alien(100,000,"x*10.0",0),Alien(200,000,"x*10",0),Alien(300,000,"x*10",0),Alien(400,000,"x*10",0),Alien(500,000,"x*10",0),Alien(600,000,"x*10",0),Alien(000,50,"-x*10",0),Alien(100,50,"-x*10.0",0),Alien(200,50,"-x*10",0),Alien(300,50,"-x*10",0),Alien(400,50,"-x*10",0),Alien(500,50,"-x*10",0),Alien(600,50,"-x*10",0),Alien(000,100,"250*sin(x/40)",1),Alien(100,100,"250*sin(x/40)",1),Alien(200,100,"250*sin(x/40)",1),Alien(300,100,"250*sin(x/40)",1),Alien(400,100,"250*sin(x/40)",1),Alien(500,100,"250*sin(x/40)",1),Alien(600,100,"250*sin(x/40)",1),Alien(000,150,"250*sin(-x/40)",1),Alien(100,150,"250*sin(-x/40)",1),Alien(200,150,"250*sin(-x/40)",1),Alien(300,150,"250*sin(-x/40)",1),Alien(400,150,"250*sin(-x/40)",1),Alien(500,150,"250*sin(-x/40)",1),Alien(600,150,"250*sin(-x/40)",1),Alien(000,200,"1*sin(x/1)",2),Alien(100,200,"1*sin(x/1)",2),Alien(200,200,"1*sin(x/1)",2),Alien(300,200,"1*sin(x/1)",2),Alien(400,200,"1*sin(x/1)",2),Alien(500,200,"1*sin(x/1)",2),Alien(600,200,"1*sin(x/1)",2),Alien(000,250,"1*sin(-x/1)",2),Alien(100,250,"1*sin(-x/1)",2),Alien(200,250,"1*sin(-x/1)",2),Alien(300,250,"1*sin(-x/1)",2),Alien(400,250,"1*sin(-x/1)",2),Alien(500,250,"1*sin(-x/1)",2),Alien(600,250,"1*sin(-x/1)",2),]

    text = tfont.render("Score: "+str(score), 1, (255, 255, 255))
    textpos = text.get_rect()
    textpos.left= 10
    textpos.top = 10
    screen.blit(text, textpos)
    display.flip()
    sleep(0.01)
