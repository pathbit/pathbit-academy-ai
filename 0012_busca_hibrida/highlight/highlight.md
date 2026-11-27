**Slide 1**
[layout: cover]
[eyebrow: Série 0012 · Busca híbrida]
[image: ../assets/01.png]
[caption: Rankings obtidos usando o mesmo dataset de seis documentos.]

Acertar o primeiro resultado pode ser pouco

Busca lexical, similaridade vetorial e cobertura no corte final de um RAG.

**Slide 2**
[layout: split]
[eyebrow: Série 0012 · Busca híbrida]
[image: ../assets/02.png]
[caption: Valores de RRF calculados a partir dos rankings locais.]

A presença em duas listas muda a posição

Na busca RE42, um aviso genérico recebe duas contribuições da RRF. O alerta necessário recebe uma.

**Slide 3**
[layout: split]
[eyebrow: Série 0012 · Busca híbrida]
[image: ../assets/03.png]
[caption: A consulta RE42 tem dois documentos relevantes no gabarito.]

RR e Recall respondem perguntas diferentes

Com dois resultados híbridos, a política está em primeiro, mas o alerta ficou de fora. RR@2 é 1,0 e Recall@2 é 0,5.

**Slide 4**
[layout: split]
[eyebrow: Série 0012 · Busca híbrida]
[image: ../assets/04.png]
[caption: IDs de results extraídos das duas execuções da CLI.]

O corte 3 inclui o alerta

Inspecione candidatos e ordem final antes de aumentar o corte. O orçamento do gerador ainda pode excluir um dos trechos.
