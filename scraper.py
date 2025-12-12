import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

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

    timestamp = datetime.now().isoformat()

    for row in rows[1:]:  # saltamos encabezado visual del SMN
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

    # Determinar si es la primera vez (CSV no existe)
    write_header = not os.path.exists(OUT_CSV)

    mode = "a"  # append siempre
    print(f"Escribiendo {len(estaciones)} filas nuevas en modo append...")

    with open(OUT_CSV, mode, newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerows(estaciones)

    print("CSV actualizado correctamente:", OUT_CSV)


if __name__ == "__main__":
    scrape_observaciones()
