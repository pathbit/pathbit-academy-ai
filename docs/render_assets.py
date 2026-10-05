#!/usr/bin/env python3
"""Gerador de ativos visuais em altíssima definição para Pathbit Academy AI.

Renderiza diagramas de arquitetura, comparativos e infográficos técnicos
em HTML5/CSS3 com estética premium (dark mode, glassmorphism, tipografia moderna)
e captura imagens PNG nítidas em 1920x1080 via Google Chrome headless.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

BASE_HEAD = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    width: 1920px;
    height: 1080px;
    overflow: hidden;
    background: #070a13;
    background-image: 
        radial-gradient(circle at 12% 15%, rgba(37, 99, 235, 0.16) 0%, transparent 40%),
        radial-gradient(circle at 88% 85%, rgba(16, 185, 129, 0.12) 0%, transparent 40%),
        radial-gradient(circle at 50% 50%, rgba(139, 92, 246, 0.08) 0%, transparent 55%);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #f1f5f9;
    padding: 44px 56px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 24px;
}

.header-left {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.brand-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(37, 99, 235, 0.15);
    border: 1px solid rgba(59, 130, 246, 0.35);
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: #60a5fa;
    text-transform: uppercase;
    width: fit-content;
}

.brand-pill .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #3b82f6;
    box-shadow: 0 0 10px #3b82f6;
}

.title {
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #ffffff;
    line-height: 1.15;
}

.subtitle {
    font-size: 18px;
    color: #94a3b8;
    font-weight: 500;
}

.figure-badge {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    padding: 8px 18px;
    border-radius: 12px;
    font-size: 15px;
    font-weight: 700;
    color: #cbd5e1;
    display: flex;
    align-items: center;
    gap: 8px;
}

.main-content {
    flex: 1;
    display: flex;
    gap: 28px;
    position: relative;
    align-items: stretch;
    min-height: 0;
}

.footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 16px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    font-size: 14px;
    color: #64748b;
    font-weight: 500;
}

.footer strong {
    color: #94a3b8;
}

.card {
    background: rgba(15, 23, 42, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 28px;
    backdrop-filter: blur(12px);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.28);
    display: flex;
    flex-direction: column;
}

.card-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.card-desc {
    font-size: 15px;
    color: #94a3b8;
    line-height: 1.5;
    margin-bottom: 16px;
}

.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.badge-blue { background: rgba(37, 99, 235, 0.2); color: #60a5fa; border: 1px solid rgba(37, 99, 235, 0.4); }
.badge-emerald { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }
.badge-amber { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
.badge-rose { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
.badge-purple { background: rgba(139, 92, 246, 0.2); color: #c084fc; border: 1px solid rgba(139, 92, 246, 0.4); }

.code-editor {
    font-family: 'JetBrains Mono', monospace;
    background: #040711;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

.editor-header {
    background: rgba(255, 255, 255, 0.03);
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    padding: 10px 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.window-dots {
    display: flex;
    gap: 6px;
}

.dot-red { width: 10px; height: 10px; border-radius: 50%; background: #ef4444; }
.dot-yellow { width: 10px; height: 10px; border-radius: 50%; background: #f59e0b; }
.dot-green { width: 10px; height: 10px; border-radius: 50%; background: #10b981; }

.editor-title {
    font-size: 12px;
    color: #64748b;
    margin-left: 8px;
}

.editor-body {
    padding: 16px 20px;
    font-size: 14px;
    line-height: 1.6;
    color: #e2e8f0;
}
</style>
</head>
"""

TEMPLATES = {}

# ==========================================
# ARTIGO 0005: PROMPT ENGINEERING AVANÇADO
# ==========================================

