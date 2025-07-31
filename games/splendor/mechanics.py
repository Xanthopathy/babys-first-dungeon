import random
from games.splendor.constants import TOKENS, GEM_MAP, RESOURCES, DEVELOPMENT_CARDS, NOBLE_TILES

def setup_game(players):
    game_state = {
        'tokens': {key: val['count'] for key, val in TOKENS.items()},
        'nobles': [],
        'cards': {
            'level_1': {'deck': [], 'revealed': []},
            'level_2': {'deck': [], 'revealed': []},
            'level_3': {'deck': [], 'revealed': []},
        },
        'players': {f'player_{i+1}': {'tokens': {}, 'cards': [], 'nobles': [], 'prestige': 0, 'user_id': None, 'reserved': []} for i in range(players)},
        'game_active': True,
        'channel_id': None,
        'turn_count': 1,
        'turn_order': [],
        'current_turn': None,
        'end_triggered': False,  # Track if game end is triggered
        'final_round': False,  # Track if in final round
    }

    # Adjust noble tiles based on player count
    noble_count = players + 1 if players >= 4 else 4 if players == 3 else 3
    shuffled_nobles = random.sample(NOBLE_TILES, noble_count)
    game_state['nobles'] = shuffled_nobles

    # Adjust token counts based on player count
    if players == 3:
        for gem in ['ruby', 'emerald', 'sapphire', 'diamond', 'onyx']:
            game_state['tokens'][gem] = 5
    elif players == 2:
        for gem in ['ruby', 'emerald', 'sapphire', 'diamond', 'onyx']:
            game_state['tokens'][gem] = 4

    for level in ['level_1', 'level_2', 'level_3']:
        shuffled_deck = random.sample(DEVELOPMENT_CARDS[level], len(DEVELOPMENT_CARDS[level]))
        game_state['cards'][level]['deck'] = shuffled_deck[4:]
        game_state['cards'][level]['revealed'] = shuffled_deck[:4]

    return game_state

def take_three_different(state, player_id, gems):
    mapped_gems = []
    for gem in gems:
        if not gem:
            continue
        mapped = GEM_MAP.get(gem.lower())
        if not mapped or mapped not in TOKENS or mapped == 'gold':
            return False, f"Invalid gem: '{gem}'. Must choose 1-3 different valid gems (gold not allowed)."
        mapped_gems.append(mapped)

    # Check for duplicates
    if len(mapped_gems) > 3 or len(set(mapped_gems)) != len(mapped_gems):
        return False, "Must choose 1-3 different valid gems (no duplicates, gold not allowed)."

    available_gems = [gem for gem in TOKENS if gem != 'gold' and state['tokens'].get(gem, 0) >= 1]
    if not mapped_gems:
        return False, f"Must specify at least one gem. Available: {', '.join(available_gems)}."

    for gem in mapped_gems:
        if state['tokens'].get(gem, 0) < 1:
            return False, f"Not enough {gem} tokens."

    for gem in mapped_gems:
        state['tokens'][gem] -= 1
        state['players'][player_id]['tokens'][gem] = state['players'][player_id]['tokens'].get(gem, 0) + 1
    
    # Construct success message with turn number, username, and emojis in 🔴🟢🔵⚪🟣 order
    username = state['joined_players'].get(state['current_turn'], {}).get('username', 'Unknown')
    gem_order = ['ruby', 'emerald', 'sapphire', 'diamond', 'onyx']
    sorted_gems = sorted(mapped_gems, key=lambda x: gem_order.index(x))
    emojis = ''.join(TOKENS[gem]['emoji'] for gem in sorted_gems)
    return True, f"Turn {state['turn_count']}: {username} took {emojis}"

