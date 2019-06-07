import pygame as pg
import sys
import time
import argparse
import copy
pg.init()

fname = sys.argv[1]
input_list1 = []

fp = open("%s"%(fname),"r")
for f in fp:
  input_list1.append(f)
input_list1 = [el.replace('\n', '') for el in input_list1]
        #self.input_list.insert(0, self.input_list[0])
#input_list1.append('nil')
WIDTH = int(input_list1[0])
HEIGHT = int(input_list1[1])
#input_list1 = input_list1[2:]


# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
#WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
#HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
TILESIZE =int(input_list1[2])

FPS = 1
TITLE = "Moving Robot - Roll No 15131, 15116, 15105"
BGCOLOR = DARKGREY

GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y, img):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #self.image = pg.image.load("robot.png").convert()
        self.image = pg.image.load(img).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy
        print "Robot x= ", self.x
        print "Robot y= ", self.y

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Game:
    def __init__(self):
        pg.init()
        self.collide_flag = False
        self.coin_taken   = False
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        self.fname = sys.argv[1]
        self.input_list = []

        fp = open("%s"%(self.fname),"r")
        for f in fp: 
            self.input_list.append(f)
        self.input_list = [el.replace('\n', '') for el in self.input_list]
        #self.input_list.insert(0, self.input_list[0])
        self.input_list.append('nil')
        self.robot_x = int(self.input_list[3])
        self.robot_y = int(self.input_list[4]) 
        self.input_list = self.input_list[5:]

        print self.input_list

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.robot = Player(self, self.robot_x, self.robot_y, "robot.png")
        print "Robot x= ", self.robot.x
        print "Robot y= ", self.robot.y
        self.coin = Player(self, 4, 5, "coin.png")
#        self.coin1 = player(self,2,2,"coin.png")
        print "Coin x= ", self.coin.x
        print "Coin y= ", self.coin.y

    def run(self):
        # game loop - set self.playing = False to end the game
        for position in self.input_list:
            print position
            self.dt = self.clock.tick(FPS)
            if self.collide_flag:
                self.coin_collide()
            if self.coin_taken:
                rect_border = self.coin.image  # reate a Surface to draw on.
                pg.draw.rect(rect_border, LIGHTGREY, rect_border.get_rect(), 1)  # Draw on it.
                self.screen.blit(rect_border, ((self.coin.x * TILESIZE) - 1, (self.coin.y * TILESIZE) - 1))
            self.events(position)
            self.update()
            self.draw()
    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()


    def coin_collide(self):
        rect_filled = self.coin.image
        pg.draw.rect(rect_filled, BGCOLOR, rect_filled.get_rect())  # Draw on it.
        self.screen.blit(rect_filled, (self.coin.x * TILESIZE, self.coin.y * TILESIZE))
            
        self.coin_taken   = True
        self.collide_flag = False

        pg.display.flip()
        
    def events(self, position):
        # catch all events here
        if position.lower() == 'up':
            self.robot.move(dy=-1)
        elif position.lower() == 'down':
            self.robot.move(dy=1)
        elif position.lower() == 'right':
            self.robot.move(dx=1)
        elif position.lower() == 'left':
            self.robot.move(dx=-1)
        elif position.lower() == 'stay':
            self.robot.move(dx=0)
        elif position.lower() == 'nil':
            self.quit()
        
        if self.robot.x == self.coin.x and \
            self.robot.y == self.coin.y:
            print "Robot and coin at same location"
            self.coin_taken   = False
            self.collide_flag = True
            self.coin_collide_x = self.coin.x
            self.coin_collide_y = self.coin.y

            robot_image = copy.copy(self.robot.image)
            self.coin.image = robot_image
            pg.display.update()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
#g.show_start_screen()
while True:
    g.new()
    g.run()
    #g.show_go_screen()
