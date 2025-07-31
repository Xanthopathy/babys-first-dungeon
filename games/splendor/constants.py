# Resource tokens
TOKENS = { # RGBWKY
    'ruby': {'emoji': '🔴', 'count': 7},
    'emerald': {'emoji': '🟢', 'count': 7},
    'sapphire': {'emoji': '🔵', 'count': 7},
    'diamond': {'emoji': '⚪', 'count': 7},
    'onyx': {'emoji': '🟣', 'count': 7},
    'gold': {'emoji': '🟡', 'count': 5} # Joker token, does not show up as a resource on the cards/tiles
}

GEM_MAP = {
    'ruby': 'ruby', 'r': 'ruby', 'red': 'ruby', '🔴': 'ruby',
    'emerald': 'emerald', 'e': 'emerald', 'green': 'emerald', 'g': 'emerald', '🟢': 'emerald',
    'sapphire': 'sapphire', 's': 'sapphire', 'blue': 'sapphire', 'b': 'sapphire', '🔵': 'sapphire',
    'diamond': 'diamond', 'd': 'diamond', 'white': 'diamond', 'w': 'diamond', '⚪': 'diamond',
    'onyx': 'onyx', 'o': 'onyx', 'purple': 'onyx', 'p': 'onyx', '🟣': 'onyx',
}

# Permanent resources
RESOURCES = {
    'ruby': {'emoji': '🟥'},
    'emerald': {'emoji': '🟩'},
    'sapphire': {'emoji': '🟦'},
    'diamond': {'emoji': '⬜'},
    'onyx': {'emoji': '🟪'}
}

