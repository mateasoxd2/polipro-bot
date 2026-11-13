import re
import unicodedata
import os
from datetime import datetime
import discord
from discord.ext import commands

# Configuración de permisos del bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ============================================================
# POLIPRO 4.0 - MOTOR ANTI-EVASIÓN
# ============================================================

# Caracteres visualmente parecidos
CONFUSABLES = str.maketrans({
    "а": "a", "е": "e", "о": "o", "р": "p",
    "с": "c", "х": "x", "у": "y", "і": "i",
    "к": "k", "м": "m", "т": "t", "в": "b",
    "Α": "a", "Β": "b", "Ε": "e", "Ι": "i",
    "Ο": "o", "Ρ": "p", "Τ": "t"
})

LEETSPEAK = str.maketrans({
    "1": "i",
    "3": "e",
    "4": "a",
    "@": "a",
    "0": "o",
    "5": "s",
    "$": "s",
    "7": "t",
    "8": "b",
    "9": "g",
    "!": "i",
    "+": "t"
})


def normalizar(texto):

    texto = texto.lower()

    # Caracteres visualmente similares
    texto = texto.translate(CONFUSABLES)

    # Eliminar acentos
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(
        c for c in texto
        if not unicodedata.combining(c)
    )

    # Convertir números y símbolos
    texto = texto.translate(LEETSPEAK)

    # Reducir letras repetidas
    texto = re.sub(r"(.)\1{2,}", r"\1", texto)

    return texto


# ============================================================
# CREACIÓN DE PATRONES
# ============================================================

def crear_patron(palabra, raiz=False):

    palabra = normalizar(palabra)

    partes = re.findall(r"\w+", palabra)

    if not partes:
        return None

    # Permite símbolos entre letras
    partes = [
        r"[^\w]*".join(re.escape(letra) for letra in parte)
        for parte in partes
    ]

    # Permite separar las palabras de una expresión
    cuerpo = r"[^\w]+".join(partes)

    if raiz:
        return re.compile(r"(?<!\w)" + cuerpo + r"\w*", re.IGNORECASE)

    return re.compile(
        r"(?<!\w)" + cuerpo + r"(?!\w)",
        re.IGNORECASE
    )


# ============================================================
# DETECTOR PRINCIPAL
# ============================================================

# Palabras normales que contienen "puta" como parte de otra palabra.
# Evita que el detector por subcadena bloquee estos casos comunes.
EXCEPCIONES_PUTO_PUTA = {
    "computadora",
    "computadoras",
    "reputacion",
    "reputaciones",
    "reputacional",
    "reputacionales",
}


def detectar_infraccion(texto):

    texto = normalizar(texto)

    # Capa especial: detectar "puto" o "puta" incluso dentro de otra
    # cadena, por ejemplo: "jhjhputogdejmierda".
    # Se revisan palabras completas (tokens) y se excluyen excepciones
    # comunes para reducir falsos positivos.
    for token in re.findall(r"\\w+", texto):
        if token in EXCEPCIONES_PUTO_PUTA:
            continue

        if "puto" in token or "puta" in token:
            coincidencia = "puto" if "puto" in token else "puta"
            return ("subcadena puto/puta", coincidencia)

    # Primera capa: palabras y expresiones exactas
    for patron in PATRONES_EXACTOS:
        coincidencia = patron.search(texto)
        if coincidencia:
            return ("palabra exacta", coincidencia.group(0))

    # Segunda capa: raíces y derivados
    for patron in PATRONES_RAICES:
        coincidencia = patron.search(texto)
        if coincidencia:
            return ("raíz o derivado", coincidencia.group(0))

    return None


# ============================================================
# REGISTRO PRIVADO DE INFRACCIONES
# ============================================================

def registrar_infraccion(message, tipo, coincidencia):

    fecha = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    canal = getattr(message.channel, "name", "canal-desconocido")

    # Guardamos solamente la coincidencia detectada, no el mensaje completo.
    registro = (
        f"[{fecha}] Usuario: {message.author} (ID: {message.author.id}) | "
        f"Canal: #{canal} | Regla: {tipo} | Coincidencia: {coincidencia}\n"
    )

    try:
        with open("polipro_registros.txt", "a", encoding="utf-8") as archivo:
            archivo.write(registro)
    except OSError as error:
        print(f"ERROR al guardar el registro de Polipro: {error}")

    print(registro.rstrip())


# ============================================================
# POLIPRO 4.0 - DICCIONARIO INTERNACIONAL
# ============================================================

