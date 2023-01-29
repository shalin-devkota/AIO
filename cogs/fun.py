import discord
from discord.ext import commands,tasks
from datetime import datetime
import random
import json
import requests
import asyncio

activeChannels =[]

class Fun(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.command()
    async def gaytest(self,ctx,user):
        a=random.randint(1,100)
        embed=discord.Embed(colour=discord.Colour.dark_purple(),description=f"{user} is {a}% gay.")
        embed.set_author(name="🏳️‍🌈🏳️‍🌈 Gay test 🏳️‍🌈🏳️‍🌈")
        await ctx.send(embed=embed)
    
    @gaytest.error
    async def gaytest_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            embed=discord.Embed(colour=discord.Colour.red(),description="I need a subject to run the test on! ")
            await ctx.send(embed=embed)

    @commands.command()
    async def chuck(self,ctx):
        request=requests.get("https://api.chucknorris.io/jokes/random")

        chuck_json=request.json()
        embed=discord.Embed(
            colour=discord.Colour.blue(),
            description = f"{chuck_json['value']}"
        )
        embed.set_author(name="Chuk Norris da man!")
        await ctx.send(embed=embed)

    @commands.command()
    async def rhyme(self,ctx,word):
        MessageToSend=""
        parameter={"rel_rhy":word}
        request = requests.get("https://api.datamuse.com/words",parameter)

        rhyme_json= request.json()
        for i in rhyme_json[0:3]:
            RhymeWordFetcher=(i['word'])
            MessageToSend=MessageToSend+ "  "+RhymeWordFetcher

        embed=discord.Embed(
        
        colour=discord.Colour.blue()
        )
        embed.set_footer(text="Powered by datamuse!")
        embed.add_field(name="Rhyme :musical_note: ", value=MessageToSend)
    
        await ctx.send(embed=embed)

    @rhyme.error
    async def rhyme_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            embed= discord.Embed(colour=discord.Colour.red(),description=f"Please enter the word to search the rhyming word for!")
            await ctx.send(embed=embed)

    @commands.command()
    async def bigtext(self,ctx,*,a):
        counter= len(a)
        a=a.lower()
        flag=int(counter)
        final=""
        for i in range (0,flag):
            letters=a[i]
            if letters=="1":
                extracter=":one:"
            elif letters=="2":
                extracter=":two:"
            elif letters=="3":
                extracter=":three:"
            elif letters=="4":
                extracter=":four:"
            elif letters=="5":
                extracter=":five:"
            elif letters=="6":
                extracter=":six:"
            elif letters=="7":
                extracter=":seven:"
            elif letters=="8":
                extracter=":eight:"
            elif letters=="9":
                extracter=":nine:"
            elif letters=="0":
                extracter=":zero:"
            elif letters==" " :
                extracter="   "
            else:
                extracter=":regional_indicator_"+letters+": "
            final=final+extracter
        await ctx.send(final)

    @bigtext.error
    async def bigtext_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            embed= discord.Embed(colour=discord.Colour.red(),description=f"Please enter the word to turn into big text!")
            await ctx.send(embed=embed)


    @commands.command()
    async def ask(self,ctx,*,question):
        responses = ["Yes","No"]
       
        await ctx.send(f"{random.choice(responses)}")

    @ask.error
    async def ask_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            embed= discord.Embed(colour=discord.Colour.red(),description=f"Please input your question!")
            await ctx.send(embed=embed)

    @commands.command(aliases=["flip"])
    async def toss(self,ctx):
        responses =["Heads","Tails"]
        embed=discord.Embed(colour=discord.Colour.green(),description=f"You got : `{random.choice(responses)}`")
        await ctx.send(embed=embed)


    @commands.command ()
    async def dice(self,ctx):
        responses=random.randint(1,6)
        embed=discord.Embed(colour=discord.Colour.green(),description=f"You got : `{responses}`")
        await ctx.send(embed=embed)
    
    @commands.command()
    async def rps(self,ctx,player):
        o=["rock","paper","scissors"]
        computer = random.choice(o)
        if player=="rock" or player=="paper" or player=="scissors":
            pass
        else:
            await ctx.send("Wrong input!")
        
        if player==computer:
            result="Draw!"
        elif player=="rock" and computer=="paper":
            result ="You lost!"
        elif player=="rock" and computer =="scissors":
            result = "You won!"
        elif player=="scissors" and computer=="rock":
            result = "You lost!"
        elif player=="scissors" and computer=="paper":
            result="You won!"
        elif player=="paper" and computer=="rock":
            result = "You won!"
        elif player=="paper" and computer =="scissors":
            result = "You lost!"

        colours ={
            'You won!' : 0x4BF012,
            'You lost!':0xF01212,
            'Draw!': 0xF5F817
        }
        embed=discord.Embed(
            colour= colours[result],
            description=f"{result}"
        )
        embed.set_author(name=f"Bot picked: {computer}")
        await ctx.send(embed=embed)
    @rps.error
    async def rps_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            embed= discord.Embed(colour=discord.Colour.red(),description=f"Please input your choice!")
            await ctx.send(embed=embed)


    @commands.command()
    async def fight(self,ctx,enemy:discord.Member):
        channel = ctx.message.channel
        channelState= checkChannel (channel)
        if channelState == "False":
            activeChannels.append(channel)
            
            Challenger= ctx.message.author
            ChallengerHP= 100
            
            EnemyHP=100
            def CheckAccept(message):
                
                return message.content=="accept" and message.author==enemy
            
            await ctx.send(f"{enemy.mention} {ctx.message.author.name} has invited you to a duel!Type `accept` in chat to accept!")
            try:
                await self.client.wait_for('message',check=CheckAccept,timeout=30)
            
            
                
                #GameState= "Started"
                firstMove=["author","enemy"]
                turn=random.choice(firstMove)
                await ctx.send("Acccepted! The game will start in 5 seconds. Get ready!")
                await asyncio.sleep(5)
                i= 1
                while ChallengerHP > 0 and EnemyHP>0:
                    print (i)
                    i +=1 
                    if turn=="author":
                        await ctx.send(f"{Challenger.mention} make your move! You can either `slap` `punch` or `kick`.")
                        def CheckChallengerMessage(message):
                            fightMoves= ['punch','kick','slap']
                            
                            return message.content.lower() in fightMoves and message.author == Challenger
                        try:
                            fightMove= await self.client.wait_for('message',check=CheckChallengerMessage,timeout=30)
                        except asyncio.TimeoutError:
                            await ctx.send(f"{Challenger.name} didn't respond in time!")
                            break
                        damage = random.randint(2,30)
                        EnemyHP = EnemyHP - damage
                        if EnemyHP < 0 :
                            EnemyHP = 0
                        embed = challengerHit(enemy,Challenger,damage,ChallengerHP,EnemyHP,fightMove)
                        await ctx.send(embed=embed)
                        turn = "enemy"
                        
                    else:
                        
                        await ctx.send(f"{enemy.mention} make your move! You can either `slap` `punch` or `kick`.")
                        def CheckEnemyMessage(message):
                            fightMoves = ['punch','kick','slap']
                            return message.content.lower() in fightMoves and message.author==enemy
                        try:
                            fightMove =await self.client.wait_for('message',check=CheckEnemyMessage,timeout= 30)
                        except asyncio.TimeoutError:
                            await ctx.send(f"{enemy.name} didn't respond in time!")
                            break
                        damage = random.randint(2,30)
                        ChallengerHP = ChallengerHP - damage
                        if ChallengerHP < 0:
                            ChallengerHP = 0
                        embed = enemyHit (enemy,Challenger,damage,ChallengerHP,EnemyHP,fightMove)
                        await ctx.send(embed=embed)
                        turn="author"
                        
                        
                        
                    
                if ChallengerHP > EnemyHP :
                    embed = discord.Embed(colour=discord.Colour.green(),description=f"{Challenger.mention} won with {ChallengerHP} hp remaining.")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(colour=discord.Colour.green(),description=f"{enemy.mention} won with {EnemyHP} hp remaining.")
                    await ctx.send(embed=embed)
                activeChannels.remove(channel)
            except asyncio.TimeoutError:
                embed=discord.Embed(colour=discord.Colour.red(),description=f"{enemy.mention} didn't accept in time! Pfft.")
                await ctx.send(embed=embed)
                
                activeChannels.remove(channel) 
    
        else:
            await ctx.send("There is already an ongoing fight in this channel. Please use another channel.")
        
        


def enemyHit(enemy,challenger,damage,ChallengerHP,EnemyHP,fightMove):
    embed = discord.Embed(
        colour= discord.Colour.red(),
        title= "Fight results",
        description= f"{enemy.name}  {fightMove.content}ed {challenger.name}  and dealt  **{damage}** damage!"
    )
    embed.add_field(name=f"{challenger.name}'s HP",value=ChallengerHP)
    embed.add_field(name=f"{enemy.name}'s HP",value=EnemyHP)
    return embed
      
def challengerHit(enemy,challenger,damage,ChallengerHP,EnemyHP,fightMove):
    embed = discord.Embed(
        colour= discord.Colour.red(),
        title= "Fight results",
        description= f"{challenger.name}  {fightMove.content}ed {enemy.name}  and dealt  **{damage}** damage!"
    )
    embed.add_field(name=f"{challenger.name}'s HP",value=ChallengerHP)
    embed.add_field(name=f"{enemy.name}'s HP",value=EnemyHP)
    return embed         


def checkChannel(channel):
    if channel in activeChannels:
        rValue = "True"
    else:
        rValue = "False"
    
    return rValue




def setup(client):
    client.add_cog(Fun(client))
    