import os
import discord
from discord.ext import commands

# Configuración de permisos del bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 1. PALABRAS EXACTAS Y ABREVIACIONES (Diccionario definitivo + términos de odio/discriminación)
PALABRAS_EXACTAS = [
    # Español / Insultos directos, abreviaciones y modismos
    "puto", "putita", "putear", "putaza", "puta", "putanga", "put", "pto", "pta", "ptas", "ptos",
    "pendejo", "pendeja", "pendejito", "pndj", "pendej",
    "idiota", "idioteces", "idiot",
    "imbecil", "imbécil", "imbcil", "imbezil",
    "verga", "vergas", "vergota", "verg",
    "zorra", "zorrita", "zorron", "zorrón", "zorr",
    "malparido", "malparida", "malpar",
    "boludo", "boluda", "boludito", "bolud",
    "pelotudo", "pelotuda", "pelotud",
    "estupido", "estúpida", "estupida", "estúpido", "estupid",
    "cagada", "cagado", "cagar", "cagon", "cagón", "cag", "kgd", "kgada", "kgado",
    "conchudo", "conchuda", "concha", "conch",
    "culiado", "culiao", "culiada", "culia", "culi", "culero", "culera", "culeros",
    "mierda", "mrds", "mierd", "mielda",
    "hdp", "hdspm", "hdsrmpm", "dhrcrmp",
    "maricon", "maricón", "maric", "mrk", "marik",
    "pnt", "pnta", "tarado", "tarada",
    
    # Términos de odio, discriminación y racismo (Nuevos de las capturas)
    "hitler", "nazi", "nigga", "nigger", "nigg", "negros", "negro", "faggot", "fag",
    "retard", "tranny",
    
    # Inglés (Arsenal completo y pesado + abreviaciones)
    "fuck", "fucking", "fucked", "fucker", "motherfucker", "mf", "fck", "fuk",
    "asshole", "ass", "arse", "arsehole", "bastard", "bitch", "bitches",
    "shit", "shitty", "bullshit", "sht", "cunt", "dick", "dickhead",
    "slut", "whore", "hoe", "thot", "prick", "dumbass", "jackass",
    "crap", "piss", "pissed", "douche", "douchebag", "wanker", "twat",
    "cock", "cocksucker", "pussy", "schlong", "bollocks",
    
    # Portugués
    "caralho", "porra", "filho da puta", "fdp", "caral",
    "merda", "viado", "cuzao", "cuzão", "bosta", "cacete", "merd", "viad", "cuz", "bost", "cacet",
    
    # Italiano
    "stronzo", "merda", "vaffanculo", "cazzo", "puttana", 
    "bastardo", "minchia", "cretino", "stronz", "vaffanc", "cazz", "puttan", "minch", "cretin"
]

# 2. RAÍCES UNIVERSALES (Atrapa variaciones nuevas, racistas, odiosas y deformadas)
RAICES_PROHIBIDAS = [
    "put", "pndj", "pendej", "idiot", "imbec", "imbcl",
    "verg", "zorr", "malpar", "bolud", "pelotud", "estupid",
    "cag", "kg", "conch", "culi", "mierd", "mrds", "mield",
    "nigg", "fck", "bitch", "cunt", "bastard", "asshol", "dickhead", "tarad",
    "hitler", "nazi", "negr"
]

def limpiar_texto(texto):
    # Convierte a minúsculas, elimina espacios, guiones, puntos y normaliza leetspeak
    texto = texto.lower()
    reemplazos = {
        '1': 'i', '3': 'e', '4': 'a', '@': 'a', '0': 'o',
        '5': 's', '$': 's', '7': 't', '8': 'b', 
        ' ': '', '-': '', '_': '', '.': '', ',': '', ';': ''
    }
    for char, letra in reemplazos.items():
        texto = texto.replace(char, letra)
    return texto

@bot.event
async def on_ready():
    print(f'👮 Polipro Versión 3.0 Ultra Blindado operativo como {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Múltiples capas de análisis para que ninguna trampa pase
    texto_crudo = message.content.lower()
    texto_sin_espacios = message.content.lower().replace(" ", "")
    contenido_limpio = limpiar_texto(message.content)

    violacion = False

    # Capa 1: Verificación de palabras exactas / abreviaciones
    for palabra in PALABRAS_EXACTAS:
        if palabra in texto_crudo or palabra in texto_sin_espacios or palabra in contenido_limpio:
            violacion = True
            break

    # Capa 2: Verificación por raíces universales
    if not violacion:
        for raiz in RAICES_PROHIBIDAS:
            if raiz in contenido_limpio or raiz in texto_sin_espacios:
                violacion = True
                break

    if violacion:
        try:
            await message.delete()
            await message.channel.send(f'{message.author.mention}, NOPE.')
        except Exception as e:
            print(f"No se pudo borrar el mensaje: {e}")

    await bot.process_commands(message)

# Toma el token de forma segura desde las variables de entorno de Railway
bot.run(os.getenv('TOKEN'))
