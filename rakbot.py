import lightbulb #Discord API Wrapper (hikari) and it's Commands Framework (lightbulb)
import pymongo #MongoDB controller
import configparser, pathlib, colorlog, logging, time

RAKBOT = None #Create globals for the bot and database
MONGO = None
SERVER_SETTINGS = None

def main():
    global RAKBOT, MONGO, SERVER_SETTINGS

    ini = configparser.ConfigParser() #Read the config file
    ini.read(pathlib.Path(__file__).parent.absolute()/"rakbot.ini")

    MONGO = pymongo.MongoClient(ini.get("Database", "MongoConnectionString")) #connect to the database
    database = MONGO[ini.get("Database", "DatabaseName")]
    SERVER_SETTINGS = database[ini.get("Database", "ServerSettingsCollectionName")] #colorlog.info(f"Running {RAKBOT.get_me().username} on RakBot core v0.0.2")

    RAKBOT = lightbulb.BotApp(
        ini.get("General", "Token"),
        default_enabled_guilds = int(ini.get("General", "DefauldGuildID")),
        help_slash_command = True,
        prefix = ini.get("General", "CommandPrefix"),
        banner = None,
        logs = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "coloured": {
                    "class": "colorlog.ColoredFormatter",
                    "datefmt": "%d/%m/%Y %H:%M:%S",
                    "format": "%(log_color)s[%(levelname)s] %(asctime)s: %(message)s"
                },
                "basic": {
                    "class": "logging.Formatter",
                    "datefmt": "%d/%m/%Y %H:%M:%S",
                    "format": "[%(levelname)s] %(asctime)s: %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "colorlog.StreamHandler",
                    "formatter": "coloured",
                    "level": "DEBUG"
                },
                "file": {
                    "class": "logging.FileHandler",
                    "filename": f"logs\\{time.strftime('%d-%m-%Y_%H-%M-%S')}.log",
                    "formatter": "basic",
                    "level": "DEBUG"
                }
            },
            "root": {
                "handlers": ["console", "file"],
                "level": "DEBUG"
            }
        } #Logger configuration
    ) #Declare and run the bot

    RAKBOT.run()

if __name__ == "__main__":
    main()
