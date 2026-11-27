# Uma citação verdadeira pode sustentar a afirmação errada

O verificador confere o ID e a ocorrência literal de cada citação no contexto enviado. Se o trecho saiu do orçamento, o resultado é uma abstenção com `unknown_source`.

## Valide contra o contexto enviado

A entrada do verificador é a lista de trechos dentro do envelope efetivamente enviado, junto com afirmações simuladas. Cada afirmação precisa ter uma citação com `source_id` e `quote`. O identificador deve corresponder ao campo `id` de um trecho. A citação deve ocorrer literalmente no texto daquela fonte. IDs repetidos tornam ambígua a origem do trecho e são recusados.

| Caso | O que procurar no relatório |
| --- | --- |
| ID presente com texto literal | `citations_verified` |
| Texto citado contém uma alteração | `quote_not_found` |
| Fonte ficou fora do contexto | `unknown_source` |
| Uma afirmação chegou sem citação | `missing_citation` |

Uma falha devolve `abstained` e lista vazia de afirmações. O consumidor pode apresentar ausência de evidência ao usuário e guardar os motivos para diagnóstico. Valide o esquema da resposta antes de enviá-la ao verificador.

## Compare a origem com o significado

Rode `--case unsupported-claim`. O trecho «O estorno é solicitado pelo painel do pedido.» existe na fonte e a citação passa. A afirmação promete concluir a operação em cinco minutos. Onde pedir e quanto demorar são propriedades diferentes. Para verificar esse tipo de suporte, use um conjunto de afirmações avaliadas e uma etapa própria de avaliação ou revisão humana. No contrato da aplicação, nomeie o sucesso pela garantia observada: `citations_verified`.

## Faça o experimento no seu terminal

No laboratório, uma promessa de estorno em cinco minutos passa quando cita uma frase real sobre onde pedir. Execute `--case unsupported-claim` e veja por que procedência e suporte semântico precisam de verificações próprias.

[Artigo completo e notebook no GitHub](https://github.com/pathbit/pathbit-academy-ai/tree/master/0014_citacoes_verificaveis)

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
