# MCP Local com Ollama — O Protocolo Aberto para Ferramentas Sem Rede, Sem Chave e Sem Nuvem

A evolução dos agentes de inteligência artificial nos últimos três anos esbarrou em um problema crônico e bem conhecido da história da engenharia de software: **o acoplamento combinatorial $M \times N$**.

Se você quisesse conectar $M$ modelos de linguagem ou frameworks de agentes (LangChain, AutoGen, CrewAI, LlamaIndex, SDKs proprietários) a $N$ ferramentas corporativas (consultas SQL, chamadas de API interna, leitura de logs, automações de sistema), precisava escrever $M \times N$ adaptadores customizados. Cada integração exigia prompts artesanais de descrição de ferramentas, deserializadores manuais de JSON, tratamentos de erro ad-hoc e uma fragilidade monumental a cada atualização de biblioteca.

A indústria de software já resolveu esse mesmo problema antes. Nos anos 2010, conectar dezenas de editores de código (VS Code, Sublime, Vim, Emacs) a dezenas de compiladores (TypeScript, Rust, Python, Go) exigia centenas de plugins frágeis. A Microsoft resolveu o impasse criando o **Language Server Protocol (LSP)**: um contrato JSON-RPC padronizado que reduziu a complexidade de $M \times N$ para $M + N$.

Em novembro de 2024, a Anthropic publicou a especificação aberta do **Model Context Protocol (MCP)**. A promessa é exatamente ser o **LSP dos Agentes de IA**: uma camada universal e aberta que padroniza como modelos de linguagem descobrem e interagem com ferramentas (*tools*), fontes de dados (*resources*) e instruções de sistema (*prompts*).

