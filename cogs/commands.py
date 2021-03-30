import discord, discord.ext.commands, discord.ext.tasks, asyncio #Discord API Wrapper, Commands Framework, Background loop Framework and Asyncio library
import re, random, num2words #Other stuff
import cogs.rakbotbase #Basic cog

class Tools(discord.ext.commands.Cog): #Admin tools stuff
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
        print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ Got angry and tried to turn me off")

class Fun(discord.ext.commands.Cog): #Fun stuff
    def __init__(self, RAKBOT):
        self.RAKBOT = RAKBOT

    @discord.ext.commands.command(pass_context = True, aliases = ["ms"])
    async def minesweeper(self, ctx, size: str = None, level: str = None): #Minesweeper minigame command
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
                level = round(size/4)
            elif level in ["easy", "e"]:
                level = round(size/2)
            elif level in ["normal", "n"]:
                level = size
            elif level in ["hard", "h"]:
                level = size*2
            elif level in ["insane", "i"]:
                level = size*4

            for i in range(0, level): #Generate random bombs on the grid
                grid[random.randint(0, size-1)][random.randint(0, size-1)] = "||:crab:||"

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

            #TODO fix this to give correct numbers

            # bombs = [round(size/4), round(size/2), size, size*2, size*4] #Bomb anount index
            # difficulty = ((-0.2*size+6)*(4*(bombs.index(level)+1))+(4*(bombs.index(level)*(0.2*size-1)))-(0.2*size-1)) #Difficulty calculation

            # if difficulty%10 == 0: #Divide difficulty /10
            #     difficulty = int(difficulty/10) 
            # else:
            #     difficulty = difficulty/10
            
            # message = f"Difficulty: ||{difficulty}||/10" #Difficulty message
            # await ctx.send(message)
            print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) plays minesweeper")
    
    @minesweeper.error
    async def minesweeper_error(self, ctx): #If off failed
        await ctx.send(f"{ctx.author.mention}\n`//saper <size> <level>`")
        print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) failed to play minesweeper")

class DnD(discord.ext.commands.Cog): #Dungeons & Dragons stuff
    def __init__(self, RAKBOT):
        self.RAKBOT = RAKBOT

    @discord.ext.commands.command(pass_context = True)
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
            await ctx.send(f"{ctx.author.mention}\n`//dice <amount of dices><k/d><type of dice> <dis/advantage>*`")
            print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) failed to roll a dice")
