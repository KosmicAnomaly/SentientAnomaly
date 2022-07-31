import discord
from discord.ext import commands


class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #server info command
    @commands.command(brief='Server info',description = 'Displays some pretty cool stats about the server')
    @commands.guild_only()
    async def serverinfo(self, ctx):
        async with ctx.typing():
            embed = discord.Embed(
                title=ctx.guild.name,
                description=
                f'{ctx.guild.member_count} Members\nCreated {ctx.guild.created_at.strftime("%m/%d/%Y")}\n{len(ctx.guild.emojis)} Emojis',
                color=0xef2906)
            embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ServerInfo(bot))
