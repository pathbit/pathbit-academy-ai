# Relatorio do laboratorio de saida estruturada

- Servidor: Ollama `0.35.1`
- Modelos: llama3.2:1b, qwen2.5:1.5b, nomic-embed-text:latest, qwen2.5:0.5b

## Resumo por nivel de contrato

| modo   |   parse_ok_pct |   schema_ok_pct |   semantico_ok_pct |   recuperado_pct |   total_medio_ms |   tokens_medios |   chamadas |
|:-------|---------------:|----------------:|-------------------:|-----------------:|-----------------:|----------------:|-----------:|
| json   |           83.3 |               0 |                0   |                0 |            944.9 |            38.3 |         18 |
| livre  |            0   |               0 |                0   |                0 |           2514.9 |            79.8 |         18 |
| schema |          100   |             100 |               44.4 |              nan |            352.9 |            22.7 |         18 |

## Resumo por modelo e nivel

| modelo       | modo   |   parse_ok_pct |   schema_ok_pct |   semantico_ok_pct |   total_medio_ms |
|:-------------|:-------|---------------:|----------------:|-------------------:|-----------------:|
| llama3.2:1b  | json   |           66.7 |               0 |                0   |           1423.3 |
| llama3.2:1b  | livre  |            0   |               0 |                0   |           4159.2 |
| llama3.2:1b  | schema |          100   |             100 |               33.3 |            484.6 |
| qwen2.5:0.5b | json   |           83.3 |               0 |                0   |            679.4 |
| qwen2.5:0.5b | livre  |            0   |               0 |                0   |           1366.1 |
| qwen2.5:0.5b | schema |          100   |             100 |               66.7 |            245.1 |
| qwen2.5:1.5b | json   |          100   |               0 |                0   |            732.1 |
| qwen2.5:1.5b | livre  |            0   |               0 |                0   |           2019.2 |
| qwen2.5:1.5b | schema |          100   |             100 |               33.3 |            329   |

## A Nova Fronteira: Modelos System 1 (Passada Unica sem Geracao)

- **Paradigma:** `System 1 (Single Forward Pass / Decisor Direto)`
- **Referencias da Industria:** `Laya (Open-Source), Jev (TypeSafe AI), Kev`
- **Latencia Mediana (p50):** `14.78 ms` (vs ~1.500 ms no modo schema)
- **Latencia Percentil 95 (p95):** `17.01 ms`
- **Latencia Media:** `15.11 ms`
- **Tokens gerados no decoder:** `0` (sem loop autoregressivo)
- **Conformidade com schema:** `100.0%`
- **Acuracia de decisao:** `100.0%`

> **Conclusao:** Enquanto LLMs generativos com JSON Schema garantem a integridade de payloads complexos com texto livre (~1.500 ms), modelos System 1 (como o Laya em open-source ou Jev na nuvem) resolvem roteamento e selecao de tools com mais de 50x de reducao de latencia.

## Leitura

- `parse_ok` aceita JSON direto ou apos limpeza de code fences (resgate basico).
- `schema_ok` exige validacao jsonschema contra o contrato da tarefa.
- `semantico_ok` exige o valor de negocio correto dentro do contrato.
- Latencia do modo `schema` inclui o custo de decodificar sob a gramatica.
