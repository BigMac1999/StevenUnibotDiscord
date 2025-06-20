import nextcord
import random
import asyncio
from mongoFile import *
from .utils import *
from nextcord.ext import commands


async def fightFunction(ctx: commands.Context, userName: str, enemyUser: str, mess: nextcord.Message, userEnemy: bool):
    embed1 = mess.embeds[0]
    embed1.set_image(url="")

    userChar = abilitiesFunction(guildID=ctx.guild.id, userName=userName)
    # userChar = returnUserCharacterDict(userName=userName)

    userHealth = userChar["health"]
    userSpeed = userChar["speed"]
    userDisplayName = userChar["name"].upper()
    userEmoji = userChar["emoji"]
    userLevel = userChar["level"]

    if userEnemy:
        bossChar = returnUserCharacterDict(userName=enemyUser)
    else:
        bossChar = returnBossCharacterDict(characterName=enemyUser)

    tie = False
    won = False
    gameOver = False
    userDMG = 0
    bossDMG = 0
    turn = 1
    tieTurn = 0

    bossHealth = bossChar["health"]
    bossSpeed = bossChar["speed"]
    bossDisplayName = bossChar["name"].upper()
    bossEmoji = bossChar["emoji"]
    bossLevel = bossChar["level"]

    xpIfWon = random.randint(pow(bossLevel, 2), pow(bossLevel, 3))
    xpIfLose = random.randint(pow(userLevel, 2), pow(userLevel, 3))

    while not gameOver:
        embed = mess.embeds[0]
        embed.clear_fields()
        embed.add_field(name=f"{userDisplayName}{userEmoji}", value=f"Health:{userHealth}")
        embed.add_field(name=f"{bossDisplayName}{bossEmoji}", value=f"Health:{bossHealth}")
        await mess.edit(embed=embed)

        # First we need to calculate the damage done by both the user and char boss
        userDMG = random.randint(int(.5 * userChar["attack"]), userChar["attack"]) - \
                  random.randint(int(.5 * bossChar["defense"]), bossChar["defense"])
        bossDMG = random.randint(int(.5 * bossChar["attack"]), bossChar["attack"]) - \
                  random.randint(int(.5 * userChar["defense"]), userChar["defense"])
        if userDMG < 0:
            userDMG = 0
        if bossDMG < 0:
            bossDMG = 0
        # Now we decide who will go first
        # print(f"User health: {userHealth} speed: {userSpeed} damage: {userDMG}")
        # print(f"Boss health: {bossHealth} speed: {bossSpeed} damage: {bossDMG}")
        if userSpeed > bossSpeed:
            # print("User was faster!")
            # User's turn
            embed.description = f"Turn {turn}\n"
            embed.description += f"{userDisplayName}{userEmoji} is faster!"
            embed.set_thumbnail(url=userChar["image_url"])
            await mess.edit(embed=embed)
            await asyncio.sleep(1)
            bossHealth -= userDMG
            embed.description += f"\n{userDisplayName}{userEmoji} dealt {userDMG} damage!"
            if userDMG == 0:
                embed.description += "\nThe opponents defense was too high! There was no damage!"
            await mess.edit(embed=embed)
            embed.clear_fields()
            embed.add_field(name=f"{userDisplayName}{userEmoji}", value=f"Health:{userHealth}")
            embed.add_field(name=f"{bossDisplayName}{bossEmoji}", value=f"Health:{bossHealth}")
            await mess.edit(embed=embed)
            await asyncio.sleep(1)
            if bossHealth <= 0:
                # print("The boss has been defeated!")
                embed.description = f"{bossDisplayName}{bossEmoji} was defeated!"
                await mess.edit(embed=embed)
                won = True
                gameOver = True
            # Oponents turn
            if not gameOver:
                embed.description = f"Turn {turn}\n"
                embed.description += f"Now it's {bossDisplayName}{bossEmoji}'s turn!"
                embed.set_thumbnail(url=bossChar["image_url"])
                await mess.edit(embed=embed)
                await asyncio.sleep(1)
                userHealth -= bossDMG
                embed.description += f"\n{bossDisplayName}{bossEmoji} dealt {bossDMG} damage!"
                if bossDMG == 0:
                    embed.description += "\nThe opponents defense was too high! There was no damage!"
                await mess.edit(embed=embed)
                embed.clear_fields()
                embed.add_field(name=f"{userDisplayName}{userEmoji}", value=f"Health:{userHealth}")
                embed.add_field(name=f"{bossDisplayName}{bossEmoji}", value=f"Health:{bossHealth}")
                await mess.edit(embed=embed)
                await asyncio.sleep(1)
                if userHealth <= 0:
                    embed.description = f"Turn {turn}\n"
                    # print("The user has been defeated!")
                    embed.description += f"{userDisplayName}{userEmoji} was defeated!"
                    await mess.edit(embed=embed)
                    won = False
                    gameOver = True
        else:
            # print("Boss was faster!")
            # Boss turn
            embed.description = f"Turn {turn}\n"
            embed.description += f"{bossDisplayName}{bossEmoji} is faster!"
            embed.set_thumbnail(url=userChar["image_url"])
            await mess.edit(embed=embed)
            await asyncio.sleep(1)
            userHealth -= bossDMG
            embed.description += f"\n{bossDisplayName}{bossEmoji} dealt {bossDMG} damage!"
            if bossDMG == 0:
                embed.description += "\nThe opponents defense was too high! There was no damage!"
            await mess.edit(embed=embed)
            embed.clear_fields()
            embed.add_field(name=f"{userDisplayName}{userEmoji}", value=f"Health:{userHealth}")
            embed.add_field(name=f"{bossDisplayName}{bossEmoji}", value=f"Health:{bossHealth}")
            await mess.edit(embed=embed)
            await asyncio.sleep(1)
            if userHealth <= 0:
                # print("The user was defeated!")
                embed.description = f"Turn {turn}\n"
                embed.description += f"{userDisplayName}{userEmoji} was defeated!"
                await mess.edit(embed=embed)
                won = False
                gameOver = True
            if not gameOver:
                embed.description = f"Turn {turn}\n"
                embed.description += f"Now it's {userDisplayName}{userEmoji}'s turn!"
                embed.set_thumbnail(url=bossChar["image_url"])
                await mess.edit(embed=embed)
                await asyncio.sleep(1)
                bossHealth -= userDMG
                embed.description += f"\n{userDisplayName}{userEmoji} dealt {userDMG} damage!"
                if userDMG == 0:
                    embed.description += "\nThe opponents defense was too high! There was no damage!"
                await mess.edit(embed=embed)
                embed.clear_fields()
                embed.add_field(name=f"{userDisplayName}{userEmoji}", value=f"Health:{userHealth}")
                embed.add_field(name=f"{bossDisplayName}{bossEmoji}", value=f"Health:{bossHealth}")
                await mess.edit(embed=embed)
                await asyncio.sleep(1)
                if bossHealth <= 0:
                    # print("The boss has been defeated!")
                    embed.description = f"Turn {turn}\n"
                    embed.description += f"{bossDisplayName}{bossEmoji} was defeated!"
                    await mess.edit(embed=embed)
                    won = True
                    gameOver = True
        turn += 1
        if bossDMG == 0 and userDMG == 0:
            tieTurn += 1
            if tieTurn >= 2:
                gameOver = True
                tie = True
        else:
            tieTurn = 0
        if not won:
            xpIfWon = xpIfLose
    return won, tie, turn, xpIfWon


