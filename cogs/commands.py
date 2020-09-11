import discord, discord.ext.commands, discord.ext.tasks, asyncio # Discord API Wrapper, Commands Framework, Background loop Framework and Asyncio library
import re, random, num2words # Other stuff
import cogs.rakbotbase # Basic cog

class Tools(discord.ext.commands.Cog): # Admin tools stuff
    def __init__(self, RAKBOT):
        self.RAKBOT = RAKBOT

    @discord.ext.commands.command(pass_context = True)
    async def wypierdalaj(self, ctx): # Turn off comand
        if ctx.author.id == 298139663560998924: # If mom
            await ctx.send(f"Dobrze mamo :c")
            print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ Mame kazała wypierdalać")
            
            await asyncio.sleep(3) # Wait 3 seconds
            await ctx.send(f"PS. Komenda zjebana, patrz: https://github.com/Rapptz/discord.py/search?q=logout&type=Issues")
            # await self.RAKBOT.close() # Turn off
        else: # If not mom
            await ctx.send(f"{random.choice(['Nie', 'Sam spierdalaj', 'XD'])}") # Random insults
            print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) sie wkurwił")

class Fun(discord.ext.commands.Cog): # Fun stuff
    def __init__(self, RAKBOT):
        self.RAKBOT = RAKBOT

    @discord.ext.commands.command(pass_context = True)
    async def saper(self, ctx, size: str = None, level: str = None): # Minesweeper minigame command
        if size not in ["tiny", "small", "medium", "big", "large", "random", "t", "s", "m", "b", "l", "r"]:
            await ctx.send(f"{ctx.author.mention}\n`//saper <size> <level>`")
            print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) failed to play minesweeper")
        elif level not in ["basic", "easy", "normal", "hard", "insane", "random", "b", "e", "n", "h", "i", "r"]:
            await ctx.send(f"{ctx.author.mention}\n`//saper <size> <level>`")
            print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) failed to play minesweeper")
        else: # If size and level are valid
            warning = 0
            grid = [[]]
            message = ""

            if size in ["random", "r"]: # If they are random then roll
                size = random.choice(["t", "s", "m", "b", "l"])
            if level in ["random", "r"]:
                level = random.choice(["b", "e", "n", "h", "i"])

            if size in ["tiny", "t"]: # Assign numerical value to size
                size = 5
            elif size in ["small", "s"]:
                size = 10
            elif size in ["medium", "m"]:
                size = 15
            elif size in ["big", "b"]:
                size = 20
            elif size in ["large", "l"]:
                size = 25

            for y in range(0, size): # Generate empty grid for given size
                for x in range(0, size):
                    grid[y].append(None)
                if y < size-1:
                    grid.append([])

            if level in ["basic", "b"]: # Calculate the amount of bombs
                level = round(size/4)
            elif level in ["easy", "e"]:
                level = round(size/2)
            elif level in ["normal", "n"]:
                level = size
            elif level in ["hard", "h"]:
                level = size*2
            elif level in ["insane", "i"]:
                level = size*4

            for i in range(0, level): # Generate random bombs on the grid
                grid[random.randint(0, size-1)][random.randint(0, size-1)] = "||:crab:||"

            for y in range(0, size): 
                for x in range(0, size):
                    if grid[y][x] == None: # If no bomb in this spot
                        for looky in range (y-1, y+2): # Look around the spot (y axis)
                            if looky >= 0 and looky < size: # If it's not off the grid (y axis)
                                for lookx in range(x-1, x+2):  # Look around the spot (x axis)
                                    if lookx >= 0 and lookx < size and grid[looky][lookx] == "||:crab:||": # If not off the grid (x axis) and there is a bomb
                                        warning += 1 # Count the bombs
                        grid[y][x] = f"||:{num2words.num2words(warning)}:||" # Add number to the grid
                        warning = 0 # Reset bomb count

            amount = size/5 # Amount of messages needed
            count = 1 # How many messages was sent
            for y in range(0, size):
                for x in range(0, size):
                    message += grid[y][x] # Generate message from the grid
                if y+1 == (size/amount)*count: # If message is full
                    await ctx.send(message) # Send it
                    count += 1 # Count it
                    message = "" # Clear it
                else:
                    message += "\n" # New line

            bombs = [round(size/4), round(size/2), size, size*2, size*4] # Bomb anount index
            difficulty = ((-0.2*size+6)*(4*(bombs.index(level)+1))+(4*(bombs.index(level)*(0.2*size-1)))-(0.2*size-1)) # Difficulty calculation
            if difficulty%10 == 0: # Divide difficulty /10
                difficulty = int(difficulty/10) 
            else:
                difficulty = difficulty/10
            
            message = f"Difficulty: ||{difficulty}||/10" # Difficulty message
            await ctx.send(message)
            print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) plays minesweeper")

