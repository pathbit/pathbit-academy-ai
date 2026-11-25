# Orçamento de contexto para RAG

[English](ARTICLE_LINKEDIN.en.md) · [Español](ARTICLE_LINKEDIN.es.md)

Depois da recuperação, o tamanho disponível tem de comportar o JSON inteiro. IDs, fonte, texto, aspas e caracteres UTF-8 contribuem para a medida.

O laboratório reserva 245 bytes e inclui dois trechos em 214 bytes. Um terceiro fica de fora pela cota da fonte e um quarto por tamanho. O relatório registra cada motivo. Para medir um limite de tokens, faça a contagem com o tokenizer da aplicação.

Selecione trechos por relevância, limite cada fonte e confira o tamanho do JSON que será enviado. [Instruções e exemplos executáveis](https://github.com/pathbit/pathbit-academy-ai/tree/master/0013_orcamento_contexto/README.md).
