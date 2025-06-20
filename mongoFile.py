import os
import random
import ssl
import certifi
import nextcord
import pymongo as pymongo
from dotenv import load_dotenv
from nextcord.ext import commands
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Connection Segment:
# load_dotenv()
# CONNECTION_STRING = os.getenv("CONNECTION_STRING")
# ca = certifi.where()
# cluster = MongoClient(CONNECTION_STRING, tlsCAFile=ca)
# db = cluster["StockCharacters"]
# collection = db["StevenUniverse"]


# Default pearl values:
#
# "name": "pearl",
# "health": 50,
# "attack": 20,
# "defense": 10,
# "speed": 20,
# "level": 1,
# "xp": 0,
# "friendship": 0,
# "image_url": "https://media1.tenor.com/images/41ca8af78b781d8a92a81ed2ed04ee1e/tenor.gif?itemid=13791581"

load_dotenv()
CONNECTION_STRING = os.getenv("CONNECTION_STRING")
ca = certifi.where()
cluster = MongoClient(CONNECTION_STRING, tlsCAFile=ca)


def returnUserJSON_CreateBlank(guildID: int, username: str, userID: int, characterName: str):
    db = cluster["StockCharacters"]
    collection = db["StevenUniverse"]
    results = collection.find_one({f"{characterName}.level": 1})
    userAdd = {
        "_id": username,
        "guildID": guildID
    }
    # print(userAdd)
    return userAdd


def returnStockCharacterDict(characterName: str):
    db = cluster["StockCharacters"]
    collection = db["StevenUniverse"]

    results = collection.find({"_id": characterName})
    # print("Results from returnStockChar")
    if results is None:
        pass
    else:
        for result in results:
            dic: dict
            dic = result["character"]
            # print(dic)
            return dic


def returnUserCharacterDict(userName: str):
    db = cluster["StockCharacters"]
    collection = db["UserCharacters"]

    results = collection.find({"_id": userName})
    # print("Results from returnStockChar")
    if results is None:
        pass
    else:
        for result in results:
            dic: dict
            dic = result["character"]
            # print(dic)
            return dic


def returnUserAbilitiesDict(userName: str):
    db = cluster["StockCharacters"]
    collection = db["UserCharacters"]

    results = collection.find({"_id": userName})
    # print("Results from returnStockChar")
    try:
        if results is None:
            pass
        else:
            for result in results:
                dic: dict
                dic = result["abilities"]
                # print(dic)
                return dic
    except Exception:
        pass


def returnUserCharacterBossDict(userName: str):
    db = cluster["StockCharacters"]
    collection = db["UserCharacters"]

    results = collection.find({"_id": userName})
    # print("Results from returnStockChar")
    if results is None:
        pass
    else:
        for result in results:
            dic: dict
            dic = result["bosses"]
            # print(dic)
            return dic


def returnBossCharacterDict(characterName: str):
    db = cluster["StockCharacters"]
    collection = db["Bosses"]

    results = collection.find({"_id": characterName})
    # print("Results from returnStockChar")
    if results is None:
        pass
    else:
        for result in results:
            dic: dict
            dic = result["character"]
            # print(dic)
            return dic


def returnFusionCharacterDict(characterName: str):
    db = cluster["StockCharacters"]
    collection = db["Fusions"]

    results = collection.find({"_id": characterName})
    # print("Results from returnStockChar")
    if results is None:
        print(f"Error: {characterName} fusion not found")
    else:
        for result in results:
            dic: dict
            dic = result["character"]
            # print(dic)
            return dic


def createBlankUserAccount(ctx: commands.Context):
    username = ctx.author.name
    userID = ctx.author.id
    guildID = ctx.guild.id
    db = cluster["StockCharacters"]
    collection = db["UserCharacters"]

    userAdd = {
        "_id": username,
        "userID": userID,
        "guildID": guildID,
        "character": {},
        "bosses": {}
    }
    collection.insert_one(userAdd)


def checkUser_Mongo(guildID: int, userName: str) -> bool:
    db = cluster["StockCharacters"]
    collection = db["UserCharacters"]
    results = collection.find({"_id": userName})
    if results is None:
        return False
    else:
        for result in results:
            return True
    return False


def checkUser_Abilities(userName: str) -> bool:
    db = cluster["StockCharacters"]
    collection = db["UserCharacters"]

    results = collection.find({"_id": userName})
    # print("Results from returnStockChar")
    if results is None:
        print(f"Error: {userName} fusion not found")
    else:
        for result in results:
            dic: dict
            try:
                dic = result["abilities"]
                for ability in result["abilities"]:
                    return True
            except Exception:
                pass
    return False


