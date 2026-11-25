# 0014 — Citas verificables en RAG

[Português (Brasil)](README.md) · [English](README.en.md)

Comprueba los IDs y las citas literales frente al contexto entregado y devuelve una abstención si falla alguna cita.

## Requisitos obligatorios

La CLI usa Python 3.10+ y la biblioteca estándar. El laboratorio funciona sin conexión, credenciales ni descargas de modelos. [Descargar Python](https://www.python.org/downloads/).

## Inicio rápido

Ejecuta estos comandos en la carpeta del laboratorio. En Windows, usa `py -3` en lugar de `python3`.

```bash
python3 src/main.py --case valid
python3 src/main.py --case altered-quote
python3 src/main.py --case unknown-source
python3 src/main.py --case unsupported-claim
```

Los cuatro casos cubren una cita verificada, un fragmento modificado, una fuente ausente y una afirmación sin respaldo semántico. El último pasa la comprobación literal. El artículo explica cómo difieren ambas verificaciones.

## Usa el contexto del laboratorio 0013

```bash
python3 ../0013_orcamento_contexto/src/main.py --bytes 245 --output context-report.json
python3 src/main.py --context-report context-report.json
python3 ../0013_orcamento_contexto/src/main.py --bytes 16 --output context-report.json
python3 src/main.py --context-report context-report.json
```

La primera verificación devuelve `citations_verified`. Con el sobre vacío, la segunda devuelve `abstained` con `unknown_source`. Puedes eliminar `context-report.json` después del ejercicio.

## Cuaderno

El cuaderno usa los mismos datos y la misma CLI. Para abrirlo con JupyterLab, crea un entorno virtual y usa el Python de ese entorno.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m jupyter lab notebooks/citacoes_verificaveis.es.ipynb
```

En Windows, usa `.venv\Scripts\python.exe` en lugar de `.venv/bin/python`.

- [Cuaderno](notebooks/citacoes_verificaveis.es.ipynb)
- [Artículo completo](article/ARTICLE.es.md)
- [Artículo para LinkedIn](article/ARTICLE_LINKEDIN.es.md)
- [Publicación para LinkedIn](article/POST_LINKEDIN.es.md)

---

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
