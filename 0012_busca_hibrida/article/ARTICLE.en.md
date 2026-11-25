# Hybrid RAG retrieval with Reciprocal Rank Fusion

[Português (Brasil)](ARTICLE.md) · [Español](ARTICLE.es.md)

A support query can contain an exact code such as `RE42` or describe the same policy in other words. The [RAG and vector database lab](../../0003_rag_vector_database/README.md) treats retrieval as a separate stage from generation. This lab evaluates retrieval itself.

## Two candidate lists

Lexical retrieval counts shared terms after removing duplicates and folding case. The literal code contributes to that count. Vector retrieval orders candidates by cosine similarity. The small vectors in the [dataset](../data/search.json) were chosen so that the ordering is easy to inspect. In an application, use the same embedding model for queries and documents and evaluate with real data.

The code discards scores of zero or less, breaks ties by ID, and retains three candidates per list. Fusion can only return candidates that occur in at least one list.

## Combine positions with RRF

For a document in position `r`, starting at 1, add `1 / (60 + r)` to its total. A document in both lists receives two contributions. A candidate ranked first in one list and second in the other receives `1/61 + 1/62`. The sum depends only on positions. [Original RRF paper](https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf).

## Measure the results

The dataset defines two relevant documents per query. `recall_at_k` measures the fraction of relevant documents retrieved. `reciprocal_rank_at_k` is the inverse position of the first relevant document and is zero when the cutoff leaves no hits.

| Query | Lexical Recall@2 | Vector Recall@2 | Hybrid Recall@2 |
| --- | --- | --- | --- |
| reset password | 0.5 | 1.0 | 1.0 |
| protocol RE42 to cancel a reservation | 0.5 | 1.0 | 0.5 |

In the second case, the order notification rises because it appears in both lists and displaces the weather document. First place remains relevant. A check that evaluates only first place misses the regression.

## Exercise

Follow the [quick start](../README.en.md) and rerun with `--top 3`. Observe the difference on the second query.

In the lab directory, save a copy of `data/search.json` as `search-depth-2.json` and set `candidate_depth` to 2 in that copy. Run the lab with the alternate file.

```bash
python3 src/main.py --dataset search-depth-2.json --top 2
```

The first two positions of the fused list stay the same for both queries in this dataset. Compare with `--top 3` on the original file to identify what the cutoff left out.

The [next lab](../../0013_orcamento_contexto/README.en.md) shows how to pack a ranked list within a size limit.
