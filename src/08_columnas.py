"""
Etapa 8 del pipeline: ELIMINACION DE COLUMNAS SIN VALOR
------------------------------------------------------------
Una sola responsabilidad: eliminar columnas que no aportan variabilidad.

  Lee : data/processed/07_departamental.csv
  Hace: - elimina NIVEL, que es constante (DIVERSIFICADO) en todo el dataset
  Escribe: data/processed/08_columnas.csv

Ejecutar:  python src/08_columnas.py
"""

import config
from utils import afirmar, banner, cargar, guardar


def main():
    banner("Etapa 8: ELIMINACION DE COLUMNAS SIN VALOR")
    df = cargar(config.RUTA_DEPARTAMENTAL, dtype=str)

    afirmar(df["NIVEL"].nunique(dropna=False) == 1,
            "NIVEL es constante antes de eliminarla")
    df = df.drop(columns=["NIVEL"])
    afirmar("NIVEL" not in df.columns, "NIVEL fue eliminada del dataset")

    guardar(df, config.RUTA_COLUMNAS)


main()
