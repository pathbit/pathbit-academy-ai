# pathbit-academy-ai

## 0005_prompt_engineering_avancado

**Ano:** 2026  
**ID do Artigo:** 0005  
**Autor:** Eliel Sousa  
**Categoria:** Inteligência Artificial / Prompt Engineering

---

### Resumo

Este módulo transforma prompt engineering em um laboratório comparativo que separa ganho de instrução de ganho de modelo:

- comparação entre `Qwen/Qwen2.5-0.5B-Instruct` e `google/flan-t5-small`
- benchmark entre `base`, `estruturado`, `few_shot` e `checklist`
- score composto por estrutura, keywords, prioridade e semântica
- delta absoluto e percentual contra a estratégia `base`
- breakdown por caso para inspecionar onde cada estratégia falha

Tudo roda localmente, sem chave de API.

---

### Tecnologias e Modelos Utilizados

- **Geração local:** `Qwen/Qwen2.5-0.5B-Instruct` e `google/flan-t5-small`
- **Embeddings para avaliação:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- **Frameworks:** `transformers`, `sentence-transformers`
- **Ambiente:** Python 3.14, Jupyter, Pandas, Matplotlib

Modelos gratuitos alternativos que você pode testar:

- `google/flan-t5-base`
- `Qwen/Qwen2.5-1.5B-Instruct` (mais pesado)

---

### Estrutura do Artigo

- `article/ARTICLE.md` - Conteúdo completo.
- `assets/` e `highlight/` - Imagens técnicas e material de apoio visual.
- `data/` - Dataset, resultados detalhados, deltas e relatório.
- `notebooks/` - Notebook interativo.
- `src/` - Launcher do notebook e runner do laboratório.

---

### Como Executar

#### Pré-requisitos

- Python 3.14
- Sem chave de API
- Internet apenas para baixar os modelos gratuitos do Hugging Face na primeira execução

#### Preparar o ambiente

```bash
git clone https://github.com/pathbit/pathbit-academy-ai.git
cd pathbit-academy-ai/0005_prompt_engineering_avancado

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### Abrir o notebook pelo launcher

```bash
python src/main.py
```

#### Rodar o laboratório diretamente

```bash
python src/prompt_benchmark.py --limit 2
```

#### Escolher modelos específicos

```bash
python src/prompt_benchmark.py --models "Qwen/Qwen2.5-0.5B-Instruct,google/flan-t5-small" --limit 2
```

#### Executar notebook diretamente

```bash
jupyter notebook notebooks/prompt_engineering_avancado.ipynb
```

---

### O que você vai aprender

1. Como comparar estratégia de prompt e modelo no mesmo dataset.
2. Como distinguir semântica aceitável de saída operacionalmente utilizável.
3. Como ler ganho absoluto e percentual contra uma baseline real.
4. Como identificar se o gargalo ainda é instrução ou se já pede RAG/fine-tuning.

---

### Artefatos gerados

Após executar o laboratório, o projeto gera:

- `data/benchmark_resultados.csv` - todas as execuções por caso, estratégia e modelo
- `data/benchmark_resumo.csv` - médias agregadas por combinação
- `data/benchmark_deltas.csv` - delta absoluto e percentual contra `base`
- `data/benchmark_case_breakdown.csv` - detalhamento por caso com campos ausentes
- `data/benchmark_relatorio.md` - leitura rápida do melhor resultado por modelo

---

### Links úteis

- Artigo completo: [ARTICLE.md](./article/ARTICLE.md)
- Repositório: [pathbit-academy-ai](https://github.com/pathbit/pathbit-academy-ai)
