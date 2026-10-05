#!/usr/bin/env python3
"""Gerador de ativos visuais em altíssima definição para Artigo 0003: RAG & Vector Databases.

Renderiza diagramas de arquitetura, fluxos, comparativos e infográficos em HTML5/CSS3
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
        <div><strong>Pathbit Academy AI</strong> • Engenharia de Dados & Modelos em Produção</div>
        <div style="display: flex; gap: 20px;">
            <span>Arquitetura de Referência</span>
            <span>RAG & Vector DB</span>
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
# FIGURA 01: OS 3 PILARES DO RAG (Retrieval-Augmented Generation)
# -------------------------------------------------------------
TEMPLATES["0003_rag_vector_database/assets/01.png"] = make_page(
    pill="Artigo 0003 • RAG & Vector Database",
    title="Os Três Pilares da Arquitetura RAG",
    subtitle="Como a orquestração de Recuperação, Aumento e Geração resolve a alucinação e a obsolescência de modelos",
    fig_badge="Figura 01",
    content_html="""
    <div class="main-content">
        <!-- Pilar 1: Recuperação -->
        <div class="card" style="flex: 1; border-color: rgba(59, 130, 246, 0.35); background: linear-gradient(180deg, rgba(59, 130, 246, 0.07) 0%, rgba(15, 23, 42, 0.7) 100%);">
            <div class="card-title" style="color: #60a5fa;">
                <span class="badge badge-blue">Pilar 01</span> Recuperação (Retrieval)
            </div>
            <div class="card-desc">Localização semântica de fragmentos de conhecimento relevantes em bases corporativas externas.</div>
            
            <div style="flex: 1; display: flex; flex-direction: column; gap: 10px; margin-top: 4px;">
                <div class="metric-pill">
                    <span class="lbl">Mecanismo Central</span>
                    <span class="val" style="color: #93c5fd;">k-NN / ANN (HNSW)</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Espaço de Busca</span>
                    <span class="val" style="color: #93c5fd;">Vetorial Denso (Cosine)</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Tempo Médio de Varredura</span>
                    <span class="val" style="color: #34d399;">8 - 25 ms</span>
                </div>
                <div class="code-box" style="margin-top: 8px;">
                    <div style="color: #64748b; margin-bottom: 4px;"># Busca Vetorial Top-K</div>
                    <div>results = vector_db.search(</div>
                    <div>&nbsp;&nbsp;query_vector=emb_q,</div>
                    <div>&nbsp;&nbsp;limit=5,</div>
                    <div>&nbsp;&nbsp;score_threshold=0.82</div>
                    <div>)</div>
                </div>
                <div style="margin-top: auto; padding: 12px; border-radius: 10px; background: rgba(59, 130, 246, 0.08); border: 1px dashed rgba(59, 130, 246, 0.25); font-size: 13px; color: #cbd5e1;">
                    💡 <strong>Garantia de Atualização:</strong> Os dados corporativos podem ser atualizados em tempo real sem retraining.
                </div>
            </div>
        </div>

        <!-- Pilar 2: Aumento -->
        <div class="card" style="flex: 1; border-color: rgba(168, 85, 247, 0.35); background: linear-gradient(180deg, rgba(168, 85, 247, 0.07) 0%, rgba(15, 23, 42, 0.7) 100%);">
            <div class="card-title" style="color: #c084fc;">
                <span class="badge badge-purple">Pilar 02</span> Aumento (Augmentation)
            </div>
            <div class="card-desc">Construção dinâmica do prompt de contexto estruturado contendo fatos validados e metadados.</div>
            
            <div style="flex: 1; display: flex; flex-direction: column; gap: 10px; margin-top: 4px;">
                <div class="metric-pill">
                    <span class="lbl">Técnica Principal</span>
                    <span class="val" style="color: #d8b4fe;">Context Injection & Rerank</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Tamanho de Janela</span>
                    <span class="val" style="color: #d8b4fe;">2k - 16k tokens úteis</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Taxa de Compressão</span>
                    <span class="val" style="color: #34d399;">~65% de ruído expurgado</span>
                </div>
                <div class="code-box" style="margin-top: 8px;">
                    <div style="color: #64748b; margin-bottom: 4px;"># Template com Fatos Ancorados</div>
                    <div>prompt = \"\"\"</div>
                    <div>[CONTEXTO AUDITÁVEL]</div>
                    <div>{reranked_chunks}</div>
                    <div>[PERGUNTA]: {user_query}</div>
                    <div>Responda citando a fonte exata.\"\"\"</div>
                </div>
                <div style="margin-top: auto; padding: 12px; border-radius: 10px; background: rgba(168, 85, 247, 0.08); border: 1px dashed rgba(168, 85, 247, 0.25); font-size: 13px; color: #cbd5e1;">
                    🎯 <strong>Mitigação de Alucinação:</strong> O modelo passa a operar como sintetizador de fatos fornecidos explicitamente.
                </div>
            </div>
        </div>

        <!-- Pilar 3: Geração -->
        <div class="card" style="flex: 1; border-color: rgba(16, 185, 129, 0.35); background: linear-gradient(180deg, rgba(16, 185, 129, 0.07) 0%, rgba(15, 23, 42, 0.7) 100%);">
            <div class="card-title" style="color: #34d399;">
                <span class="badge badge-green">Pilar 03</span> Geração (Generation)
            </div>
            <div class="card-desc">Síntese coerente em linguagem natural orientada estritamente aos documentos recuperados.</div>
            
            <div style="flex: 1; display: flex; flex-direction: column; gap: 10px; margin-top: 4px;">
                <div class="metric-pill">
                    <span class="lbl">Modelo de Raciocínio</span>
                    <span class="val" style="color: #6ee7b7;">LLM / LRM Instruction-tuned</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Faithfulness (Fidelidade)</span>
                    <span class="val" style="color: #34d399;">&gt; 98.4% com guardrails</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Rastreabilidade</span>
                    <span class="val" style="color: #6ee7b7;">ID de Documento & Parágrafo</span>
                </div>
                <div class="code-box" style="margin-top: 8px;">
                    <div style="color: #64748b; margin-bottom: 4px;"># Resposta Sintetizada com Citação</div>
                    <div>"Conforme a Política RH-2026</div>
                    <div>(Seção 4.1), o reembolso de</div>
                    <div>cursos de pós-graduação cobre</div>
                    <div>até 80% do valor mensal..."</div>
                </div>
                <div style="margin-top: auto; padding: 12px; border-radius: 10px; background: rgba(16, 185, 129, 0.08); border: 1px dashed rgba(16, 185, 129, 0.25); font-size: 13px; color: #cbd5e1;">
                    🔒 <strong>Auditoria Corporativa:</strong> Toda afirmação gerada possui um link verificável para o documento primário.
                </div>
            </div>
        </div>
    </div>
