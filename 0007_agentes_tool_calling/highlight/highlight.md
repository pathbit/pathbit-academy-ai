**Slide 1**
[layout: cover]
[eyebrow: Série 0007 · Agentes]
[image: ../assets/04.png]
[caption: Arquitetura com guardrail, planner, fallback, retrieval e auditoria.]

Agente bom não é o mais livre. É o mais governável

Este módulo mostra como dar autonomia sem perder controle: guardrail, regra de negócio, planner em JSON, fallback semântico, retrieval local e auditoria no mesmo fluxo.

**Slide 2**
[layout: split]
[eyebrow: Quando agente faz sentido]
[image: ../assets/01.png]
[caption: Comparativo entre pipeline fixo e agente autônomo com objetivo variável.]

O problema começa quando if/else já não basta

Fluxo fixo resolve o previsível. Agente entra quando a rota depende do contexto do pedido, mas ainda precisa operar com limite claro, ferramenta definida e trilha revisável.

> Autonomia útil não é improviso.
> É decisão com restrição.

**Slide 3**
[layout: split]
[eyebrow: Contenção de risco]
[image: ../assets/03.png]
[caption: Guardrail bloqueando ação arriscada antes de qualquer execução.]

Guardrail e regra de negócio vêm antes do planner

Pedido sensível nem chega ao passo de geração. Intenção óbvia pode seguir rota determinística sem desperdiçar inferência, o que reduz risco e estabiliza o comportamento onde a resposta certa já é conhecida.

**Slide 4**
[layout: split]
[eyebrow: Planejamento observável]
[image: ../assets/02.png]
[caption: Roteamento híbrido com planner em JSON e fallback por embeddings.]

Planner sem contrato explícito continua sendo caixa-preta

O planner deste módulo precisa devolver JSON com `tool`, `argument` e `reason`. Quando esse contrato falha, o router por embeddings entra como fallback ou override.

> O agente não só age.
> Ele deixa evidência de por que escolheu agir.

**Slide 5**
[layout: split]
[eyebrow: Arquitetura em camadas]
[image: ../assets/04.png]
[caption: Retrieval, execução e auditoria ficam separados para tornar o comportamento revisável.]

Retrieval, execução e auditoria ficam em camadas separadas

Buscar política, abrir ticket e gerar resposta final são passos distintos. Essa separação evita um bloco opaco único e melhora teste, revisão e observabilidade.

**Slide 6**
[layout: split]
[eyebrow: Limite importante]
[image: ../assets/05.png]
[caption: Nem todo fluxo simples precisa virar agente.]

Nem todo problema merece agente

O próprio material mostra o limite: use agente quando há contexto variável, múltiplas ferramentas e auditoria relevante para o produto. Se o fluxo é fixo, a regra é simples e o risco é baixo, pipeline determinístico continua sendo a escolha melhor.

**Slide 7**
[layout: split]
[eyebrow: Evidência observada]
[image: ../assets/04.png]
[caption: A arquitetura suportada é maior do que a amostra atualmente persistida nos arquivos.]

Os artefatos atuais provam hoje, e o código suporta mais

Nos arquivos versionados, já dá para observar guardrail, `business_rule`, retrieval, ticket simulado, resposta final e auditoria.

> Planner, fallback, override e resposta direta ainda não aparecem em toda a amostra versionada.

**Slide 8**
[layout: cta]
[eyebrow: O que este módulo entrega]
[gallery: ../assets/01.png, ../assets/03.png, ../assets/04.png]

Artigo completo + simulador local do agente

O repositório entrega notebook, cenários, logs e CSVs para revisar planejamento, execução, retrieval e auditoria.

- Artigo e notebook para entender o fluxo
- Simulador local com logs e CSVs de auditoria

> github.com/pathbit/pathbit-academy-ai