PALABRAS_EXTRA = [

    # ==================== ESPAÑOL ====================

    "forro", "forra", "forrito", "forrada",

    # Insultos detectados en las pruebas con Cher
    "verga", "pene", "puta", "puto", "crj", "carajo",
    "jueputa", "pto", "ptoo", "pendejo", "jpta",
    "poliputo", "hijuetuputamare", "hijueputamare", "kgn", "polqria", "plqria", "polqueria", "plqueria", "prqueria"
    "pinga", "poronga", "kgda", "taraado", "porqueria", "escoria", "porqria", "prqria", "xqria", "prqueria", "xqueria",

    "pito", "cagada",
    "garca", "garcar", "garcador",
    "choto", "chota", "chotazo",
    "salame", "mamerto", "mamerta",
    "gil", "gila", "gilastrun",
    "sorete", "soret", "soretito",
    "cornudo", "cornuda", "cornudazo",
    "payaso", "payasa", "pajero", "pajera",
    "pajerito", "pajerazo", "pelmazo",
    "pringado", "pringada", "inutil", "subnormal",
    "capullo", "cabrón", "cabron", "cabrona",
    "gilipollas", "jilipollas", "cojudo",
    "mamaguevo", "mamavergas", "come mierda",
    "hijueputa", "hijueputas", "malnacido",
    "malnacida", "desgraciado", "desgraciada",
    "imbecilidad", "estupidez", "taradez",
    "chupapijas", "chupaverga", "chupamedias",
    "rompebolas", "rompehuevos", "tragasables",
    "retrasado", "retrasada", "bocón", "bocon",
    "bocona", "culorroto", "culo roto",

    # ==================== INGLÉS ====================

    "dumbfuck", "dipshit", "shithead", "fuckwit",
    "fuckface", "scumbag", "jackhole",
    "douchecanoe", "asswipe", "asshat",
    "dickwad", "dickweed", "twatwaffle",
    "shitstain", "dipstick", "motherfucking",
    "dumbass", "dumbassery", "bullshitter",
    "shitbag", "shitbrain", "shitforbrains",
    "fuckhead", "fucknugget", "fucktard",
    "cockhead", "cockwomble", "wanker",
    "bellend", "knobhead", "tosser",
    "git", "minger", "numpty", "pillock",
    "arsewipe", "arsehat", "arseface",
    "prick", "twit", "moron", "cretin",
    "dunce", "scumbucket", "jackassery",

    # ==================== PORTUGUÉS ====================

    "arrombado", "arrombada", "desgraçado",
    "desgracado", "desgraçada", "desgracada",
    "babaca", "otário", "otario", "otária",
    "otaria", "idiota", "corno", "corna",
    "corno manso", "escroto", "escrota",
    "fdp", "filhodaputa", "filhodaput",
    "filha da puta", "puta que pariu",
    "vai tomar no cu", "vai se foder",
    "buceta", "boceta", "piranha", "vagabundo",
    "vagabunda", "lixo humano", "desgraça",
    "babacão", "babacao", "otário de merda",

    # ==================== FRANCÉS ====================

    "connard", "connasse", "enculé", "encule",
    "enculer", "salope", "connerie", "bordel",
    "bâtard", "batard", "ordure", "débile",
    "debile", "abruti", "abrutie", "couillon",
    "emmerdeur", "emmerdeuse", "foutre",
    "niqueur", "niqueuse", "ta gueule",
    "ferme ta gueule", "va te faire foutre",
    "fils de pute", "sale con", "grosse merde",
    "trou du cul", "branleur", "branleuse",

    # ==================== ALEMÁN ====================

    "arschloch", "fick", "ficken", "gefickt",
    "wichser", "hurensohn", "hure", "fotze",
    "mistkerl", "schlampe", "vollidiot",
    "blödmann", "blodmann", "drecksack",
    "schwanz", "kacke", "scheisse", "scheiße",
    "arsch", "arschgeige", "drecksau",
    "schweinehund", "fick dich", "verpiss dich",
    "missgeburt", "spast", "pissnelke",

    # ==================== ITALIANO ====================

    "stronzo", "stronza", "stronzata",
    "vaffanculo", "cazzo", "cazzata",
    "puttana", "bastardo", "bastarda",
    "minchia", "cretino", "cretina",
    "coglione", "cogliona", "figlio di puttana",
    "pezzo di merda", "testa di cazzo",
    "rompicoglioni", "troia", "merdoso",
    "porcodio", "porco dio", "mannaggia",
    "incapace", "deficiente", "scemo", "scema",

    # ==================== NEERLANDÉS ====================

    "klootzak", "eikel", "lul", "kut",
    "tering", "tyfus", "godverdomme",
    "sukkel", "klootviool", "hufter",
    "kanker", "hondelul", "klootzak",
    "pannenkoek", "mongool", "debiel",

    # ==================== POLACO ====================

    "kurwa", "kurwy", "chuj", "chujowy",
    "pierdol", "pierdolic", "pierdole",
    "skurwysyn", "dupa", "gówno", "gowno",
    "jebany", "jebac", "jebak", "pojeb",
    "spierdalaj", "wypierdalaj", "sukinsyn",
    "dziwka", "debil", "kretyn",

    # ==================== RUSO ====================

    "блядь", "сука", "хуй", "пизда",
    "ебать", "ебаный", "мудак", "гандон",
    "дерьмо", "сволочь", "ублюдок",
    "пидор", "пидорас", "залупа",
    "blyat", "suka", "khuy", "pizda",
    "yebat", "mudak", "dermo",
    "pidor", "pidoras", "zalupa",

    # ==================== JAPONÉS ====================

    "くそ", "ばか", "あほ", "ちくしょう",
    "やろう", "くそったれ", "死ね",
    "kuso", "baka", "aho", "chikushou",
    "yarou", "kusottare", "shine",
    "kisama", "temee",

    # ==================== COREANO ====================

    "씨발", "시발", "개새끼", "병신",
    "좆", "지랄", "꺼져", "미친놈",
    "미친년", "개자식", "씹새끼",
    "ssibal", "gaesaekki", "byeongsin",
    "jiral", "kkeojyeo", "michinnom",

    # ==================== TURCO ====================

    "siktir", "orospu", "pic", "piç",
    "salak", "aptal", "bok", "pezevenk",
    "yavsak", "yavşak", "göt", "got",
    "amcik", "amcık", "serefsiz",
    "şerefsiz", "ibne", "kahpe",

    # ==================== ÁRABE ====================

    "كلب", "حمار", "قحبة", "شرموطة",
    "كس", "زب", "خرا", "احمق",
    "kalb", "himar", "sharmuta", "ahbal",
    "khara", "ibn kalb", "kos ommak",

    # ==================== SUECO ====================

    "fan", "jävlar", "javlar", "helvete",
    "skit", "arsle", "fitta", "kuk",
    "hora", "idiot", "skithög", "skitstövel",

    # ==================== NORUEGO ====================

    "faen", "helvete", "jævel", "jaevel",
    "dritt", "kuk", "fitte", "hore",
    "drittsekk", "rasshøl",

    # ==================== DANÉS ====================

    "forhelvede", "lort", "røvhul",
    "roevhul", "pik", "kraftedeme",
    "røv", "fuckhoved", "skiderik",

    # ==================== RUMANO ====================

    "pula", "muie", "futu", "cacat",
    "căcat", "prost", "proasta", "bou",
    "nenorocit", "futu-ti", "pizda",
    "rahat", "idiotule", "tampit", "tâmpit",

    # ==================== GRIEGO ====================

    "malaka", "malakas", "skata",
    "gamoto", "poustis", "vlakas",
    "gamiesai", "arxidi", "katharma",

    # ==================== CHECO ====================

    "kurva", "kokot", "pica", "píča",
    "debil", "hajzl", "sracka", "sračka",
    "zmrd", "čurák", "curak",

    # ==================== HÚNGARO ====================

    "kurva", "fasz", "geci", "seggfej",
    "hülye", "hulye", "barom", "picsa",
    "szar", "baszdmeg", "köcsög", "kocsog",

    # ==================== HINDI ====================

    "chutiya", "bhosdike", "madarchod",
    "behenchod", "gaand", "harami",
    "kamina", "kutta", "gandu",
    "bhosdiwala", "lavde", "randi",

    # ==================== FILIPINO ====================

    "putangina", "gago", "tanga",
    "bobo", "leche", "tarantado",
    "ulol", "pakyu", "punyeta",
    "lintik", "hayop ka", "inutil",

    # ==================== INDONESIO ====================

    "anjing", "bangsat", "kontol", "memek",
    "kampret", "bajingan", "brengsek",
    "asu", "jancok", "keparat",

    # ==================== VIETNAMITA ====================

    "địt", "dit", "đụ", "du",
    "lồn", "lon", "cặc", "cac",
    "chó", "cho", "khốn nạn", "đồ ngu",

    # ==================== TAILANDÉS ====================

    "เหี้ย", "ควย", "สัส", "ไอ้โง่",
    "hia", "khuai", "sat", "ai ngo",

    # ==================== UCRANIANO ====================

    "бля", "хуй", "пизда", "сука",
    "blya", "khuy", "pizda", "suka",

    # ==================== SERBIO / CROATA ====================

    "jebem", "jebiga", "kurac", "pička",
    "picka", "govno", "smrad", "kreten",
    "majmun", "seronja",

    # ==================== ESLOVACO ====================

    "kokot", "kurva", "piča", "pica",
    "debil", "hajzel", "hovno", "jebat",

    # ==================== BULGARO ====================

    "kurva", "kurvi", "mamka", "daeb",
    "putka", "pederas", "smehnat",

]


