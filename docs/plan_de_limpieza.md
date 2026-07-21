# Plan de limpieza de los establecimientos de nivel diversificado (MINEDUC)

Antes de modificar los datos, se elabora este plan de limpieza en el que, para cada variable, se describen los problemas encontrados durante el análisis exploratorio, la regla que se utilizará para corregirlos junto con la razón por la que consideramos que funcionará, y los riesgos asociados a cada transformación. Cabe mencionar que este plan consolida lo identificado en el diagnóstico previo, de los incisos A a H.

## CODIGO:

No se identificaron problemas de calidad en esta variable, ya que el código está bien formado en las 11,867 observaciones, cumpliendo el patrón ##-##-####-##. Adicional, resulta ser una llave única a nivel nacional, sin duplicados entre archivos.

## DISTRITO:

**Problemas encontrados:** se identificaron 532 valores faltantes. Adicional, la variable mezcla dos formatos válidos, uno largo con la forma ##-##-#### y uno corto con la forma ##-###, y también aparecen 70 registros truncados, como 01-, 10- o 17-, que básicamente son códigos incompletos que no aportan información.

**Regla de corrección y justificación:** los registros truncados, al no calzar con ninguno de los dos formatos válidos, se convierten a NaN por tratarse de un dato inválido e irreparable, mientras que los dos formatos válidos se conservan tal como vienen, ya que ambos identifican correctamente al distrito. Consideramos que esto funciona porque separamos los datos que no están completados de los que sí lo están, sin tratar de eliminar ni de adivinar cuál es el valor real de esta variable para algunas observaciones en específico.

**Riesgos asociados a la transformación:** el principal riesgo es que, al mantener los dos formatos, cualquier análisis que cruce por distrito deberá contemplar ambas formas para no dejar registros fuera, y además estamos asumiendo que un código truncado es irrecuperable, cuando en teoría podría completarse si se contara con otra fuente de datos, cosa que por el momento no tenemos.

## DEPARTAMENTO:

No se identificaron problemas en esta variable, ya que se encuentra completa en todas las observaciones, presenta los 23 valores esperados y viene escrita de forma consistente, en mayúsculas y sin tildes.

## MUNICIPIO:

No se identificaron problemas reales en esta variable. Si bien en la capital los valores aparecen como ZONA 1 hasta ZONA 25 en lugar de un nombre de municipio, esto no es un error, sino la forma legítima en que se organiza la capital, de tal forma que se maneja por zonas.

## ESTABLECIMIENTO:

**Problemas encontrados:** se identificaron 5 registros que no cuentan con el nombre del centro educativo, siendo este el identificador legible con el que cualquier persona logra ubicar a la institución, por lo que resulta llamativo que estén vacíos. Cabe mencionar que los 5 casos corresponden a establecimientos que están CERRADA DEFINITIVAMENTE, de tal forma que probablemente se trate de registros antiguos en los que el nombre no quedó capturado.

**Regla de corrección y justificación:** en lugar de dejar estos registros como NaN, se construye un nombre genérico a partir de la ubicación, combinando un texto fijo que deje claro que es un nombre asignado con el municipio y el departamento del establecimiento, de tal forma que quede algo como SIN NOMBRE - VILLA NUEVA, GUATEMALA. Consideramos que esto funciona porque completa el rubro con una etiqueta útil y trazable, sin pretender adivinar el nombre real, ya que el propio texto deja explícito que el nombre no existía en el origen. Adicional, se evita usar una palabra como colegio, dado que varios de estos casos son del sector oficial y no serían colegios, por lo que un texto neutro resulta más correcto.

**Riesgos asociados a la transformación:** el principal riesgo es que estamos introduciendo un valor que no vino del origen, por lo que cualquier análisis que utilice el nombre debe tener claro que estos 5 son etiquetas construidas y no nombres reales. No obstante, al ser únicamente 5 registros de 11,867 y al dejar el texto marcado explícitamente como sin nombre, el impacto es mínimo y no se presta a confundirlo con una institución real.

## DIRECCION:

**Problemas encontrados:** se identificaron 76 valores faltantes y 5 registros que traen un punto como dirección, el cual es un no-dato disfrazado. Adicional, la variable presenta la heterogeneidad propia de un texto libre, con abreviaturas distintas y mezcla de mayúsculas y minúsculas.

**Regla de corrección y justificación:** los registros que vienen como un punto se convierten a NaN por tratarse de un no-dato, mientras que la dirección válida se conserva como texto, sin aplicar una normalización fina. Consideramos que esto funciona porque reconocemos que un punto no representa una dirección real, y a la vez evitamos alterar direcciones que sí son válidas al no forzar un formato sobre un campo que por naturaleza es libre.

