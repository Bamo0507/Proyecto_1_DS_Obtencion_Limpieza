"""
run_pipeline.py — orquestador del pipeline
------------------------------------------------------------
Una sola responsabilidad: correr las etapas en orden y detenerse en la
primera que falle (fail-fast). No re-implementa logica: solo encadena
scripts que ya funcionan solos.

Ejecutar (con el venv activado):  python src/run_pipeline.py
"""

import subprocess
import sys
from pathlib import Path

DIR_SRC = Path(__file__).resolve().parent

# Etapas en orden de ejecucion. Cada una lee la salida de la anterior.
ETAPAS = [
    "01_ingesta.py",
    "02_nulos.py",
    "03_nombres.py",
    "04_telefono.py",
    "05_distrito.py",
    "06_plan.py",
    "07_departamental.py",
    "08_columnas.py",
    "09_final.py",
]


def main():
    if not ETAPAS:
        print("[FALLO]    no hay etapas definidas en ETAPAS (ver run_pipeline.py)")
        sys.exit(1)

    for etapa in ETAPAS:
        ruta = DIR_SRC / etapa
        print()
        print("#" * 60)
        print(f"# Corriendo {etapa}")
        print("#" * 60)
        sys.stdout.flush()  # asegura que el banner salga antes de la salida de la etapa
        resultado = subprocess.run([sys.executable, str(ruta)])
        if resultado.returncode != 0:
            print()
            print(f"[FALLO]    el pipeline se detuvo en {etapa} (codigo {resultado.returncode})")
            sys.exit(1)

    print()
    print("[ok]       pipeline completo: todas las etapas corrieron sin error")


main()
