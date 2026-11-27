# Human approval and idempotency for support agents

An assistant proposes a ticket about checkout failures. The on-call engineer approves it. The caller times out while opening the ticket. A second call should recover the ticket already associated with the request, so the team has one incident to investigate.

## Model the decision

The executor reads the approval and inserts the ticket in the same SQLite transaction. A `UNIQUE` constraint on `chamados.pedido` and `ON CONFLICT ... DO NOTHING` keep retries tied to one ticket. The executor reads the existing ID and returns it. The local `--operador` label is a teaching input. In an authenticated service, use the identity and permissions from the session.

## Run the lab

Run the lab with a new database. Propose a ticket, attempt to execute it before approval, approve, then execute twice. The early attempt exits with `1`. Both approved attempts return the same `chamado`. Try a rejection with another key. An external ticket API needs its own delivery and deduplication contract.

[Full guide](https://github.com/pathbit/pathbit-academy-ai/tree/master/0011_aprovacao_idempotencia/article/ARTICLE.en.md)

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
