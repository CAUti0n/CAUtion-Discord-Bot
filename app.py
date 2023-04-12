import os
import discord
# from discord.ui import Button, View
import dotenv
from notion import get_items_info

# Set Discord Token
dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

# Set Channel id
channel_id = int(os.getenv("CHANNEL_ID"))

# Create Client
bot = discord.Bot()


'''
->  이용 신청 성공 // 신청자 디코 이름 같이 전송하기
'''

# Modal when user clicks item button
class ItemRequestModal(discord.ui.Modal):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.title = kwargs['title']

        self.add_item(discord.ui.InputText(label="Name", max_length=10))
        self.add_item(discord.ui.InputText(label="Student ID",
                      placeholder='ex) 20231234', min_length=8, max_length=8))
        self.add_item(discord.ui.InputText(label="주의사항을 모두 숙지했나요?",
                      placeholder='Y/N', min_length=1, max_length=1))

    async def callback(self, interaction: discord.Interaction):
        global title
        embed = discord.Embed(title="Successfully Request!")

        embed.add_field(name="이용자", value=self.children[0].value)
        embed.add_field(name="이용 사항", value=self.title)
        embed.add_field(name="반납 날짜", value="2023.04.01")
        await interaction.response.send_message(embeds=[embed])


# Buttons for each item when user clicks 'Item Request' button at DM
class ItemBtns(discord.ui.View):
    def __init__(self, items, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for item in items:
            disabled = 'False' if item['status'] == '이용 가능' else 'True'
            emoji = ''
            if item['type'] == 'Book':
                emoji = '📕'
            elif item['type'] == 'Lecture':
                emoji = '👁‍🗨'
            elif item['type'] == 'Account':
                emoji = '🔑'

            button = self.create_button(label=item['name'], emoji=emoji, disabled=disabled, id=item['id'])
            self.add_item(button)

    def create_button(self, label, style=discord.ButtonStyle.green, emoji=None, disabled=False, id=None):
        button = discord.ui.Button(label=label, style=style, emoji=emoji, disabled=disabled, custom_id=str(id) + ',' + label)
        button.callback = self.callback
        return button

    async def callback(self, interaction):
        button_label = interaction.data['custom_id'].split(',')[1]
        await interaction.response.send_modal(ItemRequestModal(title=button_label))


# Request Button at public channel
class RequestBtn(discord.ui.View):
    @discord.ui.button(label="Item Request", style=discord.ButtonStyle.primary, emoji="📌")
    async def click_me(self, button, interaction):
        await interaction.user.send(view=ItemBtns(items=get_items_info()))


# when the bot is ready and add the button to the channel
@bot.event
async def on_ready():
    channel = bot.get_channel(1091273144075026514)
    await channel.send(view=RequestBtn())

    print(f"{bot.user} is ready and online!")


# run the bot with the token
bot.run(token)
