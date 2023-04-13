import os
import discord
# from discord.ui import Button, View
import dotenv

from ui import RequestBtn

# Set Discord Token
dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

# Set Channel id
channel_id = int(os.getenv("CHANNEL_ID"))

# Create Client
bot = discord.Bot()


# when the bot is ready and add the button to the channel
@bot.event
async def on_ready():

    channel = bot.get_channel(channel_id)
    await channel.send(view=RequestBtn.RequestBtn())

    print(f"{bot.user} is ready and online!")


# run the bot with the token
bot.run(token)
