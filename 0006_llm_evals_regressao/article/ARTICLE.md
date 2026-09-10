# LLM Evals na prática e como escolher candidatos e detectar regressão antes do deploy

Muita conversa sobre Evals ainda para cedo demais. Compara duas respostas, declara um vencedor e trata isso como decisão técnica. Esse primeiro passo é útil, mas continua curto quando o problema real do time é outro: escolher entre candidatos completos de inferência e decidir se algum deles merece ir para produção.

Este artigo trata avaliação nesse nível. O runner compara combinações reais de modelo + prompt, pondera a criticidade dos casos, mede regressão por cenário e transforma o resultado em um gate de release. A pergunta muda de "a resposta ficou melhor?" para "qual candidato melhorou o sistema sem abrir risco onde mais importa?".

Tudo isso continua 100% gratuito, usando `Qwen/Qwen2.5-0.5B-Instruct`, `google/flan-t5-small` e embeddings com `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.

> Se você vier do artigo de [Prompt Engineering Avançado](https://github.com/pathbit/pathbit-academy-ai/blob/master/0005_prompt_engineering_avancado/article/ARTICLE.md), vai reconhecer a continuidade natural. Lá o foco era medir estratégia de prompt. Aqui o foco é comparar candidatos completos e decidir quem passa no crivo operacional.

## O problema que a comparação rasa não enxerga

![Risco de regressão](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0006_llm_evals_regressao/assets/01.png)

> Figura 1: Melhorar um caso chamativo não significa melhorar o sistema inteiro.

Quando você altera um sistema com LLM, o risco não é apenas responder pior em média. O risco real é melhorar um caso vistoso e piorar silenciosamente um cenário crítico de contrato, financeiro ou política. Se a avaliação não enxerga isso, ela não serve como mecanismo de release.

É exatamente por isso que a esteira deste artigo sai do formato "v1 contra v2" e passa para comparação entre candidatos.

## Os candidatos que entram na disputa

O runner compara três candidatos explícitos:

- `qwen_generico` como baseline;
- `qwen_estruturado` como evolução de prompt no mesmo modelo;
- `flan_estruturado` como candidato alternativo de modelo.

```python
def build_candidate_registry():
    return {
        "qwen_generico": {
            "model": "Qwen/Qwen2.5-0.5B-Instruct",
            "prompt_builder": qwen_generic_prompt,
        },
        "qwen_estruturado": {
            "model": "Qwen/Qwen2.5-0.5B-Instruct",
            "prompt_builder": qwen_structured_prompt,
        },
        "flan_estruturado": {
            "model": "google/flan-t5-small",
            "prompt_builder": flan_structured_prompt,
        },
    }
```

Isso deixa a esteira útil para trabalho real. Você consegue promover uma mudança de prompt, trocar de modelo ou comparar as duas coisas ao mesmo tempo sem mudar a estrutura de avaliação.

## O dataset carrega contexto, gabarito e criticidade

![Dataset de evals](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0006_llm_evals_regressao/assets/03.png)

> Figura 2: Cada caso traz contexto, resposta ideal, palavras críticas, categoria e peso de risco.

O `eval_dataset.csv` não tem só pergunta e resposta esperada. Ele carrega as colunas que normalmente faltam em demos superficiais:

- `contexto`
- `gold`
- `palavras_criticas`
- `categoria`
- `criticidade`

Essa diferença importa porque nem todo erro tem o mesmo peso. Um deslize em baixa criticidade é inconveniente. Uma regressão em contrato ou financeiro é risco de operação.

## O score técnico mede aderência antes de ponderar risco

![Métricas de avaliação](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0006_llm_evals_regressao/assets/02.png)

> Figura 3: O runner separa qualidade técnica do peso operacional de cada caso.

O score de cada resposta combina três dimensões:

- similaridade semântica com o `gold`;
- `keyword_recall` sobre palavras críticas;
- `faithfulness` ao contexto recebido.

```python
score_semantic = semantic_similarity(embedder, row["gold"], pred)
score_keywords = keyword_recall(keywords, pred)
score_faithfulness = faithfulness(row["contexto"], pred)
score_final = float(np.mean([score_semantic, score_keywords, score_faithfulness]))
```

Depois disso, a esteira aplica o peso de criticidade:

```python
CRITICALITY_WEIGHTS = {"alta": 1.5, "media": 1.0, "baixa": 0.8}


