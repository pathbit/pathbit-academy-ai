# Combine keyword search and embeddings in a RAG pipeline

[Português (Brasil)](ARTICLE.md) · [English](ARTICLE.en.md) · [Español](ARTICLE.es.md)

A support query may contain an exact policy code such as `RE42`, or refer to password recovery without the wording used in a document. These are two different reasons to retrieve a source.

## Model the decision

The lexical ranker counts distinct terms in common. The vector ranker uses cosine similarity on small, hand-chosen vectors. Give each ranker at most three positive candidates for the lab. A real implementation should use one embedding model for the corpus and the queries and evaluate on a larger labeled set.

## Read the result

Reciprocal Rank Fusion sums `1/(60 + rank)` for each appearance. A hit ranked first and second scores `1/61 + 1/62`. Combining ranks avoids treating lexical scores and cosine scores as values on the same scale.

## Run the lab

At `--top 2`, password reset achieves hybrid recall `1.0`. The `RE42` query falls from vector recall `1.0` to hybrid recall `0.5`. `notification` appears in both rankings and displaces `weather-alert`. The first relevant result remains first, so reciprocal rank does not reveal the loss. Compare `--top 3`, then adjust `candidate_depth` in a copy of the dataset to see the difference between candidate depth and the final cutoff.

```bash
python3 src/main.py --top 2
python3 src/main.py --top 3
```

[Full guide](../README.en.md) · [Notebook](../notebooks/busca_hibrida.en.ipynb)

[Reciprocal Rank Fusion](https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf)

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
