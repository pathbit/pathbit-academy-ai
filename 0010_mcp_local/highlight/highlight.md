**Slide 1**
[layout: cover]
[eyebrow: Série 0010 · MCP local]
[image: ../assets/06.png]
[caption: Saída real da descoberta e de duas chamadas stdio.]

A chamada funciona. E o efeito?

Uma sessão MCP pode completar mesmo quando a ferramenta recusa a operação no texto. No laboratório, o cliente reproduz isso sem Ollama.

**Slide 2**
[layout: split]
[eyebrow: Série 0010 · MCP local]
[image: ../assets/01.png]
[caption: Arquitetura da sessão MCP por stdin e stdout.]

Dois processos, dois caminhos

O cliente conversa com o servidor de ferramentas via pipes. O planejamento consulta Ollama por HTTP. As permissões do subprocesso dependem do ambiente.

**Slide 3**
[layout: split]
[eyebrow: Série 0010 · MCP local]
[image: ../assets/03.png]
[caption: No incidente preservado, um plano válido escolheu a ferramenta errada.]

Valide a forma, a escolha e o resultado

Os três modelos passaram na validação estrutural do recorte. A escolha da ferramenta variou de 4 a 10 acertos em 12 tentativas.

**Slide 4**
[layout: split]
[eyebrow: Série 0010 · MCP local]
[image: ../assets/04.png]
[caption: As medições têm escopos e estatísticas distintos.]

Meça cada etapa no recorte certo

Cinquenta chamadas a uma ferramenta fixa registraram p50 de 0,99 ms. A média de planejamento no experimento completo ficou entre 1.764,4 e 2.213,3 ms.
