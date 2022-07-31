import discord
from discord.ext import commands
from typing import Optional


class CustomSlowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #custom slowmode
    @commands.group(
        brief='Sets the slowmode',
        description='Sets a custom slowmode for a channel',
        invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self,
                       ctx,
                       channel: Optional[discord.TextChannel] = None,
                       seconds: int = None):
        if ctx.invoked_subcommand is None:
            channel = channel or ctx.channel
            if seconds == None:
                await ctx.send(
                    'Please specify the slowmode in seconds.', delete_after=10)
                return
            async with ctx.typing():
                await channel.edit(slowmode_delay=seconds)
                await ctx.send(
                    f'Ok! I set the slowmode in {channel.mention} to {seconds} seconds.'
                )

    @slowmode.command(
        name="disable",
        brief='Disables slowmode',
        description='Disables slowmode in a channel')
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def _disable(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        async with ctx.typing():
            await channel.edit(slowmode_delay=0)
        await ctx.send(f'Ok! I disabled slowmode in {channel.mention}.')

    @slowmode.group(
        brief='Sets the slowmode for a server',
        description='Sets a server-wide custom slowmode',
        invoke_without_command=True,
        aliases=['server'],
        name="global")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def _global(self, ctx, seconds: int = None):
        if ctx.invoked_subcommand is None:
            if seconds == None:
                await ctx.send(
                    'Please specify the slowmode in seconds.', delete_after=10)
                return
            async with ctx.typing():
                for channel in ctx.guild.channels:
                    await channel.edit(slowmode_delay=seconds)
            await ctx.send(
                f'Ok! I set the global slowmode in this server to {seconds} seconds.'
            )

    @_global.command(
        brief='Disables slowmode in a server',
        description='Disables slowmode in a server')
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def disable(self, ctx):
        async with ctx.typing():
            for channel in ctx.guild.channels:
                await channel.edit(slowmode_delay=0)
        await ctx.send('Ok! I disabled slowmode in this server.')


def setup(bot):
    bot.add_cog(CustomSlowmode(bot))
