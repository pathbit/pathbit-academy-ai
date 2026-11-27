# Aprobación humana e idempotencia para agentes de soporte

[Português (Brasil)](ARTICLE.md) · [English](ARTICLE.en.md) · [Español](ARTICLE.es.md)

Un asistente propone un ticket por fallos en el pago. El responsable lo aprueba. La llamada para abrir el ticket agota el tiempo de espera. El reintento debe recuperar el ticket asociado a la solicitud para que el equipo investigue un único incidente.

## Modela la decisión

Registra el título, la prioridad y la clave elegida por el cliente antes de solicitar la aprobación. El laboratorio rechaza una carga diferente con el mismo `pedido-42`. Guarda la decisión y el operador junto a la propuesta. Una propuesta pendiente o rechazada queda sin ticket.

## Interpreta el resultado

El ejecutor consulta la aprobación e inserta el ticket en la misma transacción de SQLite. La restricción `UNIQUE` de `chamados.pedido` y `ON CONFLICT ... DO NOTHING` vinculan los reintentos con un solo ticket. El ejecutor lee y devuelve el ID ya guardado. `--operador` es una etiqueta del ejercicio. En un servicio autenticado, toma la identidad y los permisos de la sesión.

## Ejecuta el laboratorio

Usa una base nueva. Registra la propuesta, intenta ejecutarla antes de aprobar, apruébala y ejecuta dos veces. El primer intento termina con código `1`. Los intentos aprobados devuelven el mismo `chamado`. Prueba un rechazo con otra clave. Una API externa necesita su propio contrato de entrega y deduplicación.

```bash
base="$(mktemp -d)/agent.sqlite"
python3 src/main.py --base "$base" propor pedido-42 --titulo 'Checkout' --prioridade alta
python3 src/main.py --base "$base" executar pedido-42
python3 src/main.py --base "$base" decidir pedido-42 aprovar --operador plantao
python3 src/main.py --base "$base" executar pedido-42
python3 src/main.py --base "$base" executar pedido-42
```

[Guía completa](../README.es.md) · [Cuaderno (PT-BR)](../notebooks/aprovacao_idempotencia.ipynb)

[SQLite](https://sqlite.org/lang_transaction.html)

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
