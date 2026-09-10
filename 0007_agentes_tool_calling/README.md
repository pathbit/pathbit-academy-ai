# pathbit-academy-ai

## 0007_agentes_tool_calling

**Ano:** 2026  
**ID do Artigo:** 0007  
**Autor:** Eliel Sousa  
**Categoria:** Inteligência Artificial / Agentes e Tool Calling

---

### Resumo

Este módulo mostra um agente local com autonomia limitada por arquitetura, não por promessa de marketing:

- guardrail e regra de negócio antes de qualquer execução
- planner que escolhe tool via JSON
- roteamento semântico como fallback ou override
- retrieval em base local JSON
- resposta final com trilha de auditoria por cenário

Tudo roda sem chave de API.

---

### Tecnologias e Modelos Utilizados

- **Planner e resposta final:** `Qwen/Qwen2.5-0.5B-Instruct`
- **Embeddings para router e retrieval:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- **Frameworks:** `transformers`, `sentence-transformers`
- **Ambiente:** Python 3.14, Jupyter, Pandas, Matplotlib

---

### Estrutura do Artigo

- `article/ARTICLE.md` - Conteúdo completo.
- `assets/` e `highlight/` - Imagens técnicas e material de apoio visual.
- `data/` - Cenários, registry de tools, base de conhecimento e auditoria.
- `notebooks/` - Notebook interativo.
- `src/` - Launcher do notebook e simulador do agente.

---

### Como Executar

#### Pré-requisitos

- Python 3.14
- Sem chave de API
- Internet apenas para baixar os modelos gratuitos na primeira execução

#### Preparar o ambiente

```bash
git clone https://github.com/pathbit/pathbit-academy-ai.git
cd pathbit-academy-ai/0007_agentes_tool_calling

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### Abrir o notebook pelo launcher

```bash
python src/main.py
```

#### Rodar o agente diretamente

```bash
python src/agent_runner.py --limit 5
```

#### Executar notebook diretamente

```bash
jupyter notebook notebooks/agentes_tool_calling.ipynb
```

---

### O que você vai aprender

1. Como encadear guardrail, regra de negócio, planner, router e execução.
2. Como usar embeddings tanto para fallback de decisão quanto para retrieval.
3. Como separar arquitetura suportada do que já está demonstrado nos artefatos gerados.
4. Como registrar trilha de auditoria suficiente para revisar cada cenário.

---

### Artefatos gerados

Ao executar o agente, você terá:

- `data/agent_runs.csv` - visão consolidada da execução por cenário
- `data/agent_audit_log.jsonl` - trilha serializada de cada execução
- `data/decision_summary.csv` - resumo por fonte de decisão e acurácia
- `data/retrieval_summary.csv` - detalhe das execuções de `buscar_politica`

Arquivos de suporte usados pelo runner:

- `data/cenarios.json`
- `data/tool_registry.json`
- `data/knowledge_base.json`

---

### Links úteis

- Artigo completo: [ARTICLE.md](./article/ARTICLE.md)
- Repositório: [pathbit-academy-ai](https://github.com/pathbit/pathbit-academy-ai)