"""
)

# -------------------------------------------------------------
# FIGURA 02: FLUXO COMPLETO DO RAG: INGESTÃO VS INFERÊNCIA
# -------------------------------------------------------------
TEMPLATES["0003_rag_vector_database/assets/02.png"] = make_page(
    pill="Artigo 0003 • RAG & Vector Database",
    title="Pipeline Duplo: Ingestão Offline vs. Inferência Online",
    subtitle="Desacoplamento de processos para garantir escalabilidade assíncrona e respostas sub-segundo",
    fig_badge="Figura 02",
    content_html="""
    <div class="main-content" style="flex-direction: column; gap: 16px;">
        <!-- Bloco 1: Pipeline Offline -->
        <div class="card" style="flex: 1; border-color: rgba(59, 130, 246, 0.3); background: rgba(59, 130, 246, 0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div class="card-title" style="color: #60a5fa; margin-bottom: 0;">
                    <span class="badge badge-blue">Pipeline Offline</span> Ingestão, Indexação e Armazenamento Vetorial
                </div>
                <span style="font-size: 12.5px; color: #94a3b8; font-family: 'JetBrains Mono', monospace;">Execução Agendada / Batch ETL (Throughput: ~2.500 págs/min)</span>
            </div>
            
            <div style="display: flex; gap: 14px; align-items: center; margin-bottom: 14px;">
                <div style="flex: 1; background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 14px; text-align: center;">
                    <div style="font-size: 11px; color: #60a5fa; font-weight: 700; text-transform: uppercase;">1. Fontes Brutas</div>
                    <div style="font-size: 15px; font-weight: 700; margin: 4px 0;">PDFs, Wiki, DBs</div>
                    <div style="font-size: 12px; color: #64748b;">Textos não estruturados</div>
                </div>
                <div style="color: #3b82f6; font-size: 20px;">➔</div>
                <div style="flex: 1; background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 14px; text-align: center;">
                    <div style="font-size: 11px; color: #60a5fa; font-weight: 700; text-transform: uppercase;">2. Parsing & Limpeza</div>
                    <div style="font-size: 15px; font-weight: 700; margin: 4px 0;">Extração de Texto</div>
                    <div style="font-size: 12px; color: #64748b;">OCR, remoção de ruídos</div>
                </div>
                <div style="color: #3b82f6; font-size: 20px;">➔</div>
                <div style="flex: 1.2; background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 14px; text-align: center;">
                    <div style="font-size: 11px; color: #60a5fa; font-weight: 700; text-transform: uppercase;">3. Chunking Inteligente</div>
                    <div style="font-size: 15px; font-weight: 700; margin: 4px 0;">512 tokens + 10% Overlap</div>
                    <div style="font-size: 12px; color: #64748b;">Preservação semântica</div>
                </div>
                <div style="color: #3b82f6; font-size: 20px;">➔</div>
                <div style="flex: 1.2; background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 14px; text-align: center;">
                    <div style="font-size: 11px; color: #60a5fa; font-weight: 700; text-transform: uppercase;">4. Modelo de Embedding</div>
                    <div style="font-size: 15px; font-weight: 700; margin: 4px 0;">text-embedding-3 / BGE</div>
                    <div style="font-size: 12px; color: #64748b;">Vetores de 1536 dimensões</div>
                </div>
                <div style="color: #3b82f6; font-size: 20px;">➔</div>
                <div style="flex: 1.3; background: rgba(37, 99, 235, 0.12); border: 1px solid rgba(59, 130, 246, 0.35); border-radius: 12px; padding: 14px; text-align: center;">
                    <div style="font-size: 11px; color: #93c5fd; font-weight: 700; text-transform: uppercase;">5. Vector Database</div>
                    <div style="font-size: 15px; font-weight: 700; margin: 4px 0; color: #60a5fa;">HNSW Index + Payload</div>
                    <div style="font-size: 12px; color: #94a3b8;">Armazenamento otimizado</div>
                </div>
            </div>

            <div style="display: flex; gap: 14px; background: rgba(0, 0, 0, 0.25); border-radius: 10px; padding: 10px 14px; font-size: 12.5px; color: #94a3b8;">
                <span style="color: #60a5fa; font-weight: 700;">⚙️ Especificações de Engenharia:</span>
                <span><strong>Batch Size:</strong> 128 chunks</span> • 
                <span><strong>Quantização:</strong> Scalar (SQ8) para reduzir 75% da RAM</span> • 
                <span><strong>Metadados Injetados:</strong> doc_id, section_id, created_at, acl_groups</span>
            </div>
        </div>

        <!-- Bloco 2: Pipeline Online -->
        <div class="card" style="flex: 1; border-color: rgba(16, 185, 129, 0.3); background: rgba(16, 185, 129, 0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div class="card-title" style="color: #34d399; margin-bottom: 0;">
                    <span class="badge badge-green">Pipeline Online</span> Inferência em Tempo Real com Resposta Fundamentada
                </div>
                <span style="font-size: 12.5px; color: #94a3b8; font-family: 'JetBrains Mono', monospace;">Orçamento de Latência p95: ~750ms total</span>
            </div>
            
            <div style="display: flex; gap: 14px; align-items: center; margin-bottom: 14px;">
                <div style="flex: 1; background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 14px; text-align: center;">
                    <div style="font-size: 11px; color: #34d399; font-weight: 700; text-transform: uppercase;">1. Pergunta do Usuário</div>
                    <div style="font-size: 15px; font-weight: 700; margin: 4px 0;">Input Textual</div>
                    <div style="font-size: 12px; color: #64748b;">Frontend / API REST</div>
                </div>
                <div style="color: #10b981; font-size: 20px;">➔</div>
                <div style="flex: 1.1; background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 14px; text-align: center;">
                    <div style="font-size: 11px; color: #34d399; font-weight: 700; text-transform: uppercase;">2. Query Embedding</div>
                    <div style="font-size: 15px; font-weight: 700; margin: 4px 0;">Vetor da Pergunta</div>
                    <div style="font-size: 12px; color: #34d399; font-family: 'JetBrains Mono';">~18 ms</div>
                </div>
                <div style="color: #10b981; font-size: 20px;">➔</div>
                <div style="flex: 1.3; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 12px; padding: 14px; text-align: center;">
                    <div style="font-size: 11px; color: #6ee7b7; font-weight: 700; text-transform: uppercase;">3. Busca Vetorial ANN</div>
                    <div style="font-size: 15px; font-weight: 700; margin: 4px 0; color: #34d399;">Top-K Chunks Relevantes</div>
                    <div style="font-size: 12px; color: #34d399; font-family: 'JetBrains Mono';">~12 ms</div>
                </div>
                <div style="color: #10b981; font-size: 20px;">➔</div>
                <div style="flex: 1.2; background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 14px; text-align: center;">
                    <div style="font-size: 11px; color: #34d399; font-weight: 700; text-transform: uppercase;">4. Augmentation Prompt</div>
                    <div style="font-size: 15px; font-weight: 700; margin: 4px 0;">Contexto + Pergunta</div>
                    <div style="font-size: 12px; color: #34d399; font-family: 'JetBrains Mono';">~4 ms</div>
                </div>
                <div style="color: #10b981; font-size: 20px;">➔</div>
                <div style="flex: 1.3; background: rgba(168, 85, 247, 0.12); border: 1px solid rgba(168, 85, 247, 0.35); border-radius: 12px; padding: 14px; text-align: center;">
                    <div style="font-size: 11px; color: #d8b4fe; font-weight: 700; text-transform: uppercase;">5. Geração LLM</div>
                    <div style="font-size: 15px; font-weight: 700; margin: 4px 0; color: #c084fc;">Resposta com Citação</div>
                    <div style="font-size: 12px; color: #d8b4fe; font-family: 'JetBrains Mono';">~550 - 900 ms</div>
                </div>
            </div>

            <div style="display: flex; gap: 14px; background: rgba(0, 0, 0, 0.25); border-radius: 10px; padding: 10px 14px; font-size: 12.5px; color: #94a3b8;">
                <span style="color: #34d399; font-weight: 700;">🚀 SLA Corporativo:</span>
                <span><strong>Filtro Pré-busca:</strong> Validação de tokens JWT em &lt;2ms</span> • 
                <span><strong>Fallback:</strong> Se score de similaridade &lt;0.70, transborda para triagem humana</span> • 
                <span><strong>Streaming:</strong> Tokens renderizados com TTFT &lt;350ms</span>
            </div>
        </div>
    </div>
