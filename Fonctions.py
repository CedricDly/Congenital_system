# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 14:51:02 2017

@author: o_pixou
"""
import Classes as c

def Robot_Test():    
    land = c.Terrain('window_test.txt')
    rob  = c.Robot(land,"Twonky")
        
    while not rob.win and rob.life>0:
        instruction = input('A votre service Maitre :\n 1-Turn_Right\n 2-Turn_Left \n 3-Forward \n 4-Backward \n 5-U-Turn \n 6-Quitter')
        if instruction == '1':
            rob.Turn_Right()
        elif instruction == '3':
            nb = input("De combien de cases Maiiiitre")
            nb=int(nb)
            rob.Forward(nb)
        elif instruction == '4':
            rob.Backward()
        elif instruction == '2':
            rob.Turn_Left()
        elif instruction == '5':
            rob.U_Turn()
        rob.handle_land()
        rob.handle_endturn()
    if rob.win:
        print('Félicitation Maiiiitre')
    else:
        print('Looser')
    
def Human_Player_Test():
    land = c.Terrain('Terrain_test.txt')
    rob  = c.Robot(land,"Twonky")
    player1 = c.Joueur_Humain(rob,'Pierre')
    while not player1.robot.win and player1.robot.life>0:
        player1.pick_cards()
        print('Picked cards ',player1.choice)
        player1.make_program()
        player1.menu_execute()
        print('Vie du Robot : ',player1.robot.life)
    if player1.robot.life<=0:
        print('looser')
    else :
        print("Félicitation Maitre")
        
        
def IA_Test_Brownien():
    land = c.Terrain('Terrain_test.txt')
    rob  = c.Robot(land,"Barry")
    player1 = c.Joueur_Brownien(rob,'Pierre')
    while not player1.robot.win and player1.robot.life>0:
        player1.pick_cards()
        print('Picked cards ',player1.choice)
        player1.make_program()
        player1.menu_execute()
        print('Vie du Robot : ',player1.robot.life)
    if player1.robot.life<=0:
        print('looser')
    else :
        print("Félicitation Maitre")


##############################################################################
###               Test section : Uncomment the one you need                ###
##############################################################################
#Robot_Test() 
#Human_Player_Test()
#IA_Test_Brownien()

land = c.Terrain('window_test.txt')
jeu =c. Game(land)