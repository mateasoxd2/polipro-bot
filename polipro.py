import os
import discord
from discord.ext import commands

# Configuración de permisos del bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Lista de palabras que Polipro va a moderar
MALAS_PALABRAS = ["insulto1", "insulto2", "palabraprohibida"]

@bot.event
async def on_ready():
    print(f'👮 Polipro está patrullando como {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    contenido = message.content.lower()
    if any(palabra in contenido for palabra in MALAS_PALABRAS):
        try:
            await message.delete()
            await message.channel.send(f'⚠️ **Polipro:** {message.author.mention}, ¡en este servidor no se permiten malas palabras!')
        except Exception as e:
            print(f"No se pudo borrar el mensaje: {e}")

    await bot.process_commands(message)

# Toma el token de forma segura desde las variables de entorno de Railway
bot.run(os.getenv('TOKEN'))