"""
)

# -------------------------------------------------------------
# FIGURA 03: COMPARAÇÃO MATRICIAL DE VECTOR DATABASES
# -------------------------------------------------------------
TEMPLATES["0003_rag_vector_database/assets/03.png"] = make_page(
    pill="Artigo 0003 • RAG & Vector Database",
    title="Matriz Comparativa de Bancos Vetoriais Corporativos",
    subtitle="Análise criteriosa de latência, escala, indexação e viabilidade de arquitetura",
    fig_badge="Figura 03",
    content_html="""
    <div class="main-content">
        <div class="card" style="flex: 1; padding: 20px;">
            <table style="width: 100%; border-collapse: separate; border-spacing: 0 8px; font-size: 13.5px;">
                <thead>
                    <tr style="color: #94a3b8; text-transform: uppercase; font-size: 11.5px; letter-spacing: 0.05em; text-align: left;">
                        <th style="padding: 10px 14px;">Banco Vetorial</th>
                        <th style="padding: 10px 14px;">Arquitetura & Tipo</th>
                        <th style="padding: 10px 14px;">Índice ANN Central</th>
                        <th style="padding: 10px 14px;">Filtro de Metadados</th>
                        <th style="padding: 10px 14px;">Latência p95</th>
                        <th style="padding: 10px 14px;">Escalabilidade</th>
                        <th style="padding: 10px 14px;">Melhor Caso de Uso</th>
                    </tr>
                </thead>
                <tbody>
                    <!-- Qdrant -->
                    <tr style="background: rgba(37, 99, 235, 0.08); border-radius: 10px;">
                        <td style="padding: 14px; font-weight: 700; color: #60a5fa; border-top-left-radius: 10px; border-bottom-left-radius: 10px;">
                            ⚡ Qdrant
                        </td>
                        <td style="padding: 14px; color: #e2e8f0;">Rust Standalone / Cloud</td>
                        <td style="padding: 14px; font-family: 'JetBrains Mono'; color: #93c5fd;">HNSW custom + Quantization</td>
                        <td style="padding: 14px;"><span class="badge badge-green">Excelente (Payload JSON)</span></td>
                        <td style="padding: 14px; font-family: 'JetBrains Mono'; color: #34d399;">~6-12 ms</td>
                        <td style="padding: 14px; color: #cbd5e1;">Bilhão de vetores</td>
                        <td style="padding: 14px; color: #94a3b8; border-top-right-radius: 10px; border-bottom-right-radius: 10px;">RAG de alta performance e microsserviços</td>
                    </tr>
                    <!-- pgvector -->
                    <tr style="background: rgba(255, 255, 255, 0.03); border-radius: 10px;">
                        <td style="padding: 14px; font-weight: 700; color: #38bdf8; border-top-left-radius: 10px; border-bottom-left-radius: 10px;">
                            🐘 pgvector (PostgreSQL)
                        </td>
                        <td style="padding: 14px; color: #e2e8f0;">Extensão Relacional ACID</td>
                        <td style="padding: 14px; font-family: 'JetBrains Mono'; color: #7dd3fc;">HNSW / IVFFlat</td>
                        <td style="padding: 14px;"><span class="badge badge-blue">Nativo SQL (JOIN/WHERE)</span></td>
                        <td style="padding: 14px; font-family: 'JetBrains Mono'; color: #fcd34d;">~20-45 ms</td>
                        <td style="padding: 14px; color: #cbd5e1;">Até dezenas de milhões</td>
                        <td style="padding: 14px; color: #94a3b8; border-top-right-radius: 10px; border-bottom-right-radius: 10px;">Aplicações já centradas em PostgreSQL</td>
                    </tr>
                    <!-- Pinecone -->
                    <tr style="background: rgba(255, 255, 255, 0.03); border-radius: 10px;">
                        <td style="padding: 14px; font-weight: 700; color: #c084fc; border-top-left-radius: 10px; border-bottom-left-radius: 10px;">
                            🌲 Pinecone
                        </td>
                        <td style="padding: 14px; color: #e2e8f0;">100% Serverless Managed</td>
                        <td style="padding: 14px; font-family: 'JetBrains Mono'; color: #d8b4fe;">Proprietário otimizado</td>
                        <td style="padding: 14px;"><span class="badge badge-purple">Metadados Filtráveis</span></td>
                        <td style="padding: 14px; font-family: 'JetBrains Mono'; color: #34d399;">~15-25 ms</td>
                        <td style="padding: 14px; color: #cbd5e1;">Auto-scaling nativo</td>
                        <td style="padding: 14px; color: #94a3b8; border-top-right-radius: 10px; border-bottom-right-radius: 10px;">Startups & MVPs sem time de DevOps</td>
                    </tr>
                    <!-- Weaviate -->
                    <tr style="background: rgba(255, 255, 255, 0.03); border-radius: 10px;">
                        <td style="padding: 14px; font-weight: 700; color: #34d399; border-top-left-radius: 10px; border-bottom-left-radius: 10px;">
                            🌀 Weaviate
                        </td>
                        <td style="padding: 14px; color: #e2e8f0;">Go Modular / GraphQL / REST</td>
                        <td style="padding: 14px; font-family: 'JetBrains Mono'; color: #6ee7b7;">HNSW Dinâmico</td>
                        <td style="padding: 14px;"><span class="badge badge-green">Busca Híbrida Nativa</span></td>
                        <td style="padding: 14px; font-family: 'JetBrains Mono'; color: #34d399;">~10-20 ms</td>
                        <td style="padding: 14px; color: #cbd5e1;">Centenas de milhões</td>
                        <td style="padding: 14px; color: #94a3b8; border-top-right-radius: 10px; border-bottom-right-radius: 10px;">Busca híbrida nativa (vetor + BM25)</td>
                    </tr>
                    <!-- Milvus -->
                    <tr style="background: rgba(255, 255, 255, 0.03); border-radius: 10px;">
                        <td style="padding: 14px; font-weight: 700; color: #f59e0b; border-top-left-radius: 10px; border-bottom-left-radius: 10px;">
                            🏛️ Milvus
                        </td>
                        <td style="padding: 14px; color: #e2e8f0;">C++ Distribuído Cloud-Native</td>
                        <td style="padding: 14px; font-family: 'JetBrains Mono'; color: #fcd34d;">Knowhere (HNSW, IVF, GPU)</td>
                        <td style="padding: 14px;"><span class="badge badge-amber">Avançado com Índices</span></td>
                        <td style="padding: 14px; font-family: 'JetBrains Mono'; color: #34d399;">~8-15 ms</td>
                        <td style="padding: 14px; color: #cbd5e1;">Bilhares distribuídos</td>
                        <td style="padding: 14px; color: #94a3b8; border-top-right-radius: 10px; border-bottom-right-radius: 10px;">Grandes corporações em escala massiva</td>
                    </tr>
                    <!-- Chroma -->
                    <tr style="background: rgba(255, 255, 255, 0.03); border-radius: 10px;">
                        <td style="padding: 14px; font-weight: 700; color: #f43f5e; border-top-left-radius: 10px; border-bottom-left-radius: 10px;">
                            🎨 Chroma
                        </td>
                        <td style="padding: 14px; color: #e2e8f0;">Python Embedded / SQLite</td>
                        <td style="padding: 14px; font-family: 'JetBrains Mono'; color: #fda4af;">HNSWlib</td>
                        <td style="padding: 14px;"><span class="badge badge-rose">Básico</span></td>
                        <td style="padding: 14px; font-family: 'JetBrains Mono'; color: #f43f5e;">~30-70 ms</td>
                        <td style="padding: 14px; color: #cbd5e1;">Local / Pequeno porte</td>
                        <td style="padding: 14px; color: #94a3b8; border-top-right-radius: 10px; border-bottom-right-radius: 10px;">Testes locais, protótipos e Jupyter Notebooks</td>
                    </tr>
                </tbody>
            </table>

            <div style="display: flex; gap: 18px; margin-top: 14px; padding-top: 14px; border-top: 1px solid rgba(255, 255, 255, 0.08);">
                <div style="flex: 1; font-size: 13px; color: #94a3b8; line-height: 1.5;">
                    💡 <strong>Critério Chave:</strong> Se você já usa PostgreSQL em produção e possui menos de 10 milhões de documentos, o <span style="color: #38bdf8;">pgvector</span> evita criar novos silos de infraestrutura.
                </div>
                <div style="flex: 1; font-size: 13px; color: #94a3b8; line-height: 1.5;">
                    🚀 <strong>Performance Pura:</strong> Para clusters com dezenas de milhões de itens, filtros complexos por tenant e SLA restrito (&lt;15ms), o <span style="color: #60a5fa;">Qdrant</span> em Rust é a referência moderna da indústria.
                </div>
            </div>
        </div>
    </div>
