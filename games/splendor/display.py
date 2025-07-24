from games.splendor.constants import TOKENS, RESOURCES

def display_board(game_state):
    board = f"**Splendor Game Board | Turn {game_state['turn_count']}**\n\n"
    
    # Display noble tiles
    board += "**__Noble Tiles__**\n"
    for noble in game_state['nobles']:
        bonuses = ", ".join([f"{v}x {RESOURCES[k]['emoji']}" for k, v in noble['bonuses'].items() if v > 0])
        board += f"Prestige: {noble['prestige']} | Bonuses: {bonuses}\n"
    #board += "\n"

    # Display development cards
    for level in ['level_3', 'level_2', 'level_1']:
        board += f"**__Level {level[-1]} Cards__ ({len(game_state['cards'][level]['deck'])} cards remaining)**\n"
        for i, card in enumerate(game_state['cards'][level]['revealed']):
            cost = ", ".join([f"{v}x {TOKENS[k]['emoji']}" for k, v in card['cost'].items() if v > 0])
            resource_emoji = RESOURCES.get(card['resource'], {}).get('emoji', '❓')
            board += f"[{i+1}] Resource: {resource_emoji} | Prestige: {card['prestige']} | Cost: {cost}\n"
        #board += "\n"

    # Display tokens
    board += "**__Available Tokens__**\n"
    token_display = " | ".join([f"{game_state['tokens'][resource]}x {data['emoji']}" for resource, data in TOKENS.items()])
    board += f"{token_display}\n"

    # Display current player
    board += "**__Players__**"
    user_to_player = {data['user_id']: key for key, data in game_state['players'].items()}
    joined_players = game_state.get('joined_players', {})
    current_player_id = game_state.get('current_turn')
    #current_player_name = joined_players.get(current_player_id, {}).get('username', 'Unknown')
    board += f"| Current Player: **<@{current_player_id}>**\n" # PINGU

    # Display players in turn order
    for user_id in game_state['turn_order']:
        player_key = user_to_player.get(user_id)
        if not player_key:
            continue
        player_data = game_state['players'][player_key]
        username = joined_players.get(user_id, {}).get('username', 'Unknown')
        if user_id == current_player_id:
            username = f"**{username}**" # Highlight current player
        prestige = player_data['prestige']
        nobles = player_data.get('nobles', [])
        nobles_display = ", ".join([f"{', '.join([f'{v}x {RESOURCES[k]['emoji']}' for k, v in noble['bonuses'].items() if v > 0])}" for noble in nobles]) or "None"
        resources = {'ruby': 0, 'emerald': 0, 'sapphire': 0, 'diamond': 0, 'onyx': 0}
        for card in player_data['cards']:
            resources[card['resource']] += 1
        resources_display = ", ".join([f"{v}x {RESOURCES[k]['emoji']}" for k, v in resources.items() if v > 0]) or "None"
        tokens = player_data.get('tokens', {})
        tokens_display = ", ".join([f"{v}x {TOKENS[k]['emoji']}" for k, v in tokens.items() if v > 0]) or "None"
        reserved = player_data.get('reserved', [])
        reserved_display = "\n".join([
            f"[{i+1}] Resource: {RESOURCES.get(card['resource'], {}).get('emoji', '❓')} | Prestige: {card['prestige']} | Cost: {', '.join([f'{v}x {TOKENS[k]['emoji']}' for k, v in card['cost'].items() if v > 0])}"
            for i, card in enumerate(reserved)
        ]) or "None"

        board += f"{username} | Prestige: {prestige} | Nobles: {nobles_display}\n"
        board += f"Resources: {resources_display}\n"
        board += f"Tokens: {tokens_display}\n"
        board += f"Reserved:\n{reserved_display}\n"

    return board