# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 11:39:54 2017

@author: cedric
"""

""" DISCLAIMER : Il est possible que vous remarquiez un problème sur la dernière ligne de la map (affichage de caractères supllémentaires).
                 Ceci est du a la difference d'encodage par defaut des fichiers textes entre Windows (CP1252 aka ANSI) et Linux (UTF-8). 
                 Ceci n'affecte en rien le deroulement des tests qui suivent.
"""
import unittest
from Classes import Terrain,Robot

class TestTerrain(unittest.TestCase):
    """ cette classe sert aux tests unitaires de la classe Terrain"""
    
    def testInitTerrain(self):
        """test de la methode init de la classe terrain"""
        terrainTest=Terrain('Terrain_test.txt')
        self.assertEqual(terrainTest.file,'Terrain_test.txt')
        self.assertEqual(terrainTest.width,17)
        self.assertEqual(terrainTest.height,11)
        self.assertEqual(terrainTest.spawn,[(1,1),(1,15),(9,1),(9,15)])
        
    def testLoadTerrain(self):
        """test de la methode Terrain.load()"""
        terrainTest=Terrain('Terrain_test.txt')
        loadtest = terrainTest.load('Terrain_test.txt')
        """ premiere etape : on extrait chaque ligne de notre terrain"""        
        fichier = open('Terrain_test.txt')
        lignes=fichier.readlines()
        fichier.close()
        for i in range(len(lignes)):
            lignes[i]=lignes[i].rstrip('\n')
                
        """deuxieme etape : on recree chaque ligne de loadtest (on aurait aussi pu a l'etape 1 
        scinder les lignes en case puis tester que chaque case soit identique)"""
        lignesDeLoadtest = []
        for j in range(len(loadtest)):
            ligne = ''
            for car in loadtest[j]:
                ligne+=car
            lignesDeLoadtest.append(ligne)
        self.assertEqual(len(lignesDeLoadtest),len(lignes))
        self.assertEqual(lignesDeLoadtest,lignes)
        
        
class TestRobot(unittest.TestCase):
    """cette classe sert aux tests unitaires de la classe Robot"""
    
    def testInitRobot(self):
        """test de la methode init de la classe Robot"""
        terrainTest=Terrain('Terrain_test.txt')        
        robotTest = Robot(terrainTest,'robotRandom')
        self.assertIn((robotTest.x,robotTest.y),[(1,1),(1,15),(9,1),(9,15)])
        self.assertIn(robotTest.dir,[0,1,2,3])
        self.assertEqual(robotTest.life,9)
        self.assertIsNot(robotTest.win,True)
        
    def testTurnRight(self):
        """test de la methode virage droite de la classe Robot"""
        terrainTest=Terrain('Terrain_test.txt')        
        robotTest = Robot(terrainTest,'RobotRandom')
        dirInit = robotTest.dir
        robotTest.Turn_Right()
        self.assertEqual(robotTest.dir,(dirInit+1)%4)
        
    def testTurnLeft(self):
        """test de la methode virage gauche de la classe Robot"""
        terrainTest=Terrain('Terrain_test.txt')        
        robotTest = Robot(terrainTest,'RobotRandom')
        dirInit = robotTest.dir
        robotTest.Turn_Left()
        self.assertEqual(robotTest.dir,(dirInit+3)%4)
        
    def testUTurn(self):
        """test de la methode U-Turn de la classe Robot"""
        terrainTest=Terrain('Terrain_test.txt')        
        robotTest = Robot(terrainTest,'RobotRandom')
        dirInit = robotTest.dir
        robotTest.U_Turn()
        self.assertEqual(robotTest.dir,(dirInit+2)%4)
        
    def testForward(self):
        """on va tester la methode forward de deux manieres : une ou il est possible d'avancer, et l'autre ou il y a un mur"""
        terrainTest=Terrain('Terrain_test.txt')        
        robotTest = Robot(terrainTest,'RobotRandom')
        
        robotTest.x,robotTest.y = 1,1 #on place volontairement le robot en (1,1)
        robotTest.dir = 2 #On oriente volontairement le robot vers le sud
        
        (X_init,Y_init) = (robotTest.x,robotTest.y)
        robotTest.Forward(1)
        self.assertEqual((robotTest.x,robotTest.y),(X_init+1,Y_init))
        
        #on teste maintenant que le robot ne va pas dans les murs
        robotTest.dir = 3
        (X_init,Y_init) = (robotTest.x,robotTest.y)
        robotTest.Forward(1)
        self.assertEqual((robotTest.x,robotTest.y),(X_init,Y_init))
        
    def testBackward(self):
        """on teste la methode backward de deux manieres : une ou il est possible de reculer, et l'autre ou il y a un mur"""
        terrainTest=Terrain('Terrain_test.txt')        
        robotTest = Robot(terrainTest,'RobotRandom')
        
        robotTest.x,robotTest.y = 1,1 #on place volontairement le robot en (1,1)
        robotTest.dir = 0 #On oriente volontairement le robot vers le nord
        
        (X_init,Y_init) = (robotTest.x,robotTest.y)
        robotTest.Backward()
        self.assertEqual((robotTest.x,robotTest.y),(X_init+1,Y_init))
        
        #on teste maintenant que le robot ne va pas dans les murs
        robotTest.dir = 1
        (X_init,Y_init) = (robotTest.x,robotTest.y)
        robotTest.Backward()
        self.assertEqual((robotTest.x,robotTest.y),(X_init,Y_init))
    
    
if __name__ == '__main__':
    print(" Lancement des tests unitaires ! ")
    unittest.main()
    
