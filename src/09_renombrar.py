"""
Etapa 9 del pipeline: RENOMBRADO DE COLUMNAS
------------------------------------------------------------
Una sola responsabilidad: dejar nombres de variables descriptivos.

  Lee : data/processed/08_columnas.csv
  Hace: - pasa los nombres de columna a minusculas
        - renombra DEPARTAMENTAL a direccion_departamental para no confundirla
          con DEPARTAMENTO
  Escribe: data/processed/09_renombrado.csv

Ejecutar:  python src/09_renombrar.py
"""

import config
from utils import afirmar, banner, cargar, guardar


def main():
    banner("Etapa 9: RENOMBRADO DE COLUMNAS")
    df = cargar(config.RUTA_COLUMNAS, dtype=str)

    afirmar(list(df.columns) == list(config.RENOMBRES.keys()),
            "las columnas de entrada coinciden con las esperadas para renombrar")

    df = df.rename(columns=config.RENOMBRES)

    afirmar(list(df.columns) == config.COLUMNAS_FINALES,
            "las columnas quedaron con los nombres descriptivos finales")

    guardar(df, config.RUTA_RENOMBRADO)


main()
