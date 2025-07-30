import discord
from discord.ext import commands


class MugenBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix="8!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print("Commands synchronized with Discord.")