**Riesgos asociados a la transformación:** al ser un texto libre que no se estandariza a fondo, cualquier análisis que dependa de la dirección exacta podría verse afectado por las variantes de escritura, como abreviaturas o acentos distintos para una misma dirección.

## TELEFONO:

**Problemas encontrados:** se identificaron 946 valores faltantes y 251 valores que no corresponden a un número simple de 8 dígitos, en donde se meten varios números dentro de una misma celda separados por guiones, comas, espacios o incluso una Y, tal como 22202870-73 o 25763, 26725 Y 21568, además de algunos números más cortos.

**Regla de corrección y justificación:** nos quedamos con un único número principal, tomando el primer número que aparece antes del primer separador, y los que resulten irreparables se dejan como NaN. Consideramos que esto funciona porque un solo número de contacto es suficiente para el propósito del registro, de tal forma que evitamos celdas con varios números que son difíciles de utilizar en un análisis.

**Riesgos asociados a la transformación:** el principal riesgo es que se pierde la información de los números secundarios, aunque esta se mantiene en el crudo, y además la regla del número principal es un supuesto, por lo que algunos números que conservemos quedarán con menos de 8 dígitos.

## SUPERVISOR:

**Problemas encontrados:** se identificaron 535 valores faltantes y al menos un error de digitación en donde un nombre termina en cero en lugar de la letra O, como en el caso de ACEVED0.

**Regla de corrección y justificación:** los valores faltantes se dejan como NaN, mientras que los errores de digitación se corrigen únicamente cuando el error es evidente, como el cero final que debería ser una O. Consideramos que esto funciona porque corregimos solo cuando el dato realmente existe y el error es claro, sin ponernos a inventar nombres que no tenemos.

**Riesgos asociados a la transformación:** corregir nombres puede introducir cierto criterio subjetivo, es por esto que nos limitamos únicamente a los errores obvios, de tal forma que minimizamos la posibilidad de alterar un nombre que en realidad sí era correcto.

## DIRECTOR:

**Problemas encontrados:** es la variable con más ausencias, con 1,732 valores faltantes que representan un 14.6%. Adicional, concentra faltantes disfrazados como SIN DATO, guiones, puntos y ceros, tal como 0, 000000 o 0000000.

**Regla de corrección y justificación:** todos esos marcadores se unifican a NaN, de forma explícita por columna, para dejarlos en un mismo estado. Consideramos que esto funciona porque el faltante queda en un único estado honesto y medible, en lugar de estar repartido en muchas representaciones distintas que dificultan cuantificar el vacío real.

**Riesgos asociados a la transformación:** estamos asumiendo que esos marcadores siempre representan un no-dato, lo cual es razonable dado el contexto de un nombre de director, aunque no podemos descartar por completo que algún valor atípico como un cero formara parte de algo real, cosa que resulta poco probable en este tipo de campo.

## NIVEL:

**Problemas encontrados:** la variable es constante, ya que todas las observaciones tienen el valor DIVERSIFICADO por el filtro con que se extrajeron los datos, cosa que además se confirma con el sufijo -46 del código, de tal forma que no aporta ninguna variabilidad al dataset.

**Regla de corrección y justificación:** se elimina la columna, en su propia etapa de la pipeline. Consideramos que esto funciona porque una variable que toma un único valor no discrimina entre observaciones ni aporta información para ningún análisis, de tal forma que solo estaría ocupando espacio.

**Riesgos asociados a la transformación:** el riesgo es que se pierde la etiqueta explícita de que todo el dataset es de nivel diversificado, cosa que se mitiga dejándolo documentado en el codebook y en este mismo plan.

## SECTOR:

No se identificaron problemas en esta variable, ya que presenta las cuatro categorías esperadas, que son PRIVADO, OFICIAL, COOPERATIVA y MUNICIPAL, con una cantidad razonable de conteos en cada una.

## AREA:

**Problemas encontrados:** la variable incluye la categoría SIN ESPECIFICAR en 3 registros, la cual es un no-dato disfrazado de categoría válida, ya que un establecimiento necesariamente es urbano o rural.

**Regla de corrección y justificación:** los registros con SIN ESPECIFICAR se convierten a NaN, y no al revés, es decir, no se estandariza todo el vacío hacia esa categoría. Consideramos que esto funciona porque reconoce que ese valor no es una categoría real sino un dato ausente, de tal forma que en los análisis no se cuente como una tercera opción válida junto a urbana y rural.

**Riesgos asociados a la transformación:** el riesgo es mínimo, ya que son únicamente 3 registros, por lo que el impacto sobre la variable es prácticamente nulo.

## STATUS:

