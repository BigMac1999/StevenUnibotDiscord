import os
import certifi
import nextcord
import nextcord.ext
import pymongo as pymongo
from dotenv import load_dotenv
from pymongo import MongoClient
from nextcord.ext import commands
from pymongo.server_api import ServerApi


def main():
    load_dotenv()

    GUILD_IDS = (
        [int(guild_id) for guild_id in os.getenv("GUILD_IDS").split(",")]
        if os.getenv("GUILD_IDS", None)
        else nextcord.utils.MISSING
    )

    # channelName = "social-credit-bank"

    # load_dotenv()
    # CONNECTION_STRING = os.getenv("CONNECTION_STRING")
    # ca = certifi.where()
    # cluster = MongoClient(CONNECTION_STRING, tlsCAFile=ca)
    # db = cluster["StockCharacters"]
    # collection = db["StevenUniverse"]

    client = commands.Bot(command_prefix="!su ")

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user.name}')
        print(f'{client.user} is connected to the following guilds:\n')
        for x in client.guilds:
            print(f'{x}(id: {x.id})')

    # Automatically checking all folders for cogs
    for folder in os.listdir("modules"):
        if os.path.exists(os.path.join("modules", folder, "cog.py")):
            client.load_extension(f"modules.{folder}.cog")

    @client.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = '***You may only use this command within a certain time frame***, try again in {:.2f} minutes'.format \
                (error.retry_after / 60)
            await ctx.send(msg)

    # @client.event
    # async def on_message(message: nextcord.Message):
    # This will process ! commands
    # await client.process_commands(message)
    # This is the passive text function
    # await on_messageCommand(message=message, client=client)

    TOKEN = os.getenv('DISCORD_TOKEN_SU_TEST')
    client.run(TOKEN)


if __name__ == '__main__':
    main()