No [Artigo 0008 da Pathbit Academy](https://github.com/pathbit/pathbit-academy-ai/blob/master/0008_llms_locais_ollama/article/ARTICLE.md), provamos a execução de LLMs 100% locais em Docker via Ollama. No [Artigo 0009](https://github.com/pathbit/pathbit-academy-ai/blob/master/0009_saida_estruturada/article/ARTICLE.md), demonstramos como o Grammar-Guided Sampling elimina alucinações de formato com schemas rígidos e como modelos System 1 decidem em sub-15ms.

Agora, no **Artigo 0010**, unimos essas pontas para fechar a Trilogia de Infraestrutura de IA Local: **conectamos um servidor MCP local via transporte `stdio` a modelos locais de inferência no Ollama**, viabilizando agentes corporativos autônomos e auditáveis, sem abrir uma única porta de rede, sem tráfego externo e sem gastar um centavo em APIs de terceiros.

---

## 1. A Anatomia da Especificação MCP: Os Três Pilares

O Model Context Protocol opera sobre a especificação **JSON-RPC 2.0**, estruturando a comunicação entre o Agente (Host/Client) e os Provedores de Contexto (MCP Servers) através de três primitivas fundamentais:

![Arquitetura MCP Local](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0010_mcp_local/assets/01.png)

> **Figura 1:** O Host inicia o Servidor MCP como subprocesso direto, trocando mensagens JSON-RPC 2.0 via pipes locais.

### 1. Ferramentas (*Tools*): Ações com Efeito Colateral
Funções executáveis invocadas pelo modelo para interagir com o ambiente externo (abrir tickets de suporte, executar consultas SQL, reiniciar containers, disparar alertas).
- O servidor MCP expõe o nome da ferramenta, uma descrição textual legível para a IA e uma especificação JSON Schema estrita dos argumentos esperados (`inputSchema`).
- O retorno é estruturado em blocos de conteúdo (`TextContent`, `ImageContent` ou `EmbeddedResource`).

### 2. Recursos (*Resources*): Dados de Leitura Passivos
Fontes de dados contextuais identificadas por URIs customizadas (ex: `suporte://politicas/devolucao` ou `file:///var/log/app.log`).
- Diferente das *tools*, os *resources* são puramente passivos (sem efeitos colaterais), funcionando como leitura de arquivos ou endpoints de documentação.
- O cliente pode listar recursos via `resources/list` e ler seu conteúdo binário ou textual via `resources/read`.

### 3. Prompts (*Prompts*): Templates Controlados pelo Servidor
Padrões de raciocínio e instruções pré-formatadas expostos diretamente pelo servidor MCP.
- Permite que a equipe responsável pelo domínio (ex: time de finanças ou suporte) versione e atualize as instruções de uso das ferramentas diretamente no servidor, sem que o cliente precise alterar seu código.

---

## 2. Por que o Transporte `stdio` é o Padrão Ouro de Segurança Corporativa

A especificação MCP prevê múltiplos transportes para a troca de mensagens JSON-RPC. Na nuvem ou em microsserviços distribuídos, o transporte comumente adotado é o **SSE (Server-Sent Events)** sobre HTTP. No entanto, para sistemas corporativos sensíveis, desktops de operadores e servidores on-premise, o transporte padrão e mais seguro é o **`stdio` (Standard Input / Standard Output)**.

| Critério de Engenharia | Transporte `stdio` (Process Pipes) | Transporte `SSE` (HTTP / WebSockets) |
| :--- | :--- | :--- |
| **Superfície de Rede** | **Zero portas abertas** (nem mesmo `localhost`) | Abre portas TCP (ex: 8080, 3000) |
| **Vulnerabilidade a Port Scan** | **Totalmente imune** (não existe socket TCP) | Suscetível a varredura interna e sniffing |
| **Isolamento de Credenciais** | O servidor MCP guarda segredos e expõe só funções | Tokens trafegam via headers HTTP |
| **Ciclo de Vida do Processo** | **Determinístico:** morre junto com o processo pai | Pode ficar órfão (*zombie process*) na máquina |
| **Latência de Transporte IPC** | **~0.99 ms** (pipes do kernel em memória) | ~5 a 25 ms (pilha TCP/IP, loopback network) |

### Como o `stdio` opera no Sistema Operacional:
1. O cliente (agente em Python) utiliza a chamada de sistema `fork()` e `exec()` para instanciar o servidor MCP como um subprocesso filho.
2. O sistema operacional cria dois pipes unidirecionais em memória RAM:
   - O descritor de arquivo `stdin` do processo filho é conectado ao canal de escrita do pai;
   - O descritor `stdout` do processo filho é conectado ao canal de leitura do pai.
3. Todas as mensagens JSON-RPC trafegam em memória de kernel através desses buffers. Se o processo pai for encerrado (por crash ou término natural), o kernel fecha os pipes, gerando um sinal `SIGPIPE` / `SIGTERM` que encerra o servidor MCP imediatamente, garantindo que nenhum processo fique rodando em segundo plano.

---

## 3. Descoberta Dinâmica de Ferramentas (`list_tools`)

Em sistemas agênticos legados, quando uma nova ferramenta de negócio era criada, o desenvolvedor do agente era obrigado a editar o prompt do sistema no cliente, atualizar schemas manuais e realizar um novo deploy do agente.

Com o MCP, o acoplamento é completamente desfeito através do **handshake de inicialização**:

![Descoberta Dinâmica de Ferramentas](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0010_mcp_local/assets/02.png)

> **Figura 2:** O cliente descobre o catálogo e os schemas das ferramentas em tempo de execução sem alterar código de cliente.

### O Protocolo JSON-RPC sob o Capô:

1. **`initialize` (Request do Cliente):**
```json
{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "pathbit-agent", "version": "1.0"}}}
```

2. **`initialize` (Response do Servidor):**
```json
{"jsonrpc": "2.0", "id": 1, "result": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "pathbit-suporte", "version": "1.0"}}}
```

3. **`tools/list` (Request do Cliente):**
```json
{"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
```

4. **`tools/list` (Response do Servidor com Schemas):**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "buscar_politica",
        "description": "Busca uma política interna da empresa pelo tópico.",
        "inputSchema": {
          "type": "object",
          "properties": {"topico": {"type": "string"}},
          "required": ["topico"]
        }
      }
    ]
  }
}
```

### Implementação do Servidor MCP em Python Puro:
No arquivo `src/mcp_server.py`, utilizamos o SDK oficial da Anthropic para expor as ferramentas de suporte:

```python
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("pathbit-suporte")

