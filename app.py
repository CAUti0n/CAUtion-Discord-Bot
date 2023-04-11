import discord
import config

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == "안녕":
            await message.channel.send('안녕하세요')

intents = discord.Intents.default()
# intents.message_content = True
client = MyClient(intents=intents)

client.run(config.TOKEN)
