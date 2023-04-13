import traceback
import discord
import call_notion_api


# Modal when user clicks item button
class ItemRequestModal(discord.ui.Modal):

    def __init__(self, data, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        print(data)

        self.add_item(discord.ui.InputText(label="Name", max_length=10))
        self.add_item(discord.ui.InputText(label="Student ID",
                      placeholder='ex) 20231234', min_length=8, max_length=8))
        self.add_item(discord.ui.InputText(label="주의사항을 모두 숙지했나요?",
                      placeholder='Y/N', min_length=1, max_length=1))

    # Request item using notion api
    # request_item(self.id, )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Successfully Request!")

        embed.add_field(name="User", value=self.children[0].value)
        embed.add_field(name="Item", value=f'{self.id}#{self.title}')
        embed.add_field(name="Due Date", value="2023.04.01")
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

    async def callback(self, interaction):
        data = interaction.data['custom_id'].split(
            ',').append(interaction.user)
        await interaction.response.send_modal(ItemRequestModal(title=data[0], data=data))


# Request Button at public channel
class RequestBtn(discord.ui.View):
    @discord.ui.button(label="Item Request", style=discord.ButtonStyle.primary, emoji="📌")
    async def click_me(self, button, interaction):
        await interaction.user.send(view=ItemBtns(items=call_notion_api.get_item_list()))
