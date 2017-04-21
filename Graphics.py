# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 11:33:53 2017

@author: o_pixou
"""

import pygame
pygame.init()


######################
#ELEMENTS DE TERRAINS#
######################

mur       = pygame.image.load("Mur.png")
sol       = pygame.image.load("Sol.png")
trou      = pygame.image.load("Trou.png")
flag      = pygame.image.load("Drapeau.png")
hwall     = pygame.image.load("Wall.png")
lwall     = pygame.transform.rotate(hwall,90)
dwall     = pygame.transform.rotate(hwall,180)
rwall     = pygame.transform.rotate(hwall,270)
TLCorner  = pygame.image.load("TLCorner.png")
BLCorner  = pygame.transform.rotate(TLCorner,90)
BRCorner  = pygame.transform.rotate(TLCorner,180)
TRCorner  = pygame.transform.rotate(TLCorner,270)
hlaser    = pygame.image.load("Mur_Laser.png")
llaser    = pygame.transform.rotate(hlaser,90)
dlaser    = pygame.transform.rotate(hlaser,180)
rlaser    = pygame.transform.rotate(hlaser,270)
Rconveyor = pygame.image.load("Conveyor.png")
Hconveyor = pygame.transform.rotate(Rconveyor,90)
Lconveyor = pygame.transform.rotate(Rconveyor,180)
Dconveyor = pygame.transform.rotate(Rconveyor,270)
CRotation = pygame.image.load("TournetteC.png")
ARotation = pygame.image.load("TournetteA.png")
MH        = pygame.image.load("mur haut.png")
MG        = pygame.image.load("mur gauche.png") 
MD        = pygame.image.load("mur droite.png")
MB        = pygame.image.load("mur bas.png")
MBD       = pygame.image.load("mur bas droite.png")
MBG       = pygame.image.load("mur bas gauche.png")
MGD       = pygame.image.load("mur gauche droite.png")
MHB       = pygame.image.load("mur haut bas.png")
MHD       = pygame.image.load("mur haut droite.png")             
MHG       = pygame.image.load("mur haut gauche.png")  
Tiles = {'W':mur,' ':sol,'H':trou,'F':flag,'-':hwall,'*':lwall,'/':dwall,'+':rwall,'#':TLCorner,'$':TRCorner,\
'€':BLCorner,'£':BRCorner,'P': hlaser,'O':llaser,'M':dlaser,'L':rlaser,'D':Rconveyor,'Z':Hconveyor,'Q':Lconveyor,'S':Dconveyor,\
'V':CRotation,'C':ARotation,'0':MH,'1':MD,'2':MB,'3':MG,'4':MHG,'5':MHD,'6':MBD,'7':MBG,'8':MHB,'9':MGD}

#####
#HUD#
#####
HUD = pygame.image.load("hud.png")
chud = pygame.image.load("chud.png")
fond = pygame.image.load("maxresdefault.jpg")

########
#ROBOTS#
########
base = pygame.image.load("Robot_I_2.png")