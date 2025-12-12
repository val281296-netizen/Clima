import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

URL = "https://www.smn.gob.ar/observaciones"
OUT_CSV = "observaciones_smn.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive"
}

def get_session():
    session = requests.Session()

    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[403, 429, 500, 502, 503, 504]
    )

    session.mount("https://", HTTPAdapter(max_retries=retries))
    session.mount("http://", HTTPAdapter(max_retries=retries))

    session.headers.update(HEADERS)
    return session


def clean_text(x):
    return x.get_text(strip=True) if x else None


def scrape_observaciones():
    print("Descargando datos del SMN...")

    session = get_session()
    r = session.get(URL, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    tabla = soup.find("table")
    if not tabla:
        raise ValueError("No se encontró la tabla de observaciones en la página")

    rows = tabla.find_all("tr")

    header = [
        "estacion", "provincia", "temperatura", "humedad",
        "presion", "viento", "direccion_viento",
        "estado", "visibilidad", "timestamp"
    ]

    estaciones = []
    timestamp = datetime.now().isoformat()

    for row in rows[1:]:  # skip header row
        cols = row.find_all("td")
        if len(cols) < 2:
            continue

        estacion = clean_text(cols[0])
        provincia = clean_text(cols[1])
        temperatura = clean_text(cols[2]) if len(cols) > 2 else None
        humedad = clean_text(cols[3]) if len(cols) > 3 else None
        viento = clean_text(cols[4]) if len(cols) > 4 else None
        direccion_viento = clean_text(cols[5]) if len(cols) > 5 else None
        presion = clean_text(cols[6]) if len(cols) > 6 else None
        visibilidad = clean_text(cols[7]) if len(cols) > 7 else None
        estado = clean_text(cols[8]) if len(cols) > 8 else None

        estaciones.append([
            estacion, provincia, temperatura, humedad,
            presion, viento, direccion_viento,
            estado, visibilidad, timestamp
        ])

    # Escribir CSV en modo append
    write_header = not os.path.exists(OUT_CSV)

    with open(OUT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerows(estaciones)

    print(f"Filas añadidas: {len(estaciones)}")
    print("CSV actualizado correctamente.")


if __name__ == "__main__":
    scrape_observaciones()
