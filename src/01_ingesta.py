"""
Etapa 1 del pipeline: INGESTA
------------------------------------------------------------
Una sola responsabilidad: consolidar los 23 CSV crudos en un unico dataset.

  Lee : data/raw/diversificado_*.csv (23 archivos)
  Hace: - carga cada archivo con dtype=str (crudo intacto)
        - valida el contrato de columnas y que CODIGO sea unico y con patron
        - los concatena en un solo dataset
  Escribe: data/processed/01_ingesta.csv

Ejecutar:  python src/01_ingesta.py
"""

import pandas as pd

import config
from utils import afirmar, banner, guardar


def main():
    banner("Etapa 1: INGESTA")
    archivos = sorted(config.DIR_RAW.glob("diversificado_*.csv"))
    afirmar(len(archivos) > 0, f"se encontraron CSV crudos en {config.DIR_RAW}")

    df = pd.concat([pd.read_csv(archivo, dtype=str) for archivo in archivos], ignore_index=True)
    print(f"[cargado]  {len(archivos)} archivos -> {df.shape[0]} filas, {df.shape[1]} columnas")

    afirmar(list(df.columns) == config.COLUMNAS_CRUDAS,
            "las columnas coinciden con el contrato COLUMNAS_CRUDAS")
    afirmar(df["CODIGO"].notna().all(), "CODIGO no tiene valores nulos")
    afirmar(df["CODIGO"].is_unique, "CODIGO es unico a nivel nacional")
    afirmar(df["CODIGO"].str.match(config.PATRON_CODIGO).all(),
            "CODIGO cumple el patron ##-##-####-##")

    guardar(df, config.RUTA_INGESTA)


main()
