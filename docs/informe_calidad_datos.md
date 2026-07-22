# Informe de calidad de los datos

Este informe compara el estado del conjunto de establecimientos educativos de nivel diversificado antes y después del proceso de limpieza. El estado "antes" corresponde a los 23 archivos crudos ya consolidados en un solo dataset (17 variables, sin ninguna transformación aplicada); el estado "después" corresponde al dataset final, luego de correr las 10 etapas del pipeline descritas en `docs/plan_de_limpieza.md` y `docs/Registro_de_Transformaciones.md`.

| Métrica | Antes | Después |
|---|---|---|
| Registros | 11,867 | 11,867 |
| Variables | 17 | 16 |
| Valores faltantes | 3,826 celdas (1.90% de 201,739) | 3,960 celdas (2.09% de 189,872) |
| Variables con NA | 6 de 17 | 6 de 16 |
| Duplicados exactos | 0 | 0 |
| Posibles duplicados | No se aplicó una técnica de similitud de cadenas; sin cifra | Sin cambios: no se implementó esta detección |
| Variables con formato inconsistente | 3 (distrito, telefono, supervisor) | 0 |
| Variables con tipo incorrecto | 0 | 0 |
| Categorías inconsistentes | 13 categorías solapadas en plan | 0 |
| Errores corregidos | 0 | 11,150 correcciones de contenido |

## Explicación de cada métrica

**Registros.** El número de filas no cambió: 11,867 antes y después. No se eliminó ningún registro porque el diagnóstico inicial no encontró duplicados exactos, y la política del proyecto fue no eliminar automáticamente los posibles duplicados parciales, sino documentarlos y conservarlos (ver más abajo).

**Variables.** El dataset crudo trae 17 columnas. Se eliminó `nivel` porque es constante en `DIVERSIFICADO` para las 11,867 observaciones (efecto del filtro con que se extrajeron los datos) y no aporta variabilidad al análisis, dejando 16 variables en el dataset final. Ninguna variable derivada fue añadida: `departamental` se renombró a `direccion_departamental` para no confundirse con `departamento`, pero sigue siendo la misma columna de origen.

**Valores faltantes.** Antes de la limpieza había 3,826 celdas vacías (1.90% del total de 201,739 celdas). Después de la limpieza hay 3,960 celdas vacías (2.09% de 189,872 celdas). El número subió porque varias de las transformaciones consistieron en destapar faltantes que venían disfrazados de valor: 70 códigos de `distrito` truncados, 5 direcciones marcadas solo con un punto, 61 marcadores de `director` como "SIN DATO" o ceros, y 3 valores de `area` como "SIN ESPECIFICAR" pasaron a NaN explícito. Ese aumento es intencional: refleja el faltante real del dataset en lugar de esconderlo detrás de una categoría o un texto sin sentido. En contraparte, los 5 registros sin `establecimiento` se completaron con un nombre trazable, por lo que esa variable dejó de tener faltantes.

**Variables con NA.** Se mantienen en 6 tanto antes como después, pero la composición cambia: antes eran `director`, `telefono`, `supervisor`, `distrito`, `direccion` y `establecimiento`; después son `director`, `telefono`, `supervisor`, `distrito`, `direccion` y `area` (`establecimiento` se completó y `area` ganó los 3 faltantes que antes estaban disfrazados de "SIN ESPECIFICAR").

**Duplicados exactos.** No se encontraron registros idénticos en todas sus columnas, ni antes ni después de la limpieza, por lo que esta métrica se mantiene en 0.

**Posibles duplicados.** El proyecto no implementó una técnica de similitud de cadenas (Levenshtein, Jaro-Winkler, RapidFuzz u equivalente) para buscar duplicados parciales, por lo que esta métrica no tiene una cifra que reportar. Lo único relacionado que existe es un hallazgo distinto del EDA inicial (`notebooks/eda_previo_limpieza.ipynb`, inciso h): agrupando por coincidencia **exacta** de `establecimiento`, `direccion`, `departamento` y `municipio` aparecen 1,545 grupos con más de un `codigo` (hasta 10 en un mismo grupo). Ese hallazgo no es una detección de duplicados: el propio análisis concluye que esos grupos son el mismo centro físico con distintos servicios autorizados (jornada o plan distinto), es decir, registros legítimos y no un problema de calidad. Confundir ese hallazgo de granularidad con "duplicados parciales" sería incorrecto, así que se deja fuera de esta métrica. Queda pendiente implementar la búsqueda de duplicados parciales por similitud de cadenas que pide el punto 5g de la guía.

**Variables con formato inconsistente.** Antes de la limpieza, tres variables presentaban problemas de formato: `distrito` (mezclaba dos formatos válidos y traía 70 códigos truncados), `telefono` (251 celdas con varios números o separadores dentro de una misma celda) y `supervisor` (un error de digitación con un 0 en lugar de la letra O). Las tres quedaron con formato consistente después de la limpieza, verificado con las pruebas automáticas de `tests/test_conjunto_limpio.py`.

**Variables con tipo incorrecto.** Ninguna variable presentó este problema, ni antes ni después. Todas las columnas del dataset son de naturaleza cualitativa (identificadores o categorías, incluidas `codigo`, `distrito` y `telefono`, que aunque parecen numéricas funcionan como etiquetas), por lo que se cargaron y se mantienen como texto desde la etapa de ingesta.

**Categorías inconsistentes.** La variable `plan` traía 13 categorías que solapaban dos ideas distintas (el horario semanal y la modalidad de estudio), como `SABATINO` y `DOMINICAL` frente a `FIN DE SEMANA`. Se consolidaron en 4 categorías finales (`ENTRE SEMANA`, `FIN DE SEMANA`, `A DISTANCIA`, `MIXTO`). El resto de variables categóricas (`sector`, `area`, `status`, `modalidad`, `jornada`) ya venían sin categorías repetidas por diferencias de escritura, lo cual se confirma después de la limpieza con las pruebas automáticas.

**Errores corregidos.** En total se modificaron 11,150 valores de contenido a lo largo de las variables `director` (61), `direccion` (5), `area` (3), `establecimiento` (5), `supervisor` (3), `telefono` (201), `distrito` (70) y `plan` (8,777), más 2,025 en `direccion_departamental` por la estandarización de tildes. Esta cifra no incluye la eliminación de la columna `nivel` (cambio estructural que afecta a las 16 columnas finales, no al contenido de una fila) ni el renombrado de columnas (cambio de esquema). El detalle completo, con la justificación de cada transformación, está en `docs/Registro_de_Transformaciones.md`.

## Reproducibilidad

Las cifras "antes" se obtienen concatenando los 23 archivos de `data/raw/` sin ninguna transformación (equivalente a `python src/01_ingesta.py`). Las cifras "después" corresponden a `data/processed/establecimientos_diversificado_limpio.csv`, generado corriendo `python src/00_init.py` y luego `python src/run_pipeline.py`.
