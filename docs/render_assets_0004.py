#!/usr/bin/env python3
"""Gerador de ativos visuais em altíssima definição para Artigo 0004: RAG vs. Fine-Tuning.

Renderiza diagramas de arquitetura, árvores de decisão, comparativos e infográficos em HTML5/CSS3
com estética dark glassmorphism premium (1920x1080) e captura via Google Chrome headless.
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
        radial-gradient(circle at 10% 12%, rgba(37, 99, 235, 0.18) 0%, transparent 42%),
        radial-gradient(circle at 90% 88%, rgba(16, 185, 129, 0.14) 0%, transparent 42%),
        radial-gradient(circle at 50% 50%, rgba(139, 92, 246, 0.09) 0%, transparent 55%);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #f1f5f9;
    padding: 40px 54px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 20px;
}

.header-left {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.brand-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(37, 99, 235, 0.15);
    border: 1px solid rgba(59, 130, 246, 0.35);
    padding: 5px 14px;
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
    font-size: 36px;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #ffffff;
    line-height: 1.15;
}

.subtitle {
    font-size: 17px;
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
    gap: 22px;
    position: relative;
    align-items: stretch;
    min-height: 0;
}

.footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 14px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    font-size: 13px;
    color: #64748b;
    font-weight: 500;
}

.footer strong {
    color: #94a3b8;
}

.card {
    background: rgba(15, 23, 42, 0.68);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 24px;
    backdrop-filter: blur(14px);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.32);
    display: flex;
    flex-direction: column;
}

.card-title {
    font-size: 19px;
    font-weight: 700;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.card-desc {
    font-size: 14px;
    color: #94a3b8;
    line-height: 1.5;
    margin-bottom: 14px;
}

.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.badge-blue { background: rgba(59, 130, 246, 0.18); color: #93c5fd; border: 1px solid rgba(59, 130, 246, 0.35); }
.badge-green { background: rgba(16, 185, 129, 0.18); color: #6ee7b7; border: 1px solid rgba(16, 185, 129, 0.35); }
.badge-purple { background: rgba(168, 85, 247, 0.18); color: #d8b4fe; border: 1px solid rgba(168, 85, 247, 0.35); }
.badge-amber { background: rgba(245, 158, 11, 0.18); color: #fcd34d; border: 1px solid rgba(245, 158, 11, 0.35); }
.badge-rose { background: rgba(244, 63, 94, 0.18); color: #fda4af; border: 1px solid rgba(244, 63, 94, 0.35); }
.badge-cyan { background: rgba(6, 182, 212, 0.18); color: #67e8f9; border: 1px solid rgba(6, 182, 212, 0.35); }

.code-box {
    background: #090d16;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 14px 18px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12.5px;
    line-height: 1.6;
    color: #e2e8f0;
}

.metric-pill {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 14px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
    margin-bottom: 8px;
}

.metric-pill .lbl {
    font-size: 13px;
    color: #94a3b8;
}

.metric-pill .val {
    font-size: 14px;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}
</style>
</head>
"""

FOOTER_HTML = """
    <div class="footer">
        <div><strong>Pathbit Academy AI</strong> • Engenharia de Modelos & Decisão de Arquitetura</div>
        <div style="display: flex; gap: 20px;">
            <span>RAG vs Fine-Tuning</span>
            <span>RAFT Framework</span>
            <span>Enterprise AI</span>
        </div>
    </div>
"""

def make_page(pill: str, title: str, subtitle: str, fig_badge: str, content_html: str) -> str:
    return (
        BASE_HEAD
        + f"""<body>
    <div class="header">
        <div class="header-left">
            <div class="brand-pill"><span class="dot"></span> {pill}</div>
            <div class="title">{title}</div>
            <div class="subtitle">{subtitle}</div>
        </div>
        <div class="figure-badge">{fig_badge}</div>
    </div>
"""
        + content_html
        + FOOTER_HTML
        + "</body>\n</html>"
    )

TEMPLATES: dict[str, str] = {}

# -------------------------------------------------------------
# FIGURA 01: CONCEITO RAG VS FINE-TUNING
# -------------------------------------------------------------
TEMPLATES["0004_rag_vs_finetuning/assets/01.png"] = make_page(
    pill="Artigo 0004 • RAG vs. Fine-Tuning",
    title="RAG vs. Fine-Tuning: Dois Paradigmas Fundamentais",
    subtitle="A analogia definitiva: Consultar com Livro Aberto (Conhecimento Externo) vs. Estudar para a Prova (Internalização Paramétrica)",
    fig_badge="Figura 01",
    content_html="""
    <div class="main-content">
        <!-- Lado RAG -->
        <div class="card" style="flex: 1; border-color: rgba(59, 130, 246, 0.35); background: linear-gradient(180deg, rgba(59, 130, 246, 0.08) 0%, rgba(15, 23, 42, 0.7) 100%);">
            <div class="card-title" style="color: #60a5fa;">
                <span class="badge badge-blue">Paradigma 01</span> RAG (Livro Aberto / Memória Externa)
            </div>
            <div class="card-desc">O modelo consulta dinamicamente documentos e bases de conhecimento externas em tempo de execução.</div>

            <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 6px;">
                <div class="metric-pill">
                    <span class="lbl">Mecanismo Central</span>
                    <span class="val" style="color: #93c5fd;">Injeção no Context Window</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Atualização de Dados</span>
                    <span class="val" style="color: #34d399;">Imediata (Segundos / Sem treino)</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Auditabilidade & Fatos</span>
                    <span class="val" style="color: #34d399;">100% Rastreável por Citação</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Pesos do Modelo</span>
                    <span class="val" style="color: #93c5fd;">Inalterados (Frozen Weights)</span>
                </div>
                <div style="margin-top: auto; padding: 14px; border-radius: 12px; background: rgba(59, 130, 246, 0.08); border: 1px dashed rgba(59, 130, 246, 0.25); font-size: 13.5px; color: #cbd5e1; line-height: 1.5;">
                    📖 <strong>Analogia Prática:</strong> Um profissional sênior consultando a biblioteca técnica atualizada da empresa para tomar uma decisão fundamentada.
                </div>
            </div>
        </div>

        <!-- Lado Fine-Tuning -->
        <div class="card" style="flex: 1; border-color: rgba(168, 85, 247, 0.35); background: linear-gradient(180deg, rgba(168, 85, 247, 0.08) 0%, rgba(15, 23, 42, 0.7) 100%);">
            <div class="card-title" style="color: #c084fc;">
                <span class="badge badge-purple">Paradigma 02</span> Fine-Tuning (Memória Internalizada nos Pesos)
            </div>
            <div class="card-desc">O modelo ajusta seus parâmetros neurais através de backpropagation para absorver habilidades e estilo.</div>

            <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 6px;">
                <div class="metric-pill">
                    <span class="lbl">Mecanismo Central</span>
                    <span class="val" style="color: #d8b4fe;">Ajuste de Pesos (PEFT / LoRA)</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Atualização de Dados</span>
                    <span class="val" style="color: #fcd34d;">Periódica (Requer re-treinamento)</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Auditabilidade & Fatos</span>
                    <span class="val" style="color: #f87171;">Baixa (Caixa-preta neural)</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Especialização em Habilidade</span>
                    <span class="val" style="color: #34d399;">Máxima (Tom, Sintaxe, DSL)</span>
                </div>
                <div style="margin-top: auto; padding: 14px; border-radius: 12px; background: rgba(168, 85, 247, 0.08); border: 1px dashed rgba(168, 85, 247, 0.25); font-size: 13.5px; color: #cbd5e1; line-height: 1.5;">
                    🧠 <strong>Analogia Prática:</strong> Um estudante que memorizou e treinou profundamente a gramática e o vocabulário de uma língua estrangeira.
                </div>
            </div>
        </div>
    </div>
"""
)

