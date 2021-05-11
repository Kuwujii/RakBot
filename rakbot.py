import discord, discord.ext.commands, discord.ext.tasks, asyncio #Discord API Wrapper, Commands Framework, Background loop Framework and Asyncio library
import pymongo #MongoDB controller
import configparser, pathlib, random #Other stuff
import cogs.rakbotbase #Base cog

def main(): #Main function
    ini = configparser.ConfigParser()
    ini.read(pathlib.Path(__file__).parent.absolute()/"rakbot.ini") #Open ini

    MONGO = pymongo.MongoClient(ini.get("Database", "MongoConnectionString")) #connect to the given database
    database = MONGO[ini.get("Database", "DatabaseName")]
    SERVER_SETTINGS = database[ini.get("Database", "ServerSettingsCollectionName")]

    RAKBOT = discord.ext.commands.Bot(ini.get("General", "CommandPrefix"), help_command = None) #Decare the bot         
    RAKBOT.add_cog(cogs.rakbotbase.RakBotBase(RAKBOT, MONGO, SERVER_SETTINGS))
    
    asyncio.get_event_loop().run_until_complete(RAKBOT.start(ini.get("General", "Token"))) #Login

if __name__ == "__main__":
    main()
