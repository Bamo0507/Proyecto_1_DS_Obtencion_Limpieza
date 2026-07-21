# Registro de transformaciones de la limpieza

En esta tabla se documenta cada modificación realizada sobre el dataset durante la limpieza, indicando la variable, el problema detectado, la transformación aplicada, la cantidad de registros afectados y la justificación. Solo se listan las variables que fueron modificadas, ya que las que no presentaron problemas se conservaron sin cambios. Los nombres de variable corresponden a los del dataset final.

| Variable | Problema detectado | Transformación | Registros afectados | Justificación |
|---|---|---|---|---|
| director | Faltantes representados de muchas formas, tanto nulos como marcadores disfrazados (SIN DATO, guiones, puntos y ceros). | Se unificaron todos esos marcadores a NaN. | 61 | Deja el faltante en un único estado honesto y medible, sin imputar. |
| direccion | 5 registros con un punto como dirección, que es un no-dato disfrazado. | El punto se convirtió a NaN. | 5 | Un punto no representa una dirección real, de tal forma que se marca como ausente. |
| area | La categoría SIN ESPECIFICAR, que en realidad es un no-dato disfrazado de categoría válida. | SIN ESPECIFICAR se convirtió a NaN. | 3 | Un establecimiento es urbano o rural, por lo que ese valor no es una categoría válida. |
| establecimiento | 5 registros sin el nombre del centro educativo. | Se construyó un nombre genérico desde la ubicación, con el formato SIN NOMBRE - MUNICIPIO, DEPARTAMENTO. | 5 | Completa el identificador legible con una etiqueta trazable, dejando explícito que el nombre no venía en el origen. |
| supervisor | Un nombre con un 0 escrito en lugar de la letra O, como en ACEVED0. | Se reemplazó el 0 pegado a letras por una O. | 3 | Corrige un error de digitación evidente sin inventar el dato, ya que el mismo supervisor aparece en 3 registros. |
| telefono | 251 valores no eran un número simple de 8 dígitos, con varios números en una celda, separadores o longitudes distintas. | Se conservó un único número principal y solamente sus dígitos. | 201 | Un solo número de contacto es suficiente y evita celdas con varios números; los que ya eran un número corto de solo dígitos no cambiaron. |
| distrito | 70 códigos truncados, como 01-, que no aportan información. | Los truncados se convirtieron a NaN, conservando los dos formatos válidos. | 70 | Separa lo irreparable de lo válido, sin adivinar el código real de esas observaciones. |
| plan | 13 categorías solapadas e inconsistentes que mezclaban el horario y la modalidad. | Se consolidaron en cuatro categorías, que son ENTRE SEMANA, FIN DE SEMANA, A DISTANCIA y MIXTO. | 8,777 | Reduce el ruido de tener categorías redundantes bajo un criterio único y explícito, en donde las que ya coincidían con su categoría destino no cambiaron. |
| direccion_departamental | Acentuación inconsistente respecto a departamento, como PETÉN frente a PETEN. | Se quitaron las tildes para alinearla con departamento. | 2,025 | Unifica el estilo de escritura sin alterar el significado ni la identidad del dato. |
| nivel | Variable constante en DIVERSIFICADO, sin ninguna variabilidad. | Se eliminó la columna. | 11,867 (toda la columna) | Una variable que toma un único valor no discrimina entre observaciones ni aporta al análisis. |
| Todas las columnas | Los nombres venían en mayúsculas y DEPARTAMENTAL se confundía con DEPARTAMENTO. | Se pasaron todos los nombres a minúsculas y DEPARTAMENTAL se renombró a direccion_departamental. | Cambio de esquema, no de registros | Deja nombres de variables descriptivos y sin ambigüedad, cumpliendo el criterio de la generación del conjunto limpio. |

## Reproducibilidad

Todo el proceso es completamente reproducible. Los datos crudos se conservan intactos en data/raw/ como fuente de verdad, mientras que el dataset limpio se regenera corriendo el pipeline por etapas, primero con python src/00_init.py para preparar el entorno y luego con python src/run_pipeline.py, que ejecuta las 10 etapas en orden y valida cada una. Cada transformación de esta tabla vive en su propia etapa numerada dentro de src/, de tal forma que se puede auditar y volver a correr de forma independiente.
