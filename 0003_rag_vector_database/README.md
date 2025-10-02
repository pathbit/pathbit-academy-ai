# pathbit-academy-ai

## 0003_rag_vector_database

**Ano:** 2025
**ID do Artigo:** 0003
**Autor:** Eliel Sousa
**Categoria:** Inteligência Artificial / RAG e Vector Databases

---

### 📌 Resumo

Este artigo explora **RAG (Retrieval Augmented Generation)** e **Vector Databases**, tecnologias fundamentais para construir sistemas de IA que acessam informações específicas e atualizadas.
Cobrimos conceitos teóricos, implementações práticas, diferentes tipos de vector databases e casos de uso reais.
Inclui exemplos práticos, código em Python e comparações de performance entre diferentes abordagens.

**🎯 NOVIDADE: Notebook otimizado para Google Colab!** Tudo em um só lugar, sem arquivos externos.

---

### 📂 Estrutura do Artigo

- **`article/ARTICLE.md`** - Conteúdo do artigo.
- **`assets/`** - Imagens, diagramas e outras mídias.
- **`data/`** - PDFs, datasets e outros dados em documentos.
- **`files/`** - Artigos de referência, documentações externas.
- **`notebooks/`** - Jupyter Notebooks com código interativo para testes.
- **`src/`** - Scripts e funções Python usados para executar o código interativo localmente.

---

### 🚀 Como Executar os Exemplos

### 📋 Pré-requisitos

- Python 3.8 ou superior
- Conta no [Groq](https://console.groq.com/) com API Key (opcional)

### 📦 Versões dos Pacotes

- **groq:** 0.32.0 (mais recente)
- **chromadb:** 0.4.22 (mais recente)
- **sentence-transformers:** 3.1.1 (mais recente)
- **numpy:** 1.26.4 (mais recente)
- **pandas:** 2.2.2 (mais recente)
- **matplotlib:** 3.9.0 (mais recente)
- **seaborn:** 0.13.2 (mais recente)
- **jupyter:** 1.1.1 (mais recente)
- **ipython:** 9.5.0 (mais recente)

### 🔧 Configuração das API Keys (Opcional)

```bash
# Definir as variáveis de ambiente (Linux/Mac)
export GROQ_API_KEY='sua_chave_groq_aqui'

# No Windows (PowerShell)
$env:GROQ_API_KEY='sua_chave_groq_aqui'

# No Windows (CMD)
set GROQ_API_KEY=sua_chave_groq_aqui
```

**Nota:** O Chroma funciona sem API Key. O Groq é opcional para exemplos avançados.

### 🚀 Execução Local

```bash
# Clonar o repositório
git clone https://github.com/pathbit/pathbit-academy-ai.git

# Entrar na pasta do artigo
cd pathbit-academy-ai/0003_rag_vector_database

# Criar ambiente virtual e instalar dependências
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

# Executar o script principal
python src/main.py
```

### 📓 Executar o Jupyter Notebook

### Opção 1: Usando o script main.py (Recomendado)

```bash
# Com o ambiente virtual ativado
python src/main.py
```

### Opção 2: Executar diretamente

```bash
# Com o ambiente virtual ativado
jupyter notebook notebooks/rag_vector_database.ipynb
```

### ⚠️ Importante para execução local

- O notebook foi adaptado para funcionar tanto no Colab quanto localmente
- **Funciona sem API Keys** - Todos os exemplos usam Chroma (gratuito)
- O Groq é opcional para exemplos avançados

### 🔧 Soluções para erros comuns

Para problemas específicos, consulte a documentação na pasta `docs/`:

- [Solução para erro do Google Colab](../../docs/SOLUCAO_ERRO_COLAB.md)
- [Solução para erro do Groq](../../docs/SOLUCAO_ERRO_GROQ.md)
- [Atualizações de versões](../../docs/ATUALIZACOES_VERSOES.md)

### 🔍 Estrutura de Arquivos

```bash
0003_rag_vector_database/
├── README.md                           # Este arquivo
├── requirements.txt                    # Dependências Python
├── article/
│   └── ARTICLE.md                     # Conteúdo do artigo
├── assets/                            # Imagens e diagramas
│   ├── 01.png - 13.png              # Imagens técnicas do artigo
│   └── IMAGENS_GUIDE.md             # Guia detalhado das imagens
├── notebooks/
│   └── rag_vector_database.ipynb     # Notebook interativo (AUTOCONTIDO)
└── src/
    └── main.py                        # Script para executar localmente
```

---

### 📚 Artigos Relacionados

- **[Artigo 0001: LLM vs LRM](../0001_llm_x_lrm/README.md)** - Entenda as diferenças entre Large Language Models e Large Reasoning Models
- **[Artigo 0002: Embeddings e Vetorização](../0002_embeddings_vetorizacao/README.md)** - O segredo da mente da IA
- **[Próximo Artigo: 0004 - Fine-tuning vs RAG](../0004_fine_tuning_vs_rag/README.md)** - Quando usar cada estratégia

---

### 🎯 O que você vai aprender

1. **Conceitos Fundamentais** - O que é RAG e por que é revolucionário
2. **Vector Databases** - Diferentes tipos e suas aplicações
3. **Implementação Prática** - Como construir um sistema RAG completo
4. **Casos de Uso Reais** - Chatbots, assistentes, análise de documentos
5. **Otimizações Avançadas** - Hybrid search, query expansion, re-ranking
6. **Comparações** - RAG vs Fine-tuning, quando usar cada estratégia

---

### 🚀 Quick Start

Se você quer começar imediatamente:

1. **Clone o repositório** e navegue até a pasta do artigo
2. **Instale as dependências** com `pip install -r requirements.txt`
3. **Execute o notebook** com `python src/main.py`
4. **Explore os exemplos** e adapte para seu projeto

---

### 💡 Dica do Autor

> RAG é a evolução natural dos embeddings. Não é só uma ferramenta de busca melhorada - é a solução real para o problema da alucinação dos LLMs, permitindo que eles acessem informações específicas, atualizadas e verificáveis. Dominar RAG é fundamental para qualquer sistema de IA que precise ser útil no mundo real.

**Eliel Sousa** - _Pathbit Academy AI_
