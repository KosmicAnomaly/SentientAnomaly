import discord
from discord.ext import commands
import time, datetime
import typing

class CoreCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Change the bot's prefix",description="Changes the bot's prefix in a server")
    @commands.has_guild_permissions(manage_guild=True)
    @commands.guild_only()
    async def prefix(self, ctx, prefix: str = None):
        async with ctx.typing():
            if not prefix:
                prefix = 'b!'
                response = f"Alright! I have set the prefix in this server to the default prefix of `{prefix}`."
            else:
                response = f"Alright! My prefix in this server is now `{prefix}`!"
            await self.bot.prefixes.upsert({
                "_id": ctx.guild.id,
                "prefix": prefix
            })
        await ctx.send(response)

    #bot stats command
    @commands.command(brief='Bot stats',description='Displays some cool information about the status of the bot')
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def botstats(self, ctx):
        async with ctx.typing():
            uptime = int(round(time.time() - self.bot.startTime))
            uptime = datetime.timedelta(seconds=uptime)

            ping = round(self.bot.latency * 1000)

            embed = discord.Embed(
                title='Bot Information',
                description=f'**Uptime:** {uptime}\n**Ping:** {ping}',
                color=0x24f061)
            embed.set_author(
                name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed.set_footer(text=f'Developed by {self.bot.developer}')
        await ctx.send(embed=embed)
      
    @commands.command(brief='Invite link',description='Sends a link to invite the bot to your server')
    async def invite(self,ctx):
      async with ctx.typing():
        embed=discord.Embed(title='**Invite Me!**', url='https://discord.com/api/oauth2/authorize?client_id=776674222760132668&permissions=8&scope=bot', color=0x18ece9)
      await ctx.send(embed=embed)

    @commands.command(brief='Support server link',description="Sends a link to the bot's support server")
    async def support(self,ctx):
      async with ctx.typing():
        embed=discord.Embed(title='**Support Server**',description='Go here to suggest features and report bugs', url='https://discord.gg/QgTgrNNqEe', color=0x18ece9)
      await ctx.send(embed=embed)

    #check to see if the bot was mentioned
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if '<@!764577620872134726>' == message.content or '<@764577620872134726>' == message.content:
            await message.channel.send('My prefix is `~`.')





def setup(bot):
    bot.add_cog(CoreCommands(bot))