"""
)

# FIGURA 04: Caso 1: Chatbot Empresarial (RH / TI / Benefícios)
TEMPLATES["0003_rag_vector_database/assets/04.png"] = make_page(
    pill="Caso Corporativo 01 • Artigo 0003",
    title="Chatbot Corporativo com Isolamento de Permissões (RBAC)",
    subtitle="Como evitar vazamento de dados confidenciais através de filtragem por metadados na recuperação",
    fig_badge="Figura 04",
    content_html="""
    <div class="main-content">
        <div class="card" style="flex: 1.2; border-color: rgba(59, 130, 246, 0.3);">
            <div class="card-title" style="color: #60a5fa;">
                <span class="badge badge-blue">Fluxo Seguro</span> Recuperação com Filtro por Perfil
            </div>
            <div class="card-desc">O usuário autenticado carrega suas permissões (roles), que restringem a busca vetorial no banco.</div>

            <div style="display: flex; flex-direction: column; gap: 12px; margin-top: 6px;">
                <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 14px;">
                    <div style="font-size: 12px; color: #60a5fa; font-weight: 700; margin-bottom: 4px;">1. IDENTIDADE DO COLABORADOR</div>
                    <div style="font-size: 13.5px; color: #e2e8f0;">Usuário: <code>joao@empresa.com</code> | Nível: <strong>Engenheiro Pleno</strong> | Depto: <strong>Engenharia</strong></div>
                </div>

                <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 14px;">
                    <div style="font-size: 12px; color: #60a5fa; font-weight: 700; margin-bottom: 4px;">2. QUERY COM INJEÇÃO DE RBAC (PAYLOAD FILTER)</div>
                    <div class="code-box" style="margin-top: 4px;">
                        <div>vector_db.search(</div>
                        <div>&nbsp;&nbsp;query_vector=emb_q,</div>
                        <div>&nbsp;&nbsp;filter={"allowed_departments": ["Engenharia", "Geral"],</div>
                        <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"confidentiality_level": {"$lte": 2}}</div>
                        <div>)</div>
                    </div>
                </div>

                <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 14px;">
                    <div style="font-size: 12px; color: #34d399; font-weight: 700; margin-bottom: 4px;">3. RESPOSTA FUNDAMENTADA COM CITAÇÃO</div>
                    <div style="font-size: 13.5px; color: #e2e8f0; line-height: 1.5;">
                        "De acordo com a <strong>Política de Benefícios 2026 (Cláusula 5.2)</strong>, colaboradores de Engenharia possuem subsídio de até R$ 350/mês para certificações em nuvem."
                    </div>
                </div>
            </div>
        </div>

        <div class="card" style="flex: 1; border-color: rgba(244, 63, 94, 0.3); background: rgba(244, 63, 94, 0.02);">
            <div class="card-title" style="color: #f87171;">
                <span class="badge badge-rose">Prevenção Crítica</span> Vazamento Evitado
            </div>
            <div class="card-desc">O que aconteceria se usássemos apenas busca semântica simples sem controle de acesso:</div>

            <div style="display: flex; flex-direction: column; gap: 14px; margin-top: 8px;">
                <div style="background: rgba(244, 63, 94, 0.08); border: 1px dashed rgba(244, 63, 94, 0.3); border-radius: 12px; padding: 16px;">
                    <div style="font-weight: 700; color: #fca5a5; margin-bottom: 6px;">❌ Risco: Dados Executivos e Bônus</div>
                    <div style="font-size: 13px; color: #cbd5e1; line-height: 1.5;">
                        Se a busca vetorial retornar chunks de "Tabelas Salariais C-Level" porque o usuário perguntou sobre "faixas de bônus", o LLM responderá vazando informações sigilosas.
                    </div>
                </div>

                <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 16px;">
                    <div style="font-weight: 700; color: #6ee7b7; margin-bottom: 6px;">✅ Solução com Vector DB Moderno</div>
                    <div style="font-size: 13px; color: #cbd5e1; line-height: 1.5;">
                        O filtro pré-busca (Pre-Filtering) elimina os nós restritos <em>antes</em> do cálculo de similaridade HNSW, garantindo latência &lt;10ms e segurança matemática 100% estrita.
                    </div>
                </div>
            </div>
        </div>
    </div>
"""
)

# FIGURA 05: Caso 2: Assistente Técnico de Engenharia (APIs & Codebases)
TEMPLATES["0003_rag_vector_database/assets/05.png"] = make_page(
    pill="Caso Corporativo 02 • Artigo 0003",
    title="Assistente Técnico de Engenharia e Troubleshooting",
    subtitle="Indexação combinada de documentação OpenAPI, logs de incidentes e commits do repositório",
    fig_badge="Figura 05",
    content_html="""
    <div class="main-content">
        <div class="card" style="flex: 1; border-color: rgba(139, 92, 246, 0.3);">
            <div class="card-title" style="color: #c084fc;">
                <span class="badge badge-purple">Entrada & Indexação</span> Fontes Técnicas
            </div>
            <div class="card-desc">Dados heterogêneos convertidos em chunks com sintaxe preservada.</div>

            <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 4px;">
                <div class="metric-pill">
                    <span class="lbl">Documentações Swagger / OpenAPI</span>
                    <span class="val" style="color: #d8b4fe;">Endpoints & Payloads</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Histórico Post-Mortem SRE</span>
                    <span class="val" style="color: #d8b4fe;">Causa-raiz & Mitigações</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Repositórios Git (.py, .ts, .cs)</span>
                    <span class="val" style="color: #d8b4fe;">Assinaturas de Funções</span>
                </div>
                <div class="code-box" style="margin-top: 6px;">
                    <div style="color: #64748b;"># Metadado Técnico do Chunk</div>
                    <div>{"file": "src/payments/gateway.py",</div>
                    <div>&nbsp;"commit": "7f8b9a1",</div>
                    <div>&nbsp;"error_code": "ERR_PAYMENT_TIMEOUT"}</div>
                </div>
            </div>
        </div>

        <div class="card" style="flex: 1.3; border-color: rgba(59, 130, 246, 0.3);">
            <div class="card-title" style="color: #60a5fa;">
                <span class="badge badge-blue">Inferência Híbrida</span> Diagnóstico de Erro em Produção
            </div>
            <div class="card-desc">Desenvolvedor pesquisa stack trace real e recebe diagnóstico + snippet de correção.</div>

            <div style="display: flex; flex-direction: column; gap: 12px; margin-top: 4px;">
                <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 12px;">
                    <div style="font-size: 11px; color: #f59e0b; font-weight: 700;">PROMPT DO ENGENHEIRO:</div>
                    <div style="font-size: 13px; font-family: 'JetBrains Mono'; color: #fcd34d; margin-top: 4px;">
                        "ConnectionResetError: [Errno 104] Connection reset by peer no endpoint /v2/checkout"
                    </div>
                </div>

                <div class="code-box">
                    <div style="color: #34d399; font-weight: 700; margin-bottom: 4px;">✓ DIAGNÓSTICO DO RAG (Baseado no Post-Mortem INC-482):</div>
                    <div style="color: #cbd5e1; font-size: 13px; line-height: 1.5;">
                        "Este erro ocorre quando o pool de conexões do Redis atinge <code>max_connections=50</code> durante picos de checkout.
                        <strong>Solução homologada:</strong> ajustar o <code>keepalive_timeout</code> para 15s e implementar backoff exponencial."
                    </div>
                    <div style="margin-top: 8px; color: #60a5fa; font-size: 12px;">
                        📄 Fonte: <em>wiki/sre/post-mortem/inc-482-redis-pool.md (Linha 42)</em>
                    </div>
                </div>
            </div>
        </div>
    </div>
"""
)

# FIGURA 06: Caso 3: Suporte ao Cliente em Escala (Atendimento N1 / N2)
TEMPLATES["0003_rag_vector_database/assets/06.png"] = make_page(
    pill="Caso Corporativo 03 • Artigo 0003",
    title="Suporte ao Cliente com Triagem Inteligente N1/N2",
    subtitle="Automação de 70%+ dos chamados recorrentes com fallback determinístico para atendentes humanos",
    fig_badge="Figura 06",
    content_html="""
    <div class="main-content">
        <div class="card" style="flex: 1; border-color: rgba(16, 185, 129, 0.3);">
            <div class="card-title" style="color: #34d399;">
                <span class="badge badge-green">Nível 1 (Autônomo)</span> Resolução Direta por RAG
            </div>
            <div class="card-desc">Chamados frequentes com alta similaridade vetorial e score &gt; 0.85.</div>

            <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 6px;">
                <div class="metric-pill">
                    <span class="lbl">Taxa de Resolução First-Contact</span>
                    <span class="val" style="color: #34d399;">73.8%</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Tempo Médio de Atendimento (TMA)</span>
                    <span class="val" style="color: #34d399;">1.2 segundos</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Custo por Ticket</span>
                    <span class="val" style="color: #34d399;">~R$ 0,04 (vs R$ 18,50 humano)</span>
                </div>
                <div style="padding: 12px; border-radius: 10px; background: rgba(16, 185, 129, 0.08); border: 1px dashed rgba(16, 185, 129, 0.25); font-size: 13px; color: #cbd5e1; margin-top: auto;">
                    💬 <strong>Exemplo:</strong> Alteração de dados cadastrais, segunda via de boleto, regras de cancelamento e status de pedidos.
                </div>
            </div>
        </div>

        <div class="card" style="flex: 1; border-color: rgba(245, 158, 11, 0.3);">
            <div class="card-title" style="color: #fbbf24;">
                <span class="badge badge-amber">Nível 2 (Híbrido)</span> Escalabilidade para Humano
            </div>
            <div class="card-desc">Situações de baixa confiança semântica ou detecção de sentimentos críticos.</div>

            <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 6px;">
                <div class="metric-pill">
                    <span class="lbl">Gatilho de Transbordo</span>
                    <span class="val" style="color: #fcd34d;">Score &lt; 0.75 ou Sentimento Irritado</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Apoio ao Atendente (Copilot)</span>
                    <span class="val" style="color: #fcd34d;">Resumo do caso + Sugestões</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Redução no Tempo de Resolução</span>
                    <span class="val" style="color: #fcd34d;">-48% no N2 Humano</span>
                </div>
                <div style="padding: 12px; border-radius: 10px; background: rgba(245, 158, 11, 0.08); border: 1px dashed rgba(245, 158, 11, 0.25); font-size: 13px; color: #cbd5e1; margin-top: auto;">
                    🛡️ <strong>Zero Alucinação com Cliente:</strong> O bot nunca arrisca inventar políticas quando o score de confiança não atinge o threshold corporativo.
                </div>
            </div>
        </div>
    </div>
