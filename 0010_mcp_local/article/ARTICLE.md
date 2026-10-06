# MCP Local com Ollama — O Protocolo Aberto para Ferramentas Sem Rede, Sem Chave e Sem Nuvem

A evolução dos agentes de inteligência artificial nos últimos anos esbarrou em um problema crônico de acoplamento de software: para cada modelo, framework ou provedor de nuvem, os desenvolvedores criavam adaptadores manuais para conectar ferramentas. Se você quisesse que o modelo consultasse uma base SQL, chamasse uma API de suporte ou executasse um script local, precisava reinventar a camada de serialização, os prompts de descrição de ferramentas e os tratamentos de erro.

Em 2024, a Anthropic publicou a especificação aberta do **Model Context Protocol (MCP)**. A promessa é direta: padronizar como modelos de linguagem interagem com ferramentas externas (*tools*), fontes de dados (*resources*) e instruções de sistema (*prompts*) sob um contrato único e universal.

No [artigo 0008](https://github.com/pathbit/pathbit-academy-ai/blob/master/0008_llms_locais_ollama/article/ARTICLE.md), provamos a execução de LLMs 100% locais via Ollama. No [artigo 0009](https://github.com/pathbit/pathbit-academy-ai/blob/master/0009_saida_estruturada/article/ARTICLE.md), demonstramos como o Grammar-Guided Sampling elimina alucinações de formato com schemas rígidos. 

Agora, no **artigo 0010 da Pathbit Academy**, unimos essas duas pontas: **conectamos um servidor MCP local via transporte `stdio` a modelos compactos locais**, fechando o ciclo agêntico com ferramentas corporativas isoladas, sem abrir uma única porta de rede e sem gastar um centavo em APIs de terceiros.

---

## 1. A Arquitetura do MCP Local com Transporte Stdio

Diferente de arquiteturas agênticas que dependem de microsserviços HTTP ou WebSockets expostos na máquina do desenvolvedor, o MCP local opera através do transporte padrão do sistema operacional: os descritores de arquivo padrão (`stdin` e `stdout`).

![Arquitetura MCP Local](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0010_mcp_local/assets/01.png)

> **Figura 1:** O Host inicia o Servidor MCP como subprocesso direto, trocando mensagens JSON-RPC 2.0 via pipes locais.

### Os Três Pilares da Arquitetura:
1. **Host Client (Agente Coordenador em Python):**
   Inicia a sessão assíncrona, conecta-se aos streams de entrada e saída do processo filho e controla o fluxo de dados.
2. **MCP Server (`mcp_server.py`):**
   Um subprocesso dedicado (`pathbit-suporte`) que expõe funções corporativas puras (consultas de políticas, abertura de tickets, busca de histórico). Ele não abre sockets de escuta e só se comunica com o processo que o instanciou.
3. **LLM Motor Local (Ollama em Docker):**
   Fornece a inferência para planejar a intenção e escolher os argumentos sob contrato estrito de JSON Schema.

### Por que o Transporte `stdio` é o Padrão Ouro para Ambientes Corporativos:
- **Zero Superfície de Ataque:** Como não há portas de rede abertas (nem mesmo em `localhost`), malwares ou processos secundários na máquina não conseguem interceptar requisições nem sondar endpoints.
- **Ciclo de Vida Determinístico:** Se o processo cliente morrer, o sistema operacional fecha automaticamente os pipes e o servidor MCP é encerrado sem deixar processos órfãos (*zombies*).
- **Zero Handshake:** Sem negociação TLS, sem resolução DNS e sem filas TCP.

---

## 2. Descoberta Dinâmica de Ferramentas (`list_tools`)

Em sistemas agênticos legados, quando uma nova ferramenta é criada no sistema, o desenvolvedor é obrigado a atualizar manualmente o prompt do sistema no cliente, reescrever esquemas e refazer o deploy do agente coordenador.

Com o MCP, o acoplamento é completamente desfeito:

![Descoberta Dinâmica de Ferramentas](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0010_mcp_local/assets/02.png)

> **Figura 2:** Handshake de inicialização: o cliente descobre o catálogo e os schemas das ferramentas em tempo de execução.

### O Fluxo no Código:
No servidor, decoramos as funções Python com `@mcp.tool()`:
```python
# src/mcp_server.py
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("pathbit-suporte")

@mcp.tool()
def buscar_politica(topico: str) -> str:
    """Busca uma política interna da empresa pelo tópico (devolucao, cancelamento, segunda_via)."""
    return POLITICAS.get(topico, f"Política '{topico}' não encontrada.")
```

No cliente, a sessão descobre dinamicamente os metadados e os converte no catálogo estruturado:
```python
# src/mcp_lab.py
async with stdio_client(params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        tools_response = await session.list_tools()
        
        catalogo = [
            {"nome": t.name, "descricao": t.description, "schema": t.inputSchema}
            for t in tools_response.tools
        ]
```

Se amanhã adicionarmos a ferramenta `consultar_fatura` no servidor MCP, o agente passa a utilizá-la imediatamente sem que seu código precise ser alterado.

---

## 3. O Loop Fechado do Agente Local com MCP

Integrando a saída estruturada do Artigo 0009 com a invocação MCP, fechamos o ciclo de execução completo:

![Loop Fechado do Agente Local](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0010_mcp_local/assets/03.png)

> **Figura 3:** O pipeline em 4 etapas: entrada do usuário, planejamento constrangido, invocação MCP e trilha de auditoria.

### 1. Injeção de Contexto no Prompt
O catálogo dinâmico descoberto é injetado no prompt do modelo:
```text
Você é o planner de um agente de suporte. Escolha a tool para a pergunta do cliente.
Tools disponíveis (catálogo descoberto via MCP):
- buscar_politica: Busca uma política interna da empresa pelo tópico
- criar_ticket: Abre um ticket de suporte técnico
- resumo_atendimento: Resume o histórico de atendimento de um cliente
- responder_direto: Use quando nenhuma tool se aplica

Pergunta do cliente: 'quero a segunda via da fatura deste mês'
Responda EXATAMENTE um JSON com "tool" e "argumentos".
```

### 2. Planejamento Constrangido com JSON Schema
Para evitar que o modelo alucine ferramentas inexistentes, passamos o schema de planejamento no parâmetro `format` do Ollama:
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

### 3. Invocação da Ferramenta via MCP
O agente executa a chamada com tipagem segura:
```python
resultado = await session.call_tool(
    plano["tool"],
    plano["argumentos"]
)
texto_resposta = resultado.content[0].text
```

> [!TIP]
> **Otimização Extrema com Modelos System 1 (Laya / Jev):** Quando a seleção de ferramentas não exige a redação de argumentos em texto livre complexo, o planner do agente pode ser delegado a um modelo **System 1** (apresentado no [Artigo 0009](https://github.com/pathbit/pathbit-academy-ai/blob/master/0009_saida_estruturada/article/ARTICLE.md)). O catálogo descoberto via `list_tools()` compõe diretamente a primitiva `Choice`, reduzindo o tempo de decisão de ~2.100 ms para meros **13 ms** — o que permite loops agênticos MCP locais em tempo real com menos de 20 ms de latência total!


---

## 4. Decomposição de Latência: Protocolo MCP vs Inferência

Um dos maiores receios ao adotar uma nova camada de abstração em arquiteturas de software é o impacto na latência de resposta.

Para responder a essa preocupação com rigor de engenharia, isolamos o protocolo MCP e executamos **50 chamadas consecutivas** de `call_tool()` diretamente pelo transporte `stdio`, sem inferência de modelo no caminho:

![Decomposição de Latência](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0010_mcp_local/assets/04.png)

> **Figura 4:** Medição de 50 chamadas de protocolo: a mediana de 1.15 ms demonstra overhead imperceptível.

### Métricas de Protocolo Medidas em CPU Local:
- **p50 (Mediana):** `0.99 ms`
- **p95 (Percentil 95):** `1.53 ms`
- **Média Global:** `1.05 ms`

### Benchmark Empírico do Planner por Modelo:

| Modelo | Validade do Plano (%) | Tool Correta (%) | Argumentos Válidos (%) | Latência Planner (ms) | Overhead MCP (ms) | Tokens Médios |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`llama3.2:1b`** | 100% | **83.3%** | 100% | 2.117 ms | 4.7 ms | 51.8 |
| **`qwen2.5:1.5b`** | 100% | 50.0% | 100% | 2.213 ms | 6.5 ms | 32.5 |
| **`qwen2.5:0.5b`** | 100% | 33.3% | 100% | 1.764 ms | 7.5 ms | 27.7 |

### O que esses números provam:
Enquanto a inferência de um modelo leve em CPU local consome entre **1.700 ms e 2.200 ms**, o ciclo completo de serialização JSON-RPC, envio pelo pipe, execução da lógica em Python e retorno consome menos de **5 milissegundos** no ciclo ponta a ponta (e apenas **0.99 ms** no teste puro de protocolo).

> **Conclusão de Performance:** O protocolo MCP adiciona menos de **0.25% de overhead** ao tempo total da requisição. O gargalo continuará sendo quase exclusivamente o tempo de inferência do LLM.


---

## 5. Governança, Menor Privilégio e Trilha de Auditoria

Em ambientes de produção corporativos, agentes de IA não podem operar como "caixas-pretas". Cada mutação de estado (abertura de ticket, estorno financeiro, alteração cadastral) precisa ser passível de auditoria regulatória.

![Governança Corporativa e Auditoria](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0010_mcp_local/assets/05.png)

> **Figura 5:** Menor privilégio, validação estrita e auditoria estruturada linha a linha.

### Padrão de Trilha de Auditoria (`mcp_resultados.csv`):
Nosso laboratório grava automaticamente cada decisão do ciclo agêntico em formato tabular:

```csv
modelo,consulta_id,repeticao,tool_escolhida,tool_esperada,acertou,argumento_ok,schema_ok,plan_ms,mcp_ms,tokens
qwen2.5:0.5b,q_fatura,0,buscar_politica,buscar_politica,True,True,True,841.2,1.15,38
qwen2.5:0.5b,q_incidente,0,criar_ticket,criar_ticket,True,True,True,912.4,1.22,42
qwen2.5:1.5b,q_devolucao,0,buscar_politica,buscar_politica,True,True,True,1140.6,1.08,36
```

Se um cliente reclamar que um chamado foi aberto com a prioridade errada, o log forense permite responder em segundos:
1. Qual modelo de linguagem gerou a decisão (`modelo`);
2. Qual prompt exato foi submetido (`consulta_id`);
3. Quanto tempo o modelo gastou planejando (`plan_ms`);
4. Quais argumentos foram repassados para a função MCP (`mcp_ms`).

---

## 6. Como Executar o Laboratório Localmente

### Opção 1: Executar o Laboratório Automatizado MCP
Certifique-se de que o container Ollama está em execução (módulo 0008):

```bash
# 1. Subir o Ollama se ainda não estiver rodando
cd pathbit-academy-ai/0008_llms_locais_ollama
docker compose up -d

# 2. Executar o laboratório MCP
cd ../0010_mcp_local
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Rodar o laboratório completo (descoberta, 50 chamadas de protocolo e plano agêntico)
python3 src/mcp_lab.py --repeat 2
```

Todos os dados serão gerados e persistidos em `data/`:
- `catalogo_tools.json`: Catálogo descoberto em runtime.
- `mcp_latencia_protocolo.json`: Métricas de latência do transporte stdio.
- `mcp_resultados.csv`: Auditoria linha a linha das chamadas agênticas.
- `mcp_relatorio.md`: Relatório executivo consolidado.

### Opção 2: Notebook Interativo
Abra o Jupyter Notebook para interagir com o servidor MCP e testar ferramentas manualmente:

```bash
python3 src/main.py
```

### Evidência de Execução do Notebook:
Abaixo, a comprovação visual da execução completa do notebook interativo com o handshake do servidor MCP, listagem dinâmica do catálogo de ferramentas e o ciclo completo de planejamento e chamada de função via stdio:

![Evidência de Execução do Notebook 0010](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0010_mcp_local/assets/evidence_notebook.png)

---


## 7. Conclusão da Trilogia de IA Local

Com este artigo, fechamos a trilogia fundamental de infraestrutura de inteligência artificial da Pathbit Academy:
1. **[0008 - LLMs Locais com Ollama](https://github.com/pathbit/pathbit-academy-ai/blob/master/0008_llms_locais_ollama/article/ARTICLE.md):** Prova de inferência e embeddings locais em Docker sem faturamento por token.
2. **[0009 - Saída Estruturada](https://github.com/pathbit/pathbit-academy-ai/blob/master/0009_saida_estruturada/article/ARTICLE.md):** Eliminação de fragilidade de parse via Grammar-Guided Sampling e JSON Schema.
3. **[0010 - MCP Local](https://github.com/pathbit/pathbit-academy-ai/blob/master/0010_mcp_local/article/ARTICLE.md):** Conexão padronizada, segura e governável com o mundo real através do Model Context Protocol.

Você tem agora em mãos uma fundação completa para construir agentes corporativos autônomos, resilientes, de baixíssimo custo e com privacidade absoluta de dados.

---

## Referências

- [Model Context Protocol (MCP) Specification — Anthropic](https://modelcontextprotocol.io/)
- [Python SDK Oficial do Model Context Protocol](https://github.com/modelcontextprotocol/python-sdk)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
