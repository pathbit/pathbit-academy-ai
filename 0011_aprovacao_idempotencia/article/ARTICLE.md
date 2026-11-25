# Aprovação humana e idempotência em agentes

No [laboratório anterior](../../0010_mcp_local/article/ARTICLE.md), um planejador local descobre e chama ferramentas MCP. Agora a ferramenta cria um chamado que precisa sobreviver a reinícios, decisões humanas e novas tentativas da mesma operação.

## As três decisões do fluxo

| Etapa | Quem inicia | O que fica registrado |
| --- | --- | --- |
| Proposta | Automação ou operador | Identificador, título e prioridade do chamado |
| Revisão | Operador | Aprovação ou recusa e nome do operador |
| Execução | Cliente da ferramenta | Identificador do chamado criado para a proposta |

O executor lê o estado persistido no SQLite. Uma proposta sem decisão ou recusada permanece sem chamado. Se uma aprovação for reenviada com o mesmo operador, a decisão existente é devolvida. Depois de decidida, a proposta mantém o título, a prioridade e a decisão originais.

## A mesma operação pode chegar duas vezes

Imagine que o cliente perca a resposta depois de a gravação ser confirmada. Ao tentar novamente, ele reaproveita o identificador enviado na primeira requisição. A restrição `UNIQUE` na tabela de chamados permite um registro por proposta. A execução verifica a aprovação e insere o chamado na mesma transação. Uma nova tentativa devolve o registro existente, inclusive quando dois processos locais tentam executar ao mesmo tempo.

Se o cliente reutilizar a chave com outro título ou prioridade, a CLI recusa a solicitação. Assim, o operador consegue revisar um conteúdo estável entre a proposta e a execução.

## Reproduza o comportamento

O [guia de execução](../README.md) e o [notebook](../notebooks/aprovacao_idempotencia.ipynb) percorrem o fluxo com uma base temporária. Execute antes de aprovar, confirme a recusa da operação e repita a chamada depois de aprovar. O mesmo identificador de chamado deve aparecer nas duas últimas respostas.

## Até onde vai a garantia

O gravador realiza um efeito dentro do próprio SQLite. Em uma integração com um sistema de chamados externo, encaminhe uma chave de idempotência ao destino e preserve o vínculo entre a proposta e a resposta externa. Uma transação local cobre apenas as operações no banco local.

O nome do operador é um dado de demonstração. Um produto real precisa obter essa identidade de uma sessão autenticada e restringir a decisão a usuários autorizados.
