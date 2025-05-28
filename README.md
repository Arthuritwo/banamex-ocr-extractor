

📄 README.md


# 🏦 Banamex OCR Extractor


Script en Python que analiza estados de cuenta **Banamex** en formato PDF utilizando OCR, extrayendo únicamente:


- 🟢 **Abonos de nómina**

- 🔴 **Cargos domiciliados (automáticos)**


Muestra los resultados en consola con un formato limpio y visual (emojis) y permite exportarlos a CSV para su posterior análisis.


---


## 📌 Características


- 🔍 Extrae únicamente líneas relevantes usando expresiones regulares.

- 💬 Muestra fecha, concepto y monto en consola.

- 📁 Opción para guardar los resultados en un archivo CSV.

- ✅ Compatible con estados de cuenta Banamex que presenten transacciones en columnas: **fecha, concepto, retiros, depósitos y saldo**.

- 🧠 Fácil de extender con nuevas palabras clave.


---


## 📸 Ejemplo en consola


```plaintext

📄 Procesando archivo: edo_cuenta_banamex.pdf


🔎 Buscando transacciones relevantes...


🟢 → ABONO DETECTADO

📆 Fecha     : 10ABR

📝 Concepto  : DEPÓSITO NÓMINA EMPRESA S.A. DE C.V.

💰 Monto(s)  : $7,850.00

--------------------------------------------------


🔴 → CARGO DETECTADO

📆 Fecha     : 11ABR

📝 Concepto  : TELMEX CARGO DOMICILIADO

💰 Monto(s)  : $499.00

--------------------------------------------------


✅ Análisis completado


📊 Resumen:

✔️  Abonos de nómina encontrados     : 2

✔️  Cargos domiciliados encontrados  : 2


📁 Archivo exportado como 'transacciones.csv'


⚙️ Requisitos


Instala las dependencias:


pip install pytesseract pdf2image


Además:

	•	📥 Tesseract OCR instalado (configura la ruta en el script si usas Windows).

	•	📥 Poppler for Windows para convertir PDF a imagen (pdf2image lo usa).

	•	El archivo PDF debe estar en la misma carpeta que el script.


🧠 ¿Cómo funciona?


	1.	Convierte el PDF a imágenes.

	2.	Extrae texto con pytesseract.

	3.	Detecta líneas que contienen abonos o cargos usando palabras clave.

	4.	Usa regex para extraer fecha (10ABR) y montos ($999.99).

	5.	Muestra en consola y pregunta si deseas exportar CSV.


📁 Estructura de salida CSV


Tipo,Fecha,Concepto,Montos

Abono,10ABR,DEPÓSITO NÓMINA EMPRESA S.A. DE C.V.,"$7,850.00"

Cargo,11ABR,TELMEX CARGO DOMICILIADO,"$499.00"


✏️ Personalización


Puedes editar estas listas en el script para agregar más coincidencias:


abonos_clave = ["nómina", "deposito nómina", "depósito nómina"]

cargos_clave = ["domiciliado", "cargo automático", "spotify", "telmex", "izzy", "netflix"]


📄 Licencia


Este proyecto es de código abierto y se distribuye bajo la licencia MIT.


✉️ Autor


Desarrollado por Arturo 🧠💻


---
