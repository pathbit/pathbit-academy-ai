**Slide 1**
[layout: cover]
[eyebrow: Série 0009 · Saída estruturada]
[image: ../assets/01.png]
[caption: Três modos de geração, da instrução textual ao esquema.]

Do JSON que abre à decisão que pode seguir

Um erro 500 chegou ao suporte. O modelo respondeu com uma rota permitida pelo esquema, mas o atendimento precisava criar um chamado.

**Slide 2**
[layout: split]
[eyebrow: Quatro saídas controladas]
[image: ../assets/07_validacao_terminal.png]
[caption: Resultado esperado para entradas fixas que o leitor pode verificar sem inferência.]

Separe leitura, estrutura e política de atendimento

Observe a terceira linha. O parser lê o objeto, o validador aceita a estrutura e a política rejeita a escolha.

**Slide 3**
[layout: split]
[eyebrow: Ollama e JSON Schema]
[image: ../assets/01.png]
[caption: A aplicação valida o conteúdo interno do campo response.]

O formato muda o pedido

- Livre: instrução no prompt.
- JSON: format recebe a string json.
- Esquema: format recebe o objeto que descreve o contrato.

**Slide 4**
[layout: split]
[eyebrow: Dados históricos • 18 casos por modo]
[image: ../assets/03.png]
[caption: Parse, esquema e decisão reportados pelo laboratório.]

De 18 objetos válidos, oito seguiram o gabarito

O modo JSON entregou 16 saídas legíveis e nenhuma que atendia ao esquema. O modo com esquema entregou 18 objetos válidos e oito decisões esperadas.

**Slide 5**
[layout: split]
[eyebrow: Latência observada]
[image: ../assets/04.png]
[caption: Média consolidada, que pode somar uma segunda tentativa.]

Meça tentativas e tamanho de saída

Os modos tiveram durações diferentes, com comprimentos de saída diferentes e uma política de retry. Para avaliar a gramática, controle esses fatores em uma nova rodada.

**Slide 6**
[layout: cta]
[eyebrow: Exercício]
[gallery: ../assets/07_validacao_terminal.png, ../assets/03.png]

Escreva uma resposta válida que deve ser recusada

Troque apenas o valor da rota. Em seguida, acrescente um campo desconhecido e teste a regra additionalProperties. Cada falha pede um teste e um tratamento na aplicação.

> github.com/pathbit/pathbit-academy-ai
