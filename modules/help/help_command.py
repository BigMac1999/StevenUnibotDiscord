from typing import Optional, Set, List

import nextcord
from nextcord.ext import commands
from nextcord import Embed


class MyHelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return f"{self.context.clean_prefix}{command.qualified_name} {command.signature}"

    async def _help_embed(self, title: str, description: Optional[str] = None, mapping: Optional[dict] = None,
                          command_set: Optional[List[commands.Command]] = None):
        embed = nextcord.Embed(title=title)
        embed.set_thumbnail(url="https://cdn.vox-cdn.com/thumbor/WvLnN4z6SYvpCG5RhYGfnHoZJco=/0x0:1920x1080/1600x900/"
                         "cdn.vox-cdn.com/uploads/chorus_image/image/49197719/a70ab82c-6119-4ea5-988b-"
                         "9aa24e716d9f.0.0.jpg")
        embed.set_footer(text="Steven's Unibot Help Message")
        if description:
            embed.description = description
        if command_set:
            # show help about all commands in the set
            filtered = await self.filter_commands(command_set, sort=True)
            for command in filtered:
                embed.add_field(name=self.get_command_signature(command), value=command.qualified_name, inline=False)
        if mapping:
            # Add a short description of commands in each cog
            for cog, command_set in mapping.items():
                filtered = await self.filter_commands(command_set, sort=True)
                if not filtered:
                    continue
                name = cog.qualified_name if cog else "No category"
                cmd_list = "".join(
                    f"`{self.context.clean_prefix}{cmd.name}`\n" for cmd in filtered
                )
                value = (
                    f"{cog.description}\n{cmd_list}"
                    if cog and cog.description
                    else cmd_list
                )
                embed.add_field(name=name, value=value)
            embed.add_field(name="To get help on a specific category",
                            value="Use !su help <> with the name of the command or category you want more help with",
                            inline=False)
            # embed.add_field(name="For any of our minigames:",
            #                 value="Use '/' to see a submenu of your guild's slash commands. Find our bot icon and "
            #                       "select a game from there!\nSome minigames include Wordle, Rock-Paper-Scissors, "
            #                       "and Rolls!",
            #                 inline=False)
            embed.add_field(name="To get started:", value="Use `!su claim` to see all availible characters."
                                                          "Use the instructions on that screen to select one.\n"
                                                          "Once you have selected your jam bud, you can begin to train"
                                                          "them with `!su train`\nOnce you have trained your jam"
                                                          "bud enough, use `!su boss` to see which bosses you can "
                                                          "take on, or use `!su fight <user>` to fight a user"
                                                          "who also already has a jam bud! \nEventually, you can even "
                                                          "use `!su fusion` to see who your jam bud can fuse with and "
                                                          "use `!su abilities` to see your availible abilities and "
                                                          "select which one to use in battle!")

        return embed

    async def send_bot_help(self, mapping: dict):
        embed = await self._help_embed(
            title="Social Credit Bot Commands",
            description=self.context.bot.description,
            mapping=mapping
        )
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command: commands.Command):
        embed = await self._help_embed(
            title=command.qualified_name,
            description=command.help,
            command_set=command.commands if isinstance(command, commands.Group) else None
        )
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog: commands.Cog):
        embed = await self._help_embed(
            title=cog.qualified_name,
            description=cog.description,
            command_set=cog.get_commands()
        )
        await self.get_destination().send(embed=embed)

    send_group_help = send_command_help
