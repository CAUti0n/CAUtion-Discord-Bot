import os
import discord
import dotenv

# Set Token
dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

# Create Client
bot = discord.Bot()



# class MyView(discord.ui.View):
#     @discord.ui.button(label = "Click me!", style=discord.ButtonStyle.primary, emoji="😎")
#     async def click_me(self, button, interaction):
#         await interaction.response.send_message("You clicked me!")

#     @discord.ui.button(label = "Click me!2", style=discord.ButtonStyle.primary, emoji="😎")
#     async def click_me2(self, button, interaction):

#         await interaction.response.send_message("You clicked me!2")


class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Short Input"))
        self.add_item(discord.ui.InputText(label="Long Input", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modal Results")
        embed.add_field(name="Short Input", value=self.children[0].value)
        embed.add_field(name="Long Input", value=self.children[1].value)
        await interaction.response.send_message(embeds=[embed])


class MyView2(discord.ui.View):
    @discord.ui.button(label="Send Modal")
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(MyModal(title="Modal via Button"))

# class MyView3(discord.ui.View):
#     @discord.ui.select( # the decorator that lets you specify the properties of the select menu
#         placeholder = "Choose a Flavor!", # the placeholder text that will be displayed if nothing is selected
#         min_values = 1, # the minimum number of values that must be selected by the users
#         max_values = 1, # the maximum number of values that can be selected by the users
#         options = [ # the list of options from which users can choose, a required field
#             discord.SelectOption(
#                 label="Vanilla",
#                 description="Pick this if you like vanilla!"
#             ),
#             discord.SelectOption(
#                 label="Chocolate",
#                 description="Pick this if you like chocolate!"
#             ),
#             discord.SelectOption(
#                 label="Strawberry",
#                 description="Pick this if you like strawberry!"
#             )
#         ]
#     )
#     async def select_callback(self, select, interaction): # the function called when the user is done selecting options
#         await print(interaction)
#         await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")


# @bot.command()
# async def flavor(ctx):
#     await ctx.send("Choose a flavor!", view=MyView3())



# @bot.slash_command()
# async def send_modal(ctx):
#     await ctx.respond(view=MyView2())



# @bot.slash_command(name = "hello", description = "Say hello to the bot")
# async def hello(ctx):
#     await ctx.respond("Hey!")



@bot.slash_command(name = "view", description = "Send a view")
async def view(ctx):
    await ctx.respond("Here's a view!", view = MyView())


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

bot.run(os.getenv('TOKEN')) # run the bot with the token
