# Combina búsqueda por palabras y embeddings en un sistema RAG

Una consulta de soporte puede incluir un código exacto como `RE42` o hablar de recuperar la contraseña con palabras distintas a las del documento. Cada caso exige una señal de recuperación diferente.

## Modela la decisión

Reciprocal Rank Fusion suma `1/(60 + rank)` por cada aparición. Un documento en primera y segunda posición suma `1/61 + 1/62`. La fusión se hace con posiciones, que se pueden combinar aunque las puntuaciones provengan de escalas distintas.

## Ejecuta el laboratorio

Con `--top 2`, la consulta de contraseña llega a recall híbrido `1.0`. En `RE42`, el recall vectorial de `1.0` cae a `0.5` al fusionar. `notification` aparece en las dos listas y desplaza `weather-alert`. El primer acierto sigue en la primera posición, por lo que el rango recíproco oculta la pérdida. Compara `--top 3` y modifica `candidate_depth` en una copia de los datos para distinguir la profundidad y el corte final.

[Guía completa](https://github.com/pathbit/pathbit-academy-ai/tree/master/0012_busca_hibrida/article/ARTICLE.es.md)

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
