# O que acontece quando um agente executa a mesma ação duas vezes?

O exemplo da vez abre um chamado de suporte. A automação registra o que pretende fazer, o operador lê a proposta e decide, e o executor consulta a decisão persistida.

Se o cliente perder a resposta após o banco gravar o chamado, ele repete a operação com o mesmo identificador. Uma restrição de unicidade impede a criação de outro chamado para aquela proposta. Uma tentativa de reutilizar a chave com conteúdo diferente é recusada.

O laboratório roda em Python e SQLite. Ele separa três perguntas que às vezes aparecem juntas em um prompt: qual ação foi proposta, quem aprovou e qual efeito foi gravado.

O [artigo completo](ARTICLE.md) explica o fluxo, apresenta os comandos e delimita o que muda quando o efeito está em um sistema externo.
