# -*- coding: utf-8 -*-
import Classes as c
import pygame
import sys
import operator
import Graphics as g
from threading import Thread
pygame.init()



global idle,walking,damaged,firing,dancing
idle,walking,damaged,firing,dancing = 0,1,2,3,4
terrain1 = 'window_test.txt'



def hello():
    while True:
        print(hello)
        

class Listen_to_Game(Thread):
    
    def __init__(self,gameobject):
        Thread.__init__(self)
        self.game = gameobject
        self.launch_init()
        print('MUDA MUDA MUDA MUDA')
        print(self.init_values)
        
    def launch_init(self):
        done = False
        while not done:
            print('trying')
            try:
                self.init_values = self.game.set_up_result
                done = True
            except AttributeError:
                pass
    
    
        
class GUI_HUD(pygame.sprite.Sprite):
    
    def __init__(self,screen,listen_object):
        self.listen = listen_object
        self.go_init()
    
    def go_init(self):
        done = False
        while not done :
            try :
                pass
            except:
                pass
            
        
        
    

class GUI_terrain(pygame.sprite.Sprite):
    
    def __init__(self,screen,terrain):
        pygame.sprite.Sprite.__init__(self)
        self.land = c.Terrain(terrain)
        self.width = self.land.width
        self.height = self.land.height
        self.create_Surface()
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)
        
    def create_Surface(self):
        empty_surface = pygame.Surface((self.width*51,self.height*51))        
        for s,i in enumerate(self.land.carte):
            for b,j in enumerate(i):
                empty_surface.blit(g.Tiles[i[b]],(b*51,s*51))
        self.image = empty_surface
        
        
    

