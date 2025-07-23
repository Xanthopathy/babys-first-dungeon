from games.splendor.mechanics import setup_game
from games.splendor.display import display_board

game_state = {}

async def handle_start(ctx, players):
    user_id = ctx.author.id
    channel_id = ctx.channel.id

    # Initialize game state
    game_state[user_id] = setup_game(players)
    game_state[user_id]['channel_id'] = channel_id

    # Display the board
    board_display = display_board(game_state[user_id])
    await ctx.send(board_display)