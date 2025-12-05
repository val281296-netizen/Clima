from pynasapower.get_data import query_power
from pynasapower.geometry import point, bbox
import datetime

# Run for point in Athens and save the result in csv format
gpoint = point(23.727539, 37.983810, "EPSG:4326")
start = datetime.date(2022, 1, 1)
end = datetime.date(2022, 2, 1)
data = query_power(gpoint, start, end, "./data", True, "ag", [], "daily", "point", "csv")

# Guardar en CSV en modo append
with open("clima_prueba.csv", "a", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    if file.tell() == 0:
        writer.writeheader()
    writer.writerows(nuevos)