POLITICAS = {
    "devolucao": "Devolução permitida em até 30 dias corridos para produtos sem uso.",
    "cancelamento": "Cancelamento sem multa pode ser solicitado em até 7 dias corridos.",
    "segunda_via": "A segunda via da fatura é emitida no portal do cliente, aba Financeiro.",
}

@mcp.tool()
def buscar_politica(topico: str) -> str:
    """Busca uma política interna da empresa pelo tópico (devolucao, cancelamento, segunda_via)."""
    return POLITICAS.get(topico.lower().replace(" ", "_"), f"Política '{topico}' não encontrada.")

@mcp.tool()
def criar_ticket(titulo: str, prioridade: str = "media") -> str:
    """Abre um ticket de suporte técnico. Prioridades aceitas: baixa, media, alta."""
    if prioridade not in ("baixa", "media", "alta"):
        return f"Erro: prioridade inválida '{prioridade}'"
    return f"Ticket #2041 aberto com sucesso: '{titulo}' (prioridade {prioridade})"

if __name__ == "__main__":
    mcp.run()
```

Se amanhã a equipe de infraestrutura adicionar a tool `reiniciar_servico` ou `consultar_extrato` neste servidor, o agente passa a enxergá-la e utilizá-la no próximo handshake, sem que uma única linha de código do agente precise ser recompilada.

---

## 4. O Loop Fechado do Agente Local com MCP e Ollama

Integrando o servidor MCP com a saída estruturada do Artigo 0009 e os modelos locais do Artigo 0008, fechamos o ciclo agêntico completo em 4 etapas:

![Loop Fechado do Agente Local](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0010_mcp_local/assets/03.png)

> **Figura 3:** O pipeline em 4 etapas: entrada do usuário, planejamento constrangido, invocação MCP e trilha de auditoria.

### 1. Injeção de Contexto no Prompt do Planner
O catálogo descoberto via `session.list_tools()` é dinamicamente injetado no prompt de sistema:
```text
Você é o planejador de um agente de suporte. Escolha a tool para a pergunta do cliente.
Tools disponíveis (catálogo descoberto dinamicamente via MCP):
- buscar_politica: Busca uma política interna da empresa pelo tópico
- criar_ticket: Abre um ticket de suporte técnico
- resumo_atendimento: Resume o histórico de atendimento de um cliente
- responder_direto: Use quando nenhuma tool se aplica

