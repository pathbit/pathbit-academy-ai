# 0014 — Verifiable RAG citations

[Português (Brasil)](README.md) · [Español](README.es.md)

Check source IDs and exact quotes against the supplied context and abstain when a citation fails.

## Required prerequisites

The CLI uses Python 3.10+ and its standard library. The lab runs offline without credentials or model downloads. [Download Python](https://www.python.org/downloads/).

## Quick start

Run these commands from this lab's directory. On Windows, use `py -3` in place of `python3`.

```bash
python3 src/main.py --case valid
python3 src/main.py --case altered-quote
python3 src/main.py --case unknown-source
python3 src/main.py --case unsupported-claim
```

The four cases cover a verified citation, an altered quote, a missing source, and a claim without semantic support. The last passes the literal check. The article explains how the two checks differ.

## Use the context from lab 0013

```bash
python3 ../0013_orcamento_contexto/src/main.py --bytes 245 --output context-report.json
python3 src/main.py --context-report context-report.json
python3 ../0013_orcamento_contexto/src/main.py --bytes 16 --output context-report.json
python3 src/main.py --context-report context-report.json
```

The first verification returns `citations_verified`. With the empty envelope, the second returns `abstained` with `unknown_source`. You can remove `context-report.json` after the exercise.

## Notebook

The notebook uses the same data and CLI. To open it with JupyterLab, create a virtual environment and use that environment's Python.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m jupyter lab notebooks/citacoes_verificaveis.en.ipynb
```

On Windows, use `.venv\Scripts\python.exe` in place of `.venv/bin/python`.

- [Notebook](notebooks/citacoes_verificaveis.en.ipynb)
- [Full article](article/ARTICLE.en.md)
- [LinkedIn article](article/ARTICLE_LINKEDIN.en.md)
- [LinkedIn post](article/POST_LINKEDIN.en.md)

---

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
