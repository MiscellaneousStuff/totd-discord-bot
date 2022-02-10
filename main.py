import os

from dotenv import load_dotenv
from discord.ext.commands import bot
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

class TotdBot(commands.Cog):

    def __init__(self, guild, rhythm_channel_id):
        self.guild = guild
        self.rhythm_channel_id = int(rhythm_channel_id)
        super(TotdBot, self).__init__()

    async def on_ready(self):
        for guild in self.guilds:
            if guild.name == self.guild:
                break
            print(
                f'{self.user} is connected to the following guild:\n'
                f'{guild.name}(id: {guild.id})'
            )

        rhythm_channel = bot.get_channel(self.rhythm_channel_id)
        await rhythm_channel.send(f"{self.user} joined to provide the totd playlist.")

    @commands.command(pass_context=True)
    async def playlist(self, ctx, *args):
        rhythm_channel = bot.get_channel(self.rhythm_channel_id)
        messages = await rhythm_channel.history(limit=100).flatten()
        playlist = []
        for m in messages:
            content = m.content
            if "open.spotify.com" in content:
                playlist.append(content)
            elif "https://www.youtube.com/watch" in content:
                playlist.append(content)
        await rhythm_channel.send("Getting current spotify and youtube tracks")

if __name__ == "__main__":
    load_dotenv()
    TOKEN      = os.getenv('DISCORD_TOKEN')
    GUILD      = os.getenv('DISCORD_GUILD')
    CHANNEL_ID = os.getenv('DISCORD_RHYTHM_CHANNEL_ID')

    bot.add_cog(TotdBot(GUILD, CHANNEL_ID))
    bot.run(TOKEN)