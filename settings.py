"""Settings from the game"""
import pygame as pg

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
EPIC = (163, 53, 238)
RARE = (0, 112, 221)
COMMON = (255, 255, 255)

# game settings
WIDTH = 1920  # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 1080  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Dungeon And Python"
BGCOLOR = BROWN
SPACING = 100


TILESIZE = 36
COLS = WIDTH / TILESIZE
ROWS = HEIGHT / TILESIZE

# Player settings
PLAYER_SPEED = 175
PLAYER_ROT_SPEED = 250
PLAYER_IMG = "robot1_gun.png"
PLAYER_HIT_RECT = pg.Rect(0, 0, 10, 10)
DELTA = 2
PM = 230
PLAYER_HEALTH = 100
PLAYER_MANA = 50
WIZARD_IMG = "Wizard.png"
ROGUE_IMG = "Rogue.png"  
BARBARIAN_IMG = "Barbarian.png"

# Wall settings
WALL_IMG = "tile.png"
GROUND_IMG = "ground.png"
ZOMBIE_GROUND_IMG = "zombie_ground.png"
VOID_IMG = "void.png"
PATH_IMG = "path.png"
REACHABLE_IMG = "reachable.png"
VOID_EDITOR_IMG = "void_editor.png"
PORTAL_IMG = "portal.png"
BACK_PORTAL_IMG = "back_portal.png"
PNJ_IMG = "pnj.png"  # Name of the folder with the image of PNJ
MERCHANT_IMG = "merchant.png"
AOE_TILE_IMG = "area_zone.png"
CONTAINER_IMG = "Container.png"


# Zombie settings
ZOMBIE_IMG = "zombie.png"
SKELETON_IMG = "skeleton.png" 
MINOTAUR_IMG = "Minotaur.png"
WOLF_IMG = "wolf.png" 
GOBLIN_IMG = "gobelin.png"
ZOMBIE_SPEED = [150, 100, 75, 125, 150]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
ZOMBIE_SPEED = [150, 100, 75, 125, 150]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
ZOMBIE_HEALTH = 70
ZOMBIE_DAMAGE = 15
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
ATTACK_RADIUS = 300
SHARE_KNOWLEDGE_RADIUS = 100

# Skill visualisation
HEAL_SKILL = "heal.png"

INVENTORY_IMG = "img_inventory.png"
INVENTORY_SELECTED = "selected.png"
INVENTORY_IMG_PNJ = "img_inventory_pnj.png"
