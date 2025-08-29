import discord, discord.ext.commands, discord.ext.tasks, asyncio #Discord API Wrapper, Commands Framework, Background loop Framework and Asyncio library
import time, glob, os, zipfile, json, pathlib #Other stuff
import cogs.tasks, cogs.events, cogs.commands #Other cogs

START_TIME = time.strftime("%d-%m-%Y_%H-%M-%S")

class RakBotBase(discord.ext.commands.Cog): #Define cog class
    def __init__(self, RAKBOT, MONGO, SERVER_SETTINGS):
        self.RAKBOT = RAKBOT
        self.MONGO = MONGO
        self.SERVER_SETTINGS = SERVER_SETTINGS

        Functions().init_log_file()

    @discord.ext.commands.Cog.listener() #On ready event
    async def on_ready(self):
        # for g in self.RAKBOT.guilds:
        #     self.RAKBOT.tree.clear_commands(guild = g)
        #     await self.RAKBOT.tree.sync(guild = g)

        await self.RAKBOT.add_cog(cogs.tasks.Background(self.RAKBOT)) #Run other cogs
        
        await self.RAKBOT.add_cog(cogs.events.Events(self.RAKBOT, self.SERVER_SETTINGS))
        
        await self.RAKBOT.add_cog(cogs.commands.Tools(self.RAKBOT, self.MONGO, self.SERVER_SETTINGS))
        # await self.RAKBOT.add_cog(cogs.commands.Fun(self.RAKBOT))
        # await self.RAKBOT.add_cog(cogs.commands.Dnd(self.RAKBOT))

        await self.RAKBOT.tree.sync()

        await self.RAKBOT.wait_until_ready()
        cogs.rakbotbase.Functions().write_log(f"Running {self.RAKBOT.user.name} on RakBot core v0.0.2")

class Functions(): #Usefull functions
    def __init__(self):
        pass

    def log_time(self): #Current time for console logs
        return time.strftime("%d-%m-%Y %H:%M:%S")

    def init_log_file(self): #Prepare new log file for the session
        try: #Create log dir if it doesn't exist
            os.chdir(pathlib.Path(__file__).parent.absolute()/"../logs")
        except FileNotFoundError as e:
            os.mkdir(pathlib.Path(__file__).parent.absolute()/"../logs")
            os.chdir(pathlib.Path(__file__).parent.absolute()/"../logs")

        for file in glob.glob("*.log"): #Zip old log files
            zipfile.ZipFile(f"{file[:-4]}.zip", mode="w").write(file)
            os.remove(file)

        log_file = open(f"{START_TIME}.log", "a") #Create the file
        log_file.close()

    def write_log(self, log_text): #Write logs to the file and print them on the console
        log_text = f"[{Functions().log_time()}] ~ {log_text}"
        
        log_file = open(f"{START_TIME}.log", "a")
        log_file.write(f"{log_text}\n")
        log_file.close()

        print(log_text)
