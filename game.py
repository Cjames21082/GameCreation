import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys


#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 8
GAME_HEIGHT = 8

#### Put class definitions here ####
class Wall(GameElement):
    IMAGE = "Wall"
    SOLID = True

    # def wall_clear(self):
    #     global SOLID
    #     SOLID = False

class TallWall(Wall):
    IMAGE = "TallWall"
    SOLID = True

class Tree(GameElement):
    IMAGE = "UglyTree"
    SOLID = False

    def interact(self, player):
        global PLAYER
        global GEM_STORAGE

        GAME_BOARD.del_el(self.x, self.y)
        gem = Gem()
        gem.x = self.x
        gem.y = self.y
        print "I'm interacting with a tree!  yay! adding gem at: %d, %d" % (self.x, self.y)
        GAME_BOARD.register(gem)
        
        #remember the gem created for future usage
        GEM_STORAGE.append(gem)


class TallTree(Tree):
    IMAGE = "TallTree"
    SOLID = True

    def interact(self, player):     # override interact function from higher level - class Tree
        pass

class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Character(GameElement):
    
    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []


    IMAGE = "Horns"

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y + 1)
        elif direction == "left":
            return (self.x -1, self.y)
        elif direction == "right":
            return (self.x +1, self.y)

        return None

class MagicKey(GameElement):
    IMAGE = "Key"
    SOLID = False


class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False


    def interact(self, player):
        player.inventory.append(self)
        self.IMAGE = "Wall"
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!"%(len(player.inventory)))

        if len(player.inventory) >= 5:
            player_has_key(PLAYER)


####   End class definitions    ####

# open text map to set gameboard and create dictionary 

f = open("map.txt")
f_read = f.read()
f.close()

text_map = f_read.split()

set_board = {".": None, "+": TallWall, "-": Wall, "#": Tree, "*": TallTree, "$": Rock}

magic_key = MagicKey()

# function to place object on the scoreboard
def place_object_list(pos, object_type):
    obj = object_type()
    GAME_BOARD.register(obj)
    GAME_BOARD.set_el(pos[0], pos[1], obj)

def player_has_key(player):
    player.inventory.append(magic_key)
    GAME_BOARD.draw_msg("You just got the key to the castle -- GO RESCUE THE BOY!!!")
    GAME_BOARD.del_el(4,4)

def initialize():
    """Put game initialization code here"""

    # set key player on board
    global PLAYER
    global GEM_STORAGE

    GEM_STORAGE = []
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(1, 6, PLAYER)
    print PLAYER
    
    # read through text map to set up gameboard using the place_object list function
    for y in range(len(text_map)):
        for x in range(len(text_map[y])):
            pos = (x,y)
            if set_board.get(text_map[y][x]) == None:
                continue
            else:
                place_object_list(pos,set_board.get(text_map[y][x]))

    # set trapped boy
    boy = Character()
    boy.IMAGE = "Boy"
    GAME_BOARD.register(boy)
    GAME_BOARD.set_el(4,3,boy)

    # random start message
    GAME_BOARD.draw_msg("This game is wicked awesome.")
    print set_board.get(text_map[2][4])

def keyboard_handler():
    global text_map
    global GEM_STORAGE

    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"
    if KEYBOARD[key.DOWN]:
        direction = "down"
    if KEYBOARD[key.LEFT]:
        direction = "left"
    if KEYBOARD[key.RIGHT]:
        direction = "right"
    
    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        # handles the exception out of bounds and exits the function
        try:            
            existing_el = GAME_BOARD.get_el(next_x, next_y)
        #print type(existing_el)
        except IndexError:
            print "You have gone out of bounds!"
            return


        if existing_el:
            existing_el.interact(PLAYER) 
        
        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)
            #if GEM_STORAGE != []:                       # won't iterate if list is empty
            for g in GEM_STORAGE:
                if g.x != PLAYER.x or g.y != PLAYER.y:
                    GEM_STORAGE.pop(0)
                    GAME_BOARD.set_el(g.x, g.y,g)
                

