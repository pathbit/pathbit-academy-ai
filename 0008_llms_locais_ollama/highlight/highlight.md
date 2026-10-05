**Slide 1**
[layout: cover]
[eyebrow: Série 0008 · LLMs Locais]
[image: ../assets/02.png]
[caption: Ollama em Docker com volume de modelos e API local.]

Stack de IA sem nuvem, sem chave e sem custo por token

Este módulo prova, com números medidos na própria máquina, que modelos pequenos em Docker atendem roteamento, extração e retrieval sem nenhuma chamada externa.

**Slide 2**
[layout: split]
[eyebrow: Por que local]
[image: ../assets/01.png]
[caption: Comparativo entre caminho de chamada na nuvem e no local.]

Local não é só economizar

A latência de rede vira loopback, o custo por token vira memória da máquina, o dado nunca sai do ambiente e a versão do modelo fica congelada no container.

> Com modelo local, o benchmark compara alvos fixos.
> Com API de nuvem, o alvo se move toda semana.

**Slide 3**
[layout: split]
[eyebrow: Infraestrutura mínima]
[image: ../assets/02.png]
[caption: Container, volume nomeado e porta local.]

Três blocos resolvem o infraestrutura

Ollama em container, modelos abertos em volume persistente e um cliente HTTP em Python padrão. Sem SDK, sem conta, sem cartão.

**Slide 4**
[layout: split]
[eyebrow: Medição honesta]
[image: ../assets/03.png]
[caption: TTFT, tokens de avaliação e vazão separados por camada.]

A latência que a nuvem esconde, aqui fica decomposta

Streaming token a token expõe o tempo até o primeiro token, a geração em si e a carga do modelo. O CSV registra cada linha para responder por que uma resposta demorou.

> Sem decomposição de latência, todo problema de performance vira opinião.

**Slide 5**
[layout: split]
[eyebrow: Benchmark medido]
[image: ../assets/04.png]
[caption: Comparativo real de três modelos pequenos em CPU: vazão, TTFT, JSON e tool.]

Modelo escolhe-se por função, não por fama

O 0.5B tem a maior vazão e planner 100% com JSON forçado. O llama3.2:1b tem o menor TTFT e devolveu JSON vazio nas 5 tentativas.

> Decodificação constrangida garante sintaxe, não conteúdo.

**Slide 6**
[layout: split]
[eyebrow: Contrato de saída]
[image: ../assets/04.png]
[caption: JSON forçado no Ollama com taxa de acerto por modelo.]

format: "json" tira o parsing da sorte

O planner do artigo 0007 dependia de JSON utilizável. O Ollama restringe a decodificação, e o laboratório mede quantas tentativas produzem JSON válido e tool correta.

**Slide 7**
[layout: split]
[eyebrow: Mesma instância, mais funções]
[image: ../assets/05.png]
[caption: Matriz de decisão de quando rodar local.]

Embeddings locais fecham o stack

O mesmo servidor entrega embeddings para o retrieval top-1. Um container cobre o que os artigos 0002, 0003 e 0007 usaram, sem chamada externa.

> Quando o dado não sai do ambiente, piloto sensível destrava na hora.

**Slide 8**
[layout: cta]
[eyebrow: O que este módulo entrega]
[gallery: ../assets/03.png, ../assets/04.png, ../assets/05.png]

Artigo completo + laboratório local de benchmarks

O repositório entrega runner, notebook, CSVs e relatório para provar o stack na sua própria máquina.

- Benchmark de chat, JSON e embeddings em um comando
- Evidência em CSV, gráfico e relatório markdown

> github.com/pathbit/pathbit-academy-ai
