"""
Pruebas automaticas de calidad del conjunto limpio (requisito 7).
------------------------------------------------------------
Verifican sobre el dataset final que:
  - no existan registros duplicados exactos
  - no existan espacios al inicio o final de los textos
  - los telefonos tengan un formato consistente
  - los departamentos y municipios pertenezcan al catalogo del MINEDUC
  - las variables tengan el tipo de dato esperado
  - no existan categorias duplicadas por diferencias de escritura
  - no existan valores invalidos detectados en el diagnostico inicial

Requiere que el pipeline ya se haya corrido (python src/run_pipeline.py).
"""

import sys
import unicodedata
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))

import config  # noqa: E402  (se importa despues de ajustar sys.path)

# Se cargan una sola vez como texto para no reinferir tipos.
df = pd.read_csv(config.RUTA_FINAL, dtype=str)
catalogo = pd.read_csv(config.RUTA_CATALOGO, dtype=str)

# Variables categoricas y su dominio valido de valores.
DOMINIOS_CATEGORICOS = {
    "sector": {"PRIVADO", "OFICIAL", "MUNICIPAL", "COOPERATIVA"},
    "area": {"URBANA", "RURAL"},
    "status": {"ABIERTA", "CERRADA TEMPORALMENTE", "CERRADA DEFINITIVAMENTE",
               "TEMPORAL TITULOS", "TEMPORAL NOMBRAMIENTO"},
    "modalidad": {"MONOLINGUE", "BILINGUE"},
    "jornada": {"DOBLE", "VESPERTINA", "MATUTINA", "SIN JORNADA", "NOCTURNA", "INTERMEDIA"},
    "plan": set(config.CATEGORIAS_PLAN),
}


def normalizar(texto):
    """Mayusculas, sin tildes y sin espacios en los bordes, para comparar."""
    if pd.isna(texto):
        return texto
    sin_tildes = "".join(
        caracter for caracter in unicodedata.normalize("NFD", texto)
        if unicodedata.category(caracter) != "Mn"
    )
    return sin_tildes.strip().upper()


def test_estructura_consistente():
    assert list(df.columns) == config.COLUMNAS_FINALES
    assert len(df) > 0


def test_sin_duplicados_exactos():
    assert df.duplicated().sum() == 0


def test_codigo_es_llave_unica():
    assert df["codigo"].is_unique


def test_sin_espacios_en_bordes():
    for columna in df.columns:
        valores = df[columna].dropna()
        con_espacios = valores[valores != valores.str.strip()]
        assert con_espacios.empty, f"{columna} tiene {len(con_espacios)} valores con espacios en los bordes"


def test_telefono_formato_consistente():
    telefono = df["telefono"].dropna()
    assert telefono.str.fullmatch(r"\d+").all(), "hay telefonos que no son solo digitos"


def test_tipos_de_dato_esperados():
    # Todas las variables son cualitativas, por lo que su tipo correcto es texto.
    # Se valida sobre los valores reales (no el dtype de pandas) para que sea
    # robusto entre versiones.
    for columna in df.columns:
        valores = df[columna].dropna()
        assert valores.map(lambda valor: isinstance(valor, str)).all(), \
            f"{columna} tiene valores que no son texto"
    # codigo es un identificador con estructura fija esperada.
    assert df["codigo"].str.match(config.PATRON_CODIGO).all()


def test_departamentos_en_catalogo():
    departamentos_validos = {normalizar(nombre) for _codigo, nombre, _slug in config.DEPARTAMENTOS}
    departamentos_datos = set(df["departamento"].map(normalizar))
    fuera = departamentos_datos - departamentos_validos
    assert not fuera, f"departamentos fuera del catalogo: {fuera}"


def test_municipios_en_catalogo():
    pares_catalogo = set(zip(catalogo["departamento"].map(normalizar),
                             catalogo["municipio"].map(normalizar)))
    pares_datos = set(zip(df["departamento"].map(normalizar),
                          df["municipio"].map(normalizar)))
    fuera = pares_datos - pares_catalogo
    assert not fuera, f"pares (departamento, municipio) fuera del catalogo: {fuera}"


def test_dominios_categoricos():
    for columna, dominio in DOMINIOS_CATEGORICOS.items():
        valores = set(df[columna].dropna().unique())
        fuera = valores - dominio
        assert not fuera, f"{columna} tiene valores fuera de su dominio: {fuera}"


def test_sin_categorias_duplicadas_por_escritura():
    for columna in DOMINIOS_CATEGORICOS:
        valores = df[columna].dropna().unique()
        normalizados = {normalizar(valor) for valor in valores}
        assert len(normalizados) == len(valores), (
            f"{columna} tiene categorias que difieren solo por escritura")


def test_sin_valores_invalidos_del_diagnostico():
    # Los no-datos disfrazados y formatos invalidos detectados ya no existen.
    assert not df["area"].dropna().eq("SIN ESPECIFICAR").any()
    assert not df["director"].dropna().isin(config.MARCADORES_NULOS["DIRECTOR"]).any()
    assert not df["direccion"].dropna().eq(".").any()
    assert df["establecimiento"].notna().all(), "hay establecimientos sin nombre"
    distrito = df["distrito"].dropna()
    formato_valido = (distrito.str.match(config.PATRON_DISTRITO_LARGO)
                      | distrito.str.match(config.PATRON_DISTRITO_CORTO))
    assert formato_valido.all(), "hay distritos con formato invalido"


def main():
    pruebas = [objeto for nombre, objeto in sorted(globals().items())
               if nombre.startswith("test_") and callable(objeto)]
    fallidos = []
    for prueba in pruebas:
        try:
            prueba()
            print(f"[ok] {prueba.__name__}")
        except Exception as error:
            fallidos.append(prueba.__name__)
            print(f"[FALLO] {prueba.__name__}: {error}")
    print()
    print(f"{len(pruebas) - len(fallidos)}/{len(pruebas)} pruebas pasaron")
    raise SystemExit(1 if fallidos else 0)


if __name__ == "__main__":
    main()
