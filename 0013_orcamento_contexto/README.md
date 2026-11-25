# 0013 — Orçamento de contexto para RAG

[English](README.en.md) · [Español](README.es.md)

Selecione trechos por relevância, limite cada fonte e confira o tamanho do JSON que será enviado.

## Pré-requisitos obrigatórios

Para a CLI, use Python 3.10+ com a biblioteca padrão. O laboratório roda offline, sem credenciais e sem baixar modelos. [Baixar Python](https://www.python.org/downloads/).

## Início rápido

Na pasta deste laboratório, execute os comandos abaixo. No Windows, substitua `python3` por `py -3`.

```bash
python3 src/main.py --bytes 245 --per-source 1
python3 src/main.py --bytes 120 --per-source 1
python3 src/main.py --bytes 245 --per-source 2
```

Com 245 bytes e cota de um por fonte, o campo `context` ocupa 214 bytes e carrega `refund-summary` e `refund-window`. Com 120 bytes, só `refund-summary` cabe. Com 245 bytes e cota de dois, entram `refund-summary` e `refund-history` em 211 bytes. Confira `skipped` para distinguir a cota de fonte do limite de bytes.

## Notebook

O notebook usa os mesmos dados e a mesma CLI. Para abrir com JupyterLab, crie um ambiente virtual e use a versão de Python desse ambiente.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m jupyter lab notebooks/orcamento_contexto.ipynb
```

No Windows, troque `.venv/bin/python` por `.venv\Scripts\python.exe`.

- [Notebook](notebooks/orcamento_contexto.ipynb)
- [Artigo completo](article/ARTICLE.md)
- [Artigo para LinkedIn](article/ARTICLE_LINKEDIN.md)
- [Post para LinkedIn](article/POST_LINKEDIN.md)

---

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
