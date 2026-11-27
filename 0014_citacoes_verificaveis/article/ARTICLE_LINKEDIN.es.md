# Verifica las citas con el contexto que recibió el modelo RAG

Un asistente indica que se puede solicitar un reembolso en el panel del pedido y atribuye la recomendación a `refund-summary`. Una fuente que existe en el índice puede haber quedado fuera del contexto. Una cita real también puede usarse para apoyar una parte diferente de la afirmación.

## Modela la decisión

`altered-quote` devuelve `quote_not_found`. `unknown-source` devuelve `unknown_source`. `unsupported-claim` puede devolver `citations_verified` aunque afirme que el reembolso tarda cinco minutos. El fragmento solo dice dónde solicitarlo. Comprueba el respaldo semántico en otra etapa y diseña un estado de abstención para la interfaz.

## Ejecuta el laboratorio

Ejecuta los casos sobre la misma fuente y compara `status` y `errors`. Exporta después dos informes del laboratorio anterior con `245` y `16` bytes. El primero puede contener `refund-summary`. El segundo solo conserva el objeto vacío. Pasa ambos por `--context-report` para observar el efecto del límite.

[Guía completa](https://github.com/pathbit/pathbit-academy-ai/tree/master/0014_citacoes_verificaveis/article/ARTICLE.es.md)

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
