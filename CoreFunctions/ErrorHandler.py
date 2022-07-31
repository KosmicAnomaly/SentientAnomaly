import discord
from discord.ext import commands
import math


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, commands.DisabledCommand,
                   commands.NoPrivateMessage)
        if isinstance(error, ignored):
            return
        elif isinstance(error, commands.BotMissingPermissions):
            missing = [
                perm.replace('_', ' ').replace('guild', 'server').title()
                for perm in error.missing_perms
            ]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]),
                                          missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = 'I need the **{}** permission(s) to run this command.'.format(
                fmt)
            await ctx.send(_message)
            return
        elif isinstance(error, commands.errors.MissingPermissions):
            missing = [
                perm.replace('_', ' ').replace('guild', 'server').title()
                for perm in error.missing_perms
            ]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]),
                                          missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = 'You need the **{}** permission(s) to use this command.'.format(
                fmt)
            await ctx.send(_message)
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You are missing a required argument!")
            await ctx.send_command_help(ctx.command).help
            return
        elif isinstance(error, commands.BadArgument):
            await ctx.send("One of your arguments is invalid!")
            await ctx.send_help(ctx.command)
            return
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                "This command is on cooldown, please retry in {}s.".format(
                    math.ceil(error.retry_after)))
            return
        elif isinstance(error, commands.NotOwner):
            async with ctx.typing():
                embed = discord.Embed(
                    title="Not the One. NOT the One.", color=0xf005d4)
                embed.set_thumbnail(
                    url=
                    'https://i.pinimg.com/600x315/02/6a/ee/026aee35d5c3ccd59daaf9360957042c.jpg'
                )
            await ctx.send(embed=embed)
            return
        elif isinstance(error, commands.NSFWChannelRequired):
            await ctx.send(
                'I refuse to use this command outside of a designated NSFW channel. This incident has been reported.'
            )
        elif isinstance(error, commands.CheckFailure):
          return
        else:
            await ctx.send(
                "If you are reading this, then it means that the developer is an idiot and I have sent him an error message."
            )
            raise error


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
