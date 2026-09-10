# Prompt engineering na prática: como medir estratégia, modelo e ganho real antes de escalar custo

Prompt engineering costuma ser tratado como ajuste cosmético. Troca-se uma instrução, roda-se meia dúzia de exemplos e conclui-se que o sistema "melhorou". O problema é que esse ritual quase nunca separa duas coisas diferentes: ganho de engenharia de prompt e ganho de capacidade do modelo.

Este artigo parte do ponto em que essa ambiguidade começa a custar caro. Em vez de discutir prompt no abstrato, ele monta um laboratório comparativo que cruza estratégia de instrução com modelo de geração. A pergunta deixa de ser "qual prompt ficou mais bonito?" e passa a ser "qual combinação entrega o melhor resultado operacional e por quê?".

> Se você ainda não leu os artigos anteriores, vale revisar a sequência: [LLM vs LRM](https://github.com/pathbit/pathbit-academy-ai/blob/master/0001_llm_x_lrm/article/ARTICLE.md), [Embeddings e Vetorização](https://github.com/pathbit/pathbit-academy-ai/blob/master/0002_embeddings_vetorizacao/article/ARTICLE.md), [RAG e Vector Database](https://github.com/pathbit/pathbit-academy-ai/blob/master/0003_rag_vector_database/article/ARTICLE.md) e [RAG vs Fine-Tuning](https://github.com/pathbit/pathbit-academy-ai/blob/master/0004_rag_vs_finetuning/article/ARTICLE.md).

## O erro que parece inteligência, mas quebra a operação

![Prompt Engineering na prática](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0005_prompt_engineering_avancado/assets/01.png)

> Figura 1: Resposta plausível não basta quando o sistema precisa de campos estáveis para operar.

O erro mais comum em projetos com LLM é confundir entendimento semântico com prontidão para produção. Um modelo pode entender o problema do usuário e ainda assim devolver um texto que o backend não consegue consumir, o time não consegue priorizar e a operação não consegue transformar em próxima ação.

É por isso que prompt genérico costuma enganar. Lendo por cima, ele parece "bom o suficiente". Quando o cenário exige estrutura, prioridade e ação objetiva com repetibilidade, ele desaba.

## O laboratório que separa estratégia de capacidade do modelo

![Framework de prompt](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0005_prompt_engineering_avancado/assets/02.png)

> Figura 2: O laboratório cruza desenho de prompt com capacidade do modelo, em vez de isolar só uma dimensão.

O experimento deste artigo testa uma matriz `modelo x estratégia`.

Modelos gratuitos usados:

- `Qwen/Qwen2.5-0.5B-Instruct`
- `google/flan-t5-small`

Estratégias comparadas:

- `base`
- `estruturado`
- `few_shot`
- `checklist`

Esse desenho é o que torna a análise útil. Com ele, você consegue responder se a melhora veio do contrato de saída, do exemplo few-shot, do checklist operacional ou simplesmente do teto do modelo.

## O contrato de saída continua sendo o divisor de águas

![Comparativo de prompt](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0005_prompt_engineering_avancado/assets/03.png)

> Figura 3: Linguagem natural só vira interface de sistema quando o formato de saída deixa de ser implícito.

O ponto de inflexão do laboratório está no contrato de saída. A estratégia `estruturado` exige três linhas fixas, com nome de campo e conteúdo previsível:

```python
def structured_prompt(texto: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "Voce e um analista de atendimento da Pathbit. Responda sempre em portugues.",
        },
        {
            "role": "user",
            "content": (
                "Analise a mensagem e responda EXATAMENTE com 3 linhas.\n"
                "resumo: <uma frase>\n"
                "prioridade: <alta|media|baixa>\n"
                "proxima_acao: <uma frase objetiva>\n"
                f"Mensagem: {texto}"
            ),
        },
    ]
```

É uma mudança simples, mas estrutural. Ela transforma uma resposta aberta em uma interface mínima que dá para validar.

As outras estratégias empurram a mesma lógica em direções diferentes:

- `few_shot` adiciona um exemplo orientador no formato alvo;
- `checklist` injeta um raciocínio operacional explícito antes da resposta;
- `base` serve como referência do que acontece quando o formato é frouxo demais.

## O benchmark mede forma e significado ao mesmo tempo

![Benchmark de prompts](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0005_prompt_engineering_avancado/assets/04.png)

> Figura 4: A comparação só fica confiável quando toda a matriz é rodada no mesmo dataset e julgada pelos mesmos critérios.

O runner percorre todos os casos do dataset em todos os modelos e estratégias configurados:

```python
DEFAULT_GENERATION_MODELS = [
    "Qwen/Qwen2.5-0.5B-Instruct",
    "google/flan-t5-small",
]

strategies = {
    "base": generic_prompt,
    "estruturado": structured_prompt,
    "few_shot": few_shot_prompt,
    "checklist": checklist_prompt,
}
```

O julgamento também não fica no "parece melhor". O score final é a média de quatro dimensões:

- `score_estrutura`
- `score_keywords`
- `score_prioridade`
- `score_semantico`

```python
def evaluate_output(output: str, row: pd.Series, embedder: SentenceTransformer) -> dict[str, float]:
    score_structure = structure_score(output)
    score_keywords = keyword_score(output, row["required_keywords"])
    score_priority = priority_score(output, row["expected_priority"])
    score_semantic = semantic_score(embedder, output, row["expected_summary"])
    score_total = float(
        np.mean([score_structure, score_keywords, score_priority, score_semantic])
    )
    return {
        "score_estrutura": score_structure,
        "score_keywords": score_keywords,
        "score_prioridade": score_priority,
        "score_semantico": score_semantic,
        "score_total": score_total,
    }
```

Esse arranjo é importante porque impede duas distorções comuns:

- achar que uma resposta boa semanticamente já está pronta para produção;
- achar que uma resposta bem formatada, mas semanticamente pobre, já resolveu o problema.

## Como ler o resultado sem se enganar

![Leitura do benchmark real](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0005_prompt_engineering_avancado/assets/06.png)

> Figura 5: O ranking fica interessante quando mostra não só quem ganhou, mas como ganhou.

Os resultados observados nesta base deixam isso muito claro.

No `Qwen/Qwen2.5-0.5B-Instruct`, a melhor estratégia foi `few_shot`, com `0.741` de `score_total`, contra `0.411` da estratégia `base`. Isso representa um ganho de `+0.330` pontos, ou `+80.2%`.

No `google/flan-t5-small`, a melhor estratégia foi `checklist`, com `0.460`, contra `0.266` da `base`. O ganho foi de `+0.193` pontos, ou `+72.6%`.

O ponto relevante não é "few-shot sempre vence" ou "checklist sempre salva". O ponto é outro:

- no `Qwen`, `few_shot` e `estruturado` sobem forte porque o modelo consegue aproveitar melhor o contrato de saída;
- no `FLAN`, a semântica permanece razoável, mas o contrato rígido continua frágil, o que derruba estrutura e prioridade;
- `checklist` não é um passe mágico: no `Qwen`, ele melhora estrutura e prioridade, mas perde bastante em semântica no conjunto atual.

Isso é exatamente o tipo de leitura que um benchmark linear, rodando um único prompt em um único modelo, não consegue entregar.

## Os artefatos que tornam a comparação auditável

O laboratório não termina em um gráfico bonito. Ele gera artefatos que deixam a leitura reproduzível:

- `benchmark_resultados.csv` com cada execução por caso, estratégia e modelo;
- `benchmark_resumo.csv` com médias agregadas por combinação;
- `benchmark_deltas.csv` com delta absoluto e percentual contra a estratégia `base`;
- `benchmark_case_breakdown.csv` com detalhe por caso, descrição da estratégia e campos ausentes;
- `benchmark_relatorio.md` com leitura rápida do melhor resultado por modelo.

Esse conjunto faz diferença porque transforma prompt engineering em análise comparável. Você deixa de discutir preferência de escrita e passa a discutir evidência.

## Quando o prompt deixa de ser o próximo passo

![Escada de evolução](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0005_prompt_engineering_avancado/assets/05.png)

> Figura 6: Prompt melhora instrução e formato; RAG e fine-tuning entram quando o gargalo muda de natureza.

O artigo não tenta vender prompt como solução universal. O que ele mostra é até onde prompt ainda paga a conta.

Prompt engineering resolve bem:

- formato de saída;
- clareza de instrução;
- alinhamento operacional mínimo;
- consistência melhor do que um prompt livre.

Quando o problema passa a ser falta de contexto atualizado, entra RAG. Quando o problema passa a ser comportamento especializado e persistente, entra fine-tuning. A utilidade deste laboratório é justamente descobrir se você já chegou nesse ponto ou se ainda está deixando ganho barato na mesa.

## Show-Me-The-Code

O artigo entrega um laboratório comparativo que permite:

- testar dois modelos gratuitos no mesmo dataset;
- comparar quatro estratégias com o mesmo critério de julgamento;
- inspecionar score agregado, delta contra baseline e breakdown por caso;
- abrir o notebook para ranking visual ou rodar o script direto para gerar artefatos.

**Opção 1** Execute o laboratório localmente e gere os resultados no terminal.

[**Abrir README.md com instruções locais**](https://github.com/pathbit/pathbit-academy-ai/blob/master/0005_prompt_engineering_avancado/README.md)

**Opção 2** Abra o notebook e compare os resultados por estratégia e por modelo.

[**Abrir notebook de testes**](https://github.com/pathbit/pathbit-academy-ai/blob/master/0005_prompt_engineering_avancado/notebooks/prompt_engineering_avancado.ipynb)

## Próximos passos

Se você quiser endurecer esse laboratório sem perder o foco:

1. aumente o dataset com mais categorias de atendimento;
2. adicione modelos gratuitos com perfis diferentes;
3. use o `benchmark_case_breakdown.csv` para analisar falhas por estratégia, não só o score médio;
4. só suba para RAG ou fine-tuning depois de provar que o gargalo não é mais instrução.

O valor deste artigo não está no tamanho do modelo. Está na qualidade da comparação.

## Referências

- [Hugging Face - Qwen 0.5B Instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct)
- [Hugging Face - FLAN-T5](https://huggingface.co/google/flan-t5-small)
- [Sentence Transformers - Multilingual MiniLM](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)
