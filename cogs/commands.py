import discord, discord.ext.commands, discord.ext.tasks, asyncio #Discord API Wrapper, Commands Framework, Background loop Framework and Asyncio library
import json, glob, os, re, random, num2words #Other stuff
import cogs.rakbotbase #Basic cog

class Tools(discord.ext.commands.Cog): #Admin tools stuffS
    def __init__(self, RAKBOT, MONGO, SERVER_SETTINGS):
        self.RAKBOT = RAKBOT
        self.MONGO = MONGO
        self.SERVER_SETTINGS = SERVER_SETTINGS

    @discord.ext.commands.command(pass_context = True, 
    aliases = list(set([ #Remove duplicates and assign them
        json.load(open(f"./lang/{lang_file_name}"))["tools"]["off"]["name"] for lang_file_name in os.listdir("./lang") 
            if json.load(open(f"./lang/{lang_file_name}"))["tools"]["off"]["name"] != "off" #Generate a list of names from all languages. Exclude default name
    ] + [ #Merge the two lists
        alias for lang_file_name in os.listdir("./lang") 
            for alias in json.load(open(f"./lang/{lang_file_name}"))["tools"]["off"]["aliases"] #Generate a list of aliases from all languages
    ])))
    @discord.ext.commands.is_owner() #If owner
    async def off(self, ctx): #Turn off comand
        file = open(f"../lang/{self.SERVER_SETTINGS.find_one({'_id': ctx.guild.id})['language']}.json") #Get server language
        await ctx.send(json.load(file)["tools"]["off"]["message"]) #Send correct message
        file.close()

        cogs.rakbotbase.Functions().write_log("Turning off") #Send logs

        self.MONGO.close() #Close connection to the database
        await self.RAKBOT.close() #Turn off the bot

    @off.error
    async def off_error(self, ctx): #If off failed
        file = open(f"../lang/{self.SERVER_SETTINGS.find_one({'_id': ctx.guild.id})['language']}.json") #Get server language
        await ctx.send(json.load(file)["tools"]["off"]["error"]) #Send correct message
        file.close()

        cogs.rakbotbase.Functions().write_log(f"{ctx.author.display_name} ({ctx.author}) got angry and tried to turn me off")

    @discord.ext.commands.group(pass_context = True, invoke_without_command = True,
    aliases = list(set([ #Remove duplicates and assign them
        json.load(open(f"./lang/{lang_file_name}"))["tools"]["language"]["name"] for lang_file_name in os.listdir("./lang") 
            if json.load(open(f"./lang/{lang_file_name}"))["tools"]["language"]["name"] != "language" #Generate a list of names from all languages. Exclude default name
    ] + [ #Merge the two lists
        alias for lang_file_name in os.listdir("./lang") 
            for alias in json.load(open(f"./lang/{lang_file_name}"))["tools"]["language"]["aliases"] #Generate a list of aliases from all languages
    ])))
    async def language(self, ctx): #Check the language of the server
        file = open(f"../lang/{self.SERVER_SETTINGS.find_one({'_id': ctx.guild.id})['language']}.json") #Get server language
        await ctx.send(json.load(file)["tools"]["language"]["message"]) #Send correct message
        file.close()

        cogs.rakbotbase.Functions().write_log(f"{ctx.author.display_name} ({ctx.author}) checked the language of the {ctx.guild.name} server")

    @language.command(pass_context = True, name = "list",
    aliases = list(set([ #Remove duplicates and assign them
        json.load(open(f"./lang/{lang_file_name}"))["tools"]["language"]["list"]["name"] for lang_file_name in os.listdir("./lang") 
            if json.load(open(f"./lang/{lang_file_name}"))["tools"]["language"]["list"]["name"] != "list" #Generate a list of names from all languages. Exclude default name
    ] + [ #Merge the two lists
        alias for lang_file_name in os.listdir("./lang") 
            for alias in json.load(open(f"./lang/{lang_file_name}"))["tools"]["language"]["list"]["aliases"] #Generate a list of aliases from all languages
    ])))
    @discord.ext.commands.has_permissions(administrator = True)
    async def language_list(self, ctx): #Check all the available languages
        e = discord.Embed(colour = 0xFF6D00) #Declare embed

        file = open(f"../lang/{self.SERVER_SETTINGS.find_one({'_id': ctx.guild.id})['language']}.json") #Get server language
        e.set_author(name = json.load(file)["tools"]["language"]["list"]["message"], icon_url = self.RAKBOT.user.avatar_url)
        file.close()

        for lang_file_name in os.listdir("../lang"): #Loop through all the languages
            lang_file = open(f"../lang/{lang_file_name}")
            lang_data = json.load(lang_file)

            e.add_field(name = f"{lang_data['icon']} {lang_data['language']} ({lang_data['region']})", value = f"`{lang_file_name[:-5]}`", inline = False)

            lang_file.close()

        await ctx.send(embed = e) #Send it
        cogs.rakbotbase.Functions().write_log(f"{ctx.author.display_name} ({ctx.author}) asked for list of languages")

    @language.command(pass_context = True, name = "set",
    aliases = list(set([ #Remove duplicates and assign them
        json.load(open(f"./lang/{lang_file_name}"))["tools"]["language"]["set"]["name"] for lang_file_name in os.listdir("./lang") 
            if json.load(open(f"./lang/{lang_file_name}"))["tools"]["language"]["set"]["name"] != "set" #Generate a list of names from all languages. Exclude default name
    ] + [ #Merge the two lists
        alias for lang_file_name in os.listdir("./lang") 
            for alias in json.load(open(f"./lang/{lang_file_name}"))["tools"]["language"]["set"]["aliases"] #Generate a list of aliases from all languages
    ])))
    @discord.ext.commands.has_permissions(administrator = True)
    async def language_set(self, ctx, language: str): #Set the language for the current server
        if f"{language}.json" in os.listdir("../lang"): #If the language exists
            self.SERVER_SETTINGS.update_one({"_id": ctx.guild.id}, {"$set": {"language": language}}) #Change the value in the database

            file = open(f"../lang/{language}.json")
            await ctx.send(json.load(file)["tools"]["language"]["set"]["message"])
            file.close()

            cogs.rakbotbase.Functions().write_log(f"{ctx.author.display_name} ({ctx.author}) set a new language for the server {ctx.guild.name}")
        else:
            file = open(f"../lang/{self.SERVER_SETTINGS.find_one({'_id': ctx.guild.id})['language']}.json") #Get server language
            await ctx.send(json.load(file)["tools"]["language"]["set"]["error"])
            file.close()

            cogs.rakbotbase.Functions().write_log(f"{ctx.author.display_name} ({ctx.author}) failed to set a new language for the server {ctx.guild.name}")

    @discord.ext.commands.command(pass_context = True, name = "shout")
    async def shout(self, ctx, member: discord.Member):
        self.RAKBOT.get_cog("Background").start_shouting_at(member)
        await ctx.send(f"Hey {member.mention}, wake up!")
        cogs.rakbotbase.Functions().write_log(f"{ctx.author.display_name} ({ctx.author}) shouts at {member.display_name} ({member})")

    @discord.ext.commands.command(pass_context = True, name = "quiet")
    async def quiet(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
            await ctx.send("Ok")
            cogs.rakbotbase.Functions().write_log(f"{ctx.author.display_name} ({ctx.author}) showed up and wanted me to stop shouting")
        else:
            await ctx.send(f"Hey {member.mention}, no need to wake up anymore")
            cogs.rakbotbase.Functions().write_log(f"{ctx.author.display_name} ({ctx.author}) stops shouting at {member.display_name} ({member})")
        self.RAKBOT.get_cog("Background").stop_shouting_at(member)

    @discord.ext.commands.group(pass_context = True, invoke_without_command = True)
    async def help(self, ctx): #General help command
        e = discord.Embed(colour = 0xFF6D00) #Declare embed
        e.set_author(name = "RakBot commands help", icon_url = self.RAKBOT.user.avatar_url)

        for cog in self.RAKBOT.cogs:
            if self.RAKBOT.get_cog(cog).get_commands() != []:
                e.add_field(name = cog, value = f"`//help {cog.lower()}`", inline = True) #Generate embed field for every cog containing commands

        await ctx.send(embed = e)
        cogs.rakbotbase.Functions().write_log(f"{ctx.author.display_name} ({ctx.author}) asked for help")

    @help.command(pass_context = True, name = "tools")
    async def help_tools(self, ctx): #Tools cog help command
        e = discord.Embed(colour = 0xFF6D00) #Declare embed
        e.set_author(name = "Tools commands usage", icon_url = self.RAKBOT.user.avatar_url)

        for command in self.RAKBOT.get_cog("Tools").get_commands():
            e.add_field(name = command.name.capitalize(), value = f"```css\n //{command} {command.description}```", inline = False) #Generate embed field for every command in cog

        await ctx.send(embed = e)
        cogs.rakbotbase.Functions().write_log(f"{ctx.author.display_name} ({ctx.author}) asked for help with tools commands")

    @help.command(pass_context = True, name = "fun")
    async def help_fun(self, ctx): #Fun cog help command
        e = discord.Embed(colour = 0xFF6D00) #Declare embed
        e.set_author(name = "Fun commands usage", icon_url = self.RAKBOT.user.avatar_url)

        for command in self.RAKBOT.get_cog("Fun").get_commands():
            e.add_field(name = command.name.capitalize(), value = f"```css\n //{command} {command.description}```", inline = False) #Generate embed field for every command in cog

        await ctx.send(embed = e)
        cogs.rakbotbase.Functions().write_log(f"{ctx.author.display_name} ({ctx.author}) asked for help with fun commands")

    @help.command(pass_context = True, name = "dnd")
    async def help_dnd(self, ctx): #DnD cog help command
        e = discord.Embed(colour = 0xFF6D00) #Declare embed
        e.set_author(name = "DnD commands usage", icon_url = self.RAKBOT.user.avatar_url)

        for command in self.RAKBOT.get_cog("DnD").get_commands():
            e.add_field(name = command.name.capitalize(), value = f"```css\n //{command} {command.description}```", inline = False) #Generate embed field for every command in cog

        await ctx.send(embed = e)
        cogs.rakbotbase.Functions().write_log(f"{ctx.author.display_name} ({ctx.author}) asked for help with DnD commands")

class Fun(discord.ext.commands.Cog): #Fun stuff
    def __init__(self, RAKBOT):
        self.RAKBOT = RAKBOT

    @discord.ext.commands.command(pass_context = True, aliases = ["ms"], description = "<size> <level>")
    async def minesweeper(self, ctx, size: str, level: str): #Minesweeper minigame command
        size, level = size.lower(), level.lower() #To lowercase

        sizes = ["small", "medium", "large", "random", "s", "m", "l", "r"]
        levels = ["basic", "easy", "normal", "hard", "insane", "random", "b", "e", "n", "h", "i", "r"]

        if size in levels and level in sizes:
            size, level = level, size

        if (size not in sizes) or (level not in levels):
            await ctx.send(f"{ctx.author.mention}\n`//saper <size> <level>`")
            cogs.rakbotbase.Functions().write_log(f"{ctx.author.display_name} ({ctx.author}) failed to play minesweeper")
        else: #If size and level are valid
            warning = 0
            grid = [[]]
            message = ""
            planted = 0

            if size in ["random", "r"]: #If they are random then roll
                size = random.choice(["s", "m", "l"])
            if level in ["random", "r"]:
                level = random.choice(["b", "e", "n", "h", "i"])

            if size in ["small", "s"]: #Assign numerical value to size
                size = 5
            elif size in ["medium", "m"]:
                size = 10
            elif size in ["large", "l"]:
                size = 15

            for y in range(0, size): #Generate empty grid for given size
                for x in range(0, size):
                    grid[y].append(None)
                if y < size-1:
                    grid.append([])

            if level in ["basic", "b"]: #Calculate the amount of bombs
                level = round((size**2)/14)
            elif level in ["easy", "e"]:
                level = round((size**2)/10)
            elif level in ["normal", "n"]:
                level = round((size**2)/7)
            elif level in ["hard", "h"]:
                level = round((size**2)/5)
            elif level in ["insane", "i"]:
                level = round((size**2)/4)

            while planted < level: #Generate random bombs on the grid
                random_x = random.randint(0, size-1)
                random_y = random.randint(0, size-1)

                if grid[random_x][random_y] != "||:crab:||":
                    grid[random_x][random_y] = "||:crab:||"
                    planted += 1

            for y in range(0, size): 
                for x in range(0, size):
                    if grid[y][x] == None: #If no bomb in this spot
                        for looky in range (y-1, y+2): #Look around the spot (y axis)
                            if looky >= 0 and looky < size: #If it's not off the grid (y axis)
                                for lookx in range(x-1, x+2):  #Look around the spot (x axis)
                                    if lookx >= 0 and lookx < size and grid[looky][lookx] == "||:crab:||": #If not off the grid (x axis) and there is a bomb
                                        warning += 1 #Count the bombs
                        grid[y][x] = f"||:{num2words.num2words(warning)}:||" #Add number to the grid
                        warning = 0 #Reset bomb count

            amount = size/5 #Amount of messages needed
            count = 1 #How many messages was sent

            for y in range(0, size):
                for x in range(0, size):
                    message += grid[y][x] #Generate message from the grid
                if y+1 == (size/amount)*count: #If message is full
                    await ctx.send(message) #Send it
                    count += 1 #Count it
                    message = "" #Clear it
                else:
                    message += "\n" #New line
            
            cogs.rakbotbase.Functions().write_log(f"{ctx.author.display_name} ({ctx.author}) plays minesweeper")
    
    @minesweeper.error
    async def minesweeper_error(self, ctx, error): #If off failed
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention}\n`//saper <size> <level>`")
            cogs.rakbotbase.Functions().write_log(f"{ctx.author.display_name} ({ctx.author}) failed to play minesweeper")

