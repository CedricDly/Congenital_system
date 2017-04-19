#coding:utf-8


import random
import operator
import time

class Terrain():
    def __init__(self,file_txt):
        self.file  = file_txt
        self.carte = self.load(self.file)
        self.constantmap = self.carte
        self.width = len(self.carte[0])
        self.height = len(self.carte)
        self.spawn = [(1,1),(1,15),(9,1),(9,15)]
        self.bot_pos = []
        self.non_collidable=[' ','F','H','Z','Q','S','D','V','C','R']          #Trucs sur lesquels on peut marcher
        self.collidable=['W','P','O','M','L','-','*','+','/','#','$','€','£']  #Trucs sur lesquels on peut pas marcher
        self.special_collidable=['0','1','2','3','4','5','6','7','8','9']
        self.load_Elements()
    def load(self,file):
        f=open(file)
        Terrain = []
        for line in f:
            L=[]
            for el in line:
                L.append(el)
            L.remove('\n')
            Terrain.append(L)
        return Terrain
    def load_Elements(self):
        Holes=[]
        tapisH, tapisG, tapisD, tapisB = [],[],[],[]
        laserH, laserG, laserD, laserB = [],[],[],[]
        turnC,turnA = [],[]
        for a,i in enumerate(self.carte) :
            for s,l in enumerate(i):
                if i[s] =='F':
                    flag =(a,s)
                if i[s] =='H':
                    Holes.append((a,s))
                if i[s] == 'Z':
                    tapisH.append((a,s))
                if i[s] == 'Q':
                    tapisG.append((a,s))
                if i[s] == 'S':
                    tapisB.append((a,s))
                if i[s] == 'D':
                    tapisD.append((a,s))
                if i[s] == 'P':
                    laserH.append((a,s))
                if i[s] == 'O':
                    laserG.append((a,s))
                if i[s] == 'M':
                    laserB.append((a,s))
                if i[s] == 'L':
                    laserD.append((a,s))
                if i[s] == 'V':
                    turnC.append((a,s))
                if i[s] == 'C':
                    turnA.append((a,s))
        self.holes = Holes
        self.flag = flag
        self.tapisG = tapisG
        self.tapisD = tapisD
        self.tapisH = tapisH
        self.tapisB = tapisB
        self.laserG = laserG
        self.laserD = laserD
        self.laserH = laserH
        self.laserB = laserB
        self.turnA = turnA
        self.turnC = turnC
        

        
    def Render(self):
        for i in self.carte:
            line = '|'.join(i)
            print(line)



