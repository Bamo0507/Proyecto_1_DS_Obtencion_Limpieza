"""
Etapa 3 del pipeline: CORRECCION DE NOMBRES
------------------------------------------------------------
Una sola responsabilidad: completar y corregir los campos de nombre.

  Lee : data/processed/02_nulos.csv
  Hace: - ESTABLECIMIENTO: construye un nombre generico desde la ubicacion
          para los registros sin nombre ("SIN NOMBRE - MUNICIPIO, DEPARTAMENTO")
        - SUPERVISOR: corrige el 0 escrito dentro de un nombre (debe ser O)
  Escribe: data/processed/03_nombres.csv

Ejecutar:  python src/03_nombres.py
"""

import re

import pandas as pd

import config
from utils import afirmar, banner, cargar, guardar

LETRA = r"[A-Za-zÁÉÍÓÚÑáéíóúñ]"


def corregir_ceros_en_nombre(nombre):
    """Un 0 pegado a letras es casi seguro una O mal escrita (ej. ACEVED0)."""
    if pd.isna(nombre):
        return nombre
    return re.sub(rf"(?<={LETRA})0|0(?={LETRA})", "O", nombre)


def main():
    banner("Etapa 3: CORRECCION DE NOMBRES")
    df = cargar(config.RUTA_NULOS, dtype=str)

    sin_nombre = df["ESTABLECIMIENTO"].isna()
    df.loc[sin_nombre, "ESTABLECIMIENTO"] = (
        config.PREFIJO_SIN_NOMBRE
        + df.loc[sin_nombre, "MUNICIPIO"].astype(str)
        + ", "
        + df.loc[sin_nombre, "DEPARTAMENTO"].astype(str)
    )
    print(f"[info]     se construyo el nombre de {int(sin_nombre.sum())} establecimientos sin nombre")

    df["SUPERVISOR"] = df["SUPERVISOR"].apply(corregir_ceros_en_nombre)

    afirmar(df["ESTABLECIMIENTO"].notna().all(), "ESTABLECIMIENTO ya no tiene nulos")
    afirmar(not df["SUPERVISOR"].dropna().str.contains(r"\d").any(),
            "SUPERVISOR ya no contiene digitos dentro de los nombres")

    guardar(df, config.RUTA_NOMBRES)


main()
