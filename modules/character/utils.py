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


def noAbilitiesEmbed(ctx: commands.Context) -> nextcord.Embed:
    em = nextcord.Embed(title=f'No Abilities Unlocked Just Yet!', color=ctx.author.color)
    em.set_thumbnail(url="https://cdn.vox-cdn.com/thumbor/WvLnN4z6SYvpCG5RhYGfnHoZJco=/0x0:1920x1080/1600x900/"
                         "cdn.vox-cdn.com/uploads/chorus_image/image/49197719/a70ab82c-6119-4ea5-988b-"
                         "9aa24e716d9f.0.0.jpg")
    em.description = "Unfortunately your character hasn't leveled up just yet and so your jam bud doesn't " \
                     "have any abilities.\nUse *!su train* to level up your character and unlock some abilities!"
    em.set_footer(text="Steven's Unibot Abilities Error Display")
    return em


def profileEmbed(ctx: commands.Context, userName: str) -> nextcord.Embed:
    characterDict = returnExistingCharacter(userName=userName)
    name = f"{characterDict['name'].upper()}{characterDict['emoji']}"
    urlText = characterDict["image_url"]
    em = nextcord.Embed(title=f"{userName}'s jam bud {name}!", color=ctx.author.color)
    em.set_thumbnail(url="https://cdn.vox-cdn.com/thumbor/WvLnN4z6SYvpCG5RhYGfnHoZJco=/0x0:1920x1080/1600x900/"
                         "cdn.vox-cdn.com/uploads/chorus_image/image/49197719/a70ab82c-6119-4ea5-988b-"
                         "9aa24e716d9f.0.0.jpg")
    em.set_footer(text="Steven's Unibot Profile Display")
    em.add_field(name="Level", value=characterDict["level"])
    em.add_field(name="XP", value=characterDict["xp"])
    em.add_field(name="Health", value=characterDict["health"])
    em.add_field(name="Attack", value=characterDict["attack"])
    em.add_field(name="Defense", value=characterDict["defense"])
    em.add_field(name="Speed", value=characterDict["speed"])
    em.add_field(name="Friendship", value=characterDict["friendship"])
    em.set_image(url=urlText)
    bossBadges = ""
    counter = 0
    userBossDict = returnUserCharacterBossDict(userName=userName)
    if userBossDict:
        for boss in userBossDict:
            bossDict = returnBossCharacterDict(boss)
            emoji = bossDict["emoji"]
            bossBadges += emoji
            counter += 1
        em.add_field(name=f"Bosses Beaten: {counter}", value=bossBadges)
    userCharAbilities = returnUserAbilitiesDict(userName=userName)
    if userCharAbilities:
        for ability in userCharAbilities:
            abilityDict = userCharAbilities[ability]
            em.add_field(name=ability.upper(), value=abilityDict["description"], inline=False)
    return em


def displayEmbed(ctx: commands.Context) -> nextcord.Embed:
    userName = ctx.author.name
    characterDict = returnExistingCharacter(userName=userName)
    name = f"{characterDict['name'].upper()}{characterDict['emoji']}"
    urlText = characterDict["image_url"]
    em = nextcord.Embed(title=f'Your jam bud {name}!', color=ctx.author.color)
    em.set_thumbnail(url="https://cdn.vox-cdn.com/thumbor/WvLnN4z6SYvpCG5RhYGfnHoZJco=/0x0:1920x1080/1600x900/"
                         "cdn.vox-cdn.com/uploads/chorus_image/image/49197719/a70ab82c-6119-4ea5-988b-"
                         "9aa24e716d9f.0.0.jpg")
    em.set_footer(text="Steven's Unibot Character Display")
    em.add_field(name="Level", value=characterDict["level"])
    em.add_field(name="XP", value=characterDict["xp"])
    em.add_field(name="Health", value=characterDict["health"])
    em.add_field(name="Attack", value=characterDict["attack"])
    em.add_field(name="Defense", value=characterDict["defense"])
    em.add_field(name="Speed", value=characterDict["speed"])
    em.add_field(name="Friendship", value=characterDict["friendship"])
    em.set_image(url=urlText)
    bossBadges = ""
    counter = 0
    userBossDict = returnUserCharacterBossDict(userName=userName)
    if userBossDict:
        for boss in userBossDict:
            bossDict = returnBossCharacterDict(boss)
            emoji = bossDict["emoji"]
            bossBadges += emoji
            counter += 1
        em.add_field(name=f"Bosses Beaten: {counter}", value=bossBadges, inline=False)
    userCharAbilities = returnUserAbilitiesDict(userName=userName)
    if userCharAbilities:
        em.add_field(name="Abilities", value="vvvvvvvvvvvvv", inline=False)
        for ability in userCharAbilities:
            abilityDict = userCharAbilities[ability]
            if abilityDict['active']:
                em.add_field(name=f'🌟{ability.upper()}🌟', value=abilityDict["description"], inline=False)
            else:
                em.add_field(name=ability.upper(), value=abilityDict["description"], inline=False)
    return em


