import discord, discord.ext.commands, discord.ext.tasks, asyncio #Discord API Wrapper, Commands Framework, Background loop Framework and Asyncio library
import random #Other stuff
import cogs.rakbotbase #Basic cog

class Background(discord.ext.commands.Cog): #Define cog class
    def __init__(self, RAKBOT):
        self.RAKBOT = RAKBOT

        self.status.start() #Start the loops

    def cog_unload(self):
        self.status.cancel()

    @discord.ext.tasks.loop(seconds = 5.0)
    async def status(self): #Change discord status of the bot once in a while
        await self.RAKBOT.change_presence(activity = discord.Game(name = random.choice(["Temp", "Test"])))

    @status.before_loop
    async def before_status(self): #Make the status loop wait for the bot to get ready to work
        await self.RAKBOT.wait_until_ready()