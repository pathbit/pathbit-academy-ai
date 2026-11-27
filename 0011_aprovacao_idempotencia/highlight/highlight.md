**Slide 1**
[layout: cover]
[eyebrow: Série 0011 · Aprovação e idempotência]
[image: ../assets/01.png]
[caption: A proposta, a decisão e o chamado persistem em SQLite.]

Quando o agente pode agir?

Aprovação humana e idempotência no registro de chamados.

**Slide 2**
[layout: split]
[eyebrow: Série 0011 · Aprovação e idempotência]
[image: ../assets/02.png]
[caption: Saída local de um pedido em base nova.]

A aprovação vincula dados e decisão

O executor recusou o comando antes da aprovação e voltou com o mesmo ID após o reenvio.

**Slide 3**
[layout: split]
[eyebrow: Série 0011 · Aprovação e idempotência]
[image: ../assets/03.png]
[caption: A consulta preserva os dados aprovados.]

Uma chave identifica um efeito específico

Informar outro título ou outra prioridade para a mesma chave conflita com a proposta existente.

**Slide 4**
[layout: split]
[eyebrow: Série 0011 · Aprovação e idempotência]
[image: ../assets/04.png]
[caption: IDs devolvidos pelos dois processos e contagem SQL.]

Dois processos retornam o mesmo chamado

A transação e a restrição de unicidade deixam um único registro. Para um fornecedor externo, leve a chave até o serviço que realiza o efeito.
