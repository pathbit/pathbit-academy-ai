# Quando juntar duas buscas piora o resultado do RAG

No laboratório, uma busca conta termos em comum e outra ordena por similaridade vetorial. A fusão RRF usa a posição de cada resultado. A consulta `RE42` mostra um caso em que uma fonte secundária sobe porque aparece nos dois rankings.

## O que cada busca consegue enxergar

O laboratório lexical conta termos únicos que ocorrem na consulta e no documento com caixa normalizada. É uma maneira de inspecionar a lógica em poucas linhas. Em uma aplicação real, um índice com BM25 ou técnica equivalente pode tratar melhor a frequência e a raridade dos termos. A busca vetorial usa similaridade de cosseno com vetores pequenos escritos no [conjunto de dados](https://github.com/pathbit/pathbit-academy-ai/blob/master/0012_busca_hibrida/data/search.json). Eles representam ordens controladas para o exercício. Ao usar embeddings reais, gere vetores para consultas e documentos com o mesmo modelo.

Pontuações menores ou iguais a zero ficam de fora. Cada método ordena seus candidatos e entrega até três IDs. A fusão recebe esses candidatos, então aumentar apenas o corte final não recupera o que nunca entrou em nenhuma lista.

## Una as posições com Reciprocal Rank Fusion

Para um documento na posição `r`, conte `1 / (60 + r)` a partir de `r = 1`. Some as contribuições das listas em que o documento aparece. Uma entrada nas posições 1 e 2 soma `1/61 + 1/62`, cerca de `0,03252`. Uma entrada que aparece apenas em primeiro soma cerca de `0,01639`. O método usa posições para combinar rankings com escalas diferentes. [Artigo original sobre RRF](https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf).

## Faça o experimento no seu terminal

Com dois resultados, o recall híbrido cai de `1,0` para `0,5` em relação à busca vetorial. A primeira resposta relevante continua no lugar. Rode com `--top 2` e `--top 3` e compare quais IDs ficaram de fora.

[Artigo completo e notebook no GitHub](https://github.com/pathbit/pathbit-academy-ai/tree/master/0012_busca_hibrida)

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
