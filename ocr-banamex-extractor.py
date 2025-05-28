from pdf2image import convert_from_path
from pathlib import Path
import pytesseract
import re

# 👉 Ruta a Tesseract OCR (ajusta si es necesario)
pytesseract.pytesseract.tesseract_cmd = r'' 

# 👉 Ruta a Poppler bin (ajusta según tu instalación)
poppler_path = r''

# 👉 Palabras clave para abonos y cargos
abonos_clave = ["NOMINA", "ABONO", "DEPOSITO NOMINA", "ABONO NOMINA", "ABONO/NOMINA", "ABON/NOMI"]
cargos_clave = ["DOMICILIADO", "NETFLIX", "CREDITO"]

# 👉 Expresiones regulares
regex_fecha = r"\b\d{1,2}\S?[A-Z]{3}\b"  # Ej. 10 ABR
regex_monto = r"\$\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?"  # Ej. $1,234.56

# 👉 Buscar primer PDF en la misma carpeta que el script
pdf_path = next(Path(__file__).parent.glob("*.pdf"), None)

if not pdf_path:
    print("❌ No se encontró un archivo PDF en la carpeta.")
    exit()

print(f"📄 Procesando archivo: {pdf_path.name}\n")

# 👉 Convertir PDF a imágenes
images = convert_from_path(
    pdf_path=str(pdf_path),
    dpi=400,
    poppler_path=poppler_path
)

print("🔎 Buscando transacciones relevantes...\n")

# 👉 Revisión por página
for num_pagina, img in enumerate(images[1:], start=2):  # [1:] para saltar portada
    texto = pytesseract.image_to_string(img, lang='spa').upper()

    lineas = texto.splitlines()

    for linea in lineas:
        if any(palabra in linea for palabra in abonos_clave):
            fecha = re.search(regex_fecha, linea.upper())
            montos = re.findall(regex_monto, linea)
            print("🟢 → ABONO DETECTADO")
            print(f"📆 Fecha     : {fecha.group() if fecha else '---'}")
            print(f"📝 Concepto  : {linea.strip()}")
            print(f"💰 Monto(s)  : {', '.join(montos) if montos else '---'}")
            print("-" * 50)

        elif any(palabra in linea for palabra in cargos_clave):
            fecha = re.search(regex_fecha, linea.upper())
            montos = re.findall(regex_monto, linea)
            print("🔴 → CARGO DETECTADO")
            print(f"📆 Fecha     : {fecha.group() if fecha else '---'}")
            print(f"📝 Concepto  : {linea.strip()}")
            print(f"💰 Monto(s)  : {', '.join(montos) if montos else '---'}")
            print("-" * 50)
