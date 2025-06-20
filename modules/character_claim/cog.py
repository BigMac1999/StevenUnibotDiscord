from typing import Optional

import nextcord

from .utils import *
from nextcord.ext import commands
from mongoFile import *



class CC(commands.Cog, name="Character Claim"):
    """Testing commands for the bot"""

    @commands.command()
    async def claim(self, ctx: commands.Context, *args: str):
        """
        Jam Bud Claiming Command

        Use:
        ```!su claim```
        This command will display all availible jam buds to claim.

        Use:
        ```!su claim (name of character)```
        This command will actively claim that character as your jam bud.
        """
        guildID = ctx.guild.id
        userName = ctx.author.name
        input = " ".join(args[:])
        # This is for debugging
        if input != "":
            if checkUser_Mongo(guildID=guildID, userName=userName):
                message1 = await ctx.send("You already have an account and a jam bud, either on this server or "
                                          "another one so you will not be able to claim a new jam bud.")
                try:
                    await message1.delete(delay=10)
                except Exception:
                    pass
            else:
                #Make sure input is valid
                if not inputCheck(userInput=input):
                    em2 = "This jam bud was not found. Make sure you spelled it right and try again!"
                    message2 = await ctx.send(em2)
                    try:
                        await message2.delete(delay=5)
                    except Exception:
                        pass
                    return
                # Create account
                createBlankUserAccount(ctx=ctx)
                # Claim character
                claimCharacter(guildID=guildID, userName=userName, character=input)
                await ctx.send("You have claimed " + input + " as a jam bud!")
        else:
            if checkUser_Mongo(guildID=guildID, userName=userName):
                message1 = await ctx.send("You already have an account and a jam bud, either on this server or "
                                          "another one so you will not be able to claim a new jam bud.")
                try:
                    await message1.delete(delay=10)
                except Exception:
                    pass

                em = displayCharactersForClaim(ctx=ctx)
                await ctx.send(embed=em)
            else:
                em = displayCharactersForClaim(ctx=ctx)
                await ctx.send(embed=em)

    @commands.command()
    async def unclaim(self, ctx: commands.Context, *args: str):
        """
        Character Unclaiming Command

        Use:
        ```!su unclaim```
        This command will unclaim the current user's current jam bud
        Be careful, this action is undo-able.
        """
        userInput = "".join(args)
        userInput = userInput.lower()
        if userInput == "y" or userInput == "yes":
            unclaimCharacter(ctx.guild.id, ctx.author.name)
            msg = "Your jam bud has been unclaimed"
            await ctx.send(msg)
        else:
            msg = "Are you sure you want to unclaim your jam bud? This is undo-able and if they are strong, you will" \
                  "never be able to get those stats or the boss badges back.\nIf you still want to continue, use the " \
                  "command: `!su unclaim y` or `!su unclaim yes`"
            message = await ctx.send(msg)
            try:
                await message.delete(delay=5)
            except Exception:
                pass




    # @commands.command()
    # async def printStock(self, ctx: commands.Context, characterName: str):
    #     """
    #     Prints stock stats for a character
    #     """
    #     charStats = returnStockCharacter(characterName)
    #     print(charStats)
    #
    # @commands.command()
    # async def addXP(self, ctx: commands.Context, characterName: str):
    #     characterName = characterName.lower()
    #     username = ctx.author.name
    #     guildID = ctx.guild.id
    #     if check_SQLByName(userName=username,guildID=guildID):
    #         updateCharacterXP_SQL(userName=username, guildID=guildID, characterName=characterName, XPAdded=100)

    def __init__(self, bot: commands.Bot):
        self.bot = bot


def setup(bot: commands.Bot):
    bot.add_cog(CC(bot))
