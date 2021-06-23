import discord
from discord.ext import commands

from main import conn


class Moderation(commands.Cog):
    """Help with Moderation of the Server"""

    def __init__(self, client):
        self.client = client

    @commands.command(Breif='Use the BANHAMMER!', help='BAN the troublemakers!')
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.User = None, reason=None):
        if member == None or member == ctx.message.author:
            await ctx.channel.send("You cannot ban yourself")
            return
        if reason == None:
            reason = "being a jerk!"
        message = f"You have been banned by {ctx.author.name} from {ctx.guild.name} for {reason}"
        await member.send(message)
        await ctx.guild.ban(member, reason=reason)
        await ctx.channel.send(f"{member} was banned by {ctx.author.name} for {reason}!")

    @commands.command(help="Use it to unban the people you BANNED!")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()

        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await member.send(
                    f'You have been Unbanned from {ctx.guild.name} by {ctx.author.name}, so now dont ever BREAK RULES AGAIN!')
                await ctx.channel.send(f"{ctx.author.name} Unbanned {user.name}#{user.discriminator}")

    @commands.command(help="KICK those annoying people out!")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def kick(self, ctx, member: discord.User = None, reason=None):
        if member == None or member == ctx.message.author:
            await ctx.channel.send("You cannot kick yourself")
            return
        if reason == None:
            reason = "being a jerk!"
        message = f"You have been kicked by {ctx.author.name} from {ctx.guild.name} for {reason}"
        await member.send(message)
        await ctx.guild.kick(member, reason=reason)
        await ctx.channel.send(f"{member} was kicked by {ctx.author.name} for {reason}!")

    @commands.command(help="Change the bot's prefix (Default=aio)")
    @commands.has_permissions(administrator=True, manage_roles=True)
    async def changeprefix(self, ctx, *, prefix):
        bettah = prefix + ' '

        cur = conn.cursor()
        cur.execute(f"UPDATE DISCORDservers set PREFIX = '{bettah}' WHERE ID = {ctx.guild.id}")
        conn.commit()

        await ctx.send(f'Ok the Prefix is changed to {bettah}')

        cur.close()
        conn.close()

    @commands.command(help="Change your Server's Info")
    @commands.has_permissions(administrator=True, manage_roles=True)
    async def infochange(self, ctx, *, info):
        cur = conn.cursor()
        cur.execute(f"UPDATE DISCORDservers set INFO = '{info}' WHERE ID = {ctx.guild.id}")
        conn.commit()

        await ctx.send(f'Ok the Prefix is changed to:\n {info}')

        cur.close()
        conn.close()

    @commands.command(help="It's use to clear messages")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=0):
        await ctx.channel.purge(limit=amount + 2)


def setup(client):
    client.add_cog(Moderation(client))
