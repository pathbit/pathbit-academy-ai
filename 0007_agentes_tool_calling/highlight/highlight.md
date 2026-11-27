**Slide 1**
[layout: cover]
[eyebrow: Série 0007 · Agentes e tool calling]
[image: ../assets/06.png]
[caption: Cinco registros versionados mostram três caminhos.]

Quem escolheu a ferramenta?

Siga a solicitação do bloqueio inicial ao resultado da ferramenta e descubra qual decisão veio do planner.

**Slide 2**
[layout: split]
[eyebrow: Série 0007 · Agentes e tool calling]
[image: ../assets/02.png]
[caption: O registro mostra o ramo que termina antes da seleção.]

O código conhece intenções frequentes

Fatura segue para política. Erro 500 normalmente segue para chamado. Pedidos que combinam os dois revelam a ordem das regras.

**Slide 3**
[layout: split]
[eyebrow: Série 0007 · Agentes e tool calling]
[image: ../assets/03.png]
[caption: A aplicação decide qual ferramenta executa a partir da proposta.]

O plano é uma proposta

O parser exige strings. O roteador por embeddings pode propor uma rota quando o plano falha ou quando um score definido favorece outra ferramenta.

**Slide 4**
[layout: split]
[eyebrow: Série 0007 · Agentes e tool calling]
[image: ../assets/04.png]
[caption: Fluxo de roteamento, execução e síntese.]

Avalie a ação e a resposta separadamente

Confira ação esperada, documento recuperado, retorno e texto final. O chamado deste laboratório é simulado e não persiste em um sistema externo.
