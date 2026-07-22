# Libro de códigos

## Metadatos generales del conjunto de datos

| Campo | Valor |
|---|---|
| Fuente de los datos | Ministerio de Educación de Guatemala (MINEDUC), Buscador de Establecimientos Educativos ([mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE](http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/)), filtrado por Nivel Escolar = DIVERSIFICADO, consultado por separado para los 23 departamentos del país. |
| Fecha de extracción | 18 de julio de 2026 |
| Versión del conjunto limpio | v1.0 — data/processed/establecimientos_diversificado_limpio.csv, generada el 21 de julio de 2026 |
| Dimensiones del conjunto limpio | 11,867 registros, 16 variables |
| Unidad de observación | Un servicio educativo autorizado de nivel diversificado (un mismo centro físico puede tener más de un registro si ofrece distintas jornadas o planes) |
| Variables derivadas | Ninguna. Todas las columnas provienen directamente de la fuente; los únicos cambios de esquema fueron renombrar departamental a direccion_departamental y eliminar nivel por ser constante. |

A continuación se describe cada variable del conjunto limpio, en el orden en que aparece en el CSV final.

## codigo

- **Descripción:** identificador único de cada establecimiento o servicio educativo autorizado; es la llave primaria del dataset.
- **Tipo de dato:** texto (identificador nominal).
- **Dominio permitido:** patrón ##-##-####-## (regex ^\d{2}-\d{2}-\d{4}-\d{2}$); el sufijo final es siempre 46, correspondiente al nivel diversificado.
- **Valores posibles:** 11,867 valores únicos, uno por registro. Ejemplo: 02-01-0027-46.
- **Tratamiento aplicado:** ninguno. No se detectaron problemas de calidad; se validó su unicidad y su patrón desde la etapa de ingesta.

## distrito

- **Descripción:** código del distrito educativo al que pertenece el establecimiento.
- **Tipo de dato:** texto (identificador nominal).
- **Dominio permitido:** formato largo ##-##-#### o formato corto ##-###; o valor faltante.
- **Valores posibles:** 1,681 valores únicos en el crudo. Ejemplos: 02-01-0175 (largo), 01-025 (corto).
- **Tratamiento aplicado:** los 70 códigos truncados que no calzaban con ningún formato válido (p. ej. 01-, 10-, 17-) se convirtieron a NaN por ser irreparables; los dos formatos válidos se conservaron tal cual. Quedó con 602 valores faltantes (5.07%).

## departamento

- **Descripción:** departamento del país donde se ubica el establecimiento. El MINEDUC maneja Ciudad Capital como una entidad separada de Guatemala.
- **Tipo de dato:** texto (categórica nominal).
- **Dominio permitido:** catálogo cerrado de 23 valores.
- **Valores posibles:** CIUDAD CAPITAL, GUATEMALA, EL PROGRESO, SACATEPEQUEZ, CHIMALTENANGO, ESCUINTLA, SANTA ROSA, SOLOLA, TOTONICAPAN, QUETZALTENANGO, SUCHITEPEQUEZ, RETALHULEU, SAN MARCOS, HUEHUETENANGO, QUICHE, BAJA VERAPAZ, ALTA VERAPAZ, PETEN, IZABAL, ZACAPA, CHIQUIMULA, JALAPA, JUTIAPA.
- **Tratamiento aplicado:** ninguno. La variable llegó completa (0 faltantes) y con escritura consistente (mayúsculas, sin tildes).

## municipio

- **Descripción:** municipio donde se ubica el establecimiento. En Ciudad Capital toma la forma de zona (ZONA 1 a ZONA 25) en lugar de un nombre de municipio, lo cual es la forma legítima en que el MINEDUC organiza la capital.
- **Tipo de dato:** texto (categórica nominal).
- **Dominio permitido:** 363 combinaciones válidas de (departamento, municipio), según el catálogo oficial cosechado de los dropdowns del buscador (data/raw/catalogo_ubicaciones.csv); 358 de esas combinaciones están representadas en los datos.
- **Valores posibles:** ejemplos: GUASTATOYA, ZONA 1, ..., ZONA 25, entre otros municipios del catálogo.
- **Tratamiento aplicado:** ninguno. Completa y consistente en todas las observaciones.

## establecimiento

- **Descripción:** nombre propio del centro educativo.
- **Tipo de dato:** texto libre (categórica nominal).
- **Dominio permitido:** cualquier cadena no vacía.
- **Valores posibles:** 6,312 valores únicos en el crudo.
- **Tratamiento aplicado:** los 5 registros sin nombre (todos con status = CERRADA DEFINITIVAMENTE) se completaron con un nombre genérico y trazable, con el formato SIN NOMBRE - MUNICIPIO, DEPARTAMENTO, construido a partir de la ubicación del establecimiento. Después de la limpieza no quedan valores faltantes en esta variable.