class Robot():
    
    def __init__(self,terrain,name):
        self.name = name
        self.terrain = terrain
        self.rspawn =random.choice(self.terrain.spawn) 

        self.x = self.rspawn[0]
        self.y = self.rspawn[1]
        self.dir = random.choice([0,1,2,3])
        self.__dicoDir = {0:'North',1:'East',2:'South',3:'West'}
        self.base = terrain.carte 
        self.__boundary = (terrain.width,terrain.height)
        self.life = 9
        self.win = False
        self.update_map()
        
    def Turn_Right(self):
        self.dir = (self.dir+1)%4
        self.update_map()
        
    def Turn_Left(self):
        self.dir = (self.dir+3)%4
        self.update_map()
        
    def U_Turn(self):
        self.dir = (self.dir+2)%4
        self.update_map()
    

        
    def Forward(self,n):
        for i in range(n):


            if self.dir ==0 and self.check(self.x -1,self.y):
                if self.terrain.carte[self.x][self.y]!='H':
                    self.x -=1


            if self.dir ==1 and self.check(self.x,self.y+1):
                if self.terrain.carte[self.x][self.y]!='H':
                    self.y +=1


            if self.dir ==2 and self.check(self.x +1,self.y):
                if self.terrain.carte[self.x][self.y]!='H':
                    self.x +=1


            if self.dir ==3 and self.check(self.x,self.y-1):
                if self.terrain.carte[self.x][self.y]!='H':
                    self.y -=1

            
                
        self.update_map()

        
    def Backward(self):
        if self.dir == 0 and self.bkcheck(self.x+1 ,self.y):
            self.x += 1
        if self.dir == 1 and self.bkcheck(self.x,self.y-1):
            self.y -= 1
        if self.dir == 2 and self.bkcheck(self.x-1 ,self.y):
            self.x -= 1
        if self.dir == 3 and self.bkcheck(self.x,self.y+1):
            self.y += 1
        self.update_map()
    
    def special_check(self,x,y):
        if self.dir==0 and (self.terrain.carte[x][y] in ['2','6','7','8'] or self.terrain.constantmap[self.x][self.y] in ['0','4','5','8']):
            return False
        elif self.dir==2 and (self.terrain.carte[x][y] in ['0','4','5','8'] or self.terrain.constantmap[self.x][self.y] in ['2','6','7','8']):
            return False
        elif self.dir==1 and (self.terrain.carte[x][y] in ['3','4','7','9'] or self.terrain.constantmap[self.x][self.y] in ['1','5','6','9']):
            return False
        elif self.dir==3 and (self.terrain.carte[x][y] in ['1','5','6','9'] or self.terrain.constantmap[self.x][self.y] in ['3','4','7','9']):
            return False
        else : 
            return True

    def bkspecial_check(self,x,y):
        if self.dir==2 and (self.terrain.carte[x][y] in ['2','6','7','8'] or self.terrain.constantmap[self.x][self.y] in ['0','4','5','8']):
            return False
        elif self.dir==0 and (self.terrain.carte[x][y] in ['0','4','5','8'] or self.terrain.constantmap[self.x][self.y] in ['2','6','7','8']):
            return False
        elif self.dir==3 and (self.terrain.carte[x][y] in ['3','4','7','9'] or self.terrain.constantmap[self.x][self.y] in ['1','5','6','9']):
            return False
        elif self.dir==1 and (self.terrain.carte[x][y] in ['1','5','6','9'] or self.terrain.constantmap[self.x][self.y] in ['3','4','7','9']):
            return False
        else : 
            return True
        
    def bkcheck(self,x,y):
        
        if self.terrain.carte[x][y] in self.terrain.special_collidable or self.terrain.constantmap[self.x][self.y] in self.terrain.special_collidable:
            if self.bkspecial_check(x,y):
                return True
            else:
                return False
        if self.terrain.carte[x][y] in self.terrain.non_collidable:
            return True
        else:
            return False
        
    def check(self,x,y):

        if self.terrain.carte[x][y] in self.terrain.special_collidable or self.terrain.constantmap[self.x][self.y] in self.terrain.special_collidable:
            if self.special_check(x,y):
                return True
            else:
                return False
        if self.terrain.carte[x][y] in self.terrain.non_collidable:
            return True
        else:
            return False
    
    def update_map(self):
        self.terrain.carte = self.terrain.load(self.terrain.file)
        self.terrain.carte[self.x][self.y] = 'R'
        self.terrain.Render()
        self.public_x,self.public_y = self.x,self.y
        print('dir : ' + self.__dicoDir[self.dir])
        self.orientation = self.__dicoDir[self.dir]
        print(self.life)
        
    def handle_land(self):
        self.__coordsRobot = (self.x, self.y)
        unchanged = True
        # Gestion du flag
        if self.__coordsRobot == self.terrain.flag:
            self.win = True 
        # Gestion des trous
        for i in self.terrain.holes:
            if self.__coordsRobot ==i:
                self.__coordsRobot=self.rspawn
        # Gestion des tapis        
        for i in self.terrain.tapisG:
            if self.__coordsRobot== i and self.check(self.x,self.y-1):
                self.__coordsRobot =(self.__coordsRobot[0],self.__coordsRobot[1]-1)
                
        for i in self.terrain.tapisD:
            if unchanged :
                if self.__coordsRobot== i and self.check(self.x,self.y+1):               
                    self.__coordsRobot =(self.__coordsRobot[0],self.__coordsRobot[1]+1)
                    unchanged = False
                    
        for i in self.terrain.tapisH:
            if self.__coordsRobot== i and self.check(self.x-1,self.y):
                self.__coordsRobot =(self.__coordsRobot[0]-1,self.__coordsRobot[1])
        
        for i in self.terrain.tapisB:
            if unchanged :
                if self.__coordsRobot== i and self.check(self.x+1,self.y):               
                    self.__coordsRobot =(self.__coordsRobot[0]+1,self.__coordsRobot[1])
                    unchanged = False
        # Gestion des rotationneurs (oui ça veut rien dire mais voilà) 
        for i in self.terrain.turnA:
            if self.__coordsRobot== i:
                self.Turn_Left()
        for i in self.terrain.turnC:
            if self.__coordsRobot== i:
                self.Turn_Right()
        # Invariant
        self.x,self.y =self.__coordsRobot
        self.update_map()
    
    def check_up_laser(self):
        vertical_exception = self.terrain.collidable + ['0','2','4','5','6','7','8','R','F']
        limit=[]
        exist = False
        for i in self.terrain.laserH:
            if self.y == i[1]:
                exist = True
                limit.append(i[0])
        if exist :
            up_blocked = False
            limit = max(limit)
            for cases in range(self.x,limit+1,-1):
                if self.terrain.carte[cases][self.y] in vertical_exception:
                    up_blocked = True

            if not up_blocked:
                self.life-=1
            if up_blocked and self.terrain.constantmap[self.x][self.y] in ['2','6','7']:
                self.life-=1

            
    def check_down_laser(self):
        vertical_exception = self.terrain.collidable + ['0','2','4','5','6','7','8','R','F']
        limit=[]
        exist = False
        for i in self.terrain.laserB:
            if self.y == i[1]:
                exist = True
                limit.append(i[0])
        if exist :
            down_blocked = False
            limit = min(limit)
            for cases in range(self.x,limit-1):
                if self.terrain.carte[cases][self.y] in vertical_exception:
                    down_blocked = True
                print(down_blocked)
                    
            if not down_blocked:
                self.life-=1
                print('perte en bas')
            if down_blocked and self.terrain.constantmap[self.x][self.y] in ['0','4','5']:
                self.life-=1
                print('perte en bas')            
        
    def check_left_laser(self):
        horizontal_exception = self.terrain.collidable + ['1','3','4','5','6','7','9','R','F']
        limit=[]
        exist = False
        for i in self.terrain.laserG:
            if self.x == i[0]:
                exist = True
                limit.append(i[1])
        if exist :
            left_blocked = False
            limit = max(limit)
            for cases in range(self.y-1,limit,-1):
                print(cases)
                if self.terrain.carte[self.x][cases] in horizontal_exception:
                    left_blocked = True
            if not left_blocked and self.terrain.constantmap[self.x][self.y] in ['3','4','7','9','F']:
                left_blocked = True
                   
            if not left_blocked:
                self.life-=1
                print('perte en bas')
            if left_blocked and self.terrain.constantmap[self.x][self.y] in ['1','5','6']:
                self.life-=1
                print('perte en bas')    

    def check_right_laser(self):
        horizontal_exception = self.terrain.collidable + ['1','3','4','5','6','7','9','R','F']
        limit=[]
        exist = False
        for i in self.terrain.laserD:
            if self.x == i[0]:
                exist = True
                limit.append(i[1])
        print('existence : ',exist)
        if exist :
            right_blocked = False
            limit = min(limit)
            print(limit)
            for cases in range(self.y+1,limit):
                print(cases)
                if self.terrain.carte[self.x][cases] in horizontal_exception:
                    right_blocked = True
            if not right_blocked and self.terrain.constantmap[self.x][self.y] in ['1','5','6','9','F']:
                right_blocked = True
                   
            if not right_blocked:
                self.life-=1
                print('perte en bas')
            if right_blocked and self.terrain.constantmap[self.x][self.y] in ['3','4','7']:
                self.life-=1
                print('perte en bas')                
        
    def handle_endturn(self):      
        self.check_up_laser()
        self.check_down_laser()
        self.check_left_laser()
        self.check_right_laser()
        
      
                    
        self.update_map()
                    

