from games.splendor.constants import TOKENS, RESOURCES

def display_board(game_state):
    board = f"**Splendor Game Board | Turn {game_state['turn_count']}**\n\n"
    
    # Display noble tiles
    board += "**Noble Tiles**\n"
    for noble in game_state['nobles']:
        bonuses = ", ".join([f"{v}x {RESOURCES[k]['emoji']}" for k, v in noble['bonuses'].items() if v > 0])
        board += f"Prestige: {noble['prestige']} | Bonuses: {bonuses}\n"
    board += "\n"

    # Display development cards
    for level in ['level_3', 'level_2', 'level_1']:
        board += f"**Level {level[-1]} Cards ({len(game_state['cards'][level]['deck'])} cards remaining)**\n"
        for i, card in enumerate(game_state['cards'][level]['revealed']):
            cost = ", ".join([f"{v}x {TOKENS[k]['emoji']}" for k, v in card['cost'].items() if v > 0])
            resource_emoji = RESOURCES.get(card['resource'], {}).get('emoji', '❓')
            board += f"[{i+1}] Resource: {resource_emoji} | Prestige: {card['prestige']} | Cost: {cost}\n"
        board += "\n"

    # Display tokens
    board += "**Available Tokens**\n"
    token_display = " | ".join([f"{game_state['tokens'][resource]}x {data['emoji']}" for resource, data in TOKENS.items()])
    board += f"{token_display}\n\n"

    # Display current player
    board += "**Players** "
    user_to_player = {data['user_id']: key for key, data in game_state['players'].items()}
    joined_players = game_state.get('joined_players', {})
    current_player_id = game_state.get('current_turn')
    current_player_name = joined_players.get(current_player_id, {}).get('username', 'Unknown')
    board += f"| Current Player: **{current_player_name}**\n"

    # Display players in turn order
    for user_id in game_state['turn_order']:
        player_key = user_to_player.get(user_id)
        if not player_key:
            continue
        player_data = game_state['players'][player_key]
        username = joined_players.get(user_id, {}).get('username', 'Unknown')
        prestige = player_data['prestige']
        nobles = player_data.get('nobles', [])
        nobles_display = ", ".join([
            ", ".join([f"{v}x {RESOURCES[k]['emoji']}" for k, v in noble['bonuses'].items() if v > 0])
            for noble in nobles
        ]) or "None"
        resources = {'ruby': 0, 'emerald': 0, 'sapphire': 0, 'diamond': 0, 'onyx': 0}
        for card in player_data['cards']:
            resources[card['resource']] += 1
        resources_display = ", ".join([f"{v}x {RESOURCES[k]['emoji']}" for k, v in resources.items() if v > 0]) or "None"
        tokens = player_data.get('tokens', {})
        tokens_display = ", ".join([f"{v}x {TOKENS[k]['emoji']}" for k, v in tokens.items() if v > 0]) or "None"
        reserved = player_data.get('reserved', [])
        reserved_display = ", ".join([
            f"{RESOURCES.get(card['resource'], {}).get('emoji', '❓')} (Prestige: {card['prestige']})"
            for card in reserved
        ]) or "None"
        board += f"{username} | Prestige: {prestige} | Nobles: {nobles_display} | Resources: {resources_display} | Tokens: {tokens_display} | Reserved: {reserved_display}\n"

    # Add command reminder
    board += "\n**Available Commands**:\n"
    board += (
        "`$take3/t3 <gem1> <gem2> <gem3>` - Take 3 different gem tokens (e.g., `$take3 ruby emerald sapphire`).\n"
        "`$take2/t2 <gem>` - Take 2 tokens of the same gem if 4+ are available (e.g., `$take2 ruby`).\n"
        "`$reserve/res <level> <index>` - Reserve a card and take a gold token (e.g., `$reserve 1 1`).\n"
        "`$purchase/buy revealed <level> <index>` - Purchase a face-up card (e.g., `$purchase revealed 1 1`).\n"
        "`$purchase/buy reserved <index>` - Purchase a reserved card (e.g., `$purchase reserved 1`).\n"
        "Gem shorthands: `ruby`, `r`, 🔴 | `emerald`, `e`, 🟢 | `sapphire`, `s`, 🔵 | `diamond`, `d`, ⚪ | `onyx`, `o`, ⚫\n"
    )

    return board