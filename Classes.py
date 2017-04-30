#coding:utf-8

""" -----DISCLAIMER-----
Certains commentaires font reference au compte-rendu de projet informatique. 
Il est de bon ton de s'en premunir afin d'exploiter au mieux les differentes explications laissees pour le lecteur
"""
import random
import operator
import time

class Terrain():
    def __init__(self,file_txt):
        """Constructeur de la classe Terrain
        Parametres
        ----------
        file_txt : fichier texte 
            Sert de base pour notre terrain (les cases sont reperees par differents caracteres) 
        """
        self.file  = file_txt #fichier hebergeant le terrain
        self.carte = self.load(self.file) #voir methode load de la classe 
        self.constantmap = self.carte #constantmap est une image a l'instant 0 de notre carte, qui servira lors de l'utilisation de la methode check
        self.width = len(self.carte[0]) #largeur du terrain
        self.height = len(self.carte) #hauteur du terrain
        self.spawn = [(1,1),(1,15),(9,1),(9,15)] #lieux d'apparition (possibles) initiaux des robots 
        self.bot_pos = []
        self.non_collidable=[' ','F','H','Z','Q','S','D','V','C','R'] #Caracteres representant les cases sur lesquels on peut marcher
        self.collidable=['W','P','O','M','L','-','*','+','/','#','$','€','£'] #Caracteres representant les cases sur lesquels on ne peut pas marcher
        self.special_collidable=['0','1','2','3','4','5','6','7','8','9'] #Caracteres representant les murs
        self.load_Elements() #voir methode load_Elements de la classe Terrain
        
    def load(self,file):
        """ methode de chargement du terrain de jeu
        
        Parametres
        ----------
        file : fichier texte
            Fichier hebergeant le terrain de jeu sous forme de caracteres
            
        Returns
        -------
        terrain : type liste
            terrain est une liste qui contient chaque case du plateau de jeu, ordonee precisement. 
            exemple : terrain[0,0] est la case tout en haut à gauche
                      terrain[i,j] est la case situee a la (i-1)ème ligne, (j-1)ème colonne
        """
        f=open(file)
        terrain = [] #creation de notre liste (de listes)
        for line in f:
            L=[] #creation d'une liste qui represente une ligne de notre terrain
            for el in line:
                L.append(el)
            L.remove('\n')
            terrain.append(L)
        return terrain
        
    def load_Elements(self):
        """ Méthode permettant de recueillir dans des listes les coordonnées des différents éléments de terrain
        Returns
        -------
        Aucun. Néanmoins, cette méthode crée des variables de classe qui regroupent par élément (tapis roulant haut, bas, laser, etc...) les coordonnées d'apparition
        """
        Holes=[] #trous
        tapisH, tapisG, tapisD, tapisB = [],[],[],[] #tapis roulants
        laserH, laserG, laserD, laserB = [],[],[],[] #lasers
        turnC,turnA = [],[] #tourniquets
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
        """ Constructeur de la classe Robot
        
        Parametres
        ----------
        terrain : fichier texte
            Terrain hebergeant la partie
        name : type str
            Nom du robot
        """
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
       
    """ important : dans les 3 prochaines methodes, rien n'est renvoye, on met seulement a jour l'orientation du robot"""    
    def Turn_Right(self):
        """ rotation du robot vers la droite
        """
        self.dir = (self.dir+1)%4
        self.update_map()
        
    def Turn_Left(self):
        """ rotation du robot vers la gauche
        """
        self.dir = (self.dir+3)%4
        self.update_map()
        
    def U_Turn(self):
        """demi-tour
        """
        self.dir = (self.dir+2)%4
        self.update_map()
    

        
    def Forward(self,n):
        """ Fonction qui gere le deplacement rectiligne du robot
        
        Parametres
        ----------
        n : type int
            nb de cases dont il faut avancer
            
        Returns
        -------
        On ne retourne rien, on met juste a jour les coordonnees du robot
        
        See also
        --------
        Description de la methode check de la classe Robot
        Descrption de la methode update_map de la classe Robot
        """
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
        """ Fonction qui gere le deplacement en marche arriere
        
        See also
        --------
        Description de la methode bkcheck de la classe Robot
        Descrption de la methode update_map de la classe Robot
        """
        if self.dir == 0 and self.bkcheck(self.x+1 ,self.y):
            self.x += 1
        if self.dir == 1 and self.bkcheck(self.x,self.y-1):
            self.y -= 1
        if self.dir == 2 and self.bkcheck(self.x-1 ,self.y):
            self.x -= 1
        if self.dir == 3 and self.bkcheck(self.x,self.y+1):
            self.y += 1
            
        self.update_map()

        
    def check(self,x,y):
        """ Vérifie si un robot peut aller sur la case de coordonnées (x , y) 
        
        Parametres
        ----------
        x et y : type int
            coordonnees de la case à checker
            
        Returns
        -------
        True or False : Vrai si le robot peut aller sur la case, Faux sinon
        
        See also
        --------
        Cette méthode ne gère pas la traversée des murs. Pour cela, se reporter à la méthode special_check()
        Cette méthode ne gère pas les robots qui recuelnt. Pour cela, se reporter à la méthode bkcheck()
        """
        if self.terrain.carte[x][y] in self.terrain.special_collidable or self.terrain.constantmap[self.x][self.y] in self.terrain.special_collidable:
            if self.special_check(x,y):
                return True
            else:
                return False
        if self.terrain.carte[x][y] in self.terrain.non_collidable:
            return True
        else:
            return False
            
            
    def special_check(self,x,y):
        """ Vérifie si un robot peut aller sur la case de coordonnées (x , y).
        La différence avec check() réside dans le fait qu'ici, on effectue des tests concernant les murs.
        
         Parametres
        ----------
        x et y : type int
            coordonnees de la case à checker
            
        Autres variables intéressantes
        ------------------------------
        self.terrain.constantmap[self.x][self.y] est utilisé pour connaitre la case sur laquelle se trouve notre robot. 
        En effet, self.terrain.carte[self.x][self.y] = 'R' quoi qu'il arrive. Ainsi, nous utilisons une copie à l'instant 0 de notre carte.
            
        Returns
        -------
        True or False : Vrai si le robot peut aller sur la case, Faux sinon
        
        See also
        --------
        Cette méthode ne gère que les tests d'un robot qui avance. Pour les tests du robot qui recule, se référer à bkspecial_check()
        """
        if self.dir==0 and (self.terrain.carte[x][y] in ['2','6','7','8'] or self.terrain.constantmap[self.x][self.y] in ['0','4','5','8']):
            return False
        elif self.dir==2 and (self.terrain.carte[x][y] in ['0','4','5','8'] or self.terrain.constantmap[self.x][self.y] in ['2','6','7','8']):
            return False
        elif self.dir==1 and (self.terrain.carte[x][y] in ['3','4','7','9'] or self.terrain.constantmap[self.x][self.y] in ['1','5','6','9']):
            return False
        elif self.dir==3 and (self.terrain.carte[x][y] in ['1','5','6','9'] or self.terrain.constantmap[self.x][self.y] in ['3','4','7','9']):
            return False
        # les quatre tests ci-dessus sont les possibilités qui impliquent un blocage du Robot. Si aucun n'est concluant, alors il peut passer
        else : 
            return True

            
    def bkcheck(self,x,y):
        """ Vérifie si un robot qui recule peut aller sur la case de coordonnées (x , y) 
        
        Parametres
        ----------
        x et y : type int
            coordonnees de la case à checker
            
        Returns
        -------
        True or False : Vrai si le robot peut aller sur la case, Faux sinon
        
        See also
        --------
        Cette méthode ne gère pas la traversée des murs. Pour cela, se reporter à la méthode bkspecial_check()
        """
        if self.terrain.carte[x][y] in self.terrain.special_collidable or self.terrain.constantmap[self.x][self.y] in self.terrain.special_collidable:
            if self.bkspecial_check(x,y):
                return True
            else:
                return False
        if self.terrain.carte[x][y] in self.terrain.non_collidable:
            return True
        else:
            return False
          
            
    def bkspecial_check(self,x,y):
        """ Vérifie si un robot qui recule peut aller sur la case de coordonnées (x , y).
        La différence avec bkcheck() réside dans le fait qu'ici, on effectue des tests concernant les murs.
        
         Parametres
        ----------
        x et y : type int
            coordonnees de la case à checker
            
        Autres variables intéressantes
        ------------------------------
        self.terrain.constantmap[self.x][self.y] est utilisé pour connaitre la case sur laquelle se trouve notre robot. 
        En effet, self.terrain.carte[self.x][self.y] = 'R' quoi qu'il arrive. Ainsi, nous utilisons une copie à l'instant 0 de notre carte.
            
        Returns
        -------
        True or False : Vrai si le robot peut aller sur la case, Faux sinon
        
        """
        if self.dir==2 and (self.terrain.carte[x][y] in ['2','6','7','8'] or self.terrain.constantmap[self.x][self.y] in ['0','4','5','8']):
            return False
        elif self.dir==0 and (self.terrain.carte[x][y] in ['0','4','5','8'] or self.terrain.constantmap[self.x][self.y] in ['2','6','7','8']):
            return False
        elif self.dir==3 and (self.terrain.carte[x][y] in ['3','4','7','9'] or self.terrain.constantmap[self.x][self.y] in ['1','5','6','9']):
            return False
        elif self.dir==1 and (self.terrain.carte[x][y] in ['1','5','6','9'] or self.terrain.constantmap[self.x][self.y] in ['3','4','7','9']):
            return False
        # les quatre tests ci-dessus sont les possibilités qui impliquent un blocage du Robot. Si aucun n'est concluant, alors il peut passer
        else : 
            return True
         
    def update_map(self):
        """ Mise à jour des principaux éléments de jeu, notamment la position des 'R' sur le terrain
        """
        self.terrain.carte = self.terrain.load(self.terrain.file)
        self.terrain.carte[self.x][self.y] = 'R'
        self.terrain.Render() #voir méthode Render()
        self.public_x,self.public_y = self.x,self.y
        print('dir : ' + self.__dicoDir[self.dir]) #affiche la direction dans laquelle se trouve le robot
        self.orientation = self.__dicoDir[self.dir]
        print(self.life) #affiche la vie actuelle du robot

        
    def handle_land(self):
        self.__coordsRobot = (self.x, self.y)
        unchanged = True
        """ Gestion du drapeau """
        if self.__coordsRobot == self.terrain.flag:
            self.win = True 
        """ Gestion des trous """
        for i in self.terrain.holes:
            if self.__coordsRobot ==i:
                self.__coordsRobot=self.rspawn
        """ Gestion des tapis """        
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
        """ Gestion des tourniquets """ 
        for i in self.terrain.turnA:
            if self.__coordsRobot== i:
                self.Turn_Left()
        for i in self.terrain.turnC:
            if self.__coordsRobot== i:
                self.Turn_Right()
        """ Invariant """
        self.x,self.y =self.__coordsRobot
        self.update_map()
 
    """ POUR LES 4 METHODES SUIVANTES :
        elles sont très similaires, seule la directon des lasers et l'orientation des murs change. 
        Ainsi la description ne sera faite qu'une seule fois
    """

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
        """ Constructeur de la classe Joueur
        
        Parametres
        ----------
        robot : objet Robot
            robot du joueur
        playername : type str
            Nom du joueur
        """
        self.robot = robot
        self.name = playername
        self.robot_life = self.robot.life
        self.deck = ['M1']*16+['M2']*12+['M3']*6+['BU']*6+['RR']*18+['RL']*18+['UT']*6 # paquet de cartes de notre joueur
        self.choice = ['Do_nothing'] # main du joueur. Le 'Do_nothing' est présent si l'utilisateur souhaite ne pas jouer l'intégralité de ses cartes
        self.menu = [] # liste qui va être complétée par les cartes que l'utilisateur veut jouer pendant un tour 
        self.flag_nb = 0
    
    def pick_cards(self):
        """ Méthode qui régit la pioche aléatoire de cartes dans le deck
            On commence par savoir si l'utilisateur à le droit de piocher.
            Si oui, alors on choisit une carte aléatoire de son deck, que l'on ajoute à sa main (variable de type liste self.choice).
            On répète l'opération jusqu'à avoir autant de cartes que de points de vie.
            
            See also
            --------
            check_pioche() de la classe Joueur
        """
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
        """ Méthode qui vérifie, en fonction de la vie de son robot, si le joueur est autorisé à tirer des cartes de son deck
        
        Returns
        -------
        True or False : Vrai si l'utilisateur est autorisé à piocher, faux sinon
        """
        if self.robot.life < 5:
            return False # si le robot a moins de 5 PV, l'utilisateur ne pioche pas de nouvelles cartes
        else:
            return True
 
    def menu_execute(self,param):
        """ Execution d'une instruction par le robot
        
        Parametres
        ----------
        param : type str
            action à effectuer par le robot
        
        Autres variables
        ----------------
        robot.win : type booléen
            on utilise cette variable au cas où le robot atteigne le drapeau avant la fin du programme
            
        Returns
        -------
        Cette méthode ne renvoit rien, elle déclenche simplement les actions adéquates
        """
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
    """ Classe définissant le joueur contrôlé par un utilisateur 
        Hérite de Joueur
    """
    def __init__(self,robot,playername):
        """ Constructeur de la classe : identique à celui de la classe mère """
        super().__init__(robot,playername)
        
    def make_program(self):
        """ Réalisation d'un tour par le joueur humain
            Il est demandé au joueur de chosir un programme parmi les cartes (aléatoires) qu'il a en main
            
            Returns
            -------
            self.menu : type liste
                cartes jouées par l'utilisateur pour ce tour
        """
        pgsize=min(5,self.robot_life) # Taille du programme (il dépend de la vie du robot)
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

        
class IA_Tout_Droit(Joueur):
    
    def __init__(self,robot,playername):
        super().__init__(robot,playername)
        self.robotDir = self.robot.dir
        self.coorFlag = self.robot.terrain.flag
        
    def mise_en_position(self):
        """Définit l'orientation dans laquelle le robot doit se mettre
        
        Returns
        -------
        direction_a_prendre : type int
            direction dans laquelle le robot doit se mettre pour aller au drapeau
        """
        posDrapeau = self.coorFlag
        if self.robot.x > posDrapeau[0]:
            direction_a_prendre = 0
        elif self.robot.x < posDrapeau[0]:
            direction_a_prendre = 2
        elif self.robot.y > posDrapeau[1]:
            direction_a_prendre = 3
        elif self.robot.y < posDrapeau[1]:
            direction_a_prendre = 1
        
        return direction_a_prendre


    def direction_rotation(self,robotDir,orientationOpti):
        """définit la carte à jouer pour que le robot se trouve dans la position optimale
        
        Parametres
        ----------
        robotDir : type int
            orientation actuelle du robot
        orientationOpti : type int
            orientation dans laquelle le robot doit se mettre
        
        Returns
        -------
        carte_a_jouer : type str
            mouvement à effectuer
        """
        carte_a_jouer = 0
        
        if robotDir == 0:
            if orientationOpti == 1 :
                carte_a_jouer = 'RR'
            elif orientationOpti == 2:
                carte_a_jouer = 'UT'
            elif orientationOpti == 3:
                carte_a_jouer = 'RL'
        
        elif robotDir == 1:
            if orientationOpti == 2 :
                carte_a_jouer = 'RR'
            elif orientationOpti == 3:
                carte_a_jouer = 'UT'
            elif orientationOpti == 0:
                carte_a_jouer = 'RL'
                
        elif robotDir == 2:
            if orientationOpti == 3 :
                carte_a_jouer = 'RR'
            elif orientationOpti == 0:
                carte_a_jouer = 'UT'
            elif orientationOpti == 1:
                carte_a_jouer = 'RL'
        
        elif robotDir == 3:
            if orientationOpti == 0 :
                carte_a_jouer = 'RR'
            elif orientationOpti == 1:
                carte_a_jouer = 'UT'
            elif orientationOpti == 2:
                carte_a_jouer = 'RL'
                
        return carte_a_jouer
            
            
    def make_program(self):
        pgsize = min(5,self.robot_life)
        remaining_choice = self.choice
        self.menu = []
        orientationOpti = self.mise_en_position()
        print("l'orientation optimale est : ", orientationOpti)
        print("coordonnees du robot : ",self.robot.x," ",self.robot.y)
        print("orientation du robot : ",self.robotDir)
        print("coordonnes du drapeau : ",self.coorFlag)
        flagOrientation = False
        flagAvancement = False
        for i in range(pgsize):
            rotationOpti = self.direction_rotation(self.robotDir,orientationOpti)
            print ("la rotation optimale est : ", rotationOpti)
            
            if rotationOpti !=0 :
                for carte in remaining_choice:
                    if carte == rotationOpti:
                        self.menu.append(carte)
                        remaining_choice.remove(carte)
                        flagOrientation = True
                        break
                    
            if flagOrientation == False and rotationOpti != 0:
                new_move = random.choice(remaining_choice)
                self.menu.append(new_move)
                if new_move !='Do_nothing':
                    remaining_choice.remove(new_move)
            else:
                for cartebis in remaining_choice:
                    if cartebis[0]=='M':
                        self.menu.append(cartebis)
                        remaining_choice.remove(cartebis)
                        flagAvancement = True
                if flagAvancement == False :
                    new_move = random.choice(remaining_choice)
                    self.menu.append(new_move)
                    if new_move !='Do_nothing':
                        remaining_choice.remove(new_move)
                    
        print('Les Dés sont jettés :')
        print('Menu : ',self.menu)
        return self.menu        