"""
)

# FIGURA 07: Caso 4: Análise Legal & Compliance
TEMPLATES["0003_rag_vector_database/assets/07.png"] = make_page(
    pill="Caso Corporativo 04 • Artigo 0003",
    title="Auditoria Jurídica & Compliance Contratual",
    subtitle="Conformidade estrita com LGPD e normas regulatórias através de extração referenciada de cláusulas",
    fig_badge="Figura 07",
    content_html="""
    <div class="main-content">
        <div class="card" style="flex: 1.2; border-color: rgba(6, 182, 212, 0.3);">
            <div class="card-title" style="color: #22d3ee;">
                <span class="badge badge-cyan">Processamento de Contrato</span> Extração & Mapeamento
            </div>
            <div class="card-desc">Varredura de centenas de páginas identificando passivos, multas e responsabilidades.</div>

            <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 6px;">
                <div class="code-box">
                    <div style="color: #67e8f9; font-weight: 700; margin-bottom: 4px;">QUERY JURÍDICA:</div>
                    <div>"Qual é a cláusula de rescisão imotivada e o prazo de aviso prévio previsto?"</div>
                </div>
                <div class="code-box" style="background: rgba(6, 182, 212, 0.06); border-color: rgba(6, 182, 212, 0.3);">
                    <div style="color: #34d399; font-weight: 700; margin-bottom: 4px;">TRECHO RECUPERADO (Contrato_Prestacao_Servicos_v4.pdf):</div>
                    <div style="font-size: 12.5px; color: #cbd5e1; line-height: 1.5;">
                        "Cláusula 12.3: Qualquer das partes poderá rescindir o presente instrumento sem justa causa, mediante aviso prévio por escrito com antecedência mínima de <strong>60 (sessenta) dias</strong>, sob pena de multa equivalente a 2 (duas) mensalidades..."
                    </div>
                </div>
            </div>
        </div>

        <div class="card" style="flex: 1; border-color: rgba(16, 185, 129, 0.3);">
            <div class="card-title" style="color: #34d399;">
                <span class="badge badge-green">Auditoria Sem Erro</span> Pilares de Validação
            </div>
            <div class="card-desc">Critérios mandatórios para aprovação de pareceres jurídicos em IA:</div>

            <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 6px;">
                <div class="metric-pill">
                    <span class="lbl">Precisão de Citação de Cláusula</span>
                    <span class="val" style="color: #34d399;">100% Determinística</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Conformidade com LGPD / GDPR</span>
                    <span class="val" style="color: #34d399;">Anonimização de PII</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Velocidade de Análise de Minuta</span>
                    <span class="val" style="color: #34d399;">De 4 dias para 3 minutos</span>
                </div>
                <div style="padding: 12px; border-radius: 10px; background: rgba(16, 185, 129, 0.08); border: 1px dashed rgba(16, 185, 129, 0.25); font-size: 13px; color: #cbd5e1; margin-top: auto;">
                    ⚖️ <strong>Assinatura Auditável:</strong> O relatório gerado anexa a página original do PDF com marca d'água de verificação para o time jurídico.
                </div>
            </div>
        </div>
    </div>
"""
)

# FIGURA 08: Caso 5: Recomendação Inteligente Multimodal
TEMPLATES["0003_rag_vector_database/assets/08.png"] = make_page(
    pill="Caso Corporativo 05 • Artigo 0003",
    title="Busca Semântica & Recomendação Multimodal em E-commerce",
    subtitle="Conexão de descrições textuais, imagens de produtos e intenção do comprador no mesmo espaço vetorial",
    fig_badge="Figura 08",
    content_html="""
    <div class="main-content">
        <div class="card" style="flex: 1; border-color: rgba(168, 85, 247, 0.3);">
            <div class="card-title" style="color: #c084fc;">
                <span class="badge badge-purple">Entrada & Espaço Vetorial</span> Embeddings Multimodais
            </div>
            <div class="card-desc">Modelos como CLIP e SigLIP unificam texto e imagens no mesmo espaço latente.</div>

            <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 6px;">
                <div class="metric-pill">
                    <span class="lbl">Modelo de Projeção</span>
                    <span class="val" style="color: #d8b4fe;">OpenAI CLIP / SigLIP</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Dimensões Unificadas</span>
                    <span class="val" style="color: #d8b4fe;">768 Dimensões</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Entrada Aceita</span>
                    <span class="val" style="color: #d8b4fe;">Foto da Câmera ou Texto Livre</span>
                </div>
                <div class="code-box" style="margin-top: 6px;">
                    <div style="color: #64748b;"># Consulta Multimodal</div>
                    <div>query_emb = clip.encode_image(photo)</div>
                    <div>recs = qdrant.search(</div>
                    <div>&nbsp;&nbsp;collection="catalog",</div>
                    <div>&nbsp;&nbsp;vector=query_emb</div>
                    <div>)</div>
                </div>
            </div>
        </div>

        <div class="card" style="flex: 1.2; border-color: rgba(16, 185, 129, 0.3);">
            <div class="card-title" style="color: #34d399;">
                <span class="badge badge-green">Experiência do Usuário</span> Superação da Busca por Palavra-Chave
            </div>
            <div class="card-desc">O cliente pesquisa conceitos abstratos e encontra exatamente o produto ideal.</div>

            <div style="display: flex; flex-direction: column; gap: 12px; margin-top: 6px;">
                <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: 10px; padding: 12px;">
                    <div style="font-size: 11.5px; color: #f87171; font-weight: 700;">BUSCA TRADICIONAL (SQL LIKE / ELASTICSEARCH BM25):</div>
                    <div style="font-size: 13px; color: #cbd5e1; margin-top: 4px;">
                        Busca: "look casual para casamento na praia no fim da tarde"<br>
                        Resultado: <em>Zero resultados ou vestidos de noiva formais caros.</em>
                    </div>
                </div>

                <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; padding: 12px;">
                    <div style="font-size: 11.5px; color: #34d399; font-weight: 700;">BUSCA SEMÂNTICA MULTIMODAL (RAG + VECTOR DB):</div>
                    <div style="font-size: 13px; color: #cbd5e1; margin-top: 4px;">
                        Resultado: <em>Camisas de linho bege, vestidos florais fluidos e calçados leves em tons claros.</em>
                    </div>
                </div>

                <div class="metric-pill" style="margin-top: auto;">
                    <span class="lbl">Aumento na Taxa de Conversão (E-commerce)</span>
                    <span class="val" style="color: #34d399;">+32.6% no Checkout</span>
                </div>
            </div>
        </div>
    </div>
