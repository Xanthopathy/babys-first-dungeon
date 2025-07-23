import random
from games.splendor.constants import TOKENS, DEVELOPMENT_CARDS, NOBLE_TILES

def setup_game(players):
    # Initialize game state
    game_state = {
        'tokens': {key: val['count'] for key, val in TOKENS.items()},
        'nobles': [],
        'cards': {
            'level_1': {'deck': [], 'revealed': []},
            'level_2': {'deck': [], 'revealed': []},
            'level_3': {'deck': [], 'revealed': []},
        },
        'players': {f'player_{i+1}': {'tokens': {}, 'cards': [], 'nobles': [], 'prestige': 0} for i in range(players)},
        'game_active': True,
        'channel_id': None,
    }

    # Shuffle and setup noble tiles
    noble_count = players + 1
    shuffled_nobles = random.sample(NOBLE_TILES, noble_count)
    game_state['nobles'] = shuffled_nobles

    # Shuffle and setup development cards
    for level in ['level_1', 'level_2', 'level_3']:
        shuffled_deck = random.sample(DEVELOPMENT_CARDS[level], len(DEVELOPMENT_CARDS[level]))
        game_state['cards'][level]['deck'] = shuffled_deck[4:]  # Remaining cards after revealing 4
        game_state['cards'][level]['revealed'] = shuffled_deck[:4]  # Reveal 4 cards

    return game_state