import discord, discord.ext.commands, discord.ext.tasks, asyncio #Discord API Wrapper, Commands Framework, Background loop Framework and Asyncio library
import time, glob, os, zipfile #Other stuff
import cogs.tasks, cogs.events, cogs.commands #Other cogs

START_TIME = time.strftime("%d-%m-%Y_%H-%M-%S")

class RakBotBase(discord.ext.commands.Cog): #Define cog class
    def __init__(self, RAKBOT):
        self.RAKBOT = RAKBOT

        Functions().init_log_file()

        self.RAKBOT.add_cog(cogs.tasks.Background(self.RAKBOT)) #Run other cogs
        
        self.RAKBOT.add_cog(cogs.events.Events(self.RAKBOT))
        
        self.RAKBOT.add_cog(cogs.commands.Tools(self.RAKBOT))
        self.RAKBOT.add_cog(cogs.commands.Fun(self.RAKBOT))
        self.RAKBOT.add_cog(cogs.commands.Dnd(self.RAKBOT))

class Functions(): #Usefull functions
    def __init__(self):
        pass

    def log_time(self): #Current time for console logs
        return time.strftime("%d-%m-%Y %H:%M:%S")

    def init_log_file(self): #Prepare new log file for the session
        if os.path.isdir("./logs") == False: #Create log dir if it doesn't exist
            os.mkdir("./logs")

        os.chdir("./logs")

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
