"""
Etapa 9 del pipeline: VALIDACION FINAL Y GUARDADO
------------------------------------------------------------
Una sola responsabilidad: validar el esquema final y guardar el dataset limpio.

  Lee : data/processed/08_columnas.csv
  Hace: - valida el esquema final (16 columnas, sin NIVEL) y la unicidad de CODIGO
        - reporta los NaN por variable (insumo para el codebook)
  Escribe: data/processed/establecimientos_diversificado_limpio.csv

Ejecutar:  python src/09_final.py
"""

import config
from utils import afirmar, banner, cargar, guardar


def main():
    banner("Etapa 9: VALIDACION FINAL Y GUARDADO")
    df = cargar(config.RUTA_COLUMNAS, dtype=str)

    columnas_esperadas = [columna for columna in config.COLUMNAS_CRUDAS if columna != "NIVEL"]
    afirmar(list(df.columns) == columnas_esperadas, "el esquema final tiene 16 columnas, sin NIVEL")
    afirmar(df["CODIGO"].is_unique, "CODIGO sigue siendo unico en el dataset final")

    print("\n[reporte]  valores faltantes por variable en el dataset limpio:")
    faltantes = df.isna().sum()
    for columna in df.columns:
        cantidad = int(faltantes[columna])
        if cantidad:
            print(f"           {columna}: {cantidad} ({cantidad / len(df) * 100:.2f}%)")

    guardar(df, config.RUTA_FINAL)


main()
