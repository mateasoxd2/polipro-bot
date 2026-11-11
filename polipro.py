import os
import discord
from discord.ext import commands

# Configuración de permisos del bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Lista ampliada de palabras prohibidas (todas en minúsculas porque el filtro usa .lower())
MALAS_PALABRAS = [
    "puto", "putita", "putear", "putaza",
    "puta", "putita", "putanga",
    "pendejo", "pendeja", "pendejito",
    "idiota", "idioteces",
    "imbecil", "imbécil",
    "verga", "vergas", "vergota",
    "zorra", "zorrita", "zorron", "zorrón",
    "malparido", "malparida",
    "boludo", "boluda", "boludito",
    "pelotudo", "pelotuda",
    "estupido", "estúpida", "estupida", "estúpido",
    "cagada", "cagado", "cagar",
    "conchudo", "conchuda", "concha"
]

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
            await message.channel.send(f'{message.author.mention}, ¡en este servidor no se permiten malas palabras!')
        except Exception as e:
            print(f"No se pudo borrar el mensaje: {e}")

    await bot.process_commands(message)

# Toma el token de forma segura desde las variables de entorno de Railway
bot.run(os.getenv('TOKEN'))
