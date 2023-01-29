import discord
from discord.ext import commands,tasks
from datetime import datetime
import json
import sqlite3




class Events(commands.Cog):
    def __init__(self,client):
        self.client=client

   
    @commands.Cog.listener()
    async def on_ready (self):
        with open ("config.json","r") as f:
            config = json.load(f)
        playing = config["STATUS"]
       
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(playing))
        print("Bot is ready")

    

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        conn=sqlite3.connect('servers.db')
        c=conn.cursor()
        c.execute("INSERT INTO servercon (guildid,prefix) VALUES (?,?)",(guild.id,"."))
        conn.commit()
        c.close()
        conn.close()

    @commands.Cog.listener()
    async def on_message(self,message):
        await self.client.process_commands(message)
        if message.content.lower()=="prefix":
            channel= message.channel
            prefix = get_prefix(message)
            await channel.send(f"The prefix for this server is `{prefix}`")


def get_prefix(message):
    conn = sqlite3.connect('servers.db')
    c=conn.cursor()
    c.execute (f"SELECT prefix FROM servercon WHERE guildid='{message.guild.id}'")
    prefix = c.fetchone()
    
    prefix = prefix [0]
   
    return prefix



def setup(client):
    client.add_cog(Events(client))