## direccion

- **Descripción:** dirección física del establecimiento.
- **Tipo de dato:** texto libre (categórica nominal).
- **Dominio permitido:** cualquier cadena no vacía; o valor faltante.
- **Valores posibles:** 7,438 valores únicos en el crudo.
- **Tratamiento aplicado:** los 5 registros que traían un punto (.) como dirección se convirtieron a NaN, por tratarse de un no-dato disfrazado; el resto del texto libre se conservó sin normalización fina, dada su heterogeneidad natural. Quedó con 81 valores faltantes (0.68%).

## telefono

- **Descripción:** número de teléfono principal de contacto del establecimiento.
- **Tipo de dato:** texto (identificador; numérico en apariencia pero sin sentido operacional).
- **Dominio permitido:** cadena de solo dígitos, longitud mayoritariamente de 8; o valor faltante.
- **Valores posibles:** 6,571 valores únicos en el crudo. Ejemplo: 79450881.
- **Tratamiento aplicado:** cuando la celda traía varios números separados por guiones, comas, espacios o la letra "Y" (p. ej. 22202870-73 o 25763, 26725 Y 21568), se conservó únicamente el primer número antes del primer separador y solo sus dígitos, afectando 201 registros. Los faltantes no cambiaron: 946 (7.97%).

## supervisor

- **Descripción:** nombre del supervisor educativo asignado al establecimiento.
- **Tipo de dato:** texto libre (categórica nominal).
- **Dominio permitido:** cualquier cadena no vacía; o valor faltante.
- **Valores posibles:** 1,280 valores únicos en el crudo.
- **Tratamiento aplicado:** se corrigió el error de digitación evidente en el que un 0 aparece pegado a letras en lugar de la letra O (p. ej. ACEVED0 → ACEVEDO), afectando 3 registros del mismo supervisor. Los faltantes no cambiaron: 535 (4.51%).

## director

- **Descripción:** nombre del director del establecimiento.
- **Tipo de dato:** texto libre (categórica nominal).
- **Dominio permitido:** cualquier cadena no vacía; o valor faltante.
- **Valores posibles:** 5,519 valores únicos en el crudo.
- **Tratamiento aplicado:** se unificaron a NaN los marcadores de no-dato disfrazados (SIN DATO, -, ., 0, 000000, 0000000), afectando 61 registros. Es la variable con más valores faltantes del dataset: 1,793 (15.11%).

## sector

- **Descripción:** entidad que administra o financia el establecimiento.
- **Tipo de dato:** texto (categórica nominal).
- **Dominio permitido:** PRIVADO, OFICIAL, COOPERATIVA, MUNICIPAL.
- **Valores posibles:** ver dominio permitido.
- **Tratamiento aplicado:** ninguno. Completa y con las 4 categorías esperadas, cada una con una cantidad razonable de conteos.

## area

- **Descripción:** área geográfica donde se ubica el establecimiento.
- **Tipo de dato:** texto (categórica nominal).
- **Dominio permitido:** URBANA, RURAL.
- **Valores posibles:** ver dominio permitido.
- **Tratamiento aplicado:** los 3 registros con SIN ESPECIFICAR (categoría no válida, ya que un establecimiento es necesariamente urbano o rural) se convirtieron a NaN. Quedó con 3 valores faltantes (0.03%).

## status

- **Descripción:** estado operativo del establecimiento.
- **Tipo de dato:** texto (categórica nominal).
- **Dominio permitido:** ABIERTA, CERRADA TEMPORALMENTE, CERRADA DEFINITIVAMENTE, TEMPORAL TITULOS, TEMPORAL NOMBRAMIENTO.
- **Valores posibles:** ver dominio permitido.
- **Tratamiento aplicado:** ninguno. Completa y consistente; cerca del 42% de los registros no están en ABIERTA, lo cual es un estado legítimo y no un error.

## modalidad

- **Descripción:** modalidad lingüística de enseñanza.
- **Tipo de dato:** texto (categórica nominal).
- **Dominio permitido:** MONOLINGUE, BILINGUE.
- **Valores posibles:** ver dominio permitido.
- **Tratamiento aplicado:** ninguno. Completa y con solo las dos categorías esperadas.

## jornada

- **Descripción:** jornada horaria en que opera el establecimiento.
- **Tipo de dato:** texto (categórica nominal).
- **Dominio permitido:** MATUTINA, VESPERTINA, DOBLE, NOCTURNA, INTERMEDIA, SIN JORNADA.
- **Valores posibles:** ver dominio permitido.
- **Tratamiento aplicado:** ninguno. SIN JORNADA se conservó como valor legítimo (corresponde a planes semipresenciales y a distancia, donde no existe una jornada fija) y no se trató como un faltante disfrazado.