class Joueur():
    def __init__(self,robot,playername):
        self.robot = robot
        self.name = playername
        self.robot_life = self.robot.life
        self.deck = ['M1']*16+['M2']*12+['M3']*6+['BU']*6+['RR']*18+['RL']*18+['UT']*6
        self.choice = ['Do_nothing']
        self.menu = []
        self.flag_nb = 0
    
    def pick_cards(self):
        if self.check_pioche()==True:
            self.choice = ['Do_nothing']
            deck = self.deck
            for i in range(self.robot.life):
                newcard = random.choice(deck)
                self.choice.append(newcard)
        else:
            print('trigger')
            self.choice = self.menu
            
    def check_pioche(self):
        if self.robot.life < 5:
            return False
        else:
            return True
 
    def menu_execute(self,param):

        if param=='M1'and not(self.robot.win):
            print('performing M1')
            self.robot.Forward(1)
            time.sleep(0.5)
        elif param=='M2'and not(self.robot.win):
            print('performing M2')
            self.robot.Forward(2)
            time.sleep(0.5)
        elif param=='M3'and not(self.robot.win):
            print('performing M3')
            self.robot.Forward(3)
            time.sleep(0.5)
        elif param=='BU'and not(self.robot.win):
            print('performing BU')
            self.robot.Backward()
            time.sleep(0.5)
        elif param=='RR'and not(self.robot.win):
            print('performing RR')
            self.robot.Turn_Right()
            time.sleep(0.5)
        elif param=='RL'and not(self.robot.win):
            print('performing RL')
            self.robot.Turn_Left()
            time.sleep(0.5)
        elif param=='UT'and not(self.robot.win):
            print('performing UT')
            self.robot.U_Turn()
            time.sleep(0.5)
        else:
            pass
        self.robot.handle_land()
        self.robot.handle_endturn()

            
            
        
        

