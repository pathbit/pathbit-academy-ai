# 0012 — Busca híbrida em RAG

[English](README.en.md) · [Español](README.es.md)

Compare busca lexical, similaridade de cosseno e Reciprocal Rank Fusion usando consultas rotuladas.

## Pré-requisitos obrigatórios

Para a CLI, use Python 3.10+ com a biblioteca padrão. O laboratório roda offline, sem credenciais e sem baixar modelos. [Baixar Python](https://www.python.org/downloads/).

## Início rápido

Na pasta deste laboratório, execute os comandos abaixo. No Windows, substitua `python3` por `py -3`.

```bash
python3 src/main.py --top 2
python3 src/main.py --top 3
```

Com `--top 2`, a fusão encontra os dois documentos pertinentes para `redefinir senha`. Para `protocolo RE42`, a fusão encontra um e a busca vetorial encontra dois. Use `--top 3` para investigar o efeito do corte.

## Notebook

O notebook usa os mesmos dados e a mesma CLI. Para abrir com JupyterLab, crie um ambiente virtual e use a versão de Python desse ambiente.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m jupyter lab notebooks/busca_hibrida.ipynb
```

No Windows, troque `.venv/bin/python` por `.venv\Scripts\python.exe`.

- [Notebook](notebooks/busca_hibrida.ipynb)
- [Artigo completo](article/ARTICLE.md)
- [Artigo para LinkedIn](article/ARTICLE_LINKEDIN.md)
- [Post para LinkedIn](article/POST_LINKEDIN.md)

---

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
