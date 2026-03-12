# Relatório de Evals

- Modelo de embedding: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
- Baseline: qwen_generico
- Melhor candidato: flan_estruturado (google/flan-t5-small)
- Score ponderado baseline: 0.932
- Score ponderado vencedor: 1.357
- Ganho ponderado: 0.425
- Regressões críticas detectadas: 2
- Gate de release: reprovado

## Ranking de candidatos

- `flan_estruturado` (google/flan-t5-small): score ponderado 1.357
- `qwen_generico` (Qwen/Qwen2.5-0.5B-Instruct): score ponderado 0.932
- `qwen_estruturado` (Qwen/Qwen2.5-0.5B-Instruct): score ponderado 0.930

## Regressões detectadas

- `qwen_estruturado` piorou `Como emitir segunda via da fatura?` em -0.200 pontos.
- `qwen_estruturado` piorou `Posso cancelar sem multa?` em -0.205 pontos.