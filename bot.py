import os
import random
import disnake
from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = commands.Bot(command_prefix=".", help_command=None, intents=disnake.Intents.all())

@bot.event
async def on_ready():
    print('Bot is ready')

@bot.command()
async def help(ctx):
    await ctx.message.reply(f".help - Help\n"
                            f".s - Start training")
async def send_random_image(ctx, folder):
    asset_dir = "assets"  # Path to the assets directory
    images = [f for f in os.listdir(os.path.join(asset_dir, folder)) if f.endswith(".png")]
    if images:
        image = random.choice(images)
        with open(os.path.join(asset_dir, folder, image), "rb") as file:
            await ctx.edit(file=disnake.File(file, filename=image))
        return True
    return False


@bot.command()
async def payday(ctx):
    asset_dir = "assets"  # Путь к директории с ресурсами
    buttons = []
    custom_ids = []  # Список для хранения custom_ids
    button = disnake.ui.Button(label='Random', style=disnake.ButtonStyle.blurple, custom_id='random')
    buttons.append(button)
    counter = [0]  # Используем список для хранения значения счетчика

    for folder_name in os.listdir(asset_dir):
        folder_path = os.path.join(asset_dir, folder_name)
        if os.path.isdir(folder_path):
            png_files = [f for f in os.listdir(folder_path) if f.endswith(".png")]
            if png_files:
                custom_id = f"folder_{folder_name}"
                custom_ids.append(custom_id)  # Сохраняем custom_id
                button = disnake.ui.Button(label=folder_name, style=disnake.ButtonStyle.grey, custom_id=custom_id)
                buttons.append(button)

    view = disnake.ui.View(timeout=None)  # Устанавливаем значение timeout в None, чтобы представление было постоянным
    for button in buttons:
        view.add_item(button)

    if len(buttons) < 2:
        message = await ctx.send("Нет доступных папок с изображениями.")
        return

    async def button_callback(interaction, counter=counter):
        if isinstance(interaction, disnake.MessageInteraction):
            await interaction.response.defer()
            counter[0] += 1  # Увеличиваем значение счетчика
            if interaction.component.custom_id != 'random':
                folder = interaction.component.custom_id.split("_")[1]
                image_sent = await send_random_image(message, folder)
                if image_sent:
                    await message.edit(content=f"👨🏽‍🦼: {interaction.author.mention}\n🗺: {folder}\n 📍: {counter[0]}", view=view)
            else:
                image_path, folder_name = await get_random_image()
                if image_path and folder_name:
                    with open(image_path, "rb") as file:
                        await message.edit(content=f"👨🏽‍🦼: {interaction.author.mention}\n🗺: {folder_name}\n 📍: {counter[0]}",
                                           file=disnake.File(file, filename="random.png"))

    # Присвоим обратный вызов каждой кнопке
    for button in buttons:
        button.callback = button_callback

    # Создаем кнопку "end"
    end_button = disnake.ui.Button(emoji='🏁', style=disnake.ButtonStyle.danger, custom_id='end')


    async def end_button_callback(interaction, counter=counter):
        if isinstance(interaction, disnake.MessageInteraction):
            await interaction.response.defer()
            # Редактируем сообщение и оставляем только значение счетчика
            await message.edit(content=f"Результат: {counter[0]}", view=None)

    # Присваиваем обратный вызов кнопке "end"
    end_button.callback = end_button_callback
    view.add_item(end_button)
    message = await ctx.send("Выбери район:", view=view)
    bot.add_view(view)




async def get_random_image():
    asset_dir = "assets"  # Путь к директории с ресурсами
    folders = [folder for folder in os.listdir(asset_dir) if os.path.isdir(os.path.join(asset_dir, folder))]
    if folders:
        random_folder = random.choice(folders)  # Выбираем случайную папку
        images = [f for f in os.listdir(os.path.join(asset_dir, random_folder)) if f.endswith(".png")]
        if images:
            random_image = random.choice(images)  # Выбираем случайное изображение из выбранной папки
            image_path = os.path.join(asset_dir, random_folder, random_image)
            return image_path, random_folder  # Возвращаем путь к изображению и название папки
    return None, None



bot.run(BOT_TOKEN)