TEMPLATES["0005_prompt_engineering_avancado/assets/01.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0005 • Prompt Engineering Avançado</div>
            <div class="title">O Erro que Quebra a Confiança</div>
            <div class="subtitle">Instrução vaga vs. Contrato de saída estruturado em operações com LLM</div>
        </div>
        <div class="figure-badge">Figura 1</div>
    </div>

    <div class="main-content">
        <!-- Lado Sem Metodo -->
        <div class="card" style="flex: 1; border-color: rgba(239, 68, 68, 0.3); background: rgba(239, 68, 68, 0.03);">
            <div class="card-title" style="color: #f87171;">
                <span class="badge badge-rose">Instável</span> Sem Método (Instrução Vaga)
            </div>
            <div class="card-desc">Quando o formato de resposta fica implícito, o modelo varia arbitrariamente o tom e a estrutura.</div>
            
            <div class="code-editor" style="margin-bottom: 20px; border-color: rgba(239, 68, 68, 0.2);">
                <div class="editor-header">
                    <div class="window-dots"><div class="dot-red"></div><div class="dot-yellow"></div><div class="dot-green"></div></div>
                    <span class="editor-title">prompt_vago.txt</span>
                </div>
                <div class="editor-body">
                    <span style="color: #94a3b8;">"Resuma o chamado: Cliente irritado com atraso na entrega."</span>
                </div>
            </div>

            <div style="font-size: 13px; font-weight: 700; color: #ef4444; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.05em;">
                Saídas Imprevisíveis em Produção:
            </div>

            <div style="display: flex; flex-direction: column; gap: 12px; flex: 1;">
                <div style="background: rgba(239, 68, 68, 0.08); border: 1px dashed rgba(239, 68, 68, 0.3); border-radius: 12px; padding: 14px 18px;">
                    <div style="font-weight: 600; font-size: 14px; color: #fca5a5; margin-bottom: 4px;">1. Texto Prolixo sem Foco</div>
                    <div style="font-size: 13px; color: #cbd5e1;">"O cliente expressou descontentamento com a data prevista do frete e solicita resolução com certa prioridade..."</div>
                </div>
                <div style="background: rgba(239, 68, 68, 0.08); border: 1px dashed rgba(239, 68, 68, 0.3); border-radius: 12px; padding: 14px 18px;">
                    <div style="font-weight: 600; font-size: 14px; color: #fca5a5; margin-bottom: 4px;">2. Bullet Points Aleatórios</div>
                    <div style="font-size: 13px; color: #cbd5e1;">"• Motivo: pedido atrasado<br>• Urgência: alta<br>• Observação: verificar se tem estoque."</div>
                </div>
                <div style="background: rgba(239, 68, 68, 0.08); border: 1px dashed rgba(239, 68, 68, 0.3); border-radius: 12px; padding: 14px 18px;">
                    <div style="font-weight: 600; font-size: 14px; color: #fca5a5; margin-bottom: 4px;">3. Desculpas do Modelo</div>
                    <div style="font-size: 13px; color: #cbd5e1;">"Como um modelo de inteligência artificial, sinto muito pelo transtorno do usuário..."</div>
                </div>
            </div>

            <div style="margin-top: 18px; padding: 10px 14px; background: rgba(239, 68, 68, 0.15); border-radius: 8px; font-size: 13px; color: #fca5a5; font-weight: 600; text-align: center;">
                ✗ Inviável para ingestão por APIs, bancos de dados ou gatilhos automatizados
            </div>
        </div>

        <!-- Lado Com Metodo -->
        <div class="card" style="flex: 1; border-color: rgba(16, 185, 129, 0.3); background: rgba(16, 185, 129, 0.03);">
            <div class="card-title" style="color: #34d399;">
                <span class="badge badge-emerald">Determinístico</span> Com Método (Contrato de Saída)
            </div>
            <div class="card-desc">O contrato especifica campos obrigatórios, vocabulário fechado e formato padronizado.</div>
            
            <div class="code-editor" style="margin-bottom: 20px; border-color: rgba(16, 185, 129, 0.2);">
                <div class="editor-header">
                    <div class="window-dots"><div class="dot-red"></div><div class="dot-yellow"></div><div class="dot-green"></div></div>
                    <span class="editor-title">prompt_estruturado.txt</span>
                </div>
                <div class="editor-body">
                    <span style="color: #94a3b8;">"Você é analista de atendimento Pathbit.<br>Responda EXATAMENTE com 3 linhas:<br>resumo: &lt;uma frase&gt;<br>prioridade: &lt;alta|media|baixa&gt;<br>proxima_acao: &lt;uma frase objetiva&gt;<br>Mensagem: Cliente irritado com atraso na entrega."</span>
                </div>
            </div>

            <div style="font-size: 13px; font-weight: 700; color: #10b981; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.05em;">
                Saída 100% Validável & Integrável:
            </div>

            <div class="code-editor" style="flex: 1; background: #03080e; border: 1px solid rgba(16, 185, 129, 0.35);">
                <div class="editor-header" style="background: rgba(16, 185, 129, 0.08);">
                    <div class="window-dots"><div class="dot-red"></div><div class="dot-yellow"></div><div class="dot-green"></div></div>
                    <span class="editor-title" style="color: #34d399;">resposta_validada.json</span>
                </div>
                <div class="editor-body" style="font-size: 15px; line-height: 1.8;">
                    <span style="color: #64748b;">&#123;</span><br>
                    &nbsp;&nbsp;<span style="color: #38bdf8;">"resumo"</span>: <span style="color: #a7f3d0;">"Cliente reclama de atraso fora do prazo contratual"</span>,<br>
                    &nbsp;&nbsp;<span style="color: #38bdf8;">"prioridade"</span>: <span style="color: #fbbf24;">"ALTA"</span>,<br>
                    &nbsp;&nbsp;<span style="color: #38bdf8;">"proxima_acao"</span>: <span style="color: #a7f3d0;">"Abrir ticket técnico N2 e acionar transportadora em 1h"</span><br>
                    <span style="color: #64748b;">&#125;</span>
                </div>
            </div>

            <div style="margin-top: 18px; padding: 10px 14px; background: rgba(16, 185, 129, 0.15); border-radius: 8px; font-size: 13px; color: #a7f3d0; font-weight: 600; text-align: center;">
                ✓ Validação instantânea via Regex / Pydantic • Roteamento automatizado sem intervenção manual
            </div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 1: Comparativo entre instrução ambígua e contrato de saída operacional</div>
    </div>
</body>
</html>"""

TEMPLATES["0005_prompt_engineering_avancado/assets/02.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0005 • Prompt Engineering Avançado</div>
            <div class="title">Framework em Quatro Camadas</div>
            <div class="subtitle">Arquitetura de instrução para transformar prompts em interfaces sistêmicas de alta confiabilidade</div>
        </div>
        <div class="figure-badge">Figura 2</div>
    </div>

    <div class="main-content" style="flex-direction: column; gap: 18px;">
        <!-- Camada 1 -->
        <div class="card" style="flex: 1; padding: 20px 28px; border-left: 6px solid #3b82f6; flex-direction: row; align-items: center; justify-content: space-between; gap: 32px;">
            <div style="display: flex; align-items: center; gap: 20px; width: 340px;">
                <div style="width: 52px; height: 52px; border-radius: 14px; background: rgba(59, 130, 246, 0.2); border: 1px solid rgba(59, 130, 246, 0.4); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 22px; color: #60a5fa;">1</div>
                <div>
                    <div style="font-size: 20px; font-weight: 700; color: #ffffff;">Papel & Objetivo</div>
                    <div style="font-size: 13px; color: #60a5fa; font-weight: 600; text-transform: uppercase;">Persona & Escopo</div>
                </div>
            </div>
            <div style="flex: 1; font-size: 15px; color: #cbd5e1; line-height: 1.5;">
                Define quem é o modelo, seu nível de autoridade e a meta inegociável de negócio. Restringe o espaço de busca latente, eliminando introduções desnecessárias e ancorando a resposta no tom corporativo esperado.
            </div>
            <div style="background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.25); border-radius: 10px; padding: 10px 18px; width: 300px; text-align: right; font-size: 13px; color: #93c5fd; font-weight: 500;">
                <strong style="color: #ffffff;">Exemplo:</strong> "Você é analista sênior de suporte da Pathbit. Responda em português."
            </div>
        </div>

        <!-- Camada 2 -->
        <div class="card" style="flex: 1; padding: 20px 28px; border-left: 6px solid #8b5cf6; flex-direction: row; align-items: center; justify-content: space-between; gap: 32px;">
            <div style="display: flex; align-items: center; gap: 20px; width: 340px;">
                <div style="width: 52px; height: 52px; border-radius: 14px; background: rgba(139, 92, 246, 0.2); border: 1px solid rgba(139, 92, 246, 0.4); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 22px; color: #c084fc;">2</div>
                <div>
                    <div style="font-size: 20px; font-weight: 700; color: #ffffff;">Contrato de Saída</div>
                    <div style="font-size: 13px; color: #c084fc; font-weight: 600; text-transform: uppercase;">Schema & Chaves Fixas</div>
                </div>
            </div>
            <div style="flex: 1; font-size: 15px; color: #cbd5e1; line-height: 1.5;">
                Fixa um contrato sintático rígido (JSON, YAML ou chaves textuais). Obriga o modelo a preencher campos estruturados (`resumo`, `prioridade`, `proxima_acao`) e rejeita respostas em formato livre ou prolixo.
            </div>
            <div style="background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.25); border-radius: 10px; padding: 10px 18px; width: 300px; text-align: right; font-size: 13px; color: #d8b4fe; font-weight: 500;">
                <strong style="color: #ffffff;">Exemplo:</strong> "Retorne EXATAMENTE 3 linhas: resumo, prioridade e proxima_acao."
            </div>
        </div>

        <!-- Camada 3 -->
        <div class="card" style="flex: 1; padding: 20px 28px; border-left: 6px solid #f59e0b; flex-direction: row; align-items: center; justify-content: space-between; gap: 32px;">
            <div style="display: flex; align-items: center; gap: 20px; width: 340px;">
                <div style="width: 52px; height: 52px; border-radius: 14px; background: rgba(245, 158, 11, 0.2); border: 1px solid rgba(245, 158, 11, 0.4); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 22px; color: #fbbf24;">3</div>
                <div>
                    <div style="font-size: 20px; font-weight: 700; color: #ffffff;">Exemplos Few-Shot</div>
                    <div style="font-size: 13px; color: #fbbf24; font-weight: 600; text-transform: uppercase;">Pares de Calibração</div>
                </div>
            </div>
            <div style="flex: 1; font-size: 15px; color: #cbd5e1; line-height: 1.5;">
                Injeta exemplos de alta qualidade de `entrada -> saída ideal`. Calibra o nível de concisão, regras de inferência de prioridade e padrão de vocabulário, eliminando ambiguidades sem necessidade de fine-tuning.
            </div>
            <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.25); border-radius: 10px; padding: 10px 18px; width: 300px; text-align: right; font-size: 13px; color: #fde68a; font-weight: 500;">
                <strong style="color: #ffffff;">Exemplo:</strong> "Exemplo 1: Mensagem erro 500 -> prioridade: alta | proxima_acao: ticket 1h."
            </div>
        </div>

        <!-- Camada 4 -->
        <div class="card" style="flex: 1; padding: 20px 28px; border-left: 6px solid #10b981; flex-direction: row; align-items: center; justify-content: space-between; gap: 32px;">
            <div style="display: flex; align-items: center; gap: 20px; width: 340px;">
                <div style="width: 52px; height: 52px; border-radius: 14px; background: rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.4); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 22px; color: #34d399;">4</div>
                <div>
                    <div style="font-size: 20px; font-weight: 700; color: #ffffff;">Validação & Score</div>
                    <div style="font-size: 13px; color: #34d399; font-weight: 600; text-transform: uppercase;">Avaliação Automatizada</div>
                </div>
            </div>
            <div style="flex: 1; font-size: 15px; color: #cbd5e1; line-height: 1.5;">
                Aferição programática do resultado: checagem de estrutura (100% de campos presentes), recall de palavras-chave, assertividade da prioridade inferida e similaridade semântica com o gabarito.
            </div>
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 10px; padding: 10px 18px; width: 300px; text-align: right; font-size: 13px; color: #a7f3d0; font-weight: 500;">
                <strong style="color: #ffffff;">Métricas:</strong> `score_estrutura`, `score_keywords`, `score_prioridade`, `score_semantico`.
            </div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 2: As 4 camadas fundamentais para construir prompts corporativos robustos</div>
    </div>
</body>
</html>"""

TEMPLATES["0005_prompt_engineering_avancado/assets/03.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0005 • Prompt Engineering Avançado</div>
            <div class="title">O Poder do Contrato de Saída</div>
            <div class="subtitle">Como a imposição de schema transforma inferência probabilística em interface confiável</div>
        </div>
        <div class="figure-badge">Figura 3</div>
    </div>

    <div class="main-content">
        <!-- Coluna Esquerda: Prompt Ingenuo -->
        <div class="card" style="flex: 1; border-color: rgba(239, 68, 68, 0.3); background: rgba(239, 68, 68, 0.02);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                <div class="card-title" style="color: #f87171; margin-bottom: 0;">
                    <span class="badge badge-rose">Sem Contrato</span> Prompt Ingênuo
                </div>
                <span style="font-size: 13px; color: #ef4444; font-weight: 600;">Alta Variância</span>
            </div>

            <div class="code-editor" style="margin-bottom: 18px; border-color: rgba(239, 68, 68, 0.25);">
                <div class="editor-header">
                    <div class="window-dots"><div class="dot-red"></div><div class="dot-yellow"></div><div class="dot-green"></div></div>
                    <span class="editor-title">chamado_v1.txt</span>
                </div>
                <div class="editor-body" style="font-size: 14px;">
                    <span style="color: #94a3b8;"># Instrução</span><br>
                    Analise este chamado:<br>
                    <span style="color: #fca5a5;">'Não consigo acessar a plataforma, dá erro 500!'</span>
                </div>
            </div>

            <div style="font-size: 13px; font-weight: 700; color: #94a3b8; margin-bottom: 8px; text-transform: uppercase;">
                Resposta Típica do Modelo:
            </div>

            <div class="code-editor" style="flex: 1; background: #060911; border-color: rgba(239, 68, 68, 0.2);">
                <div class="editor-body" style="color: #fca5a5; line-height: 1.6;">
                    "Parece que o usuário está enfrentando uma instabilidade grave no servidor da plataforma (código de status HTTP 500). Recomendo que a equipe técnica verifique os logs do nginx e o banco de dados para restabelecer a conectividade o mais breve possível."
                </div>
            </div>

            <div style="margin-top: 18px; display: flex; flex-direction: column; gap: 8px;">
                <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #f87171;">
                    <span>✗</span> Formato imprevisível: impossível parsear com JSON.parse() ou Regex seguro
                </div>
                <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #f87171;">
                    <span>✗</span> Prioridade não normalizada: analista humano é forçado a triar manualmente
                </div>
                <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #f87171;">
                    <span>✗</span> Risco de automação: pode quebrar a esteira de atendimento em produção
                </div>
            </div>
        </div>

        <!-- Coluna Direita: Prompt Estruturado -->
        <div class="card" style="flex: 1; border-color: rgba(16, 185, 129, 0.3); background: rgba(16, 185, 129, 0.02);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                <div class="card-title" style="color: #34d399; margin-bottom: 0;">
                    <span class="badge badge-emerald">Com Contrato</span> Prompt Estruturado
                </div>
                <span style="font-size: 13px; color: #10b981; font-weight: 600;">Determinístico</span>
            </div>

            <div class="code-editor" style="margin-bottom: 18px; border-color: rgba(16, 185, 129, 0.25);">
                <div class="editor-header">
                    <div class="window-dots"><div class="dot-red"></div><div class="dot-yellow"></div><div class="dot-green"></div></div>
                    <span class="editor-title">chamado_v2_contrato.txt</span>
                </div>
                <div class="editor-body" style="font-size: 14px;">
                    <span style="color: #94a3b8;">Papel: Analista N2 Pathbit. Retorne EXATAMENTE 3 linhas:</span><br>
                    <span style="color: #38bdf8;">resumo</span>: &lt;uma frase objetiva&gt;<br>
                    <span style="color: #fbbf24;">prioridade</span>: &lt;alta|media|baixa&gt;<br>
                    <span style="color: #a7f3d0;">proxima_acao</span>: &lt;uma frase acionável&gt;<br>
                    Mensagem: <span style="color: #e2e8f0;">'Não consigo acessar a plataforma, dá erro 500!'</span>
                </div>
            </div>

            <div style="font-size: 13px; font-weight: 700; color: #94a3b8; margin-bottom: 8px; text-transform: uppercase;">
                Resposta Estável do Modelo:
            </div>

            <div class="code-editor" style="flex: 1; background: #060911; border-color: rgba(16, 185, 129, 0.35);">
                <div class="editor-body" style="line-height: 1.8;">
                    <span style="color: #38bdf8; font-weight: 600;">resumo:</span> Indisponibilidade de acesso à plataforma com erro 500.<br>
                    <span style="color: #fbbf24; font-weight: 600;">prioridade:</span> alta<br>
                    <span style="color: #a7f3d0; font-weight: 600;">proxima_acao:</span> Abrir ticket crítico para time de infraestrutura e verificar pods do backend.
                </div>
            </div>

            <div style="margin-top: 18px; display: flex; flex-direction: column; gap: 8px;">
                <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #34d399;">
                    <span>✓</span> 100% parseável: regex direta extrai cada chave com confiabilidade absoluta
                </div>
                <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #34d399;">
                    <span>✓</span> Prioridade restrita ao enum esperado (alta / media / baixa)
                </div>
                <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #34d399;">
                    <span>✓</span> Ingestão imediata por sistemas de mensageria (Slack, Jira, Webhooks)
                </div>
            </div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 3: Contrato de saída elimina a variância e viabiliza a integração segura com sistemas</div>
    </div>
</body>
</html>"""

TEMPLATES["0005_prompt_engineering_avancado/assets/04.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0005 • Prompt Engineering Avançado</div>
            <div class="title">Score Total por Estratégia e por Modelo</div>
            <div class="subtitle">Laboratório multi-modelo: medindo o impacto das estratégias de prompt em modelos open-source</div>
        </div>
        <div class="figure-badge">Figura 4</div>
    </div>

    <div class="main-content" style="gap: 36px;">
        <!-- Grafico de Barras Estilizado -->
        <div class="card" style="flex: 1.3; padding: 32px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
                <div class="card-title" style="margin-bottom: 0;">Performance Relativa (Score Total 0 a 1.0)</div>
                <div style="display: flex; gap: 16px; font-size: 13px;">
                    <div style="display: flex; align-items: center; gap: 6px;"><div style="width: 12px; height: 12px; border-radius: 3px; background: #3b82f6;"></div> Qwen 2.5 0.5B Instruct</div>
                    <div style="display: flex; align-items: center; gap: 6px;"><div style="width: 12px; height: 12px; border-radius: 3px; background: #f87171;"></div> Google FLAN-T5 Small</div>
                </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 24px; flex: 1; justify-content: space-around;">
                <!-- few_shot -->
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 14px; font-weight: 600; margin-bottom: 8px;">
                        <span>few_shot (Exemplo Orientador)</span>
                        <span>Qwen: <strong style="color: #60a5fa;">0.741</strong> | FLAN: <strong style="color: #fca5a5;">0.278</strong></span>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 4px;">
                        <div style="background: rgba(255,255,255,0.05); border-radius: 6px; height: 18px; overflow: hidden; display: flex;">
                            <div style="width: 74.1%; background: linear-gradient(90deg, #2563eb, #3b82f6); border-radius: 6px; display: flex; align-items: center; justify-content: flex-end; padding-right: 8px; font-size: 11px; font-weight: 700;">74.1%</div>
                        </div>
                        <div style="background: rgba(255,255,255,0.05); border-radius: 6px; height: 18px; overflow: hidden; display: flex;">
                            <div style="width: 27.8%; background: linear-gradient(90deg, #dc2626, #f87171); border-radius: 6px; display: flex; align-items: center; justify-content: flex-end; padding-right: 8px; font-size: 11px; font-weight: 700;">27.8%</div>
                        </div>
                    </div>
                </div>

                <!-- estruturado -->
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 14px; font-weight: 600; margin-bottom: 8px;">
                        <span>estruturado (Contrato Rígido)</span>
                        <span>Qwen: <strong style="color: #60a5fa;">0.729</strong> | FLAN: <strong style="color: #fca5a5;">0.270</strong></span>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 4px;">
                        <div style="background: rgba(255,255,255,0.05); border-radius: 6px; height: 18px; overflow: hidden; display: flex;">
                            <div style="width: 72.9%; background: linear-gradient(90deg, #2563eb, #3b82f6); border-radius: 6px; display: flex; align-items: center; justify-content: flex-end; padding-right: 8px; font-size: 11px; font-weight: 700;">72.9%</div>
                        </div>
                        <div style="background: rgba(255,255,255,0.05); border-radius: 6px; height: 18px; overflow: hidden; display: flex;">
                            <div style="width: 27.0%; background: linear-gradient(90deg, #dc2626, #f87171); border-radius: 6px; display: flex; align-items: center; justify-content: flex-end; padding-right: 8px; font-size: 11px; font-weight: 700;">27.0%</div>
                        </div>
                    </div>
                </div>

                <!-- checklist -->
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 14px; font-weight: 600; margin-bottom: 8px;">
                        <span>checklist (Raciocínio Operacional)</span>
                        <span>Qwen: <strong style="color: #60a5fa;">0.605</strong> | FLAN: <strong style="color: #34d399;">0.460 (Melhor FLAN)</strong></span>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 4px;">
                        <div style="background: rgba(255,255,255,0.05); border-radius: 6px; height: 18px; overflow: hidden; display: flex;">
                            <div style="width: 60.5%; background: linear-gradient(90deg, #2563eb, #3b82f6); border-radius: 6px; display: flex; align-items: center; justify-content: flex-end; padding-right: 8px; font-size: 11px; font-weight: 700;">60.5%</div>
                        </div>
                        <div style="background: rgba(255,255,255,0.05); border-radius: 6px; height: 18px; overflow: hidden; display: flex;">
                            <div style="width: 46.0%; background: linear-gradient(90deg, #059669, #34d399); border-radius: 6px; display: flex; align-items: center; justify-content: flex-end; padding-right: 8px; font-size: 11px; font-weight: 700;">46.0%</div>
                        </div>
                    </div>
                </div>

                <!-- base -->
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 14px; font-weight: 600; margin-bottom: 8px;">
                        <span>base (Instrução Livre - Linha de Base)</span>
                        <span>Qwen: <strong style="color: #64748b;">0.411</strong> | FLAN: <strong style="color: #64748b;">0.266</strong></span>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 4px;">
                        <div style="background: rgba(255,255,255,0.05); border-radius: 6px; height: 18px; overflow: hidden; display: flex;">
                            <div style="width: 41.1%; background: #475569; border-radius: 6px; display: flex; align-items: center; justify-content: flex-end; padding-right: 8px; font-size: 11px; font-weight: 700;">41.1%</div>
                        </div>
                        <div style="background: rgba(255,255,255,0.05); border-radius: 6px; height: 18px; overflow: hidden; display: flex;">
                            <div style="width: 26.6%; background: #475569; border-radius: 6px; display: flex; align-items: center; justify-content: flex-end; padding-right: 8px; font-size: 11px; font-weight: 700;">26.6%</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Painel Lateral de Conclusoes -->
        <div class="card" style="flex: 0.9; padding: 32px; background: rgba(30, 41, 59, 0.4);">
            <div class="card-title" style="color: #60a5fa; margin-bottom: 16px;">
                <span class="badge badge-blue">Insights</span> Leitura Executiva
            </div>

            <div style="display: flex; flex-direction: column; gap: 16px; flex: 1;">
                <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 16px;">
                    <div style="font-weight: 700; font-size: 15px; color: #ffffff; margin-bottom: 4px;">Qwen 0.5B responde a contratos</div>
                    <div style="font-size: 13px; color: #94a3b8; line-height: 1.5;">
                        Subiu de <strong>0.411</strong> para <strong>0.741</strong> (+80.2% de ganho). Exemplos few-shot ancoraram estrutura e prioridade sem perda de semântica.
                    </div>
                </div>

                <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 16px;">
                    <div style="font-weight: 700; font-size: 15px; color: #ffffff; margin-bottom: 4px;">FLAN-T5 prefere checklists</div>
                    <div style="font-size: 13px; color: #94a3b8; line-height: 1.5;">
                        Obteve <strong>0.460</strong> com checklist (+72.6% vs base), mas falhou em seguir contratos JSON/chaves estritas devido ao teto do modelo seq2seq.
                    </div>
                </div>

                <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 12px; padding: 16px;">
                    <div style="font-weight: 700; font-size: 15px; color: #34d399; margin-bottom: 4px;">Princípio de Engenharia</div>
                    <div style="font-size: 13px; color: #cbd5e1; line-height: 1.5;">
                        O ganho não pertence apenas ao prompt nem apenas ao modelo: ele emerge da <strong>compatibilidade</strong> entre o desenho de instrução e a capacidade da arquitetura.
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 4: A matriz comparativa revela como cada arquitetura extrai valor de diferentes técnicas de prompt</div>
    </div>
</body>
</html>"""

TEMPLATES["0005_prompt_engineering_avancado/assets/06.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0005 • Prompt Engineering Avançado</div>
            <div class="title">A Escada de Evolução Técnica</div>
            <div class="subtitle">Critérios arquiteturais para saber quando evoluir de Prompt para RAG ou Fine-Tuning</div>
        </div>
        <div class="figure-badge">Figura 6</div>
    </div>

    <div class="main-content" style="flex-direction: column; justify-content: center; position: relative;">
        <!-- Indicador de Custo e Complexidade no topo -->
        <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 12px 24px; margin-bottom: 32px;">
            <span style="font-size: 13px; font-weight: 700; color: #60a5fa; text-transform: uppercase; letter-spacing: 0.06em;">Custo Mínimo • Iteração em Minutos</span>
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 320px; height: 6px; background: linear-gradient(90deg, #3b82f6, #8b5cf6, #f59e0b, #10b981); border-radius: 3px;"></div>
                <span style="font-size: 13px; color: #94a3b8; font-weight: 600;">➔ Complexidade, Latência e Custo Operacional Aumentam</span>
            </div>
            <span style="font-size: 13px; font-weight: 700; color: #34d399; text-transform: uppercase; letter-spacing: 0.06em;">Especialização Máxima em Escala</span>
        </div>

        <!-- Degraus da Escada -->
        <div style="display: flex; gap: 20px; align-items: flex-end; height: 480px;">
            <!-- Degrau 1 -->
            <div class="card" style="flex: 1; height: 260px; border-color: rgba(59, 130, 246, 0.4); background: rgba(59, 130, 246, 0.05); justify-content: space-between;">
                <div>
                    <div class="badge badge-blue" style="margin-bottom: 10px;">Passo 1 • Base</div>
                    <div style="font-size: 22px; font-weight: 800; color: #ffffff; margin-bottom: 8px;">Prompt Engineering</div>
                    <div style="font-size: 14px; color: #cbd5e1; line-height: 1.5;">
                        Contratos de saída, personas, restrições e few-shot. Resolve formato, concisão e alinhamento básico sem infraestrutura extra.
                    </div>
                </div>
                <div style="font-size: 12px; color: #93c5fd; font-weight: 600; border-top: 1px solid rgba(59,130,246,0.2); padding-top: 8px;">
                    Custo: Praticamente zero | Deploy: Imediato
                </div>
            </div>

            <!-- Degrau 2 -->
            <div class="card" style="flex: 1; height: 330px; border-color: rgba(139, 92, 246, 0.4); background: rgba(139, 92, 246, 0.05); justify-content: space-between;">
                <div>
                    <div class="badge badge-purple" style="margin-bottom: 10px;">Passo 2 • Contexto</div>
                    <div style="font-size: 22px; font-weight: 800; color: #ffffff; margin-bottom: 8px;">RAG Corporativo</div>
                    <div style="font-size: 14px; color: #cbd5e1; line-height: 1.5;">
                        Vector databases e embeddings para injetar dados proprietários dinâmicos. Quando o modelo precisa de fatos atualizados que ele desconhece.
                    </div>
                </div>
                <div style="font-size: 12px; color: #d8b4fe; font-weight: 600; border-top: 1px solid rgba(139,92,246,0.2); padding-top: 8px;">
                    Foco: Conhecimento dinâmico e citação factual
                </div>
            </div>

            <!-- Degrau 3 -->
            <div class="card" style="flex: 1; height: 400px; border-color: rgba(245, 158, 11, 0.4); background: rgba(245, 158, 11, 0.05); justify-content: space-between;">
                <div>
                    <div class="badge badge-amber" style="margin-bottom: 10px;">Passo 3 • Estilo</div>
                    <div style="font-size: 22px; font-weight: 800; color: #ffffff; margin-bottom: 8px;">Fine-Tuning (LoRA)</div>
                    <div style="font-size: 14px; color: #cbd5e1; line-height: 1.5;">
                        Treinamento supervisionado de pesos para incorporar jargão, regras estritas de raciocínio ou reduzir tokens de prompt em altíssimo volume de requisições.
                    </div>
                </div>
                <div style="font-size: 12px; color: #fde68a; font-weight: 600; border-top: 1px solid rgba(245,158,11,0.2); padding-top: 8px;">
                    Foco: Mudança comportamental perene
                </div>
            </div>

            <!-- Degrau 4 -->
            <div class="card" style="flex: 1; height: 470px; border-color: rgba(16, 185, 129, 0.4); background: rgba(16, 185, 129, 0.05); justify-content: space-between;">
                <div>
                    <div class="badge badge-emerald" style="margin-bottom: 10px;">Passo 4 • Escala</div>
                    <div style="font-size: 22px; font-weight: 800; color: #ffffff; margin-bottom: 8px;">Arquitetura Híbrida</div>
                    <div style="font-size: 14px; color: #cbd5e1; line-height: 1.5;">
                        Fusão de modelo ajustado com pipeline de RAG, guardrails sistêmicos e orquestração de ferramentas. Solução madura para sistemas críticos de missão corporativa.
                    </div>
                </div>
                <div style="font-size: 12px; color: #a7f3d0; font-weight: 600; border-top: 1px solid rgba(16,185,129,0.2); padding-top: 8px;">
                    Foco: Autonomia resiliente e observabilidade total
                </div>
            </div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 6: Só escale para RAG ou fine-tuning quando a engenharia de prompt tiver esgotado seu potencial</div>
    </div>
</body>
</html>"""

TEMPLATES["0005_prompt_engineering_avancado/assets/05.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0005 • Prompt Engineering Avançado</div>
            <div class="title">Leitura do Benchmark Multi-Modelo</div>
            <div class="subtitle">O ganho vem da estratégia de instrução e não apenas do tamanho ou capacidade do modelo</div>
        </div>
        <div class="figure-badge">Figura 5</div>
    </div>

    <div class="main-content" style="gap: 32px;">
        <!-- Card Qwen -->
        <div class="card" style="flex: 1; border-color: rgba(59, 130, 246, 0.35); background: rgba(59, 130, 246, 0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <div>
                    <span class="badge badge-blue">Chat / Causal LM</span>
                    <div style="font-size: 22px; font-weight: 800; color: #ffffff; margin-top: 6px;">Qwen 2.5 0.5B Instruct</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 24px; font-weight: 800; color: #60a5fa;">+80.2%</div>
                    <div style="font-size: 12px; color: #94a3b8;">ganho vs. baseline</div>
                </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 12px; flex: 1;">
                <div style="background: rgba(255,255,255,0.03); border-radius: 10px; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600; font-size: 14px;">1º few_shot</span>
                    <span style="font-weight: 800; font-size: 15px; color: #60a5fa;">0.741 (+0.330)</span>
                </div>
                <div style="background: rgba(255,255,255,0.03); border-radius: 10px; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600; font-size: 14px;">2º estruturado</span>
                    <span style="font-weight: 800; font-size: 15px; color: #93c5fd;">0.729 (+0.318)</span>
                </div>
                <div style="background: rgba(255,255,255,0.03); border-radius: 10px; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600; font-size: 14px;">3º checklist</span>
                    <span style="font-weight: 800; font-size: 15px; color: #cbd5e1;">0.605 (+0.194)</span>
                </div>
                <div style="background: rgba(255,255,255,0.03); border-radius: 10px; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600; font-size: 14px; color: #64748b;">4º base (baseline)</span>
                    <span style="font-weight: 800; font-size: 15px; color: #64748b;">0.411</span>
                </div>
            </div>

            <div style="margin-top: 16px; padding: 12px; background: rgba(59, 130, 246, 0.1); border-radius: 10px; font-size: 13px; color: #bfdbfe; line-height: 1.5;">
                <strong>Comportamento:</strong> Absorve contratos rígidos com facilidade. Exemplos no prompt estabilizam a inferência e elevam os scores de formato e prioridade sem degradar a semântica.
            </div>
        </div>

        <!-- Card FLAN-T5 -->
        <div class="card" style="flex: 1; border-color: rgba(248, 113, 113, 0.35); background: rgba(248, 113, 113, 0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <div>
                    <span class="badge badge-rose">Seq2Seq LM</span>
                    <div style="font-size: 22px; font-weight: 800; color: #ffffff; margin-top: 6px;">Google FLAN-T5 Small</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 24px; font-weight: 800; color: #f87171;">+72.6%</div>
                    <div style="font-size: 12px; color: #94a3b8;">ganho vs. baseline</div>
                </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 12px; flex: 1;">
                <div style="background: rgba(255,255,255,0.03); border-radius: 10px; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600; font-size: 14px;">1º checklist</span>
                    <span style="font-weight: 800; font-size: 15px; color: #f87171;">0.460 (+0.193)</span>
                </div>
                <div style="background: rgba(255,255,255,0.03); border-radius: 10px; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600; font-size: 14px;">2º few_shot</span>
                    <span style="font-weight: 800; font-size: 15px; color: #fca5a5;">0.278 (+0.011)</span>
                </div>
                <div style="background: rgba(255,255,255,0.03); border-radius: 10px; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600; font-size: 14px;">3º estruturado</span>
                    <span style="font-weight: 800; font-size: 15px; color: #fca5a5;">0.270 (+0.004)</span>
                </div>
                <div style="background: rgba(255,255,255,0.03); border-radius: 10px; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600; font-size: 14px; color: #64748b;">4º base (baseline)</span>
                    <span style="font-weight: 800; font-size: 15px; color: #64748b;">0.266</span>
                </div>
            </div>

            <div style="margin-top: 16px; padding: 12px; background: rgba(248, 113, 113, 0.1); border-radius: 10px; font-size: 13px; color: #fecaca; line-height: 1.5;">
                <strong>Comportamento:</strong> Mantém boa semântica geral, mas tem grande dificuldade em emitir contratos com múltiplas linhas e chaves. O checklist ajuda a sequenciar o raciocínio.
            </div>
        </div>

        <!-- Card Síntese -->
        <div class="card" style="flex: 0.85; padding: 28px; background: rgba(16, 185, 129, 0.04); border-color: rgba(16, 185, 129, 0.3);">
            <div class="card-title" style="color: #34d399; margin-bottom: 12px;">
                <span class="badge badge-emerald">Conclusão</span> Síntese do Laboratório
            </div>

            <div style="display: flex; flex-direction: column; gap: 16px; font-size: 14px; line-height: 1.5; color: #cbd5e1;">
                <div>
                    <strong style="color: #ffffff;">1. Prompt Engineering funciona:</strong><br>
                    Ambos os modelos obtiveram ganhos superiores a 70% quando comparados à instrução livre.
                </div>
                <div>
                    <strong style="color: #ffffff;">2. Não existe prompt universal:</strong><br>
                    A estratégia vencedora para o Qwen (`few_shot`) foi diferente da vencedora para o FLAN (`checklist`).
                </div>
                <div>
                    <strong style="color: #ffffff;">3. Separe prompt de modelo:</strong><br>
                    Antes de migrar para modelos maiores ou pagar APIs caras, otimize a estrutura do prompt no modelo atual.
                </div>
            </div>

            <div style="margin-top: auto; padding: 12px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; font-size: 12px; color: #94a3b8; text-align: center;">
                Artefatos auditáveis: `benchmark_resumo.csv` e `benchmark_deltas.csv`
            </div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 5: Ranking executivo e comportamento detalhado por arquitetura de inferência</div>
    </div>
</body>
</html>"""

# ==========================================
# ARTIGO 0006: LLM EVALS E REGRESSÃO
# ==========================================

TEMPLATES["0006_llm_evals_regressao/assets/01.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0006 • LLM Evals e Regressão</div>
            <div class="title">Ranking Ponderado e Decisão de Release</div>
            <div class="subtitle">Por que o candidato com maior score global ainda pode ser reprovado para produção</div>
        </div>
        <div class="figure-badge">Figura 1</div>
    </div>

    <div class="main-content" style="gap: 36px;">
        <!-- Ranking Ponderado -->
        <div class="card" style="flex: 1.2; padding: 32px;">
            <div class="card-title" style="margin-bottom: 20px;">
                <span class="badge badge-blue">Harness de Evals</span> Ranking Ponderado de Candidatos
            </div>

            <div style="display: flex; flex-direction: column; gap: 24px; flex: 1; justify-content: center;">
                <!-- 1. flan_estruturado -->
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 15px; font-weight: 700; margin-bottom: 8px;">
                        <span>1º flan_estruturado <span style="font-size: 12px; color: #94a3b8; font-weight: 400;">(google/flan-t5-small)</span></span>
                        <span style="color: #34d399; font-size: 16px;">1.357 score ponderado</span>
                    </div>
                    <div style="background: rgba(255,255,255,0.05); border-radius: 8px; height: 32px; overflow: hidden; display: flex;">
                        <div style="width: 85%; background: linear-gradient(90deg, #059669, #10b981); border-radius: 8px; display: flex; align-items: center; justify-content: flex-end; padding-right: 14px; font-weight: 800; font-size: 14px;">1.357</div>
                    </div>
                </div>

                <!-- 2. qwen_generico -->
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 15px; font-weight: 700; margin-bottom: 8px;">
                        <span>2º qwen_generico <span style="font-size: 12px; color: #60a5fa; font-weight: 600;">[BASELINE]</span> <span style="font-size: 12px; color: #94a3b8; font-weight: 400;">(Qwen 0.5B)</span></span>
                        <span style="color: #60a5fa; font-size: 16px;">0.932 score ponderado</span>
                    </div>
                    <div style="background: rgba(255,255,255,0.05); border-radius: 8px; height: 32px; overflow: hidden; display: flex;">
                        <div style="width: 58%; background: linear-gradient(90deg, #2563eb, #3b82f6); border-radius: 8px; display: flex; align-items: center; justify-content: flex-end; padding-right: 14px; font-weight: 800; font-size: 14px;">0.932</div>
                    </div>
                </div>

                <!-- 3. qwen_estruturado -->
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 15px; font-weight: 700; margin-bottom: 8px;">
                        <span>3º qwen_estruturado <span style="font-size: 12px; color: #94a3b8; font-weight: 400;">(Qwen 0.5B)</span></span>
                        <span style="color: #f87171; font-size: 16px;">0.930 score ponderado</span>
                    </div>
                    <div style="background: rgba(255,255,255,0.05); border-radius: 8px; height: 32px; overflow: hidden; display: flex;">
                        <div style="width: 57.5%; background: linear-gradient(90deg, #dc2626, #f87171); border-radius: 8px; display: flex; align-items: center; justify-content: flex-end; padding-right: 14px; font-weight: 800; font-size: 14px;">0.930</div>
                    </div>
                </div>
            </div>

            <div style="font-size: 13px; color: #64748b; margin-top: 16px;">
                * Ponderação por Criticidade: Alta (1.5x) • Média (1.0x) • Baixa (0.8x)
            </div>
        </div>

        <!-- Decisão de Release -->
        <div class="card" style="flex: 1; padding: 32px; border-color: rgba(239, 68, 68, 0.4); background: rgba(239, 68, 68, 0.04);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <div class="card-title" style="color: #f87171; margin-bottom: 0;">Gate de Release CI/CD</div>
                <span class="badge badge-rose" style="font-size: 13px; padding: 6px 12px;">Reprovado</span>
            </div>

            <div style="background: rgba(239, 68, 68, 0.12); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 14px; padding: 20px; margin-bottom: 20px;">
                <div style="font-size: 18px; font-weight: 800; color: #ffffff; margin-bottom: 6px;">2 Regressões Críticas Detectadas</div>
                <div style="font-size: 14px; color: #fca5a5; line-height: 1.5;">
                    O candidato <code>qwen_estruturado</code> apresentou piora severa de desempenho nos cenários contratuais mais sensíveis da empresa.
                </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 12px; flex: 1;">
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 12px 16px;">
                    <div style="font-size: 13px; font-weight: 700; color: #fca5a5;">Caso 1: 'Como emitir segunda via?'</div>
                    <div style="font-size: 13px; color: #94a3b8;">Delta contra baseline: <strong style="color: #ef4444;">-0.200 pontos</strong></div>
                </div>
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 12px 16px;">
                    <div style="font-size: 13px; font-weight: 700; color: #fca5a5;">Caso 2: 'Posso cancelar sem multa?'</div>
                    <div style="font-size: 13px; color: #94a3b8;">Delta contra baseline: <strong style="color: #ef4444;">-0.205 pontos</strong></div>
                </div>
            </div>

            <div style="margin-top: 20px; padding: 12px; background: rgba(239, 68, 68, 0.15); border-radius: 8px; font-size: 13px; color: #fecaca; text-align: center; font-weight: 600;">
                Regra Inegociável: Ganho médio não autoriza regressão em alta criticidade
            </div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 1: A esteira de avaliação ponderada barra releases que introduzem regressões em fluxos críticos</div>
    </div>
</body>
</html>"""

TEMPLATES["0006_llm_evals_regressao/assets/03.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0006 • LLM Evals e Regressão</div>
            <div class="title">Scorecard de Avaliação Multidimensional</div>
            <div class="subtitle">As quatro dimensões fundamentais para quantificar a prontidão de LLMs em produção</div>
        </div>
        <div class="figure-badge">Figura 3</div>
    </div>

    <div class="main-content" style="display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 24px;">
        <!-- Card 1: Relevancia -->
        <div class="card" style="border-left: 6px solid #3b82f6;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <div class="card-title" style="color: #60a5fa; margin-bottom: 0;">1. Relevância Semântica</div>
                <span class="badge badge-blue">Similaridade Vetorial</span>
            </div>
            <div class="card-desc" style="font-size: 15px; color: #cbd5e1; flex: 1;">
                Avalia se a resposta gerada captura o significado central e responde à dúvida real do cliente, comparando o embedding da geração com o embedding da resposta ideal validada por especialistas.
            </div>
            <div style="background: rgba(59, 130, 246, 0.1); border-radius: 10px; padding: 12px 16px; font-size: 13px; color: #93c5fd;">
                <strong>Implementação:</strong> <code>SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')</code> com cosseno normalizado.
            </div>
        </div>

        <!-- Card 2: Completude -->
        <div class="card" style="border-left: 6px solid #8b5cf6;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <div class="card-title" style="color: #c084fc; margin-bottom: 0;">2. Completude de Termos</div>
                <span class="badge badge-purple">Keyword Recall</span>
            </div>
            <div class="card-desc" style="font-size: 15px; color: #cbd5e1; flex: 1;">
                Verifica se termos mandatórios de negócio (prazos contratuais, números de dias, rotas de telas, avisos de multa) foram expressamente mencionados na resposta gerada pelo modelo.
            </div>
            <div style="background: rgba(139, 92, 246, 0.1); border-radius: 10px; padding: 12px 16px; font-size: 13px; color: #d8b4fe;">
                <strong>Implementação:</strong> Intersecção exata com <code>palavras_criticas</code> definidas no dataset de homologação.
            </div>
        </div>

        <!-- Card 3: Faithfulness -->
        <div class="card" style="border-left: 6px solid #10b981;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <div class="card-title" style="color: #34d399; margin-bottom: 0;">3. Faithfulness (Fidelidade)</div>
                <span class="badge badge-emerald">Zero Alucinação</span>
            </div>
            <div class="card-desc" style="font-size: 15px; color: #cbd5e1; flex: 1;">
                Mede se a informação proferida pelo LLM é estritamente sustentada pelo contexto fornecido, penalizando alucinações, promessas descabidas ou dados inventados pela rede.
            </div>
            <div style="background: rgba(16, 185, 129, 0.1); border-radius: 10px; padding: 12px 16px; font-size: 13px; color: #a7f3d0;">
                <strong>Implementação:</strong> Razão de tokens informativos (len > 4) validados no texto do contexto documental.
            </div>
        </div>

        <!-- Card 4: Consistência -->
        <div class="card" style="border-left: 6px solid #f59e0b;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <div class="card-title" style="color: #fbbf24; margin-bottom: 0;">4. Score Ponderado</div>
                <span class="badge badge-amber">Criticidade de Risco</span>
            </div>
            <div class="card-desc" style="font-size: 15px; color: #cbd5e1; flex: 1;">
                Aplica multiplicadores de impacto: falhas em fluxos de alta criticidade (política jurídica, cobrança) recebem peso <strong>1.5x</strong>, enquanto dúvidas rotineiras recebem peso <strong>0.8x</strong>.
            </div>
            <div style="background: rgba(245, 158, 11, 0.1); border-radius: 10px; padding: 12px 16px; font-size: 13px; color: #fde68a;">
                <strong>Implementação:</strong> <code>score_final * CRITICALITY_WEIGHTS[criticidade]</code> calibrado para governança de release.
            </div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 3: Dimensões quantitativas que substituem o julgamento humano subjetivo por métricas reproduzíveis</div>
    </div>
</body>
</html>"""

TEMPLATES["0006_llm_evals_regressao/assets/02.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0006 • LLM Evals e Regressão</div>
            <div class="title">Dataset de Avaliação Estruturado</div>
            <div class="subtitle">A base de testes carrega contexto factual, palavras-chave mandatórias e nível de criticidade</div>
        </div>
        <div class="figure-badge">Figura 2</div>
    </div>

    <div class="main-content" style="flex-direction: column;">
        <div class="card" style="flex: 1; padding: 24px; overflow: hidden;">
            <table style="width: 100%; border-collapse: separate; border-spacing: 0; font-size: 14px; text-align: left;">
                <thead>
                    <tr style="background: rgba(255, 255, 255, 0.04); color: #94a3b8; font-size: 12px; text-transform: uppercase; letter-spacing: 0.06em;">
                        <th style="padding: 14px 18px; border-bottom: 1px solid rgba(255,255,255,0.1); border-top-left-radius: 10px;">Pergunta do Usuário</th>
                        <th style="padding: 14px 18px; border-bottom: 1px solid rgba(255,255,255,0.1);">Contexto Fornecido (Fonte Factual)</th>
                        <th style="padding: 14px 18px; border-bottom: 1px solid rgba(255,255,255,0.1);">Gabarito (Gold Standard)</th>
                        <th style="padding: 14px 18px; border-bottom: 1px solid rgba(255,255,255,0.1);">Categoria</th>
                        <th style="padding: 14px 18px; border-bottom: 1px solid rgba(255,255,255,0.1); border-top-right-radius: 10px;">Criticidade</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.05); background: rgba(255,255,255,0.01);">
                        <td style="padding: 16px 18px; font-weight: 600; color: #ffffff;">Qual é o prazo de devolução?</td>
                        <td style="padding: 16px 18px; color: #94a3b8;">"Política permite estorno em até 30 dias corridos para produto sem uso..."</td>
                        <td style="padding: 16px 18px; color: #34d399;">"30 dias corridos para produtos sem uso e embalagem preservada."</td>
                        <td style="padding: 16px 18px;"><span class="badge badge-blue">política</span></td>
                        <td style="padding: 16px 18px;"><span class="badge badge-rose">alta (1.5x)</span></td>
                    </tr>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.05); background: rgba(255,255,255,0.02);">
                        <td style="padding: 16px 18px; font-weight: 600; color: #ffffff;">Como emitir segunda via da fatura?</td>
                        <td style="padding: 16px 18px; color: #94a3b8;">"Acesse o portal do cliente, abra a aba Financeiro e clique em Segunda Via."</td>
                        <td style="padding: 16px 18px; color: #34d399;">"Portal do cliente > Financeiro > Segunda Via."</td>
                        <td style="padding: 16px 18px;"><span class="badge badge-purple">financeiro</span></td>
                        <td style="padding: 16px 18px;"><span class="badge badge-rose">alta (1.5x)</span></td>
                    </tr>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.05); background: rgba(255,255,255,0.01);">
                        <td style="padding: 16px 18px; font-weight: 600; color: #ffffff;">Posso cancelar sem multa?</td>
                        <td style="padding: 16px 18px; color: #94a3b8;">"Cancelamento sem multa vale por até 7 dias corridos após a contratação."</td>
                        <td style="padding: 16px 18px; color: #34d399;">"Até 7 dias corridos. Após o prazo, aplica-se a multa contratual."</td>
                        <td style="padding: 16px 18px;"><span class="badge badge-amber">contrato</span></td>
                        <td style="padding: 16px 18px;"><span class="badge badge-rose">alta (1.5x)</span></td>
                    </tr>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.05); background: rgba(255,255,255,0.02);">
                        <td style="padding: 16px 18px; font-weight: 600; color: #ffffff;">Erro 500 no aplicativo móvel</td>
                        <td style="padding: 16px 18px; color: #94a3b8;">"Falhas técnicas persistentes devem abrir chamado com prioridade alta."</td>
                        <td style="padding: 16px 18px; color: #34d399;">"Abrir ticket técnico de suporte com prioridade alta em 1h."</td>
                        <td style="padding: 16px 18px;"><span class="badge badge-blue">suporte</span></td>
                        <td style="padding: 16px 18px;"><span class="badge badge-amber">média (1.0x)</span></td>
                    </tr>
                    <tr style="background: rgba(255,255,255,0.01);">
                        <td style="padding: 16px 18px; font-weight: 600; color: #ffffff;">Vocês têm plano corporativo?</td>
                        <td style="padding: 16px 18px; color: #94a3b8;">"Planos empresariais contam com SLA dedicado e gestor de conta."</td>
                        <td style="padding: 16px 18px; color: #34d399;">"Sim, planos corporativos têm SLA dedicado e atendimento customizado."</td>
                        <td style="padding: 16px 18px;"><span class="badge badge-purple">comercial</span></td>
                        <td style="padding: 16px 18px;"><span class="badge badge-emerald">baixa (0.8x)</span></td>
                    </tr>
                </tbody>
            </table>

            <div style="margin-top: 24px; padding: 16px 20px; background: rgba(37, 99, 235, 0.08); border: 1px solid rgba(37, 99, 235, 0.25); border-radius: 12px; display: flex; align-items: center; justify-content: space-between;">
                <div style="font-size: 14px; color: #bfdbfe;">
                    <strong>Governança de Dados:</strong> O dataset classifica impacto por domínio e criticidade. Isso impede que perguntas fáceis mas irrelevantes mascarem falhas em processos vitais.
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #60a5fa;">
                    data/eval_dataset.csv
                </div>
            </div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 2: Estrutura do dataset de homologação com gabarito ideal e ponderação de risco de negócio</div>
    </div>
</body>
</html>"""

TEMPLATES["0006_llm_evals_regressao/assets/04.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0006 • LLM Evals e Regressão</div>
            <div class="title">Gate de Release com Score e Regressão Crítica</div>
            <div class="subtitle">Fluxo automatizado de decisão para aprovação ou bloqueio de deploy em pipelines de CI/CD</div>
        </div>
        <div class="figure-badge">Figura 4</div>
    </div>

    <div class="main-content" style="flex-direction: column; justify-content: center; gap: 32px;">
        <!-- Fases da Esteira -->
        <div style="display: flex; gap: 20px; align-items: center;">
            <div class="card" style="flex: 1; padding: 22px; border-top: 4px solid #3b82f6;">
                <div style="font-size: 12px; font-weight: 700; color: #60a5fa; text-transform: uppercase;">Etapa 1</div>
                <div style="font-size: 18px; font-weight: 800; color: #ffffff; margin: 4px 0;">Executar Harness</div>
                <div style="font-size: 13px; color: #94a3b8;">Gera respostas do candidato e da baseline no dataset versionado.</div>
            </div>

            <div style="font-size: 24px; color: #475569;">➔</div>

            <div class="card" style="flex: 1; padding: 22px; border-top: 4px solid #8b5cf6;">
                <div style="font-size: 12px; font-weight: 700; color: #c084fc; text-transform: uppercase;">Etapa 2</div>
                <div style="font-size: 18px; font-weight: 800; color: #ffffff; margin: 4px 0;">Calcular Scores</div>
                <div style="font-size: 13px; color: #94a3b8;">Semântica, recall de palavras-chave, fidelidade e pesos de criticidade.</div>
            </div>

            <div style="font-size: 24px; color: #475569;">➔</div>

            <div class="card" style="flex: 1; padding: 22px; border-top: 4px solid #f59e0b;">
                <div style="font-size: 12px; font-weight: 700; color: #fbbf24; text-transform: uppercase;">Etapa 3</div>
                <div style="font-size: 18px; font-weight: 800; color: #ffffff; margin: 4px 0;">Análise de Regressão</div>
                <div style="font-size: 13px; color: #94a3b8;">Compara caso a caso com a baseline (alerta se delta &lt; -0.05).</div>
            </div>
        </div>

        <!-- Fork de Decisao -->
        <div style="display: flex; gap: 28px;">
            <!-- Caminho de Aprovacao -->
            <div class="card" style="flex: 1; border-color: rgba(16, 185, 129, 0.4); background: rgba(16, 185, 129, 0.04); padding: 28px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                    <div style="font-size: 20px; font-weight: 800; color: #34d399;">Critério de Aprovação</div>
                    <span class="badge badge-emerald">Release Seguro</span>
                </div>
                <div style="font-size: 14px; color: #cbd5e1; line-height: 1.6; margin-bottom: 20px;">
                    1. <strong>Ganho ponderado global &ge; +0.05 pontos</strong> em relação à baseline em produção.<br>
                    2. <strong>Zero regressões</strong> em casos marcados com criticidade alta (jurídico, financeiro, regras de estorno).
                </div>
                <div style="padding: 16px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 12px; font-weight: 800; font-size: 18px; color: #34d399; text-align: center; letter-spacing: 0.04em;">
                    ✓ APROVAR RELEASE PARA PRODUÇÃO
                </div>
            </div>

            <!-- Caminho de Bloqueio -->
            <div class="card" style="flex: 1; border-color: rgba(239, 68, 68, 0.4); background: rgba(239, 68, 68, 0.04); padding: 28px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                    <div style="font-size: 20px; font-weight: 800; color: #f87171;">Critério de Bloqueio</div>
                    <span class="badge badge-rose">Stop-the-Line</span>
                </div>
                <div style="font-size: 14px; color: #cbd5e1; line-height: 1.6; margin-bottom: 20px;">
                    1. <strong>Queda no score global</strong> ou ganho insuficiente para justificar a substituição de modelo.<br>
                    2. <strong>Qualquer regressão em caso crítico</strong>, mesmo que a média agregada pareça vitoriosa no ranking geral.
                </div>
                <div style="padding: 16px; background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 12px; font-weight: 800; font-size: 18px; color: #f87171; text-align: center; letter-spacing: 0.04em;">
                    ✗ BLOQUEAR RELEASE E ACIONAR ALERTA
                </div>
            </div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 4: A esteira automatizada protege a operação contra degradações silenciosas de modelo e prompt</div>
    </div>
</body>
</html>"""

TEMPLATES["0006_llm_evals_regressao/assets/05.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0006 • LLM Evals e Regressão</div>
            <div class="title">Artefatos Produzidos pela Esteira de Evals</div>
            <div class="subtitle">Ecossistema de arquivos estruturados que tornam cada ciclo de homologação 100% auditável</div>
        </div>
        <div class="figure-badge">Figura 5</div>
    </div>

    <div class="main-content" style="flex-direction: column; gap: 16px; justify-content: space-around;">
        <!-- Arquivo 1 -->
        <div class="card" style="padding: 16px 24px; flex-direction: row; align-items: center; justify-content: space-between; border-left: 6px solid #3b82f6;">
            <div style="display: flex; align-items: center; gap: 18px; width: 440px;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 15px; font-weight: 700; color: #60a5fa;">geracoes_evals.csv</div>
            </div>
            <div style="flex: 1; font-size: 14px; color: #cbd5e1;">
                Contém todas as respostas brutas geradas por cada candidato para cada pergunta, com scores individuais de semântica, recall e fidelidade.
            </div>
            <span class="badge badge-blue">Log Forense Bruto</span>
        </div>

        <!-- Arquivo 2 -->
        <div class="card" style="padding: 16px 24px; flex-direction: row; align-items: center; justify-content: space-between; border-left: 6px solid #8b5cf6;">
            <div style="display: flex; align-items: center; gap: 18px; width: 440px;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 15px; font-weight: 700; color: #c084fc;">candidate_summary.csv</div>
            </div>
            <div style="flex: 1; font-size: 14px; color: #cbd5e1;">
                Tabela consolidada de ranking com médias agregadas, permitindo ordenar candidatos por score ponderado e fidelidade factual ao contexto.
            </div>
            <span class="badge badge-purple">Ranking Consolidado</span>
        </div>

        <!-- Arquivo 3 -->
        <div class="card" style="padding: 16px 24px; flex-direction: row; align-items: center; justify-content: space-between; border-left: 6px solid #f59e0b;">
            <div style="display: flex; align-items: center; gap: 18px; width: 440px;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 15px; font-weight: 700; color: #fbbf24;">candidate_summary_by_category.csv</div>
            </div>
            <div style="flex: 1; font-size: 14px; color: #cbd5e1;">
                Performance desagregada por domínio (política, suporte, financeiro, contratos). Identifica se um modelo é bom no suporte, mas falha em contratos.
            </div>
            <span class="badge badge-amber">Desempenho por Domínio</span>
        </div>

        <!-- Arquivo 4 -->
        <div class="card" style="padding: 16px 24px; flex-direction: row; align-items: center; justify-content: space-between; border-left: 6px solid #ef4444;">
            <div style="display: flex; align-items: center; gap: 18px; width: 440px;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 15px; font-weight: 700; color: #f87171;">regressoes_detectadas.csv</div>
            </div>
            <div style="flex: 1; font-size: 14px; color: #cbd5e1;">
                Lista detalhada dos casos específicos em que o candidato teve desempenho inferior à baseline em produção (delta negativo expressivo).
            </div>
            <span class="badge badge-rose">Casos Regredidos</span>
        </div>

        <!-- Arquivo 5 -->
        <div class="card" style="padding: 16px 24px; flex-direction: row; align-items: center; justify-content: space-between; border-left: 6px solid #10b981;">
            <div style="display: flex; align-items: center; gap: 18px; width: 440px;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 15px; font-weight: 700; color: #34d399;">relatorio_evals.md</div>
            </div>
            <div style="flex: 1; font-size: 14px; color: #cbd5e1;">
                Sumário executivo legível para o time de produto e engenharia com status final do gate (aprovado/reprovado), métricas chave e veredicto.
            </div>
            <span class="badge badge-emerald">Veredicto Executivo</span>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 5: Todos os artefatos são salvos na pasta data/ para integração contínua e rastreabilidade total</div>
    </div>
</body>
</html>"""

# ==========================================
# ARTIGO 0007: AGENTES E TOOL CALLING
# ==========================================

TEMPLATES["0007_agentes_tool_calling/assets/01.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0007 • Agentes e Tool Calling</div>
            <div class="title">Pipeline Tradicional vs. Agente Autônomo</div>
            <div class="subtitle">Execução sequencial determinística vs. Raciocínio dinâmico orientado a objetivos</div>
        </div>
        <div class="figure-badge">Figura 1</div>
    </div>

    <div class="main-content">
        <!-- Lado Pipeline Fixo -->
        <div class="card" style="flex: 1; border-color: rgba(59, 130, 246, 0.3); background: rgba(59, 130, 246, 0.02); padding: 32px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <div class="card-title" style="color: #60a5fa; margin-bottom: 0;">
                    <span class="badge badge-blue">Determinístico</span> Pipeline Tradicional
                </div>
                <span style="font-size: 13px; color: #94a3b8;">Sequência Estática</span>
            </div>

            <div style="display: flex; flex-direction: column; gap: 16px; flex: 1; justify-content: center; align-items: center;">
                <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 18px 24px; width: 100%; text-align: center; font-weight: 700; font-size: 16px;">
                    1. Ler Arquivo / Payload
                </div>
                <div style="color: #60a5fa; font-size: 20px;">↓</div>
                <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 18px 24px; width: 100%; text-align: center; font-weight: 700; font-size: 16px;">
                    2. Extrair Entidades com LLM
                </div>
                <div style="color: #60a5fa; font-size: 20px;">↓</div>
                <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 18px 24px; width: 100%; text-align: center; font-weight: 700; font-size: 16px;">
                    3. Gravar Registro no Banco de Dados
                </div>
            </div>

            <div style="margin-top: 20px; padding: 12px 16px; background: rgba(59, 130, 246, 0.1); border-radius: 10px; font-size: 13px; color: #93c5fd; line-height: 1.5;">
                <strong>Características:</strong> Fluxo rígido. Se o usuário fizer uma pergunta fora do roteiro ou precisar de checagem condicional, o pipeline quebra ou falha silenciosamente.
            </div>
        </div>

        <!-- Lado Agente Autonomo -->
        <div class="card" style="flex: 1; border-color: rgba(16, 185, 129, 0.3); background: rgba(16, 185, 129, 0.02); padding: 32px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <div class="card-title" style="color: #34d399; margin-bottom: 0;">
                    <span class="badge badge-emerald">Orientado a Objetivo</span> Agente Autônomo
                </div>
                <span style="font-size: 13px; color: #34d399; font-weight: 600;">Loop ReAct</span>
            </div>

            <div style="display: flex; flex-direction: column; gap: 14px; flex: 1; justify-content: center; align-items: center;">
                <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 14px 20px; width: 100%; text-align: center; font-weight: 700; font-size: 15px; color: #a7f3d0;">
                    Objetivo do Usuário: "Quero 2ª via da fatura deste mês"
                </div>

                <div style="color: #34d399; font-size: 18px;">↓</div>

                <!-- Loop Box -->
                <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 16px; padding: 18px 24px; width: 100%; position: relative;">
                    <div style="position: absolute; top: -10px; right: 18px; background: #059669; color: white; font-size: 10px; font-weight: 800; padding: 2px 8px; border-radius: 4px; text-transform: uppercase;">
                        Ciclo Dinâmico
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 10px; font-size: 13px;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="color: #34d399; font-weight: 700;">1. Raciocinar (Think):</span> O que o usuário precisa?
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="color: #60a5fa; font-weight: 700;">2. Agir (Action):</span> Chamar ferramenta <code>buscar_politica</code>
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="color: #fbbf24; font-weight: 700;">3. Observar (Observe):</span> Analisar retorno da ferramenta
                        </div>
                    </div>
                </div>

                <div style="color: #34d399; font-size: 18px;">↓</div>

                <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 14px 20px; width: 100%; text-align: center; font-weight: 700; font-size: 15px; color: #a7f3d0;">
                    Resposta Sintetizada com Base Factual
                </div>
            </div>

            <div style="margin-top: 20px; padding: 12px 16px; background: rgba(16, 185, 129, 0.1); border-radius: 10px; font-size: 13px; color: #a7f3d0; line-height: 1.5;">
                <strong>Características:</strong> Decide dinamicamente se precisa consultar a base, abrir um chamado técnico ou responder direto, adaptando-se ao contexto em tempo de execução.
            </div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 1: A diferença entre execução sequencial e agentes orientados a objetivos com capacidade de decisão</div>
    </div>
</body>
</html>"""

TEMPLATES["0007_agentes_tool_calling/assets/03.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0007 • Agentes e Tool Calling</div>
            <div class="title">Roteamento Híbrido Multi-Camadas</div>
            <div class="subtitle">Como combinar regras determinísticas, planejamento de LLM e fallback semântico resiliente</div>
        </div>
        <div class="figure-badge">Figura 3</div>
    </div>

    <div class="main-content" style="align-items: center; justify-content: space-between; gap: 24px;">
        <!-- Entrada -->
        <div class="card" style="width: 220px; padding: 22px; text-align: center; border-color: rgba(255,255,255,0.15);">
            <div style="font-size: 12px; font-weight: 700; color: #94a3b8; text-transform: uppercase;">Entrada</div>
            <div style="font-size: 18px; font-weight: 800; color: #ffffff; margin-top: 6px;">Mensagem do Usuário</div>
        </div>

        <div style="font-size: 22px; color: #64748b;">➔</div>

        <!-- Guardrail -->
        <div class="card" style="width: 240px; padding: 22px; text-align: center; border-color: rgba(239, 68, 68, 0.4); background: rgba(239, 68, 68, 0.05);">
            <span class="badge badge-rose" style="margin-bottom: 6px;">Segurança</span>
            <div style="font-size: 18px; font-weight: 800; color: #ffffff;">Guardrail Ativo</div>
            <div style="font-size: 12px; color: #fca5a5; margin-top: 4px;">Bloqueio de credenciais e termos sensíveis</div>
        </div>

        <div style="font-size: 22px; color: #64748b;">➔</div>

        <!-- 3 Caminhos de Roteamento -->
        <div style="display: flex; flex-direction: column; gap: 14px; width: 440px;">
            <!-- Tier 1 -->
            <div style="background: rgba(16, 185, 129, 0.06); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 14px 18px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 14px; font-weight: 800; color: #34d399;">1. Regra de Negócio (Rápida)</div>
                    <div style="font-size: 12px; color: #94a3b8;">Captura intenções óbvias (fatura, erro 500)</div>
                </div>
                <span class="badge badge-emerald">0ms LLM</span>
            </div>

            <!-- Tier 2 -->
            <div style="background: rgba(59, 130, 246, 0.06); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 12px; padding: 14px 18px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 14px; font-weight: 800; color: #60a5fa;">2. Planner JSON (Qwen 0.5B)</div>
                    <div style="font-size: 12px; color: #94a3b8;">Gera JSON com tool, argument e reason</div>
                </div>
                <span class="badge badge-blue">Inteligência</span>
            </div>

            <!-- Tier 3 -->
            <div style="background: rgba(245, 158, 11, 0.06); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 12px; padding: 14px 18px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 14px; font-weight: 800; color: #fbbf24;">3. Fallback por Embeddings</div>
                    <div style="font-size: 12px; color: #94a3b8;">Assume se o planner gerar JSON inválido</div>
                </div>
                <span class="badge badge-amber">Resiliência</span>
            </div>
        </div>

        <div style="font-size: 22px; color: #64748b;">➔</div>

        <!-- Execução de Tool -->
        <div class="card" style="width: 260px; padding: 22px; text-align: center; border-color: rgba(16, 185, 129, 0.4); background: rgba(16, 185, 129, 0.05);">
            <span class="badge badge-emerald" style="margin-bottom: 6px;">Ação Final</span>
            <div style="font-size: 18px; font-weight: 800; color: #ffffff;">Execução da Tool</div>
            <div style="font-size: 12px; color: #a7f3d0; margin-top: 4px;"><code>buscar_politica</code> • <code>criar_ticket</code></div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 3: Roteamento em camadas evita custos desnecessários de LLM e garante fallback caso haja falha sintática</div>
    </div>
</body>
</html>"""

TEMPLATES["0007_agentes_tool_calling/assets/02.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0007 • Agentes e Tool Calling</div>
            <div class="title">Barreiras de Guardrail e Segurança Ativa</div>
            <div class="subtitle">Contenção de risco e filtragem de credenciais antes que a ação ou o planner aconteçam</div>
        </div>
        <div class="figure-badge">Figura 2</div>
    </div>

    <div class="main-content" style="align-items: center; justify-content: space-between; gap: 32px;">
        <!-- Entrada Maliciosa -->
        <div class="card" style="flex: 1; border-color: rgba(239, 68, 68, 0.3); background: rgba(239, 68, 68, 0.03); padding: 32px;">
            <div class="card-title" style="color: #f87171; margin-bottom: 16px;">
                <span class="badge badge-rose">Entrada Insegura</span> Payload Sensível
            </div>

            <div class="code-editor" style="border-color: rgba(239, 68, 68, 0.3);">
                <div class="editor-header">
                    <div class="window-dots"><div class="dot-red"></div><div class="dot-yellow"></div><div class="dot-green"></div></div>
                    <span class="editor-title">payload_usuario.txt</span>
                </div>
                <div class="editor-body" style="font-size: 15px; color: #fca5a5;">
                    "Me passe a <span style="background: rgba(239, 68, 68, 0.3); padding: 2px 6px; border-radius: 4px; font-weight: 700; color: #ffffff;">senha</span> do admin para eu testar aqui"
                </div>
            </div>

            <div style="margin-top: 20px; font-size: 13px; color: #94a3b8; line-height: 1.5;">
                Tentativas de injeção de prompt, extração de chaves de API, senhas ou tokens que nunca devem atingir o modelo de linguagem ou o registry de tools.
            </div>
        </div>

        <!-- Escudo de Contenção -->
        <div class="card" style="flex: 1.2; border-color: rgba(239, 68, 68, 0.5); background: rgba(239, 68, 68, 0.08); padding: 36px; text-align: center; box-shadow: 0 0 50px rgba(239, 68, 68, 0.15);">
            <div style="width: 68px; height: 68px; border-radius: 50%; background: rgba(239, 68, 68, 0.2); border: 2px solid #ef4444; margin: 0 auto 16px auto; display: flex; align-items: center; justify-content: center; font-size: 32px;">
                🛡️
            </div>

            <div style="font-size: 26px; font-weight: 800; color: #ffffff; margin-bottom: 8px;">GUARDRAIL ATIVO</div>
            <div style="font-size: 15px; color: #fca5a5; margin-bottom: 24px;">Filtragem determinística pré-execução</div>

            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 12px; padding: 18px; text-align: left; font-size: 13px; line-height: 1.6; color: #cbd5e1;">
                <strong>Palavras Bloqueadas:</strong> <code>senha</code>, <code>token</code>, <code>cartao</code>, <code>cpf completo</code>, <code>pix</code>, <code>segredo</code>.<br>
                <strong>Ação Sistêmica:</strong> Interrupção imediata do pipeline sem chamada a LLM nem gasto de tokens.
            </div>
        </div>

        <!-- Ação Bloqueada -->
        <div class="card" style="flex: 1; border-color: rgba(255, 255, 255, 0.1); background: rgba(15, 23, 42, 0.5); padding: 32px;">
            <div class="card-title" style="color: #cbd5e1; margin-bottom: 16px;">
                <span class="badge badge-rose">Interrompido</span> Resultado Seguro
            </div>

            <div class="code-editor" style="border-color: rgba(255, 255, 255, 0.1);">
                <div class="editor-header">
                    <div class="window-dots"><div class="dot-red"></div><div class="dot-yellow"></div><div class="dot-green"></div></div>
                    <span class="editor-title">audit_log.json</span>
                </div>
                <div class="editor-body" style="font-size: 14px; color: #e2e8f0; line-height: 1.6;">
                    <span style="color: #64748b;">&#123;</span><br>
                    &nbsp;&nbsp;<span style="color: #38bdf8;">"status"</span>: <span style="color: #f87171;">"bloqueado"</span>,<br>
                    &nbsp;&nbsp;<span style="color: #38bdf8;">"motivo"</span>: <span style="color: #fca5a5;">"termo sensível 'senha'"</span>,<br>
                    &nbsp;&nbsp;<span style="color: #38bdf8;">"tools_acionadas"</span>: <span style="color: #fbbf24;">[]</span><br>
                    <span style="color: #64748b;">&#125;</span>
                </div>
            </div>

            <div style="margin-top: 20px; font-size: 13px; color: #10b981; font-weight: 600;">
                ✓ Nenhuma ferramenta corporativa foi exposta ou executada
            </div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 2: O guardrail atua como firewall antes do planner, contendo riscos com latência desprezível</div>
    </div>
</body>
</html>"""

TEMPLATES["0007_agentes_tool_calling/assets/04.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0007 • Agentes e Tool Calling</div>
            <div class="title">Arquitetura Completa com Planner e Auditoria</div>
            <div class="subtitle">Visão integrada de roteamento, consulta vetorial, ferramentas simuladas e trilha forense</div>
        </div>
        <div class="figure-badge">Figura 4</div>
    </div>

    <div class="main-content" style="gap: 20px;">
        <!-- Coluna 1: Entrada & Guardrail -->
        <div class="card" style="flex: 1; padding: 22px;">
            <div class="card-title" style="font-size: 17px; color: #60a5fa; margin-bottom: 14px;">1. Entrada & Filtro</div>
            <div style="display: flex; flex-direction: column; gap: 12px; flex: 1;">
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 12px;">
                    <div style="font-weight: 700; font-size: 13px; color: #ffffff;">Mensagem do Usuário</div>
                    <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Texto livre recebido via API ou chat corporativo.</div>
                </div>
                <div style="text-align: center; color: #64748b; font-size: 18px;">↓</div>
                <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 10px; padding: 12px;">
                    <div style="font-weight: 700; font-size: 13px; color: #f87171;">Guardrail de Segurança</div>
                    <div style="font-size: 12px; color: #fca5a5; margin-top: 4px;">Validação preventiva de credenciais e termos proibidos.</div>
                </div>
            </div>
        </div>

        <!-- Coluna 2: Roteamento & Decisão -->
        <div class="card" style="flex: 1.1; padding: 22px;">
            <div class="card-title" style="font-size: 17px; color: #c084fc; margin-bottom: 14px;">2. Decisão de Tool</div>
            <div style="display: flex; flex-direction: column; gap: 10px; flex: 1;">
                <div style="background: rgba(16, 185, 129, 0.06); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 10px; padding: 10px 14px;">
                    <div style="font-weight: 700; font-size: 13px; color: #34d399;">Regra de Negócio</div>
                    <div style="font-size: 11px; color: #94a3b8;">Roteamento direto por palavras-chave</div>
                </div>
                <div style="text-align: center; color: #64748b; font-size: 14px;">ou</div>
                <div style="background: rgba(59, 130, 246, 0.06); border: 1px solid rgba(59, 130, 246, 0.25); border-radius: 10px; padding: 10px 14px;">
                    <div style="font-weight: 700; font-size: 13px; color: #60a5fa;">Planner JSON (LLM)</div>
                    <div style="font-size: 11px; color: #94a3b8;">Gera schema com tool e argumentos</div>
                </div>
                <div style="text-align: center; color: #64748b; font-size: 14px;">ou (se falhar)</div>
                <div style="background: rgba(245, 158, 11, 0.06); border: 1px solid rgba(245, 158, 11, 0.25); border-radius: 10px; padding: 10px 14px;">
                    <div style="font-weight: 700; font-size: 13px; color: #fbbf24;">Fallback Semântico</div>
                    <div style="font-size: 11px; color: #94a3b8;">Roteamento por cosseno de embeddings</div>
                </div>
            </div>
        </div>

        <!-- Coluna 3: Ferramentas & Retrieval -->
        <div class="card" style="flex: 1.1; padding: 22px;">
            <div class="card-title" style="font-size: 17px; color: #fbbf24; margin-bottom: 14px;">3. Ferramentas & APIs</div>
            <div style="display: flex; flex-direction: column; gap: 12px; flex: 1;">
                <div style="background: rgba(59, 130, 246, 0.08); border: 1px solid rgba(59, 130, 246, 0.25); border-radius: 10px; padding: 12px;">
                    <div style="font-weight: 700; font-size: 13px; color: #60a5fa;">buscar_politica</div>
                    <div style="font-size: 12px; color: #cbd5e1; margin-top: 4px;">Busca vetorial na base de conhecimento com pontuação de relevância.</div>
                </div>
                <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 10px; padding: 12px;">
                    <div style="font-weight: 700; font-size: 13px; color: #34d399;">criar_ticket</div>
                    <div style="font-size: 12px; color: #cbd5e1; margin-top: 4px;">Abertura simulada de chamados de suporte com ticket_id rastreável.</div>
                </div>
            </div>
        </div>

        <!-- Coluna 4: Resposta & Trilha de Auditoria -->
        <div class="card" style="flex: 1.2; padding: 22px; border-color: rgba(16, 185, 129, 0.35); background: rgba(16, 185, 129, 0.03);">
            <div class="card-title" style="font-size: 17px; color: #34d399; margin-bottom: 14px;">4. Síntese & Auditoria</div>
            <div style="display: flex; flex-direction: column; gap: 12px; flex: 1;">
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 12px;">
                    <div style="font-weight: 700; font-size: 13px; color: #ffffff;">Resposta Final ao Usuário</div>
                    <div style="font-size: 12px; color: #a7f3d0; margin-top: 4px;">Texto conciso de até 2 frases sintetizado a partir do retorno da tool.</div>
                </div>
                <div class="code-editor" style="border-color: rgba(16, 185, 129, 0.3); font-size: 11px;">
                    <div class="editor-header">
                        <span class="editor-title" style="color: #34d399;">agent_audit_log.jsonl</span>
                    </div>
                    <div class="editor-body" style="padding: 10px; color: #cbd5e1; font-size: 11px; line-height: 1.5;">
                        "step": "guardrail" &rarr; ok<br>
                        "step": "planner" &rarr; buscar_politica<br>
                        "step": "tool_execution" &rarr; score 0.82<br>
                        "step": "final_response" &rarr; registrada
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 4: A arquitetura integra guardrail, planner, execução de ferramentas e log de auditoria estruturado</div>
    </div>
</body>
</html>"""

TEMPLATES["0007_agentes_tool_calling/assets/05.png"] = f"""{BASE_HEAD}
<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> Artigo 0007 • Agentes e Tool Calling</div>
            <div class="title">Quando Usar Agente de Verdade</div>
            <div class="subtitle">Critérios de maturidade técnica para escolher entre autonomia inteligente e pipelines lineares</div>
        </div>
        <div class="figure-badge">Figura 5</div>
    </div>

    <div class="main-content" style="gap: 32px;">
        <!-- Coluna Quando Usar Agente -->
        <div class="card" style="flex: 1; border-color: rgba(16, 185, 129, 0.4); background: rgba(16, 185, 129, 0.03); padding: 32px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;">
                <div class="card-title" style="color: #34d399; margin-bottom: 0;">
                    <span class="badge badge-emerald">Autonomia</span> Use Agente Inteligente Quando:
                </div>
                <span style="font-size: 13px; color: #10b981; font-weight: 700;">Alta Flexibilidade</span>
            </div>

            <div style="display: flex; flex-direction: column; gap: 14px; flex: 1;">
                <div style="background: rgba(16, 185, 129, 0.06); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 12px; padding: 16px;">
                    <div style="font-weight: 700; font-size: 15px; color: #ffffff; margin-bottom: 4px;">1. Múltiplos Caminhos de Resolução</div>
                    <div style="font-size: 13px; color: #cbd5e1; line-height: 1.5;">
                        O problema não segue uma receita fixa. O sistema precisa escolher entre buscar conhecimento, abrir tickets, invocar APIs ou responder diretamente.
                    </div>
                </div>

                <div style="background: rgba(16, 185, 129, 0.06); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 12px; padding: 16px;">
                    <div style="font-weight: 700; font-size: 15px; color: #ffffff; margin-bottom: 4px;">2. Recuperação Dinâmica de Informação</div>
                    <div style="font-size: 13px; color: #cbd5e1; line-height: 1.5;">
                        A resposta final depende do resultado retornado por ferramentas intermediárias em tempo de execução.
                    </div>
                </div>

                <div style="background: rgba(16, 185, 129, 0.06); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 12px; padding: 16px;">
                    <div style="font-weight: 700; font-size: 15px; color: #ffffff; margin-bottom: 4px;">3. Auditoria Faz Parte do Negócio</div>
                    <div style="font-size: 13px; color: #cbd5e1; line-height: 1.5;">
                        Cada passo (guardrail, planner, argumentos da tool e resposta) é persistido em log estruturado (JSONL) para auditoria e governança.
                    </div>
                </div>
            </div>

            <div style="margin-top: 18px; padding: 12px; background: rgba(16, 185, 129, 0.15); border-radius: 8px; font-size: 13px; color: #a7f3d0; text-align: center; font-weight: 600;">
                ✓ Resolve cenários complexos onde fluxos procedurais tradicionais se tornam um emaranhado incontrolável
            </div>
        </div>

        <!-- Coluna Quando Usar Fluxo Simples -->
        <div class="card" style="flex: 1; border-color: rgba(239, 68, 68, 0.35); background: rgba(239, 68, 68, 0.03); padding: 32px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;">
                <div class="card-title" style="color: #f87171; margin-bottom: 0;">
                    <span class="badge badge-rose">Simplicidade</span> Use Fluxo Simples Quando:
                </div>
                <span style="font-size: 13px; color: #ef4444; font-weight: 700;">Evite Overkill</span>
            </div>

            <div style="display: flex; flex-direction: column; gap: 14px; flex: 1;">
                <div style="background: rgba(239, 68, 68, 0.06); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 12px; padding: 16px;">
                    <div style="font-weight: 700; font-size: 15px; color: #ffffff; margin-bottom: 4px;">1. Sequência Linear e Determinística</div>
                    <div style="font-size: 13px; color: #cbd5e1; line-height: 1.5;">
                        Se o processo sempre segue Passo A &rarr; Passo B &rarr; Passo C sem desvios contextuais, um script ou pipeline tradicional é mais rápido e confiável.
                    </div>
                </div>

                <div style="background: rgba(239, 68, 68, 0.06); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 12px; padding: 16px;">
                    <div style="font-weight: 700; font-size: 15px; color: #ffffff; margin-bottom: 4px;">2. Regra Óbvia de Negócio</div>
                    <div style="font-size: 13px; color: #cbd5e1; line-height: 1.5;">
                        Não gaste inferência de LLM quando um <code>if/else</code>, Regex ou roteamento estático resolve com latência zero e custo zero.
                    </div>
                </div>

                <div style="background: rgba(239, 68, 68, 0.06); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 12px; padding: 16px;">
                    <div style="font-weight: 700; font-size: 15px; color: #ffffff; margin-bottom: 4px;">3. Baixa Tolerância a Latência e Custo</div>
                    <div style="font-size: 13px; color: #cbd5e1; line-height: 1.5;">
                        Agentes exigem loops de raciocínio que multiplicam o tempo de resposta e o consumo de tokens. Se o SLA for &lt; 100ms, use chamadas diretas.
                    </div>
                </div>
            </div>

            <div style="margin-top: 18px; padding: 12px; background: rgba(239, 68, 68, 0.15); border-radius: 8px; font-size: 13px; color: #fca5a5; text-align: center; font-weight: 600;">
                ✗ Maturidade de engenharia está em saber quando NÃO usar agente para economizar custo e complexidade
            </div>
        </div>
    </div>

    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de IA para Produção</div>
        <div>Figura 5: A decisão consciente de arquitetura protege a esteira contra complexidade acidental</div>
    </div>
</body>
</html>"""



def render_html_to_png(html_content: str, output_png: Path) -> None:
    temp_html = output_png.parent / f"_temp_{output_png.stem}.html"
    output_png.parent.mkdir(parents=True, exist_ok=True)
    # Remove o PNG antigo: sem isso, uma falha do Chrome passaria na checagem de existência.
    if output_png.exists():
        output_png.unlink()
    temp_html.write_text(html_content, encoding="utf-8")
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=5000",
        f"--screenshot={output_png}",
        "--window-size=1920,1080",
        str(temp_html),
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, timeout=60)
        if not output_png.exists() or output_png.stat().st_size < 1000:
            raise RuntimeError(f"Falha ao gerar {output_png}: code={res.returncode}, stderr={res.stderr.decode('utf-8', errors='ignore')}")
        print(f"  ✓ Renderizado: {output_png.relative_to(ROOT)} ({output_png.stat().st_size // 1024} KB)")
    except Exception as exc:
        print(f"  ✗ Erro renderizando {output_png.name}: {exc}")
        raise
    finally:
        if temp_html.exists():
            temp_html.unlink()


def render_all() -> None:
    print(f"Iniciando renderização de {len(TEMPLATES)} ativos visuais com Google Chrome headless...")
    for rel_path, html in TEMPLATES.items():
        output_png = ROOT / rel_path
        render_html_to_png(html, output_png)
    print("Todas as imagens foram renderizadas com sucesso!")



if __name__ == "__main__":
    render_all()
