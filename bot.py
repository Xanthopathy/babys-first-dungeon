import discord
from discord.ext import commands
from config import BOT_TOKEN
from games.dungeon_crawler.manager import handle_start as handle_start_dungeon, handle_move as handle_move_dungeon, game_state as game_state_dungeon
from games.splendor.manager import handle_start as handle_start_splendor, handle_join as handle_join_splendor, handle_start_game as handle_start_game_splendor, game_state as game_state_splendor, handle_take_three, handle_take_two, handle_reserve, handle_purchase

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

# Remove default help command
bot.remove_command('help')

# Commands
@bot.command()
async def help(ctx, *args):
    if args and args[0].lower() == "dungeon":
        dungeon_commands = (
            "**Dungeon Crawler Commands:**\n"
            "`$dungeon [boards] [fog|fogless]` - Start a new dungeon crawler game (default 1 board and fogless).\n"
            "`$move <up/down/left/right> [steps]` or `$m <u/d/l/r> [steps]` or `$<u/d/l/r> [steps]` - Move the player 1 of 4 directions. Step count is 1 by default. (ex: `$move right`, `$move right 3`, `$m r`, `$m r 3`, `$r`, `$r 3`).\n"
        )
        await ctx.send(dungeon_commands)
        return
    if args and args[0].lower() == "splendor":
        splendor_commands = (
            "**Splendor Commands:**\n"
            "`$splendor` - Start a Splendor game for 2-4 players. Players must join with `$join` and start with `$start`.\n"
            "`$join` - Join a pending Splendor game in the channel.\n"
            "`$start` - Start a pending Splendor game after players have joined.\n"
            "`$end` - End the active Splendor game in the channel.\n"
            "`$take3/t3 <gem1> <gem2> <gem3>` - Take 3 different gem tokens (e.g., `$take3 ruby emerald sapphire`).\n"
            "`$take2/t2 <gem>` - Take 2 tokens of the same gem if 4+ are available (e.g., `$take2 ruby`).\n"
            "`$reserve/res <level> <index>` - Reserve a card and take a gold token (e.g., `$reserve 1 1`).\n"
            "`$purchase/buy <level> <index>` - Purchase a face-up card (e.g., `$purchase 1 1`).\n"
            "`$purchase/buy reserved <index>` - Purchase a reserved card (e.g., `$purchase reserved 1`).\n"
            "Gem shorthands:\n"
            "🔴: `ruby`, `red`, `r`\n"
            "🟢: `emerald`, `green`, `e`, `g`\n"
            "🔵: `sapphire`, `blue`, `s`, `u`\n"
            "⚪: diamond`, `white`, `d`, `w`\n"
            "⚫: `onyx`, `o`, `black`, `k`\n"
        )
        await ctx.send(splendor_commands)
        return
    help_text = (
        "**Available Commands:**\n"
        "`$help` - Show this help message.\n"
        "`$help dungeon` - Show help for Dungeon Crawler commands.\n"
        "`$help splendor` - Show help for Splendor commands.\n"
        "`$join` - Join a pending game in the channel.\n"
        "`$start` - Start a pending game after players have joined.\n"
        "`$end` - End the active game in the channel.\n"
    ) # remove [players]
    await ctx.send(help_text)

@bot.command()
async def join(ctx):
    channel_id = ctx.channel.id
    # Find pending Splendor game in this channel
    for user_id, state in list(game_state_splendor.items()):
        if state.get('channel_id') == channel_id and state.get('game_pending'):
            await handle_join_splendor(ctx, user_id)
            joined = len(state['joined_players'])
            await ctx.send(f"{joined} player(s) have joined. Need 2-4 to start.")
            return
    await ctx.send("No pending game to join in this channel. Start one with $splendor.")