def take_two_same(state, player_id, gem):
    mapped_gem = GEM_MAP.get(gem.lower(), '')
    if mapped_gem not in TOKENS or mapped_gem == 'gold':
        return False, "Invalid gem or gold cannot be taken."
    if state['tokens'].get(mapped_gem, 0) < 4:
        return False, f"Not enough {mapped_gem} tokens (need at least 4)."
    state['tokens'][mapped_gem] -= 2
    state['players'][player_id]['tokens'][mapped_gem] = state['players'][player_id]['tokens'].get(mapped_gem, 0) + 2
    # Construct success message with turn number, username, and emoji
    username = state['joined_players'].get(state['current_turn'], {}).get('username', 'Unknown')
    emoji = TOKENS[mapped_gem]['emoji'] * 2
    return True, f"Turn {state['turn_count']}: {username} took {emoji}"

def reserve_card(state, player_id, level, card_index):
    level_map = {'1': 'level_1', '2': 'level_2', '3': 'level_3'}
    mapped_level = level_map.get(str(level), level)
    if mapped_level not in ['level_1', 'level_2', 'level_3'] or card_index < 1 or card_index > len(state['cards'][mapped_level]['revealed']):
        return False, "Invalid card selection."
    if len(state['players'][player_id].get('reserved', [])) >= 3:
        return False, "You cannot reserve more than 3 cards."
    if state['tokens'].get('gold', 0) < 1:
        return False, "No gold tokens available."
    card = state['cards'][mapped_level]['revealed'].pop(card_index - 1)
    state['players'][player_id]['reserved'] = state['players'][player_id].get('reserved', []) + [card]
    state['tokens']['gold'] -= 1
    state['players'][player_id]['tokens']['gold'] = state['players'][player_id]['tokens'].get('gold', 0) + 1
    # Replenish revealed card
    if state['cards'][mapped_level]['deck']:
        state['cards'][mapped_level]['revealed'].append(state['cards'][mapped_level]['deck'].pop(0))

    username = state['joined_players'].get(state['current_turn'], {}).get('username', 'Unknown')
    gold_emoji = TOKENS['gold']['emoji']
    return True, f"Turn {state['turn_count']}: {username} reserved a level {mapped_level[-1]} card and took {gold_emoji}"

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
    
    username = state['joined_players'].get(state['current_turn'], {}).get('username', 'Unknown')
    resource_emoji = RESOURCES.get(card['resource'], {}).get('emoji', '❓')
    source_text = "reserved" if source == 'reserved' else f"level {mapped_level[-1]}"
    return True, f"Turn {state['turn_count']}: {username} purchased a {source_text} card ({resource_emoji})"

def determine_winner(state):
    max_prestige = 0
    winners = []
    for player_id, player_data in state['players'].items():
        prestige = player_data['prestige']
        if prestige > max_prestige:
            max_prestige = prestige
            winners = [(player_id, len(player_data['cards']))]
        elif prestige == max_prestige:
            winners.append((player_id, len(player_data['cards'])))

    min_cards = min(card_count for _, card_count in winners) if winners else 0
    final_winners = [pid for pid, card_count in winners if card_count == min_cards]
    
    winner_names = [
        state['joined_players'].get(state['players'][pid]['user_id'], {}).get('username', 'Unknown')
        for pid in final_winners
    ]
    if len(winner_names) > 1:
        return f"Game ended! Tied winners: {', '.join(winner_names)} with {max_prestige} prestige and {min_cards} cards each."
    return f"Game ended! Winner: {winner_names[0]} with {max_prestige} prestige and {min_cards} cards."

def next_turn(state):
    current_index = state['turn_order'].index(state['current_turn'])
    next_index = (current_index + 1) % len(state['turn_order'])
    state['current_turn'] = state['turn_order'][next_index]
    state['turn_count'] += 1

    # Check for end game condition
    player_id = f'player_{state['turn_order'].index(state['current_turn']) + 1}'
    if state['players'][player_id]['prestige'] >= 15 and not state['end_triggered']:
        state['end_triggered'] = True
        state['final_round'] = True

    # Check if final round is complete
    if state['final_round'] and next_index == 0:
        state['game_active'] = False
        return determine_winner(state)
    return None