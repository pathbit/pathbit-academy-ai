# Aprobación humana e idempotencia para agentes de soporte

[Português (Brasil)](README.md) · [English](README.en.md) · [Español](README.es.md)

Un asistente propone un ticket por fallos en el pago. El responsable lo aprueba. La llamada para abrir el ticket agota el tiempo de espera. El reintento debe recuperar el ticket asociado a la solicitud para que el equipo investigue un único incidente.

## Ejecuta el laboratorio

Usa Python 3.10+ y una terminal compatible con Bash. Ejecuta desde esta carpeta. El primer intento antes de la aprobación debe fallar. Continúa con `decidir` y compara los IDs de las dos últimas llamadas.

```bash
base="$(mktemp -d)/agent.sqlite"
python3 src/main.py --base "$base" propor pedido-42 --titulo 'Checkout' --prioridade alta
python3 src/main.py --base "$base" executar pedido-42
python3 src/main.py --base "$base" decidir pedido-42 aprovar --operador plantao
python3 src/main.py --base "$base" executar pedido-42
python3 src/main.py --base "$base" executar pedido-42
```

- [Guía completa](article/ARTICLE.es.md)
- [Cuaderno (PT-BR)](notebooks/aprovacao_idempotencia.ipynb)
- [Artículo para LinkedIn](article/ARTICLE_LINKEDIN.es.md)
- [Publicación para LinkedIn](article/POST_LINKEDIN.es.md)

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
