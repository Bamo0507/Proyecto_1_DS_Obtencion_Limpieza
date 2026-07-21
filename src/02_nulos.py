"""
Etapa 2 del pipeline: NORMALIZACION DE NULOS
------------------------------------------------------------
Una sola responsabilidad: unificar los marcadores de no-dato disfrazados a NaN.

  Lee : data/processed/01_ingesta.csv
  Hace: - por columna, convierte a NaN los tokens que en realidad son no-dato
          (DIRECTOR: SIN DATO, -, ., ceros; DIRECCION: .; AREA: SIN ESPECIFICAR)
        - NO toca JORNADA=SIN JORNADA, que es un valor legitimo
  Escribe: data/processed/02_nulos.csv

Ejecutar:  python src/02_nulos.py
"""

import config
from utils import afirmar, banner, cargar, guardar


def main():
    banner("Etapa 2: NORMALIZACION DE NULOS")
    df = cargar(config.RUTA_INGESTA, dtype=str)
    afirmar(list(df.columns) == config.COLUMNAS_CRUDAS,
            "la etapa anterior entrego el contrato de columnas esperado")

    for columna, marcadores in config.MARCADORES_NULOS.items():
        df[columna] = df[columna].mask(df[columna].isin(marcadores))

    # DIRECTOR: cualquier cadena de solo ceros tambien es un no-dato.
    df["DIRECTOR"] = df["DIRECTOR"].mask(df["DIRECTOR"].str.fullmatch(config.PATRON_CEROS, na=False))

    for columna, marcadores in config.MARCADORES_NULOS.items():
        afirmar(not df[columna].isin(marcadores).any(),
                f"{columna} ya no contiene sus marcadores de nulo")

    guardar(df, config.RUTA_NULOS)


main()