Pergunta do cliente: 'quero a segunda via da fatura deste mês'
Responda EXATAMENTE um JSON com "tool" e "argumentos".
```

### 2. Planejamento Constrangido com JSON Schema Estrito
Para garantir que o modelo não alucine nomes de ferramentas inexistentes nem emita argumentos fora da tipagem, compilamos as ferramentas do catálogo em um JSON Schema estrito (mecanismo demonstrado no Artigo 0009) e o passamos no parâmetro `format` do Ollama:

```python
PLANNER_SCHEMA = {
    "type": "object",
    "properties": {
        "tool": {
            "type": "string",
            "enum": ["buscar_politica", "criar_ticket", "resumo_atendimento", "responder_direto"]
        },
        "argumentos": {"type": "object"}
    },
    "required": ["tool", "argumentos"]
}
```

### 3. Invocação Tipada da Ferramenta via MCP
O agente dispara a chamada através da sessão assíncrona do MCP:
```python
resultado = await session.call_tool(
    plano["tool"],
    arguments=plano["argumentos"]
)
conteudo_retorno = resultado.content[0].text
```

> [!TIP]
> **Aceleração com Modelos System 1 (Laya / Jev):** Quando a seleção de ferramentas não depende da redação de argumentos em texto livre prolixo, a etapa de planejamento pode ser delegada a um modelo **System 1** (apresentado no [Artigo 0009](https://github.com/pathbit/pathbit-academy-ai/blob/master/0009_saida_estruturada/article/ARTICLE.md)). O catálogo descoberto alimenta a primitiva `Choice`, reduzindo a decisão de ferramenta de ~2.100 ms para meros **13 ms** — o que viabiliza loops agênticos locais operando em tempo real com menos de 20 ms de latência total!

---

## 5. Decomposição Cirúrgica de Latência: Protocolo MCP vs Inferência

Um dos maiores receios da engenharia ao adotar uma nova camada de abstração em arquiteturas de microsserviços é o overhead de performance. Para responder a essa questão com rigor matemático, medimos **50 chamadas consecutivas de protocolo MCP** diretamente pelo transporte `stdio`, isolando a camada de transporte da inferência do modelo:

![Decomposição de Latência](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0010_mcp_local/assets/04.png)

> **Figura 4:** Medição real de 50 chamadas de protocolo isoladas no loopback: mediana de 0.99 ms demonstra overhead imperceptível.

### Métricas de Latência do Protocolo MCP Medidas em CPU Local (`data/mcp_latencia_protocolo.json`):
- **p50 (Mediana):** **`0.99 ms`**
- **p95 (Percentil 95):** **`1.53 ms`**
- **Média Global:** **`1.08 ms`**

### Benchmark Empírico do Planner por Modelo Local:

| Modelo | Validade Estrutural do Plano (%) | Acurácia de Escolha da Tool (%) | Argumentos Válidos (%) | Latência Média do Planner (ms) | Overhead do Protocolo MCP (ms) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`llama3.2:1b`** | **100%** | **83.3%** | **100%** | 2.117 ms | 4.7 ms |
| **`qwen2.5:1.5b`** | **100%** | 50.0% | **100%** | 2.213 ms | 6.5 ms |
| **`qwen2.5:0.5b`** | **100%** | 33.3% | **100%** | 1.764 ms | 7.5 ms |

### O que esses dados provam definitivamente:
Enquanto a inferência neural de um modelo compacto em CPU local consome entre **1.700 ms e 2.200 ms**, o ciclo completo de serialização JSON-RPC, envio pelo pipe `stdio`, execução da lógica em Python e retorno consome menos de **1 milissegundo** no protocolo puro (e menos de 7 ms no ciclo ponta a ponta com overhead de aplicação).

> **Conclusão de Performance:** O protocolo MCP adiciona menos de **0.25% de overhead** ao tempo total da requisição. Qualquer esforço de otimização deve focar na quantização do modelo ou na adoção de decisores System 1, e nunca no protocolo MCP.

---

## 6. Governança Corporativa e Trilha Forense de Auditoria

Em ambientes regulados (bancos, seguradoras, saúde), agentes de IA não podem operar como "caixas-pretas". Cada ação executada (abertura de ticket, mutação em banco de dados, emissão de documento) precisa gerar uma trilha de auditoria completa e imutável.

![Governança Corporativa e Auditoria](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0010_mcp_local/assets/05.png)

> **Figura 5:** Menor privilégio, validação estrita e auditoria estruturada linha a linha.

### O Padrão de Auditoria do Laboratório (`data/mcp_resultados.csv`):
Cada interação agêntica grava um registro tabular persistido em disco:

```csv
modelo,consulta_id,repeticao,tool_escolhida,tool_esperada,acertou,argumento_ok,schema_ok,plan_ms,mcp_ms,tokens
llama3.2:1b,q_fatura,0,buscar_politica,buscar_politica,True,True,True,1842.1,1.15,48
llama3.2:1b,q_incidente,0,criar_ticket,criar_ticket,True,True,True,2104.5,1.22,54
qwen2.5:1.5b,q_cancelamento,0,buscar_politica,buscar_politica,True,True,True,2250.2,1.08,39
```

Se um cliente abrir uma auditoria questionando por que um chamado foi categorizado com prioridade errada, o log forense permite responder em segundos:
1. Qual modelo exato tomou a decisão (`modelo`);
2. Qual prompt idêntico foi processado (`consulta_id`);
3. Quanto tempo o modelo gastou deliberando (`plan_ms`);
4. Quais argumentos foram injetados na ferramenta e quanto tempo a função MCP levou para responder (`mcp_ms`).

---

## 7. O que Quebra na Prática (Failure Modes)

Operar servidores MCP locais via `stdio` traz armadilhas específicas de sistemas operacionais:

### 1. A Armadilha do Buffering no `stdout` do Python
Por padrão, quando o Python detecta que a saída padrão não é um terminal interativo (TTY), ele ativa o buffering de bloco (geralmente de 4 KB ou 8 KB). O servidor MCP gera a resposta JSON-RPC, mas o buffer retém os bytes até encher, congelando o cliente em deadlock!
- **Solução de Engenharia:** Sempre execute o subprocesso com a variável de ambiente `PYTHONUNBUFFERED=1` ou passe `-u` no comando de inicialização (`python -u src/mcp_server.py`).

### 2. A Contaminação do Stream por `print()` de Debug
Se um desenvolvedor colocar um inocente `print("Iniciando busca...")` dentro de uma função MCP, essa string é escrita diretamente no descritor de arquivo `stdout`. O cliente espera uma linha JSON-RPC válida, tenta parsear a string e estoura uma exceção fatal de protocolo!
- **Solução de Engenharia:** Em servidores MCP via `stdio`, **toda e qualquer mensagem de log ou debug deve ser enviada estritamente para o `sys.stderr`** ou através do sistema de logs oficial do framework (`logging.getLogger()`).

---

## 8. Show-Me-The-Code: Executando o Laboratório Localmente

### Opção 1: Execução Automatizada pelo Terminal
Suba o servidor Ollama (conforme o Artigo 0008) e execute o laboratório MCP completo:

```bash
# 1. Navegue até o módulo
cd pathbit-academy-ai/0010_mcp_local

