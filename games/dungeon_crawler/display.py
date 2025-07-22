from games.dungeon_crawler.constants import BACKGROUND_EMOJIS, XP_LEVELS

def board_to_string(board, player_pos, player_stats, move_count, current_board, total_boards, fog_mode, revealed_tiles=None):
    # Board | Move | Enemies Left
    display = f"Board {current_board}/{total_boards} | Move #{move_count} | Enemies Left: {sum(row.count('enemy1') + row.count('enemy2') + row.count('enemy3') for row in board)}\n\n"

    # 10x10 board
    for y in range(len(board)):
        for x in range(len(board[0])):
            if (x, y) == player_pos:
                display += BACKGROUND_EMOJIS['player']
            elif fog_mode == 'fog' and (x, y) not in revealed_tiles and (x, y) not in [
                (player_pos[0], player_pos[1] - 1),  # Up
                (player_pos[0], player_pos[1] + 1),  # Down
                (player_pos[0] - 1, player_pos[1]),  # Left
                (player_pos[0] + 1, player_pos[1])   # Right
            ]:
                display += '❔'
            else:
                display += BACKGROUND_EMOJIS[board[y][x]]
        display += "\n"

    # Stats
    gear_display = [BACKGROUND_EMOJIS[item] if item else BACKGROUND_EMOJIS['empty_slot'] for item in player_stats['gear']]
    skills_display = [item if item else BACKGROUND_EMOJIS['empty_slot'] for item in player_stats['skills']]
    items_display = [item if item else BACKGROUND_EMOJIS['empty_slot'] for item in player_stats['items']]
    next_xp = XP_LEVELS.get(player_stats['level'] + 1, float('inf'))
    display += (
        f"\n❤️HP: {player_stats['current_hp']}/{player_stats['max_hp']} | "
        f"⬆️Level: {player_stats['level']} | ⭐XP: {player_stats['xp']}/{next_xp} | "
        f"🪙Gold: {player_stats['gold']}\n"
        f"⚔️Attack: {player_stats['attack']} | 🛡️Defense: {player_stats['defense']} | 🔮Magic: {player_stats['magic']}\n"
        f"Gear: {' '.join(gear_display)}\n" 
        f"Skills: {' '.join(skills_display)}\n"
        f"Items: {' '.join(items_display)}"
    )

    return display