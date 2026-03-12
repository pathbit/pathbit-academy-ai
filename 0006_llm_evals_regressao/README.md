# pathbit-academy-ai

## 0006_llm_evals_regressao

**Ano:** 2026  
**ID do Artigo:** 0006  
**Autor:** Eliel Sousa  
**Categoria:** Inteligência Artificial / Avaliação de LLM

---

### Resumo

Este módulo monta uma esteira de avaliação voltada a decisão de release, comparando candidatos completos em vez de respostas soltas:

- baseline com `qwen_generico`, evolução com `qwen_estruturado` e candidato alternativo `flan_estruturado`
- score técnico e score ponderado por criticidade
- detecção de regressões por caso contra baseline
- gate de release que pode reprovar mesmo com ganho agregado

Tudo usando modelos gratuitos do Hugging Face.

---

### Tecnologias e Modelos Utilizados

- **Candidatos de geração:** `Qwen/Qwen2.5-0.5B-Instruct` e `google/flan-t5-small`
- **Embeddings para avaliação:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- **Frameworks:** `transformers`, `sentence-transformers`
- **Ambiente:** Python 3.14, Jupyter, Pandas, Matplotlib

---

### Estrutura do Artigo

- `article/ARTICLE.md` - Conteúdo completo.
- `assets/` e `highlight/` - Imagens técnicas e material de apoio visual.
- `data/` - Dataset, ranking, recortes por categoria, casos críticos e regressões.
- `notebooks/` - Notebook interativo.
- `src/` - Launcher do notebook e runner de evals.

---

### Como Executar

#### Pré-requisitos

- Python 3.14
- Sem chave de API
- Internet apenas para baixar os modelos gratuitos na primeira execução

#### Preparar o ambiente

```bash
git clone https://github.com/pathbit/pathbit-academy-ai.git
cd pathbit-academy-ai/0006_llm_evals_regressao

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### Abrir o notebook pelo launcher

```bash
python src/main.py
```

#### Rodar a esteira diretamente

```bash
python src/eval_runner.py --limit 3
```

#### Escolher candidatos específicos

```bash
python src/eval_runner.py --candidates "qwen_generico,qwen_estruturado,flan_estruturado" --limit 3
```

#### Executar notebook diretamente

```bash
jupyter notebook notebooks/llm_evals_regressao.ipynb
```

---

### O que você vai aprender

1. Como comparar candidatos completos de inferência na mesma esteira.
2. Como separar score técnico de peso operacional por criticidade.
3. Como detectar regressão caso a caso contra uma baseline explícita.
4. Como interpretar um gate que distingue melhor score de deploy aprovado.

---

### Artefatos gerados

Depois da execução, você terá:

- `data/geracoes_evals.csv` - respostas geradas e scores por caso
- `data/candidate_summary.csv` - ranking agregado por candidato
- `data/candidate_summary_by_category.csv` e `data/critical_cases.csv` - leitura por categoria e foco nos casos críticos
- `data/regressoes_detectadas.csv` - regressões relevantes contra baseline
- `data/relatorio_evals.md` - resumo textual de ganho e gate

---

### Links úteis

- Artigo completo: [ARTICLE.md](./article/ARTICLE.md)
- Repositório: [pathbit-academy-ai](https://github.com/pathbit/pathbit-academy-ai)