# Development cards (🔴🟢🔵⚪🟣 order)
DEVELOPMENT_CARDS = { # amount are from base game, can extend to make an algorithm that generates cards
    'level_1': [ # 40 total, 8 of each resource, 0-1 prestige (7x 0, 1x 1)
        # ruby
        {'resource': 'ruby', 'prestige': 0, 'cost': {'ruby': 1, 'emerald': 1, 'sapphire': 1, 'diamond': 1}},
        {'resource': 'ruby', 'prestige': 0, 'cost': {'ruby': 1, 'emerald': 1, 'sapphire': 2, 'diamond': 1}},
        {'resource': 'ruby', 'prestige': 0, 'cost': {'ruby': 1, 'sapphire': 2, 'diamond': 2}},
        {'resource': 'ruby', 'prestige': 0, 'cost': {'ruby': 3, 'emerald': 1, 'onyx': 1}},
        {'resource': 'ruby', 'prestige': 0, 'cost': {'ruby': 1, 'emerald': 2}},
        {'resource': 'ruby', 'prestige': 0, 'cost': {'emerald': 2, 'diamond': 2}},
        {'resource': 'ruby', 'prestige': 0, 'cost': {'emerald': 3}},
        {'resource': 'ruby', 'prestige': 1, 'cost': {'sapphire': 4}},
        # emerald
        {'resource': 'emerald', 'prestige': 0, 'cost': {'ruby': 1, 'sapphire': 1, 'diamond': 1, 'onyx': 1}},
        {'resource': 'emerald', 'prestige': 0, 'cost': {'ruby': 1, 'sapphire': 1, 'diamond': 1, 'onyx': 2}},
        {'resource': 'emerald', 'prestige': 0, 'cost': {'ruby': 2, 'sapphire': 1, 'onyx': 2}},
        {'resource': 'emerald', 'prestige': 0, 'cost': {'emerald': 1, 'sapphire': 3, 'diamond': 1}},
        {'resource': 'emerald', 'prestige': 0, 'cost': {'sapphire': 1, 'diamond': 2}},
        {'resource': 'emerald', 'prestige': 0, 'cost': {'ruby': 2, 'sapphire': 2}},
        {'resource': 'emerald', 'prestige': 0, 'cost': {'ruby': 3}},
        {'resource': 'emerald', 'prestige': 1, 'cost': {'onyx': 4}},
        # sapphire
        {'resource': 'sapphire', 'prestige': 0, 'cost': {'ruby': 1, 'emerald': 1, 'diamond': 1, 'onyx': 1}},
        {'resource': 'sapphire', 'prestige': 0, 'cost': {'ruby': 2, 'emerald': 1, 'diamond': 1, 'onyx': 1}},
        {'resource': 'sapphire', 'prestige': 0, 'cost': {'ruby': 2, 'emerald': 2, 'diamond': 1}},
        {'resource': 'sapphire', 'prestige': 0, 'cost': {'ruby': 1, 'emerald': 3, 'sapphire': 1}},
        {'resource': 'sapphire', 'prestige': 0, 'cost': {'diamond': 1, 'onyx': 2}},
        {'resource': 'sapphire', 'prestige': 0, 'cost': {'emerald': 2, 'onyx': 2}},
        {'resource': 'sapphire', 'prestige': 0, 'cost': {'onyx': 3}},
        {'resource': 'sapphire', 'prestige': 1, 'cost': {'ruby': 4}},
        # diamond
        {'resource': 'diamond', 'prestige': 0, 'cost': {'ruby': 1, 'emerald': 1, 'sapphire': 1, 'onyx': 1}},
        {'resource': 'diamond', 'prestige': 0, 'cost': {'ruby': 1, 'emerald': 2, 'sapphire': 1, 'onyx': 1}},
        {'resource': 'diamond', 'prestige': 0, 'cost': {'emerald': 2, 'sapphire': 2, 'onyx': 1}},
        {'resource': 'diamond', 'prestige': 0, 'cost': {'sapphire': 1, 'diamond': 3, 'onyx': 1}},
        {'resource': 'diamond', 'prestige': 0, 'cost': {'ruby': 2, 'onyx': 1}},
        {'resource': 'diamond', 'prestige': 0, 'cost': {'sapphire': 2, 'onyx': 2}},
        {'resource': 'diamond', 'prestige': 0, 'cost': {'sapphire': 3}},
        {'resource': 'diamond', 'prestige': 1, 'cost': {'emerald': 4}},
        # onyx
        {'resource': 'onyx', 'prestige': 0, 'cost': {'ruby': 1, 'emerald': 1, 'sapphire': 1, 'diamond': 1}},
        {'resource': 'onyx', 'prestige': 0, 'cost': {'ruby': 1, 'emerald': 1, 'sapphire': 1, 'diamond': 2}},
        {'resource': 'onyx', 'prestige': 0, 'cost': {'emerald': 1, 'diamond': 2, 'onyx': 2}},
        {'resource': 'onyx', 'prestige': 0, 'cost': {'ruby': 1, 'diamond': 1, 'onyx': 3}},
        {'resource': 'onyx', 'prestige': 0, 'cost': {'emerald': 1, 'sapphire': 2}},
        {'resource': 'onyx', 'prestige': 0, 'cost': {'ruby': 2, 'diamond': 2}},
        {'resource': 'onyx', 'prestige': 0, 'cost': {'diamond': 3}},
        {'resource': 'onyx', 'prestige': 1, 'cost': {'diamond': 4}},
    ],
    'level_2': [ # 30 total, 6 of each resource, 1-3 prestige(2x 1, 3x 2, 1x 3)
        # ruby
        {'resource': 'ruby', 'prestige': 1, 'cost': {'ruby': 2, 'sapphire': 3, 'onyx': 3}},
        {'resource': 'ruby', 'prestige': 1, 'cost': {'ruby': 2, 'diamond': 2, 'onyx': 3}},
        {'resource': 'ruby', 'prestige': 2, 'cost': {'emerald': 2, 'sapphire': 4, 'diamond': 1}},
        {'resource': 'ruby', 'prestige': 2, 'cost': {'diamond': 3, 'onyx': 5}},
        {'resource': 'ruby', 'prestige': 2, 'cost': {'onyx': 5}},
        {'resource': 'ruby', 'prestige': 3, 'cost': {'ruby': 6}},
        # emerald
        {'resource': 'emerald', 'prestige': 1, 'cost': {'ruby': 3, 'emerald': 2, 'diamond': 3}},
        {'resource': 'emerald', 'prestige': 1, 'cost': {'sapphire': 3, 'diamond': 2, 'onyx': 2}},
        {'resource': 'emerald', 'prestige': 2, 'cost': {'sapphire': 2, 'diamond': 4, 'onyx': 1}},
        {'resource': 'emerald', 'prestige': 2, 'cost': {'emerald': 3, 'sapphire': 5}},
        {'resource': 'emerald', 'prestige': 2, 'cost': {'emerald': 5}},
        {'resource': 'emerald', 'prestige': 3, 'cost': {'emerald': 6}},
        # sapphire
        {'resource': 'sapphire', 'prestige': 1, 'cost': {'ruby': 3, 'emerald': 2, 'sapphire': 2}},
        {'resource': 'sapphire', 'prestige': 1, 'cost': {'emerald': 3, 'sapphire': 2, 'onyx': 3}},
        {'resource': 'sapphire', 'prestige': 2, 'cost': {'sapphire': 3, 'diamond': 5}},
        {'resource': 'sapphire', 'prestige': 2, 'cost': {'ruby': 1, 'diamond': 2, 'onyx': 4}},
        {'resource': 'sapphire', 'prestige': 2, 'cost': {'sapphire': 5}},
        {'resource': 'sapphire', 'prestige': 3, 'cost': {'sapphire': 6}},
        # diamond
        {'resource': 'diamond', 'prestige': 1, 'cost': {'ruby': 2, 'emerald': 3, 'onyx': 2}},
        {'resource': 'diamond', 'prestige': 1, 'cost': {'ruby': 3, 'sapphire': 3, 'diamond': 2}},
        {'resource': 'diamond', 'prestige': 2, 'cost': {'ruby': 4, 'emerald': 1, 'onyx': 2}},
        {'resource': 'diamond', 'prestige': 2, 'cost': {'ruby': 5, 'onyx': 3}},
        {'resource': 'diamond', 'prestige': 2, 'cost': {'ruby': 5}},
        {'resource': 'diamond', 'prestige': 3, 'cost': {'diamond': 6}},
        # onyx
        {'resource': 'onyx', 'prestige': 1, 'cost': {'emerald': 2, 'diamond': 3, 'onyx': 2}},
        {'resource': 'onyx', 'prestige': 1, 'cost': {'emerald': 3, 'diamond': 3, 'onyx': 2}},
        {'resource': 'onyx', 'prestige': 2, 'cost': {'ruby': 2, 'emerald': 4, 'sapphire': 1}},
        {'resource': 'onyx', 'prestige': 2, 'cost': {'ruby': 3, 'emerald': 5}},
        {'resource': 'onyx', 'prestige': 2, 'cost': {'diamond': 5}},
        {'resource': 'onyx', 'prestige': 3, 'cost': {'onyx': 6}},
    ],
    'level_3': [ # 20 total, 4 of each resource, 3-5 prestige (1x 3, 2x 4, 1x 5)
        # ruby
        {'resource': 'ruby', 'prestige': 3, 'cost': {'ruby': 3, 'emerald': 3, 'sapphire': 5, 'diamond': 3, 'onyx': 3}},
        {'resource': 'ruby', 'prestige': 4, 'cost': {'emerald': 7}},
        {'resource': 'ruby', 'prestige': 4, 'cost': {'ruby': 3, 'emerald': 6, 'onyx': 3}},
        {'resource': 'ruby', 'prestige': 5, 'cost': {'ruby': 3, 'emerald': 7}},
        # emerald
        {'resource': 'emerald', 'prestige': 3, 'cost': {'ruby': 3, 'sapphire': 3, 'diamond': 5, 'onyx': 3}},
        {'resource': 'emerald', 'prestige': 4, 'cost': {'sapphire': 7}},
        {'resource': 'emerald', 'prestige': 4, 'cost': {'emerald': 3, 'sapphire': 6, 'diamond': 3}},
        {'resource': 'emerald', 'prestige': 5, 'cost': {'emerald': 3, 'sapphire': 7}},
        # sapphire
        {'resource': 'sapphire', 'prestige': 3, 'cost': {'ruby': 3, 'emerald': 3, 'diamond': 3, 'onyx': 5}},
        {'resource': 'sapphire', 'prestige': 4, 'cost': {'diamond': 7}},
        {'resource': 'sapphire', 'prestige': 4, 'cost': {'sapphire': 3, 'diamond': 6, 'onyx': 3}},
        {'resource': 'sapphire', 'prestige': 5, 'cost': {'sapphire': 3, 'diamond': 7}},
        # diamond
        {'resource': 'diamond', 'prestige': 3, 'cost': {'ruby': 5, 'emerald': 3, 'sapphire': 3, 'onyx': 3}},
        {'resource': 'diamond', 'prestige': 4, 'cost': {'onyx': 7}},
        {'resource': 'diamond', 'prestige': 4, 'cost': {'ruby': 3, 'diamond': 3, 'onyx': 6}},
        {'resource': 'diamond', 'prestige': 5, 'cost': {'diamond': 3, 'onyx': 7}},
        # onyx
        {'resource': 'onyx', 'prestige': 3, 'cost': {'ruby': 3, 'emerald': 5, 'sapphire': 3, 'diamond': 3}},
        {'resource': 'onyx', 'prestige': 4, 'cost': {'ruby': 7}},
        {'resource': 'onyx', 'prestige': 4, 'cost': {'ruby': 6, 'emerald': 3, 'onyx': 3}},
        {'resource': 'onyx', 'prestige': 5, 'cost': {'ruby': 7, 'onyx': 3}},
    ],
}

