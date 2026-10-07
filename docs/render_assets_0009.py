#!/usr/bin/env python3
"""Gerador de ativos visuais em altíssima definição para Artigo 0009 (Saída Estruturada).

Renderiza diagramas de arquitetura, comparativos e infográficos técnicos
em HTML5/CSS3 com estética premium (dark mode, glassmorphism, tipografia moderna)
e captura imagens PNG nítidas em 1920x1080 via Google Chrome headless.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Adiciona o diretório atual ao path para importar render_assets
DOCS_DIR = Path(__file__).resolve().parent
ROOT = DOCS_DIR.parent
if str(DOCS_DIR) not in sys.path:
    sys.path.insert(0, str(DOCS_DIR))

from render_assets import BASE_HEAD, render_html_to_png

TEMPLATES: dict[str, str] = {}

# ---------------------------------------------------------------------------
# FIGURA 1: Os Três Níveis de Contrato com Modelos de Linguagem
# ---------------------------------------------------------------------------
TEMPLATES["0009_saida_estruturada/assets/01.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0009 • Saída Estruturada</div>
            <div class="title">Os Três Níveis de Contrato com LLMs</div>
            <div class="subtitle">Do prompt otimista à garantia matemática em tempo de amostragem de tokens</div>
        </div>
        <div class="figure-badge">Figura 1</div>
    </div>

    <div class="main-content" style="gap: 24px; align-items: stretch;">
        <!-- Nível 1 -->
        <div class="card" style="flex: 1; border-color: rgba(239, 68, 68, 0.35); background: rgba(239, 68, 68, 0.04); justify-content: space-between;">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <span class="badge" style="background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4);">Nível 1 • Livre</span>
                    <span style="font-size: 12px; color: #94a3b8; font-weight: 600;">Prompt Only</span>
                </div>
                <div style="font-size: 20px; font-weight: 800; color: #fff; margin-bottom: 8px;">Prompt Otimista</div>
                <div style="font-size: 13.5px; color: #94a3b8; line-height: 1.6; margin-bottom: 16px;">
                    O usuário apenas instrui no prompt: <em>"Responda apenas em formato JSON"</em>. O modelo gera texto aberto sem restrição formal.
                </div>
                <div class="code-block" style="font-size: 12px; margin-bottom: 14px;">
Com certeza! Aqui está o seu JSON:
```json
{{"acao": "buscar", "id": 42}}
```
Espero ter ajudado!
                </div>
            </div>
            <div style="padding: 12px; background: rgba(239, 68, 68, 0.1); border-radius: 8px; font-size: 12.5px; color: #fca5a5; line-height: 1.5;">
                <strong>Vulnerabilidade:</strong> Delimitadores de markdown (fences), preâmbulos conversacionais, quebra de parse no backend e chaves arbitrárias.
            </div>
        </div>

        <!-- Nível 2 -->
        <div class="card" style="flex: 1; border-color: rgba(245, 158, 11, 0.35); background: rgba(245, 158, 11, 0.04); justify-content: space-between;">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <span class="badge badge-amber">Nível 2 • Modo JSON</span>
                    <span style="font-size: 12px; color: #94a3b8; font-weight: 600;">format: "json"</span>
                </div>
                <div style="font-size: 20px; font-weight: 800; color: #fff; margin-bottom: 8px;">Sintaxe Garantida</div>
                <div style="font-size: 13.5px; color: #94a3b8; line-height: 1.6; margin-bottom: 16px;">
                    O motor obriga a saída a abrir e fechar chaves válidas. A sintaxe é 100% parseável, mas o schema interno permanece desgovernado.
                </div>
                <div class="code-block" style="font-size: 12px; margin-bottom: 14px;">
{{
  "ferramenta": "buscar_politica",
  "detalhes": null
}}
// ou até objeto vazio:
{{}}
                </div>
            </div>
            <div style="padding: 12px; background: rgba(245, 158, 11, 0.1); border-radius: 8px; font-size: 12.5px; color: #fcd34d; line-height: 1.5;">
                <strong>Armadilha:</strong> <code>json.loads()</code> não estoura exceção, mas faltam campos obrigatórios, tipos vêm trocados (string em vez de int) ou enums são alucinados.
            </div>
        </div>

        <!-- Nível 3 -->
        <div class="card" style="flex: 1; border-color: rgba(16, 185, 129, 0.45); background: rgba(16, 185, 129, 0.05); justify-content: space-between;">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <span class="badge badge-emerald">Nível 3 • JSON Schema</span>
                    <span style="font-size: 12px; color: #94a3b8; font-weight: 600;">format: &lt;schema&gt;</span>
                </div>
                <div style="font-size: 20px; font-weight: 800; color: #fff; margin-bottom: 8px;">Contrato Estrito</div>
                <div style="font-size: 13.5px; color: #94a3b8; line-height: 1.6; margin-bottom: 16px;">
                    Máscara de gramática em tempo de geração: campos exigidos, tipos primitivos estritos e enums finitos validados matematicamente.
                </div>
                <div class="code-block" style="font-size: 12px; margin-bottom: 14px;">
{{
  "tool": "buscar_politica",
  "confianca": 0.95
}}
// Impossível violar enum ou tipo!
                </div>
            </div>
            <div style="padding: 12px; background: rgba(16, 185, 129, 0.12); border-radius: 8px; font-size: 12.5px; color: #6ee7b7; line-height: 1.5;">
                <strong>Garantia de Produção:</strong> Validação em tempo de amostragem. Zero falhas de validação no backend e interoperabilidade determinística.
            </div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 1: A evolução do acoplamento entre modelos de linguagem e sistemas corporativos tipados</div>
    </div>
</body>
</html>"""