class IA_DevantMaisPasTrop(IA_Tout_Droit):
    
    def __init__(self,robot,playername):
        super().__init__(robot,playername)
        
    def distanceDrapeauX(self):
        """ Retourne la distance suivant X séparant le drapeau et le robot
            Prend en compte la direction du robot
            
            Returns
            -------
            dx : type None ou int
                distance suivant x entre le robot et le drapeau. Retourne None si le robot est orienté vers le nord ou le sud
        """
        if self.robotDir == 2 :
            dx = self.coorFlag[0] - self.robot.x
        elif self.robotDir == 0:
            dx = self.robot.x - self.coorFlag[0]
        else:
            dx = None
        return dx
        
    def distanceDrapeauY(self):
        """ Retourne la distance suivant Y séparant le drapeau et le robot
            Prend en compte la direction du robot
            
            Returns
            -------
            dy : type None ou int
                distance suivant y entre le robot et le drapeau. Retourne None si le robot est orienté vers l'est ou l'ouest
        """
        if self.robotDir == 3:
            dy = self.robot.y - self.coorFlag[1]
        elif self.robotDir == 1:
            dy = self.coorFlag[1] - self.robot.y
        else :
            dy = None
        return dy
    
    def renvoieBonneValeur(self,x,y):
        if x == None and y == None :
            return 1000
        elif x == None :
            return y
        elif y == None:
            return x
                      
    def make_program_V2(self):
        """ Realisation d'un tour de jeu
            Du fait que la classe hérite de IA_Tout_Droit, le V2 est de mise
            
            Return
            ------
            self.menu : type liste
                cartes choisies pour le tour de jeu
        """
        pgsize = min(5,self.robot_life)
        remaining_choice = self.choice
        self.menu = []
        orientationOpti = self.mise_en_position()
        print("l'orientation optimale est : ", orientationOpti)
        print("direction du robot : {}".format(self.robotDir))
        flagOrientation = False
        for i in range(pgsize):
            flagAvancement = False
            rotationOpti = self.direction_rotation(self.robotDir,orientationOpti)
            print ("la rotation optimale est : ", rotationOpti)
            
            if rotationOpti != 0 :
                for carte in remaining_choice:
                    if carte == rotationOpti:
                        self.menu.append(carte)
                        remaining_choice.remove(carte)
                        flagOrientation = True
                        break
                    
            if flagOrientation == False and rotationOpti != 0:
                new_move = random.choice(remaining_choice)
                self.menu.append(new_move)
                if new_move !='Do_nothing':
                    remaining_choice.remove(new_move)
            else:
                X = self.distanceDrapeauX()
                Y = self.distanceDrapeauY()
                valeurAvancementMax = self.renvoieBonneValeur(X,Y)
                for cartebis in remaining_choice:
                    if cartebis[0]=='M':
                        if int(cartebis[1]) <= valeurAvancementMax : #l'IA droit devant mais pas trop ne dépasse pas le drapeau
                            self.menu.append(cartebis)
                            remaining_choice.remove(cartebis)
                            flagAvancement = True
                if flagAvancement == False :
                    new_move = random.choice(remaining_choice)
                    self.menu.append(new_move)
                    if new_move !='Do_nothing':
                        remaining_choice.remove(new_move)
                    
        print('Les Dés sont jettés :')
        print('Menu : ',self.menu)
        return self.menu        

        
