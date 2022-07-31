import discord
from discord.ext import commands


class WhoIs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #user info lookup
    @commands.command(brief='Returns info about a member')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def whois(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        async with ctx.typing():
            embed = discord.Embed(
                title=f'{member.name}#{member.discriminator}',
                description=member.mention,
                color=member.color)
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(
                name="Account Created",
                value=member.created_at.date(),
                inline=False)
            if member.joined_at:
                embed.add_field(
                    name="Joined Server",
                    value=member.joined_at.date(),
                    inline=False)
            if member.premium_since:
                embed.add_field(
                    name="Server Boosting Since",
                    value=member.premium_since.date(),
                    inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(WhoIs(bot))
