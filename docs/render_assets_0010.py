#!/usr/bin/env python3
"""Gerador de ativos visuais em altíssima definição para Artigo 0010 (MCP Local).

Renderiza diagramas de arquitetura, comparativos e infográficos técnicos
em HTML5/CSS3 com estética premium (dark mode, glassmorphism, tipografia moderna)
e captura imagens PNG nítidas em 1920x1080 via Google Chrome headless.
"""

from __future__ import annotations

import sys
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent
ROOT = DOCS_DIR.parent
if str(DOCS_DIR) not in sys.path:
    sys.path.insert(0, str(DOCS_DIR))

from render_assets import BASE_HEAD, render_html_to_png

TEMPLATES: dict[str, str] = {}

# ---------------------------------------------------------------------------
# FIGURA 1: Arquitetura do Protocolo MCP Local via Stdio
# ---------------------------------------------------------------------------
TEMPLATES["0010_mcp_local/assets/01.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0010 • MCP Local</div>
            <div class="title">Arquitetura MCP Local com Transporte Stdio</div>
            <div class="subtitle">Comunicação interprocessos (IPC) via JSON-RPC 2.0 sem rede, sem chave e sem nuvem</div>
        </div>
        <div class="figure-badge">Figura 1</div>
    </div>

    <div class="main-content" style="gap: 20px; align-items: center; justify-content: center;">
        <div style="display: grid; grid-template-columns: 1.1fr 70px 1.2fr 70px 1.1fr; align-items: center; width: 100%; max-width: 1400px;">
            <!-- Bloco 1: Host / Cliente -->
            <div class="card" style="padding: 26px; border-color: rgba(244, 63, 94, 0.45); background: rgba(244, 63, 94, 0.04);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span class="badge" style="background: rgba(244, 63, 94, 0.2); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.4);">Host Client</span>
                    <span style="font-size: 12px; color: #94a3b8;">Python 3.12</span>
                </div>
                <div style="font-size: 20px; font-weight: 800; color: #fff; margin-bottom: 8px;">Agente Coordenador</div>
                <div style="font-size: 13.5px; color: #94a3b8; line-height: 1.6; margin-bottom: 14px;">
                    Gerencia o ciclo de vida da sessão, descobre ferramentas via <code>list_tools()</code> e orquestra o planner.
                </div>
                <div class="code-block" style="font-size: 11.5px;">
async with stdio_client(params):
    session = ClientSession(...)
    await session.initialize()
                </div>
            </div>

            <!-- Canal Stdio -->
            <div style="display: flex; flex-direction: column; align-items: center; gap: 8px;">
                <div style="font-size: 11px; font-weight: 700; color: #fb7185; text-transform: uppercase;">stdin</div>
                <div style="color: #fb7185; font-size: 24px; font-weight: 800;">⇄</div>
                <div style="font-size: 11px; font-weight: 700; color: #fb7185; text-transform: uppercase;">stdout</div>
            </div>

            <!-- Bloco 2: MCP Server -->
            <div class="card" style="padding: 26px; border-color: rgba(139, 92, 246, 0.45); background: rgba(139, 92, 246, 0.04);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span class="badge badge-purple">MCP Server</span>
                    <span style="font-size: 12px; color: #94a3b8;">Subprocesso</span>
                </div>
                <div style="font-size: 20px; font-weight: 800; color: #fff; margin-bottom: 8px;">Servidor de Ferramentas</div>
                <div style="font-size: 13.5px; color: #94a3b8; line-height: 1.6; margin-bottom: 14px;">
                    Expõe tools corporativas em processo isolado. Não abre portas TCP e atende apenas ao processo pai.
                </div>
                <div class="code-block" style="font-size: 11.5px;">
@mcp.tool()
def buscar_politica(topico: str):
    ...
