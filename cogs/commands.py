import discord, discord.ext.commands, discord.ext.tasks, asyncio #Discord API Wrapper, Commands Framework, Background loop Framework and Asyncio library
import re, random, num2words #Other stuff
import cogs.rakbotbase #Basic cog

class Tools(discord.ext.commands.Cog): #Admin tools stuffS
    def __init__(self, RAKBOT):
        self.RAKBOT = RAKBOT

    @discord.ext.commands.command(pass_context = True)
    @discord.ext.commands.is_owner() #If owner
    async def off(self, ctx): #Turn off comand
        await ctx.send(f"Turning off now")
        print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ Turning off")
        await self.RAKBOT.close() #Turn off

    @off.error
    async def off_error(self, ctx): #If off failed
        await ctx.send(f"You're not permited to do this")
        print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) got angry and tried to turn me off")

    @discord.ext.commands.group(pass_context = True, invoke_without_command = True)
    async def help(self, ctx): #General help command
        e = discord.Embed(colour = 0xFF6D00) #Declare embed
        e.set_author(name = "RakBot commands help", icon_url = self.RAKBOT.user.avatar_url)

        for cog in self.RAKBOT.cogs:
            if self.RAKBOT.get_cog(cog).get_commands() != []:
                e.add_field(name = cog, value = f"`//help {cog.lower()}`", inline = True) #Generate embed field for every cog containing commands

        await ctx.send(embed = e)
        print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) asked for help")

    @help.command(pass_context = True)
    async def tools(self, ctx): #Tools cog help command
        e = discord.Embed(colour = 0xFF6D00) #Declare embed
        e.set_author(name = "Tools commands usage", icon_url = self.RAKBOT.user.avatar_url)

        for command in self.RAKBOT.get_cog("Tools").get_commands():
            e.add_field(name = command.name.capitalize(), value = f"```css\n //{command} {command.description}```", inline = False) #Generate embed field for every command in cog

        await ctx.send(embed = e)
        print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) asked for help with tools commands")

    @help.command(pass_context = True)
    async def fun(self, ctx): #Fun cog help command
        e = discord.Embed(colour = 0xFF6D00) #Declare embed
        e.set_author(name = "Fun commands usage", icon_url = self.RAKBOT.user.avatar_url)

        for command in self.RAKBOT.get_cog("Fun").get_commands():
            e.add_field(name = command.name.capitalize(), value = f"```css\n //{command} {command.description}```", inline = False) #Generate embed field for every command in cog

        await ctx.send(embed = e)
        print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) asked for help with fun commands")

    @help.command(pass_context = True)
    async def dnd(self, ctx): #DnD cog help command
        e = discord.Embed(colour = 0xFF6D00) #Declare embed
        e.set_author(name = "DnD commands usage", icon_url = self.RAKBOT.user.avatar_url)

        for command in self.RAKBOT.get_cog("DnD").get_commands():
            e.add_field(name = command.name.capitalize(), value = f"```css\n //{command} {command.description}```", inline = False) #Generate embed field for every command in cog

        await ctx.send(embed = e)
        print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) asked for help with DnD commands")

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

        if size not in sizes:
            await ctx.send(f"{ctx.author.mention}\n`//saper <size> <level>`")
            print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) failed to play minesweeper")
        elif level not in levels:
            await ctx.send(f"{ctx.author.mention}\n`//saper <size> <level>`")
            print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) failed to play minesweeper")
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
            
            #TODO fix
            # difficulty = round((size*(3472/135)) + (level*(91/4)) + ((size*level)*(-91/540)) + (round(level/size)*(-1547/108)) + (round((size+level)/2)*(-4145/108)))/10

            # if difficulty%1 == 0:
            #     difficulty = int(difficulty)

            # message = f"Difficulty: ||{difficulty}||/10" #Difficulty message
            # await ctx.send(message)
            print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) plays minesweeper")
    
    @minesweeper.error
    async def minesweeper_error(self, ctx, error): #If off failed
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention}\n`//saper <size> <level>`")
            print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) failed to play minesweeper")

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
                    print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) rolled a dice")
                else:
                    await ctx.send(f"{ctx.author.mention} Invalid bonus")
                    print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) failed to roll a dice")
                    
            else: #If there is no bonus
                for i in results: #For the amount of results
                    message += "**"+str(i)+"**\n" #Add them to message
                await ctx.send(f"{message}{ctx.author.mention}")
                print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) rolled a dice")
        else:
            await ctx.send(f"{ctx.author.mention} Invalid dice")
            print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) failed to roll a dice")
    
    @dice.error
    async def dice_error(self, ctx, error): #Dice roll command error
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention}\n`//dice <amount of dices><k/d><type of dice>+<multiplier> <dis/advantage>`")
            print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) failed to roll a dice")
    
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
        print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) generated DnD stats")
    
    @generateStats.error
    async def generateStats_error(self, ctx, error): #Stat generation command error
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention}\n`//genstats*`")
            print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) failed to generate DnD stats")
