# pathbit-academy-ai

## 0002_embeddings_vetorizacao

**Ano:** 2025
**ID do Artigo:** 0002
**Autor:** Eliel Sousa
**Categoria:** Inteligência Artificial / Embeddings e Vetorização

---

### 📌 Resumo

Este artigo explora **Embeddings e Vetorização**, fundamentais para que a IA entenda e processe texto de forma eficiente.
Cobrimos conceitos teóricos, implementações práticas, diferentes tipos de embeddings e casos de uso reais.
Inclui exemplos práticos, código em Python e comparações de performance entre diferentes modelos.

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
- Conta no [Hugging Face](https://huggingface.co/) (gratuita, opcional)

### 📦 Versões dos Pacotes

- **groq:** 0.32.0 (mais recente)
- **sentence-transformers:** 3.1.1 (mais recente)
- **numpy:** 1.26.4 (mais recente)
- **scikit-learn:** 1.4.2 (mais recente)
- **matplotlib:** 3.9.0 (mais recente)
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

**Nota:** O Hugging Face funciona sem API Key para modelos públicos. O Groq é opcional para alguns exemplos.

### 🚀 Execução Local

```bash
# Clonar o repositório
git clone https://github.com/pathbit/pathbit-academy-ai.git

# Entrar na pasta do artigo
cd pathbit-academy-ai/0002_embeddings_vetorizacao

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
jupyter notebook notebooks/embeddings_vetorizacao.ipynb
```

### ⚠️ Importante para execução local

- O notebook foi adaptado para funcionar tanto no Colab quanto localmente
- **Funciona sem API Keys** - Todos os exemplos usam modelos gratuitos do Hugging Face
- O Groq é opcional para exemplos avançados
- O Hugging Face funciona sem API Key para modelos públicos

### 🔧 Soluções para erros comuns

Para problemas específicos, consulte a documentação na pasta `docs/`:

- [Solução para erro do Google Colab](../../docs/SOLUCAO_ERRO_COLAB.md)
- [Solução para erro do Groq](../../docs/SOLUCAO_ERRO_GROQ.md)
- [Atualizações de versões](../../docs/ATUALIZACOES_VERSOES.md)

### 🔍 Estrutura de Arquivos

```bash
0002_embeddings_vetorizacao/
├── README.md                           # Este arquivo
├── requirements.txt                    # Dependências Python
├── article/
│   └── ARTICLE.md                     # Conteúdo do artigo
├── assets/                            # Imagens e diagramas
│   ├── 01.png - 10.png              # Imagens técnicas do artigo
├── notebooks/
│   └── embeddings_vetorizacao.ipynb  # Notebook interativo (AUTOCONTIDO)
└── src/
    └── main.py                        # Script para executar localmente
```

---

### 📚 Artigos Relacionados

- **[Artigo 0001: LLM vs LRM](../0001_llm_x_lrm/README.md)** - Entenda as diferenças entre Large Language Models e Large Reasoning Models
- **[Próximo Artigo: 0003 - RAG (Retrieval Augmented Generation)](../0003_rag/README.md)** - Como combinar embeddings com LLMs para respostas mais precisas

---

### 🎯 O que você vai aprender

1. **Conceitos Fundamentais** - O que são embeddings e por que são essenciais
2. **Tipos de Embeddings** - Diferentes modelos e suas aplicações
3. **Implementação Prática** - Como criar e usar embeddings em Python
4. **Casos de Uso Reais** - Busca semântica, classificação, clustering
5. **Otimização** - Como escolher o modelo certo para seu projeto
6. **Comparações** - Performance entre diferentes abordagens

---

### 🚀 Quick Start

Se você quer começar imediatamente:

1. **Clone o repositório** e navegue até a pasta do artigo
2. **Instale as dependências** com `pip install -r requirements.txt`
3. **Execute o notebook** com `python src/main.py`
4. **Explore os exemplos** e adapte para seu projeto

---

### 💡 Dica do Autor

> Embeddings são a ponte entre linguagem humana e matemática computacional. Dominar este conceito é fundamental para qualquer projeto de IA que trabalhe com texto. Não pule esta etapa - ela é a base para RAG, sistemas de busca semântica e muito mais.

**Eliel Sousa** - _Pathbit Academy AI_
