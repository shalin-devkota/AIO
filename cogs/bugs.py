import discord
from discord.ext import commands
import sqlite3
import random
import datetime


conn=sqlite3.connect('bugs.db')
c=conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS bugs (bugid TEXT,bug TEXT,reporter TEXT, guild TEXT,date TEXT,status INT)")
conn.commit()
c.close()
conn.close()



def is_owner(id):
    if id==397648789793669121:  
        Check="Yes"
    else:
        Check="No"
    return Check



class Bugs(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.command()
    async def bug(self,ctx,*,bug):
        status="Unresolved"
        BugID= ctx.message.id
        channel=self.client.get_channel(706729782280192012)
        reporter=ctx.message.author.id
        guild=ctx.message.guild.id
        date= datetime.date.today()
        conn=sqlite3.connect('bugs.db')
        c=conn.cursor()
        c.execute("INSERT INTO bugs (bugid,bug,reporter,guild,date,status) VALUES (?,?,?,?,?,?)",(BugID,bug,reporter,guild,date,0))
        conn.commit()
        
        
        c.close()
        conn.close()
        embed = embed_maker(BugID,status,bug)
        await channel.send(embed=embed)
        embed=discord.Embed(
            colour=discord.Colour.green(),
            description="The bug has been reported successfully"
        )
        embed.set_author(name="Bug reported!")
        await ctx.send(embed=embed)
        
       

    @commands.command()
    async def markbug(self,ctx,bugid,pstatus):
        #channel=self.client.get_channel(706729782280192012)
        Check = is_owner(ctx.message.author.id)
        if Check=="Yes":
            pstatus=pstatus.lower()
            status={
                "solved":1,
                "pending":2,
                "nei":3,
                "nab":4
            }
            conn=sqlite3.connect('bugs.db')
            c=conn.cursor()
            try:
                c.execute(f"UPDATE bugs SET status={status[pstatus]} WHERE bugid={bugid}")
                
                c.execute(f"SELECT reporter FROM bugs WHERE bugid={bugid}")
                reporter=c.fetchone()
                reporter=reporter[0]
                reporter = self.client.get_user(int(reporter))
                
                c.execute(f"SELECT bug FROM bugs WHERE bugid={bugid}")
                bug=c.fetchone()
                
                
                conn.commit()
                c.close()
                conn.close()
                await ctx.send(f"The bug has been marked as {pstatus.title()}.")
                
                
            except KeyError:
                await ctx.send("Invalid bug status!") 
        else:
            await ctx.send("Only the developer can run this command!")

        embed=discord.Embed(
            colour=0x6B6AB5,
            description= f"The dev team has responded to your bug report! It has been marked as {pstatus}."
        )
        embed.add_field(name="You reported:",value=bug[0])
        embed.set_author(name="Bug report update!")
        await reporter.send(embed=embed)

    @commands.command()
    async def buginfo(self,ctx,bugid):
        status={
                0 :"Unresolved",
                1:"Solved",              #These should be integers and not strings to prevent key error. Why am i gay
                2:"Pending",
                3:"NEI",
                4 :"NAB"
            }
        conn=sqlite3.connect('bugs.db')
        c=conn.cursor()
        c.execute(f"SELECT * FROM bugs WHERE bugid={bugid}")
        buginfo=c.fetchone()
        BugId= buginfo[0]
        Bug= buginfo[1]
        ReportedBy= buginfo[2]
        ReportedInGuild= buginfo[3]
        ReportDate= buginfo[4]
        BugStatus= status[buginfo[5]]

        
        embed=discord.Embed(
            colour=discord.Colour.red(),
            description= Bug

        )
        embed.set_author(name="Bug info!")
        embed.add_field(name="BugId  ",value=BugId)
        embed.add_field(name="Bug status  ",value=BugStatus)
        embed.add_field(name="Report Date  ",value=ReportDate)
        embed.add_field(name="Reported By  ",value=ReportedBy)
        embed.add_field(name="Reported in guild  ",value=ReportedInGuild)
        
        await ctx.send(embed=embed)
        

def embed_maker(bugid,status,bug):
    colors={
        'Unresolved': 0xDAD9E8,
        'solved': 0x1CEC1C,
        'pending': 0xF9F206,
        'nei':  0xEE1815,
        'nab': 0x3040DC
    }
    embed=discord.Embed(
            colour=colors[status],
            description = f"{bug}",
            title= f"{status.title()}"
        )
    embed.set_author(name="Bug reported!")
    embed.set_footer(text=f"BugID : {bugid}")
        
    return embed




    
def setup(client):
    client.add_cog(Bugs(client))