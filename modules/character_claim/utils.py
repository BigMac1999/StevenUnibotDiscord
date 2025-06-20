import nextcord
from nextcord.ext import commands
from mongoFile import *
from .utils import *


def inputCheck(userInput: str) -> bool:
    load_dotenv()
    CONNECTION_STRING = os.getenv("CONNECTION_STRING")
    ca = certifi.where()
    cluster = MongoClient(CONNECTION_STRING, tlsCAFile=ca)
    db = cluster["StockCharacters"]
    collection = db["StevenUniverse"]

    searchDict = {"character.name": userInput}
    results = collection.find_one({"_id": userInput})
    if results is None:
        return False
    return True


def displayCharactersForClaim(ctx: commands.Context) -> nextcord.Embed:
    em = nextcord.Embed(title=f'Jam Buds Availible to claim!', color=ctx.author.color)
    em.set_thumbnail(url="https://cdn.vox-cdn.com/thumbor/WvLnN4z6SYvpCG5RhYGfnHoZJco=/0x0:1920x1080/1600x900/"
                         "cdn.vox-cdn.com/uploads/chorus_image/image/49197719/a70ab82c-6119-4ea5-988b-"
                         "9aa24e716d9f.0.0.jpg")
    em.description = "Pick a jam bud below and use \n!su claim *name* \nto claim them as a jam bud!"
    em.set_footer(text="Steven's Unibot Character Claim Display")
    companions = returnAllCharacters()
    for x in range(len(companions.keys())):
        if companions[x] == "":
            pass
        else:
            em.add_field(name=f"{companions[x]['name'].upper()}{companions[x]['emoji']}",
                         value=f'Level: {companions[x]["level"]}')
    return em