def displayBossEmbed(ctx: commands.Context, boss: str) -> nextcord.Embed:
    # userName = ctx.author.name
    # characterDict = returnExistingCharacter(userName=userName)
    boss = boss.lower()
    characterDict = returnBossCharacterDict(characterName=boss)
    name = f"{characterDict['name'].upper()}{characterDict['emoji']}"
    urlText = characterDict["image_url"]
    em = nextcord.Embed(title=f'{name}!', color=ctx.author.color)
    em.set_thumbnail(url="https://cdn.vox-cdn.com/thumbor/WvLnN4z6SYvpCG5RhYGfnHoZJco=/0x0:1920x1080/1600x900/"
                         "cdn.vox-cdn.com/uploads/chorus_image/image/49197719/a70ab82c-6119-4ea5-988b-"
                         "9aa24e716d9f.0.0.jpg")
    em.set_footer(text="Steven's Unibot Boss Display")
    em.add_field(name="Level", value=characterDict["level"])
    em.add_field(name="Health", value=characterDict["health"])
    em.add_field(name="Attack", value=characterDict["attack"])
    em.add_field(name="Defense", value=characterDict["defense"])
    em.add_field(name="Speed", value=characterDict["speed"])
    em.set_image(url=urlText)
    return em


def trainingEmbed(ctx: commands.Context):
    userName = ctx.author.name
    characterDict = returnExistingCharacter(userName=userName)
    level = int(characterDict["level"])
    name = f"{characterDict['name'].upper()}{characterDict['emoji']}"
    n = random.randint(pow(level, 2), pow(level, 3))
    em = nextcord.Embed(title=f'Time to train!', color=ctx.author.color)
    em.set_thumbnail(url="https://68.media.tumblr.com/b3be32d1e1455b3ac60927c998194977/"
                         "tumblr_nlvwmusTnG1qjjp8ho1_500.gif")
    em.description = f"You train with your jam bud {name}, having them fight Holo-Pearl!"
    em.add_field(name="The training is successful!", value=f"Your jam bud {name} has gained {n} experience!")
    return [em, n]


def playingEmbed(ctx: commands.Context) -> nextcord.Embed:
    userName = ctx.author.name
    characterDict = returnExistingCharacter(userName=userName)
    name = f"{characterDict['name'].upper()}{characterDict['emoji']}"
    friendshipToAdd = 1

    em = nextcord.Embed(title=f'Time to train!', color=ctx.author.color)
    em.set_thumbnail(url="http://68.media.tumblr.com/7dc415c94cf28325ac753e16c300248d/"
                         "tumblr_o56c78eg3K1u8eo0po1_500.gif")
    em.description = f"{userName} plays with their jam bud {name}!"
    em.add_field(name="After a nice playdate",
                 value=f"Your jam bud {name} has gained {friendshipToAdd} friendship level!")
    addFriendship(userName=userName, friendshipToAdd=friendshipToAdd)
    return em


def abilitiesEmbed(ctx: commands.Context):
    userName = ctx.author.name
    charAbilities = returnUserAbilitiesDict(userName=userName)
    em = nextcord.Embed(title=f'Select your *Active Ability*!', color=ctx.author.color)
    em.set_thumbnail(url="https://static.miraheze.org/animatedmusclewomenwiki/thumb/e/e3/Steven_Universe_"
                         "S01E33_%E2%80%94_Garnet_struggle_under_the_weight_of_her_giant_gauntlets.gif/270px-"
                         "Steven_Universe_S01E33_%E2%80%94_Garnet_struggle_under_the_weight_of_her_giant_gauntlets.gif")
    em.description = f"{userName} select your active ability. This is the one that will activate before battle" \
                     f" and can mean the difference between victory or defeat!\nTo select your Active Ability:\n" \
                     f"`!su abilities *name of ability*`"

    for ability in charAbilities:
        # print(ability)
        dic = charAbilities[ability]
        # print(dic)
        abilityString = f"*{dic['description']}*" \
                        f"\nAttack: **x{dic['attack']}**" \
                        f"\nDefense: **x{dic['defense']}**" \
                        f"\nSpeed: **x{dic['speed']}**"
        em.add_field(name=ability.upper(), value=abilityString)
    return em