class GUI_robot(pygame.sprite.Sprite):    
    
    def __init__(self,screen,x,y,d):
        pygame.sprite.Sprite.__init__(self)
        # Variables d'affichages
        self.screen = screen
        # Variables utiles au robot
        self.x = x
        self.y = y
        self.dir = d
        self.life = 9
        self.state = idle
        # Variables de calcul
        self.add = [(0,-1),(1,0),(0,1),(-1,0)]
        self.busy = False
        # Variables graphiques
        self.image = g.base
        self.all_stance = []
        self.frame = 0
        self.latence = 10
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        # Routine d'initialisation
        self.Load_pictures()
    
    def Load_pictures(self):
        # Chargement idle
        idle = []
        for d in range(4):
            mov = []
            for frames in range(1):
                name = 'Robot_I_'+str(d)+'.png'
                im = pygame.image.load(name)
                mov.append(im)
            idle.append(mov)
        # Chargement Walking
        walking = []
        for d in range(4):
            mov =[]           
            for frame in range(5):
                name = 'Robot_W_'+str(d)+str(frame)+'.png'
                im = pygame.image.load(name)
                mov.append(im)
            walking.append(mov)
        # Chargement Damaged
        damaged = []
        for frames in range(3):
            name = 'Robot_D_'+str(frames)+'.png'
            im = pygame.image.load(name)
            damaged.append(im)
        damaged = [damaged,damaged,damaged,damaged]
        # Chargement Firing
        Firing =[]
        for d in range(4):
            mov = []
            for frames in range(2):
                name = 'Robot_F_'+str(d)+str(frames)+'.png'
                im = pygame.image.load(name)
                mov.append(im)
            Firing.append(mov)
        # Chargement Dancing
        Dancing = []
        for frames in range(3):
             name = 'Robot_E_'+str(frames)+'.png'
             im = pygame.image.load(name)
             Dancing.append(im)
        Dancing=[Dancing,Dancing,Dancing,Dancing]
        
        # Integration dans all stance:
        self.all_stance = [idle,walking,damaged,Firing,Dancing]
    
    def calculate_frame(self):
        dico_frame = {0:0,1:4,2:2,3:1,4:2}
        self.latence -=1
        if self.latence <=0:
            self.frame +=1
            self.latence = 20
        if self.frame > dico_frame[self.state]:
            self.frame,self.latence = 0,20
            
    def RR(self):
        self.dir = (self.dir+1)%4
        self.state = idle
    
    def RL(self):
        self.dir = (self.dir+3)%4
        self.state = idle
                   
    def M1(self):
        if not self.busy :
            self.state = walking
            self.type = 'M1'
            self.busy = True
            current_x = self.x
            current_y = self.y
            end = [(current_x,current_y-51),(current_x+51,current_y),(current_x,current_y+51),(current_x-51,current_y)]
            self.current_work = end[self.dir]
            
    def B1(self):
        if not self.busy :
            self.state = walking
            self.type = 'B1'
            self.busy = True
            current_x = self.x
            current_y = self.y
            end = [(current_x,current_y-51),(current_x+51,current_y),(current_x,current_y+51),(current_x-51,current_y)]
            self.current_work = end[(self.dir+2)%4]
    
    def Taunt(self):
        if not self.busy:
            self.state = dancing
            self.type = 'E'
            self.busy = True
            self.countdown = 120
            
    def Damaged(self):
        if not self.busy:
            self.state = damaged
            self.type = 'D'
            self.busy = True
            self.countdown = 120
            self.life -=1
            
    def Firing(self):
        if not self.busy:
            self.state = firing
            self.type = 'F'
            self.busy = True
            self.countdown = 100
        
            
        
    def handle_mov(self):
        if self.busy and self.type in ['M1','B1']:
            if (self.x,self.y) != self.current_work:
                print((self.x,self.y))
                print(self.current_work)
                if self.type == 'M1':
                    (self.x,self.y) = tuple(map(operator.add,(self.x,self.y),self.add[self.dir]))
                elif self.type == 'B1':
                    (self.x,self.y) = tuple(map(operator.add,(self.x,self.y),self.add[(self.dir+2)%4]))
                else:
                    pass
            else :
                self.state = idle
                self.busy = False
                self.type = None

    def handle_action(self):
        if self.busy and self.type in ['E','D','F']:
            if self.type in ['E','D','F']:
                self.countdown-=1
            if self.countdown <= 0:
                self.busy = False
                self.type = None
                self.state = idle
                    
    
    def update(self):
        print('bonjour update')
        self.handle_mov()
        self.handle_action()
        self.calculate_frame()
        self.image = self.all_stance[self.state][self.dir][self.frame]
        self.rect.center = (self.x,self.y)
        
                
                
            
def GUI_main_loop():
    screen = pygame.display.set_mode((1900,1000))
    pygame.display.set_caption("La master race - Main screen")
    background = pygame.Surface(screen.get_size())
    screen.blit(background,(0,0))
    # Les objets
    rob = GUI_robot(screen,76,76,2)
    plaine = GUI_terrain(screen,terrain1)
    # Les groupes de contrôle
    robots = pygame.sprite.Group(rob)
    terrains = pygame.sprite.Group(plaine)

    kp=True
    FPS = 60
    clock=pygame.time.Clock()
    while kp:     
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    rob.M1()
                elif event.key == pygame.K_LEFT:
                    rob.RL()
                elif event.key == pygame.K_RIGHT:
                    rob.RR()
                elif event.key == pygame.K_DOWN :
                    rob.B1()
                elif event.key == pygame.K_SPACE :
                    rob.Taunt()
                elif event.key == pygame.K_d :
                    rob.Damaged()
                elif event.key == pygame.K_f :
                    rob.Firing()
                    
            if event == pygame.QUIT:
                pygame.quit()
                sys.exit()
                kp =False
        terrains.clear(screen,background)
        robots.clear(screen,background)
        terrains.update()
        robots.update()
        terrains.draw(screen)
        robots.draw(screen)
        pygame.display.flip()
               
            
        
#GUI_main_loop()

def lancer_partie():
    land = c.Terrain('window_test.txt')
    partie = c.Game(land)
 
Thread(target = lancer_partie()).start()
#Thread(target = hello()).start()

