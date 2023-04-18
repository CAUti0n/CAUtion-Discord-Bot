import traceback
import discord
import call_notion_api



# Notion link Button
class NotionLinkBtn(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="⭐Please check the item list⭐", style=discord.ButtonStyle.link, url='https://caution.notion.site/a6d18194cf6947fcbe34124e333e818a?v=d8ae0beaf886433a9090b1f5de0eca34'))


# Modal when user clicks item button
class ItemRequestModal(discord.ui.Modal):

    # Constructor
    def __init__(self, requestInfo, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.item_id = requestInfo[0]
        self.item_name = requestInfo[1]
        self.user_name = requestInfo[2]

        self.add_item(discord.ui.InputText(label="Name", max_length=10))
        self.add_item(discord.ui.InputText(label="Student ID",
                      placeholder='ex) 20231234', min_length=8, max_length=8))
        self.add_item(discord.ui.InputText(label="주의사항을 모두 숙지했나요?",
                      placeholder='Y/N', min_length=1, max_length=1))

    # Button callback function
    async def callback(self, interaction: discord.Interaction):

        # Check if user inputted all the required fields
        if self.children[2].value != 'Y' and self.children[2].value != 'y':
            await interaction.response.send_message("⚠주의사항을 모두 숙지하지 않았습니다.", ephemeral=True)
            return

        # Request item using notion api
        try:
            call_notion_api.request_item(int(self.item_id), f'({self.children[1].value}){self.children[0].value}/{self.user_name}')
        except:
            traceback.print_exc()
            await interaction.response.send_message("⚠Failed to request item :( Please contact manager.", ephemeral=True)
            return

        # Send embed message
        embed = discord.Embed(title="Successfully Request!")
        embed.add_field(name="User", value=self.children[0].value)
        embed.add_field(name="Item", value=f'{self.item_id}#{self.item_name}')

        await interaction.response.send_message(embed=embed, view=NotionLinkBtn())



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
            else:
                emoji = '❌'

            button = self.create_button(
                label=item['name'], emoji=emoji, disabled=disabled, id=item['id'])
            self.add_item(button)

    def create_button(self, label, style=discord.ButtonStyle.green, emoji=None, disabled=False, id=None):
        button = discord.ui.Button(
            label=label, style=style, emoji=emoji, disabled=disabled, custom_id=str(id) + ',' + label)
        button.callback = self.callback
        return button

    # Button callback function
    async def callback(self, interaction):

        # data = [item_id, item_name, user]
        data = interaction.data['custom_id'].split(',')
        data.append(interaction.user.name)
        await interaction.response.send_modal(ItemRequestModal(title=data[1], requestInfo=data))


# Request Button at public channel
class RequestBtn(discord.ui.View):
    @discord.ui.button(label="Item Request", style=discord.ButtonStyle.primary, emoji="📌")

    # Button callback function
    async def callback(self, button, interaction):
        await interaction.user.send(view=ItemBtns(items=call_notion_api.get_item_list()))

