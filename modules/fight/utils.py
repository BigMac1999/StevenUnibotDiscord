import nextcord
import random
from mongoFile import *
from nextcord.ext import commands


def errorMessageEmbed(ctx: commands.Context) -> nextcord.Embed:
    em = nextcord.Embed(title=f'Claim before you take on the bosses!', color=ctx.author.color)
    em.set_thumbnail(url="https://cdn.vox-cdn.com/thumbor/WvLnN4z6SYvpCG5RhYGfnHoZJco=/0x0:1920x1080/1600x900/"
                         "cdn.vox-cdn.com/uploads/chorus_image/image/49197719/a70ab82c-6119-4ea5-988b-"
                         "9aa24e716d9f.0.0.jpg")
    em.description = "You need to claim a jam bud to use this command! Do this with !su claim"
    em.set_footer(text="Steven's Unibot Boss Error Display")
    return em


def displayBossesEmbed(ctx: commands.Context) -> nextcord.Embed:
    em = nextcord.Embed(title=f'Bosses Availible to Fight!', color=ctx.author.color)
    em.set_thumbnail(url="https://cdn.vox-cdn.com/thumbor/WvLnN4z6SYvpCG5RhYGfnHoZJco=/0x0:1920x1080/1600x900/"
                         "cdn.vox-cdn.com/uploads/chorus_image/image/49197719/a70ab82c-6119-4ea5-988b-"
                         "9aa24e716d9f.0.0.jpg")
    em.description = "Pick a boss below and use \n!su boss *boss* \nto fight them!"
    em.set_footer(text="Steven's Unibot Boss Display")
    bosses = returnAllBosses()
    found = False
    userDict = returnUserCharacterBossDict(userName=ctx.author.name)
    for x in range(len(bosses.keys())):
        if bosses[x] == "":
            pass
        else:
            # print(userDict)
            if userDict:
                # print(userDict)
                if bosses[x]['name'] in userDict:
                    em.add_field(name=f"{bosses[x]['name'].upper()}{bosses[x]['emoji']}✅",
                                 value=f'Level: {bosses[x]["level"]}')
                else:
                    # print(f"{bosses[x]['name']} not found")
                    em.add_field(name=f"{bosses[x]['name'].upper()}{bosses[x]['emoji']}",
                                 value=f'Level: {bosses[x]["level"]}')
            else:
                em.add_field(name=f"{bosses[x]['name'].upper()}{bosses[x]['emoji']}",
                             value=f'Level: {bosses[x]["level"]}')
    return em


def bossFightActiveEmbed(ctx: commands.Context, userName: str, boss: str):
    bossDict = returnBossCharacterDict(characterName=boss)
    bossEmoji = bossDict["emoji"]

    userDict = returnUserCharacterDict(userName=userName)
    userEmoji = userDict["emoji"]

    userName = userName.upper()
    boss = boss.upper()
    em = nextcord.Embed(title=f'{userName}{userEmoji} Fights {boss}{bossEmoji}!', color=ctx.author.color)
    em.set_footer(text="Steven's Unibot Boss Fight Display")
    em.description = f"Let the battle between {userName} and {boss} begin!"
    em.add_field(name=f"{userName}{userEmoji}", value="Health:")
    em.add_field(name=f"{boss}{bossEmoji}", value="Health:")
    em.set_thumbnail(url=userDict["image_url"])
    return em


def userFightActiveEmbed(ctx: commands.Context, userName: str, enemyName: str):
    enemyDict = returnUserCharacterDict(userName=enemyName)
    enemyEmoji = enemyDict["emoji"]
    enemyCharName = enemyDict["name"]

    userDict = returnUserCharacterDict(userName=userName)
    userEmoji = userDict["emoji"]
    userCharName = userDict["name"]

    userName = userName.upper()
    enemyName = enemyName.upper()
    em = nextcord.Embed(title=f'{userName}{userEmoji} Fights {enemyName}{enemyEmoji}!', color=ctx.author.color)
    em.set_footer(text="Steven's Unibot PvP Fight Display")
    em.description = f"Let the battle between {userName} and {enemyName} begin!"
    em.add_field(name=f"{userCharName}{userEmoji}", value="Health:")
    em.add_field(name=f"{enemyCharName}{enemyEmoji}", value="Health:")
    em.set_thumbnail(url=userDict["image_url"])
    return em


def alreadyBeatBossEmbed(ctx: commands.Context, userName: str, boss: str) -> nextcord.Embed:
    userName = userName.upper()
    boss = boss.upper()
    em = nextcord.Embed(title=f"{userName}, You've already beaten this boss!", color=ctx.author.color)
    em.set_thumbnail(url="https://cdn.vox-cdn.com/thumbor/WvLnN4z6SYvpCG5RhYGfnHoZJco=/0x0:1920x1080/1600x900/"
                         "cdn.vox-cdn.com/uploads/chorus_image/image/49197719/a70ab82c-6119-4ea5-988b-"
                         "9aa24e716d9f.0.0.jpg")
    em.description = f"You have already beaten {boss}. You are only allowed to challenge and defeat a boss once."
    em.description += "\nPrepare for the next battle you will have with !su train and continue challenging bosses. " \
                      "\nBest of luck!"
    em.set_footer(text="Steven's Unibot Boss Defeated Display")
    return em


def checkBossBeaten(ctx: commands.Context, userName: str, boss: str) -> bool:
    userBosses = returnUserCharacterBossDict(userName=userName)
    for bosses in userBosses:
        if bosses == boss:
            return True
    return False


def abilitiesFunction(guildID: int, userName: str):
    userChar = returnUserCharacterDict(userName=userName)
    userAbilities = returnUserAbilitiesDict(userName=userName)
    # Here we make sure the user has claimed someone
    empty = {}
    if checkUser_Mongo(guildID=guildID, userName=userName):
        # Now we want to make sure they have an active ability
        ability = returnActiveAbility(userName=userName)
        if ability is None:
            print("No Active Ability")
        else:
            userChar['attack'] = int(userChar['attack'] * ability['attack'])
            userChar['defense'] = int(userChar['defense'] * ability['defense'])
            userChar['speed'] = int(userChar['speed'] * ability['speed'])
            return userChar
    return empty