# ---------------------------------------------------------------------------
# FIGURA 2: Mecanismo de Decodificação Constrangida (Grammar-Guided Sampling)
# ---------------------------------------------------------------------------
TEMPLATES["0009_saida_estruturada/assets/02.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0009 • Saída Estruturada</div>
            <div class="title">Como Funciona a Decodificação Constrangida</div>
            <div class="subtitle">Grammar-Guided Sampling: máscara de logits via Autômato de Estados Finitos (FSM)</div>
        </div>
        <div class="figure-badge">Figura 2</div>
    </div>

    <div class="main-content" style="flex-direction: column; gap: 20px; justify-content: center;">
        <div style="display: grid; grid-template-columns: 1fr 60px 1.4fr 60px 1fr; align-items: center; width: 100%;">
            <!-- Passo 1 -->
            <div class="card" style="padding: 24px; border-color: rgba(59, 130, 246, 0.4);">
                <span class="badge badge-blue">Passo 1 • Predição LLM</span>
                <div style="font-size: 18px; font-weight: 800; margin: 12px 0 8px;">Cálculo dos Logits</div>
                <div style="font-size: 13.5px; color: #94a3b8; line-height: 1.5;">
                    A cada token gerado, a rede neural produz uma distribuição de probabilidades não normalizada (logits) sobre todo o vocabulário de ~150.000 tokens.
                </div>
                <div class="code-block" style="font-size: 11.5px; margin-top: 12px;">
"tool": [9.8],
"resposta": [8.4],
"Ol": [7.2],
"```": [6.1]
                </div>
            </div>

            <!-- Seta 1 -->
            <div style="display: flex; justify-content: center; color: #60a5fa; font-size: 28px; font-weight: 800;">→</div>

            <!-- Passo 2 -->
            <div class="card" style="padding: 24px; border-color: rgba(245, 158, 11, 0.4); background: rgba(245, 158, 11, 0.03);">
                <span class="badge badge-amber">Passo 2 • Validador de Gramática</span>
                <div style="font-size: 18px; font-weight: 800; margin: 12px 0 8px;">Máscara de Gramática (BNF / FSM)</div>
                <div style="font-size: 13.5px; color: #94a3b8; line-height: 1.5;">
                    O JSON Schema foi compilado em um Autômato de Estados Finitos. O autômato identifica o estado atual (ex: esperando o valor do enum <code>"tool"</code>).
                </div>
                <div style="margin-top: 12px; padding: 10px; background: rgba(245, 158, 11, 0.1); border-radius: 8px; font-size: 12.5px; color: #fcd34d;">
                    Tokens ilegais recebem <code>logit = -∞</code> (probabilidade 0). Apenas tokens que preservam o schema são mantidos.
                </div>
            </div>

            <!-- Seta 2 -->
            <div style="display: flex; justify-content: center; color: #10b981; font-size: 28px; font-weight: 800;">→</div>

            <!-- Passo 3 -->
            <div class="card" style="padding: 24px; border-color: rgba(16, 185, 129, 0.4);">
                <span class="badge badge-emerald">Passo 3 • Token Selecionado</span>
                <div style="font-size: 18px; font-weight: 800; margin: 12px 0 8px;">Amostragem Válida</div>
                <div style="font-size: 13.5px; color: #94a3b8; line-height: 1.5;">
                    O token amostrado pertence obrigatoriamente à linguagem do schema. A sintaxe e os tipos são imunes a alucinação estrutural.
                </div>
                <div class="code-block" style="font-size: 11.5px; margin-top: 12px;">
token_escolhido =
  "\"buscar_politica\""
status = 100% VÁLIDO
                </div>
            </div>
        </div>

        <div style="display: flex; gap: 18px; background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 18px 24px; align-items: center;">
            <div style="font-size: 32px;">💡</div>
            <div style="font-size: 14px; color: #cbd5e1; line-height: 1.6;">
                <strong>Por que o modelo não fica mais "burro"?</strong> A máscara não altera o conhecimento do modelo; ela apenas proíbe que ele gaste probabilidade em formatos inúteis para o código. O modelo é forçado a alocar 100% de sua atenção nos dados reais da resposta.
            </div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 2: O filtro opera camada a camada na inferência do Ollama/llama.cpp sem reprocessamento</div>
    </div>
</body>
</html>"""

# ---------------------------------------------------------------------------
# FIGURA 3: Matriz de Resultados Medidos: Livre vs JSON vs Schema
# ---------------------------------------------------------------------------
TEMPLATES["0009_saida_estruturada/assets/03.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0009 • Saída Estruturada</div>
            <div class="title">Conformidade e Assertividade por Modo de Execução</div>
            <div class="subtitle">54 execuções controladas com qwen2.5 (0.5B e 1.5B) e llama3.2 (1B) no Ollama</div>
        </div>
        <div class="figure-badge">Figura 3</div>
    </div>

    <div class="main-content" style="gap: 20px; align-items: stretch;">
        <!-- Card Livre -->
        <div class="card" style="flex: 1; padding: 24px; border-color: rgba(239, 68, 68, 0.4);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="badge" style="background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4);">Modo Livre</span>
                <span style="font-size: 13px; color: #ef4444; font-weight: 700;">Instável</span>
            </div>
            <div style="font-size: 32px; font-weight: 900; margin: 16px 0 6px; color: #f87171;">72.2% <span style="font-size: 14px; font-weight: 500; color: #94a3b8;">parse_ok</span></div>
            <div style="font-size: 13px; color: #94a3b8; margin-bottom: 20px;">Quase 30% das saídas falham no json.loads direto sem limpeza manual.</div>

            <div style="display: flex; flex-direction: column; gap: 12px; margin-top: auto;">
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 12.5px; margin-bottom: 4px;">
                        <span>Conformidade com Schema</span><span style="font-weight: 700; color: #f87171;">55.6%</span>
                    </div>
                    <div style="height: 8px; background: rgba(255,255,255,0.06); border-radius: 4px;"><div style="width: 55.6%; height: 100%; background: #ef4444; border-radius: 4px;"></div></div>
                </div>
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 12.5px; margin-bottom: 4px;">
                        <span>Acerto Semântico</span><span style="font-weight: 700; color: #f87171;">44.4%</span>
                    </div>
                    <div style="height: 8px; background: rgba(255,255,255,0.06); border-radius: 4px;"><div style="width: 44.4%; height: 100%; background: #ef4444; border-radius: 4px;"></div></div>
                </div>
            </div>
        </div>

        <!-- Card JSON -->
        <div class="card" style="flex: 1; padding: 24px; border-color: rgba(245, 158, 11, 0.4);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="badge badge-amber">format: "json"</span>
                <span style="font-size: 13px; color: #f59e0b; font-weight: 700;">Sintático</span>
            </div>
            <div style="font-size: 32px; font-weight: 900; margin: 16px 0 6px; color: #fbbf24;">100% <span style="font-size: 14px; font-weight: 500; color: #94a3b8;">parse_ok</span></div>
            <div style="font-size: 13px; color: #94a3b8; margin-bottom: 20px;">Sintaxe sempre válida, mas tipos e enums internos ainda falham.</div>

            <div style="display: flex; flex-direction: column; gap: 12px; margin-top: auto;">
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 12.5px; margin-bottom: 4px;">
                        <span>Conformidade com Schema</span><span style="font-weight: 700; color: #fbbf24;">66.7%</span>
                    </div>
                    <div style="height: 8px; background: rgba(255,255,255,0.06); border-radius: 4px;"><div style="width: 66.7%; height: 100%; background: #f59e0b; border-radius: 4px;"></div></div>
                </div>
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 12.5px; margin-bottom: 4px;">
                        <span>Acerto Semântico</span><span style="font-weight: 700; color: #fbbf24;">55.6%</span>
                    </div>
                    <div style="height: 8px; background: rgba(255,255,255,0.06); border-radius: 4px;"><div style="width: 55.6%; height: 100%; background: #f59e0b; border-radius: 4px;"></div></div>
                </div>
            </div>
        </div>

        <!-- Card Schema -->
        <div class="card" style="flex: 1; padding: 24px; border-color: rgba(16, 185, 129, 0.45); background: rgba(16, 185, 129, 0.04);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="badge badge-emerald">format: &lt;schema&gt;</span>
                <span style="font-size: 13px; color: #10b981; font-weight: 700;">Garantido</span>
            </div>
            <div style="font-size: 32px; font-weight: 900; margin: 16px 0 6px; color: #34d399;">100% <span style="font-size: 14px; font-weight: 500; color: #94a3b8;">schema_ok</span></div>
            <div style="font-size: 13px; color: #94a3b8; margin-bottom: 20px;">Zero falhas de contrato. 100% dos campos, tipos e enums respeitados.</div>

            <div style="display: flex; flex-direction: column; gap: 12px; margin-top: auto;">
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 12.5px; margin-bottom: 4px;">
                        <span>Conformidade com Schema</span><span style="font-weight: 700; color: #34d399;">100.0%</span>
                    </div>
                    <div style="height: 8px; background: rgba(255,255,255,0.06); border-radius: 4px;"><div style="width: 100%; height: 100%; background: #10b981; border-radius: 4px;"></div></div>
                </div>
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 12.5px; margin-bottom: 4px;">
                        <span>Acerto Semântico</span><span style="font-weight: 700; color: #34d399;">94.4%</span>
                    </div>
                    <div style="height: 8px; background: rgba(255,255,255,0.06); border-radius: 4px;"><div style="width: 94.4%; height: 100%; background: #8b5cf6; border-radius: 4px;"></div></div>
                </div>
            </div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 3: O contrato estrito eleva tanto a confiabilidade sintática quanto a assertividade semântica do modelo</div>
    </div>
</body>
</html>"""

# ---------------------------------------------------------------------------
# FIGURA 4: Efeito de Retry e Trade-off de Latência
# ---------------------------------------------------------------------------
TEMPLATES["0009_saida_estruturada/assets/04.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0009 • Saída Estruturada</div>
            <div class="title">Efeito de Retry e Custo de Latência</div>
            <div class="subtitle">O mito do "retry com prompt" versus a eficiência do schema determinístico</div>
        </div>
        <div class="figure-badge">Figura 4</div>
    </div>

    <div class="main-content" style="gap: 24px;">
        <div class="card" style="flex: 1.1; padding: 26px; border-color: rgba(139, 92, 246, 0.4);">
            <div style="font-size: 18px; font-weight: 800; margin-bottom: 12px; color: #fff;">Decomposição de Latência Média por Chamada</div>
            <div style="font-size: 13.5px; color: #94a3b8; line-height: 1.6; margin-bottom: 24px;">
                Muitos engenheiros evitam schemas temendo sobrecarga de CPU. Nossos testes provam que o overhead da gramática é mínimo se comparado à duplicação de tempo causada por retries.
            </div>

            <div style="display: flex; flex-direction: column; gap: 16px;">
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px;">
                        <span>Modo Livre (sem retry)</span><span style="font-weight: 700; color: #94a3b8;">~1.150 ms</span>
                    </div>
                    <div style="height: 12px; background: rgba(255,255,255,0.06); border-radius: 6px;"><div style="width: 45%; height: 100%; background: #64748b; border-radius: 6px;"></div></div>
                </div>

                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px;">
                        <span>Modo Schema (1 tentativa, 100% de sucesso)</span><span style="font-weight: 700; color: #34d399;">~1.380 ms (+200ms de overhead)</span>
                    </div>
                    <div style="height: 12px; background: rgba(255,255,255,0.06); border-radius: 6px;"><div style="width: 54%; height: 100%; background: #10b981; border-radius: 6px;"></div></div>
                </div>

                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px;">
                        <span>Modo Livre com Retry (falha 1ª chamada + 2ª chamada)</span><span style="font-weight: 700; color: #f87171;">~2.450 ms (2x latência!)</span>
                    </div>
                    <div style="height: 12px; background: rgba(255,255,255,0.06); border-radius: 6px;"><div style="width: 95%; height: 100%; background: #ef4444; border-radius: 6px;"></div></div>
                </div>
            </div>
        </div>

        <div class="card" style="flex: 0.9; padding: 26px; border-color: rgba(59, 130, 246, 0.4); justify-content: space-between;">
            <div>
                <span class="badge badge-blue">Regra de Ouro</span>
                <div style="font-size: 18px; font-weight: 800; margin: 12px 0 8px;">Deterministic First, Retry Second</div>
                <div style="font-size: 13.5px; color: #94a3b8; line-height: 1.6;">
                    Retries não devem ser usados para consertar sintaxe quebrada; a gramática cuida disso na primeira tentativa.
                </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 14px;">
                <div style="padding: 10px 14px; background: rgba(16, 185, 129, 0.1); border-left: 3px solid #10b981; font-size: 12.5px; color: #6ee7b7;">
                    ✓ <strong>1ª chamada:</strong> <code>temperature = 0.0</code> + JSON Schema rígido.
                </div>
                <div style="padding: 10px 14px; background: rgba(245, 158, 11, 0.1); border-left: 3px solid #f59e0b; font-size: 12.5px; color: #fcd34d;">
                    ⚠ <strong>Retry eventual:</strong> apenas se validação semântica de negócio falhar, variando para <code>temperature = 0.5</code>.
                </div>
            </div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 4: O custo de impor schema na decodificação é incomparavelmente menor que o custo de uma segunda chamada HTTP</div>
    </div>
</body>
</html>"""

# ---------------------------------------------------------------------------
# FIGURA 5: Padrão Arquitetural de Integração em Produção
# ---------------------------------------------------------------------------
TEMPLATES["0009_saida_estruturada/assets/05.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0009 • Saída Estruturada</div>
            <div class="title">Arquitetura de Integração de Saída Estruturada</div>
            <div class="subtitle">Pipeline desacoplado: do contrato Pydantic/JSON Schema ao barramento de microsserviços</div>
        </div>
        <div class="figure-badge">Figura 5</div>
    </div>

    <div class="main-content" style="flex-direction: column; gap: 20px; justify-content: center;">
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 16px; width: 100%;">
            <div class="card" style="padding: 22px; border-color: rgba(59, 130, 246, 0.4);">
                <div style="font-size: 12px; font-weight: 700; color: #60a5fa; text-transform: uppercase;">1. Definição do Contrato</div>
                <div style="font-size: 16px; font-weight: 800; margin: 8px 0;">Pydantic / JSON Schema</div>
                <div style="font-size: 13px; color: #94a3b8; line-height: 1.5;">O contrato do domínio é a única fonte da verdade, tipando campos, limites e enums.</div>
            </div>

            <div class="card" style="padding: 22px; border-color: rgba(245, 158, 11, 0.4);">
                <div style="font-size: 12px; font-weight: 700; color: #fbbf24; text-transform: uppercase;">2. Injeção no Motor</div>
                <div style="font-size: 16px; font-weight: 800; margin: 8px 0;">Ollama format=&lt;schema&gt;</div>
                <div style="font-size: 13px; color: #94a3b8; line-height: 1.5;">O motor compila a gramática e mascara os logits a cada token gerado.</div>
            </div>

            <div class="card" style="padding: 22px; border-color: rgba(16, 185, 129, 0.4);">
                <div style="font-size: 12px; font-weight: 700; color: #34d399; text-transform: uppercase;">3. Parsing Determinístico</div>
                <div style="font-size: 16px; font-weight: 800; margin: 8px 0;">Parse sem Try/Catch</div>
                <div style="font-size: 13px; color: #94a3b8; line-height: 1.5;">O backend deserializa o payload diretamente para a classe de domínio sem medo de quebra.</div>
            </div>

            <div class="card" style="padding: 22px; border-color: rgba(139, 92, 246, 0.4);">
                <div style="font-size: 12px; font-weight: 700; color: #c084fc; text-transform: uppercase;">4. Trilha de Auditoria</div>
                <div style="font-size: 16px; font-weight: 800; margin: 8px 0;">Registro em CSV/JSONL</div>
                <div style="font-size: 13px; color: #94a3b8; line-height: 1.5;">Tempo, tokens, confianca e payload persistidos para governança e monitoramento contínuo.</div>
            </div>
        </div>

        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 14px; padding: 20px 28px;">
            <div style="font-size: 15px; font-weight: 700; color: #f1f5f9; margin-bottom: 8px;">Benefício Corporativo: Eliminação de Fragilidade nos Agentes</div>
            <div style="font-size: 13.5px; color: #94a3b8; line-height: 1.6;">
                Em pipelines de agentes (como no módulo 0007 e no futuro 0010 com MCP), a saída do modelo alimenta chamadas de API reais. Usar decodificação constrangida elimina 100% dos erros de <em>KeyError</em>, <em>ValueError</em> e chamadas acidentais a endpoints inexistentes.
            </div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 5: O contrato rígido transforma inferência probabilística em chamada de função confiável</div>
    </div>
</body>
</html>"""

# ---------------------------------------------------------------------------
# FIGURA 6: A Fronteira dos Modelos "System 1" (Jev vs Laya / Kev)
# ---------------------------------------------------------------------------
TEMPLATES["0009_saida_estruturada/assets/06.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0009 • Saída Estruturada</div>
            <div class="title">Modelos "System 1" vs LLMs Generativos</div>
            <div class="subtitle">A evolução da saída estruturada: da autoregressão com Grammar Mask às decisões diretas em passada única (~30 ms)</div>
        </div>
        <div class="figure-badge">Figura 6</div>
    </div>

    <div class="main-content" style="gap: 24px; align-items: stretch;">
        <!-- Coluna Esquerda: System 2 Autoregressivo -->
        <div class="card" style="flex: 1; border-color: rgba(59, 130, 246, 0.4); background: rgba(59, 130, 246, 0.04); justify-content: space-between;">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                    <span class="badge" style="background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4);">System 2 • Autoregressivo</span>
                    <span style="font-size: 12px; color: #94a3b8; font-weight: 600;">LLM + Grammar Masking</span>
                </div>
                <div style="font-size: 20px; font-weight: 800; color: #fff; margin-bottom: 8px;">Geração Token a Token</div>
                <div style="font-size: 13.5px; color: #94a3b8; line-height: 1.6; margin-bottom: 16px;">
                    Modelos como <strong>Qwen 2.5</strong> e <strong>Llama 3.2</strong> no Ollama geram cada token sequencialmente sob um autômato FSM que mascara logits proibidos.
                </div>

                <div class="code-block" style="font-size: 12px; margin-bottom: 14px;">
// Pipeline Autoregressivo (N passadas):
Prompt ──> Decoder ──> Logits Mask FSM ──> Token t+1
Repetido ~40 vezes para compor o JSON:
{{"tool": "buscar_politica", "confianca": 0.94}}
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 14px;">
                    <div style="background: rgba(15, 23, 42, 0.6); padding: 10px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.08);">
                        <div style="font-size: 11px; color: #94a3b8;">Latência Típica (CPU)</div>
                        <div style="font-size: 18px; font-weight: 800; color: #f87171;">1.500 ~ 2.200 ms</div>
                    </div>
                    <div style="background: rgba(15, 23, 42, 0.6); padding: 10px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.08);">
                        <div style="font-size: 11px; color: #94a3b8;">Passadas na Rede</div>
                        <div style="font-size: 18px; font-weight: 800; color: #fbbf24;">N Tokens (O(N))</div>
                    </div>
                </div>
            </div>


            <div style="padding: 12px; background: rgba(59, 130, 246, 0.1); border-radius: 8px; font-size: 12.5px; color: #93c5fd; line-height: 1.5;">
                <strong>Melhor uso:</strong> Payloads que exigem texto livre, síntese semântica rica ou campos de linguagem natural no interior do JSON.
            </div>
        </div>

        <!-- Coluna Direita: System 1 Modelos de Decisão -->
        <div class="card" style="flex: 1; border-color: rgba(16, 185, 129, 0.4); background: rgba(16, 185, 129, 0.04); justify-content: space-between;">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                    <span class="badge" style="background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4);">System 1 • Não Generativo</span>
                    <span style="font-size: 12px; color: #94a3b8; font-weight: 600;">Laya (Open-Source) / Jev</span>
                </div>
                <div style="font-size: 20px; font-weight: 800; color: #fff; margin-bottom: 8px;">Decisão Direta em Passada Única</div>
                <div style="font-size: 13.5px; color: #94a3b8; line-height: 1.6; margin-bottom: 16px;">
                    Modelos como <strong>Laya</strong> (Convai, Apache 2.0) e <strong>Jev</strong> (TypeSafe AI) eliminam a geração de texto. Um encoder avalia cabeças tipadas em <strong>O(1)</strong>.
                </div>

                <div class="code-block" style="font-size: 12px; margin-bottom: 14px;">
// Pipeline System 1 (1 única passada direta):
Estado ──> Encoder (ModernBERT) ──> Cabeça de Decisão
Retorno Direto de Primitivas Tipadas:
- Choice: "buscar_politica" (Softmax Calibrado: 0.94)
- Score:  Risco = 0.12 (Escala Contínua)
- Bool:   PrecisaTool = True (Portão Binário)
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 14px;">
                    <div style="background: rgba(15, 23, 42, 0.6); padding: 10px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.08);">
                        <div style="font-size: 11px; color: #94a3b8;">Latência Típica (CPU)</div>
                        <div style="font-size: 18px; font-weight: 800; color: #34d399;">15 ~ 40 ms</div>
                    </div>
                    <div style="background: rgba(15, 23, 42, 0.6); padding: 10px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.08);">
                        <div style="font-size: 11px; color: #94a3b8;">Redução de Latência</div>
                        <div style="font-size: 18px; font-weight: 800; color: #a78bfa;">> 50x Mais Rápido</div>
                    </div>
                </div>
            </div>

            <div style="padding: 12px; background: rgba(16, 185, 129, 0.1); border-radius: 8px; font-size: 12.5px; color: #a7f3d0; line-height: 1.5;">
                <strong>Melhor uso:</strong> Roteamento de agentes, seleção de ferramentas (MCP), guardrails de segurança e triagem de alta frequência.
            </div>
        </div>
    </div>

    <!-- Barra Inferior: Arquitetura Híbrida -->
    <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 12px; padding: 16px 24px; margin-top: -8px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-size: 14px; font-weight: 800; color: #f1f5f9;">O Padrão Híbrido Corporativo:</span>
                <span style="font-size: 13px; color: #94a3b8; margin-left: 8px;">
                    Use <strong>System 1 (Laya / Jev)</strong> no portão de entrada para rotear em &lt; 40 ms ➔ Invoque <strong>System 2 (Ollama + Schema)</strong> somente quando síntese de texto for indispensável.
                </span>
            </div>
            <span class="badge" style="background: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.4); white-space: nowrap;">Arquitetura Ideal</span>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 6: Separação de responsabilidades: decisões puras em System 1 e redação criativa em System 2</div>
    </div>
</body>
</html>"""


def render_all() -> None:
    from measured_assets import overrides
    TEMPLATES.update({key: value for key, value in overrides().items() if key in TEMPLATES})
    print(f"Renderizando {len(TEMPLATES)} ativos visuais para 0009_saida_estruturada...")
    for rel_path, html in TEMPLATES.items():
        output_png = ROOT / rel_path
        render_html_to_png(html, output_png)
    print("Ativos do artigo 0009 renderizados com sucesso!")



if __name__ == "__main__":
    render_all()
