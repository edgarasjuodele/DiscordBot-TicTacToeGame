import asyncio
import discord
from discord.ext import commands
from decouple import config
import tictactoe as tictac

token = config('AUTH_TOKEN')
client = commands.Bot(command_prefix='!')
symbols = {
    "1️⃣": 1,
    "2️⃣": 2,
    "3️⃣": 3,
    "4️⃣": 4,
    "5️⃣": 5,
    "6️⃣": 6,
    "7️⃣": 7,
    "8️⃣": 8,
    "9️⃣": 9
}


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)


@client.command()
async def challenge(ctx, target: discord.Member):
    ttt = tictac.TicTac()
    sides = ['🇽', '🇴']
    msg = await ctx.send(f"{ctx.author.mention} challenged {target.mention}, choose your symbol")

    for e in sides:
        await msg.add_reaction(e)

    def check(reaction, user):
        return (reaction.message.id == msg.id) and (user.id == ctx.author.id or user.id == target.id) and \
               (str(reaction) in sides)

    try:
        reaction, user = await client.wait_for('reaction_add', check=check, timeout=60)
    except asyncio.TimeoutError:
        await ctx.send("Timed out")
    if user.id == ctx.author.id:
        if str(reaction) == '🇽':
            await ctx.send(f"{ctx.author.mention} is player 1 with symbol 🇽 and colour green")
            p1 = ctx.author
            p2 = target
            p1sym = '🇽'
            p2sym = '🇴'
        else:
            await ctx.send(f"{ctx.author.mention} is player 1 with symbol 🇴 and colour green")
            p1 = ctx.author
            p2 = target
            p1sym = '🇴'
            p2sym = '🇽'
    elif user.id == target.id:
        if str(reaction) == '🇽':
            await ctx.send(f"{target.mention} is player 1 with symbol 🇽 and colour green")
            p1 = target
            p2 = ctx.author
            p1sym = '🇽'
            p2sym = '🇴'
        else:
            await ctx.send(f"{target.mention} is player 1 with symbol 🇴 and colour green")
            p1 = target
            p2 = ctx.author
            p1sym = '🇴'
            p2sym = '🇽'

    moves = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
    embed = discord.Embed(title="TicTacToe - Green", color=0x00ff00)
    embed.add_field(name='Player 1', value='{0.mention} with {1} and colour green'.format(p1, p1sym))
    embed.add_field(name='Player 2', value='{0.mention} with {1} and colour red'.format(p2, p2sym))
    embed.set_image(url=ttt.board())
    message = await ctx.send(embed=embed)
    # Add 1 to 9 reactions
    for e in moves:
        await message.add_reaction(e)

    player = "Green"
    colour = 0x00ff00
    # Game loop
    while True:
        def check_moves(reaction, user):
            return (reaction.message.id == message.id) and (user.id == ctx.author.id or user.id == target.id) and \
                   (str(reaction) in moves)

        try:
            reaction, user = await client.wait_for('reaction_add', check=check_moves, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send("Timed out")
        if reaction:
            # Embed updates on Green user Move
            if player == "Green" and user.id == p1.id:
                status = ttt.checkwin(p1sym, symbols[str(reaction)])
                if status == 1 or status == -1:
                    embed = discord.Embed(title=f"TicTacToe - {player} Wins", color=colour)
                    embed.set_image(url=ttt.move(p1sym, symbols[str(reaction)]))
                    await message.edit(embed=embed)
                    break
                elif status == 0:
                    colour = 0x808080
                    embed = discord.Embed(title=f"TicTacToe - Draw", color=colour)
                    embed.set_image(url=ttt.move(p1sym, symbols[str(reaction)]))
                    await message.edit(embed=embed)
                    break
                else:
                    player = "Red"
                    colour = 0xff0000
                    embed = discord.Embed(title=f"TicTacToe - {player}", color=colour)
                    embed.add_field(name='Player 1', value='{0.mention} with {1} and colour green'.format(p1, p1sym))
                    embed.add_field(name='Player 2', value='{0.mention} with {1} and colour red'.format(p2, p2sym))
                    embed.set_image(url=ttt.move(p1sym, symbols[str(reaction)]))
                    await message.edit(embed=embed)
            # Embed updates on Red user Move
            elif player == "Red" and user.id == p2.id:
                status = ttt.checkwin(p2sym, symbols[str(reaction)])
                if status == 1 or status == -1:
                    embed = discord.Embed(title=f"TicTacToe - {player} Wins", color=colour)
                    embed.set_image(url=ttt.move(p2sym, symbols[str(reaction)]))
                    await message.edit(embed=embed)
                    break
                elif status == 0:
                    colour = 0x808080
                    embed = discord.Embed(title=f"TicTacToe - Draw", color=colour)
                    embed.set_image(url=ttt.move(p2sym, symbols[str(reaction)]))
                    await message.edit(embed=embed)
                    break
                else:
                    player = "Green"
                    colour = 0x00ff00
                    embed = discord.Embed(title=f"TicTacToe - {player}", color=colour)
                    embed.add_field(name='Player 1', value='{0.mention} with {1} and colour green'.format(p1, p1sym))
                    embed.add_field(name='Player 2', value='{0.mention} with {1} and colour red'.format(p2, p2sym))
                    embed.set_image(url=ttt.move(p2sym, symbols[str(reaction)]))
                    await message.edit(embed=embed)
        moves.remove(str(reaction))

client.run(token)
