# Relatorio do laboratorio de saida estruturada

- Servidor: Ollama `0.35.1`
- Modelos: llama3.2:1b, qwen2.5:1.5b, nomic-embed-text:latest, qwen2.5:0.5b

## Resumo por nivel de contrato

| modo   |   parse_ok_pct |   schema_ok_pct |   semantico_ok_pct |   recuperado_pct |   total_medio_ms |   tokens_medios |   chamadas |
|:-------|---------------:|----------------:|-------------------:|-----------------:|-----------------:|----------------:|-----------:|
| json   |            100 |               0 |                0   |                0 |          12182.5 |            34.4 |         18 |
| livre  |              0 |               0 |                0   |                0 |          18568.9 |           224.4 |         18 |
| schema |            100 |             100 |               44.4 |              nan |           2237.6 |            22.7 |         18 |

## Resumo por modelo e nivel

| modelo       | modo   |   parse_ok_pct |   schema_ok_pct |   semantico_ok_pct |   total_medio_ms |
|:-------------|:-------|---------------:|----------------:|-------------------:|-----------------:|
| llama3.2:1b  | json   |            100 |               0 |                0   |           4605.5 |
| llama3.2:1b  | livre  |              0 |               0 |                0   |          30946.3 |
| llama3.2:1b  | schema |            100 |             100 |               33.3 |           3087.5 |
| qwen2.5:0.5b | json   |            100 |               0 |                0   |           1031   |
| qwen2.5:0.5b | livre  |              0 |               0 |                0   |          11883.9 |
| qwen2.5:0.5b | schema |            100 |             100 |               66.7 |            528.4 |
| qwen2.5:1.5b | json   |            100 |               0 |                0   |          30911.1 |
| qwen2.5:1.5b | livre  |              0 |               0 |                0   |          12876.4 |
| qwen2.5:1.5b | schema |            100 |             100 |               33.3 |           3097   |

## Leitura

- `parse_ok` aceita JSON direto ou apos limpeza de code fences (resgate basico).
- `schema_ok` exige validacao jsonschema contra o contrato da tarefa.
- `semantico_ok` exige o valor de negocio correto dentro do contrato.
- Latencia do modo `schema` inclui o custo de decodificar sob a gramatica.
