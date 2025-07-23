import discord
from discord.ext import commands
from config import BOT_TOKEN
from games.dungeon_crawler.manager import handle_start as handle_start_dungeon, handle_move as handle_move_dungeon, game_state as game_state_dungeon
from games.splendor.manager import handle_start as handle_start_splendor, game_state as game_state_splendor

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

# Remove default help command
bot.remove_command('help')

# Commands
@bot.command(aliases=['help'])
async def gamehelp(ctx):
    help_text = (
        "**Available Commands:**\n"
        "`$help or $gamehelp` - Show this help message.\n"
        "`$dungeon [boards] [fog|fogless]` - Start a new dungeon crawler game (default 1 board and fogless).\n"
        "`$move <up/down/left/right> [steps]` or `$m <u/d/l/r> [steps]` or `$<u/d/l/r> [steps]` - Move the player 1 of 4 directions. Step count is 1 by default. (ex: `$move right`, `$move right 3`, `$m r`, `$m r 3`, `$r`, `$r 3`).\n"
    )
    await ctx.send(help_text)

@bot.command(aliases=['m', 'u', 'd', 'l', 'r', 'up', 'down', 'left', 'right'])
async def move(ctx, direction: str = None, steps: int = 1):
    # Only run if a dungeon game is active in this channel
    channel_id = ctx.channel.id
    active = any(
        state.get('channel_id') == channel_id and state.get('game_active')
        for state in game_state_dungeon.values()
    )
    if not active:
        await ctx.send("No active dungeon game in this channel. Start one with $dungeon.")
        return
    await handle_move_dungeon(ctx, direction, steps)

@bot.command()
async def dungeon(ctx, *modifiers): # boards: int = 1, fog: str = 'fogless'
    # Prevent multiple games in the same channel
    channel_id = ctx.channel.id    
    active = any(
        state.get('channel_id') == channel_id and state.get('game_active')
        for state in game_state_dungeon.values()
    )
    if active:
        await ctx.send("A game is already running in this channel. End it with $end before starting a new one.")
        return

    # Parse boards modifier if present
    total_boards = 1
    fog_mode = 'fogless'
    if modifiers:
        for mod in modifiers:
            if mod.isdigit():
                total_boards = int(mod)
            elif mod.lower() in ['fog', 'fogless']:
                fog_mode = mod.lower()
    await handle_start_dungeon(ctx, total_boards, fog_mode)

@bot.command()
async def splendor(ctx, players: int = 2):
    # Prevent multiple games in the same channel
    channel_id = ctx.channel.id
    active = any(
        state.get('channel_id') == channel_id and state.get('game_active')
        for state in (list(game_state_dungeon.values()) + list(game_state_splendor.values()))
    )
    if active:
        await ctx.send("A game is already running in this channel. End it with $end before starting a new one.")
        return

    if players < 2 or players > 4:
        await ctx.send("Splendor requires 2-4 players.")
        return

    await handle_start_splendor(ctx, players)

# TODO: $p1 $p2 $p3 $p4 for players to join after $splendor is called

@bot.command()
async def end(ctx):
    channel_id = ctx.channel.id
    ended = False
    
    # End dungeon
    for user_id, state in list(game_state_dungeon.items()):
        if state.get('channel_id') == channel_id and state.get('game_active'):
            state['game_active'] = False    
            del game_state_dungeon[user_id]
            ended = True

    # End splendor
    for user_id, state in list(game_state_splendor.items()):
        if state.get('channel_id') == channel_id and state.get('game_active'):
            state['game_active'] = False    
            del game_state_splendor[user_id]
            ended = True

    if ended:
        await ctx.send("Game ended in this channel.")
    else:
        await ctx.send("No active game to end in this channel.")

# Bot event
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Run the bot
bot.run(BOT_TOKEN)