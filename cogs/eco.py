import discord
from discord.ext import commands
import sqlite3
import random

conn=sqlite3.connect('userdata.db')
c=conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS userinfo(userid TEXT,bal INT,job TEXT)")
conn.commit()
c.close()
conn.close()




class Economy(commands.Cog):
    def __init__(self,client):
        self.client=client


    @commands.command()
    async def bal(self,ctx,user:discord.Member=0):
        if user == 0:
            user = ctx.message.author
            
        entry_check_and_create(str(user.id))
        Balance = get_bal(user.id)

        embed=discord.Embed(
            colour=discord.Colour.gold(),
            title = f"**{user}'s balance**",
            description= f"You currently have ${Balance}."
        
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/693104930717827092/693104965480087672/money_bag.png")
        await ctx.send(embed=embed)

   

    @commands.command()
    async def bet (self,ctx,amount):
        conn=sqlite3.connect('userdata.db')
        c=conn.cursor()
        entry_check_and_create(str(ctx.message.author.id))
        Balance = get_bal(ctx.message.author.id)
        #print(Balance)
        if Balance >= int(amount):
            BotRolled=random.randint(1,12)
            YouRolled=random.randint(1,12)
            if YouRolled > BotRolled:
                embed=discord.Embed(
                    colour=discord.Colour.gold(),
                    title="Win"
                )
                embed.set_author(name="Betting")
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/693086568197390346/693131332271734916/Dice.png")
                embed.add_field(name="You rolled",value=YouRolled, inline=True)
                embed.add_field(name="Bot rolled",value=BotRolled, inline=True)
                embed.add_field(name="You won:",value= amount, inline=False)
                await ctx.send(embed=embed)
                
                NewBalance = Balance + int(amount)
                
                c.execute(f"UPDATE userinfo SET bal={NewBalance} WHERE userid={str(ctx.message.author.id)}")
                conn.commit()
            elif YouRolled < BotRolled:
                NewBalance = Balance - int(amount)
                c.execute(f"UPDATE userinfo SET bal={NewBalance} WHERE userid={str(ctx.message.author.id)}")
                conn.commit()
                
                embed=discord.Embed(
                    colour=discord.Colour.red(),
                    title="Loss"
                )
                embed.set_author(name="Betting")
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/693086568197390346/693131332271734916/Dice.png")
                embed.add_field(name="You rolled",value=YouRolled, inline=True)
                embed.add_field(name="Bot rolled",value=BotRolled, inline=True)
                embed.add_field(name="You lost:",value= amount, inline=False)
                await ctx.send(embed=embed)
                
            else:
                embed=discord.Embed(
                    colour=discord.Colour.green(),
                    title="Draw"
                )
                embed.set_author(name="Betting")
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/693086568197390346/693131332271734916/Dice.png")
                embed.add_field(name="You rolled",value=YouRolled, inline=True)
                embed.add_field(name="Bot rolled",value=BotRolled, inline=True)
                embed.add_field(name="Draw!",value= 0, inline=False)
                await ctx.send(embed=embed)

                
                

        else:
            await ctx.send("You don't have enough balance in your account to bet that much!")

        c.close()
        conn.close()

    @commands.command()
    async def pay(self,ctx,amount,user:discord.User):
        conn=sqlite3.connect('userdata.db')
        c=conn.cursor()
        PayerBalance = get_bal(ctx.message.author.id)
        ReceiverBalance= get_bal(user.id)
        entry_check_and_create(user.id)
        
        if PayerBalance >= int(amount):
            NewPayerBalance= PayerBalance - int(amount)
            NewReceiverBalance = ReceiverBalance + int(amount)
            c.execute(f"UPDATE userinfo SET bal={NewPayerBalance} WHERE userid={ctx.message.author.id}")
            c.execute(f"UPDATE userinfo SET bal={NewReceiverBalance} WHERE userid={user.id}")
            conn.commit()
            c.close()
            conn.close()
            await ctx.send("Payment successful!")
        else:
            await ctx.send("You don't have enough money to perform that transaction!")

    @commands.command()
    async def give(self,ctx,amount,user:discord.User):
        Check = is_owner(ctx.message.author.id)
        if Check== "Yes":
            conn=sqlite3.connect('userdata.db')
            c=conn.cursor()
            ReceiverBalance= get_bal(user.id)
            entry_check_and_create(user.id)
            NewReceiverBalance = ReceiverBalance + int(amount)
            c.execute(f"UPDATE userinfo SET bal={NewReceiverBalance} WHERE userid={user.id}")
            conn.commit()
            c.close()
            conn.close()
            await ctx.send("Payment successful!")
        else:
            await ctx.send("Only the bot owner can run this command!")
        
    @commands.command()
    async def joblist(self,ctx):
        await ctx.send("Teacher - 100 \n Streamer - 300")

    @commands.command()
    async def startjob (self,ctx,job):
        job= job.lower()
        jobs = ['teacher','streamer']
        conn=sqlite3.connect('userdata.db')
        c=conn.cursor()
        entry_check_and_create(ctx.message.author.id)
        c.execute (f"SELECT job from userinfo WHERE userid={ctx.message.author.id}")
        conn.commit()
        result = c.fetchone()
        if result[0] is None or result[0] == "resigned" and job in jobs:
            c.execute (f"UPDATE userinfo SET job='{job}' WHERE userid={ctx.message.author.id}")
            conn.commit()
            embed=discord.Embed(colour=discord.Colour.green(),description=f"You have taken the {job} job.")
            await ctx.send(embed=embed)
        elif job not in jobs:
            embed=discord.Embed(colour=discord.Colour.red(),description=f"That job doesn't exist!")
            await ctx.send(embed=embed)

        else:
            embed=discord.Embed(colour=discord.Colour.red(),description=f"You already have a job.")
            await ctx.send(embed=embed)
        c.close()
        conn.close()


    @commands.command()
    async def myjob(self,ctx):
        entry_check_and_create(ctx.message.author.id)
        conn=sqlite3.connect('userdata.db')
        c=conn.cursor()
        c.execute(f"SELECT job FROM userinfo WHERE userid={ctx.message.author.id}")
        conn.commit()
        job = c.fetchone()
        
        if job[0] is None or job[0] =="resigned":
            embed=discord.Embed(
                colour=discord.Colour.red(),
                description = "You don't have a job."
            )
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(
                colour= discord.Colour.green(),
                description = (f"Your current job is {job[0].title()}")
            )
            embed.set_author(name="Your job.")
            await ctx.send(embed=embed)
        c.close()
        conn.close()


    @commands.command()
    async def resign(self,ctx):
        jobStatus = "resigned"
        entry_check_and_create(ctx.message.author.id)
        conn=sqlite3.connect('userdata.db')
        c=conn.cursor()
        c.execute(f"SELECT job FROM userinfo WHERE userid={ctx.message.author.id}")
        conn.commit()
        currentJob = c.fetchone()
        currentJob = currentJob[0]
        if currentJob is None or currentJob == "resigned":
            embed=discord.Embed(colour=discord.Colour.red(),description="You don't have a job to quit.")
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(colour=discord.Colour.red(),description=f"You have quit your {currentJob} job")
            await ctx.send(embed=embed)  
            c.execute (f"UPDATE userinfo SET job='{jobStatus}' WHERE userid={ctx.message.author.id}")
            conn.commit()
        c.close()
        conn.close()

    @commands.command()
    async def work(self,ctx):
        await ctx.send("The economy system is still under construction. More will be added in future patches as I decide on how to make the system more interactive / unique. -GenVenom (Developer)")

def get_bal(passedid):
    conn=sqlite3.connect('userdata.db')
    c=conn.cursor()
    c.execute(f"SELECT bal FROM userinfo WHERE userid={passedid}")
    bal= c.fetchone()
       
    if bal is None:
        Balance = 100
    if bal is not None:
        balint= int(bal[0])
        Balance = balint
    return Balance
    

def entry_check_and_create(userid):
    conn=sqlite3.connect('userdata.db')
    c=conn.cursor()
    c.execute(f"SELECT userid FROM userinfo WHERE userid={userid}")
    result = c.fetchone()
    if result is None:
        c.execute(f"INSERT INTO userinfo (userid,bal,job) VALUES(?,?,?)",(userid,100,None))
        conn.commit()
    if result is not None:
        pass
    
    c.close()
    conn.close()


def is_owner(id):
    if id==397648789793669121:  
        Check="Yes"
    else:
        Check="No"
    return Check
 


def setup(client):
    client.add_cog(Economy(client))