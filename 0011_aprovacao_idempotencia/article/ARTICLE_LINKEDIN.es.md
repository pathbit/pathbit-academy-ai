# Aprobación humana e idempotencia para agentes de soporte

Un asistente propone un ticket por fallos en el pago. El responsable lo aprueba. La llamada para abrir el ticket agota el tiempo de espera. El reintento debe recuperar el ticket asociado a la solicitud para que el equipo investigue un único incidente.

## Modela la decisión

El ejecutor consulta la aprobación e inserta el ticket en la misma transacción de SQLite. La restricción `UNIQUE` de `chamados.pedido` y `ON CONFLICT ... DO NOTHING` vinculan los reintentos con un solo ticket. El ejecutor lee y devuelve el ID ya guardado. `--operador` es una etiqueta del ejercicio. En un servicio autenticado, toma la identidad y los permisos de la sesión.

## Ejecuta el laboratorio

Usa una base nueva. Registra la propuesta, intenta ejecutarla antes de aprobar, apruébala y ejecuta dos veces. El primer intento termina con código `1`. Los intentos aprobados devuelven el mismo `chamado`. Prueba un rechazo con otra clave. Una API externa necesita su propio contrato de entrega y deduplicación.

[Guía completa](https://github.com/pathbit/pathbit-academy-ai/tree/master/0011_aprovacao_idempotencia/article/ARTICLE.es.md)

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
