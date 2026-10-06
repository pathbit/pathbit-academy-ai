**Slide 1**
[layout: cover]
[eyebrow: Série 0009 · Saída Estruturada]
[image: ../assets/01.png]
[caption: Os três níveis de contrato entre LLMs e código corporativo.]

Saída Estruturada com LLMs: Do Prompt ao Schema Validado

Este módulo prova, com dados medidos em modelos locais, como sair do prompt ingênuo e garantir 100% de conformidade de schema sem quebra de parse no backend.

**Slide 2**
[layout: split]
[eyebrow: O problema da fragilidade]
[image: ../assets/01.png]
[caption: Três níveis: prompt livre, format json e json_schema.]

Prompt otimista não é contrato de engenharia

Pedir JSON no texto livre resulta em markdown fences, preâmbulos e chaves alucinadas. O `json.loads` quebra e derruba o pipeline de produção.

> Em produção corporativa, confiar em prompt livre para gerar JSON é assumir débito técnico no primeiro deploy.

**Slide 3**
[layout: split]
[eyebrow: Sob o capô]
[image: ../assets/02.png]
[caption: Logits masking guiado por Autômato de Estados Finitos.]

Grammar-Guided Sampling: máscara de logits em tempo real

O schema é compilado em uma máquina de estados finitos. A cada token gerado pelo modelo, tokens inválidos recebem probabilidade zero.

> O modelo não tem como errar a sintaxe: a máscara física impede qualquer token ilegal.

**Slide 4**
[layout: split]
[eyebrow: Evidência empírica]
[image: ../assets/03.png]
[caption: Comparativo medido: conformidade e assertividade nos 3 modos.]

Números medidos: de 55% a 100% de conformidade

No modo livre, quase 30% das chamadas sequer parseiam. Com `format: <schema>`, a conformidade salta para 100% e a assertividade de negócio atinge o teto.

> Schema estrito não engessa o modelo: ele concentra a probabilidade na semântica correta.

**Slide 5**
[layout: split]
[eyebrow: O custo do retry]
[image: ../assets/04.png]
[caption: Trade-off de latência: 200ms de schema vs 2x latência no retry.]

O mito do retry compensatório

Tentar consertar saída livre com novo prompt custa o dobro da latência. A imposição de schema adiciona overhead desprezível e resolve na 1ª tentativa.

> Retries devem tratar regras de negócio semânticas, nunca sintaxe quebrada.

**Slide 6**
[layout: split]
[eyebrow: Arquitetura de produção]
[image: ../assets/05.png]
[caption: Pipeline desacoplado do schema Pydantic ao barramento de eventos.]

Contrato desacoplado e tipagem estrita

O contrato em Pydantic/JSON Schema vira especificação única. O backend deserializa com garantia total e audita cada decisão em CSV/JSONL.

> A saída estruturada transforma um gerador probabilístico de texto em uma API determinística.

**Slide 7**
[layout: split]
[eyebrow: A fronteira System 1]
[image: ../assets/06.png]
[caption: Modelos de decisão rápida: Laya (Open-Source) e Jev (TypeSafe).]

Modelos System 1: Decisão Direta em ~30 ms

Por que gerar 40 tokens sequenciais se o sistema precisa apenas de uma decisão tipada? Modelos System 1 usam passada única (O(1)) para Choice, Score e Bool com mais de 50x de redução de latência.

> A separação moderna: decisões em System 1 (< 40ms) e redação rica em System 2.

**Slide 8**
[layout: cta]
[eyebrow: O que este módulo entrega]
[gallery: ../assets/02.png, ../assets/03.png, ../assets/06.png]

Saída Estruturada + Modelos System 1

Do prompt otimista à garantia formal via Grammar-Guided Sampling, com benchmarks empíricos em modelos locais.

- 100% de conformidade de schema sem quebra de parse
- Desacoplamento com Pydantic e JSON Schema estrito
- Avaliação empírica de decisores System 1 vs autoregressão

> github.com/pathbit/pathbit-academy-ai


