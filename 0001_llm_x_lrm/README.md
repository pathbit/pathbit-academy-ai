# pathbit-academy-ai

## 0001_llm_x_lrm

**Ano:** 2025
**ID do Artigo:** 0001
**Autor:** Eliel Sousa
**Categoria:** Inteligência Artificial / Modelos de Linguagem

---

### 📌 Resumo

Este artigo explora as diferenças entre **LLM (Large Language Models)** e **LRM (Large Reasoning Models)**, cobrindo conceitos, casos de uso, vantagens e limitações.
Inclui exemplos práticos, código em Python e comparações de desempenho.

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

#### 📋 Pré-requisitos

- Python 3.14
- Conta no [Groq](https://console.groq.com/) com API Key

#### 📦 Versões dos Pacotes

- **Groq:** 0.32.0 (mais recente)
- **Jupyter:** 1.1.1 (mais recente)
- **IPython:** 9.5.0 (mais recente)

#### 🔧 Configuração da API Key

```bash
# Definir a variável de ambiente (Linux/Mac)
export GROQ_API_KEY='sua_chave_aqui'

# No Windows (PowerShell)
$env:GROQ_API_KEY='sua_chave_aqui'

# No Windows (CMD)
set GROQ_API_KEY=sua_chave_aqui
```

#### 🚀 Execução Local

```bash
# Clonar o repositório
git clone https://github.com/pathbit/pathbit-academy-ai.git

# Entrar na pasta do artigo
cd pathbit-academy-ai/0001_llm_x_lrm

# Criar ambiente virtual e instalar dependências
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

# Executar o script principal
python src/main.py
```

#### 📓 Executar o Jupyter Notebook

#### Opção 1: Usando o script main.py (Recomendado)

```bash
# Com o ambiente virtual ativado
python src/main.py
```

#### Opção 2: Executar diretamente

```bash
# Com o ambiente virtual ativado
jupyter notebook notebooks/comparacao_llm_lrm.ipynb
```

#### ⚠️ Importante para execução local

- O notebook foi adaptado para funcionar tanto no Colab quanto localmente
- Se executar localmente, será solicitada a API Key do Groq
- Certifique-se de ter a `GROQ_API_KEY` configurada ou digite quando solicitado

#### 🔧 Soluções para erros comuns

Para problemas específicos, consulte a documentação na pasta `docs/`:

- [Solução para erro do Google Colab](../../docs/SOLUCAO_ERRO_COLAB.md)
- [Solução para erro do Groq](../../docs/SOLUCAO_ERRO_GROQ.md)
- [Atualizações de versões](../../docs/ATUALIZACOES_VERSOES.md)

#### 🔍 Estrutura de Arquivos

```bash
0001_llm_x_lrm/
├── README.md                           # Este arquivo
├── requirements.txt                    # Dependências Python
├── article/
│   └── ARTICLE.md                     # Conteúdo do artigo
├── assets/                            # Imagens e diagramas
├── notebooks/
│   └── comparacao_llm_lrm.ipynb      # Notebook interativo
└── src/
    └── main.py                        # Script principal
```