def claimCharacter(guildID: int, userName: str, character: str):
    db = cluster["StockCharacters"]
    collection = db["UserCharacters"]
    if checkUser_Mongo(guildID=guildID, userName=userName):
        character = returnStockCharacterDict(characterName=character)
        collection.update_one({"_id": userName, "guildID": guildID}, {"$set": {"character": character}})
        # print("Added User " + userName + " of guild " + str(guildID) + " with character " + str(character))


def unclaimCharacter(guildID: int, userName: str):
    db = cluster["StockCharacters"]
    collection = db["UserCharacters"]
    if checkUser_Mongo(guildID=guildID, userName=userName):
        # collection.update_one({"_id": userName, "guildID": guildID}, {"$set": {"character": {}}})
        collection.delete_one({"_id": userName})
        # print("Added User " + userName + " of guild " + str(guildID) + " with character " + str(character))


def deleteCharacterAbilities(guildID: int, userName: str):
    db = cluster["StockCharacters"]
    collection = db["UserCharacters"]
    if checkUser_Mongo(guildID=guildID, userName=userName):
        collection.update_one({"_id": userName, "guildID": guildID}, {"$unset": {"abilities": ""}})


def returnExistingCharacter(userName: str):
    db = cluster["StockCharacters"]
    collection = db["UserCharacters"]

    results = collection.find({"_id": userName})
    # print("Results from returnExistingChar")
    if results is None:
        pass
    else:
        for result in results:
            dic: dict
            dic = result["character"]
            # print(dic)
            return dic


def updateCharacterDict(userName: str, charDict: dict):
    db = cluster["StockCharacters"]
    collection = db["UserCharacters"]

    collection.update_one({"_id": userName}, {"$set": {"character": charDict}})


async def addXP(userName: str, xpToAdd: int, ctx: commands.Context):
    # Function will only be called when it is known the user has an account
    db = cluster["StockCharacters"]
    collection = db["UserCharacters"]

    levelUp = False
    healthString = ""
    attackString = ""
    defenseString = ""
    speedString = ""

    # Get current XP value
    userDict = returnExistingCharacter(userName=userName)
    currentXP = int(userDict["xp"])
    currentLevel = int(userDict["level"])
    oldXP = int(userDict["xp"])
    oldLevel = int(userDict["level"])
    # Add xpToAdd to currentXP
    newXP = currentXP + xpToAdd
    levelThreshold = pow(currentLevel, 3)
    nextLevelThreshold = pow(currentLevel + 1, 3)
    if newXP >= levelThreshold:
        levelUp = True
    if levelUp:
        healthString = f'{userDict["health"]}/'
        attackString = f'{userDict["attack"]}/'
        defenseString = f'{userDict["defense"]}/'
        speedString = f'{userDict["speed"]}/'
        # If it does level up, check that it only levels up once
        if (newXP - levelThreshold) < nextLevelThreshold:
            currentXP = newXP - levelThreshold
            currentLevel += 1
            userDict['level'] = currentLevel
            userDict = levelUpStatBuff(charDict=userDict, guildID=ctx.guild.id, userName=userName)
        # If it levels up more than once, we need to make a loop to remove XP until it is within range
        if newXP - levelThreshold >= nextLevelThreshold:
            # Checks if theres at least two levels to go
            while newXP - levelThreshold >= nextLevelThreshold:
                newXP -= levelThreshold
                currentLevel += 1
                userDict['level'] = currentLevel
                userDict = levelUpStatBuff(charDict=userDict, guildID=ctx.guild.id, userName=userName)
                levelThreshold = pow(currentLevel, 3)
                nextLevelThreshold = pow(currentLevel + 1, 3)
                # Checks if there is one level to go:
                if (newXP - levelThreshold) < nextLevelThreshold:
                    newXP = newXP - levelThreshold
                    currentLevel += 1
                    userDict['level'] = currentLevel
                    userDict = levelUpStatBuff(charDict=userDict, guildID=ctx.guild.id, userName=userName)
            currentXP = newXP
    # If the character didn't level up, we can just add the XP and be done.
    else:
        # print("Character didn't level up")
        currentXP = newXP
    # At this point, currentXP and currentLevel are updated, now we want to update the dict
    userDict["xp"] = currentXP
    userDict["level"] = currentLevel
    # and then database
    collection.update_one({"_id": userName}, {"$set": {"character": userDict}})
    newDict = returnExistingCharacter(userName=userName)
    if levelUp:
        collection.update_one({"_id": userName}, {"$set": {"character": userDict}})
        em = nextcord.Embed(title=f'{userName}, Your jam bud {userDict["name"].upper()} leveled up!',
                            color=ctx.author.color)
        em.set_thumbnail(url="http://i2.kym-cdn.com/photos/images/original/001/193/161/f96.gif")
        em.add_field(name="Old Level/XP:", value=f"{oldLevel}/{oldXP}")
        em.add_field(name="New Level/XP:", value=f"{currentLevel}/{currentXP}")
        em.add_field(name="Old/New Health:", value=f'{healthString}{userDict["health"]}')
        em.add_field(name="Old/New Attack:", value=f'{attackString}{userDict["attack"]}')
        em.add_field(name="Old/New Defense:", value=f'{defenseString}{userDict["defense"]}')
        em.add_field(name="Old/New Speed:", value=f'{speedString}{userDict["speed"]}')
        em.set_footer(text="Steven's Unibot Level Up Message")
        message1 = await ctx.send(embed=em)
        # To be implemented later:
        try:
            await message1.delete(delay=10)
        except Exception:
            pass


