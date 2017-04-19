#coding:utf8
import pygame
import sys
import Graphics as g
pygame.init()
import Classes as c
def main():
 
    screen = pygame.display.set_mode((1000,1000))
    pygame.display.set_caption("Visualisation d'un terrain")
    background = pygame.Surface(screen.get_size())
    terrain = c.Terrain('Terrain_test.txt')
    for s,i in enumerate(terrain.carte):
        for b,j in enumerate(i):
            background.blit(g.Tiles[i[b]],(b*51,s*51))

    screen.blit(background,(0,0))
    kp=True
    FPS = 60
    clock=pygame.time.Clock()
    while kp:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event == pygame.QUIT:
                pygame.quit()
                sys.exit()
                kp =False
        pygame.display.flip()
        
main()
