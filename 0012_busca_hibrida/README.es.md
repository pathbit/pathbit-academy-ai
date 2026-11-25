# 0012 — Búsqueda híbrida para RAG

[Português (Brasil)](README.md) · [English](README.en.md)

Compara búsqueda léxica, similitud del coseno y Reciprocal Rank Fusion con consultas etiquetadas.

## Requisitos obligatorios

La CLI usa Python 3.10+ y la biblioteca estándar. El laboratorio funciona sin conexión, credenciales ni descargas de modelos. [Descargar Python](https://www.python.org/downloads/).

## Inicio rápido

Ejecuta estos comandos en la carpeta del laboratorio. En Windows, usa `py -3` en lugar de `python3`.

```bash
python3 src/main.py --top 2
python3 src/main.py --top 3
```

Con `--top 2`, la fusión recupera ambos documentos pertinentes para `redefinir senha`. Para `protocolo RE42`, la fusión encuentra uno y la búsqueda vectorial encuentra ambos. Usa `--top 3` para examinar el efecto del corte.

## Cuaderno

El cuaderno usa los mismos datos y la misma CLI. Para abrirlo con JupyterLab, crea un entorno virtual y usa el Python de ese entorno.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m jupyter lab notebooks/busca_hibrida.es.ipynb
```

En Windows, usa `.venv\Scripts\python.exe` en lugar de `.venv/bin/python`.

- [Cuaderno](notebooks/busca_hibrida.es.ipynb)
- [Artículo completo](article/ARTICLE.es.md)
- [Artículo para LinkedIn](article/ARTICLE_LINKEDIN.es.md)
- [Publicación para LinkedIn](article/POST_LINKEDIN.es.md)

---

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
