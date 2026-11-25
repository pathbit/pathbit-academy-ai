# Presupuesto de contexto para RAG

[Português (Brasil)](ARTICLE_LINKEDIN.md) · [English](ARTICLE_LINKEDIN.en.md)

Después de recuperar los documentos, el espacio disponible tiene que admitir el JSON completo. Los IDs, las fuentes, el texto, las comillas y los caracteres UTF-8 contribuyen al tamaño medido.

El laboratorio reserva 245 bytes e incluye dos fragmentos en 214 bytes. Un tercero se excluye por la cuota de fuente y un cuarto por tamaño. El informe registra ambos motivos. Usa el tokenizador de la aplicación para medir un presupuesto de tokens.

Selecciona fragmentos por pertinencia, limita cada fuente y comprueba el tamaño del JSON que se enviará. [Instrucciones y ejemplos ejecutables](https://github.com/pathbit/pathbit-academy-ai/tree/master/0013_orcamento_contexto/README.es.md).
