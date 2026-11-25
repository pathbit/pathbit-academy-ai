# Búsqueda híbrida en RAG con Reciprocal Rank Fusion

[Português (Brasil)](ARTICLE.md) · [English](ARTICLE.en.md)

Una consulta de soporte puede contener un código exacto, como `RE42`, o describir la misma política con otras palabras. En el [laboratorio de RAG y bases vectoriales](../../0003_rag_vector_database/README.md), la recuperación es una etapa separada de la generación. Aquí evaluamos esa recuperación.

## Dos listas de candidatos

La búsqueda léxica cuenta los términos comunes después de eliminar duplicados y unificar mayúsculas y minúsculas. El código literal aporta al conteo. La búsqueda vectorial ordena por similitud del coseno. Los vectores pequeños del [conjunto de datos](../data/search.json) se eligieron para poder inspeccionar el orden. En una aplicación, genera los vectores de consulta y documento con el mismo modelo de embeddings y evalúa con datos reales.

El código descarta puntuaciones iguales o inferiores a cero, resuelve empates por ID y conserva tres candidatos por lista. La fusión solo puede devolver candidatos presentes en alguna de las listas.

## Combina posiciones con RRF

Para un documento en la posición `r`, empezando en 1, suma `1 / (60 + r)` a su total. Un documento presente en ambas listas recibe dos aportaciones. Un candidato en primer lugar en una lista y en segundo en la otra recibe `1/61 + 1/62`. La suma depende solo de las posiciones. [Artículo original sobre RRF](https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf).

## Mide los resultados

El conjunto de datos define dos documentos pertinentes por consulta. `recall_at_k` mide la fracción de documentos pertinentes recuperados. `reciprocal_rank_at_k` es el inverso de la posición del primer documento pertinente y vale cero cuando el corte deja la lista sin aciertos.

| Consulta | Recall@2 léxico | Recall@2 vectorial | Recall@2 híbrido |
| --- | --- | --- | --- |
| restablecer contraseña | 0,5 | 1,0 | 1,0 |
| protocolo RE42 para cancelar una reserva | 0,5 | 1,0 | 0,5 |

En el segundo caso, la notificación del pedido sube porque aparece en ambas listas y desplaza al documento meteorológico. El primer lugar sigue siendo pertinente. Una comprobación centrada en el primer lugar pasa por alto la regresión.

## Ejercicio

Sigue el [inicio rápido](../README.es.md) y repite con `--top 3`. Observa la diferencia en la segunda consulta.

En la carpeta del laboratorio, guarda una copia de `data/search.json` como `search-depth-2.json` y cambia `candidate_depth` a 2 en esa copia. Ejecuta el laboratorio con el archivo alternativo.

```bash
python3 src/main.py --dataset search-depth-2.json --top 2
```

Las dos primeras posiciones de la lista fusionada se mantienen para ambas consultas de este conjunto. Compáralas con `--top 3` en el archivo original para identificar qué quedó fuera del corte.

El [siguiente laboratorio](../../0013_orcamento_contexto/README.es.md) muestra cómo empaquetar una lista ordenada dentro de un límite de tamaño.
