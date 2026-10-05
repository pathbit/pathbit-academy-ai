**Slide 1**
[layout: cover]
[eyebrow: Série 0010 · MCP Local]
[image: ../assets/01.png]
[caption: Arquitetura MCP local com transporte stdio e Ollama.]

MCP Local: Model Context Protocol 100% Offline com Ollama

Este módulo conecta o protocolo aberto da Anthropic a um servidor local via stdio e modelos de inferência offline, provando ferramentas governáveis sem rede e sem chaves.

**Slide 2**
[layout: split]
[eyebrow: Por que MCP]
[image: ../assets/01.png]
[caption: Transporte por stdin/stdout elimina exposição de rede.]

O padrão aberto para conectar ferramentas a LLMs

Em vez de criar adaptadores manuais para cada framework, o Model Context Protocol padroniza ferramentas, recursos e prompts sob uma especificação universal.

> Com transporte stdio, o protocolo roda inteiramente dentro da máquina: zero portas TCP, zero tráfego externo.

**Slide 3**
[layout: split]
[eyebrow: Descoberta dinâmica]
[image: ../assets/02.png]
[caption: list_tools descobre ferramentas e schemas em tempo de execução.]

Desacoplamento total entre agente e ferramentas

O agente inicia a sessão e pergunta ao servidor quais tools estão disponíveis via `list_tools()`. As ferramentas entram no prompt do modelo sem código fixo.

> Você adiciona ou remove capacidades no servidor MCP sem alterar uma única linha do agente.

**Slide 4**
[layout: split]
[eyebrow: O ciclo completo]
[image: ../assets/03.png]
[caption: Loop fechado: pergunta, planner com schema, call_tool e auditoria.]

Do texto livre à ação real na máquina

A pergunta do usuário é processada pelo Ollama com schema rígido (artigo 0009). O plano resultante dispara a tool correspondente via `session.call_tool()`.

> O modelo apenas planeja a intenção; quem toca no dado é a ferramenta inspecionada.

**Slide 5**
[layout: split]
[eyebrow: Desempenho medido]
[image: ../assets/04.png]
[caption: 50 chamadas de protocolo: p50 de 1.15 ms vs 1.000 ms do modelo.]

Overhead do protocolo é inferior a 0.2%

Medimos 50 chamadas de protocolo isoladas: mediana de 1.15 ms. Comparado ao tempo de geração do modelo, o custo de adotar MCP é imperceptível.

> Padronização com MCP não compromete a performance da sua arquitetura agêntica.

**Slide 6**
[layout: split]
[eyebrow: Governança e auditoria]
[image: ../assets/05.png]
[caption: Audit trail completo em CSV/JSONL com menor privilégio por domínio.]

Auditoria forense e menor privilégio

Cada decisão agêntica, argumentos validados e tempos de execução são gravados em log estruturado. Em ambientes corporativos, auditoria é pré-requisito de deploy.

> Governança transforma autonomia probabilística em sistema confiável para produção.
