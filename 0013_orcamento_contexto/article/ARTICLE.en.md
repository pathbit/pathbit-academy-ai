# Pack RAG context within a measurable budget

[Português (Brasil)](ARTICLE.md) · [English](ARTICLE.en.md) · [Español](ARTICLE.es.md)

A request asks where to request a refund and how to find its deadline. The retrieval list can rank two documents from returns above a billing note. Keeping the top hits without checking sources may leave part of the question unanswered.

## Model the decision

The lab measures the compact UTF-8 JSON envelope `{"documents":[...]}` including fields, punctuation and escaped or multibyte characters. `bytes_used` describes that envelope, not the containing report. For model input limits, count tokens for the actual model over the complete request and reserve room for output.

## Read the result

The packer sorts by score and breaks ties by ID. It checks the quota per source, then tries the document against the full serialized envelope. It records `source_limit` or `byte_budget` and keeps trying shorter candidates. This is a greedy strategy. It does not optimize total coverage.

## Run the lab

At `245` bytes and a quota of one per source, `refund-summary` and `refund-window` occupy `214` bytes. At `120` bytes, only the summary fits. Raising the source quota to two with `245` bytes keeps `refund-summary` and `refund-history` in `211` bytes. The shorter result loses the billing evidence. Compare the `context` and `skipped` fields.

```bash
python3 src/main.py --bytes 245 --per-source 1
python3 src/main.py --bytes 120 --per-source 1
python3 src/main.py --bytes 245 --per-source 2
```

[Full guide](../README.en.md) · [Notebook](../notebooks/orcamento_contexto.en.ipynb)

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