## plan

- **Descripción:** plan u horario de estudios del establecimiento; combina la periodicidad semanal y la modalidad de estudio.
- **Tipo de dato:** texto (categórica nominal).
- **Dominio permitido:** ENTRE SEMANA, FIN DE SEMANA, A DISTANCIA, MIXTO.
- **Valores posibles:** ver dominio permitido. Antes de la limpieza existían 13 categorías solapadas (DIARIO(REGULAR), tres variantes de SEMIPRESENCIAL, FIN DE SEMANA, SABATINO, DOMINICAL, A DISTANCIA, VIRTUAL A DISTANCIA, MIXTO, IRREGULAR, INTERCALADO).
- **Tratamiento aplicado:** las 13 categorías originales se consolidaron en las 4 finales, afectando 8,777 registros. El mapeo completo, con la justificación de cada agrupación, está documentado en src/config.py (MAPA_PLAN) y en docs/plan_de_limpieza.md.

## direccion_departamental

- **Descripción:** dirección departamental del MINEDUC que administra el establecimiento; es una unidad administrativa más fina que departamento, ya que subdivide algunos departamentos (p. ej. Guatemala en norte, sur, oriente y occidente).
- **Tipo de dato:** texto (categórica nominal).
- **Dominio permitido:** 26 valores (23 departamentos más subdivisiones administrativas).
- **Valores posibles:** ejemplos: GUATEMALA NORTE, PETEN, QUICHE.
- **Tratamiento aplicado:** se quitaron las tildes (p. ej. PETÉN → PETEN) para alinear la acentuación con departamento, afectando 2,025 registros. Además, la variable se renombró de DEPARTAMENTAL a direccion_departamental para no confundirse con departamento.

## Reglas de limpieza aplicadas

- Se unificaron a NaN los marcadores de no-dato disfrazados: director (SIN DATO, -, ., 0, 000000, 0000000), direccion (.) y area (SIN ESPECIFICAR).
- establecimiento: los 5 registros sin nombre se completaron con un nombre genérico y trazable (SIN NOMBRE - MUNICIPIO, DEPARTAMENTO).
- supervisor: se corrigió el 0 escrito en lugar de la letra O (p. ej. ACEVED0 → ACEVEDO).
- telefono: se conservó un único número principal (solo dígitos), descartando números secundarios y separadores.
- distrito: los códigos truncados (p. ej. 01-) se convirtieron a NaN; se conservaron los dos formatos válidos.
- plan: las 13 categorías originales se consolidaron en 4 (ENTRE SEMANA, FIN DE SEMANA, A DISTANCIA, MIXTO).
- direccion_departamental: se quitaron las tildes para alinear la acentuación con departamento.
- Cambios de esquema: se eliminó nivel (constante en DIVERSIFICADO) y se renombró departamental a direccion_departamental.
- No se imputó ningún valor ni se eliminó ninguna fila (ver la política de valores faltantes más abajo).

El detalle por variable, con conteos exactos y la justificación de cada transformación, está en docs/Registro_de_Transformaciones.md.

## Política de valores faltantes (NaN)

La limpieza deja cada celda en uno de dos estados: válida o faltante (NaN). No se imputan los faltantes en esta etapa, ya que cómo tratarlos (descartar filas, imputar por media, mediana o modelo) es una decisión de análisis que se documenta y justifica más adelante en el EDA. Por la misma razón, tampoco se eliminan filas por tener valores faltantes: una fila con un solo dato ausente sigue siendo útil para los análisis que no dependan de esa columna, y borrarla impondría a todos los análisis la restricción de uno solo.

Los valores faltantes del dataset final son de dos tipos, ambos legítimos. El primero ocurre cuando **el dato nunca se capturó en el origen**, ya sea porque la celda venía vacía o traía un marcador de nulo; en ese caso el NaN es simplemente la forma honesta de decir que el dato no existe, y es lo que pasa en director, telefono, supervisor, direccion, area y en la mayor parte de distrito. El segundo ocurre cuando **había un valor pero no era confiable**, de tal forma que conservarlo sesgaría el análisis; esto aplica a los 70 códigos truncados de distrito, que no calzaban con ningún formato válido.

La variable establecimiento no tiene faltantes en el dataset final, ya que los 5 registros sin nombre se completaron con una etiqueta trazable.

## Reproducibilidad

El conjunto limpio se regenera corriendo python src/00_init.py seguido de python src/run_pipeline.py desde la raíz del repositorio, tomando como fuente los 23 archivos crudos en data/raw/.
