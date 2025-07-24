import random
from games.splendor.mechanics import setup_game, take_three_different, take_two_same, reserve_card, purchase_card, next_turn
from games.splendor.display import display_board

game_state = {}

async def handle_start(ctx):
    user_id = ctx.author.id
    channel_id = ctx.channel.id

    # Initialize pending game state
    game_state[user_id] = {
        'channel_id': channel_id,
        'game_pending': True,
        'game_active': False,
        'players_needed': 4,  # Max allowed
        'joined_players': {ctx.author.id: {'username': ctx.author.name}},
    }

async def handle_join(ctx, user_id):
    if user_id not in game_state or not game_state[user_id].get('game_pending'):
        await ctx.send("No pending Splendor game to join.")
        return

    state = game_state[user_id]
    if len(state['joined_players']) >= state['players_needed']:
        await ctx.send("The game is already full.")
        return

    if ctx.author.id in state['joined_players']:
        await ctx.send("You have already joined the game.")
        return

    state['joined_players'][ctx.author.id] = {'username': ctx.author.name}
    await ctx.send(f"{ctx.author.name} has joined the game. {len(state['joined_players'])}/{state['players_needed']} players joined.")

async def handle_start_game(ctx, user_id):
    if user_id not in game_state or not game_state[user_id].get('game_pending'):
        await ctx.send("No pending Splendor game to start.")
        return

    state = game_state[user_id]
    joined = len(state['joined_players'])
    if joined < 2 or joined > 4:
        await ctx.send(f"Cannot start: {joined} player(s) joined. Need 2-4 players.")
        return

    # Set up the actual game
    player_count = joined
    game_data = setup_game(player_count)
    game_data['channel_id'] = state['channel_id']
    game_data['game_pending'] = False
    game_data['game_active'] = True
    game_data['turn_count'] = 1
    game_data['turn_order'] = list(state['joined_players'].keys())
    game_data['joined_players'] = state['joined_players']
    game_data['last_board_message_id'] = None  # Initialize message ID tracking
    random.shuffle(game_data['turn_order'])
    game_data['current_turn'] = game_data['turn_order'][0]
    
    # Map joined players to game state
    game_data['players'] = {f'player_{i+1}': {
        'tokens': {}, 'cards': [], 'nobles': [], 'prestige': 0, 'user_id': user_id
    } for i, user_id in enumerate(state['joined_players'].keys())}
    
    game_state[user_id] = game_data
    board_display = display_board(game_state[user_id])
    await ctx.send(f"Splendor game started! Turn order: {', '.join([state['joined_players'][pid]['username'] for pid in game_data['turn_order']])}")
    message = await ctx.send(board_display)
    game_state[user_id]['last_board_message_id'] = message.id  # Store initial board message ID

async def handle_take_three(ctx, user_id, colors):
    state = game_state.get(user_id)
    if not state or not state.get('game_active'):
        await ctx.send("No active Splendor game in this channel.")
        return
    player_id = next((pid for pid, data in state['players'].items() if data['user_id'] == ctx.author.id), None)
    if not player_id or state['current_turn'] != ctx.author.id:
        await ctx.send("It's not your turn or you're not in this game.")
        return
    success, message = take_three_different(state, player_id, colors)
    await ctx.send(message)
    if success:
        next_turn(state)
        board_display = display_board(state)
        if state['turn_count'] % 10 == 0 or state['last_board_message_id'] is None:
            new_message = await ctx.send(board_display)
            state['last_board_message_id'] = new_message.id
        else:
            try:
                channel = ctx.channel
                old_message = await channel.fetch_message(state['last_board_message_id'])
                await old_message.edit(content=board_display)
            except:
                new_message = await ctx.send(board_display)
                state['last_board_message_id'] = new_message.id

async def handle_take_two(ctx, user_id, color):
    state = game_state.get(user_id)
    if not state or not state.get('game_active'):
        await ctx.send("No active Splendor game in this channel.")
        return
    player_id = next((pid for pid, data in state['players'].items() if data['user_id'] == ctx.author.id), None)
    if not player_id or state['current_turn'] != ctx.author.id:
        await ctx.send("It's not your turn or you're not in this game.")
        return
    success, message = take_two_same(state, player_id, color)
    await ctx.send(message)
    if success:
        next_turn(state)
        board_display = display_board(state)
        if state['turn_count'] % 10 == 0 or state['last_board_message_id'] is None:
            new_message = await ctx.send(board_display)
            state['last_board_message_id'] = new_message.id
        else:
            try:
                channel = ctx.channel
                old_message = await channel.fetch_message(state['last_board_message_id'])
                await old_message.edit(content=board_display)
            except:
                new_message = await ctx.send(board_display)
                state['last_board_message_id'] = new_message.id

async def handle_reserve(ctx, user_id, level, card_index):
    state = game_state.get(user_id)
    if not state or not state.get('game_active'):
        await ctx.send("No active Splendor game in this channel.")
        return
    player_id = next((pid for pid, data in state['players'].items() if data['user_id'] == ctx.author.id), None)
    if not player_id or state['current_turn'] != ctx.author.id:
        await ctx.send("It's not your turn or you're not in this game.")
        return
    success, message = reserve_card(state, player_id, level, card_index)
    await ctx.send(message)
    if success:
        next_turn(state)
        board_display = display_board(state)
        if state['turn_count'] % 10 == 0 or state['last_board_message_id'] is None:
            new_message = await ctx.send(board_display)
            state['last_board_message_id'] = new_message.id
        else:
            try:
                channel = ctx.channel
                old_message = await channel.fetch_message(state['last_board_message_id'])
                await old_message.edit(content=board_display)
            except:
                new_message = await ctx.send(board_display)
                state['last_board_message_id'] = new_message.id

async def handle_purchase(ctx, user_id, source, level, card_index):
    state = game_state.get(user_id)
    if not state or not state.get('game_active'):
        await ctx.send("No active Splendor game in this channel.")
        return
    player_id = next((pid for pid, data in state['players'].items() if data['user_id'] == ctx.author.id), None)
    if not player_id or state['current_turn'] != ctx.author.id:
        await ctx.send("It's not your turn or you're not in this game.")
        return
    success, message = purchase_card(state, player_id, source, level, card_index)
    await ctx.send(message)
    if success:
        next_turn(state)
        board_display = display_board(state)
        if state['turn_count'] % 10 == 0 or state['last_board_message_id'] is None:
            new_message = await ctx.send(board_display)
            state['last_board_message_id'] = new_message.id
        else:
            try:
                channel = ctx.channel
                old_message = await channel.fetch_message(state['last_board_message_id'])
                await old_message.edit(content=board_display)
            except:
                new_message = await ctx.send(board_display)
                state['last_board_message_id'] = new_message.id