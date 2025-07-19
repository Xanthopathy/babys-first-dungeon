from constants import BACKGROUND_EMOJIS, XP_LEVELS

def board_to_string(board, player_pos, player_stats, move_count, current_board, total_boards):
    display = f"Board {current_board}/{total_boards} | Move #{move_count} | Enemies Left: {sum(row.count('enemy1') + row.count('enemy2') + row.count('enemy3') for row in board)}\n"
    for y in range(len(board)):
        for x in range(len(board[0])):
            if (x, y) == player_pos:
                display += BACKGROUND_EMOJIS['player']
            else:
                display += BACKGROUND_EMOJIS[board[y][x]]
        display += "\n"
    inventory_display = [BACKGROUND_EMOJIS[item] if item else BACKGROUND_EMOJIS['empty_slot'] for item in player_stats['inventory']]
    next_xp = XP_LEVELS.get(player_stats['level'] + 1, float('inf'))
    display += f"\nHP: {player_stats['current_hp']}/{player_stats['max_hp']} | Level: {player_stats['level']} | XP: {player_stats['xp']}/{next_xp} | Inventory: {' '.join(inventory_display)}"
    return display