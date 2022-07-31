import discord
from discord.ext import commands


class ClearMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #clear messages command
    @commands.command(
        aliases=['remove', 'delete', 'yeetmsg', 'clean'],
        brief='Deletes messages',description = 'Deletes messages from a channel')
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def purge(self, ctx, amount: int = None):
        def is_not_pinned(message):
            return not message.pinned

        amount = amount or None
        if amount == None:
            await ctx.send(
                'Please specify an amount of messages to delete.',
                delete_after=10)
            return
        if amount > 100:
            await ctx.send(
                'For safety reasons, I politely refuse to delete more than 100 messages at a time.',
                delete_after=10)
            return
        async with ctx.typing():
            await ctx.channel.purge(limit=amount + 1, check=is_not_pinned)
        await ctx.send(f'Deleted {amount} message(s).', delete_after=10)


def setup(bot):
    bot.add_cog(ClearMessages(bot))
