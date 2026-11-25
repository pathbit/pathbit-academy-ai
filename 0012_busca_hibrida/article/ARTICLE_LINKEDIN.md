# Busca híbrida em RAG

[English](ARTICLE_LINKEDIN.en.md) · [Español](ARTICLE_LINKEDIN.es.md)

A mesma consulta pode carregar um identificador exato e um conceito que aparece no índice com outras palavras. A fusão RRF soma posições vindas de uma lista lexical e outra vetorial. Isso permite comparar a ordem sem calibrar as duas escalas de pontuação.

No laboratório, a fusão melhora a cobertura da busca lexical na consulta de senha. Na consulta do protocolo RE42, a primeira posição continua correta, mas a cobertura cai de 1,0 para 0,5 em relação à busca vetorial. A avaliação precisa medir a primeira resposta e os demais resultados exibidos.

Compare busca lexical, similaridade de cosseno e Reciprocal Rank Fusion usando consultas rotuladas. [Instruções e exemplos executáveis](https://github.com/pathbit/pathbit-academy-ai/tree/master/0012_busca_hibrida/README.md).
