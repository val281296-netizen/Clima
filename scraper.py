import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime, timedelta

CSV_FILE = "climasurgba.csv"
URL = "https://www.climasurgba.com.ar/detallados/{year}/{month}/{day}"

# Fecha de hoy
today = datetime.today()
url = URL.format(year=today.year, month=str(today.month).zfill(2), day=str(today.day).zfill(2))

# Crear CSV si no existe
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["fecha", "hora", "temperatura", "humedad", "viento", "direccion_viento", "lluvia", "presion"])

# Descargar página
r = requests.get(url)
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")

# Seleccionar tabla de observaciones (ajustar según HTML)
tabla = soup.find("table")
rows = tabla.find_all("tr")[1:]  # Saltar header

with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for row in rows:
        cols = [c.text.strip() for c in row.find_all("td")]
        # Guardar cada 2 horas
        hora = int(cols[0].split(":")[0])
        if hora % 2 == 0:
            writer.writerow([today.strftime("%Y-%m-%d")] + cols)
