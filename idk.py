import discord
from discord_slash import SlashCommand
import pickle
import asyncio
from discord.ext import commands


# create a global variable for the file name
this_list_file = "thislist.pkl"

# create a function to save the list to the file
def save_list(thislist):
    # open the file in write mode
    with open(this_list_file, "wb") as f:
        # use pickle to dump the list to the file
        pickle.dump(thislist, f)

# create a function to load the list from the file
def load_list():
    # open the file in read mode
    with open(this_list_file, "rb") as f:
        # use pickle to load the list from the file
        thislist = pickle.load(f)
    # return the list
    return thislist

# try to load the list from the file, or create a new one if it fails
try:
    thislist = load_list()
except:
    thislist = []

bot = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)
client = discord.Client()

@bot.event
async def on_ready():
    print('Bot is ready.')

@slash.slash(name="unmute", description="Unmutes a user in the current channel.")
async def unmute(ctx, user: discord.Member):
    # get the channel where the command was used
    channel = ctx.channel
    # create a permission overwrite object that allows send_messages and speak permissions
    overwrite = discord.PermissionOverwrite(send_messages=True, speak=True)
    # apply the overwrite to the user in the channel
    await channel.set_permissions(user, overwrite=overwrite)
    # send a confirmation message that only the user who used the command can see
    await ctx.send(f"{user.mention} has been unmuted.")
    
@slash.slash(name="add_user", description="Adds a user to the block list.")
async def add_user(ctx, user: discord.Member):
    # get the user id
    user_id = user.id
    # check if the user id is already in the list
    if user_id in thislist:
        # send a message saying the user is already blocked
        await ctx.send(f"{user.mention} is already blocked.")
    else:
        # add the user id to the list
        thislist.insert((1+len(thislist)), user_id)
        print(user_id)
        # send a confirmation message
        await ctx.send(f"{user.mention} has been added to the block list.")

        # save the list to the file before exiting
        save_list(thislist)
        
@slash.slash(name="remove_user", description="Removes a user from the block list.")
async def remove_user(ctx, user: discord.Member):
    # get the user id
    user_id = user.id
    # check if the user id is in the list
    if user_id in thislist:
        # remove the user id from the list
        thislist.remove(user_id)
        # send a confirmation message
        await ctx.send(f"{user.mention} has been removed from the block list.")

        # save the list to the file before exiting
        save_list(thislist)
    else:
        # send a message saying the user is not blocked
        await ctx.send(f"{user.mention} is not blocked.")


@bot.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('<@1116492998021238905>'):
        user_input = message.content.replace('<@1116492998021238905>', '')
        # Get the message ID and reply to it
        reply_message = await message.channel.fetch_message(message.id)
        await reply_message.reply("yo")
        
    if message.author == bot.user:
        return
        
    
    # change the user id to the one you want to mute
    if message.author.id in thislist:
        # change the role name to the one you have for muted users
        channel = message.channel
        user = message.author
        # check if there is a role with the name 'Muted'
        overwrite = discord.PermissionOverwrite(send_messages=False, speak=False)
        # if not, create one
        await channel.set_permissions(user, overwrite=overwrite)
        
        # change the time to the one you want for muting duration (in seconds)
        await asyncio.sleep(7)
        overwrite = discord.PermissionOverwrite(send_messages=True, speak=True)
        await channel.set_permissions(user, overwrite=None)
    # this line should be unindented
    await bot.process_commands(message)

bot.run("put discord bot key here")