# 2. RAÍCES UNIVERSALES (Atrapa variaciones nuevas, racistas, odiosas y deformadas)

RAICES_EXTRA = [

    # Español
    "verga", "puta", "caraj", "pendej", "jueput", "mierd", "mrd",
    "verga", "pene", "puta", "puto", "crj", "carajo",
    "jueputa", "pto", "ptoo", "pendejo", "jpta",
    "poliputo", "hijuetuputamare", "hijueputamare", "kgn", "polqria", "plqria", "po
    "pinga", "poronga", "kgda", "taraado", "porqueria", "escoria", "porqria", "prqria", "xqria", "prqueria", "xqueria",
    "hijueput", "hijuetuput", "poliput", "pinga", "puto",
    "porong", "crj", "jpta", "pto", "kgda", "pta"
    "forr", "garc", "chot", "soret", "pajer",
    "cornud", "mamert", "capull", "cabr",
    "gilipoll", "malnacid", "jod", "bolu",
    "rompebol", "chupaver", "chupapij", "cgd"

    # Inglés
    "dumbf", "dipsh", "shithead", "fuckfac",
    "scumb", "asswip", "dickwad", "shitst",
    "fuckwit", "fuckhead", "cockhead", "nig",
    "twatwaff", "shitbrain", "arsewipe",

    # Portugués
    "arromb", "babac", "otari", "escrot",
    "piran", "vagabund", "filhodaput",

    # Francés
    "connard", "connass", "encul", "salop",
    "emmerd", "abrut", "branleur",

    # Alemán
    "arschloch", "hurens", "wichs", "scheiss",
    "schlamp", "drecks", "schweinehund",

    # Italiano
    "stronz", "vaffanc", "cazz", "puttan",
    "coglion", "rompicogl", "merdos",

    # Neerlandés
    "klootzak", "godver", "hondelul",

    # Polaco
    "kurw", "pierdol", "skurwys", "pojeb",
    "spierdal", "wypierdal",

    # Ruso
    "бляд", "сука", "хуй", "пизд", "ебан",
    "blyat", "mudak", "pizd", "pidor",

    # Japonés / Coreano
    "kuso", "baka", "chikush", "씨발",
    "시발", "개새끼", "병신",

    # Turco
    "siktir", "orospu", "pezevenk",
    "serefsiz", "şerefsiz",

    # Hindi
    "chutiy", "madarch", "behench",
    "bhosd", "haram",

    # Filipino
    "putang", "tarantad", "punyet",

    # Otros
    "anjing", "bangsat", "kontol",
    "jancok", "brengsek", "keparat",
]


