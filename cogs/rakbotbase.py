import discord, discord.ext.commands, discord.ext.tasks, asyncio #Discord API Wrapper, Commands Framework, Background loop Framework and Asyncio library
import time #Other stuff
import cogs.events, cogs.commands #Other cogs

class RakBotBase(discord.ext.commands.Cog): #Define cog class
    def __init__(self, RAKBOT):
        self.RAKBOT = RAKBOT

        self.RAKBOT.add_cog(cogs.events.Events(self.RAKBOT)) #Run other cogs
        
        self.RAKBOT.add_cog(cogs.commands.Tools(self.RAKBOT))
        self.RAKBOT.add_cog(cogs.commands.Fun(self.RAKBOT))
        self.RAKBOT.add_cog(cogs.commands.DnD(self.RAKBOT))

class Functions(): #Usefull functions
    def __init__(self):
        pass

    def log_time(self): #Current time for console logs
        return time.strftime("%d-%m-%Y %H:%M:%S")