class Dnd(discord.ext.commands.Cog, name = "DnD"): #Dungeons & Dragons stuff
    def __init__(self, RAKBOT):
        self.RAKBOT = RAKBOT

    @discord.ext.commands.command(pass_context = True, description = "[amount]<k/d><sides>[+multiplier] [dis/advantage]")
    async def dice(self, ctx, dice: str, bonus = None): #Dice roll command
        dice = dice.lower() #Dice to lowercase
        results = []
        message = ""

        if dice[0] == "k" or dice[0] == "d": #If dice starts with k or d
            dice = "1"+dice #Add 1 in front

        if "+" not in dice: #If no modifier add modifier 0
            dice = dice+"+0"

        if re.match("(^([1-9][0-9]*)([k, d])([1-9][0-9]*)([+])([0-9]*)$)", dice): #If dice is <any number><k or d><any number><+><any number>
            for kd in ["k", "d"]: #Repeat for k and d
                if len(dice.split(kd)) == 2: #If it can be splitted
                    dice = dice.split(kd) #Split dice in the spot of k or d
                    damount = int(dice[0]) #Parse int (amount of dices)
                    dtype_n_dmodifier = dice[1] #Save dice type and modifier
                    if len(dtype_n_dmodifier.split("+")) == 2: #If it can be splitted
                        dtype_n_dmodifier = dtype_n_dmodifier.split("+") #Split dice in the spot of +
                        dtype = int(dtype_n_dmodifier[0]) #Parse int (dice type)
                        dmodifier = int(dtype_n_dmodifier[1]) #Parse int (dice modifier)
                    break

            for i in range(0, damount): #For the amount of dices
                results.append(random.randint(1, dtype)+dmodifier) #Roll a dice, add modifier and add to result table

            if bonus != None: #If there is a bonus
                bonus = bonus.lower() #Bonus to lowercase
                if bonus in ["a", "adv", "advantage", "d", "dis", "disadvantage"]: #If bonus is valid
                    bonus_results = []
                    for i in range(0, damount): #For the amount of dices
                        bonus_results.append(random.randint(1, dtype)+dmodifier) #Roll a dice, add modifier and add to bonus result table

                    for i in range(0, len(results)): #For the amount of results pairs
                        if bonus[0] == "a": #If advantage
                            if results[i] > bonus_results[i]: #Add results to message and bold better result from the pair
                                message += "**"+str(results[i])+"** "+str(bonus_results[i])+"\n"
                            else:
                                message += str(results[i])+" **"+str(bonus_results[i])+"**\n"
                        elif bonus[0] == "d": #If disadvantage
                            if results[i] < bonus_results[i]: #Add results to message and bold worse result from the pair
                                message += "**"+str(results[i])+"** "+str(bonus_results[i])+"\n"
                            else:
                                message += str(results[i])+" **"+str(bonus_results[i])+"**\n"
                    await ctx.send(f"{message}{ctx.author.mention}")
                    cogs.rakbotbase.Functions().write_log(f"{ctx.author.display_name} ({ctx.author}) rolled a dice")
                else:
                    await ctx.send(f"{ctx.author.mention} Invalid bonus")
                    cogs.rakbotbase.Functions().write_log(f"{ctx.author.display_name} ({ctx.author}) failed to roll a dice")
                    
            else: #If there is no bonus
                for i in results: #For the amount of results
                    message += "**"+str(i)+"**\n" #Add them to message
                await ctx.send(f"{message}{ctx.author.mention}")
                cogs.rakbotbase.Functions().write_log(f"{ctx.author.display_name} ({ctx.author}) rolled a dice")
        else:
            await ctx.send(f"{ctx.author.mention} Invalid dice")
            cogs.rakbotbase.Functions().write_log(f"{ctx.author.display_name} ({ctx.author}) failed to roll a dice")
    
    @dice.error
    async def dice_error(self, ctx, error): #Dice roll command error
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention}\n`//dice <amount of dices><k/d><type of dice>+<multiplier> <dis/advantage>`")
            cogs.rakbotbase.Functions().write_log(f"{ctx.author.display_name} ({ctx.author}) failed to roll a dice")

    @discord.ext.commands.command(pass_context = True, aliases = ["gs"])
    async def generateStats(self, ctx): #Generate random stats command
        results = []
        message = ""

        for stat in range(0, 6): #For each stat
            results.append([random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)]) #Roll 4 times
            trimmed = results[stat].copy()
            trimmed.remove(min(trimmed)) #Get 3 highest results
            trim_sum = 0

            message += f"{min(results[stat])} " #Add the lowest to the message

            for roll in trimmed:
                trim_sum += roll #Sum the highest rolls
                message += f"**{roll}** " #Add them to the message

            message += f"= {trim_sum}\n" #Add the sum to the message

        total = 0

        for roll in range(0, 24): #Get the total roll score
            total += results[int(roll/4)][int(roll%4)]

        message += f"Total: {total}" #Finish the message

        await ctx.send(f"{ctx.author.mention}\n{message}")
        cogs.rakbotbase.Functions().write_log(f"{ctx.author.display_name} ({ctx.author}) generated DnD stats")
    
    @generateStats.error
    async def generateStats_error(self, ctx, error): #Stat generation command error
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention}\n`//genstats*`")
            cogs.rakbotbase.Functions().write_log(f"{ctx.author.display_name} ({ctx.author}) failed to generate DnD stats")