@bot.command()
async def start(ctx):
    channel_id = ctx.channel.id
    # Find pending Splendor game in this channel
    for user_id, state in list(game_state_splendor.items()):
        if state.get('channel_id') == channel_id and state.get('game_pending'):
            joined = len(state['joined_players'])
            if joined < 2 or joined > 4:
                await ctx.send(f"Cannot start: {joined} player(s) joined. Need 2-4 players.")
                return
            await handle_start_game_splendor(ctx, user_id)
            return
    await ctx.send("No pending game to start in this channel. Start one with $splendor.")

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
        if state.get('channel_id') == channel_id and (state.get('game_active') or state.get('game_pending')):
            state['game_active'] = False
            state['game_pending'] = False
            del game_state_splendor[user_id]
            ended = True

    if ended:
        await ctx.send("Game ended in this channel.")
    else:
        await ctx.send("No active game to end in this channel.")

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
async def splendor(ctx):
    channel_id = ctx.channel.id
    # Prevent multiple games in the same channel
    active = any(
        state.get('channel_id') == channel_id and (state.get('game_active') or state.get('game_pending'))
        for state in (list(game_state_dungeon.values()) + list(game_state_splendor.values()))
    )
    if active:
        await ctx.send("A game is already running or pending in this channel. End it with $end or start it with $start.")
        return

    await handle_start_splendor(ctx)
    await ctx.send("A game of Splendor is starting! Players need to type `$join` to join. Minimum 2, maximum 4 players.")

@bot.command(aliases=['t3'])
async def take3(ctx, gem1: str = None, gem2: str = None, gem3: str = None):
    channel_id = ctx.channel.id
    if gem1 is None or gem2 is None or gem3 is None:
        await ctx.send("Usage: `$take3 <gem1> <gem2> <gem3>` (e.g., `$take3 ruby emerald sapphire`). Use `$help splendor` for gem shorthands.")
        return
    for user_id, state in game_state_splendor.items():
        if state.get('channel_id') == channel_id and state.get('game_active'):
            await handle_take_three(ctx, user_id, [gem1, gem2, gem3])
            return
    await ctx.send("No active Splendor game in this channel.")

@bot.command(aliases=['t2'])
async def take2(ctx, gem: str = None):
    channel_id = ctx.channel.id
    if gem is None:
        await ctx.send("Usage: `$take2 <gem>` (e.g., `$take2 ruby`). Use `$help splendor` for gem shorthands.")
        return
    for user_id, state in game_state_splendor.items():
        if state.get('channel_id') == channel_id and state.get('game_active'):
            await handle_take_two(ctx, user_id, gem)
            return
    await ctx.send("No active Splendor game in this channel.")

@bot.command(aliases=['res'])
async def reserve(ctx, level: str = None, card_index: int = None):
    channel_id = ctx.channel.id
    if level is None or card_index is None:
        await ctx.send("Usage: `$reserve <level> <index>` (e.g., `$reserve 1 1`).")
        return
    for user_id, state in game_state_splendor.items():
        if state.get('channel_id') == channel_id and state.get('game_active'):
            await handle_reserve(ctx, user_id, level, card_index)
            return
    await ctx.send("No active Splendor game in this channel.")

@bot.command(aliases=['buy'])
async def purchase(ctx, source_or_level: str = None, index_or_level: int = None, card_index: int = None):
    channel_id = ctx.channel.id
    if source_or_level is None or index_or_level is None:
        await ctx.send("Usage: `$purchase <level> <index>` (e.g., `$purchase 1 1`) or `$purchase reserved <index>` (e.g., `$purchase reserved 1`).")
        return
    for user_id, state in game_state_splendor.items():
        if state.get('channel_id') == channel_id and state.get('game_active'):
            source = 'revealed' if source_or_level.lower() != 'reserved' else 'reserved'
            level = source_or_level if source == 'revealed' else 'reserved'
            index = index_or_level if source == 'revealed' else source_or_level
            if source == 'revealed' and card_index is not None:
                index = card_index
            await handle_purchase(ctx, user_id, source, level, index)
            return
    await ctx.send("No active Splendor game in this channel.")

# Bot event
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Run the bot
bot.run(BOT_TOKEN)