class Game:
    def __init__(self,terrain):
        """ Constructeur de la classe
        
        Parametres
        ----------
        terrain : fichier texte
            terrain de jeu pour la partie
        """
        self.terrain = terrain
        self.type = [Joueur_Humain,Joueur_Brownien,IA_Tout_Droit] #types d'IA et humain disponibles
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
        player_nb = int(input("Combien de joueurs disputerons cette partie ?\n Maximum de 4 joueurs   "))
        self.player_nb = min(player_nb,4)
        print("-----------------------")
        print("| Création des Robots |")
        print("-----------------------")
        for i in range(self.player_nb):
            self.robot_lst.append(Robot(self.terrain,"Twonky"))

        for s,i in enumerate(self.robot_lst):
            i.x,i.y = self.terrain.spawn[s][0],self.terrain.spawn[s][1]
            #self.robot_lst[i].rspawn = self.terrain.spawn[i]
            
        for i in range(self.player_nb):
            type,name = 'no','no'
            print("----------------------------")
            print("|Paramétrage du joueur {} : |".format(i+1))
            print("----------------------------")
            while type not in [1,2,3,4]:
                type = int(input("Type du Joueur {} \n 1: Human \n 2: COM (Brownien) \n 3: COM (IA_Tout_Droit) \n 4: COM (IA_Tout_Droit_Mais_Pas_Trop) \n".format(i+1)))
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
        for s,i in enumerate(self.robot_lst):
            print('le robot {} est en position {}'.format(s+1,(i.x,i.y)))
        
    def Game_state(self):
        a = self.terrain.carte
        for c,s in enumerate(a):
            for g,o in enumerate(s):
                if s[g]=='R':
                    s[g]==self.terrain.constantmap[c][g]
        for i in self.robot_lst:
            a[i.x][i.y]='R'
        print("voila ce qu'il y a après")
        self.terrain.Render()
        for i in self.player_lst:
            print("###########################")
            print("{} et son robot {}".format(i.name,i.robot.name))
            print("position : ({},{})".format(i.robot.x,i.robot.y))
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
