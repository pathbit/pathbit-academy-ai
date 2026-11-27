# Verifica las citas con el contexto que recibió el modelo RAG

[Português (Brasil)](ARTICLE.md) · [English](ARTICLE.en.md) · [Español](ARTICLE.es.md)

Un asistente indica que se puede solicitar un reembolso en el panel del pedido y atribuye la recomendación a `refund-summary`. Una fuente que existe en el índice puede haber quedado fuera del contexto. Una cita real también puede usarse para apoyar una parte diferente de la afirmación.

## Modela la decisión

Valida cada `source_id` con los identificadores del contexto exacto de la generación. Comprueba que `quote` aparezca de forma literal. Rechaza identificadores duplicados. Si una cita falla, devuelve `abstained`, una lista de afirmaciones vacía y códigos para el diagnóstico.

## Interpreta el resultado

`altered-quote` devuelve `quote_not_found`. `unknown-source` devuelve `unknown_source`. `unsupported-claim` puede devolver `citations_verified` aunque afirme que el reembolso tarda cinco minutos. El fragmento solo dice dónde solicitarlo. Comprueba el respaldo semántico en otra etapa y diseña un estado de abstención para la interfaz.

## Ejecuta el laboratorio

Ejecuta los casos sobre la misma fuente y compara `status` y `errors`. Exporta después dos informes del laboratorio anterior con `245` y `16` bytes. El primero puede contener `refund-summary`. El segundo solo conserva el objeto vacío. Pasa ambos por `--context-report` para observar el efecto del límite.

```bash
python3 src/main.py --case valid
python3 src/main.py --case altered-quote
python3 src/main.py --case unknown-source
python3 src/main.py --case unsupported-claim
```

[Guía completa](../README.es.md) · [Cuaderno](../notebooks/citacoes_verificaveis.es.ipynb)

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
