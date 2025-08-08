import discord, discord.ext.commands, discord.ext.tasks #discord.py, API wrapper
import pymongo #MongoDB controller
import configparser, pathlib
import cogs.rakbotbase

RAKBOT = None #Create globals for the bot and database
MONGO = None
SERVER_SETTINGS = None

class RakBot(discord.ext.commands.Bot):
    async def setup_hook(self):
        await self.add_cog(cogs.rakbotbase.RakBotBase(RAKBOT, MONGO, SERVER_SETTINGS))

def main():
    global RAKBOT, MONGO, SERVER_SETTINGS

    ini = configparser.ConfigParser() #Read the config file
    ini.read(pathlib.Path(__file__).parent.absolute()/"rakbot.ini")

    MONGO = pymongo.MongoClient(ini.get("Database", "MongoConnectionString")) #connect to the database
    database = MONGO[ini.get("Database", "DatabaseName")]
    SERVER_SETTINGS = database[ini.get("Database", "ServerSettingsCollectionName")]

    RAKBOT = RakBot(command_prefix='!', intents = discord.Intents.default(), help_command = None)
    tree = RAKBOT.tree

    RAKBOT.run(ini.get("General", "Token"))

if __name__ == "__main__":
    main()
