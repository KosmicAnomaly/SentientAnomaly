import discord
from discord.ext import commands
import re

class OnMessage(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    #check to see if the bot was mentioned
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.bot:
            return
        if '<@!776674222760132668>' == message.content or '<@776674222760132668>' == message.content:
            prefix = await self.bot.command_prefix(self.bot, message)
            await message.channel.send(f'My prefix is `{prefix}`.')
        
        if not message.guild:
          return
          
        #curse filter
        settings = await self.bot.curseFilterModule.find(message.guild.id)
        settings = settings['filters']

        message_content = message.content.strip().lower().replace('||','')
        message_content = re.split('[^a-zA-Z]', message_content)

        if "Cuss" in settings:
            if any(bad_word in message_content for bad_word in self.bot.cussWords):
                await message.channel.send(
                    f'{message.author.mention} watch your language, you f||or||king ||ice||hole.',
                    delete_after=7)
                await message.delete()
                return
        if "Vulgar" in settings:
            if any(bad_word in message_content for bad_word in self.bot.vulgarWords):
                await message.channel.send(
                    f'{message.author.mention} watch your language, you f||or||king ||ice||hole.',
                    delete_after=7)
                await message.delete()
                return
        if "Discriminatory" in settings:
            if any(bad_word in message_content
                  for bad_word in self.bot.discriminatoryWords):
                await message.channel.send(
                    f'{message.author.mention} watch your language, you f||or||king ||ice||hole.',
                    delete_after=7)
                await message.delete()
                return

        #invite blocker
        if message.author.guild_permissions.administrator == False:
          blockedTerms = ['discord.gg','discord.com/invite','discordapp.com/invite','invite.gg']
          res = [term for term in blockedTerms if(term in message_content)]
          if res:
            await message.channel.send(
                      f"{message.author.mention} please don't send invites.",
                      delete_after=7)
            await message.delete()
        
        await self.bot.process_commands(message)
      
    @commands.Cog.listener()
    async def on_message_edit(self, oldMessage, newMessage):
        if newMessage.author.bot or not newMessage.guild:
            return
        if newMessage.author.guild_permissions.administrator == False:
          #curse filter
          settings = await self.bot.curseFilterModule.find(newMessage.guild.id)
          settings = settings['filters']

          message_content = newMessage.content.strip().lower()
          message_content = re.split('[^a-zA-Z]', message_content)

          if "Cuss" in settings:
              if any(bad_word in message_content for bad_word in self.bot.cussWords):
                  await newMessage.channel.send(
                      f'{newMessage.author.mention} watch your language, you f||or||king ||ice||hole.',
                      delete_after=7)
                  await newMessage.delete()
                  return
          if "Vulgar" in settings:
              if any(bad_word in message_content for bad_word in self.bot.vulgarWords):
                  await newMessage.channel.send(
                      f'{newMessage.author.mention} watch your language, you f||or||king ||ice||hole.',
                      delete_after=7)
                  await newMessage.delete()
                  return
          if "Discriminatory" in settings:
              if any(bad_word in message_content
                    for bad_word in self.bot.discriminatoryWords):
                  await newMessage.channel.send(
                      f'{newMessage.author.mention} watch your language, you f||or||king ||ice||hole.',
                      delete_after=7)
                  await newMessage.delete()
                  return

          #invite blocker
          blockedTerms = ['discord.gg','discord.com/invite','discordapp.com/invite','invite.gg']
          message_content = newMessage.content.strip().lower()
          res = [term for term in blockedTerms if(term in message_content)]
          if res:
            modules = await self.bot.enabledModules.find(newMessage.guild.id)
            modules = modules["modules"]
            if 'InviteBlocker' in modules:
              await newMessage.channel.send(
                      f"{newMessage.author.mention} please don't send invites.",
                      delete_after=7)
              await newMessage.delete()

def setup(bot):
    bot.add_cog(OnMessage(bot))
