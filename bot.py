import discord
from discord.ext import commands
import random
from game_mechanics import create_board, handle_move
from display import board_to_string
from constants import HP_PER_LEVEL
from config import BOT_TOKEN

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Remove default help command
bot.remove_command('help')

# Game state storage
game_state = {}

# Commands
@bot.command(name='gamehelp')
async def gamehelp(ctx):
    help_text = (
        "**Available Commands:**\n"
        "`!start [boards]` - Start a new dungeon crawler game (default 1 board).\n"
        "`!move <direction> [steps]` or `!m <u/d/l/r> [steps]` - Move the player (up, down, left, right or u, d, l, r). Optional steps (e.g., `!m r 3`).\n"
        "`!u [steps]`, `!d [steps]`, `!l [steps]`, `!r [steps]` - Move up, down, left, or right (e.g., `!d 3`).\n"
        "`!gamehelp` - Show this help message."
    )
    await ctx.send(help_text)

@bot.command(aliases=['m', 'u', 'd', 'l', 'r'])
async def move(ctx, direction: str = None, steps: int = 1):
    user_id = ctx.author.id

    # Handle single-letter alias with just a number (e.g., !d 3)
    invoked = ctx.invoked_with.lower()
    if invoked in ['u', 'd', 'l', 'r']:
        # If direction is actually a number, swap
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

    continue_game, message_id = await handle_move(ctx, game_state, user_id, direction, steps)
    if not continue_game:
        return

    board = game_state[user_id]['board']
    player_pos = game_state[user_id]['player_pos']
    player_stats = game_state[user_id]['player_stats']
    move_count = game_state[user_id]['move_count']

    board_message = board_to_string(board, player_pos, player_stats, move_count, game_state[user_id]['current_board'], game_state[user_id]['total_boards'])
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

@bot.command()
async def start(ctx, total_boards: int = 1):
    user_id = ctx.author.id
    if user_id in game_state and game_state[user_id]['game_active']:
        await ctx.send("You already have an active game! Use !move, !m, !u, !d, !l, or !r to continue.")
        return
    game_state[user_id] = {
        'board': create_board(total_boards, 1),
        'player_pos': random.choice([(4, 4), (4, 5), (5, 4), (5, 5)]),
        'player_stats': {'current_hp': HP_PER_LEVEL[1], 'max_hp': HP_PER_LEVEL[1], 'level': 1, 'xp': 0, 'inventory': [None] * 4},
        'game_active': True,
        'move_count': 0,
        'message_id': None,
        'current_board': 1,
        'total_boards': max(1, total_boards)
    }
    msg = await ctx.send(board_to_string(game_state[user_id]['board'], game_state[user_id]['player_pos'], game_state[user_id]['player_stats'], 0, 1, game_state[user_id]['total_boards']))
    game_state[user_id]['message_id'] = msg.id

# Bot event
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Run the bot
bot.run(BOT_TOKEN)