No se identificaron problemas de calidad en esta variable. Si bien cerca del 42% de los registros no están ABIERTA, ya que hay establecimientos cerrados temporal o definitivamente, ambos estados son válidos, de tal forma que la variable se conserva sin cambios y la decisión de filtrar o no los cerrados se deja para cada análisis en específico.

## MODALIDAD:

No se identificaron problemas en esta variable, ya que solo presenta las dos categorías esperadas, que son MONOLINGUE y BILINGUE.

## JORNADA:

No se identificaron problemas que ameriten una transformación. Si bien aparece la categoría SIN JORNADA en 1,099 registros, al cruzarla con PLAN se observa que casi todos corresponden a planes semipresenciales o a distancia, en donde efectivamente no existe una jornada fija, de tal forma que no es un faltante disfrazado sino un valor legítimo que se conserva. Cabe mencionar que únicamente se revisarían los 2 casos que aparecen con un plan de fin de semana, por no calzar con ese patrón.

## PLAN:

**Problemas encontrados:** la variable tiene 13 categorías solapadas e inconsistentes que además mezclan dos ideas distintas, el horario semanal, como entre semana o fin de semana, y la modalidad de estudio, como presencial, semipresencial o a distancia. Adicional, hay categorías como SABATINO y DOMINICAL que en la práctica son fin de semana, y otras como IRREGULAR e INTERCALADO que resultan poco claras.

**Regla de corrección y justificación:** se consolidan las 13 categorías en cuatro, que son ENTRE SEMANA, FIN DE SEMANA, A DISTANCIA y MIXTO, sobreescribiendo la columna. La categoría ENTRE SEMANA agrupa el diario regular y los semipresenciales de un día, de dos días y sin día especificado, dado que su jornada es de entre semana; FIN DE SEMANA agrupa el fin de semana, el semipresencial de fin de semana, el sabatino y el dominical; A DISTANCIA agrupa el a distancia y el virtual, ya que son una modalidad y no un horario; y MIXTO queda únicamente para mixto, irregular e intercalado. Consideramos que esto funciona porque agrupa las categorías bajo un criterio único y explícito, de tal forma que se reduce el ruido de tener tantas categorías redundantes.

**Riesgos asociados a la transformación:** el principal riesgo es que se trata de una agrupación interpretativa, en donde mandar el semipresencial de un día a la semana hacia entre semana es un supuesto, ya que no se especifica cuál día es. Adicional, se pierde el detalle fino, como la diferencia entre sabatino y dominical o entre presencial y semipresencial, aunque este detalle se mantiene recuperable desde el crudo.

## DEPARTAMENTAL:

**Problemas encontrados:** la variable viene con tildes, como PETÉN o QUICHÉ, a diferencia de DEPARTAMENTO, que viene sin tildes, de tal forma que hay una inconsistencia de acentuación entre dos variables que representan lo geográfico. Cabe mencionar que además subdivide algunos departamentos, como Guatemala en norte, sur, oriente y occidente, razón por la cual tiene 26 valores para 23 departamentos, aunque esto último no es un error sino una unidad administrativa más fina.

**Regla de corrección y justificación:** se estandariza la acentuación quitando las tildes, para alinearla con DEPARTAMENTO y con la forma en que vienen escritos el resto de los nombres, mientras que la subdivisión administrativa se conserva por ser información real. Consideramos que esto funciona porque unifica el estilo de escritura sin alterar el significado del dato.

**Riesgos asociados a la transformación:** el riesgo es bajo, ya que quitar las tildes es un cambio cosmético que no modifica el contenido ni la identidad de la dirección departamental.

## Etapas de la pipeline

A partir de todo lo anterior, las transformaciones se organizan en las siguientes etapas de la pipeline, en donde cada etapa tiene una única responsabilidad y valida tanto su entrada como su salida:

1. **Ingesta:** cargar los 23 archivos con dtype de texto, validar el contrato de columnas y consolidarlos en un solo dataset, verificando que CODIGO siga siendo único y con el patrón esperado.
2. **Normalización de nulos:** unificar a NaN los marcadores de no-dato disfrazados de forma explícita por columna, en DIRECTOR, DIRECCION y AREA.
3. **Corrección de nombres:** construir el nombre genérico de los 5 registros de ESTABLECIMIENTO sin nombre y corregir el error de digitación evidente en SUPERVISOR.
4. **Teléfono:** quedarse con un único número principal y marcar como NaN los irreparables.
5. **Distrito:** convertir a NaN los códigos truncados, conservando los dos formatos válidos.
6. **Plan:** consolidar las 13 categorías en las cuatro definidas.
7. **Departamental:** estandarizar la acentuación quitando las tildes.
8. **Columnas:** eliminar NIVEL por ser constante.
9. **Final:** validaciones finales, clasificación de cada NaN y guardado del dataset limpio.
