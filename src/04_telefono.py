"""
Etapa 4 del pipeline: ESTANDARIZACION DE TELEFONO
------------------------------------------------------------
Una sola responsabilidad: dejar un unico numero de telefono por registro.

  Lee : data/processed/03_nombres.csv
  Hace: - se queda con el primer numero (antes del primer separador) y solo sus digitos
        - lo que quede sin digitos se marca como NaN
  Escribe: data/processed/04_telefono.csv

Ejecutar:  python src/04_telefono.py
"""

import re

import pandas as pd

import config
from utils import afirmar, banner, cargar, guardar


def numero_principal(telefono):
    if pd.isna(telefono):
        return telefono
    primer_numero = re.split(config.SEPARADORES_TELEFONO, telefono.strip())[0]
    digitos = re.sub(r"\D", "", primer_numero)
    return digitos if digitos else pd.NA


def main():
    banner("Etapa 4: ESTANDARIZACION DE TELEFONO")
    df = cargar(config.RUTA_NOMBRES, dtype=str)

    df["TELEFONO"] = df["TELEFONO"].apply(numero_principal)

    telefonos_validos = df["TELEFONO"].dropna()
    afirmar(telefonos_validos.str.fullmatch(r"\d+").all(),
            "TELEFONO no nulo contiene unicamente digitos, sin separadores")

    guardar(df, config.RUTA_TELEFONO)


main()