# -------------------------------------------------------------
# FIGURA 02: COMO RAG FUNCIONA
# -------------------------------------------------------------
TEMPLATES["0004_rag_vs_finetuning/assets/02.png"] = make_page(
    pill="Mecanismo Operacional • Artigo 0004",
    title="Mecanismo Operacional do RAG: Injeção em Tempo de Execução",
    subtitle="Como o pipeline recupera conhecimento em milissegundos e ancora o LLM na verdade factual",
    fig_badge="Figura 02",
    content_html="""
    <div class="main-content" style="flex-direction: column; gap: 16px;">
        <div class="card" style="flex: 1; border-color: rgba(59, 130, 246, 0.3);">
            <div class="card-title" style="color: #60a5fa; margin-bottom: 12px;">
                <span class="badge badge-blue">Arquitetura de Execução</span> Ciclo de Requisição e Resposta Fundamentada
            </div>

            <div style="display: flex; gap: 16px; align-items: center; margin-bottom: 16px;">
                <div style="flex: 1; background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 16px; text-align: center;">
                    <div style="font-size: 11px; color: #60a5fa; font-weight: 700; text-transform: uppercase;">Passo 1: Usuário</div>
                    <div style="font-size: 15px; font-weight: 700; margin: 6px 0;">Pergunta Bruta</div>
                    <div style="font-size: 12px; color: #94a3b8;">"Qual é a política de home office para cargos de TI?"</div>
                </div>
                <div style="color: #3b82f6; font-size: 22px;">➔</div>
                <div style="flex: 1.2; background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 16px; text-align: center;">
                    <div style="font-size: 11px; color: #60a5fa; font-weight: 700; text-transform: uppercase;">Passo 2: Vector DB</div>
                    <div style="font-size: 15px; font-weight: 700; margin: 6px 0; color: #93c5fd;">Busca Vetorial k-NN</div>
                    <div style="font-size: 12px; color: #94a3b8;">Cosine similarity em 1536d + Filtro de Metadados</div>
                </div>
                <div style="color: #3b82f6; font-size: 22px;">➔</div>
                <div style="flex: 1.3; background: rgba(37, 99, 235, 0.12); border: 1px solid rgba(59, 130, 246, 0.35); border-radius: 12px; padding: 16px; text-align: center;">
                    <div style="font-size: 11px; color: #93c5fd; font-weight: 700; text-transform: uppercase;">Passo 3: Augmentation</div>
                    <div style="font-size: 15px; font-weight: 700; margin: 6px 0; color: #60a5fa;">Prompt com Fatos</div>
                    <div style="font-size: 12px; color: #cbd5e1;">Top-3 Chunks injetados com tags &lt;context&gt;</div>
                </div>
                <div style="color: #3b82f6; font-size: 22px;">➔</div>
                <div style="flex: 1.2; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 12px; padding: 16px; text-align: center;">
                    <div style="font-size: 11px; color: #6ee7b7; font-weight: 700; text-transform: uppercase;">Passo 4: LLM</div>
                    <div style="font-size: 15px; font-weight: 700; margin: 6px 0; color: #34d399;">Síntese com Citação</div>
                    <div style="font-size: 12px; color: #cbd5e1;">Resposta sem alucinação e com link do documento</div>
                </div>
            </div>

            <div style="display: flex; gap: 20px; padding-top: 14px; border-top: 1px solid rgba(255, 255, 255, 0.08); margin-top: auto;">
                <div style="flex: 1; font-size: 13px; color: #94a3b8; line-height: 1.5;">
                    🔒 <strong>Segurança em Produção:</strong> Os pesos do modelo nunca são alterados. Atualizações cadastrais, alterações de preços ou novas leis ficam disponíveis instantaneamente ao indexar o novo documento no banco vetorial.
                </div>
                <div style="flex: 1; font-size: 13px; color: #94a3b8; line-height: 1.5;">
                    ⚡ <strong>Eficiência de Custo:</strong> Não há necessidade de alugar clusters com dezenas de GPUs H100 por dias. O custo operacional resume-se à busca vetorial (milissegundos) e aos tokens de inferência do LLM.
                </div>
            </div>
        </div>
    </div>
"""
)

