**Slide 1**
AGENTES E TOOL CALLING
Quando a autonomia ajuda e quando ela vira risco.

**Slide 2**
O QUE FOI ELEVADO NO ARTIGO
Não é só roteamento por palavra-chave.
Agora existe planner, fallback, retrieval e auditoria.

**Slide 3**
O STACK GRATUITO
- planner e resposta final com Qwen 0.5B Instruct
- embeddings de roteamento com MiniLM multilingual
- base local em JSON
- zero API paga

**Slide 4**
COMO O AGENTE FUNCIONA
1. guardrail
2. planner em JSON
3. fallback por embeddings
4. execução da tool
5. resposta final

**Slide 5**
O QUE O PLANNER ENTREGA
Ele devolve:
- tool
- argument
- reason

Ou seja, o agente passa a explicar por que escolheu agir daquele jeito.

**Slide 6**
O QUE A AUDITORIA REGISTRA
- tool planejada
- tool executada
- uso de fallback
- documento recuperado
- resposta final

**Slide 7**
POR QUE ISSO IMPORTA
Autonomia sem trilha de auditoria é só uma caixa-preta simpática.
Autonomia com rastreabilidade vira arquitetura séria.

**Slide 8**
O QUE VOCÊ CONSEGUE RODAR
- planner local
- retrieval em base local
- ticket simulado
- agent_runs.csv
- agent_audit_log.jsonl

**Slide 9**
Link do artigo nos comentários.
Agente bom não é o mais livre. É o mais governável.