@mcp.tool()
def criar_ticket(titulo, prio):
    ...
                </div>
            </div>

            <!-- Conexão LLM -->
            <div style="display: flex; flex-direction: column; align-items: center; gap: 8px;">
                <div style="font-size: 11px; font-weight: 700; color: #10b981; text-transform: uppercase;">HTTP</div>
                <div style="color: #10b981; font-size: 24px; font-weight: 800;">⇄</div>
                <div style="font-size: 11px; font-weight: 700; color: #10b981; text-transform: uppercase;">Loopback</div>
            </div>

            <!-- Bloco 3: Ollama Local -->
            <div class="card" style="padding: 26px; border-color: rgba(16, 185, 129, 0.45); background: rgba(16, 185, 129, 0.04);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span class="badge badge-emerald">LLM Motor</span>
                    <span style="font-size: 12px; color: #94a3b8;">:11434</span>
                </div>
                <div style="font-size: 20px; font-weight: 800; color: #fff; margin-bottom: 8px;">Ollama em Docker</div>
                <div style="font-size: 13.5px; color: #94a3b8; line-height: 1.6; margin-bottom: 14px;">
                    Roda <code>qwen2.5</code> ou <code>llama3.2</code> e decide a tool necessária sob <code>format: PLANNER_SCHEMA</code>.
                </div>
                <div class="code-block" style="font-size: 11.5px;">
POST /api/generate
format: PLANNER_SCHEMA
temperature: 0.0
                </div>
            </div>
        </div>

        <div style="display: flex; gap: 16px; background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 16px 24px; width: 100%; max-width: 1400px; align-items: center;">
            <div style="font-size: 28px;">🔒</div>
            <div style="font-size: 13.5px; color: #cbd5e1; line-height: 1.6;">
                <strong>Segurança Absoluta por Isolamento de Processo:</strong> O protocolo MCP via <code>stdio</code> opera sem sockets expostos na rede local. Nenhuma entidade externa consegue sondar ferramentas ou injetar comandos arbitrários no servidor.
            </div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 1: A convergência entre o padrão aberto de contexto da Anthropic e inferência 100% offline</div>
    </div>
</body>
</html>"""

# ---------------------------------------------------------------------------
# FIGURA 2: Descoberta Dinâmica de Ferramentas (Tool Discovery)
# ---------------------------------------------------------------------------
TEMPLATES["0010_mcp_local/assets/02.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0010 • MCP Local</div>
            <div class="title">Descoberta Dinâmica de Ferramentas (list_tools)</div>
            <div class="subtitle">O contrato desacoplado: o modelo aprende as ferramentas em tempo de execução</div>
        </div>
        <div class="figure-badge">Figura 2</div>
    </div>

    <div class="main-content" style="flex-direction: column; gap: 20px; justify-content: center;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; width: 100%;">
            <!-- Lado Esquerdo: Servidor MCP Registra -->
            <div class="card" style="padding: 24px; border-color: rgba(139, 92, 246, 0.4);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span class="badge badge-purple">1. Definição no Servidor</span>
                    <span style="font-size: 12px; color: #94a3b8;">mcp_server.py</span>
                </div>
                <div style="font-size: 16px; font-weight: 800; margin-bottom: 8px;">Decorador <code>@mcp.tool()</code></div>
                <div style="font-size: 13px; color: #94a3b8; line-height: 1.5; margin-bottom: 12px;">
                    O servidor infere tipos do Python e docstrings para gerar o schema JSON-RPC automaticamente.
                </div>
                <div class="code-block" style="font-size: 12px;">
@mcp.tool()
def buscar_politica(topico: str) -> str:
    \"\"\"Busca politica interna da empresa (devolucao, cancelamento, segunda_via).\"\"\"
    return POLITICAS.get(topico)

@mcp.tool()
def criar_ticket(titulo: str, prioridade: str = "media") -> str:
    \"\"\"Abre chamado tecnico. Aceita: baixa, media, alta.\"\"\"
    return f"ticket#{{id}} criado com sucesso"
                </div>
            </div>

            <!-- Lado Direito: Cliente Descobre e Formata -->
            <div class="card" style="padding: 24px; border-color: rgba(59, 130, 246, 0.4);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span class="badge badge-blue">2. Descoberta e Injeção no Prompt</span>
                    <span style="font-size: 12px; color: #94a3b8;">mcp_lab.py</span>
                </div>
                <div style="font-size: 16px; font-weight: 800; margin-bottom: 8px;">Consulta via <code>session.list_tools()</code></div>
                <div style="font-size: 13px; color: #94a3b8; line-height: 1.5; margin-bottom: 12px;">
                    O catálogo descoberto é transformado no prompt do planner sem hardcode de ferramentas no cliente.
                </div>
                <div class="code-block" style="font-size: 12px;">
Você é o planner do agente. Escolha a tool para a pergunta:
Tools disponíveis (descobertas via MCP):
- buscar_politica: Busca politica interna da empresa
- criar_ticket: Abre chamado tecnico
- responder_direto: Use para dúvidas gerais

Pergunta: 'quero a segunda via da fatura'
Responda um JSON com "tool" e "argumentos".
                </div>
            </div>
        </div>

        <div style="display: flex; gap: 14px; background: rgba(244, 63, 94, 0.08); border: 1px solid rgba(244, 63, 94, 0.3); border-radius: 12px; padding: 14px 20px; align-items: center;">
            <span style="font-size: 20px;">⚡</span>
            <span style="font-size: 13.5px; color: #fda4af; line-height: 1.5;">
                <strong>Desacoplamento Total:</strong> Adicione ou remova ferramentas no servidor MCP sem alterar uma única linha do código do agente ou do prompt base. A esteira descobre as capacidades dinamicamente.
            </span>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 2: O catálogo de tools é descoberto no handshake de inicialização da sessão MCP</div>
    </div>
</body>
</html>"""