class Joueur_Humain(Joueur):
    def __init__(self,robot,playername):
        super().__init__(robot,playername)
        
    def make_program(self):
        pgsize=min(5,self.robot_life)
        remaining_choice = self.choice
        self.menu = []
        choix = 0
        for i in range(pgsize):
            while choix not in remaining_choice :
                print('Possibilités restantes :' )
                print(remaining_choice)
                print('Votre menu actuel')
                print(self.menu)
                choix = input("Phase N°{} du programme Maiiiitre ?".format(i+1))
            self.menu.append(choix)
            if choix !='Do_nothing':
                remaining_choice.remove(choix)
            choix = 0
        print('Tout sera fait selon vos désirs Maiiiiitre:')
        print('Menu final',self.menu)
        return self.menu

    
class Joueur_Brownien(Joueur):
    def __init__(self,robot,playername):
        super().__init__(robot,playername)
        
    def make_program(self):
        pgsize=min(5,self.robot_life)
        remaining_choice = self.choice
        self.menu = []
        for i in range(pgsize):
            new_move = random.choice(remaining_choice)
            self.menu.append(new_move)
            if new_move !='Do_nothing':
                remaining_choice.remove(new_move)
        print('Les Dés sont jettés :')
        print('Menu : ',self.menu)
        return self.menu
        