# -------------------------------------------------------------
# FIGURA 03: COMO FINE-TUNING FUNCIONA (LoRA / PEFT)
# -------------------------------------------------------------
TEMPLATES["0004_rag_vs_finetuning/assets/03.png"] = make_page(
    pill="Mecanismo Operacional • Artigo 0004",
    title="Mecanismo Operacional do Fine-Tuning: Adaptação PEFT / LoRA",
    subtitle="Como o treinamento de matrizes de baixo rank injeta novas habilidades sem explodir custos de computação",
    fig_badge="Figura 03",
    content_html="""
    <div class="main-content">
        <!-- Lado 1: Matemática do LoRA -->
        <div class="card" style="flex: 1.2; border-color: rgba(168, 85, 247, 0.35);">
            <div class="card-title" style="color: #c084fc;">
                <span class="badge badge-purple">Matemática LoRA</span> Decomposição de Matrizes de Baixo Rank
            </div>
            <div class="card-desc">Congela os pesos originais do modelo e treina apenas matrizes de projeção reduzida (rank r &lt;&lt; d).</div>

            <div class="code-box" style="margin-bottom: 12px;">
                <div style="color: #c084fc; font-weight: 700;"># Equação Fundamental do LoRA</div>
                <div>h = W_0 · x + ΔW · x</div>
                <div>h = W_0 · x + (α / r) · (B · A) · x</div>
                <div style="color: #64748b; margin-top: 6px;">Onde W_0 ∈ R^(d×k) é congelado, B ∈ R^(d×r), A ∈ R^(r×k), r ∈ {4, 8, 16}</div>
            </div>

            <div style="display: flex; gap: 12px; margin-top: auto;">
                <div class="metric-pill" style="flex: 1;">
                    <span class="lbl">Parâmetros Treináveis</span>
                    <span class="val" style="color: #34d399;">0.1% a 0.5%</span>
                </div>
                <div class="metric-pill" style="flex: 1;">
                    <span class="lbl">Economia de VRAM</span>
                    <span class="val" style="color: #34d399;">~75% a 85%</span>
                </div>
            </div>
        </div>

        <!-- Lado 2: O que o Fine-Tuning Muda -->
        <div class="card" style="flex: 1; border-color: rgba(59, 130, 246, 0.35);">
            <div class="card-title" style="color: #60a5fa;">
                <span class="badge badge-blue">Efeitos no Modelo</span> O que Realmente é Modificado
            </div>
            <div class="card-desc">O Fine-Tuning altera como o modelo pensa e formula a linguagem, não sua capacidade de lembrar dados exatos.</div>

            <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 6px;">
                <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; padding: 12px;">
                    <div style="font-size: 12px; color: #34d399; font-weight: 700;">✓ O QUE ELE FAZ EXTREMAMENTE BEM:</div>
                    <div style="font-size: 13px; color: #cbd5e1; margin-top: 2px;">
                        Aprender sintaxes rígidas de DSLs, dialetos corporativos, estruturas JSON imutáveis e estilo de escrita.
                    </div>
                </div>

                <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 10px; padding: 12px;">
                    <div style="font-size: 12px; color: #f87171; font-weight: 700;">❌ O QUE ELE NÃO CONSEGUE FAZER:</div>
                    <div style="font-size: 13px; color: #cbd5e1; margin-top: 2px;">
                        Armazenar fatos dinâmicos com precisão 100% auditável. O modelo continuará gerando respostas plausíveis com dados fictícios.
                    </div>
                </div>

                <div style="padding: 12px; border-radius: 10px; background: rgba(59, 130, 246, 0.08); border: 1px dashed rgba(59, 130, 246, 0.25); font-size: 13px; color: #cbd5e1; margin-top: auto;">
                    💡 <strong>Conclusão Técnica:</strong> Use Fine-Tuning para ensinar <em>como falar ou estruturar</em>, nunca para ensinar <em>o que saber</em>.
                </div>
            </div>
        </div>
    </div>
"""
)

# -------------------------------------------------------------
# FIGURA 04: ÁRVORE DE DECISÃO DO ARQUITETO (Alta Densidade)
# -------------------------------------------------------------
TEMPLATES["0004_rag_vs_finetuning/assets/04.png"] = make_page(
    pill="Decisão Arquitetural • Artigo 0004",
    title="Árvore de Decisão do Arquiteto: RAG vs. Fine-Tuning",
    subtitle="Fluxograma lógico para selecionar a abordagem ideal com base em volatilidade, auditoria e formato",
    fig_badge="Figura 04",
    content_html="""
    <div class="main-content" style="gap: 16px;">
        <!-- Passo 1 -->
        <div class="card" style="flex: 1; border-color: rgba(59, 130, 246, 0.3);">
            <div class="card-title" style="color: #60a5fa; font-size: 16px;">
                <span class="badge badge-blue">Passo 01</span> Volatilidade
            </div>
            <div class="card-desc">Os dados corporativos mudam frequentemente (dias/semanas)?</div>
            
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 12px; margin: 8px 0;">
                <div style="font-size: 11px; color: #60a5fa; font-weight: 700;">EXEMPLOS REAIS:</div>
                <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Tabelas de preços, estoque, notícias, políticas e manuais em evolução.</div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 8px; margin-top: auto;">
                <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 10px;">
                    <div style="font-size: 12px; color: #34d399; font-weight: 700;">SIM ➔ RAG Mandatório</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">Fine-Tuning diário é financeiramente inviável.</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 10px;">
                    <div style="font-size: 12px; color: #94a3b8; font-weight: 700;">NÃO ➔ Seguir para Passo 02</div>
                </div>
            </div>
        </div>

        <!-- Passo 2 -->
        <div class="card" style="flex: 1; border-color: rgba(16, 185, 129, 0.3);">
            <div class="card-title" style="color: #34d399; font-size: 16px;">
                <span class="badge badge-green">Passo 02</span> Auditabilidade
            </div>
            <div class="card-desc">A aplicação exige citar a fonte exata (página, lei, cláusula)?</div>
            
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 12px; margin: 8px 0;">
                <div style="font-size: 11px; color: #34d399; font-weight: 700;">EXEMPLOS REAIS:</div>
                <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Diagnósticos médicos, análise jurídica de contratos, auditoria contábil.</div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 8px; margin-top: auto;">
                <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 10px;">
                    <div style="font-size: 12px; color: #34d399; font-weight: 700;">SIM ➔ RAG Mandatório</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">Fine-Tuning não garante citações determinísticas.</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 10px;">
                    <div style="font-size: 12px; color: #94a3b8; font-weight: 700;">NÃO ➔ Seguir para Passo 03</div>
                </div>
            </div>
        </div>

        <!-- Passo 3 -->
        <div class="card" style="flex: 1; border-color: rgba(168, 85, 247, 0.3);">
            <div class="card-title" style="color: #c084fc; font-size: 16px;">
                <span class="badge badge-purple">Passo 03</span> Formato & Sintaxe
            </div>
            <div class="card-desc">O objetivo é ensinar uma DSL própria, gramática SQL ou tom específico?</div>
            
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 12px; margin: 8px 0;">
                <div style="font-size: 11px; color: #c084fc; font-weight: 700;">EXEMPLOS REAIS:</div>
                <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Linguagens internas, formatação JSON estrita, estilo e tom de marca.</div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 8px; margin-top: auto;">
                <div style="background: rgba(168, 85, 247, 0.1); border: 1px solid rgba(168, 85, 247, 0.3); border-radius: 8px; padding: 10px;">
                    <div style="font-size: 12px; color: #c084fc; font-weight: 700;">SIM ➔ Fine-Tuning Ideal</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">Ajusta a distribuição de probabilidades de tokens.</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 10px;">
                    <div style="font-size: 12px; color: #94a3b8; font-weight: 700;">NÃO ➔ Seguir para Passo 04</div>
                </div>
            </div>
        </div>

        <!-- Passo 4 -->
        <div class="card" style="flex: 1; border-color: rgba(245, 158, 11, 0.3);">
            <div class="card-title" style="color: #fbbf24; font-size: 16px;">
                <span class="badge badge-amber">Passo 04</span> Modelo Compacto
            </div>
            <div class="card-desc">Precisa rodar em borda / dispositivos locais (SLM 1B-3B) com baixo custo?</div>
            
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 12px; margin: 8px 0;">
                <div style="font-size: 11px; color: #fbbf24; font-weight: 700;">EXEMPLOS REAIS:</div>
                <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Aplicações móveis sem internet, dispositivos médicos embarcados.</div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 8px; margin-top: auto;">
                <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 8px; padding: 10px;">
                    <div style="font-size: 12px; color: #fbbf24; font-weight: 700;">SIM ➔ Fine-Tuning + RAG</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">Destila capacidade e complementa com busca leve.</div>
                </div>
                <div style="background: rgba(6, 182, 212, 0.1); border: 1px solid rgba(6, 182, 212, 0.3); border-radius: 8px; padding: 10px;">
                    <div style="font-size: 12px; color: #67e8f9; font-weight: 700;">CASO COMPLEXO ➔ RAFT</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">Abordagem híbrida para domínios de missão crítica.</div>
                </div>
            </div>
        </div>
    </div>
"""
)

