"""
config.py — rutas y contratos en un solo lugar
------------------------------------------------------------
Ningun script inventa sus propias rutas ni sus propias listas de columnas:
todo vive aqui y los scripts lo importan. Es la unica fuente de verdad.
"""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIR_RAW = RAIZ / "data" / "raw"
DIR_PROCESSED = RAIZ / "data" / "processed"

# ==========================================================================
# OBTENCION (extraccion.py) — buscador de establecimientos del MINEDUC
# ==========================================================================
# Sitio: ASP.NET WebForms detras de Imperva, con dropdowns en cascada
# (elegir departamento hace un postback que puebla municipio). Por eso se
# maneja con un navegador real (Playwright), no con requests.

URL_BUSCADOR = "https://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/"

# Prefijo comun de los ids de los controles del formulario (WebForms).
PREFIJO = "#_ctl0_ContentPlaceHolder1_"
ID_DEPARTAMENTO = PREFIJO + "cmbDepartamento"
ID_MUNICIPIO = PREFIJO + "cmbMunicipio"
ID_NIVEL = PREFIJO + "cmbNivel"
ID_CONSULTAR = PREFIJO + "IbtnConsultar"
ID_TABLA_RESULTADO = PREFIJO + "dgResultado"
ID_CERRAR_AVISO = "#_ctl0_btnCerrarAvisoLegal"

# Valor del dropdown Nivel Escolar que nos interesa: DIVERSIFICADO.
NIVEL_DIVERSIFICADO = "46"

# Navegador de Playwright: None usa el chromium que instala 00_init.py
# (reproducible). Si Imperva llegara a retar a ese chromium, cambiar a
# "chrome" para usar el Google Chrome del sistema.
CANAL_NAVEGADOR = None

# Los 23 departamentos del pais: (codigo del dropdown, nombre, slug de archivo).
# Se itera sobre todos para garantizar TODOS los establecimientos del pais.
DEPARTAMENTOS = [
    ("00", "CIUDAD CAPITAL", "ciudad_capital"),
    ("01", "GUATEMALA", "guatemala"),
    ("02", "EL PROGRESO", "el_progreso"),
    ("03", "SACATEPEQUEZ", "sacatepequez"),
    ("04", "CHIMALTENANGO", "chimaltenango"),
    ("05", "ESCUINTLA", "escuintla"),
    ("06", "SANTA ROSA", "santa_rosa"),
    ("07", "SOLOLA", "solola"),
    ("08", "TOTONICAPAN", "totonicapan"),
    ("09", "QUETZALTENANGO", "quetzaltenango"),
    ("10", "SUCHITEPEQUEZ", "suchitepequez"),
    ("11", "RETALHULEU", "retalhuleu"),
    ("12", "SAN MARCOS", "san_marcos"),
    ("13", "HUEHUETENANGO", "huehuetenango"),
    ("14", "QUICHE", "quiche"),
    ("15", "BAJA VERAPAZ", "baja_verapaz"),
    ("16", "ALTA VERAPAZ", "alta_verapaz"),
    ("17", "PETEN", "peten"),
    ("18", "IZABAL", "izabal"),
    ("19", "ZACAPA", "zacapa"),
    ("20", "CHIQUIMULA", "chiquimula"),
    ("21", "JALAPA", "jalapa"),
    ("22", "JUTIAPA", "jutiapa"),
]


def ruta_raw_departamento(codigo, slug):
    """Ruta del CSV crudo de un departamento: data/raw/diversificado_NN_slug.csv"""
    return DIR_RAW / f"diversificado_{codigo}_{slug}.csv"


# Contrato de las columnas crudas: los 17 encabezados que devuelve la tabla
# de resultados del buscador, en orden y con el texto exacto de la fuente.
# El crudo se guarda tal cual (no se normalizan nombres aqui: eso es limpieza).
COLUMNAS_CRUDAS = [
    "CODIGO",
    "DISTRITO",
    "DEPARTAMENTO",
    "MUNICIPIO",
    "ESTABLECIMIENTO",
    "DIRECCION",
    "TELEFONO",
    "SUPERVISOR",
    "DIRECTOR",
    "NIVEL",
    "SECTOR",
    "AREA",
    "STATUS",
    "MODALIDAD",
    "JORNADA",
    "PLAN",
    "DEPARTAMENTAL",
]

# ==========================================================================
# LIMPIEZA (run_pipeline.py) — rutas por etapa
# ==========================================================================
# TODO: definir cuando lleguen las instrucciones de limpieza. Ejemplo:
# RUTA_INGESTA = DIR_PROCESSED / "01_ingesta.csv"     # <- 01_ingesta.py
# RUTA_FINAL   = DIR_PROCESSED / "establecimientos_diversificado_limpio.csv"
