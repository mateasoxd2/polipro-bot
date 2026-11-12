import os
import discord
from discord.ext import commands

# Configuración de permisos del bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 1. PALABRAS EXACTAS Y ABREVIACIONES (Español, Inglés ampliado, Portugués e Italiano)
PALABRAS_EXACTAS = [
    # Español / Insultos directos y abreviaciones crudas
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
    "cagada", "cagado", "cagar", "cagon", "cagón", "cag",
    "conchudo", "conchuda", "concha", "conch",
    "culiado", "culiao", "culiada", "culia", "culi",
    "mierda", "mrds", "mierd",
    "hdp", "hdspm", "hdsrmpm", "dhrcrmp",
    "maricon", "maricón", "maric", "mrk",
    "pnt", "pnta",
    
    # Inglés (Arsenal completo y pesado + abreviaciones)
    "fuck", "fucking", "fucked", "fucker", "motherfucker", "mf", "fck", "fuk",
    "asshole", "ass", "arse", "arsehole", "bastard", "bitch", "bitches",
    "shit", "shitty", "bullshit", "sht", "cunt", "dick", "dickhead",
    "slut", "whore", "hoe", "thot", "prick", "dumbass", "jackass",
    "crap", "piss", "pissed", "douche", "douchebag", "wanker", "twat",
    "cock", "cocksucker", "pussy", "schlong", "bollocks",
    "nigger", "nigga", "nigg", "faggot", "fag", "retard", "tranny",
    
    # Portugués
    "caralho", "porra", "filho da puta", "fdp", "caral",
    "merda", "viado", "cuzao", "cuzão", "bosta", "cacete", "merd", "viad", "cuz", "bost", "cacet",
    
    # Italiano
    "stronzo", "merda", "vaffanculo", "cazzo", "puttana", 
    "bastardo", "minchia", "cretino", "stronz", "vaffanc", "cazz", "puttan", "minch", "cretin"
]

# 2. RAÍCES UNIVERSALES (Atrapa cualquier deformación, variante nueva o insulto compuesto)
RAICES_PROHIBIDAS = [
    "put", "pndj", "pendej", "idiot", "imbec", "imbcl",
    "verg", "zorr", "malpar", "bolud", "pelotud", "estupid",
    "cag", "conch", "culi", "mierd", "mrds",
    "nigg", "fck", "bitch", "cunt", "bastard", "asshol", "dickhead"
]

def limpiar_texto(texto):
    # Convierte a minúsculas, elimina espacios y normaliza símbolos/números (anti-trampas)
    texto = texto.lower()
    reemplazos = {
        '1': 'i', '3': 'e', '4': 'a', '@': 'a', '0': 'o',
        '5': 's', '$': 's', '7': 't', '8': 'b', ' ': '', '-': '', '_': '', '.': ''
    }
    for char, letra in reemplazos.items():
        texto = texto.replace(char, letra)
    return texto

@bot.event
async def on_ready():
    print(f'👮 Polipro Multilingüe Extremo está patrullando como {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Texto original sin espacios para abreviaciones juntas
    texto_crudo = message.content.lower().replace(" ", "")
    
    # Texto normalizado anti-leetspeak y símbolos
    contenido_limpio = limpiar_texto(message.content)

    violacion = False

    # Verificamos si alguna palabra exacta o abreviatura encaja
    for palabra in PALABRAS_EXACTAS:
        if palabra in texto_crudo or palabra in contenido_limpio:
            violacion = True
            break

    # Si no, revisamos por raíces prohibidas
    if not violacion:
        for raiz in RAICES_PROHIBIDAS:
            if raiz in contenido_limpio:
                violacion = True
                break

    if violacion:
        try:
            await message.delete()
            await message.channel.send(f'{message.author.mention}, ¡imposible burlar a Polipro! Cero tolerancia a insultos en ningún idioma.')
        except Exception as e:
            print(f"No se pudo borrar el mensaje: {e}")

    await bot.process_commands(message)

# Toma el token de forma segura desde las variables de entorno de Railway
bot.run(os.getenv('TOKEN'))
