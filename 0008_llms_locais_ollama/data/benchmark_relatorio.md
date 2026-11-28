# Relatorio do laboratorio local de LLMs

- Servidor: Ollama `0.35.1` em `http://localhost:11434`
- Modelos no container: llama3.2:1b, qwen2.5:1.5b, nomic-embed-text:latest, qwen2.5:0.5b
- Execucao: 36 chamadas de chat, sem chave de API, sem custo por token

## Chat: latencia e vazao por modelo

| modelo | ttft_medio_ms | total_medio_ms | tokens_por_segundo | tokens_gerados_medios | chamadas |
| --- | --- | --- | --- | --- | --- |
| qwen2.5:0.5b | 62.4 | 592.7 | 187.8 | 73.7 | 12 |
| qwen2.5:1.5b | 81.3 | 320.0 | 106.1 | 21.2 | 12 |
| llama3.2:1b | 47.5 | 436.1 | 89.0 | 33.3 | 12 |

## Saída estruturada • objeto com campos exigidos e ferramenta correta

| modelo | tentativas | json_valido | json_valido_pct | tool_correta | tool_correta_pct |
| --- | --- | --- | --- | --- | --- |
| qwen2.5:0.5b | 5 | 5 | 100.0 | 5 | 100.0 |
| qwen2.5:1.5b | 5 | 5 | 100.0 | 5 | 100.0 |
| llama3.2:1b | 5 | 0 | 0.0 | 0 | 0.0 |

## Embeddings locais (nomic-embed-text)

| modelo_embedding | dimensao | documentos | latencia_batch_docs_ms | latencia_batch_queries_ms | taxa_acerto_top1 |
| --- | --- | --- | --- | --- | --- |
| nomic-embed-text | 768 | 8 | 1278.4 | 43.7 | 1.0 |

## Leitura dos resultados

- O runner da época media o tempo até o primeiro texto e usava o total quando não havia texto visível.
- A vazão usa contagem e duração da geração. A latência total inclui outras etapas.
- `json_valido` registra objetos lidos com as chaves `tool` e `reason`. A ferramenta escolhida é avaliada em outra coluna.
- A taxa top-1 representa quatro consultas de demonstração sobre oito documentos.
