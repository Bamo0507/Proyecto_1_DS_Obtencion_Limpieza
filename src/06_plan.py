"""
Etapa 6 del pipeline: CONSOLIDACION DE PLAN
------------------------------------------------------------
Una sola responsabilidad: reducir PLAN a 4 categorias.

  Lee : data/processed/05_distrito.csv
  Hace: - mapea las 13 categorias originales a ENTRE SEMANA, FIN DE SEMANA,
          A DISTANCIA o MIXTO
  Escribe: data/processed/06_plan.csv

Ejecutar:  python src/06_plan.py
"""

import config
from utils import afirmar, banner, cargar, guardar


def main():
    banner("Etapa 6: CONSOLIDACION DE PLAN")
    df = cargar(config.RUTA_DISTRITO, dtype=str)

    categorias_presentes = set(df["PLAN"].dropna().unique())
    categorias_sin_mapear = categorias_presentes - set(config.MAPA_PLAN)
    afirmar(not categorias_sin_mapear,
            f"todas las categorias de PLAN estan en el mapa (sin mapear: {categorias_sin_mapear})")

    df["PLAN"] = df["PLAN"].map(config.MAPA_PLAN)

    afirmar(set(df["PLAN"].dropna().unique()).issubset(set(config.CATEGORIAS_PLAN)),
            "PLAN solo contiene las 4 categorias finales")

    guardar(df, config.RUTA_PLAN)


main()
