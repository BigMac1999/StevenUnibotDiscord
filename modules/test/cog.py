import nextcord
from nextcord.ext import commands
from mongoFile import *


class Test(commands.Cog, name="Test"):
    """Testing commands for the bot"""

    # load_dotenv()

    # GUILD_IDS = (
    #     [int(guild_id) for guild_id in os.getenv("GUILD_IDS").split(",")]
    #     if os.getenv("GUILD_IDS", None)
    #     else nextcord.utils.MISSING
    # )

    @commands.command()
    async def test(self, ctx: commands.Context):
        """
        First testing command:

        Admins, beware of using this command.
        """
        #await ctx.send("Testing command")
        if ctx.message.author.guild_permissions.administrator:
            await addXP(userName=ctx.author.name, xpToAdd=100000, ctx=ctx)
            addFriendship(userName=ctx.author.name, friendshipToAdd=20)
            msg = "Testing!"
            await ctx.send(msg)
        else:
            msg = "Test"
            await ctx.send(msg)

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # @nextcord.slash_command(name="shop", description="Redeem your Social Credit", guild_ids=GUILD_IDS)
    # async def shop(self, interaction: nextcord.Interaction):
    #     """Open a shop where you can redeem social credit"""
    #     em: nextcord.Embed
    #     em = generate_shop_embed(interaction=interaction)
    #     await interaction.send(embed=em)


def setup(bot: commands.Bot):
    bot.add_cog(Test(bot))
