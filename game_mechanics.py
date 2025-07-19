import random
from constants import BOARD_SIZE, MAX_STEPS, ENEMY_XP, ENEMY_DAMAGE, ITEM_BONUSES, HP_PER_LEVEL, XP_LEVELS

def create_board(total_boards, current_board):
    board = _init_board()
    _place_walls(board)
    _place_enemies(board, double_spawn=True)
    _place_items(board)
    _place_door_or_boss(board, total_boards, current_board)
    return board

def _init_board():
    return [['floor' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def _get_reserved_positions():
    # Reserved for player spawn
    return [(4, 4), (4, 5), (5, 4), (5, 5)]

def _place_walls(board):
    num_walls = int(BOARD_SIZE * BOARD_SIZE * 0.1) # 10% of the board
    reserved = set(_get_reserved_positions())
    candidates = [(x, y) for y in range(BOARD_SIZE) for x in range(BOARD_SIZE) if (x, y) not in reserved]
    wall_positions = random.sample(candidates, num_walls)
    for x, y in wall_positions:
        board[y][x] = 'wall'

def _place_enemies(board, double_spawn=False):
    reserved = set(_get_reserved_positions())
    floor_tiles = [(x, y) for y in range(BOARD_SIZE) for x in range(BOARD_SIZE)
                   if board[y][x] == 'floor' and (x, y) not in reserved]
    random.shuffle(floor_tiles)
    base_enemies = ['enemy1', 'enemy2', 'enemy3']
    enemy_types = base_enemies * (2 if double_spawn else 1)
    placements = []
    for enemy in enemy_types:
        if floor_tiles:
            pos = floor_tiles.pop()
            placements.append((enemy, pos))
    for enemy, (x, y) in placements:
        board[y][x] = enemy

def _place_items(board):
    reserved = set(_get_reserved_positions())
    floor_tiles = [(x, y) for y in range(BOARD_SIZE) for x in range(BOARD_SIZE)
                   if board[y][x] == 'floor' and (x, y) not in reserved]
    random.shuffle(floor_tiles)
    items = ['sword', 'shield']
    for item in items:
        if floor_tiles:
            x, y = floor_tiles.pop()
            board[y][x] = item

def _place_door_or_boss(board, total_boards, current_board):
    corner = random.choice([(0, 0), (0, BOARD_SIZE-1), (BOARD_SIZE-1, 0), (BOARD_SIZE-1, BOARD_SIZE-1)])
    if current_board < total_boards:
        board[corner[1]][corner[0]] = 'door'
    elif current_board == total_boards:
        board[corner[1]][corner[0]] = 'boss'

def calculate_player_power(player_stats):
    power = player_stats['level'] * 5
    for item in player_stats['inventory']:
        if item:
            power += ITEM_BONUSES.get(item, 0)
    return power

async def handle_combat(ctx, player_stats, enemy_type, enemy_level):
    enemy_power = enemy_level * 5
    player_power = calculate_player_power(player_stats)
    total_power = player_power + enemy_power
    win_chance = player_power / total_power
    combat_info = f"Combat: Player Power {player_power} vs Enemy (Level {enemy_level}) Power {enemy_power}\nWin Chance: {win_chance:.2%}\n"
    if random.random() < win_chance:
        xp_gain = ENEMY_XP[enemy_type]
        player_stats['xp'] += xp_gain
        await ctx.send(f"{combat_info}You defeated the level {enemy_level} enemy and gained {xp_gain} XP!")
        return True, xp_gain
    else:
        damage = ENEMY_DAMAGE[enemy_type]
        player_stats['current_hp'] -= damage
        await ctx.send(f"{combat_info}The level {enemy_level} enemy dealt {damage} damage! Your HP: {player_stats['current_hp']}/{player_stats['max_hp']}")
        return False, 0

async def handle_move(ctx, game_state, user_id, direction, steps):
    player_pos = game_state[user_id]['player_pos']
    board = game_state[user_id]['board']
    player_stats = game_state[user_id]['player_stats']
    move_count = game_state[user_id]['move_count'] + 1
    message_id = game_state[user_id].get('message_id')
    current_board = game_state[user_id]['current_board']
    total_boards = game_state[user_id]['total_boards']

    direction_map = {'u': 'up', 'd': 'down', 'l': 'left', 'r': 'right'}
    direction = direction_map.get(direction.lower(), direction.lower())
    if direction not in ['up', 'down', 'left', 'right']:
        await ctx.send("Invalid direction! Use up, down, left, right or u, d, l, r.")
        return False, None

    x, y = player_pos
    for _ in range(min(steps, MAX_STEPS)):
        if direction == 'up':
            new_pos = (x, y - 1)
        elif direction == 'down':
            new_pos = (x, y + 1)
        elif direction == 'left':
            new_pos = (x - 1, y)
        elif direction == 'right':
            new_pos = (x + 1, y)

        if not (0 <= new_pos[0] < BOARD_SIZE and 0 <= new_pos[1] < BOARD_SIZE):
            await ctx.send("Out of bounds!")
            break
        if board[new_pos[1]][new_pos[0]] == 'wall':
            await ctx.send("You hit a wall!")
            break

        if board[new_pos[1]][new_pos[0]] in ['sword', 'shield']:
            await _pickup_item(ctx, player_stats, board, new_pos)
            break

        if board[new_pos[1]][new_pos[0]] in ['enemy1', 'enemy2', 'enemy3']:
            enemy_type = board[new_pos[1]][new_pos[0]]
            enemy_level = {'enemy1': 1, 'enemy2': 2, 'enemy3': 3}[enemy_type]
            win, xp_gain = await handle_combat(ctx, player_stats, enemy_type, enemy_level)
            if win:
                board[new_pos[1]][new_pos[0]] = 'floor'
            else:
                if player_stats['current_hp'] <= 0:
                    await ctx.send("You died! Game over!")
                    game_state.pop(user_id)
                    return False, None
                break

        if board[new_pos[1]][new_pos[0]] == 'door':
            await _enter_door(ctx, game_state, user_id, move_count)
            return True, message_id

        if board[new_pos[1]][new_pos[0]] == 'boss':
            win, _ = await handle_combat(ctx, player_stats, 'boss', 5)
            if win:
                await ctx.send("You defeated the final boss! You win!")
                game_state.pop(user_id)
                return False, None
            else:
                if player_stats['current_hp'] <= 0:
                    await ctx.send("You died! Game over!")
                    game_state.pop(user_id)
                    return False, None
                break

        await _check_level_up(ctx, player_stats)

        x, y = new_pos
        game_state[user_id]['player_pos'] = (x, y)

    game_state[user_id]['move_count'] = move_count
    return True, message_id

async def _pickup_item(ctx, player_stats, board, pos):
    item = board[pos[1]][pos[0]]
    for i, slot in enumerate(player_stats['inventory']):
        if slot is None:
            player_stats['inventory'][i] = item
            await ctx.send(f"Picked up {item}!")
            board[pos[1]][pos[0]] = 'floor'
            return
    await ctx.send("Inventory full! Cannot pick up item.")

async def _enter_door(ctx, game_state, user_id, move_count):
    game_state[user_id]['current_board'] += 1
    total_boards = game_state[user_id]['total_boards']
    game_state[user_id]['board'] = create_board(total_boards, game_state[user_id]['current_board'])
    game_state[user_id]['player_pos'] = random.choice(_get_reserved_positions())
    await ctx.send(f"Entered door to board {game_state[user_id]['current_board']}/{total_boards}!")
    game_state[user_id]['move_count'] = move_count

async def _check_level_up(ctx, player_stats):
    next_level = player_stats['level'] + 1
    if next_level in XP_LEVELS and player_stats['xp'] >= XP_LEVELS[next_level]:
        player_stats['level'] = next_level
        player_stats['max_hp'] = HP_PER_LEVEL[next_level]
        player_stats['current_hp'] = min(player_stats['current_hp'] + 5, player_stats['max_hp'])
        await ctx.send(f"Level up! You are now Level {next_level}.")