import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.command()
    async def help(self,ctx):
        embed= discord.Embed(
            colour = discord.Colour.green(),
            description = "Use the prefix before each command to run it. (Duh)"
        )
        embed.set_author(name="Help!")
        embed.add_field(name="Moderation commands",value= "`kick`,`ban`,`mute`,`unmute`,`clear`,`slowmode`,`settopic`,`setrole`,`changenick`,`setprefix`",inline=False)
        embed.add_field(name="fun",value="`gaytest`,`chuck`,`rhyme`,`bigtext`,`ask`,`toss`,`dice`,`rps`,`fight`,",inline=False)
        embed.add_field(name="bug",value="`bug`")
        embed.add_field(name="reddit",value="`subreddit`,`redditor`,`srsearch`,`rsearch`,`tifu`,`ns`,`ra`,`hot`,`meme`",inline=False)
        
        embed.add_field(name="economy",value="`bal`,`pay`,`joblist`,`bet`,`startjob`,`myjob`,`resign`",inline=False)
        embed.set_footer(text="Seen a bug? Use the bug command to notify the devs!")
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))