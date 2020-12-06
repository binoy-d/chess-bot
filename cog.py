from discord.ext import commands
import pickle
import json
from elo import rate_1vs1
import discord

class Chess(commands.Cog):
    

    def __init__(self, bot):
        self.bot = bot
        self.data = dict()
        with open("data.dat", "rb") as f:
            try:
                self.data = pickle.load(f)
            except EOFError:
                with open("data.dat", "wb") as f2:
                    pickle.dump(dict(), f2)
    
    def write_data(self):
        with open("data.dat", "wb") as f:
            pickle.dump(self.data, f)
    
    @commands.command(name = "check")
    async def check(self, context, argument = ""):
        await context.send("mate!")
    
    @commands.command(name ="add-user", aliases = [ "user-add", "addusr", "usradd"])
    async def add_user(self, context, argument = ""):
        if '<@!' not in argument:
            await context.send(f"no at mention detected in {argument}")
            return
        
        await context.send(f"adding user: {argument}")
        userid = argument[3:-1]
        print(f"adding {userid}")
        if len(argument) == 0:
            await context.send(f"no user specified")
        else:
            if userid not in self.data:
                self.data[userid] = 1500
            await context.send(f"{argument} rank = {self.data[userid]}")
            self.write_data()

    @commands.command(name = "get-score")
    async def get_score(self, context, argument = ""):
        if len(argument) == 0 or argument[3:-1] not in self.data:
            await context.send(f"user {argument} not found!")
        else:
            userid = argument[3:-1]
            await context.send(f"current score of {argument}:{self.data[userid]}")
    
    @commands.command(name = "add-game")
    async def add_game(self, context, user1 = None,  user2  = None, draw = None):
        if user1 is None or user2 is None:
            await context.send(f"syntax wrong")
            return
        else:
            userid1 = user1[3:-1]
            userid2 = user2[3:-1]

            if userid1 not in self.data:
                self.data[userid1] = 1500

            if userid2 not in self.data:    
                self.data[userid2] = 1500
            
            newscore1, newscore2 = rate_1vs1(self.data[userid1], self.data[userid2], draw is not None)
            self.data[userid1] = newscore1
            self.data[userid2] = newscore2
            await context.send(f"New Scores!\n{user1}: {self.data[userid1]}\n{user2}:{self.data[userid2]}")
            self.write_data()

    @commands.command(name = "get-ranking")
    async def get_ranking(self, context, arg = None):
        out = ""
        i = 1
        format_row = "{:12}"
        out+=format_row.format("#", "User", "ELO")+"\n"
        for userid, score in sorted(self.data.items(), key =  lambda x: (x[1], x[0]), reverse=True):
            out+=format_row.format(str(i))+"     "
            out+=format_row.format(str(self.bot.get_user(int(userid))))+"     "
            out+=format_row.format(str(score))+"     \n"
            i+=1
        print(out)
        await context.send(embed=self.generateEmbed(context, 'Rankings', out))
    
    def generateEmbed(self, ctx: commands.Context, title, description=""):
        embed = discord.Embed(
            colour = ctx.author.colour,
            title = title,
            description = description
        )
        return embed
