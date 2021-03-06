######################################
#current release date:      01/01/2021
#current version:           2.0
######################################

#import modules
import os
from typing import NewType
import discord
from discord.ext import commands
from discord.ext.commands import Bot, bot
from os import listdir
from os.path import isfile, join
import datetime
import importlib
import json


#client const
OSBuid : float = 2.0
Now = datetime.datetime.now()
#Set to True to run on a test server
IsDebug : bool = True


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = ['$']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ? to be used in DMs
        return '$'

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)

bot = commands.Bot(command_prefix=get_prefix, description='Version ' + str(OSBuid))

#load everything
if __name__ == "__main__":
    cogs_dir = "Cogs"
    module_dir = "Modules"
    gbl = globals()

    #load all cogs
    #goes through each file in the cogs directory
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            #tries to load them
            bot.load_extension(cogs_dir + "." + extension)
        except Exception as e:
            #throws an error if it can't
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    
    #load all modules
    #goes through each file in the cogs directory
    for module in [f.replace('.py', '') for f in listdir(module_dir) if isfile(join(module_dir, f))]:
        try:
            #tries to load them
            moduleToImport = module_dir + '.' + module
            gbl[moduleToImport] = importlib.import_module(moduleToImport)
        except Exception as e:
            #throws an error if it can't
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(module, exc))

@bot.event
async def on_ready():
    #gets time and date
    time_date = Now.strftime("%d-%m-%Y %H:%M")
    #print when the bot is ready as well as the date and time for the user
    print("""
    ######################
    #####Starting Bot#####
    ######################
    """)
    print("Bot Online!")
    print('Current time is:' + time_date)
    print("Name: {}".format(bot.user.name))
    print("ID: {}".format(bot.user.id))
    print("OS Build: {}".format(OSBuid))
    print(f"connected to {bot.guilds}") 
    if IsDebug:
        print("""
    ######################
    ####Bot is in Debug###
    ######################
    """)
    else:
        print("""
    ######################
    ####Bot is in Prod####
    ######################
    """)

    #check the bot is not running in debug
    if not IsDebug:
        #open/create the json file
        with open(directory) as f:
            data = json.load(f)
        #find the correct key
        for i in data:
            if i == 'Tokens':
                for FoundToken in data['Tokens']:
                    if FoundToken['Name'] == 'Prod':
                        #if found write the new value
                        FoundToken['Token'] = Token
        #save the new json
        with open(directory, "w") as f:
            json.dump(data, f, indent=4)

    #sets the presence of the bot
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name='Version ' + str(OSBuid)))


@bot.event
async def on_message(message):
    channel = message.channel
    if message.author == bot.user:
        return

    global culprit_user
    #saves the user who sent it for a response 
    sending_user = message.author.mention
    matt_id = '<@98128408969506816 00000>'

    #for matt 
    if sending_user == matt_id:
        culprit_user = message.author.mention
        matt_message = (culprit_user + ' weeb')     
        #send the message
        await channel.send(matt_message)
        return culprit_user 
    
    if (bot.user != sending_user):
        #keywords you want to respond to (summit)
        sum_message_emotes = (':sum' , ':NotW')
        sum_message_emotes_whitelist = (':summitPls:')
        #searches for the emotes
        if sum_message_emotes_whitelist in message.content:
            #does nothing
            return
        elif any(x in message.content for x in sum_message_emotes):
            #puts the message together
            sum_message = (sending_user + ' Summit1G emotes :nauseated_face:')     
            #send the message
            await channel.send(sum_message)
            #returns the user so it can be used in other commands
            return sending_user      

    await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    channel = message.channel        
    #message to respond when trying to delete the emote
    message_retry = (culprit_user + ' Summit1G emotes :nauseated_face:')
    #message to respond with when trying to delete the responce 
    message_response = (message_retry + ' nice try :stuck_out_tongue_winking_eye:')
    #emotes to search for --> should be the same as the on_message command
    message_emotes = (':sum' , ':NotW')
    #add a string to the end
    sum_message_evidance = (message_response + " Don't Hide the evidence")
    #add a string to the end
    sum_message_evidance_persistant = (message_response + " you can try but we know")
    
    #searches if the response tries to get delted 
    if message.content in {message_retry, message_response}:
        #sends the message
        await channel.send(message_response)

    #searches if the evidance tries to get delted 
    if any(x in message.content for x in message_emotes):
        #sends the message
        await channel.send(sum_message_evidance)

    #searches if the message for the evidance tries to get deleted 
    if message.content == sum_message_evidance:
        #sends the message
        await channel.send(sum_message_evidance_persistant)

    #searches if the message for the evidance response tries to get deleted 
    if message.content == sum_message_evidance_persistant:
        #sends the message
        await channel.send(sum_message_evidance_persistant)

    #matt reply
    matt_message = (culprit_user + ' weeb')
    matt_message_response = (culprit_user + " another one weeb")
    if message.content in {matt_message, matt_message_response}: 
        await channel.send(matt_message_response)

    #command needed to use other commands   
    await bot.process_commands(message)
        

#set variables
Token = ''
directory = 'Json/Token.json'
#if the file is found
if os.path.isfile(directory):
    #open the json file
    with open(directory) as f:
        #load the contents
        data = json.load(f)

    #loops through the json file
    for i in data:
        #look for tokens
        if i == 'Tokens':
            #go through the multiple tokens
            for FoundToken in data['Tokens']:
                #check if the bot is running the debug token
                if IsDebug:
                    #if so use the token
                    #check the name of the token
                    if FoundToken['Name'] == 'Debug':
                        #if the length of the token is 0
                        if len(FoundToken['Token']) == 0:
                            #set debug to off to use the prod token
                            IsDebug = False
                            break   
                        #if the token is a value
                        else:
                            #use the token
                            Token = FoundToken['Token']
                #if not using debug token
                elif not IsDebug:
                    #check the name 
                    if FoundToken['Name'] == 'Prod':
                        #check the lenght of the token
                        if len(FoundToken['Token']) == 0:
                            #if it is not a value
                            break
                        else:
                            #use the token
                            Token = FoundToken['Token']
                    
#if the file does not exist
if not os.path.isfile(directory):
    #make the user enter the token
    Token = input('Please enter your token')
    #set the new json 
    NewToken = {
        "Name":"Prod",
        "Token":Token 
    }
    #write the new token to the file created
    with open(directory, "w") as write_file:
        json.dump({"Tokens": [NewToken]}, write_file, indent=4)

try:
    bot.run(Token)
except:
    print('No valid Token')
finally:
    exit()