**Slide 1**
[layout: cover]
[eyebrow: Série 0005 · Prompt Engineering]
[image: ../assets/04.png]
[caption: Benchmark comparando a matriz completa de estratégia e modelo.]

O prompt "melhor" não existe sem benchmark

Quando você compara estratégia e modelo ao mesmo tempo, prompt engineering deixa de ser opinião. O artigo mostra como medir ganho real antes de subir custo ou escalar stack.

**Slide 2**
[layout: split]
[eyebrow: O problema operacional]
[image: ../assets/01.png]
[caption: Resposta plausível ainda pode quebrar a operação quando não existe contrato de saída.]

Resposta plausível ainda pode quebrar a operação

Prompt genérico costuma convencer na leitura rápida. Quando a saída precisa virar interface de sistema, ele falha justamente onde o time depende de previsibilidade: resumo estável, prioridade confiável e próxima ação objetiva.

> Entender a mensagem não basta.
> A saída precisa funcionar como interface.

**Slide 3**
[layout: split]
[eyebrow: O desenho do laboratório]
[image: ../assets/02.png]
[caption: Framework em quatro camadas para separar instrução, formato e validação.]

O laboratório separa estratégia de capacidade do modelo

O runner cruza `Qwen/Qwen2.5-0.5B-Instruct` e `google/flan-t5-small` com quatro estratégias: `base`, `estruturado`, `few_shot` e `checklist`.

Isso permite responder de onde veio o ganho: do contrato de saída, do exemplo orientador, do checklist operacional ou do teto do próprio modelo.

**Slide 4**
[layout: split]
[eyebrow: O primeiro salto real]
[image: ../assets/03.png]
[caption: Comparativo entre instrução vaga e prompt com saída estruturada.]

Contrato de saída continua sendo o divisor de águas

O primeiro avanço não é escrever um prompt mais bonito. É exigir formato estável, com campos nomeados e estrutura mínima validável para o restante do sistema.

> Linguagem natural vira interface de sistema
> quando o formato deixa de ser implícito.

**Slide 5**
[layout: split]
[eyebrow: Medição séria]
[image: ../assets/04.png]
[caption: A matriz inteira roda no mesmo dataset e é julgada pelos mesmos critérios.]

Benchmark bom mede forma e significado ao mesmo tempo

O score final combina estrutura, keywords obrigatórias, acerto de prioridade e similaridade semântica. Isso evita duas ilusões comuns: texto bonito sem utilidade operacional, ou formato rígido com resposta semanticamente fraca.

**Slide 6**
[layout: split]
[eyebrow: Resultado observado]
[image: ../assets/06.png]
[caption: Leitura do benchmark multi-modelo com score total e delta sobre a baseline.]

O ganho muda com o modelo, não só com o prompt

> Qwen: `few_shot` 0.741 vs `base` 0.411, ganho de +80.2%.
> FLAN: `checklist` 0.460 vs `base` 0.266, ganho de +72.6%.

A leitura correta é simples: o mesmo prompt não rende igual em todo modelo.

**Slide 7**
[layout: split]
[eyebrow: Próximo passo certo]
[image: ../assets/05.png]
[caption: Escada de evolução técnica entre prompt engineering, RAG, fine-tuning e híbrido.]

Prompt ainda paga a conta, mas só até certo ponto

Se o problema é formato, instrução e consistência mínima, ainda há ganho barato na mesa. Quando o gargalo vira contexto atualizado ou comportamento especializado e persistente, aí a próxima conversa deixa de ser prompt e passa a ser RAG ou fine-tuning.

**Slide 8**
[layout: cta]
[eyebrow: O que este módulo entrega]
[gallery: ../assets/01.png, ../assets/04.png, ../assets/05.png]

Artigo completo + código para rodar localmente

No repositório, este módulo entrega artigo aprofundado, notebook, benchmark local, CSVs detalhados e leitura por delta contra baseline.

- Artigo com análise completa do experimento
- Notebook para inspecionar ranking e gráficos
- Runner local com artefatos auditáveis

> github.com/pathbit/pathbit-academy-ai
