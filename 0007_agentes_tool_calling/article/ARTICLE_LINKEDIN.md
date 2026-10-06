# Agentes inteligentes e tool calling na prática: como conceder autonomia sem perder controle em produção

Demonstrações de agentes autônomos baseados em inteligência artificial costumam impressionar em apresentações comerciais porque ocultam deliberadamente as etapas mais desafiadoras da engenharia de software: governança de riscos, controle de efeitos colaterais, tratamento de falhas do planejador e rastreabilidade forense de decisões. Em um ambiente controlado, a interface conversa com naturalidade, uma ferramenta é disparada sem atritos e o resultado parece perfeito. No entanto, quando esse mesmo fluxo é submetido ao tráfego caótico de produção, a fragilidade dessa autonomia desprovida de limites manifesta-se em chamadas fantasmas de APIs, quebras de estado e custos descontrolados.

O desafio central ao projetar agentes corporativos não é conferir liberdade irrestrita ao modelo, mas construir barreiras determinísticas que contenham a incerteza probabilística da inferência. Um agente verdadeiramente pronto para produção opera sob uma arquitetura de defesa em profundidade, combinando filtros prévios de segurança, regras determinísticas de negócio, planejadores constrangidos em contratos estruturados, fallbacks semânticos e trilhas completas de auditoria.

Este artigo disseca a construção de um agente híbrido e observável executado integralmente em hardware local com modelos abertos. Demonstramos como desacoplar intenção, planejamento, execução e geração final, garantindo que o software tome decisões úteis sem expor a infraestrutura da organização a riscos operacionais desnecessários.

---

## O ponto de ruptura do fluxo determinístico

Muitos sistemas rotulados como agentes no mercado nada mais são do que fluxos rígidos de if e else disfarçados de inteligência artificial.

![Fluxo simples versus agente](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0007_agentes_tool_calling/assets/01.png)

> Figura 1. A evolução de fluxos rígidos para uma arquitetura agêntica com planejamento autônomo e observabilidade estrita.

Em uma automação convencional, a entrada do usuário é submetida a um conjunto estático de palavras-chave que ativa uma função previamente codificada. Embora esse padrão funcione para árvores de decisão simples, ele é incapaz de interpretar nuances coloquiais, decompor solicitações multifacetadas ou adaptar sua estratégia diante de respostas parciais de ferramentas externas.

A transição para um agente inteligente exige responder a requisitos arquiteturais complexos: como bloquear solicitações maliciosas antes de acionar a inteligência artificial, como economizar inferência em intenções óbvias, como garantir que o plano emitido pelo modelo seja parseável por sistemas de backend e como recuperar a execução quando o modelo alucinar parâmetros inexistentes.

---

## A infraestrutura enxuta do laboratório

Para provar que autonomia controlada não depende de faturamentos astronômicos em nuvens proprietárias, o laboratório deste módulo utiliza exclusivamente ferramentas abertas executadas em memória local de processo.

O modelo `Qwen2.5-0.5B-Instruct` é empregado para duas tarefas distintas: a etapa de planejamento estruturado (planner) e a síntese da resposta conversacional final. A biblioteca `sentence-transformers` com os pesos multilíngues do `paraphrase-multilingual-MiniLM-L12-v2` sustenta o roteamento semântico de intenções e a recuperação de documentos. Na camada de persistência local, catálogos em formato JSON padronizam o registro de ferramentas disponíveis, a base de conhecimento e os cenários reais de homologação.

Todo o ciclo opera sem chaves de API, sem autenticações externas e sem custos de tokens, garantindo repetibilidade absoluta em qualquer ambiente corporativo isolado.

---

## A cadeia de decisão antes da inferência probabilística

Em uma arquitetura de missão crítica, a inferência gerativa nunca deve ser o primeiro ponto de contato com o dado do usuário. A decisão começa restringindo o espaço de incerteza.

![Guardrails de segurança](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0007_agentes_tool_calling/assets/02.png)

> Figura 2. A esteira de triagem posicionando guardrails determinísticos e regras de negócio antes do acionamento do planner.

O primeiro escudo do pipeline é o guardrail de segurança. Essa camada determinística inspeciona a entrada em busca de padrões sensíveis como credenciais de acesso, tokens de API, números completos de cartão de crédito, chaves Pix ou tentativas explícitas de engenharia social reversa.

```python
def guardrail(texto: str) -> tuple[bool, str]:
    bloqueios = ["senha", "token", "cartao", "cpf completo", "pix", "segredo"]
    for bloqueio in bloqueios:
        if bloqueio in texto.lower():
            return False, f"Solicitacao bloqueada por seguranca: '{bloqueio}'"
    return True, "ok"
```

Se um termo proibido for detectado, o sistema interrompe o processamento imediatamente, devolvendo uma mensagem de recusa padronizada sem consumir um único ciclo de inferência neural.

O segundo escudo é a regra de negócio determinística. Solicitações recorrentes e óbvias, a exemplo de pedidos de segunda via de boleto, cancelamentos diretos ou relatos de erro interno 500, são encaminhadas instantaneamente para seus respectivos microsserviços via código convencional. Isso evita gastar tempo e processamento em cenários onde o caminho operacional já é perfeitamente conhecido.

---

## O planner sob contrato explícito de dados

Quando a solicitação supera os filtros iniciais e exige raciocínio contextual, o controle é transferido para o módulo planejador (planner).

![Tool calling na prática](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0007_agentes_tool_calling/assets/03.png)

> Figura 3. O planner gerando chamadas de ferramentas sob contrato estrito de dados validável pelo backend.

