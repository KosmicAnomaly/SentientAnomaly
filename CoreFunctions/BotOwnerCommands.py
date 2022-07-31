import discord
from discord.ext import commands


class BotOwnerCommands(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    #logout command
    @commands.command(aliases=['shutdown', 'yeetbot'])
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send('I must go, my people need me.')
        await self.bot.logout()

    #change activity command
    @commands.command(aliases=['activity', 'status'])
    @commands.is_owner()
    async def changeactivity(self, ctx, *, activity: str = 'for ~help'):
        await self.bot.change_presence(activity=discord.Game(name=activity))
        await ctx.send('Activity changed.')


def setup(bot):
    bot.add_cog(BotOwnerCommands(bot))
