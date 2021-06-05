import pygame
import os
import time
import random
pygame.font.init()

class Util:
    def __init__(self):
        print(f'init Util class{os.linesep}')
    #__init__
#Util

class SpaceGame:
    def __init__(self):
        print(f'init Game class{os.linesep}')
        print(f'charging dependencies...{os.linesep}')
        self.gameUtil = Util()
        #set game window
        self.WIDTH, self.HEIGHT = 650, 650
        self.GAME_WINDOW = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("SPACE GAME TUTORIAL")
        #load game assets
        self.RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
        self.GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
        self.BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
        #player ship
        self.YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
        #lasers
        self.RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
        self.GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
        self.BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
        self.YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
        #background
        self.BG = pygame.image.load(os.path.join("assets", "background-black.png"))
        self.main()
    #__init__

    def main(self):
        #keep the game running
        run = True
        #check the game every n times
        FPS = 60

        level = 1
        lives = 5
        main_font = pygame.font.SysFont("comicsans", 50)
        #pygame lib for tome
        clock = pygame.time.Clock()

        #reedraw thescreen with updated elements
        def redraw_window():
            self.GAME_WINDOW.blit(self.BG, (0,0))
            #draw text
            level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
            lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))

            x = self.WIDTH - level_label.get_width() - 10
            #set position in screen
            self.GAME_WINDOW.blit(lives_label, (10,10))
            self.GAME_WINDOW.blit(level_label, (x, 10))



            pygame.display.update()
        #redraw_window

        while run:
            #check the game
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
    #main
#SpaceGame

startGameVar = SpaceGame()