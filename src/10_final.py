"""
Etapa 10 del pipeline: VALIDACION FINAL Y GUARDADO
------------------------------------------------------------
Una sola responsabilidad: validar el esquema final y guardar el dataset limpio.

  Lee : data/processed/09_renombrado.csv
  Hace: - valida el esquema final (16 columnas descriptivas) y la unicidad de codigo
        - reporta los NaN por variable (insumo para el codebook)
  Escribe: data/processed/establecimientos_diversificado_limpio.csv

Ejecutar:  python src/10_final.py
"""

import config
from utils import afirmar, banner, cargar, guardar


def main():
    banner("Etapa 10: VALIDACION FINAL Y GUARDADO")
    df = cargar(config.RUTA_RENOMBRADO, dtype=str)

    afirmar(list(df.columns) == config.COLUMNAS_FINALES,
            "el esquema final tiene las 16 columnas descriptivas esperadas")
    afirmar(df["codigo"].is_unique, "codigo sigue siendo unico en el dataset final")

    print("\n[reporte]  valores faltantes por variable en el dataset limpio:")
    faltantes = df.isna().sum()
    for columna in df.columns:
        cantidad = int(faltantes[columna])
        if cantidad:
            print(f"           {columna}: {cantidad} ({cantidad / len(df) * 100:.2f}%)")

    guardar(df, config.RUTA_FINAL)


main()