def weighted_score(score: float, criticidade: str) -> float:
    return score * CRITICALITY_WEIGHTS.get(criticidade, 1.0)
```

Esse segundo passo é o que tira a avaliação da média ingênua. Um candidato pode parecer aceitável olhando só o `score_final` e ainda assim ser insuficiente quando os casos mais sensíveis passam a valer mais.

## A regressão deixa de ser um detalhe invisível

![Gate de release](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0006_llm_evals_regressao/assets/04.png)

> Figura 4: A decisão final combina ranking agregado com inspeção de regressões caso a caso.

O runner não escolhe vencedor apenas por média. Ele também calcula delta por cenário contra a baseline:

```python
comparison["delta_vs_baseline"] = comparison["score_ponderado"] - comparison["baseline_score"]
regressions = comparison[
    (comparison["candidate"] != baseline_name)
    & (comparison["delta_vs_baseline"] < -0.05)
]
```

Com os artefatos observados nesta pasta, o ranking ficou assim:

- `flan_estruturado`: `score_ponderado` de `1.357`;
- `qwen_generico`: `0.932`;
- `qwen_estruturado`: `0.930`.

O detalhe importante é que o melhor score agregado não liberou deploy automaticamente. O relatório atual mostra:

- baseline ponderada em `0.932`;
- melhor candidato em `1.357`;
- ganho ponderado de `0.425`;
- `2` regressões críticas detectadas;
- gate final `reprovado`.

Isso acontece porque o gate implementado hoje é conservador:

```python
gate = "aprovado" if gain >= 0.05 and critical_regressions.empty else "reprovado"
```

Ou seja: a esteira não olha só para o campeão do ranking. Ela também considera se o conjunto comparado produziu regressões críticas. Nos dados atuais, o `flan_estruturado` lidera o ranking, mas o `qwen_estruturado` piora dois casos críticos. O resultado é um release reprovado.

Esse comportamento é uma decisão explícita da implementação atual. Ele transforma a avaliação em um harness de decisão mais duro do que um leaderboard simples.

## Os artefatos que saem da esteira

![Pipeline de avaliação contínua](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0006_llm_evals_regressao/assets/05.png)

> Figura 5: A esteira produz material suficiente para análise agregada, por categoria e por caso crítico.

Depois da execução, a pasta `data/` concentra seis saídas principais:

- `geracoes_evals.csv` com cada resposta gerada e seus scores;
- `candidate_summary.csv` com ranking agregado por candidato;
- `candidate_summary_by_category.csv` e `critical_cases.csv` para leitura por categoria e foco nos casos de criticidade alta;
- `regressoes_detectadas.csv` com deltas negativos relevantes contra a baseline;
- `relatorio_evals.md` com resumo textual de ranking, ganho e gate.

É esse conjunto que faz o artigo sair do território do post conceitual. Você passa a ter evidência suficiente para discutir promoção, reprovação e risco residual.

## Show-Me-The-Code

O artigo entrega uma esteira de avaliação que permite:

- comparar candidatos completos de inferência, não só respostas soltas;
- medir score técnico e score ponderado pelo risco do caso;
- detectar regressões contra baseline no nível de cada pergunta;
- produzir ranking, recorte por categoria, recorte crítico e relatório de release.

**Opção 1** Execute a esteira localmente e gere os relatórios no terminal.

[**Abrir README.md com instruções locais**](https://github.com/pathbit/pathbit-academy-ai/blob/master/0006_llm_evals_regressao/README.md)

**Opção 2** Abra o notebook e acompanhe o ranking entre candidatos.

[**Abrir notebook de testes**](https://github.com/pathbit/pathbit-academy-ai/blob/master/0006_llm_evals_regressao/notebooks/llm_evals_regressao.ipynb)

## Próximos passos

Se você quiser endurecer ainda mais essa esteira:

1. aumente o número de categorias e criticidades no CSV;
2. adicione candidatos novos na registry;
3. decida se o gate deve olhar o conjunto inteiro ou apenas o candidato vencedor;
4. reaplique a mesma estrutura para comparar prompt, modelo e RAG no mesmo pipeline.

É nesse ponto que Evals deixa de ser discurso sobre qualidade e vira critério de decisão técnica.

## Referências

- [Hugging Face - Qwen 0.5B Instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct)
- [Hugging Face - FLAN-T5](https://huggingface.co/google/flan-t5-small)
- [Sentence Transformers - Multilingual MiniLM](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)
