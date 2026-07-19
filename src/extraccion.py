"""
Obtencion del pipeline: EXTRACCION DE ESTABLECIMIENTOS (MINEDUC)
------------------------------------------------------------
Una sola responsabilidad: descargar del buscador del MINEDUC todos los
establecimientos de nivel DIVERSIFICADO del pais y guardarlos crudos.

  Lee : buscador web del MINEDUC (config.URL_BUSCADOR)
  Hace: - para cada uno de los 23 departamentos:
          selecciona departamento -> Nivel=DIVERSIFICADO -> Consultar
        - verifica que las filas parseadas == "N Establecimientos encontrados"
          (fail-fast: nunca guarda un departamento incompleto)
  Escribe: data/raw/diversificado_NN_<slug>.csv  (uno por departamento)

Este es el paso de OBTENCION: siembra data/raw/ una sola vez. Queda fuera
de run_pipeline.py (que orquesta la limpieza). data/raw/ es la fuente de
verdad congelada; para re-descargar un departamento, borra su .csv.

Ejecutar (con el venv activado):  python src/extraccion.py
"""

import re
import sys
import time

import pandas as pd
from playwright.sync_api import TimeoutError as PWTimeout
from playwright.sync_api import sync_playwright

import config
from utils import afirmar, banner, guardar

# Patron del codigo de establecimiento (##-##-####-##): ancla para contar filas.
PATRON_CODIGO = re.compile(r"^\d{2}-\d{2}-\d{4}-\d{2}$")
# Etiqueta que el sitio muestra con el total: "N Establecimientos encontrados".
PATRON_TOTAL = re.compile(r"(\d+)\s*Establecimientos encontrados")

MAX_INTENTOS = 3          # reintentos por departamento ante fallos de red
ESPERA_REINTENTO = 5      # segundos antes de reintentar
ESPERA_ENTRE_DEPTOS = 2   # pausa cortes entre departamentos (ser amable)
TIMEOUT = 120_000         # ms


# --- JS que extrae las filas de la tabla de resultados ---------------------
# Devuelve una lista de filas; cada fila es la lista de textos de sus celdas.
# Se toman solo las filas hijas directas de la tabla (evita tablas anidadas).
JS_FILAS = """
(sel) => {
  const t = document.querySelector(sel);
  if (!t) return null;
  const filas = t.querySelectorAll(':scope > tbody > tr');
  return Array.from(filas).map(
    tr => Array.from(tr.querySelectorAll(':scope > td, :scope > th'))
             .map(c => c.innerText.replace(/\\s+/g, ' ').trim())
  );
}
"""


def cerrar_aviso(page):
    """Cierra el modal de aviso legal si aparece al cargar."""
    try:
        if page.locator(config.ID_CERRAR_AVISO).is_visible(timeout=1500):
            with page.expect_navigation():
                page.locator(config.ID_CERRAR_AVISO).click()
    except PWTimeout:
        pass


def consultar_departamento(page, codigo):
    """Corre la busqueda de un departamento y devuelve (filas, total_anunciado).

    filas: lista de listas (celdas de cada fila, incluida la cabecera).
    total_anunciado: entero que el sitio reporta como total encontrado.
    """
    page.goto(config.URL_BUSCADOR, wait_until="domcontentloaded", timeout=TIMEOUT)
    cerrar_aviso(page)

    # Elegir departamento dispara un postback que recarga la pagina.
    with page.expect_navigation(wait_until="domcontentloaded", timeout=TIMEOUT):
        page.select_option(config.ID_DEPARTAMENTO, codigo)
    # Municipio queda en TODOS (default); solo fijamos el nivel.
    page.select_option(config.ID_NIVEL, config.NIVEL_DIVERSIFICADO)
    with page.expect_navigation(wait_until="domcontentloaded", timeout=TIMEOUT):
        page.click(config.ID_CONSULTAR)

    html = page.content()
    m = PATRON_TOTAL.search(html)
    total = int(m.group(1)) if m else None
    filas = page.evaluate(JS_FILAS, config.ID_TABLA_RESULTADO)
    return filas, total


def a_dataframe(filas):
    """Convierte las filas crudas en un DataFrame con las columnas del contrato.

    - Descarta la primera celda de cada fila (columna vacia de la tabla).
    - Se queda solo con filas cuyo CODIGO calza el patron (ignora cabecera/pie).
    """
    datos = []
    for fila in filas:
        if len(fila) < len(config.COLUMNAS_CRUDAS) + 1:
            continue
        celdas = fila[1:1 + len(config.COLUMNAS_CRUDAS)]
        if PATRON_CODIGO.match(celdas[0]):
            datos.append(celdas)
    return pd.DataFrame(datos, columns=config.COLUMNAS_CRUDAS)


def extraer_uno(page, codigo, nombre):
    """Extrae un departamento con reintentos; valida completitud; guarda."""
    for intento in range(1, MAX_INTENTOS + 1):
        try:
            filas, total = consultar_departamento(page, codigo)
            afirmar(total is not None,
                    f"{nombre}: se leyo el total 'N Establecimientos encontrados'")
            df = a_dataframe(filas)
            afirmar(len(df) == total,
                    f"{nombre}: filas parseadas ({len(df)}) == anunciadas ({total})")
            guardar(df, config.ruta_raw_departamento(codigo, nombre_slug(codigo)))
            return len(df)
        except PWTimeout as e:
            print(f"[reintento] {nombre}: timeout (intento {intento}/{MAX_INTENTOS})")
            if intento == MAX_INTENTOS:
                afirmar(False, f"{nombre}: agotados los reintentos ({e})")
            time.sleep(ESPERA_REINTENTO)


def nombre_slug(codigo):
    """Devuelve el slug de archivo del departamento a partir de su codigo."""
    for cod, _, slug in config.DEPARTAMENTOS:
        if cod == codigo:
            return slug
    afirmar(False, f"codigo de departamento desconocido: {codigo}")


def main():
    banner("OBTENCION: establecimientos DIVERSIFICADO (MINEDUC), por departamento")
    total_pais = 0
    canal = config.CANAL_NAVEGADOR

    with sync_playwright() as p:
        lanzar = {"headless": True}
        if canal:
            lanzar["channel"] = canal
        navegador = p.chromium.launch(**lanzar)
        page = navegador.new_page()
        page.set_default_timeout(TIMEOUT)

        for codigo, nombre, slug in config.DEPARTAMENTOS:
            ruta = config.ruta_raw_departamento(codigo, slug)
            if ruta.exists():
                print(f"[ok]       {nombre}: ya existe {ruta.name}, se omite")
                continue
            print(f"\n[extrayendo] {codigo} {nombre}")
            n = extraer_uno(page, codigo, nombre)
            total_pais += n
            time.sleep(ESPERA_ENTRE_DEPTOS)

        navegador.close()

    print()
    print(f"[ok]       obtencion completa: {total_pais} establecimientos nuevos guardados en {config.DIR_RAW}")


main()