# Noble tiles (🔴🟢🔵⚪🟣 order)
NOBLE_TILES = [
    # 4-4
    {'prestige': 3, 'bonuses': {'ruby': 4, 'emerald': 4}},
    {'prestige': 3, 'bonuses': {'ruby': 4, 'sapphire': 4}},
    {'prestige': 3, 'bonuses': {'ruby': 4, 'diamond': 4}},
    {'prestige': 3, 'bonuses': {'ruby': 4, 'onyx': 4}},
    {'prestige': 3, 'bonuses': {'emerald': 4, 'sapphire': 4}},
    {'prestige': 3, 'bonuses': {'emerald': 4, 'diamond': 4}},
    {'prestige': 3, 'bonuses': {'emerald': 4, 'onyx': 4}},
    {'prestige': 3, 'bonuses': {'sapphire': 4, 'diamond': 4}},
    {'prestige': 3, 'bonuses': {'sapphire': 4, 'onyx': 4}},
    {'prestige': 3, 'bonuses': {'diamond': 4, 'onyx': 4}},
    # 3-3-3
    {'prestige': 3, 'bonuses': {'ruby': 3, 'emerald': 3, 'sapphire': 3}},
    {'prestige': 3, 'bonuses': {'ruby': 3, 'emerald': 3, 'diamond': 3}},
    {'prestige': 3, 'bonuses': {'ruby': 3, 'emerald': 3, 'onyx': 3}},
    {'prestige': 3, 'bonuses': {'ruby': 3, 'sapphire': 3, 'diamond': 3}},
    {'prestige': 3, 'bonuses': {'ruby': 3, 'sapphire': 3, 'onyx': 3}},
    {'prestige': 3, 'bonuses': {'ruby': 3, 'diamond': 3, 'onyx': 3}},
    {'prestige': 3, 'bonuses': {'emerald': 3, 'sapphire': 3, 'diamond': 3}},
    {'prestige': 3, 'bonuses': {'emerald': 3, 'sapphire': 3, 'onyx': 3}},
    {'prestige': 3, 'bonuses': {'emerald': 3, 'diamond': 3, 'onyx': 3}},
    {'prestige': 3, 'bonuses': {'sapphire': 3, 'diamond': 3, 'onyx': 3}},
]