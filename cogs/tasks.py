import discord, discord.ext.commands, discord.ext.tasks, asyncio #Discord API Wrapper, Commands Framework, Background loop Framework and Asyncio library
import random #Other stuff

class Background(discord.ext.commands.Cog): #Define cog class
    def __init__(self, RAKBOT):
        self.RAKBOT = RAKBOT
        self.SHOUT_AT = []

        self.status_loop.start() #Start the loops
        self.shout_loop.start()

    def cog_unload(self):
        self.status_loop.cancel()
        self.shout_loop.cancel()

    def start_shouting_at(self, member): #Add user to list of users to wake up
        if member not in self.SHOUT_AT:
            self.SHOUT_AT.append(member)

    def stop_shouting_at(self, member): #Remove user from list of users to wake up
        if member in self.SHOUT_AT:
            self.SHOUT_AT.remove(member)

    @discord.ext.tasks.loop(minutes = 30.0)
    async def status_loop(self): #Change discord status of the bot once in a while
        await self.RAKBOT.change_presence(activity = discord.Game(name = random.choice([
            f"monitoring {len(self.RAKBOT.guilds)} servers",
            "with a ban hammer"
        ])))

    @status_loop.before_loop
    async def before_status_loop(self): #Make the status loop wait for the bot to get ready to work
        await self.RAKBOT.wait_until_ready()

    @discord.ext.tasks.loop(seconds = 1.0)
    async def shout_loop(self): #Loop that tries to wake up certain list of users
        for member in self.SHOUT_AT:
            await member.send("Hey, wake up") #TODO

    @shout_loop.before_loop
    async def before_shout_loop(self):
        await self.RAKBOT.wait_until_ready()
