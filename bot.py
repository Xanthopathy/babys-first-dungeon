import discord
from discord.ext import commands
from config import BOT_TOKEN
from games.dungeon_crawler.manager import handle_start as handle_start_dungeon, handle_move as handle_move_dungeon, game_state as game_state_dungeon

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Remove default help command
bot.remove_command('help')

# Commands
@bot.command(aliases=['help'])
async def gamehelp(ctx):
    help_text = (
        "**Available Commands:**\n"
        "`!help or !gamehelp` - Show this help message.\n"
        "`!start [game]` - Start a new game.\n"
        "`!start dungeon [boards] [fog|fogless]` - Start a new dungeon crawler game (default 1 board and fogless).\n"
        "`!move <direction> [steps]` or `!m <u/d/l/r> [steps]` or `!<u/d/l/r> [steps]` - Move the player (up, down, left, right or u, d, l, r). Step count is 1 by default. (ex: `!move right`, `!move right 3`, `!m r`, `!m r 3`, `!r`, `!r 3`).\n"
    )
    await ctx.send(help_text)

@bot.command(aliases=['m', 'u', 'd', 'l', 'r'])
async def move(ctx, direction: str = None, steps: int = 1):
    await handle_move_dungeon(ctx, direction, steps)

@bot.command()
async def start(ctx, game: str = None, *modifiers):
    if game is None:
        await ctx.send("Specify a game to start. Example: !start dungeon 2 fog")
        return
    
    # Prevent multiple games in the same channel
    from games.dungeon_crawler.manager import game_state
    channel_id = ctx.channel.id
    for state in game_state.values():
        if state.get('channel_id') == channel_id and state.get('game_active'):
            await ctx.send("A game is already running in this channel. End it with !end before starting a new one.")
            return

    if game.lower() == "dungeon":
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
    else:
        await ctx.send(f"Unknown game '{game}'. Available games: dungeon")

@bot.command()
async def end(ctx):
    channel_id = ctx.channel.id
    #print(f"Attempting to end game in channel {channel_id}, current game_state: {game_state_dungeon}")  # Debug
    
    ended = False
    for user_id, state in list(game_state_dungeon.items()):
        if state.get('channel_id') == channel_id and state.get('game_active'):
            state['game_active'] = False    
            del game_state_dungeon[user_id]
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