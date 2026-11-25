# 0011 — Aprovação humana e idempotência em agentes

O laboratório estende o [exemplo de ferramentas MCP](../0010_mcp_local/article/ARTICLE.md). Uma automação pode propor um chamado de suporte. O operador registra a decisão, e o executor aplica apenas a proposta aprovada.

## Executar o laboratório

Use Python 3.10+ e rode os comandos a partir desta pasta. O fluxo de linha de comando usa apenas a biblioteca padrão.

```bash
base="$(mktemp -d)/agente.sqlite"
python3 src/main.py --base "$base" propor pedido-42 --titulo "Checkout indisponível" --prioridade alta
python3 src/main.py --base "$base" executar pedido-42
python3 src/main.py --base "$base" decidir pedido-42 aprovar --operador plantao
python3 src/main.py --base "$base" executar pedido-42
python3 src/main.py --base "$base" executar pedido-42
python3 src/main.py --base "$base" consultar pedido-42
```

A primeira execução devolve um erro. Depois da aprovação, ambas as chamadas retornam o mesmo número de chamado. Para verificar o percurso de recusa, registre outro pedido e use `decidir <pedido> rejeitar --operador plantao`.

Para abrir o [notebook](notebooks/aprovacao_idempotencia.ipynb), instale `requirements.txt` no ambiente virtual e execute `jupyter lab notebooks/aprovacao_idempotencia.ipynb`.

- [Artigo completo](article/ARTICLE.md)
- [Versão para LinkedIn](article/ARTICLE_LINKEDIN.md)
- [Post para LinkedIn](article/POST_LINKEDIN.md)
