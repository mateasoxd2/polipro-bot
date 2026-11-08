import discord
from discord.ext import commands

# Configuración de permisos del bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Lista de palabras que Polipro va a moderar (agregá las que quieras entre comillas)
MALAS_PALABRAS = ["insulto1", "insulto2", "palabraprohibida"]

@bot.event
async def on_ready():
    print(f'👮 Polipro está patrullando como {bot.user}')

@bot.event
async def on_message(message):
    # Evitar que el bot se responda a sí mismo
    if message.author == bot.user:
        return

    # Verificar si el mensaje contiene alguna palabra prohibida
    contenido = message.content.lower()
    if any(palabra in contenido for palabra in MALAS_PALABRAS):
        try:
            await message.delete()  # Borra el mensaje al instante
            await message.channel.send(f'⚠️ **Polipro:** {message.author.mention}, ¡en este servidor no se permiten malas palabras!')
        except Exception as e:
            print(f"No se pudo borrar el mensaje: {e}")
        return

    await bot.process_commands(message)

# Reemplazá 'MTU2OTAxNjA2NTExODMxNDY0OQ.GCG-qx.JEZ5g90vupMedXCMWay1SesdEuQGp9rmOUTooY' por el token de tu bot de Discord
bot.run('')
