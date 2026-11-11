import os
import discord
from discord.ext import commands

# Configuración de permisos del bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Lista completa y blindada (palabras enteras + abreviaciones + raíces)
PALABRAS_PROHIBIDAS = [
    # Español / Abreviaciones / Raíces / Recortes
    "puto", "putita", "putear", "putaza", "puta", "putanga", "put",
    "pendejo", "pendeja", "pendejito", "pndj", "pendej",
    "idiota", "idioteces", "idiot",
    "imbecil", "imbécil",
    "verga", "vergas", "vergota", "verg",
    "zorra", "zorrita", "zorron", "zorrón", "zorr",
    "malparido", "malparida", "malpar",
    "boludo", "boluda", "boludito", "bolud",
    "pelotudo", "pelotuda", "pelotud",
    "estupido", "estúpida", "estupida", "estúpido", "estupid",
    "cagada", "cagado", "cagar", "cagon", "cagón", "cag",
    "conchudo", "conchuda", "concha", "conch",
    "culiado", "culiao", "culiada", "culia", "culi",
    "mierda", "mrds", "mierd",
    "putas", "putos", "ptas", "ptos",
    
    # Inglés
    "fuck", "fucking", "fucked", "motherfucker", "asshole", "fck", "fuk",
    "bitch", "shit", "bullshit", "cunt", "dick", "sht",
    "bastard", "slut", "whore", "prick", "dumbass",
    
    # Portugués
    "caralho", "porra", "puta", "filho da puta", "fdp", "caral",
    "merda", "viado", "cuzao", "cuzão", "bosta", "cacete", "merd", "viad", "cuz", "bost", "cacet",
    
    # Italiano
    "stronzo", "merda", "vaffanculo", "cazzo", "puttana", 
    "bastardo", "minchia", "cretino", "stronz", "vaffanc", "cazz", "puttan", "minch", "cretin"
]

def limpiar_texto(texto):
    # Convierte a minúsculas y reemplaza números/símbolos comunes por letras (anti-trampas)
    texto = texto.lower()
    reemplazos = {
        '1': 'i',
        '3': 'e',
        '4': 'a',
        '@': 'a',
        '0': 'o',
        '5': 's',
        '$': 's',
        '7': 't',
        '8': 'b'
    }
    for char, letra in reemplazos.items():
        texto = texto.replace(char, letra)
    return texto

@bot.event
async def on_ready():
    print(f'👮 Polipro Definitivo está patrullando como {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Limpiamos el texto de trampas numéricas y símbolos
    contenido_limpio = limpiar_texto(message.content)

    # Revisamos si alguna palabra o abreviatura está contenida en el mensaje
    if any(palabra in contenido_limpio for palabra in PALABRAS_PROHIBIDAS):
        try:
            await message.delete()
            await message.channel.send(f'{message.author.mention}, ¡acá no se salta el filtro ni con números ni con abreviaciones, cero malas palabras!')
        except Exception as e:
            print(f"No se pudo borrar el mensaje: {e}")

    await bot.process_commands(message)

# Toma el token de forma segura desde las variables de entorno de Railway
bot.run(os.getenv('TOKEN'))