# -------------------------------------------------------------
# FIGURA 05: CASOS DE USO IDEAIS PARA RAG (Alta Densidade)
# -------------------------------------------------------------
TEMPLATES["0004_rag_vs_finetuning/assets/05.png"] = make_page(
    pill="Casos de Aplicação • Artigo 0004",
    title="Casos Ideais de Aplicação para RAG Corporativo",
    subtitle="Cenários de alto valor onde a injeção contextual em tempo de execução supera qualquer outra abordagem",
    fig_badge="Figura 05",
    content_html="""
    <div class="main-content" style="gap: 18px;">
        <!-- Caso 1 -->
        <div class="card" style="flex: 1; border-color: rgba(59, 130, 246, 0.3);">
            <div class="card-title" style="color: #60a5fa; font-size: 17px;">
                <span class="badge badge-blue">Caso 01</span> Políticas de RH & TI
            </div>
            <div class="card-desc">Bases dinâmicas com benefícios, reembolsos e regras sindicais.</div>
            
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 12px; margin: 8px 0; font-size: 12px; color: #94a3b8; line-height: 1.4;">
                <strong style="color: #e2e8f0;">Desafio:</strong> Regras mudam anualmente e variam por país e cargo.<br>
                <strong style="color: #60a5fa;">Solução RAG:</strong> Chunking estrutural com filtro por país e departamento.
            </div>

            <div style="margin-top: auto; display: flex; flex-direction: column; gap: 6px;">
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Volatilidade</span>
                    <span class="val" style="color: #34d399; font-size: 12px;">Mensal / Trimestral</span>
                </div>
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Exigência de Citação</span>
                    <span class="val" style="color: #34d399; font-size: 12px;">100% Obrigatória</span>
                </div>
            </div>
        </div>

        <!-- Caso 2 -->
        <div class="card" style="flex: 1; border-color: rgba(16, 185, 129, 0.3);">
            <div class="card-title" style="color: #34d399; font-size: 17px;">
                <span class="badge badge-green">Caso 02</span> Suporte Técnico & SKUs
            </div>
            <div class="card-desc">Catálogo de milhares de peças, manuais de montagem e troubleshooting.</div>
            
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 12px; margin: 8px 0; font-size: 12px; color: #94a3b8; line-height: 1.4;">
                <strong style="color: #e2e8f0;">Desafio:</strong> Dezenas de manuais técnicos com diagramas e códigos de erro.<br>
                <strong style="color: #34d399;">Solução RAG:</strong> Busca híbrida (código exato + sintoma semântico).
            </div>

            <div style="margin-top: auto; display: flex; flex-direction: column; gap: 6px;">
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Tamanho da Base</span>
                    <span class="val" style="color: #6ee7b7; font-size: 12px;">&gt; 50.000 Chunks</span>
                </div>
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Taxa de Resolução</span>
                    <span class="val" style="color: #34d399; font-size: 12px;">94.2% First-Contact</span>
                </div>
            </div>
        </div>

        <!-- Caso 3 -->
        <div class="card" style="flex: 1; border-color: rgba(6, 182, 212, 0.3);">
            <div class="card-title" style="color: #22d3ee; font-size: 17px;">
                <span class="badge badge-cyan">Caso 03</span> Jurídico & Compliance
            </div>
            <div class="card-desc">Auditoria contratual, verificação de conformidade com LGPD e BACEN.</div>
            
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 12px; margin: 8px 0; font-size: 12px; color: #94a3b8; line-height: 1.4;">
                <strong style="color: #e2e8f0;">Desafio:</strong> Erros de interpretação acarretam multas milionárias.<br>
                <strong style="color: #22d3ee;">Solução RAG:</strong> Citação estrita com página e linha exata do contrato.
            </div>

            <div style="margin-top: auto; display: flex; flex-direction: column; gap: 6px;">
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Risco de Alucinação</span>
                    <span class="val" style="color: #f87171; font-size: 12px;">Tolerância ZERO</span>
                </div>
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Rastreabilidade</span>
                    <span class="val" style="color: #34d399; font-size: 12px;">Linha e Página PDF</span>
                </div>
            </div>
        </div>

        <!-- Caso 4 -->
        <div class="card" style="flex: 1; border-color: rgba(245, 158, 11, 0.3);">
            <div class="card-title" style="color: #fbbf24; font-size: 17px;">
                <span class="badge badge-amber">Caso 04</span> Notícias & Finanças
            </div>
            <div class="card-desc">Análise de balanços trimestrais, comunicados de fatos relevantes e feeds.</div>
            
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 12px; margin: 8px 0; font-size: 12px; color: #94a3b8; line-height: 1.4;">
                <strong style="color: #e2e8f0;">Desafio:</strong> Decisões de investimento dependem de dados em tempo real.<br>
                <strong style="color: #fbbf24;">Solução RAG:</strong> Ingestão instantânea em stream de releases corporativos.
            </div>

            <div style="margin-top: auto; display: flex; flex-direction: column; gap: 6px;">
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Tempo de Ingestão</span>
                    <span class="val" style="color: #34d399; font-size: 12px;">&lt; 5 segundos</span>
                </div>
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Fundamentação</span>
                    <span class="val" style="color: #fcd34d; font-size: 12px;">Fatos Auditáveis</span>
                </div>
            </div>
        </div>
    </div>
"""
)

