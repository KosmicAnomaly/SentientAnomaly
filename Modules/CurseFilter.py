import discord
from discord.ext import commands
import re




class CurseFilter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        #Open list of curses
        with open("BadWords/cussWords.txt") as cussWordslist:
          self.bot.cussWords = [
            cussWord.lower().replace('\n', '').replace('\t', '')
            for cussWord in cussWordslist.readlines()
        ]
        with open("BadWords/discriminatoryWords.txt") as discriminatoryWordsList:
          self.bot.discriminatoryWords = [
            discriminatoryWord.lower().replace('\n', '').replace('\t', '')
            for discriminatoryWord in discriminatoryWordsList.readlines()
        ]
        with open("BadWords/vulgarWords.txt") as vulgarWordsList:
          self.bot.vulgarWords = [
            vulgarWord.lower().replace('\n', '').replace('\t', '')
            for vulgarWord in vulgarWordsList.readlines()
        ]

    @commands.command(
        aliases=['cursetoggle'],
        brief='Curse filter settings',
        description=
        'Toggles various curse filters (Cuss/Vulgar/Discriminatory) on and off'
    )
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def cursefiltertoggle(self, ctx, filter: str = None):
        if filter == None or filter not in [
                'Cuss', 'Vulgar', 'Discriminatory'
        ]:
            await ctx.send(
                'Please specify which of the following curse filters you want to toggle:\nCuss\nVulgar\nDiscriminatory'
            )
        else:
            async with ctx.typing():
                settings = await self.bot.curseFilterModule.find(ctx.guild.id)
                settings = settings['filters']
            if filter in settings:
                await ctx.send(f'Toggled {filter} off')
                settings.remove(filter)
            else:
                await ctx.send(f'Toggled {filter} on')
                settings.append(filter)
            await self.bot.curseFilterModule.upsert({
                "_id": ctx.guild.id,
                "filters": settings
            })


def setup(bot):
    bot.add_cog(CurseFilter(bot))
