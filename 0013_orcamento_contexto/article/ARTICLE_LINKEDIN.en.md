# Context budgeting for RAG

[Português (Brasil)](ARTICLE_LINKEDIN.md) · [Español](ARTICLE_LINKEDIN.es.md)

After retrieval, the space available has to fit the whole JSON document. IDs, sources, text, quotes, and UTF-8 characters all contribute to the measured size.

The lab reserves 245 bytes and fits two passages into 214 bytes. A third is excluded by the source quota and a fourth by size. The report records both reasons. Use your application's tokenizer to measure a token budget.

Select passages by relevance, cap each source, and check the size of the JSON that will be sent. [Instructions and runnable examples](https://github.com/pathbit/pathbit-academy-ai/tree/master/0013_orcamento_contexto/README.en.md).