# ============================================================
# LISTAS BASE (en el archivo que revisamos no estaban definidas)
# ============================================================

PALABRAS_EXACTAS = []
RAICES_PROHIBIDAS = []


# ============================================================
# COMPILAR DICCIONARIOS - SIEMPRE DESPUÉS DE DEFINIR LAS LISTAS
# ============================================================

DICCIONARIO_COMPLETO = PALABRAS_EXACTAS + PALABRAS_EXTRA
RAICES_COMPLETAS = RAICES_PROHIBIDAS + RAICES_EXTRA

PATRONES_EXACTOS = []
for palabra in DICCIONARIO_COMPLETO:
    patron = crear_patron(palabra)
    if patron is not None:
        PATRONES_EXACTOS.append(patron)

PATRONES_RAICES = []
for raiz in RAICES_COMPLETAS:
    patron = crear_patron(raiz, raiz=True)
    if patron is not None:
        PATRONES_RAICES.append(patron)


@bot.event
async def on_message(message):

    # Ignorar bots
    if message.author.bot:
        return

    # Analizar el contenido
    resultado = detectar_infraccion(message.content)

    if resultado is not None:
        tipo, coincidencia = resultado

        # Registrar el intento antes de borrar el mensaje
        registrar_infraccion(message, tipo, coincidencia)

        try:
            await message.delete()

            await message.channel.send(
                f"{message.author.mention}, NOPE. "
                "Tu mensaje fue eliminado por Polipro."
            )

        except discord.Forbidden:
            print("ERROR: Polipro no tiene permiso para eliminar mensajes.")

        except discord.HTTPException as e:
            print(f"ERROR de Discord: {e}")

    await bot.process_commands(message)


# Toma el token de forma segura desde las variables de entorno de Railway
token = os.getenv('TOKEN')
if not token:
    raise RuntimeError("No se encontró la variable de entorno TOKEN. Configurala en Railway o en tu entorno local.")

bot.run(token)
