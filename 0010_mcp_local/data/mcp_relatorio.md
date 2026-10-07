# Relatorio do laboratorio MCP local

- Servidor de modelos: Ollama `0.35.1` | Servidor de tools: MCP stdio `pathbit-suporte`
- Tools descobertas: buscar_politica, criar_ticket, resumo_atendimento
- Custo do pulo de protocolo (call_tool): p50 0.99 ms / p95 1.53 ms em 50 chamadas

## Planner por modelo

| modelo       |   plano_valido_pct |   tool_certa_pct |   argumento_ok_pct |   plan_medio_ms |   mcp_medio_ms |   tokens_medios |
|:-------------|-------------------:|-----------------:|-------------------:|----------------:|---------------:|----------------:|
| llama3.2:1b  |                100 |             83.3 |                100 |          2117.6 |            4.7 |            51.8 |
| qwen2.5:1.5b |                100 |             50   |                100 |          2213.3 |            6.5 |            32.5 |
| qwen2.5:0.5b |                100 |             33.3 |                100 |          1764.4 |            7.5 |            27.7 |

## Leitura

- `plan_ms` domina: o modelo em CPU custa ordens de magnitude mais que o protocolo.
- O pulo MCP (`mcp_ms`) e milissegundos; o gargalo segue sendo a geracao do plano.
- A decisao correta depende do modelo, nao do protocolo - o MCP garante o contrato.
