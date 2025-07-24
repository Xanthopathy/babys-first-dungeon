import random
from games.splendor.constants import TOKENS, RESOURCES, DEVELOPMENT_CARDS, NOBLE_TILES

def setup_game(players):
    game_state = {
        'tokens': {key: val['count'] for key, val in TOKENS.items()},
        'nobles': [],
        'cards': {
            'level_1': {'deck': [], 'revealed': []},
            'level_2': {'deck': [], 'revealed': []},
            'level_3': {'deck': [], 'revealed': []},
        },
        'players': {f'player_{i+1}': {'tokens': {}, 'cards': [], 'nobles': [], 'prestige': 0, 'user_id': None} for i in range(players)},
        'game_active': True,
        'channel_id': None,
        'turn_count': 1,
        'turn_order': [],
        'current_turn': None,
    }

    noble_count = players + 1
    shuffled_nobles = random.sample(NOBLE_TILES, noble_count)
    game_state['nobles'] = shuffled_nobles

    for level in ['level_1', 'level_2', 'level_3']:
        shuffled_deck = random.sample(DEVELOPMENT_CARDS[level], len(DEVELOPMENT_CARDS[level]))
        game_state['cards'][level]['deck'] = shuffled_deck[4:]
        game_state['cards'][level]['revealed'] = shuffled_deck[:4]

    return game_state

def take_three_different(state, player_id, gems):
    gem_map = {
        'r': 'ruby', 'red': 'ruby', '🔴': 'ruby',
        'e': 'emerald', 'green': 'emerald', 'g': 'emerald', '🟢': 'emerald',
        's': 'sapphire', 'blue': 'sapphire', 'u': 'sapphire', '🔵': 'sapphire',
        'd': 'diamond', 'white': 'diamond', 'w': 'diamond', '⚪': 'diamond',
        'o': 'onyx', 'black': 'onyx', 'k': 'onyx', '⚫': 'onyx',
        'ruby': 'ruby', 'emerald': 'emerald', 'sapphire': 'sapphire', 'diamond': 'diamond', 'onyx': 'onyx'
    }
    mapped_gems = [gem_map.get(gem.lower(), '') for gem in gems]
    if len(mapped_gems) != 3 or len(set(mapped_gems)) != 3 or any(g not in TOKENS for g in mapped_gems):
        return False, "Must choose 3 different valid gems."
    for gem in mapped_gems:
        if state['tokens'].get(gem, 0) < 1:
            return False, f"Not enough {gem} tokens."
    for gem in mapped_gems:
        state['tokens'][gem] -= 1
        state['players'][player_id]['tokens'][gem] = state['players'][player_id]['tokens'].get(gem, 0) + 1
    return True, "Took 3 different tokens."

def take_two_same(state, player_id, gem):
    gem_map = {
        'r': 'ruby', 'red': 'ruby', '🔴': 'ruby',
        'e': 'emerald', 'green': 'emerald', 'g': 'emerald', '🟢': 'emerald',
        's': 'sapphire', 'blue': 'sapphire', 'b': 'sapphire', '🔵': 'sapphire',
        'd': 'diamond', 'white': 'diamond', 'w': 'diamond', '⚪': 'diamond',
        'o': 'onyx', 'black': 'onyx', '⚫': 'onyx',
        'ruby': 'ruby', 'emerald': 'emerald', 'sapphire': 'sapphire', 'diamond': 'diamond', 'onyx': 'onyx'
    }
    mapped_gem = gem_map.get(gem.lower(), '')
    if mapped_gem not in TOKENS or mapped_gem == 'gold':
        return False, "Invalid gem or gold cannot be taken."
    if state['tokens'].get(mapped_gem, 0) < 4:
        return False, f"Not enough {mapped_gem} tokens (need at least 4)."
    state['tokens'][mapped_gem] -= 2
    state['players'][player_id]['tokens'][mapped_gem] = state['players'][player_id]['tokens'].get(mapped_gem, 0) + 2
    return True, f"Took 2 {mapped_gem} tokens."

