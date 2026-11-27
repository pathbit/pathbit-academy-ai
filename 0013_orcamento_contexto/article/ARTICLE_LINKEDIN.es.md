# Construye el contexto de un RAG dentro de un límite medible

Una consulta pregunta dónde solicitar un reembolso y cómo consultar el plazo. La búsqueda puede situar dos documentos de devoluciones antes de una nota de facturación. Si se toman los primeros resultados sin comprobar sus fuentes, parte de la pregunta puede quedar sin evidencia.

## Modela la decisión

El empaquetador ordena por puntuación y desempata por ID. Comprueba la cuota por fuente y después serializa el objeto con el fragmento candidato. Registra `source_limit` o `byte_budget` y continúa con los siguientes. La estrategia es voraz y no optimiza toda la cobertura.

## Ejecuta el laboratorio

Con `245` bytes y un fragmento por fuente, `refund-summary` y `refund-window` ocupan `214` bytes. Con `120`, solo cabe el resumen. Con una cuota de dos y `245` bytes, `refund-summary` y `refund-history` ocupan `211` bytes. El resultado más corto pierde la evidencia de facturación. Compara `context` y `skipped`.

[Guía completa](https://github.com/pathbit/pathbit-academy-ai/tree/master/0013_orcamento_contexto/article/ARTICLE.es.md)

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
