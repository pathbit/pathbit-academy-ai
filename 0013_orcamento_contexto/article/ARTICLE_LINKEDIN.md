# Quais trechos chegam ao modelo quando o contexto tem limite?

Na pergunta sobre estorno, os dois documentos mais parecidos podem ser da mesma fonte. Uma cota por fonte abre espaço para um trecho de cobrança que responde à parte da pergunta sobre prazos.

## Meça aquilo que vai para a requisição

O exemplo conta os bytes de `{"documents":[...]}` depois de serializar JSON compacto em UTF-8. Cada entrada inclui `id`, `source` e `text`. Conta aspas, chaves, separadores e caracteres multibyte que aparecem em `estorno é solicitado`. O relatório externo inclui `bytes_used`, `context` e motivos de exclusão. A medida refere-se ao JSON interno que você obtém ao interpretar `context`.

Uma API de modelos normalmente limita tokens, e pode ter limites de payload também. Para planejar a produção, conte tokens com o tokenizer adequado à requisição completa, incluindo mensagens, instruções e ferramentas, e reserve espaço para a resposta. O laboratório usa bytes para repetir a mesma medição sem depender de um modelo.

## Use uma cota quando a mesma fonte domina

Os [trechos de exemplo](https://github.com/pathbit/pathbit-academy-ai/blob/master/0013_orcamento_contexto/data/context.json) são ordenados por relevância e desempate por ID. O empacotador verifica a cota de fonte, mede o envelope com o próximo trecho e registra `source_limit` ou `byte_budget` quando a inclusão falha. Um trecho curto no fim da lista ainda pode caber depois que um anterior ficou de fora.

| Teto e cota | Contexto que cabe | Bytes |
| --- | --- | --- |
| `245`, uma entrada por fonte | `refund-summary` e `refund-window` | 214 |
| `120`, uma entrada por fonte | `refund-summary` | Confira `bytes_used` no relatório |
| `245`, duas entradas por fonte | `refund-summary` e `refund-history` | 211 |

Na última linha, os dois trechos de `returns` deixam pouco espaço para `billing`. A redução de três bytes no resultado significa que os dois trechos escolhidos são menores juntos. Ela não indica melhora na cobertura da pergunta sobre prazos. Use a coluna de exclusões para explicar a decisão.

## Faça o experimento no seu terminal

No exercício, `245` bytes com cota de um preservam duas fontes. Aumentar a cota produz um pacote três bytes menor e perde a evidência de cobrança. Compare a seleção e os motivos do descarte antes de medir só o tamanho.

[Artigo completo e notebook no GitHub](https://github.com/pathbit/pathbit-academy-ai/tree/master/0013_orcamento_contexto)

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)
