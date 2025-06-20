import nextcord
from nextcord.ext import commands
from mongoFile import *
from .utils import *
from .fight import *


class fight(commands.Cog, name="Fight"):
    """Fighting commands for the bot"""

    @commands.command()
    async def boss(self, ctx: commands.Context, *args: str):
        """
        Fight the bosses!

        Use:
        ```!su boss```
        This command will open a menu, showing all available bosses to fight against
        and will also show which bosses you have already beaten.
        Note: You can only beat a boss with a particular jam bud once.

        Use:
        ```!su boss (boss you wish to fight)```
        This command will prompt an active fight between your jam bud and the boss.
        Should you win, you gain XP.
        """
        userName = ctx.author.name
        userID = ctx.author.id
        guildID = ctx.guild.id
        userInput = " ".join(args[:])
        userInput = userInput.lower()
        if not checkUser_Mongo(guildID=guildID, userName=userName):
            em = errorMessageEmbed(ctx=ctx)
            message1 = await ctx.send(embed=em)
            try:
                await message1.delete(delay=5)
            except Exception:
                pass
        else:
            # Actual commands for function start here
            if userInput == "":
                # This is the case for when the user doesn't give any arguments'
                em = displayBossesEmbed(ctx=ctx)
                await ctx.send(embed=em)
            else:
                # Here we need to validate the input
                if not bossInputCheck(userInput=userInput):
                    # Invalid error message
                    message = await ctx.send("Invalid Input! Make sure you spelled the bosses' name correctly!")
                    try:
                        await message.delete(delay=10)
                    except Exception:
                        pass
                else:
                    # This is if there is a valid message
                    # Here we make sure they haven't already beaten the boss
                    check = checkBossBeaten(ctx=ctx, userName=userName, boss= userInput)
                    # print(check)
                    if check:
                        # print("Boss beaten!")
                        em1 = alreadyBeatBossEmbed(ctx=ctx, userName=userName, boss=userInput)
                        message2 = await ctx.send(embed=em1)
                        try:
                            await message2.delete(delay=10)
                        except Exception:
                            pass
                    else:
                        # print("Loop reached")
                        # Here we insert the fighting mechanism.
                        em = bossFightActiveEmbed(ctx=ctx, userName=userName, boss=userInput)
                        message1 = await ctx.send(embed=em)
                        won, xp = await fightBoss(ctx=ctx, userName=userName, enemy=userInput, mess=message1)
                        if won:
                            await addXP(userName=userName, xpToAdd=xp, ctx=ctx)
                            addDefeatedBossToUser(userName=userName, boss=userInput)

    @commands.command()
    async def fight(self, ctx: commands.Context, enemy: nextcord.User):
        """
        Fight another user!

        Use:
        ```!su fight (@user you wish to fight)```
        This command will prompt an active fight between your jam bud and the mentioned user's jam bud.
        Should you win, you gain XP.
        Should you lose, you lose XP.
        """
        userName = ctx.author.name
        userID = ctx.author.id
        guildID = ctx.guild.id
        if not checkUser_Mongo(guildID=guildID, userName=userName):
            em = errorMessageEmbed(ctx=ctx)
            message1 = await ctx.send(embed=em)
            try:
                await message1.delete(delay=5)
            except Exception:
                pass
        else:
            if not checkUser_Mongo(guildID=guildID, userName=enemy.name):
                msg = "This user does not yet have a jam bud for them to fight with. The fight will not commence"
                message1 = await ctx.send(msg)
                try:
                    await message1.delete(delay=5)
                except Exception:
                    pass
            else:
                # Here we insert the fighting mechanism.
                em = userFightActiveEmbed(ctx=ctx, userName=userName, enemyName=enemy.name)
                message1 = await ctx.send(embed=em)
                won, xp = await fightUser(ctx=ctx, userName=userName, enemyUserName=enemy.name, mess=message1)
                if won:
                    await addXP(userName=userName, xpToAdd=xp, ctx=ctx)
                else:
                    await addXP(userName=enemy.name, xpToAdd=xp, ctx=ctx)


    def __init__(self, bot: commands.Bot):
        self.bot = bot


def setup(bot: commands.Bot):
    bot.add_cog(fight(bot))
