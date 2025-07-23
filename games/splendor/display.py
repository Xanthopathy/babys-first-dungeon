from games.splendor.constants import TOKENS

def display_board(game_state):
    board = "**Splendor Game Board**\n\n"
    
    # Display noble tiles
    board += "**Noble Tiles**\n"
    for noble in game_state['nobles']:
        bonuses = ", ".join([f"{k}: {v}" for k, v in noble['bonuses'].items()])
        board += f"Prestige: {noble['prestige']} | Bonuses: {bonuses}\n"
    board += "\n"

    # Display development cards
    for level in ['level_3', 'level_2', 'level_1']:  # Display in descending order
        board += f"**Level {level[-1]} Cards**\n"
        for card in game_state['cards'][level]['revealed']:
            cost = ", ".join([f"{k}: {v}" for k, v in card['cost'].items()])
            board += f"Resource: {card['resource']} | Prestige: {card['prestige']} | Cost: {cost}\n"
        board += f"Deck: {len(game_state['cards'][level]['deck'])} cards remaining\n\n"

    # Display tokens
    board += "**Tokens**\n"
    for resource, data in TOKENS.items():
        board += f"{data['emoji']} {resource.capitalize()}: {game_state['tokens'][resource]}\n"

    return board