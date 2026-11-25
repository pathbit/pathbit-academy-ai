# Orçamento de contexto com medidas reproduzíveis

[English](ARTICLE.en.md) · [Español](ARTICLE.es.md)

A [busca híbrida](../../0012_busca_hibrida/README.md) entrega uma lista de candidatos. Antes de montar a requisição, é preciso decidir quais trechos cabem e registrar as exclusões. Neste laboratório, o teto é em bytes para permitir uma medida independente de fornecedor de modelo.

## Meça o payload que será enviado

O empacotador preserva o ID, a fonte e o texto. Ele serializa o envelope `{"documents":[...]}` como JSON compacto em UTF-8. O valor `bytes_used` inclui o envelope, chaves, vírgulas, escapes e caracteres multibyte como `ç`. Ele mede o campo `context` depois de decodificar o relatório externo. O relatório em si tem outros campos e outro tamanho.

Em uma aplicação com limite de tokens, conte a entrada inteira com o tokenizer do modelo. Inclua instruções, mensagens, ferramentas e reserva para a resposta. A contagem de bytes deste exercício mede o transporte do JSON.

## Escolha em ordem e registre a decisão

1. Ordene por relevância decrescente, com desempate pelo ID.
2. Aplique a cota por fonte antes de tentar encaixar o trecho.
3. Aceite o trecho se o JSON completo couber.
4. Continue percorrendo a lista após uma exclusão. Um candidato menor pode caber no espaço restante.

A entrada padrão tem quatro trechos. Com 245 bytes e cota de um por fonte, o empacotador inclui `refund-summary` e `refund-window`, totalizando 214 bytes. O histórico excede a cota da fonte e o apêndice excede o orçamento. Cada exclusão devolve um motivo distinto.

## Limites e exercício

Esta estratégia é gulosa pela pontuação. Um trecho comprido bem ranqueado pode ocupar espaço que acomodaria dois trechos menores. Em conjuntos grandes, serializar o JSON inteiro a cada tentativa também tem custo. Meça a cobertura de evidências obtida por unidade de orçamento antes de trocar o algoritmo.

No [início rápido](../README.md), reduza o limite para 120 bytes e veja o trecho de cobrança desaparecer. Aumente a cota para duas entradas e compare as exclusões. O [próximo laboratório](../../0014_citacoes_verificaveis/README.md) usa o contexto exportado para conferir as citações de uma resposta.
