"""
Etapa 5 del pipeline: ESTANDARIZACION DE DISTRITO
------------------------------------------------------------
Una sola responsabilidad: rechazar los codigos de distrito invalidos.

  Lee : data/processed/04_telefono.csv
  Hace: - conserva los dos formatos validos (largo ##-##-#### y corto ##-###)
        - los codigos truncados (ej. 01-) se marcan como NaN por ser irreparables
  Escribe: data/processed/05_distrito.csv

Ejecutar:  python src/05_distrito.py
"""

import re

import pandas as pd

import config
from utils import afirmar, banner, cargar, guardar


def distrito_valido(distrito):
    if pd.isna(distrito):
        return distrito
    if re.match(config.PATRON_DISTRITO_LARGO, distrito) or re.match(config.PATRON_DISTRITO_CORTO, distrito):
        return distrito
    return pd.NA


def main():
    banner("Etapa 5: ESTANDARIZACION DE DISTRITO")
    df = cargar(config.RUTA_TELEFONO, dtype=str)

    df["DISTRITO"] = df["DISTRITO"].apply(distrito_valido)

    distritos_validos = df["DISTRITO"].dropna()
    cumple_formato = (distritos_validos.str.match(config.PATRON_DISTRITO_LARGO)
                      | distritos_validos.str.match(config.PATRON_DISTRITO_CORTO))
    afirmar(cumple_formato.all(), "DISTRITO no nulo cumple uno de los dos formatos validos")

    guardar(df, config.RUTA_DISTRITO)


main()
