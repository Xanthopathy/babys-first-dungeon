import discord
import random
from games.dungeon_crawler.mechanics import create_board, handle_move as mechanics_handle_move
from games.dungeon_crawler.display import board_to_string
from games.dungeon_crawler.constants import HP_PER_LEVEL, BOARD_SIZE

# Game state storage
game_state = {}

async def handle_start(ctx, total_boards, fog_mode):
    user_id = ctx.author.id
    channel_id = ctx.channel.id

    # Prevent multiple games in the same channel
    for state in game_state.values():
        if state.get('channel_id') == channel_id and state.get('game_active'):
            await ctx.send("A game is already running in this channel. End it with !end before starting a new one.")
            return
        
    # Prevent multiple games for the same user
    if user_id in game_state and game_state[user_id]['game_active']:
        await ctx.send("You already have an active game! Use !move, !m, !u, !d, !l, or !r to continue.")
        return
    
    # Initialize game state
    player_pos = random.choice([(4, 4), (4, 5), (5, 4), (5, 5)])
    revealed_tiles = set()
    if fog_mode == 'fog':
        x, y = player_pos
        adjacent_tiles = [
            (x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)
        ]
        for pos in adjacent_tiles:
            if 0 <= pos[0] < BOARD_SIZE and 0 <= pos[1] < BOARD_SIZE:
                revealed_tiles.add(pos)

    game_state[user_id] = {
        'board': create_board(total_boards, 1, player_pos),
        'player_pos': player_pos,
        'player_stats': {
            'current_hp': HP_PER_LEVEL[1], 
            'max_hp': HP_PER_LEVEL[1], 
            'level': 1, 
            'xp': 0, 
            'inventory': [None] * 4
        },
        'game_active': True,
        'move_count': 0,
        'message_id': None,
        'current_board': 1,
        'total_boards': max(1, total_boards),
        'fog_mode': fog_mode,
        'channel_id': channel_id,
        'revealed_tiles': revealed_tiles
    }
    msg = await ctx.send(
        board_to_string(
            game_state[user_id]['board'], 
            game_state[user_id]['player_pos'], 
            game_state[user_id]['player_stats'], 
            0, 
            1, 
            game_state[user_id]['total_boards'], 
            game_state[user_id]['fog_mode'],
            game_state[user_id]['revealed_tiles']
        )
    )
    game_state[user_id]['message_id'] = msg.id

async def handle_move(ctx, direction, steps):
    user_id = ctx.author.id

    # Handle single-letter alias with just a number (e.g., !d 3)
    invoked = ctx.invoked_with.lower()
    if invoked in ['u', 'd', 'l', 'r']:
        if direction is not None and direction.isdigit():
            steps = int(direction)
            direction = invoked
        else:
            direction = invoked

    if direction is None:
        await ctx.send("Specify a direction (u/d/l/r or up/down/left/right).")
        return
    
    if user_id not in game_state or not game_state[user_id]['game_active']:
        await ctx.send("No active game! Start one with !start.")
        return

    continue_game, message_id = await mechanics_handle_move(ctx, game_state, user_id, direction, steps)
    if not continue_game:
        return

    # Update revealed tiles in fog mode
    if game_state[user_id]['fog_mode'] == 'fog':
        x, y = game_state[user_id]['player_pos']
        adjacent_tiles = [
            (x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)
        ]
        for pos in adjacent_tiles:
            if 0 <= pos[0] < BOARD_SIZE and 0 <= pos[1] < BOARD_SIZE:
                game_state[user_id]['revealed_tiles'].add(pos)

    board = game_state[user_id]['board']
    player_pos = game_state[user_id]['player_pos']
    player_stats = game_state[user_id]['player_stats']
    move_count = game_state[user_id]['move_count']
    fog_mode = game_state[user_id]['fog_mode']
    revealed_tiles = game_state[user_id]['revealed_tiles']

    board_message = board_to_string(board, player_pos, player_stats, move_count, game_state[user_id]['current_board'], game_state[user_id]['total_boards'], fog_mode, revealed_tiles)
    if move_count % 5 == 0 or not message_id:
        msg = await ctx.send(board_message)
        game_state[user_id]['message_id'] = msg.id
    else:
        try:
            msg = await ctx.channel.fetch_message(message_id)
            await msg.edit(content=board_message)
        except discord.NotFound:
            msg = await ctx.send(board_message)
            game_state[user_id]['message_id'] = msg.id