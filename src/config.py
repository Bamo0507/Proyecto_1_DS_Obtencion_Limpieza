"""
config.py — rutas y contratos de columnas en un solo lugar
------------------------------------------------------------
Ningun script inventa sus propias rutas ni sus propias listas de columnas:
todo vive aqui y las etapas lo importan. Es la unica fuente de verdad.
"""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIR_RAW = RAIZ / "data" / "raw"
DIR_PROCESSED = RAIZ / "data" / "processed"

# --- Rutas por etapa -------------------------------------------------------
# Una ruta por etapa, comentada con el script que la produce.
# TODO: definir cuando tengamos el dataset y las etapas.
#
# RUTA_CRUDA   = DIR_RAW / "<archivo>.csv"                 # entrada, nunca se modifica
# RUTA_INGESTA = DIR_PROCESSED / "01_ingesta.csv"          # <- 01_ingesta.py
# ...
# RUTA_FINAL   = DIR_PROCESSED / "<nombre>_limpio.csv"     # <- ultima etapa

# --- Contrato de entrada ---------------------------------------------------
# Columnas que DEBEN venir en el crudo; las etapas lo usan para validar.
# TODO: llenar con las columnas reales del dataset.
#
# COLUMNAS_CRUDAS = [ ... ]
