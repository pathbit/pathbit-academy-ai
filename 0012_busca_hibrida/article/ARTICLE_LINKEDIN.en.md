# Combine keyword search and embeddings in a RAG pipeline

A support query may contain an exact policy code such as `RE42`, or refer to password recovery without the wording used in a document. These are two different reasons to retrieve a source.

## Model the decision

Reciprocal Rank Fusion sums `1/(60 + rank)` for each appearance. A hit ranked first and second scores `1/61 + 1/62`. Combining ranks avoids treating lexical scores and cosine scores as values on the same scale.

## Run the lab

At `--top 2`, password reset achieves hybrid recall `1.0`. The `RE42` query falls from vector recall `1.0` to hybrid recall `0.5`. `notification` appears in both rankings and displaces `weather-alert`. The first relevant result remains first, so reciprocal rank does not reveal the loss. Compare `--top 3`, then adjust `candidate_depth` in a copy of the dataset to see the difference between candidate depth and the final cutoff.

[Full guide](https://github.com/pathbit/pathbit-academy-ai/tree/master/0012_busca_hibrida/article/ARTICLE.en.md)

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
