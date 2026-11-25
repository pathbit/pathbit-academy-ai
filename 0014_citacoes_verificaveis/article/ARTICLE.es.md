# Citas verificables en respuestas de RAG

[Português (Brasil)](ARTICLE.md) · [English](ARTICLE.en.md)

Un asistente de soporte puede citar la política correcta con texto modificado o remitir a una fuente que quedó fuera del contexto. El verificador recibe el sobre que se envió y un conjunto de afirmaciones con citas. Informa qué evidencias se pueden verificar frente a esa entrada.

## Comprueba la fuente y el fragmento

Cada afirmación necesita al menos una cita con `source_id` y `quote`. El identificador debe corresponder al `id` de un fragmento y el texto citado debe aparecer literalmente. Los IDs duplicados vuelven ambiguo el origen y se rechazan.

Si falla alguna cita, la salida usa `abstained`, deja vacía la lista de afirmaciones y conserva los motivos. La interfaz puede mostrar una respuesta de abstención y el equipo puede distinguir un error de fuente de uno de fragmento.

| Caso | Resultado |
| --- | --- |
| Identificador y fragmento coinciden con el contexto | `citations_verified` |
| Se cambió una palabra de la cita | `quote_not_found` |
| El ID existe solo en el índice y quedó fuera del contexto | `unknown_source` |
| La afirmación carece de citas | `missing_citation` |

## Separa la procedencia del respaldo semántico

El caso `unsupported-claim` vincula un fragmento real sobre dónde solicitar un reembolso con una promesa de cinco minutos. La verificación literal pasa. El texto describe dónde solicitarlo, mientras el plazo requiere otra evidencia. Expón ese límite en el contrato de la API y mide por separado el respaldo semántico con revisión humana o una etapa de evaluación de RAG.

## Ejercicio de extremo a extremo

Sigue el [inicio rápido](../README.es.md) y pasa al verificador el informe del [empaquetador de contexto](../../0013_orcamento_contexto/README.es.md). Con el tamaño predeterminado, cabe el fragmento `refund-summary` y la cita pasa. Con 16 bytes solo cabe el sobre vacío y el mismo ID da `unknown_source`.

El laboratorio usa respuestas preparadas para comprobar el contrato de salida. En un producto, valida primero el formato de la respuesta del modelo y trata la abstención como un resultado normal que la interfaz pueda presentar.
