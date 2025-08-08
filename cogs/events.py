import discord, discord.ext.commands, discord.ext.tasks, asyncio #Discord API Wrapper, Commands Framework, Background loop Framework and Asyncio library
import cogs.rakbotbase #Basic cog

class Events(discord.ext.commands.Cog): #Define cog class
    def __init__(self, RAKBOT, SERVER_SETTINGS):
        self.RAKBOT = RAKBOT
        self.SERVER_SETTINGS = SERVER_SETTINGS

    @discord.ext.commands.Cog.listener() #Set default language as British English when joining the server
    async def on_guild_join(self, guild):
        self.SERVER_SETTINGS.insert_one({"_id": guild.id, "language": "en_GB"})
        cogs.rakbotbase.Functions().write_log(f"Got invited to {guild.name} server")

    @discord.ext.commands.Cog.listener() #Remove server settings when kicked from it
    async def on_guild_remove(self, guild):
        self.SERVER_SETTINGS.delete_one({"_id": guild.id})
        cogs.rakbotbase.Functions().write_log(f"Got kicked from {guild.name} server")

    @discord.ext.commands.Cog.listener()
    async def on_message(self, message): #On message seen
        if message.author.bot == False:
            words = message.content.lower().split() #Create array of words in message
            vowels = ['a', 'e', 'i', 'o', 'u', 'y', 'ą', 'ę', 'ó'] #Array of vowels
            line_count = 0 #Syllabes in Haiku line
            line = 1 #Current Haiku line
            output = "" #Output

            for word_og in words: #For each word
                word = word_og 
                word_count = 0 #Syllabes in current word

                if word[0] in vowels: #If word starts with a vowel
                    word_count += 1 #+1 Syllabe

                for i in range(1, len(word)): #For each character in word
                    if word[i] in vowels and word[i-1] not in vowels: #If it's a vowel and the previous one is not a vowel
                        word_count += 1 #+1 Syllabe
                
                if word_count == 0: #If no syllabes
                    word_count = 1 #Syllabes = 1

                if line_count == 0: #If first word in line
                    word = word.capitalize() #Capitalize first letter

                if line in [1, 3] and word_count <= 5: #If 1st or 3rd line and word has less than/just 5 syllabes
                    line_count += word_count #Add word syllabes to line syllabes

                    if line_count < 5: #If line not full
                        output += word+" " #Add to output and continue
                    elif line_count == 5 and line == 1: #If line has 5 syllabes and it's 1st line
                        output += word #Add to output
                        title = (output+".").capitalize() #Create title
                        output += ",\n"
                        line += 1 #Go 2nd line
                        line_count = 0 #Reset syllabes in line
                    elif line_count == 5 and line == 3 and word_og == words[-1]: #If line has 5 syllabes, it's 3rd line and the word is last in the list
                        output += word+"." #Finish output
                        
                        await message.channel.send(f"**{title}**\n\n*{output}*\n     ~ {message.author.mention}") #Send the Hiku
                        cogs.rakbotbase.Functions().write_log(f"{message.author.display_name} ({message.author}) accidentally wrote a Haiku")
                    else: #Else not a Hiku
                        break
            
                elif line == 2 and word_count <= 7: #If 2nd line and word has less than/just 7 syllabes
                    line_count += word_count #Add word syllabes to line syllabes

                    if line_count < 7: #If line has less than 7 syllabes
                        output += word+" " #Add to output
                    elif line_count == 7: #If line has 7 syllabes
                        output += word+",\n" #Add to output
                        line += 1 #Go to 3rd line
                        line_count = 0 #Reset syllabes in line
                    else: #Else not a Haiku
                        break
                else: #Else not a Haiku
                    break
        