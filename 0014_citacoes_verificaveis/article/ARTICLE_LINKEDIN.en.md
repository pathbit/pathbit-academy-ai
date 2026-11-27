# Verify citations against the context supplied to a RAG model

A shopping assistant says to request a refund from the order panel. It attributes the advice to `refund-summary`. A source in the full index may have been excluded from the generation context, and a citation can quote a real sentence about the wrong part of the claim.

## Model the decision

`altered-quote` produces `quote_not_found`. `unknown-source` produces `unknown_source`. `unsupported-claim` can return `citations_verified` while claiming that a refund takes five minutes. The quote only says where to request it. Use a separate evidence review for semantic support and design an abstention state in the UI.

## Run the lab

Run the cases on the same source and compare `status` and `errors`. Then export two context reports from the preceding lab using `245` and `16` bytes. The first can contain `refund-summary`, and the second holds only the empty envelope. Pass each report through `--context-report` to see how the context cutoff changes the verifier's result.

[Full guide](https://github.com/pathbit/pathbit-academy-ai/tree/master/0014_citacoes_verificaveis/article/ARTICLE.en.md)

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
