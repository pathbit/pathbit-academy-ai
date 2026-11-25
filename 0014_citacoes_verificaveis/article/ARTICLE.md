# Citações verificáveis em respostas de RAG

[English](ARTICLE.en.md) · [Español](ARTICLE.es.md)

Um assistente de suporte pode citar a política certa com um texto alterado ou usar uma fonte que ficou de fora do contexto. O verificador recebe o envelope efetivamente enviado e um conjunto de afirmações com citações. Ele devolve evidências verificadas sobre essa entrada.

## Confira fonte e trecho

Cada afirmação precisa de pelo menos uma citação com `source_id` e `quote`. O identificador corresponde ao campo `id` de um trecho, e o texto citado deve estar literalmente no trecho. IDs duplicados tornam a origem ambígua e são recusados.

Quando alguma citação falha, a saída usa `abstained`, deixa a lista de afirmações vazia e conserva os motivos para diagnóstico. Assim, a interface pode oferecer uma resposta de abstenção e a equipe pode distinguir erro de fonte de erro de trecho.

| Caso | Resultado |
| --- | --- |
| Identificador e trecho correspondem ao contexto | `citations_verified` |
| Palavra alterada na citação | `quote_not_found` |
| ID presente apenas no índice, fora do contexto | `unknown_source` |
| Afirmação sem citações | `missing_citation` |

## Separe procedência e suporte semântico

O caso `unsupported-claim` associa um trecho real sobre onde abrir um estorno a uma promessa de cinco minutos. A verificação literal passa. O trecho descreve um local de solicitação, enquanto o prazo depende de outra evidência. Exponha esse limite no contrato da API e avalie suporte semântico separadamente com revisão humana ou uma etapa própria de avaliação de RAG.

## Exercício de ponta a ponta

Siga o [início rápido](../README.md) e passe ao verificador o relatório do [empacotador de contexto](../../0013_orcamento_contexto/README.md). No exemplo padrão, o trecho `refund-summary` cabe e a citação passa. Com 16 bytes, cabe apenas o envelope vazio e o mesmo ID resulta em `unknown_source`.

O laboratório usa respostas simuladas para exercitar o contrato de saída. Em um produto, valide o formato da resposta do modelo antes desta etapa e trate a abstenção como um resultado normal que a interface sabe apresentar.
