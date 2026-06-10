"""Simulação da camada ESP32.

O ESP32 não mede El Niño. Ele representa a validação local de campo, simulando
umidade do solo e temperatura observada no talhão.
"""
import random
import time
from datetime import datetime
from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parents[1]
OUT = BASE_DIR / "outputs" / "leituras_esp32_simulado.csv"

municipios = ["Rio Verde", "Jataí", "Montividiu", "Mineiros", "Santa Helena de Goiás"]


def gerar_leituras(n=12, delay=0.2):
    OUT.parent.mkdir(exist_ok=True)
    existe = OUT.exists()
    with OUT.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow(["timestamp", "municipio", "umidade_solo_pct", "temperatura_local_c", "status_sensor"])
        for _ in range(n):
            mun = random.choice(municipios)
            umid = round(random.uniform(14, 42), 1)
            temp = round(random.uniform(26, 38), 1)
            status = "solo seco" if umid < 20 else "atenção" if umid < 28 else "adequado"
            writer.writerow([datetime.now().isoformat(timespec="seconds"), mun, umid, temp, status])
            print(f"ESP32 simulado | {mun} | umidade={umid}% | temp={temp}C | {status}")
            time.sleep(delay)


if __name__ == "__main__":
    gerar_leituras()
