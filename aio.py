import discord 
from discord.ext import commands, tasks
from discord.utils import get
import os
import json
import sqlite3

intents = discord.Intents.default()
intents.all()



with open ("config.json","r") as f:
    config = json.load(f)

def get_prefix(client,message):
    conn = sqlite3.connect('servers.db')
    c=conn.cursor()
    c.execute (f"SELECT prefix FROM servercon WHERE guildid='{message.guild.id}'")
    prefix = c.fetchone()
    
    prefix = prefix [0]
    
        

    return prefix


client = commands.Bot(command_prefix=get_prefix,case_insensitive=True,intents=intents)
client.remove_command("help")
owner_idss = config["owner_id"]
TOKEN = config["Token"]

conn = sqlite3.connect('servers.db')
c=conn.cursor()
c.execute ("CREATE TABLE IF NOT EXISTS servercon (guildid TEXT, prefix TEXT)")
conn.commit()
c.close()
conn.close()

#loads all the cogs inside the cogs folder on startup
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')    


@client.command()
#to load a cog
async def load(ctx,cname):
    author=ctx.message.author.id #gets the author's id.
    if author==397648789793669121: #checks if the authors id matches the owner's id.
        client.load_extension(f"cogs.{cname}")
        await ctx.send(f"Successfully loaded {cname}")
    else:
        await ctx.send("Only the bot owner can use this command.")

@client.command()
# to unload a cog
async def unload(ctx,cname):
    author=ctx.message.author.id #gets the author's id.
    if author==397648789793669121: #checks if the authors id matches the owner's id.
        client.unload_extension(f"cogs.{cname}")
    else:
        await ctx.send("Only the bot owner can use this command!")
    
@client.command()
#to reaload an ALREADY LOADED cog
async def reload(ctx,cname):
    author=ctx.message.author.id #gest the author's id.
    if author==397648789793669121: #checks if the authors id matches the owner's id.
        client.unload_extension(f"cogs.{cname}")
        client.load_extension(f"cogs.{cname}")
        await ctx.send(f"Successfully reloaded {cname}.")
    else:
        await ctx.send("Only the bot owner can use this command!")




client.run(TOKEN)



 