"""
)

# -------------------------------------------------------------
# FIGURA 09: ARQUITETURA RAG DE PRODUÇÃO COMPLETA
# -------------------------------------------------------------
TEMPLATES["0003_rag_vector_database/assets/09.png"] = make_page(
    pill="Arquitetura de Referência • Artigo 0003",
    title="Arquitetura RAG Corporativa de Produção (End-to-End)",
    subtitle="Componentes essenciais para alta escalabilidade, tolerância a falhas, governança e observabilidade",
    fig_badge="Figura 09",
    content_html="""
    <div class="main-content" style="gap: 16px;">
        <!-- Coluna 1: Gateway & Ingestão -->
        <div class="card" style="flex: 1; border-color: rgba(59, 130, 246, 0.3);">
            <div class="card-title" style="color: #60a5fa; font-size: 17px;">
                <span class="badge badge-blue">Camada 01</span> Ingestão & Roteamento
            </div>
            <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 6px;">
                <div class="metric-pill">
                    <span class="lbl">API Gateway / Auth</span>
                    <span class="val" style="color: #93c5fd;">OAuth2 + JWT RBAC</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Query Rewriter / HyDE</span>
                    <span class="val" style="color: #93c5fd;">Expansão Semântica</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Extrator ETL Assíncrono</span>
                    <span class="val" style="color: #93c5fd;">Apache Tika / Unstructured</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Chunker Hierárquico</span>
                    <span class="val" style="color: #93c5fd;">Small-to-Big Retrieval</span>
                </div>
            </div>

            <div style="margin-top: auto; padding: 14px; background: rgba(59, 130, 246, 0.08); border-radius: 12px; border: 1px dashed rgba(59, 130, 246, 0.25); font-size: 12.5px; color: #cbd5e1; line-height: 1.5;">
                <strong style="color: #60a5fa;">💡 Prática de Produção:</strong> A expansão HyDE (Hypothetical Document Embeddings) sintetiza uma resposta teórica antes da busca para alinhar a distância vetorial.
            </div>
        </div>

        <!-- Coluna 2: Indexação & Vector DB -->
        <div class="card" style="flex: 1; border-color: rgba(16, 185, 129, 0.3);">
            <div class="card-title" style="color: #34d399; font-size: 17px;">
                <span class="badge badge-green">Camada 02</span> Recuperação & Índices
            </div>
            <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 6px;">
                <div class="metric-pill">
                    <span class="lbl">Vector Database Cluster</span>
                    <span class="val" style="color: #6ee7b7;">Qdrant / Milvus / pgvector</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Algoritmo de Indexação</span>
                    <span class="val" style="color: #6ee7b7;">HNSW + Product Quantization</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Busca Híbrida</span>
                    <span class="val" style="color: #6ee7b7;">Dense (Cosine) + Sparse (BM25)</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Reranker Neural</span>
                    <span class="val" style="color: #6ee7b7;">Cross-Encoder (BGE / Cohere)</span>
                </div>
            </div>

            <div style="margin-top: auto; padding: 14px; background: rgba(16, 185, 129, 0.08); border-radius: 12px; border: 1px dashed rgba(16, 185, 129, 0.25); font-size: 12.5px; color: #cbd5e1; line-height: 1.5;">
                <strong style="color: #34d399;">⚡ Otimização HNSW:</strong> Configurar <code>M=16</code> e <code>ef_search=64</code> assegura 98% de recall com tempo de busca sub-10ms em bases de milhões de vetores.
            </div>
        </div>

        <!-- Coluna 3: LLM & Guardrails -->
        <div class="card" style="flex: 1; border-color: rgba(168, 85, 247, 0.3);">
            <div class="card-title" style="color: #c084fc; font-size: 17px;">
                <span class="badge badge-purple">Camada 03</span> Raciocínio & Segurança
            </div>
            <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 6px;">
                <div class="metric-pill">
                    <span class="lbl">Prompt Engine</span>
                    <span class="val" style="color: #d8b4fe;">Context Window Assembly</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Modelo de Raciocínio</span>
                    <span class="val" style="color: #d8b4fe;">Claude / GPT-4o / DeepSeek R1</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Safety Guardrails</span>
                    <span class="val" style="color: #d8b4fe;">NeMo / Llama-Guard 3</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Output Parser</span>
                    <span class="val" style="color: #d8b4fe;">JSON Schema Determinístico</span>
                </div>
            </div>

            <div style="margin-top: auto; padding: 14px; background: rgba(168, 85, 247, 0.08); border-radius: 12px; border: 1px dashed rgba(168, 85, 247, 0.25); font-size: 12.5px; color: #cbd5e1; line-height: 1.5;">
                <strong style="color: #c084fc;">🛡️ Barreira de Segurança:</strong> Os guardrails analisam tanto o prompt contra injeções quanto o output contra vazamento de PII e alucinações factuais.
            </div>
        </div>

        <!-- Coluna 4: Observabilidade -->
        <div class="card" style="flex: 1; border-color: rgba(245, 158, 11, 0.3);">
            <div class="card-title" style="color: #fbbf24; font-size: 17px;">
                <span class="badge badge-amber">Camada 04</span> Governança & Métricas
            </div>
            <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 6px;">
                <div class="metric-pill">
                    <span class="lbl">Tracer de Latência</span>
                    <span class="val" style="color: #fcd34d;">OpenTelemetry / Langfuse</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Monitor de Alucinação</span>
                    <span class="val" style="color: #fcd34d;">RAGAS Faithfulness &gt; 0.90</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Gestão de Custos</span>
                    <span class="val" style="color: #fcd34d;">Controle de Tokens / Cache</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Log de Auditoria</span>
                    <span class="val" style="color: #fcd34d;">Immutable Query Trace</span>
                </div>
            </div>

            <div style="margin-top: auto; padding: 14px; background: rgba(245, 158, 11, 0.08); border-radius: 12px; border: 1px dashed rgba(245, 158, 11, 0.25); font-size: 12.5px; color: #cbd5e1; line-height: 1.5;">
                <strong style="color: #fbbf24;">📊 Ciclo de Feedback:</strong> Logs com baixa nota de relevância alimentam automaticamente a fila de re-indexação e curadoria técnica.
            </div>
        </div>
    </div>
"""
)

# -------------------------------------------------------------
# FIGURA 10: AS 5 ESTRATÉGIAS DE CHUNKING (Alta Densidade)
# -------------------------------------------------------------
TEMPLATES["0003_rag_vector_database/assets/10.png"] = make_page(
    pill="Engenharia de Dados • Artigo 0003",
    title="As 5 Estratégias Fundamentais de Chunking",
    subtitle="Como a fragmentação do texto define diretamente a precisão semântica e evita perda de contexto",
    fig_badge="Figura 10",
    content_html="""
    <div class="main-content" style="gap: 16px;">
        <!-- Estratégia 1 -->
        <div class="card" style="flex: 1; border-color: rgba(59, 130, 246, 0.3);">
            <div class="card-title" style="color: #60a5fa; font-size: 16px;">
                <span class="badge badge-blue">01</span> Fixo com Overlap
            </div>
            <div class="card-desc">Janela de tamanho fixo com sobreposição nas bordas.</div>
            
            <div class="code-box" style="margin-bottom: 10px; font-size: 11px;">
                [--- Chunk A: 500t ---]<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[-- Overlap: 50t --]<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[--- Chunk B: 500t ---]
            </div>

            <div style="display: flex; flex-direction: column; gap: 6px; margin: 8px 0;">
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Custo CPU Ingestão</span>
                    <span class="val" style="color: #34d399; font-size: 12px;">Mínimo</span>
                </div>
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Integridade Frasal</span>
                    <span class="val" style="color: #f87171; font-size: 12px;">Baixa</span>
                </div>
            </div>

            <div style="font-size: 12px; color: #94a3b8; line-height: 1.4; margin-top: auto; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.08);">
                <strong>Aplicação:</strong> Protótipos rápidos e documentos de texto corrido sem formatação complexa.
            </div>
        </div>

        <!-- Estratégia 2 -->
        <div class="card" style="flex: 1; border-color: rgba(16, 185, 129, 0.3);">
            <div class="card-title" style="color: #34d399; font-size: 16px;">
                <span class="badge badge-green">02</span> Recursivo Frasal
            </div>
            <div class="card-desc">Divisão hierárquica por quebras naturais do idioma.</div>
            
            <div class="code-box" style="margin-bottom: 10px; font-size: 11px;">
                separators = [<br>
                &nbsp;&nbsp;"\\n\\n", "\\n", ". ", " "<br>
                ]<br>
                chunk_size = 512
            </div>

            <div style="display: flex; flex-direction: column; gap: 6px; margin: 8px 0;">
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Custo CPU Ingestão</span>
                    <span class="val" style="color: #34d399; font-size: 12px;">Baixo</span>
                </div>
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Integridade Frasal</span>
                    <span class="val" style="color: #34d399; font-size: 12px;">Alta</span>
                </div>
            </div>

            <div style="font-size: 12px; color: #94a3b8; line-height: 1.4; margin-top: auto; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.08);">
                <strong>Aplicação:</strong> Padrão geral para 80% das aplicações corporativas de artigos, notícias e e-mails.
            </div>
        </div>

        <!-- Estratégia 3 -->
        <div class="card" style="flex: 1; border-color: rgba(168, 85, 247, 0.3);">
            <div class="card-title" style="color: #c084fc; font-size: 16px;">
                <span class="badge badge-purple">03</span> Estrutural (Doc)
            </div>
            <div class="card-desc">Respeita seções Markdown (H1, H2), HTML ou tabelas.</div>
            
            <div class="code-box" style="margin-bottom: 10px; font-size: 11px;">
                # Header 1 (Meta: Seção)<br>
                ## Header 2 (Meta: Tópico)<br>
                [Chunk com Breadcrumb]
            </div>

            <div style="display: flex; flex-direction: column; gap: 6px; margin: 8px 0;">
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Injeção de Metadados</span>
                    <span class="val" style="color: #d8b4fe; font-size: 12px;">Excelente</span>
                </div>
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Preservação Contexto</span>
                    <span class="val" style="color: #34d399; font-size: 12px;">Total</span>
                </div>
            </div>

            <div style="font-size: 12px; color: #94a3b8; line-height: 1.4; margin-top: auto; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.08);">
                <strong>Aplicação:</strong> Wikis do Confluence, documentações OpenAPI, manuais de produtos e contratos.
            </div>
        </div>

        <!-- Estratégia 4 -->
        <div class="card" style="flex: 1; border-color: rgba(245, 158, 11, 0.3);">
            <div class="card-title" style="color: #fbbf24; font-size: 16px;">
                <span class="badge badge-amber">04</span> Semântico Adaptativo
            </div>
            <div class="card-desc">Corta o texto apenas quando o tema semântico muda.</div>
            
            <div class="code-box" style="margin-bottom: 10px; font-size: 11px;">
                sim(sent_1, sent_2) = 0.89<br>
                sim(sent_2, sent_3) = 0.41<br>
                ➔ Ponto de Quebra!
            </div>

            <div style="display: flex; flex-direction: column; gap: 6px; margin: 8px 0;">
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Homogeneidade</span>
                    <span class="val" style="color: #34d399; font-size: 12px;">Máxima</span>
                </div>
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Custo de Ingestão</span>
                    <span class="val" style="color: #fcd34d; font-size: 12px;">Alto</span>
                </div>
            </div>

            <div style="font-size: 12px; color: #94a3b8; line-height: 1.4; margin-top: auto; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.08);">
                <strong>Aplicação:</strong> Transcrições de áudio/reuniões, podcasts e relatórios discursivos densos.
            </div>
        </div>

        <!-- Estratégia 5 -->
        <div class="card" style="flex: 1; border-color: rgba(6, 182, 212, 0.3);">
            <div class="card-title" style="color: #22d3ee; font-size: 16px;">
                <span class="badge badge-cyan">05</span> Parent-Child
            </div>
            <div class="card-desc">Busca em micro-blocos e injeta o bloco-pai no LLM.</div>
            
            <div class="code-box" style="margin-bottom: 10px; font-size: 11px;">
                [Parent Block: 1024 tokens]<br>
                &nbsp;&nbsp;↳ Mini A: 128t (Index)<br>
                &nbsp;&nbsp;↳ Mini B: 128t (Index)
            </div>

            <div style="display: flex; flex-direction: column; gap: 6px; margin: 8px 0;">
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Precisão de Busca</span>
                    <span class="val" style="color: #34d399; font-size: 12px;">Extrema</span>
                </div>
                <div class="metric-pill" style="padding: 6px 10px; margin-bottom: 0;">
                    <span class="lbl" style="font-size: 11.5px;">Contexto Síntese</span>
                    <span class="val" style="color: #34d399; font-size: 12px;">Completo</span>
                </div>
            </div>

            <div style="font-size: 12px; color: #94a3b8; line-height: 1.4; margin-top: auto; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.08);">
                <strong>Aplicação:</strong> Pipelines de alta precisão (jurídico, financeiro e suporte técnico N2).
            </div>
        </div>
    </div>
