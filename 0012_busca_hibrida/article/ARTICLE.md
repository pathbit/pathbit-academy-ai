# Busca híbrida em RAG com Reciprocal Rank Fusion

[English](ARTICLE.en.md) · [Español](ARTICLE.es.md)

Uma consulta de suporte pode conter um código exato, como `RE42`, ou descrever a mesma política com outras palavras. No [laboratório de RAG e banco vetorial](../../0003_rag_vector_database/README.md), a busca é uma etapa separada da geração. Aqui ela é o objeto da avaliação.

## Duas listas de candidatos

A busca lexical conta os termos em comum, com palavras únicas e caixa normalizada. Isso dá peso ao código literal. A busca vetorial ordena por similaridade de cosseno. Os vetores pequenos do [conjunto de dados](../data/search.json) foram escolhidos para tornar a ordem inspecionável. Em uma aplicação, gere vetores de consulta e documento com o mesmo modelo de embeddings e avalie com dados reais.

O código descarta pontuações menores ou iguais a zero, usa o ID para desempatar e limita cada lista a três candidatos. A fusão só pode devolver candidatos presentes em pelo menos uma das listas.

## Combine posições com RRF

Para um documento na posição `r`, iniciada em 1, some `1 / (60 + r)` ao seu total. Um documento que aparece nas duas listas recebe duas contribuições. Um candidato na primeira posição em uma lista e na segunda em outra recebe `1/61 + 1/62`. A soma usa apenas as posições. [Artigo original sobre RRF](https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf).

## Meça os resultados

O conjunto de dados define dois documentos pertinentes por consulta. `recall_at_k` mede a fração dos documentos pertinentes recuperados. `reciprocal_rank_at_k` mede o inverso da posição do primeiro pertinente e vale zero quando o corte fica sem acertos.

| Consulta | Recall@2 lexical | Recall@2 vetorial | Recall@2 híbrido |
| --- | --- | --- | --- |
| redefinir senha | 0,5 | 1,0 | 1,0 |
| protocolo RE42 para cancelar reserva | 0,5 | 1,0 | 0,5 |

No segundo caso, a notificação de pedido sobe por aparecer nas duas listas e desloca o documento de meteorologia. A primeira posição ainda é pertinente. Uma checagem que olha só a primeira posição perde a regressão.

## Exercício

Siga o [início rápido](../README.md) e repita com `--top 3`. Confira a diferença na segunda consulta.

Na pasta do laboratório, salve uma cópia de `data/search.json` como `search-depth-2.json` e altere `candidate_depth` para 2 nessa cópia. Execute com o arquivo alternativo.

```bash
python3 src/main.py --dataset search-depth-2.json --top 2
```

As duas primeiras posições da lista fundida permanecem iguais para as duas consultas desse conjunto. Compare com o resultado de `--top 3` no arquivo original para identificar o que ficou fora do corte.

O [laboratório seguinte](../../0013_orcamento_contexto/README.md) mostra como empacotar uma lista ordenada dentro de um limite de tamanho.
