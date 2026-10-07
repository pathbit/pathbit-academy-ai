**Slide 1**
[layout: cover]
[eyebrow: Série 0009 · Saída Estruturada]
[image: ../assets/01.png]
[caption: Os três níveis de contrato entre LLMs e código corporativo.]

Saída Estruturada com LLMs: Do Prompt ao Schema Validado

Este módulo prova, com dados medidos em modelos locais, como distinguir parse, schema e decisão correta. O consumidor continua validando timeout, truncamento e contrato.

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

O runtime usa o subconjunto de schema suportado para guiar a gramática. JSON aninhado não se reduz a uma FSM simples; valide a saída no consumidor.

> O modelo não tem como errar a sintaxe: a máscara física impede qualquer token ilegal.

**Slide 4**
[layout: split]
[eyebrow: Evidência empírica]
[image: ../assets/03.png]
[caption: Comparativo medido: conformidade e assertividade nos 3 modos.]

Dados preservados: forma válida não significa decisão correta

Livre: 0% parse. JSON: 88,9% parse e 0% schema. Schema: 100% conformidade e 44,4% acerto semântico. São 18 linhas consolidadas por modo, com até um retry.

> Schema estrito não engessa o modelo: ele concentra a probabilidade na semântica correta.

**Slide 5**
[layout: split]
[eyebrow: O custo do retry]
[image: ../assets/04.png]
[caption: Tempos consolidados e custo acumulado de retry.]

O mito do retry compensatório

Retries aumentam o custo de forma variável. Neste recorte, schema teve média de 400,5 ms e livre 3.007,7 ms; não é medição isolada de overhead nem SLA.

> Retries devem tratar regras de negócio semânticas, nunca sintaxe quebrada.

**Slide 6**
[layout: split]
[eyebrow: Arquitetura de produção]
[image: ../assets/05.png]
[caption: Pipeline desacoplado do schema Pydantic ao barramento de eventos.]

Contrato desacoplado e tipagem estrita

O contrato em Pydantic/JSON Schema vira especificação única. O backend valida ou rejeita a saída; isso não prova correção semântica ou conformidade regulatória.

> A saída estruturada transforma um gerador probabilístico de texto em uma API determinística.

**Slide 7**
[layout: split]
[eyebrow: A fronteira roteamento não generativo]
[image: ../assets/06.png]
O benchmark local mede embeddings e três rótulos; não executa modelos comerciais de decisão.

Modelos roteamento não generativo: Decisão Direta em ~30 ms

O benchmark local mede embeddings e três rótulos; não executa modelos comerciais de decisão.

> A separação moderna: decisões em roteamento não generativo (< 40ms) e redação rica em System 2.

**Slide 8**
[layout: cta]
[eyebrow: O que este módulo entrega]
[gallery: ../assets/02.png, ../assets/03.png, ../assets/06.png]

Saída Estruturada + Modelos roteamento não generativo

Do prompt otimista à garantia formal via Grammar-Guided Sampling, com benchmarks empíricos em modelos locais.

- 100% de conformidade no recorte, com validação no consumidor
- Desacoplamento com Pydantic e JSON Schema estrito
- Avaliação empírica de decisores roteamento não generativo vs autoregressão

> github.com/pathbit/pathbit-academy-ai