def addAbilities(guildID: int, userName: str, charName: str, charLevel: int):
    db = cluster["StockCharacters"]
    collection = db["UserCharacters"]
    # Here we make sure the user has claimed someone
    if checkUser_Mongo(guildID=guildID, userName=userName):
        dic = returnUserAbilitiesDict(userName=userName)
        # Now we want to check if they hit a level they gain an ability.
        collection = db["StevenUniverse"]
        results = collection.find({"_id": charName})
        if results is None:
            return False
        else:
            for result in results:
                abilities = result["abilities"]
                for ability in abilities:
                    if int(ability) == charLevel:
                        if dic is None:
                            dic = abilities[ability]
                        else:
                            dic.update(abilities[ability])
                        collection = db["UserCharacters"]
                        collection.update_one({"_id": userName, "guildID": guildID}, {"$set": {"abilities": dic}})
                        return
        collection = db["Fusions"]
        results = collection.find({"_id": charName})
        if results is None:
            return False
        else:
            for result in results:
                abilities = result["abilities"]
                for ability in abilities:
                    if int(ability) == charLevel:
                        if dic is None:
                            dic = abilities[ability]
                        else:
                            dic.update(abilities[ability])
                        collection = db["UserCharacters"]
                        collection.update_one({"_id": userName, "guildID": guildID}, {"$set": {"abilities": dic}})
                        return



def abilitiesLevelCheck(charName: str, level: int) -> bool:
    db = cluster["StockCharacters"]
    collection = db["StevenUniverse"]
    results = collection.find({"_id": charName})
    if results is None:
        print("This must be a fusion at abilitiesLeveLCheck")
        return False
    else:
        for result in results:
            # print(result)
            abilities = result["abilities"]
            # print(abilities)
            for ability in abilities:
                # print(level)
                # print(ability)
                if int(ability) == level:
                    # print(f"Ability found at level {level}")
                    return True

    collection = db["Fusions"]
    results = collection.find({"_id": charName})
    if results is None:
        return False
    else:
        for result in results:
            abilities = result["abilities"]
            for ability in abilities:
                if int(ability) == level:
                    print(f"Ability found at level {level}")
                    return True

def levelUpStatBuff(charDict: dict, guildID: int, userName: str) -> dict:
    db = cluster["StockCharacters"]
    collection = db["StevenUniverse"]

    level = int(charDict["level"])
    factor = random.uniform(0.0, 0.2)
    charDict["health"] = int(int(charDict["health"]) + factor * charDict["health"])
    factor = random.uniform(0.0, 0.2)
    charDict["attack"] = int(int(charDict["attack"]) + factor * charDict["attack"])
    factor = random.uniform(0.0, 0.2)
    charDict["defense"] = int(int(charDict["defense"]) + factor * charDict["defense"])
    factor = random.uniform(0.0, 0.2)
    charDict["speed"] = int(int(charDict["speed"]) + factor * charDict["speed"])
    # print("HERE!")
    if abilitiesLevelCheck(charName=charDict["name"].lower(), level=level):
        # print("HERE")
        addAbilities(guildID=guildID, userName=userName, charName=charDict['name'], charLevel=charDict['level'])
    return charDict