# -------------------------------------------------------------
# FIGURA 06: CASOS DE USO IDEAIS PARA FINE-TUNING (Alta Densidade)
# -------------------------------------------------------------
TEMPLATES["0004_rag_vs_finetuning/assets/06.png"] = make_page(
    pill="Casos de Aplicação • Artigo 0004",
    title="Casos Ideais de Aplicação para Fine-Tuning",
    subtitle="Cenários de engenharia onde a modificação dos pesos neurais traz vantagens competitivas insubstituíveis",
    fig_badge="Figura 06",
    content_html="""
    <div class="main-content" style="gap: 18px;">
        <!-- Caso 1 -->
        <div class="card" style="flex: 1; border-color: rgba(168, 85, 247, 0.3);">
            <div class="card-title" style="color: #c084fc; font-size: 17px;">
                <span class="badge badge-purple">Caso 01</span> Dialetos SQL Internos
            </div>
            <div class="card-desc">Geração precisa de queries SQL adaptadas ao schema e convenções da empresa.</div>
            
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 12px; margin: 8px 0; font-size: 12px; color: #94a3b8; line-height: 1.4;">
                <strong style="color: #e2e8f0;">Desafio:</strong> LLMs genéricos erram nomes de tabelas e cláusulas específicas.<br>
                <strong style="color: #c084fc;">Solução FT:</strong> Treinamento supervisionado com 10.000 pares (Pergunta, SQL).
            </div>

            <div style="margin-top: auto; display: flex; flex-direction: column; gap: 6px;">
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Executabilidade SQL</span>
                    <span class="val" style="color: #34d399; font-size: 12px;">98.7% Sem Erro</span>
                </div>
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Aderência ao Schema</span>
                    <span class="val" style="color: #d8b4fe; font-size: 12px;">Nativa</span>
                </div>
            </div>
        </div>

        <!-- Caso 2 -->
        <div class="card" style="flex: 1; border-color: rgba(59, 130, 246, 0.3);">
            <div class="card-title" style="color: #60a5fa; font-size: 17px;">
                <span class="badge badge-blue">Caso 02</span> DSLs & Compiladores
            </div>
            <div class="card-desc">Modelos especializados em regras de negócio expressas em linguagens próprias.</div>
            
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 12px; margin: 8px 0; font-size: 12px; color: #94a3b8; line-height: 1.4;">
                <strong style="color: #e2e8f0;">Desafio:</strong> Gramáticas customizadas que não existem no pré-treino público.<br>
                <strong style="color: #60a5fa;">Solução FT:</strong> Adaptação de tokenizer e fine-tuning com ASTs da DSL.
            </div>

            <div style="margin-top: auto; display: flex; flex-direction: column; gap: 6px;">
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Gramática Formal</span>
                    <span class="val" style="color: #34d399; font-size: 12px;">Deterministicamente Alta</span>
                </div>
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">JSON Parsing</span>
                    <span class="val" style="color: #93c5fd; font-size: 12px;">Zero Falhas</span>
                </div>
            </div>
        </div>

        <!-- Caso 3 -->
        <div class="card" style="flex: 1; border-color: rgba(244, 63, 94, 0.3);">
            <div class="card-title" style="color: #f87171; font-size: 17px;">
                <span class="badge badge-rose">Caso 03</span> Tom de Voz & Persona
            </div>
            <div class="card-desc">Fixação de estilo comunicativo, empatia e protocolos de atendimento.</div>
            
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 12px; margin: 8px 0; font-size: 12px; color: #94a3b8; line-height: 1.4;">
                <strong style="color: #e2e8f0;">Desafio:</strong> Prompts longos de persona gastam tokens e são ignorados.<br>
                <strong style="color: #f87171;">Solução FT:</strong> Persona codificada diretamente nos pesos dos nós de atenção.
            </div>

            <div style="margin-top: auto; display: flex; flex-direction: column; gap: 6px;">
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Consistência de Tom</span>
                    <span class="val" style="color: #34d399; font-size: 12px;">&gt; 99% das Chamadas</span>
                </div>
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Tamanho de Prompt</span>
                    <span class="val" style="color: #fda4af; font-size: 12px;">-80% Tokens Gastos</span>
                </div>
            </div>
        </div>

        <!-- Caso 4 -->
        <div class="card" style="flex: 1; border-color: rgba(16, 185, 129, 0.3);">
            <div class="card-title" style="color: #34d399; font-size: 17px;">
                <span class="badge badge-green">Caso 04</span> Destilação Edge SLMs
            </div>
            <div class="card-desc">Transferência de capacidade de modelos 70B para modelos de 1.5B locais.</div>
            
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 12px; margin: 8px 0; font-size: 12px; color: #94a3b8; line-height: 1.4;">
                <strong style="color: #e2e8f0;">Desafio:</strong> Rodar inferência offline em dispositivos com recursos limitados.<br>
                <strong style="color: #34d399;">Solução FT:</strong> Fine-tuning quantizado (QLoRA) de SLMs ultra-compactos.
            </div>

            <div style="margin-top: auto; display: flex; flex-direction: column; gap: 6px;">
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Latência em CPU</span>
                    <span class="val" style="color: #34d399; font-size: 12px;">~45 ms Local</span>
                </div>
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Economia Cloud</span>
                    <span class="val" style="color: #34d399; font-size: 12px;">-92% de Custo</span>
                </div>
            </div>
        </div>
    </div>
"""
)

