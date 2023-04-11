import os
import discord
# from discord.ui import Button, View
import dotenv

# Set Token
dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

# Create Client
bot = discord.Bot()


'''
    이용 가능 리스트 보여주기 버튼  / followup 삭제
->  이용 가능한 리스트로 버튼이 등장 / disable 이용
->  해당 버튼을 클릭하면 모달이 등장
->  모달에 본인 정보를 제출
->  이용 신청 성공 // 신청자 디코 이름 같이 전송하기
'''


class RequestModal(discord.ui.Modal):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.title = kwargs['title']

        self.add_item(discord.ui.InputText(label="Name", max_length=10))
        self.add_item(discord.ui.InputText(label="Student ID", placeholder='ex) 20231234', min_length=8, max_length=8))
        self.add_item(discord.ui.InputText(label="주의사항을 모두 숙지했나요?", placeholder='Y/N', min_length=1, max_length=1))

    async def callback(self, interaction: discord.Interaction):
        global title
        embed = discord.Embed(title="Successfully Request!")

        embed.add_field(name="이용자", value=self.children[0].value)
        embed.add_field(name="이용 사항", value=self.title)
        embed.add_field(name="반납 날짜", value="2023.04.01")
        await interaction.response.send_message(embeds=[embed])


class AvailableListBtns(discord.ui.View):
    @discord.ui.button(label = "C로 배우는 암호학 프로그래밍", style=discord.ButtonStyle.green, emoji="📕", disabled=False)
    async def click_event1(self, button, interaction):
        await interaction.response.send_modal(RequestModal(title="C로 배우는 암호학 프로그래밍"))

    @discord.ui.button(label = "C로 배우는 암호학 프로그래밍", style=discord.ButtonStyle.green, emoji="📕", disabled=False)
    async def click_event2(self, button, interaction):
        await interaction.response.send_modal(RequestModal(title="C로 배우는 암호학 프로그래밍"))

    @discord.ui.button(label = "리버싱 핵심원리", style=discord.ButtonStyle.green, emoji="📕", disabled=False)
    async def click_event3(self, button, interaction):
        await interaction.response.send_modal(RequestModal(title="리버싱 핵심원리"))

    @discord.ui.button(label = "[인프런] 침투테스트 전문가", style=discord.ButtonStyle.green, emoji="🍂", disabled=False)
    async def click_event4(self, button, interaction):
        await interaction.response.send_modal(RequestModal(title="[인프런] 침투테스트 전문가"))

    @discord.ui.button(label = "Hack The Box VIP Account", style=discord.ButtonStyle.green, emoji="📦", disabled=False)
    async def click_event5(self, button, interaction):
        await interaction.response.send_modal(RequestModal(title="Hack The Box VIP Account"))



class RequestBtn(discord.ui.View):
    @discord.ui.button(label = "Show Available List", style=discord.ButtonStyle.primary, emoji="📌")

    async def click_me(self, button, interaction):
        await interaction.user.send(view=AvailableListBtns())
        # await interaction.response.send_message(view=AvailableListBtns())



@bot.slash_command()
async def send_modal(ctx):
    await ctx.respond(view=RequestBtn())





@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


# run the bot with the token
bot.run(token)
