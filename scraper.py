import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

BASE_URL = "https://www.climasurgba.com.ar/detallados"
CSV_FILE = "climasurgba.csv"

# Cabeceras para simular navegador
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

# Horas a extraer (cada 2 horas)
HORAS_2H = [f"{h:02d}:00" for h in range(0, 24, 2)]

def scrape_dia(fecha_str):
    url = f"{BASE_URL}/{fecha_str.replace('-', '/')}"
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
    hoy = datetime.now().strftime("%Y-%m-%d")
    filas = scrape_dia(hoy)
    if not filas:
        print("No hay datos para hoy.")
        return

    # Chequear si existe CSV
    existe = os.path.exists(CSV_FILE)

    # Crear header dinámico
    if filas:
        # La primera fila ya tiene fecha y hora + resto de columnas
        header = ["fecha", "hora"] + [f"col{i}" for i in range(1, len(filas[0])-1)]
    
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow(["fecha", "hora", "temperatura", "humedad", "viento",
                             "direccion_viento", "lluvia", "presion"])
        writer.writerows(filas)

    print(f"Se agregaron {len(filas)} filas al CSV.")

if __name__ == "__main__":
    main()