class Game:
    def __init__(self,terrain):
        self.terrain = terrain
        self.type = [Joueur_Humain,Joueur_Brownien]
        self.haste = {'M3':0,'M2':50,'M1':100,'BU':100,'RR':150,'RL':150,'UT':150,'Do_nothing':150}
        self.robot_lst = []
        self.player_lst = []
        self.won_game = False
        self.set_parameters()
        self.Game_start()
        self.Game_master()
        
               
        
    def set_parameters(self):
        print("------------------------------------------------------")
        print("| Début du programme d'initialisation de la partie : |")
        print("------------------------------------------------------")
        player_nb = int(input("Combien de joueur disputerons cette partie ?\n Maximum de 4 joueurs   "))
        self.player_nb = min(player_nb,4)
        print("-----------------------")
        print("| Création des Robots |")
        print("-----------------------")
        for i in range(self.player_nb):
            self.robot_lst.append(Robot(self.terrain,"Twonky"))

        for s,i in enumerate(self.robot_lst):
            i.x,i.y = self.terrain.spawn[s][0],self.terrain.spawn[s][0]
            #self.robot_lst[i].rspawn = self.terrain.spawn[i]
            
        for i in range(self.player_nb):
            type,name = 'no','no'
            print("----------------------------")
            print("|Paramétrage du joueur {} : |".format(i+1))
            print("----------------------------")
            while type not in [1,2]:
                type = int(input("Type du Joueur {} \n 1: Human \n 2: COM (Brownien) \n".format(i+1)))
            name = input("Quel est le nom du Joueur {} ?\n".format(i+1))
            self.player_lst.append(self.type[type-1](self.robot_lst[i],name))
            
        
        return self.robot_lst,self.player_lst
    
    def make_turn(self):
        self.all_menus = []
        self.all_turn = []
        self.instructions = []
        for i in self.player_lst:
            self.all_menus.append(i.menu)
        nb_ply = len(self.all_menus)
        print('nombre de joueurs',nb_ply)
        for i in range(5):
            self.all_turn.append([])
        for i in range(5):
            for j in range(nb_ply):
                self.all_turn[i].append((self.all_menus[j][i],self.haste[self.all_menus[j][i]],j))
        for i in self.all_turn:
            i.sort(key=operator.itemgetter(1))
        for i in self.all_turn:
            self.instructions+=i
            
            
    def is_possible(self,order):
        mov = order[0]
        rob = self.robot_lst[order[2]]
        cpt = 0
        if mov not in ['M1','BU']:
            return True,[]
        elif mov =='M1':
            if rob.dir == 0:
                if self.terrain.carte[rob.x-1][rob.y] !='R':
                    return True,[(0,0)]
                else:
                    for i in range(1,4):
                        if rob.x-i >=0 and self.terrain.carte[rob.x-i][rob.y] =='R':
                            cpt +=1
                    if self.terrain.carte[rob.x-cpt-1][rob.y] in self.terrain.non_collidable:
                        corr = [(-1,0)]
                        for i in range(1,cpt+1):
                            corr.append((rob.x-i,rob.y))
                        
                        return True,corr
                    else : 
                        return False,[(0,0)]
                    
                   
                    
            elif rob.dir == 1:

                if self.terrain.carte[rob.x][rob.y+1] !='R':
                    return True,[(0,0)]
                else:
                    for i in range(1,3):
                        if rob.y+i <= len(self.terrain.carte[0])-1 and self.terrain.carte[rob.x][rob.y+i] =='R':
                            cpt +=1
                            
                    if self.terrain.carte[rob.x][rob.y+cpt+1] in self.terrain.non_collidable:
                        corr = [(0,1)]
                        for i in range(1,cpt+1):
                            corr.append((rob.x,rob.y+i))
                        
                        return True,corr
                    else : 
                        return False,[(0,0)]
                    
            elif rob.dir == 2:

                if self.terrain.carte[rob.x+1][rob.y] !='R':

                    return True,[(0,0)]
                else:

                    for i in range(1,3):

                        if rob.x+i <= len(self.terrain.carte)-1 and self.terrain.carte[rob.x+i][rob.y] =='R':
                            cpt +=1
                            

                    if self.terrain.carte[rob.x+cpt+1][rob.y] in self.terrain.non_collidable:
                        corr = [(1,0)]
                        for i in range(1,cpt+1):
                            corr.append((rob.x+i,rob.y))
                        
                        return True,corr
                    else : 
                        return False,[(0,0)]
                    
            elif rob.dir ==3:
                if self.terrain.carte[rob.x][rob.y-1] !='R':

                    return True,[(0,0)]
                else:

                    for i in range(1,3):
                        if rob.y-i <= len(self.terrain.carte[0])-1 and self.terrain.carte[rob.x][rob.y-i] =='R':
                            cpt +=1
                            

                    if self.terrain.carte[rob.x][rob.y-cpt-1] in self.terrain.non_collidable:
                        corr = [(0,-1)]
                        for i in range(1,cpt+1):
                            corr.append((rob.x,rob.y-i))
                        
                        return True,corr
                    else : 
                        return False,[(0,0)]
            else :
                return True,[(0,0)]
            
            
        elif mov =='BU':
            if rob.dir == 0:
                if self.terrain.carte[rob.x+1][rob.y] !='R':

                    return True,[(0,0)]
                else:

                    for i in range(1,3):

                        if rob.x+i <= len(self.terrain.carte)-1 and self.terrain.carte[rob.x+i][rob.y] =='R':
                            cpt +=1
                            

                    if self.terrain.carte[rob.x+cpt+1][rob.y] in self.terrain.non_collidable:
                        corr = [(1,0)]
                        for i in range(1,cpt+1):
                            corr.append((rob.x+i,rob.y))
                        
                        return True,corr
                    else : 
                        return False,[(0,0)]
                    
            elif rob.dir == 1:
                if self.terrain.carte[rob.x][rob.y-1] !='R':

                    return True,[(0,0)]
                else:

                    for i in range(1,3):
                        if rob.y-i <= len(self.terrain.carte[0])-1 and self.terrain.carte[rob.x][rob.y-i] =='R':
                            cpt +=1
                            

                    if self.terrain.carte[rob.x][rob.y-cpt-1] in self.terrain.non_collidable:
                        corr = [(0,-1)]
                        for i in range(1,cpt+1):
                            corr.append((rob.x,rob.y-i))
                        
                        return True,corr
                    else : 
                        return False,[(0,0)]
                
            elif rob.dir == 2:
                if self.terrain.carte[rob.x-1][rob.y] !='R':
                    return True,[(0,0)]
                else:
                    for i in range(1,4):
                        if rob.x-i >=0 and self.terrain.carte[rob.x-i][rob.y] =='R':
                            cpt +=1
                    if self.terrain.carte[rob.x-cpt-1][rob.y] in self.terrain.non_collidable:
                        corr = [(-1,0)]
                        for i in range(1,cpt+1):
                            corr.append((rob.x-i,rob.y))
                        
                        return True,corr
                    else : 
                        return False,[(0,0)]
            elif rob.dir ==3:
                if self.terrain.carte[rob.x][rob.y+1] !='R':
                    return True,[(0,0)]
                else:
                    for i in range(1,3):
                        if rob.y+i <= len(self.terrain.carte[0])-1 and self.terrain.carte[rob.x][rob.y+i] =='R':
                            cpt +=1
                            
                    if self.terrain.carte[rob.x][rob.y+cpt+1] in self.terrain.non_collidable:
                        corr = [(0,1)]
                        for i in range(1,cpt+1):
                            corr.append((rob.x,rob.y+i))
                        
                        return True,corr
                    else : 
                        return False,[(0,0)]
                
            else :
                return True,[(0,0)]
        
            
        
    
    def execute_turn(self):
        s=[]

        for i in self.instructions:
            if i[0]=='M3':
                s.append(('M1',0,i[2]))
                s.append(('M1',0,i[2]))
                s.append(('M1',0,i[2]))
            elif i[0]=='M2':
                s.append(('M1',0,i[2]))
                s.append(('M1',0,i[2]))
            else:
                s.append(i)
        self.instructions = s
       
            
        for i in self.instructions:
            print('Action du robot N°{} :'.format(i[2]+1))
            Bool,corr = self.is_possible(i)
            
            print('collision possible ')
            print(Bool,corr)
            if Bool :
                for h in self.robot_lst:
                    unfinished = True
                    for s in corr[1:]:
                        if unfinished:
                            if (h.x,h.y)== s :
                                h.x+=corr[0][0]
                                h.y+=corr[0][1]                            
                                unfinished = False
                                print('Application de la collision')
                                self.Game_state()
                self.player_lst[i[2]].menu_execute(i[0])

            
                
    
    def ask_players(self):
        for i in self.player_lst:
            i.pick_cards()
            i.make_program()
        self.make_turn()
        self.execute_turn()
        
    
    def evaluate_win(self):
        self.won_game = False
        for i in self.robot_lst:
            if i.win == True:
                self.won_game = True
                
    def burry_losers(self):
        for i in self.robot_lst:
            if i.life<=0:
                self.robot_list.remove(i)
                
    def eraser_cannon(self):
        print('\n')
        print("###########################")
        print("Début de la phase de Tir")
        print("###########################")
        print('\n')
        coord=[]
        locked_up = False
        locked_right = False
        locked_down = False
        locked_left = False
        for G in self.robot_lst:
            coord.append((G.x,G.y))
        coord_set = set(coord)
        for h,i in enumerate(self.robot_lst):
            current_coord = set([(i.x,i.y)])
            target = coord_set.difference(current_coord)
            if i.dir == 0:
                for j in list(target):
                    if i.y == j[1] and i.x > j[0]:
                        locked_up = True
            elif i.dir == 1:
                for j in list(target):
                    if i.x == j[0] and i.y < j[1]:
                        locked_right = True
                
            elif i.dir == 2:
                for j in list(target):
                    if i.y == j[1] and i.x < j[0]:
                        locked_down = True
            elif i.dir == 3:
                for j in list(target):
                    if i.x == j[0] and i.y > j[1]:
                        locked_left = True
            else :
                pass
        
            if locked_up:
                for s,l in enumerate(self.robot_lst):
                    if l != i and i.y == l.y and i.x > l.x :
                        l.life -=1
                        print("le robot {} s'est fait fumé par le robot {}".format(s+1,h+1))
            
            if locked_right:
                for s,l in enumerate(self.robot_lst):
                    if l != i and i.x == l.x and i.y < l.y :
                        l.life -=1
                        print("le robot {} s'est fait fumé par le robot {}".format(s+1,h+1))
            
            
            if locked_down:
                for s,l in enumerate(self.robot_lst):
                    if l != i and i.y == l.y and i.x < l.x :
                        l.life -=1
                        print("le robot {} s'est fait fumé par le robot {}".format(s+1,h+1))
                    

            if locked_left:
                for s,l in enumerate(self.robot_lst):
                    if l != i and i.x == l.x and i.y > l.y :
                        l.life -=1
                        print("le robot {} s'est fait fumé par le robot {}".format(s+1,h+1))
                
    def Game_start(self):
        print("##################")
        print("Debut de la partie")
        print("##################")
        self.Game_state()
        
    def Game_state(self):
        for i in self.robot_lst:
            self.terrain.carte[i.public_x][i.public_y]='R'
        self.terrain.Render()
        for i in self.player_lst:
            print("###########################")
            print("{} et son robot {}".format(i.name,i.robot.name))
            print("position : ({},{})".format(i.robot.public_x,i.robot.public_y))
            print("Points de Vie actuels : {}".format(i.robot.life))
            print("Direction actuelle : {}".format(i.robot.orientation))
            print("###########################")
            print('\n')
            
        
    
    def Finished(self):
        print("############")
        print("Jeu Terminé")
        print("############")
    
    def Victory(self):
        for s,i in enumerate(self.robot_lst):
            if i.win == True:
                winner = s
        print("#####################")
        print("Annonce des résultats")
        print("#####################")
        print('VICTOIRE DU JOUEUR ',self.player_lst[winner].name)
        print('Félicitation')
        
    def Game_over(self) :
        print("#####################")
        print("Annonce des résultats")
        print("#####################")
        print("Tous les Compétiteurs ont été détruits")
        print("G-A-M-E__O-V-E-R")
                
                
        
    def Game_master(self):
        while not(self.won_game) and len(self.robot_lst)>=1:
            self.ask_players()
            self.eraser_cannon()
            self.burry_losers()
            self.evaluate_win()
            self.Game_state()
        if self.won_game:
            self.Finished()
            self.Victory()
        if len(self.robot_lst)<=0:
            self.Finished()
            self.Game_Over()
            

            
            
        
        
            
            
        
        
        
    
    
 


