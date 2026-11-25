# Verifiable citations in RAG answers

[Português (Brasil)](ARTICLE.md) · [Español](ARTICLE.es.md)

A support assistant can cite the correct policy with altered wording or reference a source omitted from the context. The verifier receives the actual input envelope and a set of claims with citations. It reports which evidence can be verified against that input.

## Check the source and excerpt

Each claim needs at least one citation containing `source_id` and `quote`. The identifier must match a passage's `id`, and the quote must occur literally in the passage. Duplicate IDs make the source ambiguous and are rejected.

When any citation fails, the output uses `abstained`, returns an empty list of claims, and preserves diagnostic reasons. The interface can show an abstention response, and the team can distinguish a source error from an excerpt error.

| Case | Result |
| --- | --- |
| Identifier and excerpt match the context | `citations_verified` |
| A word in the citation was changed | `quote_not_found` |
| The ID exists only in the index, outside the context | `unknown_source` |
| The claim has no citations | `missing_citation` |

## Separate provenance from semantic support

The `unsupported-claim` case attaches a real excerpt about where to request a refund to a five-minute promise. Literal verification passes. The passage describes where to ask, while the time limit requires separate evidence. Expose that boundary in the API contract and evaluate semantic support separately through human review or a dedicated RAG evaluation stage.

## End-to-end exercise

Follow the [quick start](../README.en.md) and pass the [context packer](../../0013_orcamento_contexto/README.en.md) report to the verifier. At the default size, the `refund-summary` passage fits and the citation passes. At 16 bytes, only the empty envelope fits, and the same ID produces `unknown_source`.

The lab uses canned answers to exercise the output contract. In a product, validate the model response format first and treat abstention as a normal result the interface can display.
