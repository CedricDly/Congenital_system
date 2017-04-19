# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 11:39:54 2017

@author: cedric
"""

import unittest
from Classes import Terrain,Robot

class TestTerrain(unittest.TestCase):
    """ cette classe sert aux tests unitaires de la classe Terrain"""
    
    def testInitTerrain(self):
        """test de la methode init de la classe terrain"""
        terrainTest=Terrain('Terrain_test.txt')
        self.assertEqual(terrainTest.file,'Terrain_test.txt')
        self.assertEqual(terrainTest.width,14)
        self.assertEqual(terrainTest.height,12)
        self.assertEqual(terrainTest.spawn,(1,1))
        
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
        robotTest = Robot(terrainTest,5,7,3)
        self.assertEqual(robotTest._Robot__x,5)
        self.assertEqual(robotTest._Robot__y,7)
        self.assertEqual(robotTest._Robot__dir,3)
        self.assertEqual(robotTest.life,9)
        self.assertIsNot(robotTest.win,True)
        
    def testTurnRight(self):
        """test de la methode virage droite de la classe Robot"""
        terrainTest=Terrain('Terrain_test.txt')        
        robotTest = Robot(terrainTest)
        robotTest.Turn_Right()
        self.assertEqual(robotTest._Robot__dir,2)
        
    def testTurnLeft(self):
        """test de la methode virage gauche de la classe Robot"""
        terrainTest=Terrain('Terrain_test.txt')        
        robotTest = Robot(terrainTest)
        robotTest.Turn_Left()
        self.assertEqual(robotTest._Robot__dir,0)
        
    def testUTurn(self):
        """test de la methode U-Turn de la classe Robot"""
        terrainTest=Terrain('Terrain_test.txt')        
        robotTest = Robot(terrainTest)
        robotTest.U_Turn()
        self.assertEqual(robotTest._Robot__dir,3)
    
    
if __name__ == '__main__':
    unittest.main()
    