def returnAllBosses():
    db = cluster["StockCharacters"]
    collection = db["Bosses"]
    boss = {0: "", 1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "", 10: ""}
    results = collection.find().sort("character.level", pymongo.ASCENDING)
    counter = 0
    for result in results:
        boss[counter] = result["character"]
        counter += 1
    return boss


def returnAllCharacters():
    db = cluster["StockCharacters"]
    collection = db["StevenUniverse"]
    companions = {0: "", 1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "", 10: ""}
    results = collection.find()
    counter = 0
    for result in results:
        companions[counter] = result["character"]
        counter += 1
    return companions


def addDefeatedBossToUser(userName: str, boss: str):
    db = cluster["StockCharacters"]
    collection = db["UserCharacters"]
    userDict = returnUserCharacterBossDict(userName=userName)
    userDict[boss] = True
    collection.update_one({"_id": userName}, {"$set": {"bosses": userDict}})


def bossInputCheck(userInput: str) -> bool:
    db = cluster["StockCharacters"]
    collection = db["Bosses"]

    results = collection.find_one({"_id": userInput})
    if results is None:
        # print("This boss was not found. inputCheck failed for " + userInput)
        return False
    return True


def addFriendship(userName: str, friendshipToAdd: int):
    characterDict = returnUserCharacterDict(userName=userName)
    characterDict["friendship"] += friendshipToAdd
    updateCharacterDict(userName=userName, charDict=characterDict)


def returnFusionsForCharacter(characterName: str):
    db = cluster["StockCharacters"]
    collection = db["StevenUniverse"]

    results = collection.find({"_id": characterName})
    # print(results)
    # print(results["fusions"])
    # return results["fusions"]
    if results is None:
        pass
    else:
        for result in results:
            dic: dict
            dic = result["fusions"]
            # print(dic)
            return dic


def boolFusionsCheck(characterName: str):
    db = cluster["StockCharacters"]
    collection = db["StevenUniverse"]

    results = collection.find({"_id": characterName})
    # print(results)
    if results is None:
        pass
    else:
        for result in results:
            try:
                if result["fusions"]:
                    return True
            except Exception:
                pass
    return False


def fusionInputCheck(userCharName: str, userInput: str):
    db = cluster["StockCharacters"]
    collection = db["StevenUniverse"]
    check = False

    results = collection.find_one({"_id": userCharName})
    if results is None:
        return False
    else:
        dic = results["fusions"]
        if dic:
            for char in dic:
                newDic = dic[char]
                if newDic['fusion'] == userInput:
                    return True, char
        else:
            # print("False1")
            return False
    # print("False2")
    return False


def abilityInputCheck(userName: str, userInput: str):
    db = cluster["StockCharacters"]
    collection = db["UserCharacters"]
    check = False

    results = collection.find_one({"_id": userName})
    if results is None:
        # print("This userCharName was not found. inputCheck failed for " + userInput)
        return False
    else:
        dic = results["abilities"]
        if dic:
            for char in dic:
                if char == userInput:
                    return True
        else:
            return False
    return False


def returnActiveAbility(userName: str):
    db = cluster["StockCharacters"]
    collection = db["UserCharacters"]
    check = False

    results = collection.find_one({"_id": userName})
    if results is None:
        # print("This userCharName was not found. inputCheck failed for " + userInput)
        return False
    else:
        dic = results["abilities"]
        if dic:
            for char in dic:
                dic1 = dic[char]
                if dic1['active']:
                    return dic1


def abilitySetActive(userName: str, userInput: str):
    db = cluster["StockCharacters"]
    collection = db["UserCharacters"]
    check = False

    results = collection.find_one({"_id": userName})
    if results is None:
        # print("This userCharName was not found. inputCheck failed for " + userInput)
        return False
    else:
        dic = results["abilities"]
        if dic:
            for char in dic:
                if char == userInput:
                    dic[char]['active'] = True
                else:
                    dic[char]['active'] = False
            collection.update_one({"_id": userName}, {"$set": {"abilities": dic}})

def abilitySetNoneActive(userName: str, userInput: str):
    db = cluster["StockCharacters"]
    collection = db["UserCharacters"]
    check = False

    results = collection.find_one({"_id": userName})
    if results is None:
        # print("This userCharName was not found. inputCheck failed for " + userInput)
        return False
    else:
        dic = results["abilities"]
        if dic:
            for char in dic:
                dic[char]['active'] = False
            collection.update_one({"_id": userName}, {"$set": {"abilities": dic}})
