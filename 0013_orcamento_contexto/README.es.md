# 0013 — Presupuesto de contexto para RAG

[Português (Brasil)](README.md) · [English](README.en.md)

Selecciona fragmentos por pertinencia, limita cada fuente y comprueba el tamaño del JSON que se enviará.

## Requisitos obligatorios

La CLI usa Python 3.10+ y la biblioteca estándar. El laboratorio funciona sin conexión, credenciales ni descargas de modelos. [Descargar Python](https://www.python.org/downloads/).

## Inicio rápido

Ejecuta estos comandos en la carpeta del laboratorio. En Windows, usa `py -3` en lugar de `python3`.

```bash
python3 src/main.py --bytes 245 --per-source 1
python3 src/main.py --bytes 120 --per-source 1
python3 src/main.py --bytes 245 --per-source 2
```

Con 245 bytes y una cuota de uno por fuente, `context` ocupa 214 bytes y contiene `refund-summary` y `refund-window`. Con 120 bytes solo cabe `refund-summary`. Con 245 bytes y una cuota de dos, `refund-summary` y `refund-history` caben en 211 bytes. Revisa `skipped` para distinguir la cuota de fuente del límite de bytes.

## Cuaderno

El cuaderno usa los mismos datos y la misma CLI. Para abrirlo con JupyterLab, crea un entorno virtual y usa el Python de ese entorno.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m jupyter lab notebooks/orcamento_contexto.es.ipynb
```

En Windows, usa `.venv\Scripts\python.exe` en lugar de `.venv/bin/python`.

- [Cuaderno](notebooks/orcamento_contexto.es.ipynb)
- [Artículo completo](article/ARTICLE.es.md)
- [Artículo para LinkedIn](article/ARTICLE_LINKEDIN.es.md)
- [Publicación para LinkedIn](article/POST_LINKEDIN.es.md)

---

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
