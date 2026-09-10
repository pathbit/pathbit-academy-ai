# 🚀 Pathbit Academy AI

Conteúdos sobre inteligência artificial publicados pela **Pathbit**.

---

## 📚 Artigos Disponíveis

### [0001 - LLM vs LRM](./0001_llm_x_lrm/)

**Ano:** 2025 | **Categoria:** Inteligência Artificial / Modelos de Linguagem

Explora as diferenças entre **LLM (Large Language Models)** e **LRM (Large Reasoning Models)**, cobrindo conceitos, casos de uso, vantagens e limitações. Inclui exemplos práticos, código em Python e comparações de desempenho.

[📖 Ler Artigo](./0001_llm_x_lrm/) | [🔧 Executar Localmente](./0001_llm_x_lrm/README.md)

---

### [0002 - Embeddings e Vetorização](./0002_embeddings_vetorizacao/)

**Ano:** 2025 | **Categoria:** Inteligência Artificial / Embeddings e Vetorização

Explora **Embeddings e Vetorização**, fundamentais para que a IA entenda e processe texto de forma eficiente. Cobrimos conceitos teóricos, implementações práticas, diferentes tipos de embeddings e casos de uso reais. Inclui exemplos práticos, código em Python e comparações de performance entre diferentes modelos.

[📖 Ler Artigo](./0002_embeddings_vetorizacao/) | [🔧 Executar Localmente](./0002_embeddings_vetorizacao/README.md)

---

### [0003 - RAG e Vector Database](./0003_rag_vector_database/)

**Ano:** 2025 | **Categoria:** Inteligência Artificial / RAG e Vector Databases

Explora **RAG (Retrieval Augmented Generation)** e **Vector Databases**, tecnologias fundamentais para construir sistemas de IA que acessam informações específicas e atualizadas. Cobrimos conceitos teóricos, implementações práticas, diferentes tipos de vector databases e casos de uso reais. Inclui exemplos práticos, código em Python e comparações de performance entre diferentes abordagens.

[📖 Ler Artigo](./0003_rag_vector_database/) | [🔧 Executar Localmente](./0003_rag_vector_database/README.md)

---

### [0004 - RAG vs Fine-Tuning](./0004_rag_vs_finetuning/)

**Ano:** 2025 | **Categoria:** Inteligência Artificial / RAG vs Fine-Tuning

Explora as diferenças entre **RAG** e **Fine-Tuning**, ajudando você a escolher a abordagem certa para seu projeto de IA. Cobrimos comparações técnicas, análise de custos, casos práticos de sucesso e fracasso, e quando usar cada estratégia. Inclui fine-tuning REAL com LoRA, matriz de decisão objetiva e exemplos executáveis em Python com caso de uso de assistente de investimentos.

[📖 Ler Artigo](./0004_rag_vs_finetuning/) | [🔧 Executar Localmente](./0004_rag_vs_finetuning/README.md)

---

### [0005 - Prompt Engineering Avançado](./0005_prompt_engineering_avancado/)

**Ano:** 2026 | **Categoria:** Inteligência Artificial / Prompt Engineering

Transforma prompt engineering em um laboratório comparativo entre `Qwen` e `FLAN`, medindo estrutura, keywords, prioridade e semântica para separar ganho de prompt de ganho de modelo.

[📖 Ler Artigo](./0005_prompt_engineering_avancado/) | [🔧 Executar Localmente](./0005_prompt_engineering_avancado/README.md)

---

### [0006 - LLM Evals e Regressão](./0006_llm_evals_regressao/)

**Ano:** 2026 | **Categoria:** Inteligência Artificial / Avaliação de LLM

Mostra uma esteira de evals que compara candidatos completos, pondera criticidade, detecta regressões por caso e explicita quando o melhor score ainda não é suficiente para liberar deploy.

[📖 Ler Artigo](./0006_llm_evals_regressao/) | [🔧 Executar Localmente](./0006_llm_evals_regressao/README.md)

---

### [0007 - Agentes e Tool Calling](./0007_agentes_tool_calling/)

**Ano:** 2026 | **Categoria:** Inteligência Artificial / Agentes

Apresenta um agente local com guardrail, regra de negócio, planner JSON, roteamento semântico, retrieval e trilha de auditoria para operar com autonomia sem perder controle.

[📖 Ler Artigo](./0007_agentes_tool_calling/) | [🔧 Executar Localmente](./0007_agentes_tool_calling/README.md)

---

## 📖 Documentação

### 🔧 Soluções para Problemas Comuns

- **[Erro do Google Colab](./docs/SOLUCAO_ERRO_COLAB.md)** - Resolução do erro `ModuleNotFoundError: No module named 'google'`
- **[Erro do Groq](./docs/SOLUCAO_ERRO_GROQ.md)** - Resolução do erro `TypeError: Client.__init__() got an unexpected keyword argument 'proxies'`
- **[Atualizações de Versões](./docs/ATUALIZACOES_VERSOES.md)** - Histórico de atualizações dos pacotes

### 📁 Estrutura do Projeto

```bash
pathbit-academy-ai/
├── README.md                          # Este arquivo
├── docs/                              # Documentação técnica
│   ├── SOLUCAO_ERRO_COLAB.md
│   ├── SOLUCAO_ERRO_GROQ.md
│   └── ATUALIZACOES_VERSOES.md
├── 0001_llm_x_lrm/                    # Artigo 0001
│   ├── README.md
│   ├── requirements.txt
│   ├── article/
│   ├── assets/
│   ├── notebooks/
│   └── src/
├── 0002_embeddings_vetorizacao/       # Artigo 0002
│   ├── README.md
│   ├── requirements.txt
│   ├── article/
│   ├── assets/
│   ├── notebooks/
│   └── src/
├── 0003_rag_vector_database/          # Artigo 0003
│   ├── README.md
│   ├── requirements.txt
│   ├── article/
│   ├── assets/
│   ├── notebooks/
│   └── src/
├── 0004_rag_vs_finetuning/            # Artigo 0004
│   ├── README.md
│   ├── requirements.txt
│   ├── article/
│   ├── assets/
│   ├── notebooks/
│   └── src/
├── 0005_prompt_engineering_avancado/  # Artigo 0005
│   ├── README.md
│   ├── requirements.txt
│   ├── article/
│   ├── assets/
│   ├── notebooks/
│   └── src/
├── 0006_llm_evals_regressao/          # Artigo 0006
│   ├── README.md
│   ├── requirements.txt
│   ├── article/
│   ├── assets/
│   ├── notebooks/
│   └── src/
└── 0007_agentes_tool_calling/         # Artigo 0007
    ├── README.md
    ├── requirements.txt
    ├── article/
    ├── assets/
    ├── notebooks/
    └── src/
```

---

## 🛠️ Como Contribuir

1. Clone o repositório
2. Crie uma nova pasta para seu artigo seguindo o padrão `XXXX_titulo_do_artigo`
3. Siga a estrutura de pastas estabelecida
4. Adicione seu artigo à lista acima

## 📋 Estrutura Padrão dos Artigos

```bash
XXXX_titulo_do_artigo/
├── README.md                    # Instruções de execução e resumo
├── requirements.txt             # Dependências Python
├── article/
│   └── ARTICLE.md              # Conteúdo do artigo
├── assets/                     # Imagens e diagramas
├── notebooks/                  # Jupyter Notebooks interativos
└── src/
    └── main.py                 # Script para execução local
```

---

**Desenvolvido com ❤️ pela [Pathbit](https://pathbit.com)**
