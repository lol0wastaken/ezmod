import os
from itertools import cycle
import psycopg2
import discord
from discord.ext import commands, tasks
from pretty_help import PrettyHelp

DB_NAME = "x"
DB_USER = "x"
DB_PASS = "x"
DB_HOST = "x"
DB_PORT = "x"

conn = psycopg2.connect(database=DB_NAME, user=DB_USER,
                        password=DB_PASS, host=DB_HOST, port=DB_PORT)


# the word used before the actual command
def get_prefix(client, message):
    cur = conn.cursor()
    cur.execute(f"""SELECT PREFIX FROM DISCORDservers WHERE ID = {message.guild.id}""")
    prefix = cur.fetchall()
    for row in prefix:
        return row[0]

    conn.close()


client = commands.Bot(command_prefix=get_prefix, help_command=PrettyHelp(dm_help=None))
status = cycle(['(aio help) with Functions', '(aio help) Aio Ooof Ooof', '(aio help) Aio is Cool'])



# the commands
@client.event
async def on_ready():
    change_status.start()
    print('bot is ready.')


@tasks.loop(seconds=4)
async def change_status():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(next(status)))


@client.event
async def on_guild_join(guild):
    cur = conn.cursor()
    cur.execute(f"""INSERT INTO DISCORDservers (ID, PREFIX, INFO) VALUES ({guild.id}, 'aio ',
    'No Info Given to give info for your server type aio infochange (Your Server Info Here)')""")
    conn.commit()

    conn.close()


@client.event
async def on_guild_remove(guild):
    cur = conn.cursor()
    cur.execute(f"""DELETE FROM DISCORDservers WHERE ID = {guild.id}""")
    conn.commit()

    conn.close()


# later
@client.event
async def on_member_join(member):
    print(f'{member} joined.')


@client.event
async def on_member_remove(member):
    print(f'{member} left.')


# cogs

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


# Handling errors
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            'Sorry But Check if you have typed anything in uppercase or if the command exists or type in a required Value/Word.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have all the required Permissions :angry:")


client.run('x')