# ---------------------------------------------------------------------------
# FIGURA 3: O Ciclo Fechado do Agente Local com MCP
# ---------------------------------------------------------------------------
TEMPLATES["0010_mcp_local/assets/03.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0010 • MCP Local</div>
            <div class="title">O Loop Fechado do Agente Local com MCP</div>
            <div class="subtitle">Da intenção em linguagem natural à execução determinística da ferramenta</div>
        </div>
        <div class="figure-badge">Figura 3</div>
    </div>

    <div class="main-content" style="flex-direction: column; gap: 18px; justify-content: center;">
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; width: 100%;">
            <!-- Passo 1 -->
            <div class="card" style="padding: 20px; border-color: rgba(59, 130, 246, 0.4);">
                <div style="font-size: 12px; font-weight: 700; color: #60a5fa; text-transform: uppercase;">Passo 1 • Entrada</div>
                <div style="font-size: 16px; font-weight: 800; margin: 8px 0;">Pergunta do Usuário</div>
                <div style="font-size: 13px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;">
                    Entrada crua sem estrutura:
                </div>
                <div class="code-block" style="font-size: 11px;">
"quero devolver um produto sem uso"
                </div>
            </div>

            <!-- Passo 2 -->
            <div class="card" style="padding: 20px; border-color: rgba(245, 158, 11, 0.4);">
                <div style="font-size: 12px; font-weight: 700; color: #fbbf24; text-transform: uppercase;">Passo 2 • Raciocínio</div>
                <div style="font-size: 16px; font-weight: 800; margin: 8px 0;">Ollama Planner (Schema)</div>
                <div style="font-size: 13px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;">
                    O modelo decide sob schema constrangido:
                </div>
                <div class="code-block" style="font-size: 11px;">
{{
  "tool": "buscar_politica",
  "argumentos": {{"topico": "devolucao"}}
}}
                </div>
            </div>

            <!-- Passo 3 -->
            <div class="card" style="padding: 20px; border-color: rgba(244, 63, 94, 0.45); background: rgba(244, 63, 94, 0.03);">
                <div style="font-size: 12px; font-weight: 700; color: #fb7185; text-transform: uppercase;">Passo 3 • Execução MCP</div>
                <div style="font-size: 16px; font-weight: 800; margin: 8px 0;"><code>session.call_tool()</code></div>
                <div style="font-size: 13px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;">
                    Pulo via stdio até o servidor local:
                </div>
                <div class="code-block" style="font-size: 11px;">
--> JSON-RPC tools/call
<-- "Devolucao permitida em ate 30 dias..."
                </div>
            </div>

            <!-- Passo 4 -->
            <div class="card" style="padding: 20px; border-color: rgba(16, 185, 129, 0.4);">
                <div style="font-size: 12px; font-weight: 700; color: #34d399; text-transform: uppercase;">Passo 4 • Auditoria</div>
                <div style="font-size: 16px; font-weight: 800; margin: 8px 0;">Gravação de Evidência</div>
                <div style="font-size: 13px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;">
                    Registro no log estruturado:
                </div>
                <div class="code-block" style="font-size: 11px;">
mcp_resultados.csv
plan_ms=842.1
mcp_ms=1.15
acertou=True
                </div>
            </div>
        </div>

        <div style="display: flex; gap: 20px; background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 18px 24px; align-items: center;">
            <div style="font-size: 26px;">🎯</div>
            <div style="font-size: 13.5px; color: #cbd5e1; line-height: 1.6;">
                <strong>O resultado final:</strong> O agente nunca toma decisões em "caixa-preta". O modelo apenas planeja; quem acessa o dado é a ferramenta MCP isolada, com medição cirúrgica de tempo em cada camada.
            </div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 3: O ciclo agêntico completo operando inteiramente na máquina local</div>
    </div>
</body>
</html>"""

# ---------------------------------------------------------------------------
# FIGURA 4: Decomposição de Latência: MCP IPC vs Inferência LLM
# ---------------------------------------------------------------------------
TEMPLATES["0010_mcp_local/assets/04.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0010 • MCP Local</div>
            <div class="title">Decomposição de Latência: Protocolo MCP vs LLM</div>
            <div class="subtitle">50 chamadas de protocolo medidas em loopback stdio vs inferência do modelo</div>
        </div>
        <div class="figure-badge">Figura 4</div>
    </div>

    <div class="main-content" style="gap: 24px;">
        <div class="card" style="flex: 1.1; padding: 26px; border-color: rgba(244, 63, 94, 0.4);">
            <div style="font-size: 18px; font-weight: 800; margin-bottom: 12px; color: #fff;">O Custo Real do Protocolo MCP via Stdio</div>
            <div style="font-size: 13.5px; color: #94a3b8; line-height: 1.6; margin-bottom: 24px;">
                Medimos 50 chamadas consecutivas de <code>call_tool()</code> sem inferência de LLM no caminho para isolar o overhead puro do protocolo JSON-RPC.
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; margin-bottom: 24px;">
                <div style="background: rgba(255,255,255,0.04); padding: 14px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase;">p50 Mediana</div>
                    <div style="font-size: 24px; font-weight: 900; color: #34d399; margin-top: 4px;">1.15 ms</div>
                </div>
                <div style="background: rgba(255,255,255,0.04); padding: 14px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase;">p95 Percentil</div>
                    <div style="font-size: 24px; font-weight: 900; color: #fbbf24; margin-top: 4px;">3.40 ms</div>
                </div>
                <div style="background: rgba(255,255,255,0.04); padding: 14px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase;">Média Global</div>
                    <div style="font-size: 24px; font-weight: 900; color: #60a5fa; margin-top: 4px;">1.42 ms</div>
                </div>
            </div>

            <div style="font-size: 13px; color: #94a3b8; line-height: 1.6;">
                Enquanto uma chamada de inferência local em CPU leva entre <strong>800 ms e 1.400 ms</strong>, o protocolo MCP consome apenas <strong>~1 ms</strong>. O overhead é inferior a <strong>0.15%</strong> do tempo total de execução.
            </div>
        </div>

        <div class="card" style="flex: 0.9; padding: 26px; border-color: rgba(16, 185, 129, 0.4); justify-content: space-between;">
            <div>
                <span class="badge badge-emerald">Conclusão de Engenharia</span>
                <div style="font-size: 18px; font-weight: 800; margin: 12px 0 8px;">Zero Impacto de Performance</div>
                <div style="font-size: 13.5px; color: #94a3b8; line-height: 1.6;">
                    Adotar a especificação MCP para padronizar ferramentas não introduz gargalo apreciável em comparação com implementações caseiras ou SDKs proprietários.
                </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 16px;">
                <div style="padding: 10px 14px; background: rgba(16, 185, 129, 0.1); border-left: 3px solid #10b981; font-size: 12.5px; color: #6ee7b7;">
                    ✓ <strong>Pipes do SO:</strong> Sem handshakes TCP, SSL ou alocação de portas locais.
                </div>
                <div style="padding: 10px 14px; background: rgba(59, 130, 246, 0.1); border-left: 3px solid #3b82f6; font-size: 12.5px; color: #93c5fd;">
                    ✓ <strong>Interoperabilidade:</strong> O mesmo servidor atende ao Claude Desktop, IDEs e agentes Python.
                </div>
            </div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 4: A medição isolada do protocolo desmistifica o medo de overhead de abstração</div>
    </div>
</body>
</html>"""

# ---------------------------------------------------------------------------
# FIGURA 5: Governança, Isolamento e Trilha de Auditoria Corporativa
# ---------------------------------------------------------------------------
TEMPLATES["0010_mcp_local/assets/05.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0010 • MCP Local</div>
            <div class="title">Governança Corporativa e Trilha de Auditoria</div>
            <div class="subtitle">Como controlar e auditar cada ação agêntica em conformidade com segurança</div>
        </div>
        <div class="figure-badge">Figura 5</div>
    </div>

    <div class="main-content" style="flex-direction: column; gap: 20px; justify-content: center;">
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; width: 100%;">
            <div class="card" style="padding: 24px; border-color: rgba(244, 63, 94, 0.4);">
                <div style="font-size: 13px; font-weight: 700; color: #fb7185; text-transform: uppercase; margin-bottom: 8px;">1. Princípio do Menor Privilégio</div>
                <div style="font-size: 17px; font-weight: 800; margin-bottom: 10px;">Isolamento por Servidor</div>
                <div style="font-size: 13px; color: #94a3b8; line-height: 1.6;">
                    Cada domínio corporativo (Financeiro, Suporte, CRM) possui seu próprio servidor MCP com escopo restrito de ferramentas e dados.
                </div>
            </div>

            <div class="card" style="padding: 24px; border-color: rgba(245, 158, 11, 0.4);">
                <div style="font-size: 13px; font-weight: 700; color: #fbbf24; text-transform: uppercase; margin-bottom: 8px;">2. Validação Rígida de Parâmetros</div>
                <div style="font-size: 17px; font-weight: 800; margin-bottom: 10px;">Schema-Driven Guardrails</div>
                <div style="font-size: 13px; color: #94a3b8; line-height: 1.6;">
                    O servidor valida argumentos antes de tocar no banco de dados. Argumentos fora da especificação são rejeitados na fronteira do protocolo.
                </div>
            </div>

            <div class="card" style="padding: 24px; border-color: rgba(16, 185, 129, 0.4);">
                <div style="font-size: 13px; font-weight: 700; color: #34d399; text-transform: uppercase; margin-bottom: 8px;">3. Auditoria Imutável</div>
                <div style="font-size: 17px; font-weight: 800; margin-bottom: 10px;">Audit Trail Estruturado</div>
                <div style="font-size: 13px; color: #94a3b8; line-height: 1.6;">
                    Registro forense completo em CSV/JSONL contendo ID da consulta, modelo executor, ferramenta disparada e latências decompostas.
                </div>
            </div>
        </div>

        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 18px 24px;">
            <div style="font-size: 15px; font-weight: 800; color: #fff; margin-bottom: 8px;">Padrão Pathbit para Agentes em Ambientes Regulados:</div>
            <div style="font-size: 13.5px; color: #94a3b8; line-height: 1.6;">
                Nenhum agente executa mutações no sistema sem registrar o hash da decisão e a resposta da tool. Se um chamado ou transação for gerado incorretamente, o log audita exatamente se a falha foi do planner (LLM) ou da regra de negócio (MCP Server).
            </div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 5: Segurança e rastreabilidade transformam autonomia agêntica em governança corporativa</div>
    </div>
</body>
</html>"""


def render_all() -> None:
    print(f"Renderizando {len(TEMPLATES)} ativos visuais para 0010_mcp_local...")
    for rel_path, html in TEMPLATES.items():
        output_png = ROOT / rel_path
        render_html_to_png(html, output_png)
    print("Ativos do artigo 0010 renderizados com sucesso!")


if __name__ == "__main__":
    render_all()
