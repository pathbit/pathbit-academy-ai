**Slide 1**
[layout: cover]
[eyebrow: Série 0006 · LLM Evals]
[image: ../assets/01.png]
[caption: Ranking ponderado de candidatos com decisão final de release.]

Melhor score não basta para liberar deploy

Este módulo transforma LLM Evals em critério de release. Em vez de comparar respostas soltas, a esteira escolhe entre candidatos completos de inferência e reprova mudanças que abrem risco onde mais importa.

**Slide 2**
[layout: split]
[eyebrow: O dado que muda a conversa]
[image: ../assets/03.png]
[caption: Dataset com contexto, gabarito, categoria e criticidade por caso.]

Sem criticidade, a média engana

O dataset não tem só pergunta e resposta ideal. Ele carrega contexto, palavras críticas, categoria e criticidade para que erro operacional não pese igual a detalhe cosmético.

> Um caso crítico ruim vale mais
> do que um caso trivial bonito.

**Slide 3**
[layout: split]
[eyebrow: Como o score é calculado]
[image: ../assets/02.png]
[caption: Scorecard da avaliação separando dimensões técnicas antes do peso de risco.]

O score técnico mede aderência antes de ponderar risco

Cada resposta é julgada por similaridade semântica, `keyword_recall` e `faithfulness` ao contexto. Só depois disso a criticidade entra como peso e altera o ranking quando o caso é mais sensível.

**Slide 4**
[layout: split]
[eyebrow: O gate de release]
[image: ../assets/04.png]
[caption: Fluxo do gate combinando score ponderado e regressões críticas.]

Release gate olha ranking e regressão ao mesmo tempo

A decisão final não depende só do campeão da média. O runner calcula delta contra a baseline e procura regressões críticas antes de aprovar a mudança.

> Melhor candidato: `flan_estruturado` com 1.357.
> Gate atual: reprovado por 2 regressões críticas.

**Slide 5**
[layout: split]
[eyebrow: O ponto de maturidade]
[image: ../assets/01.png]
[caption: O score mais alto não virou deploy automático na esteira atual.]

O melhor resultado agregado não liberou produção

A baseline ponderada ficou em `0.932` e o melhor candidato abriu ganho de `0.425`. Mesmo assim, o release foi bloqueado porque o conjunto comparado criou risco em casos críticos.

Leaderboard bonito perde para política de release defensável.

**Slide 6**
[layout: split]
[eyebrow: Evidência suficiente]
[image: ../assets/05.png]
[caption: Artefatos produzidos pela esteira para leitura agregada, por categoria e por caso.]

Evals bom deixa rastro suficiente para revisão

A esteira gera `candidate_summary.csv`, `regressoes_detectadas.csv`, recortes por categoria, casos críticos e um relatório textual para explicar por que o deploy foi aprovado ou barrado.

**Slide 7**
[layout: split]
[eyebrow: O que muda para o time]
[image: ../assets/02.png]
[caption: Avaliação deixa de ser comparação rasa e vira governança de mudança.]

Comparar candidatos completos muda a discussão do time

Aqui o debate sai de "resposta A vs resposta B" e vira "qual combinação de modelo e prompt melhora o sistema sem esconder regressão operacional".

> Evals deixa de ser vitrine de qualidade
> e vira governança de mudança.

**Slide 8**
[layout: cta]
[eyebrow: O que este módulo entrega]
[gallery: ../assets/01.png, ../assets/03.png, ../assets/04.png]

Artigo completo + esteira pronta para rodar

O módulo entrega runner local, notebook, ranking por candidato, análise crítica e gate final documentado para discutir promoção de release com evidência.

- Artigo com leitura técnica do ranking
- Notebook e CSVs para revisão detalhada
- Harness de release com baseline e regressão

> github.com/pathbit/pathbit-academy-ai
