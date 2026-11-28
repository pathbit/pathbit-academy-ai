# 0014 — Citações verificáveis em RAG

Valide IDs de fonte e citações literais contra o contexto entregue e devolva uma abstenção quando uma citação falhar.

## Pré-requisitos obrigatórios

Para a CLI, use Python 3.10+ com a biblioteca padrão. O laboratório roda offline, sem credenciais e sem baixar modelos. [Baixar Python](https://www.python.org/downloads/).

## Início rápido

Na pasta deste laboratório, execute os comandos abaixo. No Windows, substitua `python3` por `py -3`.

```bash
python3 src/main.py --case valid
python3 src/main.py --case altered-quote
python3 src/main.py --case unknown-source
python3 src/main.py --case unsupported-claim
```

Os quatro casos têm, em ordem, citação verificada, trecho alterado, fonte ausente e afirmação sem suporte semântico. O último passa na checagem literal. O artigo mostra a diferença entre as duas verificações.

## Use o contexto do laboratório 0013

```bash
python3 ../0013_orcamento_contexto/src/main.py --bytes 245 --output context-report.json
python3 src/main.py --context-report context-report.json
python3 ../0013_orcamento_contexto/src/main.py --bytes 16 --output context-report.json
python3 src/main.py --context-report context-report.json
```

A primeira verificação retorna `citations_verified`. Com o envelope vazio, a segunda retorna `abstained` com `unknown_source`. Você pode excluir `context-report.json` depois do exercício.

## Notebook

O notebook usa os mesmos dados e a mesma CLI. Para abrir com JupyterLab, crie um ambiente virtual e use a versão de Python desse ambiente.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m jupyter lab notebooks/citacoes_verificaveis.ipynb
```

No Windows, troque `.venv/bin/python` por `.venv\Scripts\python.exe`.

- [Notebook](notebooks/citacoes_verificaveis.ipynb)
- [Artigo completo](article/ARTICLE.md)
- [Artigo para LinkedIn](article/ARTICLE_LINKEDIN.md)
- [Post para LinkedIn](article/POST_LINKEDIN.md)
- [Destaques em PDF](highlight/highlights_0014.pdf)

---

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
