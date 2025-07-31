from games.splendor.constants import TOKENS, RESOURCES

def display_board(game_state):
    board = f"**__Splendor Game Board__ | __Turn {game_state['turn_count']}__**\n"
    
    # Display noble tiles
    board += "**__Noble Tiles__**\n"
    for noble in game_state['nobles']:
        bonuses = ", ".join([f"{v}x {RESOURCES[k]['emoji']}" for k, v in noble['bonuses'].items() if v > 0])
        board += f"__Prestige__: {noble['prestige']} | __Bonuses__: {bonuses}\n"
    #board += "\n"

    # Display development cards
    for level in ['level_3', 'level_2', 'level_1']:
        board += f"**__Level {level[-1]} Cards__ ({len(game_state['cards'][level]['deck'])} cards remaining)**\n"
        for i, card in enumerate(game_state['cards'][level]['revealed']):
            cost = ", ".join([f"{v}x {TOKENS[k]['emoji']}" for k, v in card['cost'].items() if v > 0])
            resource_emoji = RESOURCES.get(card['resource'], {}).get('emoji', '❓')
            board += f"[{i+1}] __Resource__: {resource_emoji} | __Prestige__: {card['prestige']} | __Cost__: {cost}\n"
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
    board += f" | __Current Player__: **<@{current_player_id}>**\n" # PINGU

    # Display players in turn order
    for idx, user_id in enumerate(game_state['turn_order']):
        player_key = user_to_player.get(user_id)
        if not player_key:
            continue
        player_data = game_state['players'][player_key]
        username = joined_players.get(user_id, {}).get('username', 'Unknown')
        if user_id == current_player_id:
            username = f"**{username}**" # Highlight current player
        prestige = player_data['prestige']
        nobles = player_data.get('nobles', [])
        nobles_display = ", ".join([f"{', '.join([f'{v}x {RESOURCES[k]['emoji']}' for k, v in sorted(noble['bonuses'].items(), key=lambda x: ['ruby', 'emerald', 'sapphire', 'diamond', 'onyx'].index(x[0])) if v > 0])}" for noble in nobles]) or "None"
        resources = {'ruby': 0, 'emerald': 0, 'sapphire': 0, 'diamond': 0, 'onyx': 0}
        for card in player_data['cards']:
            resources[card['resource']] += 1
        resources_display = ", ".join([f"{v}x {RESOURCES[k]['emoji']}" for k, v in sorted(resources.items(), key=lambda x: ['ruby', 'emerald', 'sapphire', 'diamond', 'onyx'].index(x[0])) if v > 0]) or "None"
        tokens = player_data.get('tokens', {})
        tokens_display = ", ".join([f"{v}x {TOKENS[k]['emoji']}" for k, v in sorted(tokens.items(), key=lambda x: ['ruby', 'emerald', 'sapphire', 'diamond', 'onyx', 'gold'].index(x[0])) if v > 0]) or "None"
        reserved = player_data.get('reserved', [])
        if reserved:
            reserved_display = "\n".join([
                f"[{i+1}] __Resource__: {RESOURCES.get(card['resource'], {}).get('emoji', '❓')} | __Prestige__: {card['prestige']} | __Cost__: {', '.join([f'{v}x {TOKENS[k]['emoji']}' for k, v in sorted(card['cost'].items(), key=lambda x: ['ruby', 'emerald', 'sapphire', 'diamond', 'onyx', 'gold'].index(x[0])) if v > 0])}"
                for i, card in enumerate(reserved)
            ])
        else:
            reserved_display = "None"

        board += f"[{username}] | __Prestige__: {prestige} | __Nobles__: {nobles_display}\n"
        board += f"__Resources__: {resources_display}\n"
        board += f"__Tokens__: {tokens_display}\n"
        board += f"__Reserved__: {reserved_display}\n"
        # Only add separator if not the last player
        if idx != len(game_state['turn_order']) - 1:
            board += f"============================================================\n"
    return board