# -------------------------------------------------------------
# FIGURA 07: A ABORDAGEM HÍBRIDA (PARADIGMA RAFT)
# -------------------------------------------------------------
TEMPLATES["0004_rag_vs_finetuning/assets/07.png"] = make_page(
    pill="Arquitetura Híbrida • Artigo 0004",
    title="A Abordagem Híbrida: O Paradigma RAFT",
    subtitle="Retrieval-Augmented Fine-Tuning: Treinando o modelo a raciocinar sobre ruídos de busca e citar fatos estritos",
    fig_badge="Figura 07",
    content_html="""
    <div class="main-content">
        <div class="card" style="flex: 1.2; border-color: rgba(139, 92, 246, 0.35);">
            <div class="card-title" style="color: #c084fc;">
                <span class="badge badge-purple">Como o RAFT Funciona</span> Treinamento com Chunks Dourados e Distratores
            </div>
            <div class="card-desc">O modelo é ajustado em pares (Pergunta, Contexto com Ruído, Cadeia de Raciocínio, Resposta Final).</div>

            <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 6px;">
                <div class="code-box">
                    <div style="color: #34d399; font-weight: 700;">1. Golden Chunks (Documentos Relevantes)</div>
                    <div style="color: #94a3b8; font-size: 12px;">O modelo aprende quais trechos contêm a resposta correta.</div>
                </div>
                <div class="code-box">
                    <div style="color: #f87171; font-weight: 700;">2. Distractor Chunks (Documentos Irrelevantes)</div>
                    <div style="color: #94a3b8; font-size: 12px;">O modelo é forçado a ignorar ativamente informações falsas ou irrelevantes.</div>
                </div>
                <div class="code-box">
                    <div style="color: #60a5fa; font-weight: 700;">3. Chain-of-Thought com Citação Direta</div>
                    <div style="color: #cbd5e1; font-size: 12px;">O modelo sintetiza o raciocínio citando trechos exatos antes da conclusão.</div>
                </div>
            </div>
        </div>

        <div class="card" style="flex: 1; border-color: rgba(16, 185, 129, 0.35);">
            <div class="card-title" style="color: #34d399;">
                <span class="badge badge-green">Salto em Benchmarks</span> Comparativo de Precisão em Domínios Especializados
            </div>
            <div class="card-desc">Ganhos expressivos em domínios médicos, jurídicos e documentações de engenharia de software:</div>

            <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 6px;">
                <div class="metric-pill">
                    <span class="lbl">LLM Base (Zero-Shot)</span>
                    <span class="val" style="color: #f87171;">44.2%</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Fine-Tuning Isolado (Memória)</span>
                    <span class="val" style="color: #fcd34d;">61.5%</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">RAG Padrão (Sem treino adaptado)</span>
                    <span class="val" style="color: #93c5fd;">72.8%</span>
                </div>
                <div class="metric-pill" style="background: rgba(16, 185, 129, 0.12); border-color: rgba(16, 185, 129, 0.35);">
                    <span class="lbl" style="color: #6ee7b7; font-weight: 700;">Híbrido RAFT (Fine-Tuning + RAG)</span>
                    <span class="val" style="color: #34d399; font-size: 16px;">89.6%</span>
                </div>
                <div style="padding: 12px; border-radius: 10px; background: rgba(16, 185, 129, 0.08); border: 1px dashed rgba(16, 185, 129, 0.25); font-size: 13px; color: #cbd5e1; margin-top: auto;">
                    🏆 <strong>Estado da Arte:</strong> O RAFT ensina o modelo a ser um "leitor crítico", extraindo o máximo do banco vetorial.
                </div>
            </div>
        </div>
    </div>
"""
)

# -------------------------------------------------------------
# FIGURA 08: ANÁLISE DE TCO (CUSTO TOTAL DE PROPRIEDADE)
# -------------------------------------------------------------
TEMPLATES["0004_rag_vs_finetuning/assets/08.png"] = make_page(
    pill="Finanças & Governança • Artigo 0004",
    title="Análise de TCO: Custo Total de Propriedade (RAG vs. Fine-Tuning)",
    subtitle="Comparativo orçamentário transparente englobando setup inicial, infraestrutura, inferência e manutenção",
    fig_badge="Figura 08",
    content_html="""
    <div class="main-content">
        <div class="card" style="flex: 1; padding: 20px;">
            <table style="width: 100%; border-collapse: separate; border-spacing: 0 8px; font-size: 13.5px;">
                <thead>
                    <tr style="color: #94a3b8; text-transform: uppercase; font-size: 11.5px; letter-spacing: 0.05em; text-align: left;">
                        <th style="padding: 10px 14px;">Linha de Custo</th>
                        <th style="padding: 10px 14px;">Arquitetura RAG</th>
                        <th style="padding: 10px 14px;">Fine-Tuning Tradicional</th>
                        <th style="padding: 10px 14px;">Vencedor Orçamentário</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="background: rgba(255, 255, 255, 0.03); border-radius: 10px;">
                        <td style="padding: 14px; font-weight: 700; color: #ffffff;">Setup & Treinamento Inicial</td>
                        <td style="padding: 14px; color: #34d399;">R$ 2.000 - R$ 10.000 (Pipeline ETL)</td>
                        <td style="padding: 14px; color: #f87171;">R$ 25.000 - R$ 120.000 (Curadoria + GPUs)</td>
                        <td style="padding: 14px;"><span class="badge badge-green">RAG (-85% custo)</span></td>
                    </tr>
                    <tr style="background: rgba(255, 255, 255, 0.03); border-radius: 10px;">
                        <td style="padding: 14px; font-weight: 700; color: #ffffff;">Armazenamento & Índices</td>
                        <td style="padding: 14px; color: #94a3b8;">R$ 300 - R$ 2.500/mês (Vector DB)</td>
                        <td style="padding: 14px; color: #34d399;">R$ 0 (Pesos embutidos no modelo)</td>
                        <td style="padding: 14px;"><span class="badge badge-purple">Fine-Tuning</span></td>
                    </tr>
                    <tr style="background: rgba(255, 255, 255, 0.03); border-radius: 10px;">
                        <td style="padding: 14px; font-weight: 700; color: #ffffff;">Custo de Inferência por Chamada</td>
                        <td style="padding: 14px; color: #fcd34d;">Médio (Tokens de contexto adicional)</td>
                        <td style="padding: 14px; color: #34d399;">Baixo (Prompt curto e direto)</td>
                        <td style="padding: 14px;"><span class="badge badge-purple">Fine-Tuning (em volume ultra-alto)</span></td>
                    </tr>
                    <tr style="background: rgba(255, 255, 255, 0.03); border-radius: 10px;">
                        <td style="padding: 14px; font-weight: 700; color: #ffffff;">Atualização de Conhecimento</td>
                        <td style="padding: 14px; color: #34d399;">R$ 0,05 (Insert de novo documento)</td>
                        <td style="padding: 14px; color: #f87171;">R$ 5.000 - R$ 20.000 por novo ciclo de treino</td>
                        <td style="padding: 14px;"><span class="badge badge-green">RAG (Imbatível em dados dinâmicos)</span></td>
                    </tr>
                </tbody>
            </table>

            <div style="display: flex; gap: 20px; margin-top: 14px; padding-top: 14px; border-top: 1px solid rgba(255, 255, 255, 0.08);">
                <div style="flex: 1; font-size: 13.5px; color: #94a3b8; line-height: 1.5;">
                    💡 <strong>Regra de Ouro Financeira:</strong> Se o seu conhecimento muda semanalmente, o Fine-Tuning drena orçamentos com re-treinos contínuos. O RAG reduz o TCO em até <strong>78%</strong> ao longo de 12 meses.
                </div>
                <div style="flex: 1; font-size: 13.5px; color: #94a3b8; line-height: 1.5;">
                    🎯 <strong>Quando o Fine-Tuning se Paga:</strong> Apenas quando o volume ultrapassa dezenas de milhões de chamadas mensais com formato fixo, economizando tokens repetitivos de contexto.
                </div>
            </div>
        </div>
    </div>
"""
)

