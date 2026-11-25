# 0012 — Hybrid retrieval for RAG

[Português (Brasil)](README.md) · [Español](README.es.md)

Compare lexical retrieval, cosine similarity, and Reciprocal Rank Fusion using labeled queries.

## Required prerequisites

The CLI uses Python 3.10+ and its standard library. The lab runs offline without credentials or model downloads. [Download Python](https://www.python.org/downloads/).

## Quick start

Run these commands from this lab's directory. On Windows, use `py -3` in place of `python3`.

```bash
python3 src/main.py --top 2
python3 src/main.py --top 3
```

At `--top 2`, fusion retrieves both relevant documents for `redefinir senha`. For `protocolo RE42`, fusion retrieves one and vector retrieval finds both. Use `--top 3` to inspect the cutoff effect.

## Notebook

The notebook uses the same data and CLI. To open it with JupyterLab, create a virtual environment and use that environment's Python.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m jupyter lab notebooks/busca_hibrida.en.ipynb
```

On Windows, use `.venv\Scripts\python.exe` in place of `.venv/bin/python`.

- [Notebook](notebooks/busca_hibrida.en.ipynb)
- [Full article](article/ARTICLE.en.md)
- [LinkedIn article](article/ARTICLE_LINKEDIN.en.md)
- [LinkedIn post](article/POST_LINKEDIN.en.md)

---

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
