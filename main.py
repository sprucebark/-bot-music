import discord
import os
from discord.ext import commands
import random

from music_cog import Music

import keep_alive

Bot = commands.Bot(command_prefix='+')
Bot.remove_command("help")

@Bot.event
async def on_command_error(ctx, error):
 if isinstance(error, commands.CommandOnCooldown):
   msg = "Coba Beberapa saat lagi!".format(error.retry_after)

   await ctx.send(msg)

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@Bot.command()
@commands.cooldown(5,10,commands.BucketType.user)
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("Game sedang berlangsungS.")

@Bot.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " Menang!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("Seri!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Pastikan memilih antar 1 sampai 9 di tempat yang masih kosong.")
        else:
            await ctx.send("Bukan giliranmu.")
    else:
        await ctx.send("Mulai baru dengan !tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Mention 2 Player untuk mulai!.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Pastikan untuk Ping/Mention Teman (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Pilih lokasi nya.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Pastikan untuk mengisi integer.")

@Bot.event
async def on_ready():
  await Bot.change_presence(activity=discord.Game(name="+help for info"))

@Bot.group(invoke_without_command=True)
async def help(ctx):
  em = discord.Embed(title = "Help", description = "Gunakan +help <command> untuk info lebih lanjut.", color = ctx.author.color)  

  em.add_field(name = "Music", value = "play,pause,resume,queue,join,leave,skip,remove,clear,np,volume,alias,tictactoe")

  await ctx.send(embed = em)

@help.command()
async def tictactoe(ctx):

  em = discord.Embed(title = "Tic-Tac-Toe", description = "TicTacToe game", color = ctx.author.color)

  em.add_field(name = "***Syntax***", value = "+tictactoe <player 1> <player 2>, +place <tempat ingin ditaruh(dari pojok kiri atas ke kanan) dalam nomer> ")

  await ctx.send(embed=em)

@help.command()
async def play(ctx):

  em = discord.Embed(title = "Play", description = "Memainkan Music", color = ctx.author.color)

  em.add_field(name = "***Syntax***", value = "+play <music yang diinginkan>")

  await ctx.send(embed=em)

@help.command()
async def pause(ctx):

  em = discord.Embed(title = "Pause", description = "Menghentikan music sementara sampai command resume terkirim", color = ctx.author.color)

  em.add_field(name = "***Syntax***", value = "+pause")

  await ctx.send(embed=em)

@help.command()
async def resume(ctx):

  em = discord.Embed(title = "resume", description = "Melanjutkan music bila music di pause", color = ctx.author.color)

  em.add_field(name = "***Syntax***", value = "+resume")

  await ctx.send(embed=em)

@help.command()
async def queue(ctx):

  em = discord.Embed(title = "Queue", description = "Menunjukkan queue atau antrian bila ada", color = ctx.author.color)

  em.add_field(name = "***Syntax***", value = "+queue")

  await ctx.send(embed=em)

@help.command()
async def join(ctx):

  em = discord.Embed(title = "Join", description = "Membuat Bot masuk ke dalam voice channel yang lu udh masukin", color = ctx.author.color)

  em.add_field(name = "***Syntax***", value = "+join")

  await ctx.send(embed=em)

@help.command()
async def leave(ctx):

  em = discord.Embed(title = "Leave", description = "Membuat bot Meninggalkan voice channel dan menghentikan lagu yang dimainkan", color = ctx.author.color)

  em.add_field(name = "***Syntax***", value = "+leave")

  await ctx.send(embed=em)

@help.command()
async def skip(ctx):

  em = discord.Embed(title = "Skip", description = "Skip ke lagu selanjutnya bila ada, bila tidak maka musik akan berhenti", color = ctx.author.color)

  em.add_field(name = "***Syntax***", value = "+skip")

  await ctx.send(embed=em)

@help.command()
async def remove(ctx):

  em = discord.Embed(title = "Remove", description = "Menghapus suatu lagu di antrian", color = ctx.author.color)

  em.add_field(name = "***Syntax***", value = "+play <urutan lagu(1+)>")

  await ctx.send(embed=em)

@help.command()
async def np(ctx):

  em = discord.Embed(title = "np", description = "Menunjukkan identifikasi lagu yang sedang dimainkan", color = ctx.author.color)

  em.add_field(name = "***Syntax***", value = "+np")

  await ctx.send(embed=em)

@help.command()
async def volume(ctx):

  em = discord.Embed(title = "Volume", description = "Mengatur volume bot untuk yang memberi command", color = ctx.author.color)

  em.add_field(name = "***Syntax***", value = "+volume <1-100>")

  await ctx.send(embed=em)

@help.command()
async def alias(ctx):

  em = discord.Embed(title = "Alias", description = "Command singkat untuk mempermudah", color = ctx.author.color)

  em.add_field(name = "***alias play***", value = "+play,+sing,+p")
  em.add_field(name = "***alias join***", value = "+join,+connect,+j")
  em.add_field(name = "***alias pause***", value = "+pause")
  em.add_field(name = "***alias resume***", value = "+resume")
  em.add_field(name = "***alias skip***", value = "+skip")
  em.add_field(name = "***alias remove***", value = "+rm,+remove,+rem")
  em.add_field(name = "***alias clear***", value = "+clear,+clr,+cl,+cr")
  em.add_field(name = "***alias queue***", value = "+queue,+playslist,+que")
  em.add_field(name = "***alias np***", value = "+np,+current,+currentsong,+playing")
  em.add_field(name = "***alias volume***", value = "+volume,+v,+vol")
  em.add_field(name = "***alias leave***", value = "+leave,+stop,+dc,+disconnect,+bye")

  await ctx.send(embed=em)
                     

Bot.add_cog(Music(Bot))

my_secret = os.environ['token']
Bot.run(my_secret)