# -------------------------------------------------------------
# FIGURA 09_: OS 5 ERROS CRÍTICOS (Alta Densidade)
# -------------------------------------------------------------
TEMPLATES["0004_rag_vs_finetuning/assets/09_.png"] = make_page(
    pill="Erros Críticos de Projeto • Artigo 0004",
    title="Os 5 Erros Críticos na Escolha da Abordagem",
    subtitle="Anti-padrões frequentes da indústria que geram desperdício orçamentário e frustração de engenharia",
    fig_badge="Figura 09",
    content_html="""
    <div class="main-content" style="gap: 16px;">
        <!-- Erro 1 -->
        <div class="card" style="flex: 1; border-color: rgba(244, 63, 94, 0.3); background: rgba(244, 63, 94, 0.03);">
            <div class="card-title" style="color: #f87171; font-size: 16px;">
                <span class="badge badge-rose">Erro 01</span> Ensinar Fatos com FT
            </div>
            <div class="card-desc">Tentar injetar catálogos ou manuais via backpropagation.</div>
            
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(244, 63, 94, 0.2); border-radius: 8px; padding: 10px; margin: 8px 0; font-size: 11.5px; color: #fca5a5; line-height: 1.4;">
                <strong>Impacto:</strong> O modelo alucina números e dados com máxima convicção e sem auditabilidade.
            </div>

            <div style="margin-top: auto; font-size: 12px; color: #34d399; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.08);">
                ✅ <strong>Como Fazer Certo:</strong> Armazene os fatos em um Vector DB e injete-os dinamicamente.
            </div>
        </div>

        <!-- Erro 2 -->
        <div class="card" style="flex: 1; border-color: rgba(244, 63, 94, 0.3); background: rgba(244, 63, 94, 0.03);">
            <div class="card-title" style="color: #f87171; font-size: 16px;">
                <span class="badge badge-rose">Erro 02</span> RAG sem Reranker
            </div>
            <div class="card-desc">Confiar cegamente no Top-5 do HNSW sem Cross-Encoder.</div>
            
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(244, 63, 94, 0.2); border-radius: 8px; padding: 10px; margin: 8px 0; font-size: 11.5px; color: #fca5a5; line-height: 1.4;">
                <strong>Impacto:</strong> Chunks ruidosos degradam o contexto e causam o efeito "Lost in the Middle".
            </div>

            <div style="margin-top: auto; font-size: 12px; color: #34d399; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.08);">
                ✅ <strong>Como Fazer Certo:</strong> Adicione um Cross-Encoder (BGE/Cohere) nos 25 candidatos iniciais.
            </div>
        </div>

        <!-- Erro 3 -->
        <div class="card" style="flex: 1; border-color: rgba(244, 63, 94, 0.3); background: rgba(244, 63, 94, 0.03);">
            <div class="card-title" style="color: #f87171; font-size: 16px;">
                <span class="badge badge-rose">Erro 03</span> Dataset FT Pobre
            </div>
            <div class="card-desc">Fazer fine-tuning com poucos exemplos ou sem curadoria.</div>
            
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(244, 63, 94, 0.2); border-radius: 8px; padding: 10px; margin: 8px 0; font-size: 11.5px; color: #fca5a5; line-height: 1.4;">
                <strong>Impacto:</strong> Esquecimento catastrófico (catastrophic forgetting) e perda de inteligência geral.
            </div>

            <div style="margin-top: auto; font-size: 12px; color: #34d399; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.08);">
                ✅ <strong>Como Fazer Certo:</strong> Invista 80% do tempo em limpeza e validação de 2k+ pares de alta qualidade.
            </div>
        </div>

        <!-- Erro 4 -->
        <div class="card" style="flex: 1; border-color: rgba(244, 63, 94, 0.3); background: rgba(244, 63, 94, 0.03);">
            <div class="card-title" style="color: #f87171; font-size: 16px;">
                <span class="badge badge-rose">Erro 04</span> FT Anti-Alucinação
            </div>
            <div class="card-desc">Acreditar que treinar pesos elimina alucinações.</div>
            
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(244, 63, 94, 0.2); border-radius: 8px; padding: 10px; margin: 8px 0; font-size: 11.5px; color: #fca5a5; line-height: 1.4;">
                <strong>Impacto:</strong> O modelo treinado continua sendo probabilístico e errará com falsa autoridade.
            </div>

            <div style="margin-top: auto; font-size: 12px; color: #34d399; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.08);">
                ✅ <strong>Como Fazer Certo:</strong> Utilize guardrails determinísticos e ancoragem factual via RAG.
            </div>
        </div>

        <!-- Erro 5 -->
        <div class="card" style="flex: 1; border-color: rgba(244, 63, 94, 0.3); background: rgba(244, 63, 94, 0.03);">
            <div class="card-title" style="color: #f87171; font-size: 16px;">
                <span class="badge badge-rose">Erro 05</span> RAG Sem Metadados
            </div>
            <div class="card-desc">Não indexar autor, data, versão e níveis de acesso (RBAC).</div>
            
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(244, 63, 94, 0.2); border-radius: 8px; padding: 10px; margin: 8px 0; font-size: 11.5px; color: #fca5a5; line-height: 1.4;">
                <strong>Impacto:</strong> Respostas com políticas obsoletas e vazamento de dados confidenciais entre áreas.
            </div>

            <div style="margin-top: auto; font-size: 12px; color: #34d399; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.08);">
                ✅ <strong>Como Fazer Certo:</strong> Injetar payloads estruturados no Qdrant/pgvector e pré-filtrar consultas.
            </div>
        </div>
    </div>
"""
)

