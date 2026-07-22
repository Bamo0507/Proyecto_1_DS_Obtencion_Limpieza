# Informe de calidad de los datos

Este informe compara el estado del conjunto de establecimientos educativos de nivel diversificado antes y después del proceso de limpieza. El estado "antes" corresponde a los 23 archivos crudos ya consolidados en un solo dataset (17 variables, sin ninguna transformación aplicada); el estado "después" corresponde al dataset final, luego de correr las 10 etapas del pipeline descritas en docs/plan_de_limpieza.md y docs/Registro_de_Transformaciones.md.

| Métrica | Antes | Después |
|---|---|---|
| Registros | 11,867 | 11,867 |
| Variables | 17 | 16 |
| Valores faltantes | 3,826 celdas (1.90% de 201,739) | 3,960 celdas (2.09% de 189,872) |
| Variables con NA | 6 de 17 | 6 de 16 |
| Duplicados exactos | 0 | 0 |
| Posibles duplicados | No se aplicó detección por similitud | 0 fusionados o eliminados; los registros multi-servicio se conservan como legítimos |
| Variables con formato inconsistente | 3 (distrito, telefono, direccion_departamental) | 0 |
| Variables con tipo incorrecto | 0 | 0 |
| Categorías inconsistentes | 0 | 0 |
| Errores corregidos | 0 | 11,150 correcciones de contenido |

## Explicación de cada métrica

**Registros.** El número de filas no cambió: 11,867 antes y después. No se eliminó ningún registro porque el diagnóstico inicial no encontró duplicados exactos, y la política del proyecto fue no eliminar automáticamente los posibles duplicados parciales, sino documentarlos y conservarlos (ver más abajo).

**Variables.** El dataset crudo trae 17 columnas. Se eliminó nivel porque es constante en DIVERSIFICADO para las 11,867 observaciones (efecto del filtro con que se extrajeron los datos) y no aporta variabilidad al análisis, dejando 16 variables en el dataset final. Ninguna variable derivada fue añadida: departamental se renombró a direccion_departamental para no confundirse con departamento, pero sigue siendo la misma columna de origen.

**Valores faltantes.** Antes de la limpieza había 3,826 celdas vacías (1.90% del total de 201,739 celdas). Después de la limpieza hay 3,960 celdas vacías (2.09% de 189,872 celdas). El número subió porque varias de las transformaciones consistieron en destapar faltantes que venían disfrazados de valor: 70 códigos de distrito truncados, 5 direcciones marcadas solo con un punto, 61 marcadores de director como "SIN DATO" o ceros, y 3 valores de area como "SIN ESPECIFICAR" pasaron a NaN explícito. Ese aumento es intencional: refleja el faltante real del dataset en lugar de esconderlo detrás de una categoría o un texto sin sentido. En contraparte, los 5 registros sin establecimiento se completaron con un nombre trazable, por lo que esa variable dejó de tener faltantes.

**Variables con NA.** Se mantienen en 6 tanto antes como después, pero la composición cambia: antes eran director, telefono, supervisor, distrito, direccion y establecimiento; después son director, telefono, supervisor, distrito, direccion y area (establecimiento se completó y area ganó los 3 faltantes que antes estaban disfrazados de "SIN ESPECIFICAR").

**Duplicados exactos.** No se encontraron registros idénticos en todas sus columnas, ni antes ni después de la limpieza, por lo que esta métrica se mantiene en 0.

**Posibles duplicados.** Para buscar posibles duplicados, se agruparon los registros acorde a las características que tuvieran que ver con el nombre del establecimiento, la dirección, el municipio y el departamento, ya que la lógica era que, si se comparten estos cuatro atributos, probablemente se está haciendo referencia al mismo lugar. Con este criterio se identificaron 1,545 grupos que compartían esas variables. Sin embargo, al analizar cada una de las observaciones dentro de estos grupos, nos dimos cuenta de que había escenarios en donde lo único que cambiaba era el plan, y es ahí donde caímos en cuenta de que en realidad cada observación no representa un único establecimiento, sino un servicio educativo. Por ejemplo, un mismo establecimiento puede prestar educación en jornada matutina y a la vez en jornada vespertina, o tener un servicio entre semana y otro en fin de semana. Es por esto que estas observaciones no se consideran duplicados, de tal forma que se conservan todas como registros legítimos, sin fusionar ni eliminar ninguna.

**Variables con formato inconsistente.** Antes de la limpieza, tres variables presentaban problemas de formato: distrito, que mezclaba dos formatos válidos y traía 70 códigos truncados; telefono, con 251 celdas que tenían varios números o separadores dentro de una misma celda; y direccion_departamental, que venía con una acentuación inconsistente respecto a departamento, con 2,025 valores con tilde. Las tres quedaron con formato consistente después de la limpieza, lo cual se valida con las comprobaciones del pipeline y las pruebas automáticas. Cabe mencionar que la corrección del 0 escrito en lugar de la letra O en supervisor se contabiliza como un error corregido y no como un problema de formato, por tratarse de un error de digitación puntual.

**Variables con tipo incorrecto.** Ninguna variable presentó este problema, ni antes ni después. Todas las columnas del dataset son de naturaleza cualitativa (identificadores o categorías, incluidas codigo, distrito y telefono, que aunque parecen numéricas funcionan como etiquetas), por lo que se cargaron y se mantienen como texto desde la etapa de ingesta.

**Categorías inconsistentes.** Ninguna de las variables categóricas presentaba el mismo valor escrito de formas distintas, por lo que esta métrica queda en 0 tanto antes como después. Estas variables son sector, area, status, modalidad, jornada, plan, departamento y municipio. Ahora bien, en el caso del plan sí se unificaron sus 13 categorías originales en solo 4, que son entre semana, fin de semana, a distancia y mixto, ya que muchas de ellas estaban repetidas en el dataset original y resultaban redundantes al hacer referencia a lo mismo.

**Errores corregidos.** En total se modificaron 11,150 valores de contenido a lo largo de las variables director (61), direccion (5), area (3), establecimiento (5), supervisor (3), telefono (201), distrito (70) y plan (8,777), más 2,025 en direccion_departamental por la estandarización de tildes. Esta cifra no incluye la eliminación de la columna nivel (cambio estructural que afecta a las 16 columnas finales, no al contenido de una fila) ni el renombrado de columnas (cambio de esquema). El detalle completo, con la justificación de cada transformación, está en docs/Registro_de_Transformaciones.md.

## Reproducibilidad

Las cifras "antes" se obtienen concatenando los 23 archivos de data/raw/ sin ninguna transformación (equivalente a python src/01_ingesta.py). Las cifras "después" corresponden a data/processed/establecimientos_diversificado_limpio.csv, generado corriendo python src/00_init.py y luego python src/run_pipeline.py.
