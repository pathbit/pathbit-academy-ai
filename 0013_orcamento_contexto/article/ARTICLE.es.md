# Presupuesto de contexto con mediciones reproducibles

[Português (Brasil)](ARTICLE.md) · [English](ARTICLE.en.md)

La [búsqueda híbrida](../../0012_busca_hibrida/README.es.md) entrega una lista ordenada. Antes de montar la solicitud, hay que decidir qué fragmentos caben y registrar las exclusiones. Este laboratorio fija el límite en bytes para medirlo con independencia del proveedor del modelo.

## Mide la carga que se va a enviar

El empaquetador conserva el ID, la fuente y el texto. Serializa el sobre `{"documents":[...]}` como JSON compacto en UTF-8. El valor `bytes_used` incluye el sobre, las claves, las comas, los escapes y caracteres multibyte como `ç`. Mide el campo `context` después de decodificar el informe externo. El informe tiene campos adicionales y un tamaño distinto.

En una aplicación con límite de tokens, cuenta toda la entrada con el tokenizador del modelo. Incluye instrucciones, mensajes, herramientas y una reserva para la respuesta. Este ejercicio cuenta los bytes que usa el transporte de JSON.

## Selecciona en orden y registra la decisión

1. Ordena por pertinencia decreciente, con desempate por ID.
2. Aplica la cuota por fuente antes de intentar incluir el fragmento.
3. Acepta el fragmento si cabe el JSON completo.
4. Sigue recorriendo la lista tras una exclusión. Un candidato más corto puede caber en el espacio restante.

La entrada predeterminada tiene cuatro fragmentos. Con 245 bytes y una entrada por fuente, se incluyen `refund-summary` y `refund-window`, con un total de 214 bytes. El historial supera la cuota de la fuente y el apéndice supera el presupuesto. Cada exclusión devuelve un motivo distinto.

## Límites y ejercicio

Esta estrategia elige de forma voraz por puntuación. Un fragmento largo y bien posicionado puede ocupar el espacio de dos más cortos. Volver a codificar el JSON completo en cada intento también tiene un coste con entradas grandes. Mide la cobertura de evidencias por unidad de presupuesto antes de cambiar el algoritmo.

En el [inicio rápido](../README.es.md), reduce el límite a 120 bytes y comprueba que desaparece el fragmento de facturación. Aumenta la cuota a dos entradas y compara las exclusiones. El [siguiente laboratorio](../../0014_citacoes_verificaveis/README.es.md) verifica las citas de una respuesta frente al contexto exportado.
