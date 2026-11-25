# Context budgets with reproducible measurements

[Português (Brasil)](ARTICLE.md) · [Español](ARTICLE.es.md)

[Hybrid retrieval](../../0012_busca_hibrida/README.en.md) delivers a ranked candidate list. Before building the request, decide which passages fit and record the exclusions. This lab specifies the limit in bytes for a measurement independent of any model provider.

## Measure the payload that will be sent

The packer keeps the ID, source, and text. It encodes the `{"documents":[...]}` envelope as compact UTF-8 JSON. The `bytes_used` value includes the envelope, keys, commas, escapes, and multibyte characters such as `ç`. It measures the `context` field after decoding the outer report. The report itself has extra fields and a different size.

In a token-limited application, count the entire input with the model tokenizer. Include instructions, messages, tools, and a reservation for the response. This exercise counts bytes in the JSON sent over the transport.

## Select in order and record each decision

1. Sort by decreasing relevance, breaking ties by ID.
2. Apply the source quota before trying to fit the passage.
3. Accept the passage when the entire JSON fits.
4. Keep scanning after an exclusion. A shorter candidate can fit into the remaining space.

The default input has four passages. At 245 bytes and one passage per source, the packer includes `refund-summary` and `refund-window`, for 214 bytes. The history exceeds the source quota and the appendix exceeds the budget. Each exclusion produces a distinct reason.

## Limitations and exercise

This strategy greedily selects by score. A long, highly ranked passage can take the space of two shorter passages. Re-encoding the complete JSON for each attempt also has a cost on large inputs. Measure evidence coverage per unit of budget before changing the algorithm.

In the [quick start](../README.en.md), reduce the limit to 120 bytes and watch the billing passage disappear. Raise the quota to two passages and compare the exclusions. The [next lab](../../0014_citacoes_verificaveis/README.en.md) checks answer citations against exported context.
