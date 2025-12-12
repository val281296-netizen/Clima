import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

URL = "https://www.smn.gob.ar/observaciones"
OUT_CSV = "observaciones_smn.csv"

def clean_text(x):
    return x.get_text(strip=True) if x else None

def scrape_observaciones():
    print("Descargando datos del SMN...")

    r = requests.get(URL, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    estaciones = []
    tabla = soup.find("table")

    if not tabla:
        raise ValueError("No se encontró la tabla de observaciones en la página")

    rows = tabla.find_all("tr")

    header = [
        "estacion", "provincia", "temperatura", "humedad", 
        "presion", "viento", "direccion_viento", 
        "estado", "visibilidad", "timestamp"
    ]

    for row in rows[1:]:  # saltamos header de la tabla del SMN
        cols = row.find_all("td")
        if len(cols) < 5:
            continue

        estacion = clean_text(cols[0])
        provincia = clean_text(cols[1])
        temperatura = clean_text(cols[2])
        humedad = clean_text(cols[3])
        viento = clean_text(cols[4])
        direccion_viento = clean_text(cols[5]) if len(cols) > 5 else None
        presion = clean_text(cols[6]) if len(cols) > 6 else None
        visibilidad = clean_text(cols[7]) if len(cols) > 7 else None
        estado = clean_text(cols[8]) if len(cols) > 8 else None

        timestamp = datetime.now().isoformat()

        estaciones.append([
            estacion, provincia, temperatura, humedad,
            presion, viento, direccion_viento,
            estado, visibilidad, timestamp
        ])

    # Escribimos CSV
    print(f"Generando CSV con {len(estaciones)} estaciones...")

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(estaciones)

    print("CSV generado correctamente:", OUT_CSV)


if __name__ == "__main__":
    scrape_observaciones()
