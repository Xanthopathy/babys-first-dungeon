# Emoji mappings
BACKGROUND_EMOJIS = {
    'wall': '⬛',  # White square for walls
    'floor': '⬜',
    'player': '😀',
    'enemy1': '👾',  # Level 1 enemy
    'enemy2': '👹',  # Level 2 enemy
    'enemy3': '😈',  # Level 3 enemy
    'sword': '🗡️',  # +2 power
    'shield': '🛡️',  # +3 power
    'empty_slot': '⬛',
    'door': '🚪',
    'boss': '👑'
}

# Game settings
BOARD_SIZE = 10
MAX_STEPS = 10
XP_LEVELS = {2: 5, 3: 10}  # XP needed for level 2, 3
HP_PER_LEVEL = {1: 10, 2: 15, 3: 20}  # Max HP per level
ENEMY_XP = {'enemy1': 1, 'enemy2': 2, 'enemy3': 3, 'boss': 5}  # XP per enemy
ENEMY_DAMAGE = {'enemy1': 1, 'enemy2': 2, 'enemy3': 3, 'boss': 5}  # Damage per enemy
ITEM_BONUSES = {'sword': 2, 'shield': 3}  # Power bonuses for items