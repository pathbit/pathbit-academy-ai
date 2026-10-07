# Relatorio do laboratorio local de LLMs

- Servidor: Ollama `0.35.1` em `http://localhost:11434`
- Modelos no container: llama3.2:1b, qwen2.5:1.5b, nomic-embed-text:latest, qwen2.5:0.5b
- Execucao: 36 chamadas de chat, sem chave de API, sem custo por token

## Chat: latencia e vazao por modelo

| modelo | ttft_medio_ms | total_medio_ms | tokens_por_segundo | tokens_gerados_medios | chamadas |
| --- | --- | --- | --- | --- | --- |
| qwen2.5:0.5b | 78.1 | 649.6 | 156.2 | 73.7 | 12 |
| qwen2.5:1.5b | 95.6 | 399.2 | 86.7 | 21.2 | 12 |
| llama3.2:1b | 112.6 | 1270.0 | 32.9 | 33.3 | 12 |

## Saida estruturada: JSON valido e tool correta

| modelo | tentativas | json_valido | json_valido_pct | tool_correta | tool_correta_pct |
| --- | --- | --- | --- | --- | --- |
| qwen2.5:0.5b | 5 | 5 | 100.0 | 5 | 100.0 |
| qwen2.5:1.5b | 5 | 5 | 100.0 | 5 | 100.0 |
| llama3.2:1b | 5 | 0 | 0.0 | 0 | 0.0 |

## Embeddings locais (nomic-embed-text)

| modelo_embedding | dimensao | documentos | latencia_batch_docs_ms | latencia_batch_queries_ms | taxa_acerto_top1 |
| --- | --- | --- | --- | --- | --- |
| nomic-embed-text | 768 | 8 | 1911.6 | 39.0 | 1.0 |

## Interpretacao

- TTFT e total medem a experiencia real de quem usa o sistema local.
- Tokens/s mostra o tamanho pratico de resposta possivel dentro do SLA.
- JSON valido e tool correta mostram se o modelo sustenta um planner de agente.
- Retrieval top-1 prova que a mesma maquina resolve roteamento semantico sem nuvem.
