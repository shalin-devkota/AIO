import discord
from discord.ext import commands
import asyncio
import sqlite3

class Mod(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.command()
    async def kick(self,ctx, member: discord.Member,*,reason=None):
        if ctx.message.author.guild_permissions.kick_members:
            await member.kick(reason=reason)
            embed= discord.Embed(colour= discord.Colour.red(),description =f"Kicked member {member}")
            embed.add_field(name="Reason",value=reason)
            embed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=embed)
        
        else:
            embed=memberLackingPerm()
            await ctx.send(embed=embed)
    @kick.error
    async def kick_error(self,ctx,error):
        error = getattr(error, "original", error)
        if isinstance(error,commands.MissingRequiredArgument):
            embed=discord.Embed(colour=discord.Colour.red(), description="Please mention the name of the user to kick.")
            await ctx.send(embed=embed)
        
        elif (error,commands.BotMissingPermissions):
            embed=botLackingPerm()
            await ctx.send(embed=embed)
    
    @commands.command()
    async def ban(self,ctx, member : discord.Member,*, reason=None):
        if ctx.message.author.guild_permissions.ban_members:
            await member.ban(reason=reason)
            embed= discord.Embed(colour= discord.Colour.red(),description =f"Banned member {member}")
            embed.add_field(name="Reason",value=reason)
            embed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=embed)
        
        else:
            embed=memberLackingPerm()
            await ctx.send(embed=embed)


    @ban.error
    async def ban_error(self,ctx,error):
        error = getattr(error, "original", error)
        if isinstance(error,commands.MissingRequiredArgument):
            embed=discord.Embed(colour=discord.Colour.red(), description="Please mention the name of the user to ban.")
            await ctx.send(embed=embed)
        
        elif (error,commands.BotMissingPermissions):
            embed= botLackingPerm()
            await ctx.send(embed=embed)
    
   

    @commands.command()
    async def mute(self,ctx,member:discord.Member,reason=None):
        try:
            role=discord.utils.get(ctx.guild.roles,name="muted")
            if ctx.message.author.guild_permissions.administrator:
                await member.add_roles(role)
                embed= discord.Embed(colour= discord.Colour.red(),description =f"Muted member {member}")
                embed.add_field(name="Reason",value=reason)
                embed.set_thumbnail(url=member.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed=memberLackingPerm()
                await ctx.send(embed=embed)
        except AttributeError:
            embed=discord.Embed(colour=discord.Colour.red(), description="The mute role is not properly set up in this server.")
            await ctx.send(embed=embed)

    @mute.error
    async def mute_error(self,ctx,error):
        error = getattr(error, "original", error)
        if isinstance(error,commands.MissingRequiredArgument):
            embed=discord.Embed(colour=discord.Colour.red(), description="Please mention the name of the user to mute.")
            await ctx.send(embed=embed)
        
    


    @commands.command()
    async def unmute(self,ctx,member:discord.Member,reason=None):
        try:
            role=discord.utils.get(ctx.guild.roles,name="muted")
            if ctx.message.author.guild_permissions.administrator:
                await member.remove_roles(role)
                embed= discord.Embed(colour= discord.Colour.green(),description =f"Unmuted member {member}")
                embed.add_field(name="Reason",value=reason)
                embed.set_thumbnail(url=member.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed= memberLackingPerm()
                await ctx.send(embed=embed)
        except AttributeError:
            embed=discord.Embed(colour=discord.Colour.red(), description="The mute role is not properly set up in this server.")
            await ctx.send(embed=embed)
    
    @unmute.error
    async def unmute_error(self,ctx,error):
        error = getattr(error, "original", error)
        if isinstance(error,commands.MissingRequiredArgument):
            embed=discord.Embed(colour=discord.Colour.red(), description="Please mention the name of the user to unmute.")
            await ctx.send(embed=embed)
   

    @commands.command()
    async def clear(self,ctx,amount=1):
        if ctx.message.author.guild_permissions.manage_messages:
            await ctx.message.delete()
            await ctx.channel.purge(limit=amount)
        else:
            embed= memberLackingPerm()
            await ctx.send(embed=embed)

    @clear.error
    async def clear_error(self,ctx,error):
        error = getattr(error,"original",error)
        if (error,commands.BotMissingPermissions):
            embed=discord.Embed(colour=discord.Colour.red(), description="I dont have the required permissions to carry out this action.")
            await ctx.send(embed=embed)


    @commands.command()
    async def slowmode(self,ctx,*,time=10):
        if ctx.message.author.guild_permissions.manage_channels:
            await ctx.channel.edit(slowmode_delay=time)
            await ctx.message.delete()
        else:
            embed= memberLackingPerm()
            await ctx.send(embed=embed)
        

    @slowmode.error
    async def slowmode_error(self,ctx,error):
        error = getattr(error,"original",error)
        if (error,commands.BotMissingPermissions):
            embed=discord.Embed(colour=discord.Colour.red(), description="I dont have the required permissions to carry out this action.")
            await ctx.send(embed=embed)

    @commands.command()
    async def settopic(self,ctx,*,topic):
        if ctx.message.author.guild_permissions.manage_channels:
            await ctx.channel.edit(topic=topic)
            await ctx.message.delete()
        else:
            await ctx.send(embed=memberLackingPerm())

    @settopic.error
    async def settopic_error(self,ctx,error):
        error = getattr(error,"original",error)
        if (error,commands.BotMissingPermissions):
            embed=discord.Embed(colour=discord.Colour.red(), description="I dont have the required permissions to carry out this action.")
            await ctx.send(embed=embed)
        elif (error,commands.MissingRequiredArgument):
            embed=discord.Embed(colour=discord.Colour.red(),description="Please mention the topic you would like to set for this channel.")
 
    @commands.command()
    async def setrole(self,ctx,member: discord.Member,role):
        role=discord.utils.get(ctx.guild.roles,name=role)
        if role in ctx.guild.roles:
            if ctx.message.author.guild_permissions.manage_roles:
                await member.add_roles(role)
                embed=discord.Embed(colour=discord.Colour.green(),description = f"{member} has been given the {role} role!")
                await ctx.send(embed=embed)
            else:
                await ctx.send(embed = memberLackingPerm())
        else:
            embed=discord.Embed(colour=discord.Colour.red(),description=f"Role does not exist!")
            await ctx.send(embed=embed)
        
              
    @setrole.error
    async def setrole_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            embed=discord.Embed(colour=discord.Colour.red(),description=f"Please mention a user to grant the role to and the name of the role.")
        elif (error,commands.BotMissingPermissions):
            embed=botLackingPerm()
            await ctx.send(embed=embed)
       



    @commands.command()
    async def changenick(self,ctx,member:discord.Member,*,nick):
        if ctx.message.author.guild_permissions.manage_nicknames:
            await member.edit(nick=nick)
            embed=discord.Embed(colour=discord.Colour.green(),description=f"Name change successful!")
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed= memberLackingPerm())
    
    @changenick.error
    async def changenick_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            embed=discord.Embed(colour=discord.Colour.red(),description=f"Please mention a user to change nickname and the new nickname.")
        elif (error,commands.BotMissingPermissions):
            embed=botLackingPerm()
        await ctx.send(embed=embed)

    @commands.command()
    async def setprefix(self,ctx,prefix):
        if ctx.message.author.guild_permissions.administrator:
            conn=sqlite3.connect('servers.db')
            c=conn.cursor()
            c.execute(f"UPDATE servercon SET prefix='{prefix}' WHERE guildid={ctx.message.guild.id}")
            conn.commit()
            c.close()
            conn.close()
            await ctx.send(f"The prefix for this server has been set to : `{prefix}`")
        else:
            await ctx.send(embed= memberLackingPerm())

    @setprefix.error
    async def setprefix_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            embed=discord.Embed(colour= discord.Colour.red(),description="Please mention the new prefix to set for this server.")
            await ctx.send(embed=embed)

def memberLackingPerm():
    embed=discord.Embed(colour=discord.Colour.red(), description="You dont have the required permissions to carry out this action.")
    return embed

def botLackingPerm():
    embed=discord.Embed(colour=discord.Colour.red(), description="I am missing required permissions for this action.")
    return embed

def setup(client):
    client.add_cog(Mod(client))

