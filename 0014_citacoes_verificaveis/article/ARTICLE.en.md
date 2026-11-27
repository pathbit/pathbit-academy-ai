# Verify citations against the context supplied to a RAG model

[Português (Brasil)](ARTICLE.md) · [English](ARTICLE.en.md) · [Español](ARTICLE.es.md)

A shopping assistant says to request a refund from the order panel. It attributes the advice to `refund-summary`. A source in the full index may have been excluded from the generation context, and a citation can quote a real sentence about the wrong part of the claim.

## Model the decision

Validate each `source_id` against the chunk IDs in the exact context sent to generation. Check `quote` as a literal substring. Reject duplicate context identifiers. Return `abstained` with an empty claims list and diagnostic codes when any citation fails.

## Read the result

`altered-quote` produces `quote_not_found`. `unknown-source` produces `unknown_source`. `unsupported-claim` can return `citations_verified` while claiming that a refund takes five minutes. The quote only says where to request it. Use a separate evidence review for semantic support and design an abstention state in the UI.

## Run the lab

Run the cases on the same source and compare `status` and `errors`. Then export two context reports from the preceding lab using `245` and `16` bytes. The first can contain `refund-summary`, and the second holds only the empty envelope. Pass each report through `--context-report` to see how the context cutoff changes the verifier's result.

```bash
python3 src/main.py --case valid
python3 src/main.py --case altered-quote
python3 src/main.py --case unknown-source
python3 src/main.py --case unsupported-claim
```

[Full guide](../README.en.md) · [Notebook](../notebooks/citacoes_verificaveis.en.ipynb)

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
