# Human approval and idempotency for support agents

[Português (Brasil)](README.md) · [English](README.en.md) · [Español](README.es.md)

An assistant proposes a ticket about checkout failures. The on-call engineer approves it. The caller times out while opening the ticket. A second call should recover the ticket already associated with the request, so the team has one incident to investigate.

## Run the lab

Use Python 3.10+ and a shell compatible with Bash. Run the commands from this directory. The first execution should fail. Continue to `decidir` and compare the ticket IDs returned by the last two calls.

```bash
base="$(mktemp -d)/agent.sqlite"
python3 src/main.py --base "$base" propor pedido-42 --titulo 'Checkout' --prioridade alta
python3 src/main.py --base "$base" executar pedido-42
python3 src/main.py --base "$base" decidir pedido-42 aprovar --operador plantao
python3 src/main.py --base "$base" executar pedido-42
python3 src/main.py --base "$base" executar pedido-42
```

- [Full guide](article/ARTICLE.en.md)
- [Notebook (PT-BR)](notebooks/aprovacao_idempotencia.ipynb)
- [LinkedIn article](article/ARTICLE_LINKEDIN.en.md)
- [LinkedIn post](article/POST_LINKEDIN.en.md)

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
