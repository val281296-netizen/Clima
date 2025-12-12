from datetime import datetime
import requests
from bs4 import BeautifulSoup
import csv
import os

BASE_URL = "https://www.climasurgba.com.ar/detallados"
CSV_FILE = "climasurgba.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

HORAS_2H = [f"{h:02d}:00" for h in range(0, 24, 2)]

def scrape_dia(fecha):
    # fecha en formato datetime
    fecha_str = fecha.strftime("%Y-%m-%d")
    url = f"{BASE_URL}/{fecha.strftime('%Y/%m/%d')}"  # construye la URL automáticamente
    print(f"Scrapeando: {url}")

    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    tabla = soup.find("table")
    if not tabla:
        print("No se encontró la tabla de datos.")
        return []

    rows = tabla.find_all("tr")
    data = []

    for row in rows[1:]:  # saltar header
        cols = row.find_all("td")
        if len(cols) < 2:
            continue
        hora = cols[0].get_text(strip=True)
        if hora not in HORAS_2H:
            continue  # solo cada 2 horas

        fila = [fecha_str, hora] + [c.get_text(strip=True) for c in cols[1:]]
        data.append(fila)

    return data

def main():
    hoy = datetime.now()
    filas = scrape_dia(hoy)
    if not filas:
        print("No hay datos para hoy.")
        return

    existe = os.path.exists(CSV_FILE)

    # Crear CSV si no existe
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not existe:
            # Aquí definís tus columnas según el sitio
            writer.writerow(["fecha", "hora", "temperatura", "humedad", "viento",
                             "direccion_viento", "lluvia", "presion"])
        writer.writerows(filas)

    print(f"Se agregaron {len(filas)} filas al CSV.")

if __name__ == "__main__":
    main()

