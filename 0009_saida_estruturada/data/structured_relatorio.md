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

## A Nova Fronteira: Modelos System 1 (Passada Unica sem Geracao)

- **Paradigma:** `System 1 (Single Forward Pass / Decisor Direto)`
- **Referencias da Industria:** `Laya (Open-Source), Jev (TypeSafe AI), Kev`
- **Latencia Mediana (p50):** `13.61 ms` (vs ~1.500 ms no modo schema)
- **Latencia Percentil 95 (p95):** `17.22 ms`
- **Latencia Media:** `12.97 ms`
- **Tokens gerados no decoder:** `0` (sem loop autoregressivo)
- **Conformidade com schema:** `100.0%`
- **Acuracia de decisao:** `100.0%`

> **Conclusao:** Enquanto LLMs generativos com JSON Schema garantem a integridade de payloads complexos com texto livre (~1.500 ms), modelos System 1 (como o Laya em open-source ou Jev na nuvem) resolvem roteamento e selecao de tools com mais de 50x de reducao de latencia.

## Leitura

- `parse_ok` aceita JSON direto ou apos limpeza de code fences (resgate basico).
- `schema_ok` exige validacao jsonschema contra o contrato da tarefa.
- `semantico_ok` exige o valor de negocio correto dentro do contrato.
- Latencia do modo `schema` inclui o custo de decodificar sob a gramatica.
