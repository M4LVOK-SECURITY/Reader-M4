import os
import sys
import subprocess

# Función para verificar e instalar módulos si no están presentes
def check_and_install(module):
    try:
        __import__(module)
    except ImportError:
        print(f"\n[+] Instalando {module}...\n")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])

# Verificar e instalar los módulos necesarios
modules = ["gtts", "pymupdf"]
for module in modules:
    check_and_install(module)

import fitz  # PyMuPDF para leer PDFs
from gtts import gTTS

# Función para mostrar el banner
def show_banner():
    print("""
███╗   ███╗██████╗ 
████╗ ████║██╔══██╗
██╔████╔██║██████╔╝
██║╚██╔╝██║██╔═══╝ 
██║ ╚═╝ ██║██║     
╚═╝     ╚═╝╚═╝   By M4   
    """)

# Función para leer texto desde un archivo TXT
def read_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Función para leer texto desde un archivo PDF
def read_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text.strip()

# Función para crear el audiolibro
def create_audiobook(file_path, output_file, lang):
    file_path = file_path.strip().replace("\\", "/")  # Corrige la ruta
    if not os.path.exists(file_path):
        print(f"\n[ERROR] El archivo '{file_path}' no existe. Verifica la ruta e inténtalo de nuevo.\n")
        sys.exit(1)

    # Detectar si es TXT o PDF
    file_ext = os.path.splitext(file_path)[1].lower()
    if file_ext == ".txt":
        text = read_txt(file_path)
    elif file_ext == ".pdf":
        text = read_pdf(file_path)
    else:
        print("\n[ERROR] Formato de archivo no soportado. Use .txt o .pdf\n")
        sys.exit(1)

    # Generar el audio
    tts = gTTS(text=text, lang=lang)
    tts.save(output_file)
    print(f"\n[+] Audiolibro guardado exitosamente en '{output_file}'\n")
    os.system(f"start {output_file}")  # Reproducir el archivo

# Mostrar banner M4
show_banner()

# Pedir la ruta del archivo y eliminar espacios extra
file_path = input("\nIngrese la ruta del archivo (TXT o PDF): ").strip().replace("\\", "/")

# Verificar que el archivo exista antes de continuar
if not os.path.exists(file_path):
    print(f"\n[ERROR] El archivo '{file_path}' no existe. Verifica la ruta y vuelve a intentarlo.\n")
    sys.exit(1)

# Pedir el idioma de salida
lang = input("\nIngrese el idioma de salida (es para español, en para inglés): ").strip().lower()
if lang not in ['es', 'en']:
    print("\n[ERROR] Idioma no soportado. Use 'es' para español o 'en' para inglés.\n")
    sys.exit(1)

# Pedir el nombre del archivo de salida
output_file = input("\nIngrese el nombre del archivo de salida (sin extensión): ").strip() + ".mp3"

# Crear el audiolibro
create_audiobook(file_path, output_file, lang)