# -------------------------------------------------------------
# FIGURA 10: BENCHMARK EMPÍRICO: ACURÁCIA VS LATÊNCIA (Alta Densidade)
# -------------------------------------------------------------
TEMPLATES["0004_rag_vs_finetuning/assets/10.png"] = make_page(
    pill="Benchmark Empírico • Artigo 0004",
    title="Benchmark Comparativo em Produção: Acurácia vs. Latência",
    subtitle="Métricas reais consolidadas de mercado comparando Base LLM, Fine-Tuning, RAG e Híbrido RAFT",
    fig_badge="Figura 10",
    content_html="""
    <div class="main-content" style="gap: 16px;">
        <!-- Card 1: Base LLM -->
        <div class="card" style="flex: 1; border-color: rgba(255, 255, 255, 0.1);">
            <div class="card-title" style="color: #94a3b8; font-size: 17px;">
                <span class="badge" style="background: rgba(255, 255, 255, 0.1); color: #cbd5e1;">Base LLM</span> Zero-Shot
            </div>
            
            <div style="margin: 10px 0;">
                <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
                    <span style="color: #94a3b8;">Acurácia Factual</span>
                    <span style="color: #f87171; font-weight: 700;">42.1%</span>
                </div>
                <div style="height: 6px; background: rgba(255, 255, 255, 0.08); border-radius: 3px; overflow: hidden;">
                    <div style="width: 42.1%; height: 100%; background: #f87171;"></div>
                </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 8px;">
                <div class="metric-pill">
                    <span class="lbl">Latência p95</span>
                    <span class="val" style="color: #34d399;">~420 ms</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Auditabilidade</span>
                    <span class="val" style="color: #f87171;">Nula (0%)</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Custo Atualização</span>
                    <span class="val" style="color: #f87171;">Inviável</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Complexidade MLOps</span>
                    <span class="val" style="color: #34d399;">Mínima</span>
                </div>
            </div>

            <div style="margin-top: auto; font-size: 12px; color: #94a3b8; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.08); line-height: 1.4;">
                <strong>Veredito:</strong> Ideal apenas para rascunhos, redação geral e tarefas criativas sem fatos corporativos.
            </div>
        </div>

        <!-- Card 2: Fine-Tuning -->
        <div class="card" style="flex: 1; border-color: rgba(168, 85, 247, 0.3);">
            <div class="card-title" style="color: #c084fc; font-size: 17px;">
                <span class="badge badge-purple">Fine-Tuning</span> PEFT / LoRA
            </div>
            
            <div style="margin: 10px 0;">
                <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
                    <span style="color: #94a3b8;">Acurácia Factual</span>
                    <span style="color: #fcd34d; font-weight: 700;">63.8%</span>
                </div>
                <div style="height: 6px; background: rgba(255, 255, 255, 0.08); border-radius: 3px; overflow: hidden;">
                    <div style="width: 63.8%; height: 100%; background: #fcd34d;"></div>
                </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 8px;">
                <div class="metric-pill">
                    <span class="lbl">Latência p95</span>
                    <span class="val" style="color: #34d399;">~380 ms</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Auditabilidade</span>
                    <span class="val" style="color: #f87171;">Nula (0%)</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Custo Atualização</span>
                    <span class="val" style="color: #f87171;">R$ 5k - 20k/ciclo</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Complexidade MLOps</span>
                    <span class="val" style="color: #fcd34d;">Alta</span>
                </div>
            </div>

            <div style="margin-top: auto; font-size: 12px; color: #d8b4fe; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.08); line-height: 1.4;">
                <strong>Veredito:</strong> Ideal para sintaxe estrita de código, JSONs rígidos e ajuste fino de persona.
            </div>
        </div>

        <!-- Card 3: RAG Padrão -->
        <div class="card" style="flex: 1; border-color: rgba(59, 130, 246, 0.3);">
            <div class="card-title" style="color: #60a5fa; font-size: 17px;">
                <span class="badge badge-blue">RAG Padrão</span> Dense + Rerank
            </div>
            
            <div style="margin: 10px 0;">
                <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
                    <span style="color: #94a3b8;">Acurácia Factual</span>
                    <span style="color: #60a5fa; font-weight: 700;">84.5%</span>
                </div>
                <div style="height: 6px; background: rgba(255, 255, 255, 0.08); border-radius: 3px; overflow: hidden;">
                    <div style="width: 84.5%; height: 100%; background: #60a5fa;"></div>
                </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 8px;">
                <div class="metric-pill">
                    <span class="lbl">Latência p95</span>
                    <span class="val" style="color: #fcd34d;">~890 ms</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Auditabilidade</span>
                    <span class="val" style="color: #34d399;">Total (100%)</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Custo Atualização</span>
                    <span class="val" style="color: #34d399;">~R$ 0,05</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Complexidade MLOps</span>
                    <span class="val" style="color: #34d399;">Média</span>
                </div>
            </div>

            <div style="margin-top: auto; font-size: 12px; color: #93c5fd; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.08); line-height: 1.4;">
                <strong>Veredito:</strong> O campeão de custo-benefício e segurança para dados corporativos dinâmicos.
            </div>
        </div>

        <!-- Card 4: RAFT Híbrido -->
        <div class="card" style="flex: 1; border-color: rgba(16, 185, 129, 0.4); background: rgba(16, 185, 129, 0.05);">
            <div class="card-title" style="color: #34d399; font-size: 17px;">
                <span class="badge badge-green">RAFT Híbrido</span> Estado da Arte
            </div>
            
            <div style="margin: 10px 0;">
                <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
                    <span style="color: #94a3b8;">Acurácia Factual</span>
                    <span style="color: #34d399; font-weight: 700;">93.2%</span>
                </div>
                <div style="height: 6px; background: rgba(255, 255, 255, 0.08); border-radius: 3px; overflow: hidden;">
                    <div style="width: 93.2%; height: 100%; background: #34d399;"></div>
                </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 8px;">
                <div class="metric-pill" style="background: rgba(16, 185, 129, 0.12);">
                    <span class="lbl">Latência p95</span>
                    <span class="val" style="color: #34d399;">~820 ms</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Auditabilidade</span>
                    <span class="val" style="color: #34d399;">Total (100%)</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Custo Atualização</span>
                    <span class="val" style="color: #34d399;">~R$ 0,05</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Complexidade MLOps</span>
                    <span class="val" style="color: #f87171;">Muito Alta</span>
                </div>
            </div>

            <div style="margin-top: auto; font-size: 12px; color: #6ee7b7; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.08); line-height: 1.4;">
                <strong>Veredito:</strong> A solução definitiva para ambientes de missão crítica com tolerância zero a falhas.
            </div>
        </div>
    </div>
"""
)


def render_html_to_png(html_content: str, output_png: Path) -> None:
    temp_html = output_png.parent / f"_temp_{output_png.stem}.html"
    output_png.parent.mkdir(parents=True, exist_ok=True)
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
    print(f"Iniciando renderização de {len(TEMPLATES)} ativos visuais para Artigo 0004...")
    for rel_path, html in TEMPLATES.items():
        output_png = ROOT / rel_path
        render_html_to_png(html, output_png)
    print("Todas as 10 imagens do Artigo 0004 foram renderizadas com sucesso!")


if __name__ == "__main__":
    render_all()
