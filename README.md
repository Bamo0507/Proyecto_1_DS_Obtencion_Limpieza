# Proyecto 1: Obtención y limpieza de establecimientos de nivel diversificado (MINEDUC)

Este proyecto obtiene y limpia el catálogo de establecimientos educativos de nivel diversificado de Guatemala, publicado por el Ministerio de Educación (MINEDUC). A lo largo de esta fase se descargaron los datos CRUZ para las diversas instituciones que se encuentran en el país, se definió y ejecutó un pipeline de limpieza por etapas, y se documentó y validó todo el proceso.

## Cómo reproducir

1. **python src/00_init.py**: crea el entorno virtual e instala las dependencias.
2. **source .venv/bin/activate**: activa el entorno (en Windows: .venv\Scripts\activate).
3. **python src/run_pipeline.py**: corre las 10 etapas de limpieza y genera el conjunto limpio.
4. **pytest**: ejecuta las pruebas de validación (también funciona python tests/test_conjunto_limpio.py).

La extracción de los datos crudos es un paso previo que se corre una sola vez con **python src/extraccion.py**; de todas formas, los datos crudos ya vienen versionados en la carpeta data/raw/, aparte se tiene data/processed/ con los CSVs ya transformados.

## Fases del proyecto

### 1. Extracción de datos

Se descargaron del buscador del MINEDUC todos los establecimientos de nivel diversificado del país, consultando por separado cada uno de los 23 departamentos, y se guardaron como CSV crudos, uno por departamento.

Dónde: [src/extraccion.py](src/extraccion.py) (script de extracción) y [data/raw/](data/raw/) (23 archivos crudos).

### 2. Análisis inicial de los datos

Análisis exploratorio previo a la limpieza que diagnostica el estado del crudo: número de registros y variables, tipos de dato, valores faltantes, duplicados, valores fuera de dominio, formatos inconsistentes y los problemas potenciales de calidad.

Dónde: [notebooks/eda_previo_limpieza.ipynb](notebooks/eda_previo_limpieza.ipynb).

### 3. Plan de limpieza

Documento que, para cada variable, describe el problema detectado, la regla que se utilizará para corregirlo con su justificación, y los riesgos de la transformación; además define las etapas de la pipeline.

Dónde: [docs/plan_de_limpieza.md](docs/plan_de_limpieza.md).

### 4. Pipeline de limpieza

Diez etapas encadenadas, con una sola responsabilidad por archivo, que llevan del crudo al conjunto limpio validando la entrada y la salida en cada paso. Están orquestadas por run_pipeline.py, con las rutas y constantes en config.py y las utilidades compartidas en utils.py.

Dónde: [src/](src/) (etapas 01_ingesta.py a 10_final.py) y [src/run_pipeline.py](src/run_pipeline.py).

### 5. Registro de transformaciones

Tabla que documenta cada modificación realizada: variable, problema detectado, transformación aplicada, registros afectados y justificación. Los conteos de registros afectados se calculan de forma reproducible en un notebook de trazabilidad.

Dónde: [docs/Registro_de_Transformaciones.md](docs/Registro_de_Transformaciones.md) y [notebooks/registros_afectados.ipynb](notebooks/registros_afectados.ipynb).

### 6. Validación del conjunto limpio

Pruebas automáticas que verifican la calidad del dataset final: ausencia de duplicados exactos, sin espacios en los bordes, teléfonos con formato consistente, departamentos y municipios dentro del catálogo oficial, tipos de dato esperados, categorías sin variantes de escritura y ausencia de los valores inválidos detectados en el diagnóstico.

Dónde: [tests/test_conjunto_limpio.py](tests/test_conjunto_limpio.py).

### 7. Informe de calidad de datos

Comparación del conjunto de datos antes y después de la limpieza, con una tabla de métricas y la explicación de cada una.

Dónde: [docs/informe_calidad_datos.md](docs/informe_calidad_datos.md).

### 8. Generación del conjunto limpio

El único conjunto de datos limpio, con la información de los 23 departamentos consolidada, con estructura consistente, nombres descriptivos y formato uniforme, listo para análisis.

Dónde: data/processed/establecimientos_diversificado_limpio.csv (se genera al correr el pipeline).

### 9. Libro de códigos

Diccionario del conjunto limpio: para cada variable incluye su descripción, tipo de dato, dominio permitido, valores posibles y tratamiento aplicado; más los metadatos del conjunto (fuente, fecha de extracción y versión) y la política de valores faltantes.

Dónde: [docs/libro_de_codigos.md](docs/libro_de_codigos.md).
