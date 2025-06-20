import nextcord
from nextcord.ext import commands
from mongoFile import *
from .utils import *
from .fusion import *


class character(commands.Cog, name="Character"):
    """Jam bud commands for the bot"""

    @commands.command()
    async def profile(self, ctx: commands.Context, user: nextcord.User):
        """
        Display another user's jam buds

        Use:
        ```!su profile (@user)```
        This command will allow you to see another user's profile.
        It will show you their jam bud, their stats, and their level/XP.

        Note: The user must be mentioned (@user) and they must also have a jam bud claimed
        """
        userName = user.name
        userID = user.id
        guildID = ctx.guild.id
        if not checkUser_Mongo(guildID=guildID, userName=userName):
            # Error case that someone uses this command without a jam bud
            msg = "This user has not claimed a jam bud or may not exist. Please try again or try another user"
            message1 = await ctx.send(msg)
            try:
                await message1.delete(delay=5)
            except Exception:
                pass
        else:
            em = profileEmbed(ctx=ctx, userName=userName)
            await ctx.send(embed=em)

    @commands.command()
    async def display(self, ctx: commands.Context, *args: str):
        """
        Display a jam bud

        Use:
        ```!su display```
        This command will let you see your own profile.
        It will show your jam bud, their stats, and their level/XP.

        Use:
        ```!su display (name of a boss)```
        This command with the name of a boss at the end will display a bosses' profile
        It will show their stats and level
        """
        userName = ctx.author.name
        userID = ctx.author.id
        guildID = ctx.guild.id
        userInput = " ".join(args[:])
        userInput = userInput.lower()
        if not checkUser_Mongo(guildID=guildID, userName=userName):
            # Error case that someone uses this command without a jam bud
            em = errorMessageEmbed(ctx=ctx)
            message1 = await ctx.send(embed=em)
            try:
                await message1.delete(delay=5)
            except Exception:
                pass
        else:
            if userInput == "":
                em = displayEmbed(ctx=ctx)
                await ctx.send(embed=em)
            else:
                if not bossInputCheck(userInput=userInput):
                    # Invalid error message
                    message = await ctx.send("Invalid Input! Make sure you spelled the bosses' name correctly!")
                    try:
                        await message.delete(delay=10)
                    except Exception:
                        pass
                else:
                    em = displayBossEmbed(ctx=ctx, boss=userInput)
                    await ctx.send(embed=em)


    # @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command()
    async def train(self, ctx: commands.Context):
        """
        Train with your jam bud.

        Use:
        ```!su train```
        This command can only be used once in a certain time frame and will add XP to your jam bud.
        (based off of their current level and stats)
        """
        userName = ctx.author.name
        userID = ctx.author.id
        guildID = ctx.guild.id
        if not checkUser_Mongo(guildID=guildID, userName=userName):
            await ctx.send("You need to claim a jam bud first!")
        else:
            duo = []
            duo = trainingEmbed(ctx=ctx)
            message2 = await ctx.send(embed=duo[0])
            # try:
            #     await message2.delete(delay=10)
            # except Exception:
            #     pass
            await addXP(userName=userName, xpToAdd=duo[1], ctx=ctx)
            try:
                await ctx.message.delete(delay=5)
            except Exception:
                pass

    # @commands.cooldown(1, 1, commands.BucketType.user)
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.cooldown(1, 120, commands.BucketType.user)
    @commands.command()
    async def play(self, ctx: commands.Context):
        """
        Play with your jam bud.

        Playing with your jam bud will increase its friendship level towards you.
        This will be used to further strengthen your bond with your jam bud and make it even stronger!

        Use:
        ```!su play```
        This command has a chance to increase your friendship level with your jam bud.
        """
        userName = ctx.author.name
        userID = ctx.author.id
        guildID = ctx.guild.id
        if not checkUser_Mongo(guildID=guildID, userName=userName):
            await ctx.send("You need to claim somebody first!")
        else:
            em = playingEmbed(ctx=ctx)
            await ctx.send(embed=em)
            addFriendship(ctx.author.name, friendshipToAdd=1)

    @commands.command()
    async def fusion(self, ctx: commands.Context, *args: str):
        """
        Fuse your jam bud!

        Use:
        ```!su fusion```
        This command will let show you possible people your jam bud can fuse with.
        Only those shown in the show are available here (up to the point I've watched at lease)
        Note: Most fusions are spoilers and as such the name of the fusions are redacted on discord.


        Use:
        ```!su fusion (name of a character)```
        This command will actively fuse your jam bud with the character of your choosing, making your new jam bud
        that fusion!
        """
        userName = ctx.author.name
        userID = ctx.author.id
        guildID = ctx.guild.id
        userInput = " ".join(args)
        userInput = userInput.lower()
        # First we make sure that they have a jam bud
        if not checkUser_Mongo(guildID=guildID, userName=userName):
            await ctx.send("You need to claim somebody first!")
        else:
            userDict = returnUserCharacterDict(userName=userName)
            userCharName = userDict["name"]
            userFriendship = userDict["friendship"]
            # print(userDict)
            # Now we need to make sure their friendship level is high enough
            if userFriendship < 20:
                await ctx.send("Your friendship with your jam bud is too low for this!"
                               "\n Use !su play to begin to increase it!")
            else:
                # Here we check if there is an input given by the user
                if userInput == "":
                    # First we need to make sure that that character has cannonically availble fusions.
                    if not fusionCheck(ctx=ctx, userCharacterDict=userDict):
                        # Display message that current character has no fusions.
                        await ctx.send("This jam bud doesn't have any fusions unfortunately.")
                    # If there are availible fusions, we need to display them
                    else:
                        em = displayFusionsEmbed(ctx=ctx, userCharacterDict=userDict)
                        await ctx.send(embed=em)
                else:
                    # Now we know theres an input, here we need to validate it. This should check
                    # If the user input matches something from their fusions check.
                    check = fusionInputCheck(userCharName=userCharName, userInput=userInput)
                    if not check[0]:
                        await ctx.send("This fusion was not found. Please make sure you spelled it right.")
                    else:
                        # At this point, the input has been validated, and we need to convert the fusion
                        fusionFunction(ctx=ctx, userCharDict=userDict, fusionCharName=check[1])
                        em = completedFusionsEmbed(ctx=ctx, oldName=userCharName, newName=check[1])
                        await ctx.send(embed=em)

    @commands.command()
    async def abilities(self, ctx: commands.Context, *args: str):
        """
        Set abilities for your jam bud!
        Note: An Active Ability is the ability that will go into effect during any boss/user battles

        Use:
        ```!su abilities```
        This command will display all abilities your jam bud currently has and a brief description of what they do.
        If you have already selected an Active Ability, it will have stars around its name.

        Use:
        ```!su abilities (name of a valid ability)```
        This command will set the ability you have selected as your Active Ability. This is the buff that will occur
        to your jam bud's stats before any battle.

        Use:
        ```!su abilities none```
        Using the *!su abilities* command followed by the word "none" will un-set your Active Ability so you will
        not have an Active Ability
        """
        userName = ctx.author.name
        userID = ctx.author.id
        guildID = ctx.guild.id
        userInput = " ".join(args[:])
        userInput = userInput.lower()

        # First we want to make sure that the user has a jam bud
        if not checkUser_Mongo(guildID=guildID, userName=userName):
            # Error case that someone uses this command without a jam bud
            em = errorMessageEmbed(ctx=ctx)
            message1 = await ctx.send(embed=em)
            try:
                await message1.delete(delay=5)
            except Exception:
                pass
        else:
            # Now we want to check if there is an input if not
            if userInput == "":
                # Now we check to see if they have an ability
                if not checkUser_Abilities(userName=userName):
                    em1 = noAbilitiesEmbed(ctx=ctx)
                    message2 = await ctx.send(embed=em1)
                    try:
                        await message2.delete(delay=5)
                    except Exception:
                        pass
                else:
                    # Here we've checked that the user's jam bud does have abilities and just display them
                    em2 = abilitiesEmbed(ctx=ctx)
                    await ctx.send(embed=em2)
            elif userInput == "none":
                # Here the input is specifically 'none' and so they do not want an active ability at all.
                abilitySetNoneActive(userName=userName, userInput=userInput)
                msg = "You have no active ability!"
                message2 = await ctx.send(msg)
                try:
                    await message2.delete(delay=5)
                except Exception:
                    pass
            else:
                # Now we need to validate the input
                if not abilityInputCheck(userName=userName, userInput=userInput):
                    await ctx.send("This ability was not found. Make sure you spelled it correctly and try again!")
                else:
                    # Here the input is validated and now we need to set the ability value to true.
                    abilitySetActive(userName=userName, userInput=userInput)
                    msg = f"You have set your active ability to {userInput.upper()}!"
                    message2 = await ctx.send(msg)
                    try:
                        await message2.delete(delay=5)
                    except Exception:
                        pass


def setup(bot: commands.Bot):
    bot.add_cog(character(bot))
