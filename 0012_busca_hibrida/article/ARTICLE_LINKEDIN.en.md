# Hybrid retrieval for RAG

[Português (Brasil)](ARTICLE_LINKEDIN.md) · [Español](ARTICLE_LINKEDIN.es.md)

A query can carry an exact identifier and a concept expressed differently in the index. RRF adds contributions from positions in lexical and vector rankings. That makes the rankings comparable without calibrating the two scoring scales.

In the lab, fusion improves lexical coverage for the password query. On the RE42 query, first place stays relevant, but coverage falls from 1.0 to 0.5 compared with vector retrieval. Evaluate both the first answer and the other results you show.

Compare lexical retrieval, cosine similarity, and Reciprocal Rank Fusion using labeled queries. [Instructions and runnable examples](https://github.com/pathbit/pathbit-academy-ai/tree/master/0012_busca_hibrida/README.en.md).