Em vez de permitir que o modelo responda em texto aberto, o prompt de sistema restringe a saída a um objeto JSON contendo três propriedades obrigatórias: o nome da ferramenta a ser acionada (`tool`), o parâmetro operacional a ser enviado (`argument`) e a justificativa lógica da escolha (`reason`).

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
                "Retorne EXATAMENTE um JSON com as chaves tool, argument e reason."
            ),
        },
    ]
```

Essa amarração sintática transforma a intenção do modelo em um contrato tipado, permitindo que a camada de integração valide os tipos antes de disparar qualquer requisição para serviços externos.

---

## O fallback semântico como rede de segurança

Modelos compactos de linguagem executados localmente podem, ocasionalmente, emitir JSON com aspas malformadas ou chaves fora de padrão. Em sistemas frágeis, essa falha de parse causaria uma exceção fatal.

O agente deste laboratório implementa uma rede de segurança semântica baseada em embeddings contínuos:

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

Se a tentativa de decodificação do JSON falhar, a esteira ativa o roteador semântico de fallback, calculando a similaridade de cosseno entre a mensagem do usuário e as descrições funcionais de cada ferramenta do catálogo. A ferramenta com maior afinidade vetorial é selecionada automaticamente, garantindo que o fluxo prossiga com estabilidade mesmo na ocorrência de ruído sintático.

---

## Desacoplamento entre recuperação, execução e síntese

Um dos maiores erros de design em agentes é misturar a tomada de decisão com a execução de efeitos colaterais e a formatação final do texto.

![Arquitetura mínima de agente](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0007_agentes_tool_calling/assets/04.png)

> Figura 4. Camadas desacopladas separando o planejamento estratégico da execução de ferramentas e da síntese final.

Na arquitetura proposta, se a ferramenta planejada for `buscar_politica`, o agente dispara uma busca semântica em uma base local de procedimentos e extrai o documento pertinente. Se a ferramenta escolhida for `criar_ticket`, o sistema aciona uma rotina observável que gera um identificador único de chamado, registra a prioridade e anexa o assunto sem depender da inferência neural.

Apenas após a coleta dos dados operacionais da ferramenta é que o modelo de linguagem é reativado para gerar a resposta amigável ao usuário, injetando o resultado da execução como contexto factual imutável.

---

## Governança através de trilha forense de auditoria

Autonomia sem rastreabilidade é inaceitável em ambientes corporativos sujeitos a conformidade regulatória.

![Casos ideais de uso](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0007_agentes_tool_calling/assets/05.png)

> Figura 5. Trilha forense de auditoria capturando cada transição de estado, ferramenta acionada e justificativa do agente.

A esteira registra cada passo do ciclo agêntico no arquivo `data/agent_audit_trail.csv`. Para cada interação do usuário, o sistema audita o texto original recebido, o status do guardrail de segurança, a decisão do planejador com seu payload JSON bruto, o caminho de execução utilizado (se houve acionamento normal, bypass de regra de negócio ou fallback semântico), a ferramenta invocada, o tempo de execução e a resposta final entregue.

Essa trilha permite que auditores e engenheiros inspecionem anomalias, identifiquem ferramentas que falham com frequência e depurem o comportamento do agente sem depender de suposições.

---

## Execução prática do laboratório passo a passo

O repositório disponibiliza todos os scripts, ferramentas mockadas e bases de conhecimento para testar o agente no seu próprio computador.

Para rodar a bateria de testes automatizada via terminal:

```bash
cd pathbit-academy-ai/0007_agentes_tool_calling

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python src/main.py --check
```

Para inspecionar visualmente as ativações de ferramentas, os bloqueios de guardrails e o arquivo de auditoria linha a linha, inicie o Jupyter Notebook interativo:

```bash
jupyter notebook notebooks/agentes_tool_calling.ipynb
```

A execução é puramente local e consome menos de um gigabyte de memória RAM em CPU convencional.

---

## Próximos passos na jornada de IA da Pathbit Academy

Com os princípios de planejamento agêntico, guardrails e observabilidade estabelecidos em memória de processo, surge a necessidade de desacoplar o motor de inferência em um servidor dedicado de alto desempenho, eliminando dependências de bibliotecas pesadas de Python e permitindo servir modelos de linguagem com métricas estritas de latência e consumo de hardware.

No [Artigo 0008 (LLMs Locais com Ollama)](https://github.com/pathbit/pathbit-academy-ai/blob/master/0008_llms_locais_ollama/article/ARTICLE.md), iniciamos a trilogia de infraestrutura avançada de IA local, demonstrando como empacotar e servir modelos abertos em containers Docker com custo marginal zero por token.

---

## Referências

- [Yao, Shunyu et al.: ReAct (Synergizing Reasoning and Acting in Language Models - ICLR 2023)](https://arxiv.org/abs/2210.03629)
- [Schick, Timo et al.: Toolformer (Language Models Can Teach Themselves to Use Tools - NeurIPS 2023)](https://arxiv.org/abs/2302.04761)
- [Anthropic: Building Effective Agents (Architectural Guidelines)](https://www.anthropic.com/research/building-effective-agents)
- [Wang, Lei et al.: A Survey on Large Language Model based Autonomous Agents](https://arxiv.org/abs/2308.11432)
- [Qwen Team: Qwen2.5 Function Calling and Agent Capabilities](https://qwenlm.github.io/)

---

Repositório oficial no GitHub no endereço https://github.com/pathbit/pathbit-academy-ai no módulo 0007_agentes_tool_calling.

#InteligenciaArtificial #AgentesAI #ToolCalling #ReAct #Qwen #Python #EngenhariaDeSoftware #PathbitAcademy