"""
)

# -------------------------------------------------------------
# FIGURA 11: OTIMIZAÇÃO AVANÇADA: BUSCA HÍBRIDA & RERANKER
# -------------------------------------------------------------
TEMPLATES["0003_rag_vector_database/assets/11.png"] = make_page(
    pill="Otimização de Performance • Artigo 0003",
    title="Busca Híbrida (Dense + Sparse) com Reranker Cross-Encoder",
    subtitle="Como combinar o melhor de palavras-chave exatas e similaridade semântica para maximizar o Hit-Rate",
    fig_badge="Figura 11",
    content_html="""
    <div class="main-content">
        <!-- Lado 1: Busca Híbrida -->
        <div class="card" style="flex: 1.2; border-color: rgba(59, 130, 246, 0.3);">
            <div class="card-title" style="color: #60a5fa;">
                <span class="badge badge-blue">Etapa 01</span> Busca Híbrida + Fusão Recíproca (RRF)
            </div>
            <div class="card-desc">Supera as fraquezas isoladas do BM25 (perde sinônimos) e do vetor denso (perde códigos e SKUs exatos).</div>

            <div style="display: flex; gap: 12px; margin-top: 6px;">
                <div style="flex: 1; background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 12px;">
                    <div style="font-size: 11px; color: #93c5fd; font-weight: 700;">BUSCA DENSA (VETORIAL)</div>
                    <div style="font-size: 13px; margin: 4px 0; color: #e2e8f0;">Similaridade Semântica</div>
                    <div style="font-size: 11.5px; color: #94a3b8;">Captura intenção e conceitos</div>
                </div>
                <div style="flex: 1; background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 12px;">
                    <div style="font-size: 11px; color: #34d399; font-weight: 700;">BUSCA ESPARSA (BM25)</div>
                    <div style="font-size: 13px; margin: 4px 0; color: #e2e8f0;">Correspondência Exata</div>
                    <div style="font-size: 11.5px; color: #94a3b8;">Excelente para códigos e IDs</div>
                </div>
            </div>

            <div class="code-box" style="margin-top: 12px;">
                <div style="color: #64748b; margin-bottom: 2px;"># Reciprocal Rank Fusion (RRF)</div>
                <div>RRF_Score(d) = Σ [ 1 / (60 + rank_dense(d)) ] + [ 1 / (60 + rank_bm25(d)) ]</div>
            </div>

            <div style="margin-top: auto; padding: 12px; border-radius: 10px; background: rgba(59, 130, 246, 0.08); border: 1px dashed rgba(59, 130, 246, 0.25); font-size: 13px; color: #cbd5e1;">
                📈 <strong>Ganho Médio:</strong> A busca híbrida eleva o Recall@10 de 72% para <strong>91.4%</strong> em bases heterogêneas.
            </div>
        </div>

        <!-- Lado 2: Cross-Encoder Reranker -->
        <div class="card" style="flex: 1; border-color: rgba(16, 185, 129, 0.3);">
            <div class="card-title" style="color: #34d399;">
                <span class="badge badge-green">Etapa 02</span> Cross-Encoder Reranker
            </div>
            <div class="card-desc">Reordenação profunda dos 30 candidatos brutos para filtrar os 5 melhores.</div>

            <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 6px;">
                <div class="metric-pill">
                    <span class="lbl">Entrada Inicial do Vector DB</span>
                    <span class="val" style="color: #cbd5e1;">Top-30 Chunks Candidatos</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Atenção Cruzada (Cross-Attention)</span>
                    <span class="val" style="color: #6ee7b7;">Query ⨂ Passage Simultâneo</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Filtro Final para o Contexto LLM</span>
                    <span class="val" style="color: #34d399;">Top-5 Chunks Mais Precisos</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Latência Adicional do Rerank</span>
                    <span class="val" style="color: #34d399;">~15 - 35 ms</span>
                </div>
                <div style="margin-top: auto; padding: 12px; border-radius: 10px; background: rgba(16, 185, 129, 0.08); border: 1px dashed rgba(16, 185, 129, 0.25); font-size: 13px; color: #cbd5e1;">
                    🎯 <strong>Fidelidade Máxima:</strong> Reduz o custo de tokens no LLM em até 60% e elimina o problema de "Lost in the Middle".
                </div>
            </div>
        </div>
    </div>
