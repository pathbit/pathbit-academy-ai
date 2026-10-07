# LLM Evals e testes de regressão: como escolher candidatos e barrar falhas antes do deploy

A avaliação de sistemas baseados em modelos de linguagem é um dos elos mais vulneráveis da engenharia moderna de software. Em equipes sem práticas maduras de observabilidade, a homologação de uma alteração no prompt ou a troca de um modelo de fundação costuma se apoiar em testes anedóticos. Um desenvolvedor submete três ou quatro perguntas no terminal, inspeciona visualmente as respostas, acha o resultado convincente e promove a versão para produção.

Esse método informal, conhecido na comunidade técnica como vibe check, cria uma falsa sensação de segurança. Em sistemas determinísticos tradicionais, suítes completas de testes unitários e de integração impedem que alterações em um microsserviço quebrem regras já consolidadas. No universo probabilístico dos modelos gerativos, porém, uma modificação no texto do prompt de sistema pode melhorar visivelmente casos gerais de conversação, mas degradar silenciosamente cenários contratuais críticos de alta gravidade.

Este artigo apresenta uma esteira automatizada e rigorosa de avaliação contínua (LLM Evals) com detecção determinística de regressões. O laboratório compara candidatos completos de inferência combinando modelos abertos e estratégias de prompt, pondera a criticidade dos cenários pelo risco de negócio e transforma o resultado em um gate formal de liberação de versão.

---

## O risco da média ingênua e as regressões silenciosas

O perigo mais insidioso em esteiras de inteligência artificial não é o modelo responder mal em todos os cenários, mas introduzir regressões pontuais em casos de alta sensibilidade.

![Risco de regressão](../assets/01.png)

> Figura 1. O perigo de aprovar alterações guiando-se por médias agregadas que ocultam falhas em cenários de alta criticidade.

Se uma equipe avalia seus prompts calculando apenas a média geral de acertos sobre cem casos de teste, um ganho vistoso em oitenta perguntas rotineiras de atendimento ao cliente pode elevar a pontuação agregada do sistema. No entanto, se essa mesma alteração fizer o modelo falhar nas duas únicas perguntas que envolviam prazos legais de rescisão contratual ou regras de estorno financeiro, o sistema tornou-se mais perigoso para o negócio, apesar de a média aritmética sugerir evolução.

Para que uma esteira de avaliação atue como ferramenta real de governança, ela precisa desacoplar a análise agregada da inspeção de limites críticos, rejeitando qualquer release que degrade regras fundamentais de operação.

---

## O registro de candidatos como unidade de implantação

Em engenharia de software com IA, um deploy nunca envolve apenas o peso do modelo ou o arquivo de texto do prompt isoladamente. A unidade atômica que entra em produção é a combinação do modelo de fundação com seu prompt constrangido e seus hiperparâmetros de inferência.

O laboratório deste módulo estrutura essa comparação definindo três candidatos formais em um registro unificado:

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

O primeiro candidato, `qwen_generico`, atua como a baseline do sistema, representando o modelo aberto da família Qwen executado com instruções padrão em texto livre. O segundo candidato, `qwen_estruturado`, avalia o ganho obtido ao impor um contrato estrito de saída sem alterar o hardware subjacente. Por fim, o terceiro candidato, `flan_estruturado`, introduz uma mudança na arquitetura do modelo, testando o encoder-decoder da família FLAN sob a mesma especificação de campos.

Esse desenho modular permite comparar promoção de prompts, migração de modelos ou refatorações simultâneas de arquitetura mantendo exatamente o mesmo crivo de homologação.

---

## Anatomia de um dataset de teste profissional

Diferente de datasets ingênuos que se limitam a pares de pergunta e resposta, o arquivo de avaliação deste laboratório (`eval_dataset.csv`) incorpora metadados operacionais essenciais para governança.

![Dataset de evals](../assets/02.png)

> Figura 2. Estrutura do dataset incorporando contexto factual, gabarito de referência, termos mandatórios e classificação de risco.

Cada registro da base carrega cinco colunas técnicas: o contexto documental recebido pelo modelo, o gabarito ideal esperado (gold), a lista de palavras-chave mandatórias para aquela resposta, a categoria operacional do chamado (como financeiro, suporte técnico ou comercial) e a classificação de criticidade do cenário, dividida em alta, média e baixa.

Essa catalogação prévia estabelece a base para ponderar a severidade das falhas. Uma resposta imprecisa sobre horários de atendimento gera ruído passageiro, enquanto uma falha em uma cláusula financeira de criticidade alta gera prejuízo patrimonial direto.

---

## Decomposição técnica da pontuação e pesos de criticidade

A avaliação de cada candidato evita depender exclusivamente de julgamentos subjetivos, combinando três métricas algorítmicas complementares.

![Métricas de avaliação](../assets/03.png)

> Figura 3. Cálculo da pontuação multidimensional combinando similaridade semântica, retenção de palavras críticas e fidelidade ao contexto.

A similaridade semântica compara embeddings da resposta e do gabarito. O keyword recall mede cobertura literal de termos. A função chamada `faithfulness` neste runner mede **sobreposição de tokens da resposta com o contexto**, não implicação lógica nem verdade factual. Uma frase que troca “permitido” por “não permitido” pode preservar muitas palavras e obter nota alta; casos assim exigem verificações específicas.

```python
score_semantic = semantic_similarity(embedder, row["gold"], pred)
score_keywords = keyword_recall(keywords, pred)
score_faithfulness = faithfulness(row["contexto"], pred)
score_final = float(np.mean([score_semantic, score_keywords, score_faithfulness]))
```

