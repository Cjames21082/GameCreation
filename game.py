import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

f = open("map.txt")
f_read = f.read()
f.close()

text_map = f_read.split()

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

class TallWall(GameElement):
    IMAGE = "TallWall"
    SOLID = True

class Tree(GameElement):
    IMAGE = "UglyTree"
    SOLID = False

class TallTree(GameElement):
    IMAGE = "TallTree"
    SOLID = True

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


class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!"%(len(player.inventory)))

####   End class definitions    ####

def place_object_list(pos, object_type):

    #objects = []

    # for pos in positions:
    obj = object_type()
    GAME_BOARD.register(obj)
    GAME_BOARD.set_el(pos[0], pos[1], obj)
    #objects.append(obj)

    #return objects


def initialize():
    """Put game initialization code here"""

    set_board = {".": None, "+": TallWall, "-": Wall, "#": Tree, "*": TallTree, "$": Rock}

    for y in range(len(text_map)):
        for x in range(len(text_map[y])):
            pos = (x,y)
            if set_board.get(text_map[y][x]) == None:
                continue
            else:
                place_object_list(pos,set_board.get(text_map[y][x]))


    # rock_positions = [
    #         (1,3),
    #         (3,1),
    #         (3,5)
    # ]   

    # rocks = place_object_list(rock_positions, Rock)
    # # rocks[-1].SOLID = False
        
    # for rock in rocks:
    #     print rock

    # # Build the wall that traps the stupid boy.
    # wall_positions = [
    #         (3,3),
    #         (4,2),
    #         (4,4),
    #         (5,3)
    # ]

    # tallwall_positions = [
    #         (3,2),
    #         (3,4),
    #         (5,2),
    #         (5,4)
    # ]


    # walls = place_object_list(wall_positions, Wall)
    # talls = place_object_list(tallwall_positions, TallWall)

    boy = Character()
    boy.IMAGE = "Boy"
    GAME_BOARD.register(boy)
    GAME_BOARD.set_el(4,3,boy)

    # tree_positions = [
    #         (0,1),
    #         (0,6),
    #         (4,0),
    #         (5,7),
    #         (4,6),
    #         (6,5),
    #         (5,5),
    #         (5,6),
    #         (6,6),
    #         (6,7),
    #         (2,6),
    #         (7,2)
    # ]

    # trees = place_object_list(tree_positions, Tree)
    
    # tall_tree = Tree()
    # tall_tree.IMAGE = "TallTree"
    # tall_tree.SOLID = True
    # GAME_BOARD.register(tall_tree)
    # GAME_BOARD.set_el(7, 0 , tall_tree)

    # In the initialize() function
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 2, PLAYER)
    print PLAYER
    
    GAME_BOARD.draw_msg("This game is wicked awesome.")

    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(2, 1, gem)

def keyboard_handler():
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

        existing_el = GAME_BOARD.get_el(next_x, next_y)

        if existing_el:
            existing_el.interact(PLAYER) 
        
        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)

