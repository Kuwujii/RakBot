import lightbulb #Discord API Wrapper (hikari) and it's Commands Framework (lightbulb)
import pymongo #MongoDB controller
import configparser, pathlib

RAKBOT = None #Create globals for the bot and database
MONGO = None
SERVER_SETTINGS = None

def main():
    global RAKBOT, MONGO, SERVER_SETTINGS

    ini = configparser.ConfigParser() #Read the config file
    ini.read(pathlib.Path(__file__).parent.absolute()/"rakbot.ini")

    MONGO = pymongo.MongoClient(ini.get("Database", "MongoConnectionString")) #connect to the database
    database = MONGO[ini.get("Database", "DatabaseName")]
    SERVER_SETTINGS = database[ini.get("Database", "ServerSettingsCollectionName")]

    RAKBOT = lightbulb.BotApp(
        ini.get("General", "Token"),
        default_enabled_guilds = int(ini.get("General", "DefauldGuildID")),
        help_slash_command = True,
        prefix = ini.get("General", "CommandPrefix")
    ) #Declare and run the bot

    RAKBOT.run()


if __name__ == "__main__":
    main()
