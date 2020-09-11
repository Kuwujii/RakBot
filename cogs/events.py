import discord, discord.ext.commands, discord.ext.tasks, asyncio # Discord API Wrapper, Commands Framework, Background loop Framework and Asyncio library
import cogs.rakbotbase # Basic cog

class Events(discord.ext.commands.Cog): # Define cog class
    def __init__(self, RAKBOT):
        self.RAKBOT = RAKBOT

    @discord.ext.commands.Cog.listener() # On ready event
    async def on_ready(self):
        await self.RAKBOT.wait_until_ready()
        print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ RakBot v0.0a by Kuwujii: ON")