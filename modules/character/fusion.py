import nextcord
import random
import asyncio
from mongoFile import *
from .utils import *
from nextcord.ext import commands


def fusionFunction(ctx: commands.Context, userCharDict: dict, fusionCharName: str):
    # Here we need to take their current character, take the old stats, and reset the level.
    # print("Prior dict:")
    # print(userCharDict)
    currentCharDict = userCharDict
    # print("first fusion char dict")
    fusionCharDict = returnFusionCharacterDict(characterName=fusionCharName)
    # print(fusionCharDict)
    # Here we need to set the stats.
    fusionCharDict["health"] = currentCharDict["health"]
    fusionCharDict["attack"] = currentCharDict["attack"]
    fusionCharDict["defense"] = currentCharDict["defense"]
    fusionCharDict["speed"] = currentCharDict["speed"]
    fusionCharDict["level"] = 1
    fusionCharDict["xp"] = 0
    fusionCharDict["friendship"] = currentCharDict["friendship"]
    deleteCharacterAbilities(guildID=ctx.guild.id, userName=ctx.author.name)
    updateCharacterDict(userName=ctx.author.name, charDict=fusionCharDict)
    # print("Post Dict:")
    # print(fusionCharDict)


def fusionCheck(ctx: commands.Context, userCharacterDict: dict) -> bool:
    name = userCharacterDict["name"]
    if boolFusionsCheck(characterName=name):
        return True
    else:
        return False


def displayFusionsEmbed(ctx: commands.Context, userCharacterDict: dict) -> nextcord.Embed:
    em = nextcord.Embed(title=f'Fusions Available for your Jam Bud!', color=ctx.author.color)
    em.set_thumbnail(url="https://cdn.vox-cdn.com/thumbor/WvLnN4z6SYvpCG5RhYGfnHoZJco=/0x0:1920x1080/1600x900/"
                         "cdn.vox-cdn.com/uploads/chorus_image/image/49197719/a70ab82c-6119-4ea5-988b-"
                         "9aa24e716d9f.0.0.jpg")
    em.description = "Pick a fusion below and use \n!su fusion *character to fuse* \nto fuse with them!" \
                     "\n *Because many fusions are a spoiler, any spoilers will be marked off with a spoiler -> ||spoiler||*"
    em.set_footer(text="Steven's Unibot Fusion Display")
    # print(userCharacterDict["name"])
    fusions = returnFusionsForCharacter(characterName=userCharacterDict["name"])
    # print(fusions)
    for char in fusions:
        dic = fusions[char]
        # print(dic)
        em.add_field(name=dic['fusion'].upper(), value=f"||{char.upper()}{dic['emoji']}||")
    return em


def completedFusionsEmbed(ctx: commands.Context, oldName: str, newName: str) -> nextcord.Embed:
    em = nextcord.Embed(title=f'{ctx.author.name}, your jam bud {oldName.upper()} turned into {newName.upper()}!',
                        color=ctx.author.color)
    em.set_thumbnail(url="https://cdn.vox-cdn.com/thumbor/WvLnN4z6SYvpCG5RhYGfnHoZJco=/0x0:1920x1080/1600x900/"
                         "cdn.vox-cdn.com/uploads/chorus_image/image/49197719/a70ab82c-6119-4ea5-988b-"
                         "9aa24e716d9f.0.0.jpg")
    em.description = f"Your jam bud {oldName.upper()}'s fusion is complete! Your jam bud is now {newName.upper()}!" \
                     f"\nTheir stats have stayed the same but their level has been reset which will allow you two " \
                     f"to grow even stronger!"
    em.set_footer(text="Steven's Unibot Fusion Complete Display")
    return em
