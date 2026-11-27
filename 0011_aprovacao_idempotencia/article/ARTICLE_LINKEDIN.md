# O agente pode propor um chamado. Quem autoriza a criação?

Uma requisição pode gravar o chamado e perder a resposta. No laboratório, a aprovação fica ligada à proposta e o SQLite devolve o mesmo ID em duas execuções do mesmo pedido.

## Desenhe os estados antes da ferramenta

| Estado | Como chega nele | Efeito persistido |
| --- | --- | --- |
| `pendente` | O agente registra a proposta `pedido-42` | Título e prioridade para revisão |
| `aprovada` ou `rejeitada` | Uma pessoa registra a decisão | Decisão e identificador do operador |
| `executada` | O executor encontra uma proposta aprovada | ID de chamado ligado à proposta |

A interface de aprovação deve apresentar o conteúdo que será executado. No exemplo, a etapa `propor` recebe uma chave escolhida pelo cliente. Se `pedido-42` já aponta para outro título ou prioridade, a ferramenta retorna erro. Isso amarra a decisão ao conteúdo que o operador viu. Reenviar a mesma decisão com o mesmo operador recupera o estado salvo.

## Onde a idempotência é aplicada

A aprovação é consultada dentro da mesma transação que tenta inserir o chamado. A coluna `chamados.pedido` tem `UNIQUE`, e o `INSERT ... ON CONFLICT(pedido) DO NOTHING` reaproveita a associação existente. A própria chave do pedido permite recuperar o resultado após um timeout, inclusive em outra execução da CLI. Os comandos usam `BEGIN IMMEDIATE` para coordenar as escritas no SQLite. [Implementação do laboratório](https://github.com/pathbit/pathbit-academy-ai/blob/master/0011_aprovacao_idempotencia/src/main.py) · [Transações do SQLite](https://sqlite.org/lang_transaction.html).

## Faça o experimento no seu terminal

Rode uma execução pendente, uma aprovada e uma repetida. Observe `estado` e `chamado` em cada saída. A aprovação explica por que a execução pode acontecer. A chave do pedido explica por que ela não cria outra linha.

[Artigo completo e notebook no GitHub](https://github.com/pathbit/pathbit-academy-ai/tree/master/0011_aprovacao_idempotencia)

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
