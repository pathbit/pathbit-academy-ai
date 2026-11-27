# Human approval and idempotency for support agents

[Português (Brasil)](ARTICLE.md) · [English](ARTICLE.en.md) · [Español](ARTICLE.es.md)

An assistant proposes a ticket about checkout failures. The on-call engineer approves it. The caller times out while opening the ticket. A second call should recover the ticket already associated with the request, so the team has one incident to investigate.

## Model the decision

Record the title, priority, and client-selected key before asking a human to approve. The lab rejects a different payload under the same `pedido-42`. Store the decision and operator with the proposal. An unapproved or rejected request stays without a ticket.

## Read the result

The executor reads the approval and inserts the ticket in the same SQLite transaction. A `UNIQUE` constraint on `chamados.pedido` and `ON CONFLICT ... DO NOTHING` keep retries tied to one ticket. The executor reads the existing ID and returns it. The local `--operador` label is a teaching input. In an authenticated service, use the identity and permissions from the session.

## Run the lab

Run the lab with a new database. Propose a ticket, attempt to execute it before approval, approve, then execute twice. The early attempt exits with `1`. Both approved attempts return the same `chamado`. Try a rejection with another key. An external ticket API needs its own delivery and deduplication contract.

```bash
base="$(mktemp -d)/agent.sqlite"
python3 src/main.py --base "$base" propor pedido-42 --titulo 'Checkout' --prioridade alta
python3 src/main.py --base "$base" executar pedido-42
python3 src/main.py --base "$base" decidir pedido-42 aprovar --operador plantao
python3 src/main.py --base "$base" executar pedido-42
python3 src/main.py --base "$base" executar pedido-42
```

[Full guide](../README.en.md) · [Notebook (PT-BR)](../notebooks/aprovacao_idempotencia.ipynb)

[SQLite](https://sqlite.org/lang_transaction.html)

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
