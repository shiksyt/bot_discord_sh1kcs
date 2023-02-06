# At the top of the file.
import disnake
from disnake.ext import commands
from disnake import TextInputStyle

intents = disnake.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="?", intents=intents)


class MyModal(disnake.ui.Modal):
    def __init__(self):
        # The details of the modal, and its components
        components = [
            disnake.ui.TextInput(
                label="Ваш никнейм",
                placeholder="SosiskaKiller",
                custom_id="Name",
                style=TextInputStyle.short,
                max_length=20,
            ),
            disnake.ui.TextInput(
                label="Сколько вам лет?",
                placeholder="56",
                custom_id="Let",
                style=TextInputStyle.short,
                max_length=2,
            ),
        ]
        super().__init__(title="Create Tag", components=components)

    # The callback received when the user input is completed.
    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(title="Заявка")
        for key, value in inter.text_values.items():
            embed.add_field(
                name=key.capitalize(),
                value=value[:1024],
                inline=False,
            )
        await inter.response.send_message(embed=embed)

class TicketModal(disnake.ui.Modal):
    def __init__(self, type: int):
        # The details of the modal, and its components
        self.type = type
        if type == 1:
            components = [
                disnake.ui.TextInput(
                    label="Ваш никнейм",
                    placeholder="SosiskaKiller",
                    custom_id="Ник",
                    style=TextInputStyle.short,
                    max_length=20,
                ),
                disnake.ui.TextInput(
                    label="Сколько вам лет?",
                    placeholder="56",
                    custom_id="Лет",
                    style=TextInputStyle.short,
                    max_length=2,
                ),
                disnake.ui.TextInput(
                    label="Что вы можете сделать для нас?",
                    placeholder="Я могу кушать!",
                    custom_id="О себе",
                    style=TextInputStyle.paragraph,
                    max_length=300,
                ),
            ]
            title = "Заявка!"
        elif type == 2:
            components = [
                disnake.ui.TextInput(
                    label="Ваш ник",
                    placeholder="SosiskaKiller",
                    custom_id="Ник",
                    style=TextInputStyle.short,
                    max_length=20,
                ),
                disnake.ui.TextInput(
                    label="На что жалоба",
                    placeholder="На админов",
                    custom_id="Проблема",
                    style=TextInputStyle.short,
                    max_length=50,
                ),
                disnake.ui.TextInput(
                    label="Подробная информация",
                    placeholder="Его имя кира Ёшикаге",
                    custom_id="Больше информации",
                    style=TextInputStyle.paragraph,
                    max_length=1000,
                ),
            ]
            title = "Помощь админа"
        super().__init__(title=title, components=components)

    # The callback received when the user input is completed.
    async def callback(self, inter: disnake.ModalInteraction):
        if self.type == 1:
            channel = await inter.guild.create_text_channel(name=f"заявка-{inter.author}", category= inter.guild.get_channel(1071849211341050008))
            user= await bot.fetch_user(inter.author.id)
            await channel.set_permissions(user, read_messages=True, send_messages=True)
            embed = disnake.Embed(title="Заявка")
            for key, value in inter.text_values.items():
                embed.add_field(
                    name=key.capitalize(),
                    value=value[:1024],
                    inline=False,
                )
            await inter.response.send_message(embed=embed, ephemeral=True)
            await channel.send(
                embed=embed,
                components=[
                disnake.ui.Button(label="Закрыть тикет", style=disnake.ButtonStyle.success, custom_id="close_ticket"),
                ],
                )
        elif self.type == 2:
            channel = await inter.guild.create_text_channel(name=f"поддержка-{inter.author}", category= inter.guild.get_channel(1071849328030793739))
            user= await bot.fetch_user(inter.author.id)
            await channel.set_permissions(user, read_messages=True, send_messages=True)
            embed = disnake.Embed(title="Поддержка")
            for key, value in inter.text_values.items():
                embed.add_field(
                    name=key.capitalize(),
                    value=value[:1024],
                    inline=False,
                )
            await inter.response.send_message(embed=embed, ephemeral=True)
            await channel.send(
                embed=embed,
                components=[
                disnake.ui.Button(label="Закрыть тикет", style=disnake.ButtonStyle.success, custom_id="close_ticket"),
                ],
                )

async def _create_ticket(inter: disnake.AppCmdInter):
    await inter.response.send_message(
        embed= disnake.Embed().add_field(name="Создать тикет.", value="Нажми на нужную кнопку.", inline=True),
        components=[
            disnake.ui.Button(label="Подать заявку!", style=disnake.ButtonStyle.success, custom_id="new_bro"),
            disnake.ui.Button(label="Помощь администрации!", style=disnake.ButtonStyle.success, custom_id="admin_help"),
        ]
    )

async def _tags(inter):
    await inter.response.send_modal(modal=MyModal())

embed1 = disnake.Embed(title="Проверка", description=f"Проверяем...", color=0xffffff)
print("Бот готов к работе!")


# The slash command that responds with a message.
@bot.slash_command()
async def buttons(inter: disnake.ApplicationCommandInteraction):
    await inter.response.send_message(
        "Заявка.",
        components=[
            disnake.ui.Button(label="Подать заявку!", style=disnake.ButtonStyle.success, custom_id="yes"),
        ],
    )

@bot.listen("on_button_click")
async def help_listener(inter: disnake.MessageInteraction):
    if inter.component.custom_id == "yes":
        await _tags(inter)
    elif inter.component.custom_id == "new_bro":
        await inter.response.send_modal(modal=TicketModal(1))
    elif inter.component.custom_id == "admin_help":
        await inter.response.send_modal(modal=TicketModal(2))
    elif inter.component.custom_id == "close_ticket":
        await inter.channel.delete()

@bot.slash_command()
async def tags(inter: disnake.AppCmdInter):
    """Sends a Modal to create a tag."""
    await inter.response.send_modal(modal=MyModal())

#@bot.slash_command()
#async def create_ticket(inter: disnake.AppCmdInter):
#    await _create_ticket(inter)


bot.run("MTA3MTM3NzU0MzM2Nzc3NDMwOA.GWP3Ja.JWSLEYAefyp8llX6GoifuQuYzM3GqyaOenUXNI")