"""
)

# -------------------------------------------------------------
# FIGURA 12: FRAMEWORK DE AVALIAÇÃO RAG (Alta Densidade)
# -------------------------------------------------------------
TEMPLATES["0003_rag_vector_database/assets/12.png"] = make_page(
    pill="Governança & Qualidade • Artigo 0003",
    title="Framework de Avaliação RAG: As 4 Métricas Essenciais",
    subtitle="Como mensurar cientificamente precisão de recuperação e fidelidade de geração (RAG Triad & RAGAS)",
    fig_badge="Figura 12",
    content_html="""
    <div class="main-content" style="gap: 16px;">
        <!-- Métrica 1 -->
        <div class="card" style="flex: 1; border-color: rgba(59, 130, 246, 0.35); background: linear-gradient(180deg, rgba(59, 130, 246, 0.08) 0%, rgba(15, 23, 42, 0.7) 100%);">
            <div class="card-title" style="color: #60a5fa;">
                <span class="badge badge-blue">Métrica 01</span> Context Relevance
            </div>
            <div class="card-desc">Quão relevantes são os fragmentos recuperados para a pergunta?</div>
            
            <div class="metric-pill">
                <span class="lbl">Meta Corporativa</span>
                <span class="val" style="color: #34d399;">&gt; 0.88</span>
            </div>

            <div class="code-box" style="font-size: 11px; margin: 8px 0;">
                # Avalia ruído na recuperação<br>
                Relevance = |Chunks Úteis| / |Total Chunks Top-K|
            </div>

            <div style="background: rgba(239, 68, 68, 0.06); border-radius: 8px; padding: 8px 10px; font-size: 11.5px; color: #fca5a5; margin-bottom: 8px;">
                ⚠️ <strong>Causa de Baixa Nota:</strong> Chunk size muito grande (&gt;1000t) ou falta de reranker.
            </div>

            <div style="margin-top: auto; font-size: 12px; color: #93c5fd; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.08);">
                🛠️ <strong>Ação:</strong> Aplicar Parent-Child ou diminuir chunk para 256 tokens com reranker neural.
            </div>
        </div>

        <!-- Métrica 2 -->
        <div class="card" style="flex: 1; border-color: rgba(168, 85, 247, 0.35); background: linear-gradient(180deg, rgba(168, 85, 247, 0.08) 0%, rgba(15, 23, 42, 0.7) 100%);">
            <div class="card-title" style="color: #c084fc;">
                <span class="badge badge-purple">Métrica 02</span> Context Recall
            </div>
            <div class="card-desc">O pipeline recuperou todas as informações necessárias para a resposta?</div>
            
            <div class="metric-pill">
                <span class="lbl">Meta Corporativa</span>
                <span class="val" style="color: #34d399;">&gt; 0.92</span>
            </div>

            <div class="code-box" style="font-size: 11px; margin: 8px 0;">
                # Avalia omissão de fatos<br>
                Recall = |Fatos Recuperados| / |Fatos da Resposta Real|
            </div>

            <div style="background: rgba(239, 68, 68, 0.06); border-radius: 8px; padding: 8px 10px; font-size: 11.5px; color: #fca5a5; margin-bottom: 8px;">
                ⚠️ <strong>Causa de Baixa Nota:</strong> Top-K muito baixo (ex: k=2) ou falha na correspondência léxica.
            </div>

            <div style="margin-top: auto; font-size: 12px; color: #d8b4fe; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.08);">
                🛠️ <strong>Ação:</strong> Implementar busca híbrida (BM25 + Dense) e expandir Top-K inicial para 25.
            </div>
        </div>

        <!-- Métrica 3 -->
        <div class="card" style="flex: 1; border-color: rgba(16, 185, 129, 0.35); background: linear-gradient(180deg, rgba(16, 185, 129, 0.08) 0%, rgba(15, 23, 42, 0.7) 100%);">
            <div class="card-title" style="color: #34d399;">
                <span class="badge badge-green">Métrica 03</span> Faithfulness
            </div>
            <div class="card-desc">A resposta gerada é 100% inferível dos trechos recuperados (Zero Alucinação)?</div>
            
            <div class="metric-pill">
                <span class="lbl">Meta Corporativa</span>
                <span class="val" style="color: #34d399;">&gt; 0.98</span>
            </div>

            <div class="code-box" style="font-size: 11px; margin: 8px 0;">
                # Avalia verdade factual<br>
                Faithfulness = |Afirmações Fundamentadas| / |Afirmações|
            </div>

            <div style="background: rgba(239, 68, 68, 0.06); border-radius: 8px; padding: 8px 10px; font-size: 11.5px; color: #fca5a5; margin-bottom: 8px;">
                ⚠️ <strong>Causa de Baixa Nota:</strong> LLM criativo demais (temperatura &gt; 0.3) ou prompt permissivo.
            </div>

            <div style="margin-top: auto; font-size: 12px; color: #6ee7b7; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.08);">
                🛠️ <strong>Ação:</strong> Setar <code>temperature=0.0</code> e instruir citação estrita de fontes com verificação.
            </div>
        </div>

        <!-- Métrica 4 -->
        <div class="card" style="flex: 1; border-color: rgba(245, 158, 11, 0.35); background: linear-gradient(180deg, rgba(245, 158, 11, 0.08) 0%, rgba(15, 23, 42, 0.7) 100%);">
            <div class="card-title" style="color: #fbbf24;">
                <span class="badge badge-amber">Métrica 04</span> Answer Relevance
            </div>
            <div class="card-desc">A resposta atende diretamente e de forma completa ao que o usuário solicitou?</div>
            
            <div class="metric-pill">
                <span class="lbl">Meta Corporativa</span>
                <span class="val" style="color: #34d399;">&gt; 0.90</span>
            </div>

            <div class="code-box" style="font-size: 11px; margin: 8px 0;">
                # Avalia utilidade prática<br>
                Relevance = CosineSim(Emb(Resposta), Emb(Pergunta))
            </div>

            <div style="background: rgba(239, 68, 68, 0.06); border-radius: 8px; padding: 8px 10px; font-size: 11.5px; color: #fca5a5; margin-bottom: 8px;">
                ⚠️ <strong>Causa de Baixa Nota:</strong> O modelo respondeu algo verdadeiro, mas ignorou o pedido central.
            </div>

            <div style="margin-top: auto; font-size: 12px; color: #fcd34d; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.08);">
                🛠️ <strong>Ação:</strong> Estruturar o prompt com Few-Shot examples e saída em JSON Schema estrito.
            </div>
        </div>
    </div>
"""
)

# -------------------------------------------------------------
# FIGURA 13: MATRIZ ESTRATÉGICA: RAG VS FINE-TUNING
# -------------------------------------------------------------
TEMPLATES["0003_rag_vector_database/assets/13.png"] = make_page(
    pill="Decisão Arquitetural • Artigo 0003",
    title="RAG vs. Fine-Tuning: Critérios para a Escolha Estratégica",
    subtitle="Quando usar injeção contextual em tempo de execução vs. especialização paramétrica de pesos",
    fig_badge="Figura 13",
    content_html="""
    <div class="main-content">
        <!-- Lado RAG -->
        <div class="card" style="flex: 1; border-color: rgba(59, 130, 246, 0.35); background: rgba(59, 130, 246, 0.03);">
            <div class="card-title" style="color: #60a5fa;">
                <span class="badge badge-blue">RAG</span> Conhecimento Externo Dinâmico
            </div>
            <div class="card-desc">Adiciona fatos, documentos e dados mutáveis sem alterar os pesos do modelo.</div>

            <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 6px;">
                <div class="metric-pill">
                    <span class="lbl">Frequência de Atualização</span>
                    <span class="val" style="color: #34d399;">Tempo Real (Segundos)</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Rastreabilidade & Citação</span>
                    <span class="val" style="color: #34d399;">100% Exata com Link do Doc</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Custo de Implementação</span>
                    <span class="val" style="color: #34d399;">Baixo / Médio (Sem GPU de Treino)</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Risco de Alucinação</span>
                    <span class="val" style="color: #34d399;">Mínimo (Ancorado no contexto)</span>
                </div>
                <div style="margin-top: auto; padding: 12px; border-radius: 10px; background: rgba(59, 130, 246, 0.08); border: 1px dashed rgba(59, 130, 246, 0.25); font-size: 13px; color: #cbd5e1;">
                    🎯 <strong>Melhor Para:</strong> Manuais, políticas internas, catálogos em mudança constante, suporte técnico e conformidade jurídica.
                </div>
            </div>
        </div>

        <!-- Lado Fine-Tuning -->
        <div class="card" style="flex: 1; border-color: rgba(168, 85, 247, 0.35); background: rgba(168, 85, 247, 0.03);">
            <div class="card-title" style="color: #c084fc;">
                <span class="badge badge-purple">Fine-Tuning</span> Estilo, Tom & Sintaxe Estrita
            </div>
            <div class="card-desc">Ensina novas habilidades, formatos determinísticos e vocabulário especializado.</div>

            <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 6px;">
                <div class="metric-pill">
                    <span class="lbl">Frequência de Atualização</span>
                    <span class="val" style="color: #fcd34d;">Periódica (Re-treino semanal/mensal)</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Rastreabilidade & Citação</span>
                    <span class="val" style="color: #f87171;">Caixa-preta (Pesos neurais)</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Custo de Implementação</span>
                    <span class="val" style="color: #fcd34d;">Médio / Alto (Clusters de GPUs A100/H100)</span>
                </div>
                <div class="metric-pill">
                    <span class="lbl">Especialização em Formato</span>
                    <span class="val" style="color: #34d399;">Máxima (JSON estrito, SQL, Código)</span>
                </div>
                <div style="margin-top: auto; padding: 12px; border-radius: 10px; background: rgba(168, 85, 247, 0.08); border: 1px dashed rgba(168, 85, 247, 0.25); font-size: 13px; color: #cbd5e1;">
                    🚀 <strong>Melhor Para:</strong> Linguagens DSL próprias, saída JSON invariável, estilo de escrita específico e SLMs compactos (1B-7B) em borda.
                </div>
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
    print(f"Iniciando renderização de {len(TEMPLATES)} ativos visuais para Artigo 0003...")
    for rel_path, html in TEMPLATES.items():
        output_png = ROOT / rel_path
        render_html_to_png(html, output_png)
    print("Todas as 13 imagens do Artigo 0003 foram renderizadas com sucesso!")


if __name__ == "__main__":
    render_all()
