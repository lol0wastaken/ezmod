# all the imports
from discord.ext import commands

from main import conn


class Intro(commands.Cog):
    """These Commands are for Introduction"""

    def __init__(self, client):
        self.client = client

    @commands.command(help='No one uses this command')
    async def hello(self, ctx):
        await ctx.send('Hi you Bot')

    @commands.command(help="Use this command to see the server's info set by the Admins/Mods")
    async def serverinfo(self, ctx):
        cur = conn.cursor()
        cur.execute(f"""SELECT INFO FROM DISCORDservers WHERE ID = {ctx.guild.id}""")
        info = cur.fetchall()
        for row in info:
            await ctx.send(row[0])

        conn.close()


def setup(client):
    client.add_cog(Intro(client))