def reserve_card(state, player_id, level, card_index):
    level_map = {'1': 'level_1', '2': 'level_2', '3': 'level_3'}
    mapped_level = level_map.get(str(level), level)
    if mapped_level not in ['level_1', 'level_2', 'level_3'] or card_index < 1 or card_index > len(state['cards'][mapped_level]['revealed']):
        return False, "Invalid card selection."
    if state['tokens'].get('gold', 0) < 1:
        return False, "No gold tokens available."
    card = state['cards'][mapped_level]['revealed'].pop(card_index - 1)
    state['players'][player_id]['reserved'] = state['players'][player_id].get('reserved', []) + [card]
    state['tokens']['gold'] -= 1
    state['players'][player_id]['tokens']['gold'] = state['players'][player_id]['tokens'].get('gold', 0) + 1
    # Replenish revealed card
    if state['cards'][mapped_level]['deck']:
        state['cards'][mapped_level]['revealed'].append(state['cards'][mapped_level]['deck'].pop(0))
    return True, "Card reserved and gold token taken."

def purchase_card(state, player_id, source, level, card_index):
    level_map = {'1': 'level_1', '2': 'level_2', '3': 'level_3'}
    mapped_level = level_map.get(str(level), level) if source == 'revealed' else 'reserved'
    if source not in ['revealed', 'reserved'] or (source == 'revealed' and (mapped_level not in ['level_1', 'level_2', 'level_3'] or card_index < 1 or card_index > len(state['cards'][mapped_level]['revealed']))) or (source == 'reserved' and (card_index < 1 or card_index > len(state['players'][player_id].get('reserved', [])))):
        return False, "Invalid card selection."
    
    card = state['players'][player_id]['reserved'][card_index - 1] if source == 'reserved' else state['cards'][mapped_level]['revealed'][card_index - 1]
    
    # Check if player can afford the card
    resources = {res: sum(1 for c in state['players'][player_id]['cards'] if c['resource'] == res) for res in RESOURCES}
    tokens = state['players'][player_id].get('tokens', {})
    gold_tokens = tokens.get('gold', 0)
    for res, cost in card['cost'].items():
        available = resources.get(res, 0) + tokens.get(res, 0)
        if available < cost:
            needed = cost - available
            if gold_tokens < needed:
                return False, f"Not enough resources or gold to purchase card."
            gold_tokens -= needed
    
    # Pay for the card, using gold last
    for res, cost in card['cost'].items():
        needed = cost - resources.get(res, 0)
        if needed > 0:
            if tokens.get(res, 0) >= needed:
                state['players'][player_id]['tokens'][res] -= needed
                state['tokens'][res] += needed
            else:
                tokens_needed = min(needed, tokens.get(res, 0))
                gold_needed = needed - tokens_needed
                state['players'][player_id]['tokens'][res] = state['players'][player_id]['tokens'].get(res, 0) - tokens_needed
                state['players'][player_id]['tokens']['gold'] -= gold_needed
                state['tokens'][res] += tokens_needed
                state['tokens']['gold'] += gold_needed
    
    # Add card to player's collection
    if source == 'reserved':
        state['players'][player_id]['reserved'].pop(card_index - 1)
    else:
        state['cards'][mapped_level]['revealed'].pop(card_index - 1)
        if state['cards'][mapped_level]['deck']:
            state['cards'][mapped_level]['revealed'].append(state['cards'][mapped_level]['deck'].pop(0))
    
    state['players'][player_id]['cards'].append(card)
    state['players'][player_id]['prestige'] += card['prestige']
    
    # Check for noble visits
    player_resources = {res: sum(1 for c in state['players'][player_id]['cards'] if c['resource'] == res) for res in RESOURCES}
    for noble in state['nobles'][:]:
        if all(player_resources.get(res, 0) >= count for res, count in noble['bonuses'].items()):
            state['players'][player_id]['nobles'].append(noble)
            state['nobles'].remove(noble)
            state['players'][player_id]['prestige'] += noble['prestige']
    
    return True, "Card purchased."

def next_turn(state):
    current_index = state['turn_order'].index(state['current_turn'])
    next_index = (current_index + 1) % len(state['turn_order'])
    state['current_turn'] = state['turn_order'][next_index]
    state['turn_count'] += 1