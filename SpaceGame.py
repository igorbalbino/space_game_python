import pygame
import os
import time
import random

pygame.font.init()

print(f'getting dependencies...{os.linesep}')
#set game window
WIDTH, HEIGHT = 700, 750
GAME_WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE GAME TUTORIAL")
#load game assets
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
#player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
#lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
#background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

class Util:
    def __init__(self):
        print(f'init Util class{os.linesep}')
    #__init__
#Util

class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cooldown_counter = 0
    #__init__

    def draw(self, window):
        #cria retangulo com os parametros "local <onde desenhar>, cor, (position and size), pizel size"
        #pygame.draw.rect(window, (255,0,0), (self.x, self.y, 50, 50), 2)
        #old line ^
        window.blit(self.ship_img, (self.x,  self.y))
    #draw

    #retorna o tamanho da superficie no eixo x
    def get_width(self):
        return self.ship_img.get_width()

    # retorna o tamanho da superficie no eixo y
    def get_height(self):
        return self.ship_img.get_height()
    #get_width
#Ship

class Player(Ship):
    def __init__(self, x, y, health=100):
        #call __init__ from extention class Ship - where super() references Ship
        super().__init__(x, y, health)
        #VAR SHOULD BE GLOBAL
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        #create a mask using the surface "self.ship_img"
        #agora sabemos onde os pixels estão ou não estão, e sabemos quando eles colidem com outros pixels
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
#Player

class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
    }
    def __init__(self, x, y, color, health=100):
        #call __init__ from extention class Ship - where super() references Ship
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
    #__init__

    def move(self, vel):
        self.y += vel
    #move

    def remove(self):
        print("remove enemy")
    #remove
#Enemy

class SpaceGame:
    def __init__(self):
        print(f'init Game class{os.linesep}')
        self.gameUtil = Util()
        self.main()
    #__init__

    def main(self):
        #keep the game running
        run = True
        #check the game every n times
        FPS = 60
        level = 0
        lives = 5
        main_font = pygame.font.SysFont("comicsans", 50)

        #enemies status
        enemies = []
        wave_length = 5
        enemy_vel = 1

        #velocidade que o player se movimenta
        player_vel = 10

        #instancia classe player
        player = Player(WIDTH/2.4, HEIGHT - (player_vel+100))
        #pygame lib for tome
        clock = pygame.time.Clock()

        lost = False

        #reedraw thescreen with updated elements
        def redraw_window():
            #position the element "BG" in x=0 and y=0
            GAME_WINDOW.blit(BG, (0,0))
            #create text drawing
            level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
            lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))

            #set the x position of level_label
            x = WIDTH - level_label.get_width() - 10

            #set position in screen
            GAME_WINDOW.blit(lives_label, (10,10))
            GAME_WINDOW.blit(level_label, (x, 10))

            for enemy in enemies:
                enemy.draw(GAME_WINDOW)

            player.draw(GAME_WINDOW)

            pygame.display.update()
        #redraw_window

        while run:
            #check the game
            clock.tick(FPS)

            if lives <= 0 or player.health <= 0:
                lost = True

                #PAREI AQUIIIIIIIIIIIIII

            if len(enemies) == 0:
                level += 1
                wave_length += 5
                for i in range(wave_length):
                    enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -30), random.choice(["red","green","blue"]))
                    enemies.append(enemy)

            #se algum evento ocorrer, esse é pego por "pygame.event.get()"
            for event in pygame.event.get():
                #validaçoes de movimento não ficaram aqui pois
                #se feitas aqui, só poderiam ser checadas uma tecla de cada vez
                #nesse caso, movimentos diagonais seriam impossiveis
                if event.type == pygame.QUIT:
                    run = False

            #capturando teclas e movimentando elemento
            #return the dictionary of the pressed keys
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[pygame.K_w] and player.y - player_vel > 5:
                player.y -= player_vel
            if keys[pygame.K_DOWN] or keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT:
                player.y += player_vel
            if keys[pygame.K_LEFT] or keys[pygame.K_a] and player.x - player_vel > 0:
                player.x -= player_vel
            if keys[pygame.K_RIGHT] or keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:
                player.x += player_vel

            #using [:] makes a copy
            for enemy in enemies[:]:
                enemy.move(enemy_vel)
                if enemy.y + enemy.get_height() > HEIGHT:
                    lives -= 1
                    enemy.remove(enemy)

            #call redraw_window()
            redraw_window()

    #main
#SpaceGame

startGameVar = SpaceGame()