class DnD(discord.ext.commands.Cog): # Dungeons & Dragons stuff
    def __init__(self, RAKBOT):
        self.RAKBOT = RAKBOT

    @discord.ext.commands.command(pass_context = True)
    async def dice(self, ctx, dice: str, bonus = None): # Dice roll command
        dice = dice.lower() # Dice to lowercase
        results = []
        message = ""

        if dice[0] == "k" or dice[0] == "d": # If dice starts with k or d
            dice = "1"+dice # Add 1 in front

        if re.match("((^([1-9])[0-9]*)([k, d])([1-9][0-9]*)$)", dice): # If dice is <any number><k or d><any number>
            for s in ["k", "d"]: # Repeat for k and d
                if len(dice.split(s)) == 2: # If it can be splitted
                    dice = dice.split(s) # Split dice in the spot of k or d
                    dice[0] = int(dice[0]) # Parse int (amount of dices)
                    dice[1] = int(dice[1]) # Parse int (dice type)
                    break

            for i in range(0, dice[0]): # For the amount of dices
                results.append(random.randint(1, dice[1])) # Roll a dice and add to result table

            if bonus != None: # If there is a bonus
                bonus = bonus.lower() # Bonus to lowercase
                if bonus in ["a", "adv", "advantage", "d", "disadv", "disadvantage"]: # If bonus is valid
                    bonus_results = []
                    for i in range(0, dice[0]): # For the amount of dices
                        bonus_results.append(random.randint(1, dice[1])) # Roll a dice and add to bonus result table

                    for i in range(0, len(results)): # For the amount of results pairs
                        if bonus[0] == "a": # If advantage
                            if results[i] > bonus_results[i]: # Add results to message and bold better result from the pair
                                message += "**"+str(results[i])+"** "+str(bonus_results[i])+"\n"
                            else:
                                message += str(results[i])+" **"+str(bonus_results[i])+"**\n"
                        elif bonus[0] == "d": # If disadvantage
                            if results[i] < bonus_results[i]: # Add results to message and bold worse result from the pair
                                message += "**"+str(results[i])+"** "+str(bonus_results[i])+"\n"
                            else:
                                message += str(results[i])+" **"+str(bonus_results[i])+"**\n"
                    await ctx.send(f"{message}{ctx.author.mention}")
                    print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) rolled a dice")
                else:
                    await ctx.send(f"{ctx.author.mention} Invalid bonus")
                    print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) failed to roll a dice")
                    
            else: # If there is no bonus
                for i in results: # For the amount of results
                    message += "**"+str(i)+"**\n" # Add them to message
                    await ctx.send(f"{message}{ctx.author.mention}")
                    print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) rolled a dice")
        else:
            await ctx.send(f"{ctx.author.mention} Invalid dice")
            print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) failed to roll a dice")
    
    @dice.error
    async def dice_error(self, ctx, error): # Dice roll command error
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention}\n`//dice <amount of dices><k/d><type of dice> <dis/advantage>*`")
            print(f"[{cogs.rakbotbase.Functions().log_time()}] ~ {ctx.author.display_name} ({ctx.author}) failed to roll a dice")
