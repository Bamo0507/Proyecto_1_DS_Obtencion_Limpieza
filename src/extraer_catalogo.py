"""
Obtencion del catalogo oficial de ubicaciones (MINEDUC)
------------------------------------------------------------
Una sola responsabilidad: cosechar el catalogo de departamentos y municipios
directamente de los dropdowns del buscador del MINEDUC.

  Lee : dropdowns del buscador (config.URL_BUSCADOR)
  Hace: - para cada departamento, lee las opciones del dropdown de municipio
        - arma la lista (departamento, municipio) oficial
  Escribe: data/raw/catalogo_ubicaciones.csv

Este catalogo es la referencia oficial contra la cual las pruebas de validacion
verifican que los departamentos y municipios de los datos sean validos. Se
guarda fiel a la fuente; la normalizacion (tildes, mayusculas) se hace al comparar.

Ejecutar (con el venv activado):  python src/extraer_catalogo.py
"""

import time

import pandas as pd
from playwright.sync_api import TimeoutError as PWTimeout
from playwright.sync_api import sync_playwright

import config
from utils import afirmar, banner, guardar

TIMEOUT = 120_000


def cerrar_aviso(page):
    try:
        if page.locator(config.ID_CERRAR_AVISO).is_visible(timeout=1500):
            with page.expect_navigation():
                page.locator(config.ID_CERRAR_AVISO).click()
    except PWTimeout:
        pass


def main():
    banner("OBTENCION: catalogo oficial de departamentos y municipios (MINEDUC)")
    filas = []

    with sync_playwright() as playwright:
        lanzar = {"headless": True}
        if config.CANAL_NAVEGADOR:
            lanzar["channel"] = config.CANAL_NAVEGADOR
        navegador = playwright.chromium.launch(**lanzar)
        page = navegador.new_page()
        page.set_default_timeout(TIMEOUT)

        for codigo, nombre, _slug in config.DEPARTAMENTOS:
            page.goto(config.URL_BUSCADOR, wait_until="domcontentloaded", timeout=TIMEOUT)
            cerrar_aviso(page)
            with page.expect_navigation(wait_until="domcontentloaded", timeout=TIMEOUT):
                page.select_option(config.ID_DEPARTAMENTO, codigo)

            opciones = page.locator(config.ID_MUNICIPIO + " option").all_inner_texts()
            municipios = [opcion.strip() for opcion in opciones if opcion.strip().upper() != "TODOS"]
            afirmar(len(municipios) > 0, f"{nombre}: se obtuvieron municipios del dropdown")
            for municipio in municipios:
                filas.append((nombre, municipio))
            print(f"[ok]       {nombre}: {len(municipios)} municipios")
            time.sleep(1)

        navegador.close()

    catalogo = pd.DataFrame(filas, columns=["departamento", "municipio"])
    guardar(catalogo, config.RUTA_CATALOGO)


main()
