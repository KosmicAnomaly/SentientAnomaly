import discord
from discord.ext import commands


class KickBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #kick member command
    @commands.command(aliases=['yeet'], brief='Kicks a member',description = 'Kicks a member from the server')
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self,
                   ctx,
                   target: discord.Member = None,
                   *,
                   reason="No reason provided"):
        if target == None:
            await ctx.send('Please specify a user to kick.')
            return
        if ctx.author.top_role.position > target.top_role.position:
            async with ctx.typing():
                if target.dm_channel == None:
                    await target.create_dm()
                embed = discord.Embed(
                    title=f"You have been kicked from {ctx.guild}",
                    color=0xff0000)
                embed.add_field(name="Reason", value=reason, inline=False)
                embed.set_footer(text=f"You were kicked by {ctx.author}")
                await target.dm_channel.send(embed=embed)
                await target.kick(reason=reason)
            await ctx.send('Kicked member.')
        else:
            await ctx.send(
                "You can't kick someone whose highest role is above yours!")
            return

    #ban member command
    @commands.command(aliases=['permayeet'], brief='Bans a member',description = 'Bans a member from the server')
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self,
                  ctx,
                  target: discord.Member = None,
                  *,
                  reason="No reason provided"):
        if target == None:
            await ctx.send('Please specify a member to ban.')
            return
        if ctx.author.top_role.position < target.top_role.position:
            await ctx.send(
                "You can't ban someone whose highest role is above yours!")
            return
        else:
            await target.ban(reason=reason)
            await ctx.send('Banned member.')

    #unban member
    @commands.command(aliases=['unyeet'], brief='Unbans a member',description = 'Unbans a member from the server')
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self,
                    ctx,
                    target: discord.Member = None,
                    *,
                    reason="No reason provided"):
        if target == None:
            await ctx.send('Please specify a member to unban.')
            return
        else:
            await target.unban(reason=reason)
            await ctx.send('Unbanned member.')


def setup(bot):
    bot.add_cog(KickBan(bot))
