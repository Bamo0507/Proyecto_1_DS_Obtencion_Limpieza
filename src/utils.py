"""
utils.py — esqueleto compartido por todas las etapas del pipeline
------------------------------------------------------------
Aqui vive el I/O y la validacion que cada etapa reutiliza, para que todas
se lean igual: cargar -> validar -> transformar -> validar -> guardar.

El logging es parte del estandar: prefijos alineados y consistentes
([cargado], [guardado], [ok], [FALLO]) para que la salida del pipeline
cuente la historia de cuantas filas entraron y que cambio.
"""

import sys
from pathlib import Path

import pandas as pd


def banner(titulo):
    """Imprime un separador visual con el titulo de la etapa."""
    print()
    print("=" * 60)
    print(titulo)
    print("=" * 60)


def cargar(ruta, **kwargs):
    """Lee un CSV y reporta filas/columnas cargadas.

    Por defecto se lee con dtype=str en ingesta para no dejar que pandas
    infiera tipos antes de tiempo; cada etapa decide sus kwargs.
    """
    ruta = Path(ruta)
    df = pd.read_csv(ruta, **kwargs)
    print(f"[cargado]  {ruta.name} -> {df.shape[0]} filas, {df.shape[1]} columnas")
    return df


def guardar(df, ruta):
    """Escribe un CSV en data/processed/, creando la carpeta si hace falta."""
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ruta, index=False)
    print(f"[guardado] {ruta.name} -> {df.shape[0]} filas, {df.shape[1]} columnas")


def afirmar(condicion, mensaje):
    """Validacion fail-fast.

    Imprime "[ok] mensaje" si la condicion se cumple; si no, imprime
    "[FALLO] mensaje" y corta el proceso con sys.exit(1) para que jamas
    se arrastren datos malos hacia la siguiente etapa.
    """
    if condicion:
        print(f"[ok]       {mensaje}")
    else:
        print(f"[FALLO]    {mensaje}")
        sys.exit(1)