async def fightBoss(ctx: commands.Context, userName: str, enemy: str, mess: nextcord.Message):
    won = False
    tie = False
    turn = 0
    xpIfWon = 0
    won, tie, turn, xpIfWon = await fightFunction(ctx=ctx, userName=userName, enemyUser=enemy,
                                                  mess=mess, userEnemy=False)
    if not tie:
        if not won:
            xpIfWon = 0
        else:
            embed = mess.embeds[0]
            embed.description += f"\nYour jam bud has earned {xpIfWon} XP!"
            await mess.edit(embed=embed)
    else:
        embed = mess.embeds[0]
        embed.description = f"{userName}, the fight ended in a draw!"
        embed.description += f"\nBoth {userName} and {enemy} had too " \
                             f"high of a defense! Nobody could get in a single attack point!"
        await mess.edit(embed=embed)
        xpIfWon = 0
    return won, xpIfWon


async def fightUser(ctx: commands.Context, userName: str, enemyUserName: str, mess: nextcord.Message):
    won, tie, turn, xpIfWon = await fightFunction(ctx=ctx, userName=userName, enemyUser=enemyUserName,
                                                  mess=mess, userEnemy=True)
    if not tie:
        if not won:
            embed = mess.embeds[0]
            embed.description += f"\n{enemyUserName}, Your jam bud has earned {xpIfWon} XP!"
            await mess.edit(embed=embed)
        else:
            embed = mess.embeds[0]
            embed.description += f"\n{userName}, your jam bud has earned {xpIfWon} XP!"
            await mess.edit(embed=embed)
    else:
        embed = mess.embeds[0]
        embed.description = f"{userName}, the fight ended in a draw!"
        embed.description += f"\nBoth {userName}'s jam bud and {enemyUserName}'s jam bud had too " \
                             f"high of a defense! Nobody could get in a single attack point!"
        await mess.edit(embed=embed)
    return won, xpIfWon
