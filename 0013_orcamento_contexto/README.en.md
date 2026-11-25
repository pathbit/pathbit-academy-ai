# 0013 — Context budgeting for RAG

[Português (Brasil)](README.md) · [Español](README.es.md)

Select passages by relevance, cap each source, and check the size of the JSON that will be sent.

## Required prerequisites

The CLI uses Python 3.10+ and its standard library. The lab runs offline without credentials or model downloads. [Download Python](https://www.python.org/downloads/).

## Quick start

Run these commands from this lab's directory. On Windows, use `py -3` in place of `python3`.

```bash
python3 src/main.py --bytes 245 --per-source 1
python3 src/main.py --bytes 120 --per-source 1
python3 src/main.py --bytes 245 --per-source 2
```

With 245 bytes and a quota of one per source, `context` takes 214 bytes and contains `refund-summary` and `refund-window`. With 120 bytes, only `refund-summary` fits. With 245 bytes and a quota of two, `refund-summary` and `refund-history` fit in 211 bytes. Check `skipped` to distinguish the source quota from the byte limit.

## Notebook

The notebook uses the same data and CLI. To open it with JupyterLab, create a virtual environment and use that environment's Python.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m jupyter lab notebooks/orcamento_contexto.en.ipynb
```

On Windows, use `.venv\Scripts\python.exe` in place of `.venv/bin/python`.

- [Notebook](notebooks/orcamento_contexto.en.ipynb)
- [Full article](article/ARTICLE.en.md)
- [LinkedIn article](article/ARTICLE_LINKEDIN.en.md)
- [LinkedIn post](article/POST_LINKEDIN.en.md)

---

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
