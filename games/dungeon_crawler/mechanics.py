import random
from games.dungeon_crawler.constants import BOARD_SIZE, MAX_STEPS, ENEMY_XP, ENEMY_DAMAGE, ITEM_BONUSES, HP_PER_LEVEL, XP_LEVELS

def create_board(total_boards, current_board, player_pos):
    board = _init_board()
    event_positions = _place_event_tiles(board, player_pos, total_boards, current_board)
    _place_walls(board, player_pos, event_positions)
    return board

def _init_board():
    return [['floor' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def _get_reserved_positions(player_pos):
    return [player_pos] # Currently reserve only the player's spawn position, done like this in case more reserved positions are needed later

def _place_event_tiles(board, player_pos, total_boards, current_board):
    reserved = set(_get_reserved_positions(player_pos))
    floor_tiles = [(x, y) for y in range(BOARD_SIZE) for x in range(BOARD_SIZE) if (x, y) not in reserved]
    random.shuffle(floor_tiles)
    
    # Place items
    items = ['sword', 'shield']
    item_positions = []
    for item in items:
        if floor_tiles:
            x, y = floor_tiles.pop()
            board[y][x] = item
            item_positions.append((x, y))
    
    # Place enemies
    base_enemies = ['enemy1', 'enemy2', 'enemy3']
    enemy_types = base_enemies * 2
    enemy_positions = []
    for enemy in enemy_types:
        if floor_tiles:
            x, y = floor_tiles.pop()
            board[y][x] = enemy
            enemy_positions.append((x, y))
    
    # Place door or boss
    corner = random.choice([(0, 0), (0, BOARD_SIZE-1), (BOARD_SIZE-1, 0), (BOARD_SIZE-1, BOARD_SIZE-1)])
    board[corner[1]][corner[0]] = 'door' if current_board < total_boards else 'boss'
    
    return item_positions + enemy_positions + [corner]

def _place_walls(board, player_pos, event_positions):
    from collections import deque
    
    def is_path_available(start, targets, board):
        visited = set()
        queue = deque([start])
        while queue:
            x, y = queue.popleft()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] != 'wall' and (nx, ny) not in visited:
                    queue.append((nx, ny))
        return all(target in visited for target in targets)
    
    random_wall_percentage = random.uniform(0.2, 0.4) # 20% to 40% of the board can be walls
    num_walls = int(BOARD_SIZE * BOARD_SIZE * random_wall_percentage)
    reserved = set([player_pos] + event_positions)
    candidates = [(x, y) for y in range(BOARD_SIZE) for x in range(BOARD_SIZE) if (x, y) not in reserved]
    random.shuffle(candidates)
    
    walls_placed = 0
    for x, y in candidates:
        if walls_placed >= num_walls:
            break
        board[y][x] = 'wall'
        if not is_path_available(player_pos, event_positions, board):
            board[y][x] = 'floor'
            continue
        walls_placed += 1

def calculate_player_power(player_stats):
    power = player_stats['level'] * 5 + player_stats['attack'] + player_stats['defense'] + player_stats['magic']
    for gear in player_stats['gear']:
        if gear:
            bonuses = ITEM_BONUSES.get(gear, {})
            power += bonuses.get('attack', 0) + bonuses.get('defense', 0) + bonuses.get('magic', 0)
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
        player_stats['gold'] += enemy_level  # Gain gold equal to enemy level
        await ctx.send(f"{combat_info}You defeated the level {enemy_level} enemy and gained {xp_gain} XP and {enemy_level} gold!")
        return True, xp_gain
    else:
        damage = max(1, ENEMY_DAMAGE[enemy_type] - player_stats['def'] // 5)  # Defense reduces damage
        player_stats['current_hp'] -= damage
        await ctx.send(f"{combat_info}The level {enemy_level} enemy dealt {damage} damage! Your HP: {player_stats['current_hp']}/{player_stats['max_hp']}")
        return False, 0

async def handle_move(ctx, game_state, user_id, direction, steps):
    player_pos = game_state[user_id]['player_pos']
    board = game_state[user_id]['board']
    player_stats = game_state[user_id]['player_stats']
    turn_count = game_state[user_id]['move_count']
    message_id = game_state[user_id].get('message_id')
    fog_mode = game_state[user_id]['fog_mode']
    revealed_tiles = game_state[user_id]['revealed_tiles']

    direction_map = {'u': 'up', 'd': 'down', 'l': 'left', 'r': 'right'}
    direction = direction_map.get(direction.lower(), direction.lower())
    if direction not in ['up', 'down', 'left', 'right']:
        await ctx.send("Invalid direction! Use up, down, left, right or u, d, l, r.")
        return False, None

    x, y = player_pos
    event_tiles = ['wall', 'door', 'enemy1', 'enemy2', 'enemy3', 'sword', 'shield', 'boss']

    for _ in range(min(steps, MAX_STEPS)):
        turn_count += 1
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

        if board[y][x] == 'floor':
            board[y][x] = 'visited_floor'

        if fog_mode == 'fog':
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                    revealed_tiles.add((nx, ny))

        if board[new_pos[1]][new_pos[0]] in event_tiles:
            if board[new_pos[1]][new_pos[0]] in ['sword', 'shield']:
                await _pickup_item(ctx, player_stats, board, new_pos)
                x, y = new_pos
                game_state[user_id]['player_pos'] = (x, y)
            elif board[new_pos[1]][new_pos[0]] in ['enemy1', 'enemy2', 'enemy3', 'boss']:
                enemy_type = board[new_pos[1]][new_pos[0]]
                enemy_level = {'enemy1': 1, 'enemy2': 2, 'enemy3': 3, 'boss': 5}[enemy_type]
                win, _ = await handle_combat(ctx, player_stats, enemy_type, enemy_level)
                if win:
                    board[new_pos[1]][new_pos[0]] = 'visited_floor'
                    x, y = new_pos
                    game_state[user_id]['player_pos'] = (x, y)
                else:
                    if player_stats['current_hp'] <= 0:
                        await ctx.send("You died! Game over!")
                        game_state.pop(user_id)
                        return False, None
                    break
            elif board[new_pos[1]][new_pos[0]] == 'door':
                await _enter_door(ctx, game_state, user_id, turn_count)
                return True, message_id
            break

        await _check_level_up(ctx, player_stats)
        x, y = new_pos
        game_state[user_id]['player_pos'] = (x, y)

    game_state[user_id]['move_count'] = turn_count
    return True, message_id

async def _pickup_item(ctx, player_stats, board, pos):
    item = board[pos[1]][pos[0]]
    for i, slot in enumerate(player_stats['gear']):
        if slot is None:
            player_stats['gear'][i] = item
            bonuses = ITEM_BONUSES.get(item, {})
            if 'attack' in bonuses:
                player_stats['attack'] += bonuses['attack']
            if 'defense' in bonuses:
                player_stats['defense'] += bonuses['defense']
            await ctx.send(f"Picked up {item}! Stats updated.")
            board[pos[1]][pos[0]] = 'floor'
            return
    await ctx.send("Gear slots full! Cannot pick up gear.")

async def _enter_door(ctx, game_state, user_id, turn_count):
    game_state[user_id]['current_board'] += 1
    total_boards = game_state[user_id]['total_boards']
    player_pos = random.choice([(4, 4), (4, 5), (5, 4), (5, 5)])
    game_state[user_id]['board'] = create_board(total_boards, game_state[user_id]['current_board'], player_pos)
    game_state[user_id]['player_pos'] = player_pos
    await ctx.send(f"Entered door to board {game_state[user_id]['current_board']}/{total_boards}!")
    game_state[user_id]['move_count'] = turn_count

async def _check_level_up(ctx, player_stats):
    next_level = player_stats['level'] + 1
    if next_level in XP_LEVELS and player_stats['xp'] >= XP_LEVELS[next_level]:
        player_stats['level'] = next_level
        player_stats['max_hp'] = HP_PER_LEVEL[next_level]
        player_stats['current_hp'] = min(player_stats['current_hp'] + 5, player_stats['max_hp'])
        player_stats['atk'] += 1  # Increase attack on level up
        player_stats['def'] += 1  # Increase defense on level up
        player_stats['mag'] += 1  # Increase magic on level up
        await ctx.send(f"Level up! You are now Level {next_level}. Stats increased.")