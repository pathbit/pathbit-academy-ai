# Relatorio do laboratorio de saida estruturada

- Servidor: Ollama `0.35.1`
- Modelos: llama3.2:1b, qwen2.5:1.5b, nomic-embed-text:latest, qwen2.5:0.5b

## Resumo por nivel de contrato

| modo   |   parse_ok_pct |   schema_ok_pct |   semantico_ok_pct |   recuperado_pct |   total_medio_ms |   tokens_medios |   chamadas |
|:-------|---------------:|----------------:|-------------------:|-----------------:|-----------------:|----------------:|-----------:|
| json   |           88.9 |               0 |                0   |                0 |           1158.3 |            39.2 |         18 |
| livre  |            0   |               0 |                0   |                0 |           3007.7 |            87.2 |         18 |
| schema |          100   |             100 |               44.4 |              nan |            400.5 |            22.7 |         18 |

## Resumo por modelo e nivel

| modelo       | modo   |   parse_ok_pct |   schema_ok_pct |   semantico_ok_pct |   total_medio_ms |
|:-------------|:-------|---------------:|----------------:|-------------------:|-----------------:|
| llama3.2:1b  | json   |           66.7 |               0 |                0   |           2192   |
| llama3.2:1b  | livre  |            0   |               0 |                0   |           4383.2 |
| llama3.2:1b  | schema |          100   |             100 |               33.3 |            466.8 |
| qwen2.5:0.5b | json   |          100   |               0 |                0   |            594   |
| qwen2.5:0.5b | livre  |            0   |               0 |                0   |           1697.3 |
| qwen2.5:0.5b | schema |          100   |             100 |               66.7 |            269.4 |
| qwen2.5:1.5b | json   |          100   |               0 |                0   |            688.8 |
| qwen2.5:1.5b | livre  |            0   |               0 |                0   |           2942.6 |
| qwen2.5:1.5b | schema |          100   |             100 |               33.3 |            465.3 |

## Roteamento por similaridade de embeddings

- Implementação avaliada: `nomic-embed-text` e similaridade de cosseno entre a consulta e três descrições de rota.
- Chamadas avaliadas: 6 (três consultas em duas repetições).
- Valor na posição central superior, publicado como p50 pelo runner: 13,61 ms.
- p95 registrado: 17,22 ms.
- Média registrada: 12,97 ms.
- Rótulos esperados: 6 de 6.
- Tokens gerados no decoder: 0.

> O tempo inclui ler o embedding da consulta e comparar com os vetores de referência já calculados. O formato do resultado vem do código. Este ensaio não é um teste de equivalência com o benchmark generativo.

## Leitura

- `parse_ok` aceita JSON direto ou apos limpeza de code fences (resgate basico).
- `schema_ok` exige validacao jsonschema contra o contrato da tarefa.
- `semantico_ok` exige o valor de negocio correto dentro do contrato.
- A latência por caso soma as tentativas executadas. As médias não isolam o custo de decodificar sob a gramática.
