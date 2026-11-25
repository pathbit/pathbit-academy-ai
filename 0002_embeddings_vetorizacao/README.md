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

- Python 3.14+ (compatível com 3.10+) executando em ambiente virtual isolado (.venv)
- Acesso ao Hugging Face na primeira execução para baixar o modelo público de embeddings

### 📦 Versões dos Pacotes

- **sentence-transformers:** 3.1.1 (versão histórica; consulte o ambiente instalado)
- **numpy:** 1.26.4 (versão histórica; consulte o ambiente instalado)
- **scikit-learn:** 1.4.2 (versão histórica; consulte o ambiente instalado)
- **matplotlib:** 3.9.0 (versão histórica; consulte o ambiente instalado)
- **jupyter:** 1.1.1 (versão histórica; consulte o ambiente instalado)
- **ipython:** 9.5.0 (versão histórica; consulte o ambiente instalado)

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

### Opção 1 - Usando o script main.py (Recomendado)

```bash
# Com o ambiente virtual ativado
python src/main.py
```

### Opção 2 - Executar diretamente

```bash
# Com o ambiente virtual ativado
jupyter notebook notebooks/embeddings_vetorizacao.ipynb
```

### ⚠️ Importante para execução local

- O notebook foi adaptado para funcionar tanto no Colab quanto localmente
- O notebook usa um modelo público do Hugging Face e roda sem chave de API.

### 🔧 Soluções para erros comuns

Para problemas específicos, consulte a documentação na pasta `docs/`:

- [Solução para erro do Google Colab](../docs/SOLUCAO_ERRO_COLAB.md)
- [Atualizações de versões](../docs/ATUALIZACOES_VERSOES.md)

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
- **[Próximo Artigo: 0003 - RAG (Retrieval Augmented Generation)](../0003_rag_vector_database/README.md)** - Como combinar embeddings com LLMs para respostas mais precisas

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
