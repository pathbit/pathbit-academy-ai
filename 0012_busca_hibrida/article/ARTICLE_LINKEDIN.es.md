# Búsqueda híbrida para RAG

[Português (Brasil)](ARTICLE_LINKEDIN.md) · [English](ARTICLE_LINKEDIN.en.md)

Una consulta puede contener un identificador exacto y un concepto expresado de otro modo en el índice. RRF suma aportaciones según las posiciones de las listas léxica y vectorial. Así combina las listas sin calibrar sus escalas de puntuación.

En el laboratorio, la fusión mejora la cobertura léxica en la consulta sobre contraseña. Para RE42, el primer lugar sigue siendo pertinente, pero la cobertura baja de 1,0 a 0,5 frente a la búsqueda vectorial. Evalúa tanto el primer acierto como el resto de los resultados.

Compara búsqueda léxica, similitud del coseno y Reciprocal Rank Fusion con consultas etiquetadas. [Instrucciones y ejemplos ejecutables](https://github.com/pathbit/pathbit-academy-ai/tree/master/0012_busca_hibrida/README.es.md).
