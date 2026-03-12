# Agentes e tool calling na prática: como dar autonomia sem perder controle

Muita demo de agente parece convincente porque pula exatamente as partes que mais dão trabalho: controle de risco, recuperação de contexto, fallback quando o planner falha e trilha de auditoria para revisar o que aconteceu. A interface conversa bem, a tool dispara e a resposta volta redonda. O problema é que esse tipo de fluxo raramente aguenta o primeiro choque com operação real.

Este artigo parte do ponto em que um roteador de intenção já não basta mais. O exemplo implementa uma arquitetura híbrida com guardrail, regra de negócio, planner em JSON, roteamento semântico por embeddings, retrieval em base local e registro passo a passo de auditoria. O objetivo não é romantizar autonomia. É mostrar como limitar risco enquanto o sistema ainda decide.

> Se você vier do artigo anterior de [LLM Evals](https://github.com/pathbit/pathbit-academy-ai/blob/master/0006_llm_evals_regressao/article/ARTICLE.md), vai reconhecer a continuidade. Depois de medir candidatos e regressão, o próximo passo natural é perguntar como um agente decide, executa e deixa evidência suficiente para ser revisado.

## O ponto em que if/else para de bastar

![Fluxo simples versus agente](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0007_agentes_tool_calling/assets/01.png)

> Figura 1: A diferença relevante não é "ter conversa", mas conseguir decidir com restrição e observabilidade.

Grande parte do que é chamado de agente no mercado ainda é um fluxo determinístico disfarçado. A entrada bate em um conjunto de palavras-chave, escolhe uma função e retorna um texto final. Isso pode servir como MVP, mas não explica os problemas centrais de uma arquitetura com autonomia parcial.

Para ficar tecnicamente útil, o exemplo precisava responder a perguntas mais difíceis:

- como bloquear solicitações inseguras antes de qualquer ação;
- como evitar gastar inferência em intenções óbvias;
- como estruturar um plano parseável;
- como sobreviver quando esse plano não vem utilizável;
- como revisar o que aconteceu sem depender só da resposta final.

## O stack gratuito que sustenta a arquitetura

O agente usa três blocos principais:

- `Qwen/Qwen2.5-0.5B-Instruct` para planejamento e resposta final;
- `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` para router semântico e retrieval;
- `tool_registry.json`, `knowledge_base.json` e `cenarios.json` como base local observável.

Nada de API paga. Nada de serviço externo obrigatório. Tudo roda localmente.

## A cadeia de decisão começa antes do planner

![Guardrails de segurança](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0007_agentes_tool_calling/assets/03.png)

> Figura 2: O agente só fica interessante quando a decisão começa com restrição, não com geração.

Antes de qualquer planejamento, o runner aplica dois filtros práticos.

O primeiro é o `guardrail`, que barra pedidos sensíveis como senha, token, cartão, CPF completo e Pix:

```python
def guardrail(texto: str) -> tuple[bool, str]:
    bloqueios = ["senha", "token", "cartao", "cpf completo", "pix", "segredo"]
    for bloqueio in bloqueios:
        if bloqueio in texto.lower():
            return False, f"Solicitacao bloqueada por seguranca: '{bloqueio}'"
    return True, "ok"
```

O segundo é a regra de negócio determinística para intenções muito óbvias, como fatura, devolução, cancelamento, erro `500` e indisponibilidade. Isso evita gastar geração onde o caminho já é conhecido e deixa o sistema mais estável.

Essa ordem importa. O agente não começa decidindo livremente. Ele começa restringindo o espaço de decisão.

## O planner escolhe tool com contrato explícito

![Tool calling na prática](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0007_agentes_tool_calling/assets/02.png)

> Figura 3: Quando o planner precisa devolver JSON válido, tool calling deixa de ser só intenção implícita.

Quando a solicitação não cai em bloqueio nem em regra de negócio, entra o planner. O prompt pede uma saída estruturada com três chaves:

- `tool`
- `argument`
- `reason`

```python
def planner_prompt(entrada: str, tools: list[dict[str, str]]) -> list[dict[str, str]]:
    tool_lines = "\n".join(
        f"- {tool['name']}: {tool['description']} | argumento: {tool['argument_name']}"
        for tool in tools
    )
    return [
        {
            "role": "system",
            "content": "Voce e um planner de agente. Responda apenas com JSON valido.",
        },
        {
            "role": "user",
            "content": (
                "Escolha a melhor tool para a solicitacao abaixo.\n"
                "Tools disponiveis:\n"
                f"{tool_lines}\n\n"
                f"Solicitacao: {entrada}\n"
                'Retorne EXATAMENTE um JSON com as chaves "tool", "argument" e "reason".'
            ),
        },
    ]
```

Esse detalhe é o que separa um roteador implícito de um passo de planejamento observável. O plano vira payload validável, não apenas interpretação informal de texto.

## O fallback semântico impede falha frágil de parsing

Modelos pequenos nem sempre devolvem JSON limpo. Um agente que depende de uma única tentativa de parsing quebra cedo demais. Por isso, o código implementa uma segunda linha de defesa com embeddings:

```python
def route_with_embeddings(query: str, embedder: SentenceTransformer, tools: list[dict[str, str]]) -> tuple[str, float]:
    labels = [tool["name"] for tool in tools]
    descriptions = [tool["description"] for tool in tools]
    vectors = embedder.encode([query, *descriptions], normalize_embeddings=True)
    query_vector = vectors[0]
    tool_vectors = vectors[1:]
    scores = [float(np.dot(query_vector, vector)) for vector in tool_vectors]
    best_index = int(np.argmax(scores))
    return labels[best_index], float(scores[best_index])
```

O runner suporta três caminhos semânticos diferentes depois do planner:

- `planner` quando o JSON vem utilizável;
- `router_fallback` quando o plano não pode ser parseado;
- `router_override` quando o router semântico contradiz o planner com score suficiente.

Essa distinção é importante porque "ter fallback" e "mostrar fallback nos artefatos atuais" são coisas diferentes.

## Retrieval e execução continuam sendo etapas separadas

![Arquitetura mínima de agente](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0007_agentes_tool_calling/assets/04.png)

> Figura 4: Planejamento, execução e auditoria ficam em camadas diferentes para tornar o comportamento revisável.

Se a ação escolhida for `buscar_politica`, o agente faz retrieval na base local antes de gerar a resposta:

```python
def retrieve_policy(query: str, embedder: SentenceTransformer, knowledge_base: list[dict[str, str]]) -> tuple[dict[str, str], float]:
    documents = [entry["conteudo"] for entry in knowledge_base]
    vectors = embedder.encode([query, *documents], normalize_embeddings=True)
    query_vector = vectors[0]
    document_vectors = vectors[1:]
    scores = [float(np.dot(query_vector, vector)) for vector in document_vectors]
    best_index = int(np.argmax(scores))
    return knowledge_base[best_index], float(scores[best_index])
```

Se a ação for `criar_ticket`, o agente simula a abertura do chamado e devolve um payload observável com `ticket_id`, prioridade e assunto. Se a ação final cair em `resposta_direta`, ele usa a base local de capacidades do assistente como fonte.

Essa separação de camadas é importante porque evita misturar decisão, recuperação de contexto e resposta final em um único bloco opaco.

## O que os artefatos atuais mostram de fato

![Casos ideais de uso](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0007_agentes_tool_calling/assets/05.png)

> Figura 5: A maturidade do agente não está só na arquitetura suportada, mas na evidência concreta que ele deixa.

Nos arquivos gerados hoje nesta pasta, a evidência observada é a seguinte:

- `decision_summary.csv` registra decisões vindas de `business_rule` para `buscar_politica` e `criar_ticket`;
- `retrieval_summary.csv` mostra duas execuções de `buscar_politica`, com documento recuperado e `knowledge_score`;
- `agent_runs.csv` inclui um bloqueio por guardrail e três execuções operacionais bem-sucedidas;
- `agent_audit_log.jsonl` persiste a trilha serializada de cada cenário executado.

Isso significa que os artefatos versionados atualmente demonstram com clareza:

- guardrail em ação;
- regra de negócio em ação;
- retrieval em base local e abertura simulada de ticket;
- resposta final gerada a partir do resultado da tool;
- auditoria por cenário.

Ao mesmo tempo, o código suporta caminhos adicionais que não aparecem nos CSVs atualmente versionados:

- `planner`;
- `router_fallback`;
- `router_override`;
- `resposta_direta`.

Essa distinção é importante para não superprometer. A arquitetura implementada é maior do que a amostra persistida, e o artigo precisa tratar isso com precisão.

## A trilha de auditoria é o que impede a demo bonita de virar caixa-preta

O `agent_runs.csv` não registra apenas "qual tool foi chamada". Ele guarda contexto suficiente para revisão:

```text
entrada | planned_tool | acao | status | router_score | knowledge_score | documento | used_fallback | decision_source | plan_reason | resposta
```

E o `agent_audit_log.jsonl` preserva a sequência de passos internos de cada execução, incluindo guardrail, decisão, tool execution e prévia da resposta final.

É isso que torna o exemplo operacionalmente interessante. O agente não só responde. Ele deixa rastro.

## Show-Me-The-Code

O artigo entrega um agente local com:

- guardrail antes de qualquer execução;
- regra de negócio para intenções óbvias;
- planner em JSON com roteamento semântico como fallback e override;
- retrieval em base local para `buscar_politica`;
- resposta final gerada a partir do resultado da tool, com `agent_runs.csv`, `decision_summary.csv`, `retrieval_summary.csv` e `agent_audit_log.jsonl`.

**Opção 1** Execute o simulador localmente e acompanhe os cenários no terminal.

[**Abrir README.md com instruções locais**](https://github.com/pathbit/pathbit-academy-ai/blob/master/0007_agentes_tool_calling/README.md)

**Opção 2** Abra o notebook e acompanhe planejamento, execução, retrieval e auditoria passo a passo.

[**Abrir notebook de testes**](https://github.com/pathbit/pathbit-academy-ai/blob/master/0007_agentes_tool_calling/notebooks/agentes_tool_calling.ipynb)

## Próximos passos

Se você quiser endurecer essa base sem sair do stack gratuito:

1. execute todos os cenários do `cenarios.json` para persistir também o caminho de `resposta_direta`;
2. crie cenários que forcem `planner`, `router_fallback` e `router_override`;
3. adicione testes específicos para schema do plano e decisão de tool;
4. avalie a resposta final do agente com um judge local ou outra esteira de evals.

A diferença entre um agente chamativo e um agente útil está nesse detalhe: autonomia com restrição, contexto e auditoria.

## Referências

- [Hugging Face - Qwen 0.5B Instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct)
- [Sentence Transformers - Multilingual MiniLM](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)
- [OWASP - Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