Após o cálculo do escore bruto, o runner aplica multiplicadores ponderados conforme a criticidade do cenário:

```python
CRITICALITY_WEIGHTS = {"alta": 1.5, "media": 1.0, "baixa": 0.8}

def weighted_score(score: float, criticidade: str) -> float:
    return score * CRITICALITY_WEIGHTS.get(criticidade, 1.0)
```

Essa multiplicação recalibra a influência dos casos no ranking global. Um candidato mediano em perguntas simples que gabarita todos os cenários de risco elevado supera um candidato superficialmente eloquente que tropeça nas perguntas cruciais.

---

## Detecção de regressões e o gate automatizado de release

O diferencial entre um leaderboard decorativo e um sistema de engenharia reside na capacidade de impedir deploys que violem políticas de qualidade.

![Gate de release](../assets/04.png)

> Figura 4. O mecanismo de gate automatizado avaliando deltas de regressão cenário a cenário antes de autorizar o deploy.

O runner calcula o delta individual de cada caso comparando o desempenho do novo candidato com a pontuação histórica da baseline:

```python
comparison["delta_vs_baseline"] = comparison["score_ponderado"] - comparison["baseline_score"]
regressions = comparison[
    (comparison["candidate"] != baseline_name)
    & (comparison["delta_vs_baseline"] < -0.05)
]
```

Uma queda maior que **0,05 pontos de score ponderado** é registrada como regressão. Não são cinco pontos percentuais de acurácia: o score é multiplicado por criticidade e pode ultrapassar 1. O relatório lista todos os candidatos, mas a decisão de deploy considera apenas regressões do candidato escolhido.

A regra de liberação de versão implementada na esteira é intencionalmente conservadora:

```python
gate = "aprovado" if gain >= 0.05 and critical_regressions.empty else "reprovado"
```

O candidato escolhido precisa ganhar pelo menos **0,05 pontos ponderados** sobre a baseline e não ter regressões críticas acima do limiar. Essa regra não detecta quedas menores que 0,05 nem garante qualidade absoluta. Em produção, acrescente pisos por categoria, casos adversos e repetições; uma comparação relativa pode aprovar dois candidatos ruins.

Os dados preservados registram `flan_estruturado` com **1,357** e baseline `qwen_generico` com **0,750**. As regressões registradas pertencem a `qwen_estruturado`, não ao FLAN. A versão anterior do gate misturava candidatos e podia reprovar o vencedor por falhas de outro; o runner agora filtra pelo candidato escolhido. Os relatórios históricos em `data/` permanecem intactos e devem ser lidos como evidência daquela versão, não como decisão do código corrigido.

![Pipeline de avaliação contínua](../assets/05.png)

> Figura 5. O fluxo contínuo de auditoria gerando artefatos estruturados para conferência detalhada da equipe de engenharia.

---

## Execução prática do laboratório passo a passo

O repositório fornece a suíte completa de avaliação pronta para ser executada localmente em CPU pura via linha de comando ou pelo Jupyter Notebook.

Para rodar a bateria de testes e gerar os relatórios de regressão pelo terminal:

```bash
cd pathbit-academy-ai/0006_llm_evals_regressao

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python src/main.py --check  # verifica o launcher
python src/eval_runner.py --limit 3
```

Para inspecionar o ranking, os deltas por caso e as respostas de cada candidato, utilize o notebook:

```bash
jupyter notebook notebooks/llm_evals_regressao.ipynb
```

Ao término do processo, a pasta `data/` armazena todos os registros da esteira: `geracoes_evals.csv` com cada texto gerado e suas respectivas notas, `candidate_summary.csv` consolidando as médias por modelo, `regressoes_detectadas.csv` listando todos os deltas negativos apurados e `relatorio_evals.md` sintetizando a decisão final do gate.

---

## Próximos passos na jornada de IA da Pathbit Academy

Dominar a avaliação e os gates de regressão garante a previsibilidade de modelos pontuais de resposta. O passo seguinte na maturidade de inteligência artificial envolve conceder autonomia ao modelo para decidir quais ações tomar no mundo real, orquestrando ferramentas corporativas e navegando em árvores dinâmicas de decisão.

No [Artigo 0007 (Agentes e Tool Calling)](https://github.com/pathbit/pathbit-academy-ai/blob/master/0007_agentes_tool_calling/article/ARTICLE.md), exploramos como desenhar agentes inteligentes com planners constrangidos, guardrails de segurança determinísticos e recuperação contextual, mantendo o controle total sobre efeitos colaterais e custos de execução.

---

## Referências

- [Zheng, Lianmin et al.: Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (NeurIPS 2023)](https://arxiv.org/abs/2306.05685)
- [Es, Shahul et al.: Ragas (Automated Evaluation of Retrieval Augmented Generation)](https://arxiv.org/abs/2309.15217)
- [Ribeiro, Marco Tulio et al.: Beyond Accuracy (Behavioral Testing of NLP Models with CheckList - ACL 2020)](https://arxiv.org/abs/2005.04118)
- [Lin, Chin-Yew: ROUGE (A Package for Automatic Evaluation of Summaries)](https://aclanthology.org/W04-1013/)
- [Documentação oficial da biblioteca Hugging Face Evaluate](https://huggingface.co/docs/evaluate)

---

Repositório oficial no GitHub no endereço https://github.com/pathbit/pathbit-academy-ai no módulo 0006_llm_evals_regressao.

#InteligenciaArtificial #LLMEvals #TestesDeRegressao #QA #DevOps #Python #EngenhariaDeSoftware #PathbitAcademy
