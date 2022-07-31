import discord
from discord.ext import commands


class ModuleInstaller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #module
    @commands.group(
        aliases=['m'],
        brief='Displays information about a module',
        description=
        'Displays information about a module (module names are case-sensitive)',
        invoke_without_command=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.guild_only()
    async def module(self, ctx, module: str = None):
        if ctx.invoked_subcommand is None:
            if module == None:
                await ctx.send(
                    'Please specify a module or use one of the subcommands')
                await ctx.send_help(ctx.command)
            else:
                async with ctx.typing():
                    modules = await self.bot.enabledModules.find(ctx.guild.id)
                    modules = modules['modules']
                if module in modules:
                  moduleDict = [item for item in self.bot.ModuleDescriptions if item["Module"] == module][0]
                  async with ctx.typing():
                    embed=discord.Embed(title=moduleDict["Module"], description=moduleDict["Description"], color=0x47f592)
                    embed.add_field(name="Commands", value=moduleDict["Commands"], inline=False)
                    embed.set_footer(text=f"Category: {moduleDict['Category']}")
                  await ctx.send(embed=embed)

                else:
                    await ctx.send("That module isn't installed!")

    #module add
    @module.command(
        aliases=['a'],
        brief='Adds a module',
        description=
        'Adds a module to the server (module names are case-sensitive)')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def add(self, ctx, module: str = None):
        async with ctx.typing():
            modules = await self.bot.enabledModules.find(ctx.guild.id)
            modules = modules['modules']
            availableModules = [
                m for m in self.bot.loadedModules if m not in modules
            ]
        if module == None or not module in self.bot.loadedModules:
            if module == None:
                await ctx.send('Please specify which module you want to add!')
            else:
                await ctx.send("That module doesn't exist!")
            async with ctx.typing():
                embed = discord.Embed(
                    title="Available Modules",
                    description=str(availableModules)[1:-1].replace("'", "`"),
                    color=0x963fee)
                embed.set_footer(
                    text=
                    f"{len(modules)} Installed out of {len(self.bot.loadedModules)}"
                )
            await ctx.send(embed=embed)
        elif module in modules:
            await ctx.send(f"`{module}` is already added to this server!")
        else:
            modules.append(module)
            await self.bot.enabledModules.upsert({
                "_id": ctx.guild.id,
                "modules": modules
            })
            await ctx.send(f"Awesome! `{module}` has been added to the server."
                           )

    #module remove
    @module.command(
        aliases=['r'],
        brief='Removes a module',
        description=
        'Removes a module from the server (module names are case-sensitive)')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def remove(self, ctx, module: str = None):
        async with ctx.typing():
            modules = await self.bot.enabledModules.find(ctx.guild.id)
        modules = modules['modules']
        if module == None or not module in modules:
            if not module in modules:
                await ctx.send(f"`{module}` is not installed on this server!")
            async with ctx.typing():
                embed = discord.Embed(
                    title="Added Modules",
                    description=str(modules)[1:-1].replace("'", "`"),
                    color=0x963fee)
                embed.set_footer(
                    text=
                    f"{len(modules)} Installed out of {len(self.bot.loadedModules)}"
                )
            await ctx.send(embed=embed)
        else:
            modules.remove(module)
            await self.bot.enabledModules.upsert({
                "_id": ctx.guild.id,
                "modules": modules
            })
            await ctx.send(f"Ok! `{module}` has been removed from the server.")

    #module installed
    @module.command(
        aliases=['i'],
        brief='Lists installed modules',
        description='Lists the modules that are installed on the server')
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.guild_only()
    async def installed(self, ctx):
        async with ctx.typing():
            modules = await self.bot.enabledModules.find(ctx.guild.id)
            modules = modules['modules']
            embed = discord.Embed(
                title="Added Modules",
                description=str(modules)[1:-1].replace("'", "`"),
                color=0x963fee)
            embed.set_footer(
                text=
                f"{len(modules)} Installed out of {len(self.bot.loadedModules)}"
            )
        await ctx.send(embed=embed)

    #module available
    @module.command(
        aliases=['av'],
        brief='Lists available modules',
        description='Lists modules that can be installed on the server')
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.guild_only()
    async def available(self, ctx):
        async with ctx.typing():
            modules = await self.bot.enabledModules.find(ctx.guild.id)
            modules = modules['modules']
            availableModules = [
                m for m in self.bot.loadedModules if m not in modules
            ]
            embed = discord.Embed(
                title="Available Modules",
                description=str(availableModules)[1:-1].replace("'", "`"),
                color=0x963fee)
            embed.set_footer(
                text=
                f"{len(modules)} Installed out of {len(self.bot.loadedModules)}"
            )
        await ctx.send(embed=embed)

    #module list
    @module.command(
        aliases=['l'],
        brief='Lists all modules',
        description="Lists all modules that have been loaded into the bot's code"
    )
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.guild_only()
    async def list(self, ctx):
        async with ctx.typing():
            installedModules = await self.bot.enabledModules.find(ctx.guild.id)
            installedModules = installedModules['modules']
            modules = self.bot.loadedModules
            embed = discord.Embed(
                title="Modules",
                description=str(modules)[1:-1].replace("'", "`"),
                color=0x963fee)
            embed.set_footer(
                text=
                f"{len(installedModules)} Installed out of {len(self.bot.loadedModules)}"
            )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ModuleInstaller(bot))