# 2. Configure o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Execute a bateria completa de testes
python src/mcp_lab.py --repeat 2
```

### Artefatos Gerados Automaticamente em `data/`:
- `catalogo_tools.json`: Catálogo de ferramentas e schemas descobertos em tempo de execução via `session.list_tools()`.
- `mcp_latencia_protocolo.json`: Métricas de telemetria das 50 chamadas de transporte stdio (p50 de 0.99 ms).
- `mcp_resultados.csv`: Trilha de auditoria forense linha a linha de cada decisão agêntica.
- `mcp_resumo.csv`: Consolidação de conformidade, acerto de ferramenta e latência por modelo.
- `mcp_relatorio.md`: Relatório executivo completo em Markdown.
- `mcp_comparativo.png`: Gráfico comparativo de latência do planner vs overhead do protocolo MCP.

### Opção 2: Notebook Interativo
```bash
python src/main.py
```

### Evidência de Execução Real:
Abaixo, a captura de tela comprovando a execução real do notebook interativo com o handshake do servidor MCP, listagem dinâmica do catálogo de ferramentas e o ciclo completo de planejamento e chamada de função via stdio:

![Evidência de Execução do Notebook 0010](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0010_mcp_local/assets/evidence_notebook.png)

---

## 9. Conclusão da Trilogia de Infraestrutura de IA Local

Com a conclusão deste artigo, a **Pathbit Academy** fecha a trilogia fundamental para construir sistemas de inteligência artificial soberanos, determinísticos e corporativos:

1. **[0008 — LLMs Locais com Ollama](https://github.com/pathbit/pathbit-academy-ai/blob/master/0008_llms_locais_ollama/article/ARTICLE.md):** Estabelecemos a infraestrutura de inferência e busca vetorial local em Docker com custo marginal zero.
2. **[0009 — Saída Estruturada e Modelos System 1](https://github.com/pathbit/pathbit-academy-ai/blob/master/0009_saida_estruturada/article/ARTICLE.md):** Blindamos a saída probabilística com Grammar-Guided Sampling (100% de conformidade de schema) e aceleramos decisões com decisores System 1 em passada única (~13 ms).
3. **[0010 — MCP Local via Stdio](https://github.com/pathbit/pathbit-academy-ai/blob/master/0010_mcp_local/article/ARTICLE.md):** Padronizamos a integração universal com ferramentas corporativas através de pipes seguros do sistema operacional com menos de 1 ms de overhead.

Você possui agora o conhecimento arquitetural, os dados empíricos e o código executável para levar agentes de IA para produção em escala, com independência total de fornecedores de nuvem, conformidade regulatória plena e previsibilidade máxima de engenharia.

---

## Referências Técnicas

- [Model Context Protocol Specification — Anthropic](https://modelcontextprotocol.io/)
- [Python SDK Oficial do Model Context Protocol](https://github.com/modelcontextprotocol/python-sdk)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
- [Language Server Protocol (LSP) Specification — Microsoft](https://microsoft.github.io/language-server-protocol/)
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/)
