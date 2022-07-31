import discord
from discord.ext import commands


class ChannelLock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #lock channel command
    @commands.command(
        brief='Locks a channel',
        description=
        'Locks a channel in a server, which prevents members from sending messages in that channel'
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        async with ctx.typing():
            overwrite = discord.PermissionOverwrite()
            overwrite.send_messages = False
            await ctx.channel.set_permissions(
                ctx.guild.default_role,
                overwrite=overwrite,
                reason='Locked channel')
        await ctx.send(
            'This channel has been locked and messages can no longer be sent.')

    #unlock channel command
    @commands.command(
        brief='Unlocks a channel',
        description='Unlocks a channel that has been locked')
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        async with ctx.typing():
            overwrite = discord.PermissionOverwrite()
            overwrite.send_messages = None
            await ctx.channel.set_permissions(
                ctx.guild.default_role,
                overwrite=overwrite,
                reason='Unlocked channel')
        await ctx.send('Unlocked channel.')


def setup(bot):
    bot.add_cog(ChannelLock(bot))
