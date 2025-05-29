from pdf2image import convert_from_path
from pathlib import Path
import pytesseract
import re

# 👉 Ruta a Tesseract OCR (ajusta si es necesario)
pytesseract.pytesseract.tesseract_cmd = r'' 

# 👉 Ruta a Poppler bin (ajusta según tu instalación)
poppler_path = r''

# 👉 Expresiones regulares
regex_fecha = r"\d{2}-[A-Z]{3}-\d{4}"  # Ej. 28-MAR-2025
regex_abono_nomina = r"ABONO\sPAGO\sDE\sNOMINA"  #
#regex_monto = r"\d{1,3}(?:[,\s]?\d{3})*(?:[.,]\d{1,2})"  # Más flexible: 5,314.82, 5314.82, 5 314.82, 5314,82, 5314.8
regex_monto = r"\d{1,3}(?:,\d{3})*(?:\.\d{2})" #5,314.82

regex_cargo = r"(?:MEGACABLE)(?!\s*ABONO\s*PAGO\s*DE\s*NOMINA)"  # Cargos, evitando ABONO NOMINA

# 👉 Buscar primer PDF en la misma carpeta que el script
pdf_path = next(Path(__file__).parent.glob("*.pdf"), None)

if not pdf_path:
    print("❌ No se encontró un archivo PDF en la carpeta.")
    exit()

print(f"📄 Procesando archivo: {pdf_path.name}\n")

# 👉 Convertir PDF a imágenes
images = convert_from_path(
    pdf_path=str(pdf_path),
    dpi=400,  # Ajustaste el DPI para que funcione bien
    poppler_path=poppler_path
)

print("🔎 Buscando transacciones relevantes...\n")

# 👉 Revisión por página
for num_pagina, img in enumerate(images[1:], start=2):  # Saltar portada
    texto = pytesseract.image_to_string(img, lang='eng').upper()
    lineas = texto.splitlines()

    for idx, linea in enumerate(lineas):
        texto_linea = linea.strip()

        # 🔍 Detectar ABONOS
        abono_match = re.search(regex_abono_nomina, texto_linea)
        if abono_match:
            # 👉 Buscar fecha en esta línea o anterior
            fecha = re.search(regex_fecha, texto_linea)
            if not fecha and idx > 0:
                fecha = re.search(regex_fecha, lineas[idx - 1].upper())
            if not fecha and idx > 1:
                fecha = re.search(regex_fecha, lineas[idx - 2].upper())
            if not fecha and idx > 2:
                fecha = re.search(regex_fecha, lineas[idx - 3].upper())

            # 👉 Buscar monto en esta línea o adyacentes
            monto = re.search(regex_monto, texto_linea)
            if not monto and idx + 1 < len(lineas):
                monto = re.search(regex_monto, lineas[idx + 1])
            if not monto and idx + 2 < len(lineas):
                monto = re.search(regex_monto, lineas[idx + 2])
            if not monto and idx + 3 < len(lineas):
                monto = re.search(regex_monto, lineas[idx + 3])
            if not monto and idx > 0:
                monto = re.search(regex_monto, lineas[idx - 1])
            if not monto and idx > 1:
                monto = re.search(regex_monto, lineas[idx - 2])
            if not monto and idx > 2:
                monto = re.search(regex_monto, lineas[idx - 3])

            # 👉 Imprimir abono
            print("🟢 → ABONO DETECTADO")
            print(f"📆 Fecha     : {fecha.group() if fecha else '---'}")
            print(f"📝 Concepto  : {abono_match.group()}")
            print(f"💰 Monto     : {monto.group() if monto else '---'}")
            print("-" * 50)

        # 🔍 Detectar CARGOS
        elif re.search(regex_cargo, texto_linea):
            # 👉 Buscar fecha en esta línea o anterior
            fecha = re.search(regex_fecha, texto_linea)
            if not fecha and idx > 0:
                fecha = re.search(regex_fecha, lineas[idx - 1].upper())
            if not fecha and idx > 1:
                fecha = re.search(regex_fecha, lineas[idx - 2].upper())
            if not fecha and idx > 2:
                fecha = re.search(regex_fecha, lineas[idx - 3].upper())

            # 👉 Buscar monto en esta línea o adyacentes
            monto = re.search(regex_monto, texto_linea)
            if not monto and idx + 1 < len(lineas):
                monto = re.search(regex_monto, lineas[idx + 1])
            if not monto and idx + 2 < len(lineas):
                monto = re.search(regex_monto, lineas[idx + 2])
            if not monto and idx + 3 < len(lineas):
                monto = re.search(regex_monto, lineas[idx + 3])
            if not monto and idx > 0:
                monto = re.search(regex_monto, lineas[idx - 1])
            if not monto and idx > 1:
                monto = re.search(regex_monto, lineas[idx - 2])
            if not monto and idx > 2:
                monto = re.search(regex_monto, lineas[idx - 3])

            # 👉 Imprimir cargo
            print("🔴 → CARGO DETECTADO")
            print(f"📆 Fecha     : {fecha.group() if fecha else '---'}")
            print(f"📝 Concepto  : {texto_linea}")
            print(f"💰 Monto     : {monto.group() if monto else '---'}")
            print("-" * 50)