"""
Etapa 7 del pipeline: ESTANDARIZACION DE DEPARTAMENTAL
------------------------------------------------------------
Una sola responsabilidad: unificar la acentuacion de DEPARTAMENTAL.

  Lee : data/processed/06_plan.csv
  Hace: - quita las tildes de DEPARTAMENTAL para alinearla con DEPARTAMENTO
  Escribe: data/processed/07_departamental.csv

Ejecutar:  python src/07_departamental.py
"""

import unicodedata

import pandas as pd

import config
from utils import afirmar, banner, cargar, guardar


def quitar_tildes(texto):
    if pd.isna(texto):
        return texto
    return "".join(
        caracter for caracter in unicodedata.normalize("NFD", texto)
        if unicodedata.category(caracter) != "Mn"
    )


def main():
    banner("Etapa 7: ESTANDARIZACION DE DEPARTAMENTAL")
    df = cargar(config.RUTA_PLAN, dtype=str)

    df["DEPARTAMENTAL"] = df["DEPARTAMENTAL"].apply(quitar_tildes)

    afirmar(not df["DEPARTAMENTAL"].dropna().str.contains(r"[ÁÉÍÓÚÑáéíóúñ]").any(),
            "DEPARTAMENTAL ya no contiene tildes")

    guardar(df, config.RUTA_DEPARTAMENTAL)


main()
