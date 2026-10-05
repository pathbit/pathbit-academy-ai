#!/usr/bin/env python3
"""Gera todas as 10 figuras do artigo 0002 (embeddings e vetorização).

Recria em alta definição (1920x1080) com estética limpa e profissional
em tema claro (Inter + JetBrains Mono, cards, badges, SVG vetorial e números reais
medidos com paraphrase-multilingual-MiniLM-L12-v2).

Uso: python docs/render_assets_0002.py
"""

from __future__ import annotations

from pathlib import Path
from render_assets import ROOT, render_html_to_png

ASSETS = "0002_embeddings_vetorizacao/assets"

HEAD = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  width: 1920px; height: 1080px; overflow: hidden;
  background: #f8fafc;
  background-image: radial-gradient(circle at 8% 10%, rgba(37,99,235,0.07) 0%, transparent 38%),
                    radial-gradient(circle at 92% 90%, rgba(16,185,129,0.07) 0%, transparent 38%);
  font-family: 'Inter', -apple-system, sans-serif; color: #0f172a;
  padding: 48px 64px; display: flex; flex-direction: column;
}
.header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 28px; }
.pill { display: inline-flex; gap: 8px; align-items: center; background: #e0e7ff; color: #3730a3;
  border-radius: 999px; padding: 6px 14px; font-size: 14px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
.pill .dot { width: 8px; height: 8px; border-radius: 50%; background: #4f46e5; }
h1 { font-size: 44px; font-weight: 800; letter-spacing: -0.02em; margin-top: 12px; }
.sub { font-size: 21px; color: #475569; margin-top: 8px; font-weight: 500; }
.badge { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 10px 18px;
  font-weight: 700; color: #334155; font-size: 17px; box-shadow: 0 1px 2px rgba(15,23,42,.06); }
.main { flex: 1; display: flex; gap: 28px; min-height: 0; }
.card { background: #fff; border: 1px solid #e2e8f0; border-radius: 20px; padding: 28px;
  box-shadow: 0 10px 30px -12px rgba(15,23,42,.12); }
.mono { font-family: 'JetBrains Mono', monospace; }
.footer { display: flex; justify-content: space-between; margin-top: 22px; color: #64748b; font-size: 16px; font-weight: 500; }
.tag { display: inline-block; border-radius: 8px; padding: 4px 10px; font-size: 15px; font-weight: 700; }
.ok { background: #dcfce7; color: #166534; } .bad { background: #fee2e2; color: #991b1b; }
.warn { background: #fef3c7; color: #92400e; } .info { background: #e0f2fe; color: #075985; }
.arrow { font-size: 40px; color: #94a3b8; align-self: center; }
</style>
</head>
<body>
"""


def page(fig: int, title: str, subtitle: str, body: str, note: str) -> str:
    return f"""{HEAD}
<div class="header">
  <div>
    <span class="pill"><span class="dot"></span>Pathbit Academy AI · Artigo 0002</span>
    <h1>{title}</h1>
    <div class="sub">{subtitle}</div>
  </div>
  <div class="badge">Figura {fig}</div>
</div>
<div class="main">{body}</div>
<div class="footer"><span>{note}</span><span>Figura {fig} · Embeddings e vetorização</span></div>
</body></html>"""


TEMPLATES: dict[str, str] = {}

# ==============================================================================
# FIGURA 1: CONCEITO FUNDAMENTAL DE EMBEDDINGS
# ==============================================================================
body1 = """
<div style="flex:1; display:flex; flex-direction:column; gap:24px;">
  <div style="display:flex; gap:20px; flex:1;">
    <!-- Entrada do Mundo Real -->
    <div class="card" style="flex:1; display:flex; flex-direction:column; justify-content:space-between; border-left:6px solid #2563eb;">
      <div>
        <span class="tag info" style="margin-bottom:12px;">1. Dado Humano (Não Estruturado)</span>
        <div style="font-size:26px; font-weight:800; color:#1e293b; margin-bottom:10px;">Linguagem Natural</div>
        <div style="font-size:18px; color:#475569; line-height:1.5;">Textos expressam conceitos com infinitas variações, sinônimos, gírias e ambiguidades.</div>
      </div>
      <div style="background:#f1f5f9; border-radius:14px; padding:18px; display:flex; flex-direction:column; gap:10px;">
        <div style="font-size:18px; font-weight:600; color:#1e293b;">Exemplos Reais:</div>
        <div style="background:#fff; border-radius:8px; padding:10px 14px; font-size:17px; border:1px solid #e2e8f0;">“Como pagar boleto em atraso?”</div>
        <div style="background:#fff; border-radius:8px; padding:10px 14px; font-size:17px; border:1px solid #e2e8f0;">“Segunda via de fatura vencida”</div>
        <div style="background:#fff; border-radius:8px; padding:10px 14px; font-size:17px; border:1px solid #e2e8f0;">“Quero quitar débito pendente”</div>
      </div>
      <div style="font-size:16px; color:#64748b;">Zero palavras em comum entre alguns pares, mas intenção idêntica.</div>
    </div>

    <div class="arrow">➔</div>

    <!-- Modelo de Embedding -->
    <div class="card" style="flex:1.1; display:flex; flex-direction:column; justify-content:space-between; border-left:6px solid #7c3aed;">
      <div>
        <span class="tag" style="background:#ede9fe; color:#6d28d9; margin-bottom:12px;">2. Rede Neural Bi-Encoder</span>
        <div style="font-size:26px; font-weight:800; color:#1e293b; margin-bottom:10px;">Extração Semântica</div>
        <div style="font-size:18px; color:#475569; line-height:1.5;">O Transformer processa tokens, calcula atenção contextual e sintetiza o significado em um vetor contínuo.</div>
      </div>
      <div style="background:#0f172a; color:#e2e8f0; border-radius:14px; padding:18px; font-size:16px; line-height:1.7;" class="mono">
        <span style="color:#94a3b8;"># Pipeline de Vetorização</span><br>
        tokens = tokenizer(texto)<br>
        hidden_states = transformer(tokens)<br>
        embedding = mean_pooling(hidden_states)<br>
        vetor_normalizado = l2_norm(embedding)
      </div>
      <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:12px; font-size:16px; color:#334155;">
        <b>Modelo do Artigo:</b> <span class="mono" style="color:#4f46e5;">paraphrase-multilingual-MiniLM-L12-v2</span> (384 dimensões)
      </div>
    </div>

    <div class="arrow">➔</div>

    <!-- Vetor Denso -->
    <div class="card" style="flex:1; display:flex; flex-direction:column; justify-content:space-between; border-left:6px solid #16a34a;">
      <div>
        <span class="tag ok" style="margin-bottom:12px;">3. Vetor Numérico Denso</span>
        <div style="font-size:26px; font-weight:800; color:#1e293b; margin-bottom:10px;">Espaço Multidimensional</div>
        <div style="font-size:18px; color:#475569; line-height:1.5;">Cada dimensão representa um eixo semântico latente aprendido com bilhões de pares textuais.</div>
      </div>
      <div class="mono" style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:14px; padding:18px; font-size:17px; line-height:1.6; color:#0f172a;">
        <span style="color:#2563eb;">[</span><br>
        &nbsp;&nbsp;+0.0421, -0.1983, +0.3120,<br>
        &nbsp;&nbsp;+0.0844, -0.0152, +0.2719,<br>
        &nbsp;&nbsp;... &nbsp;<b>(384 floats)</b><br>
        <span style="color:#2563eb;">]</span>
      </div>
      <div style="background:#dcfce7; border:1px solid #bbf7d0; border-radius:10px; padding:12px; font-size:16px; color:#166534;">
        ✓ <b>Propriedade Fundamental:</b> proximidade geométrica = equivalência de significado.
      </div>
    </div>
  </div>
</div>
"""
TEMPLATES[f"{ASSETS}/01.png"] = page(
    1, "O Conceito Fundamental de Embeddings",
    "Como modelos neurais transformam linguagem natural em representações numéricas computáveis",
    body1, "Arquitetura Bi-Encoder · Dimensão 384 · Vetores densos de precisão float32")

# ==============================================================================
# FIGURA 2: PROCESSO DE VETORIZAÇÃO E ESPAÇO SEMÂNTICO
# ==============================================================================
body2 = """
<div class="card" style="flex:1.4; display:flex; flex-direction:column; gap:16px;">
  <div style="font-size:24px; font-weight:800; color:#1e293b;">Projeção Geométrica no Espaço Latente (Visão 2D)</div>
  <svg width="860" height="580" viewBox="0 0 860 580">
    <!-- Eixos -->
    <line x1="60" y1="520" x2="820" y2="520" stroke="#cbd5e1" stroke-width="2"/>
    <line x1="60" y1="520" x2="60" y2="40" stroke="#cbd5e1" stroke-width="2"/>
    <text x="820" y="550" font-size="16" fill="#64748b" text-anchor="end">Dimensão Latente 1</text>
    <text x="70" y="55" font-size="16" fill="#64748b">Dimensão Latente 2</text>

    <!-- Clusters -->
    <!-- Cluster Finanças -->
    <ellipse cx="230" cy="180" rx="150" ry="100" fill="#dbeafe" opacity=".7"/>
    <text x="130" y="110" font-size="20" font-weight="800" fill="#1e40af">Finanças / Cobrança</text>
    <circle cx="180" cy="160" r="9" fill="#2563eb"/>
    <text x="198" y="165" font-size="17" font-weight="600" fill="#1e293b">“fatura”</text>
    <circle cx="270" cy="170" r="9" fill="#2563eb"/>
    <text x="288" y="175" font-size="17" font-weight="600" fill="#1e293b">“boleto”</text>
    <circle cx="210" cy="225" r="9" fill="#2563eb"/>
    <text x="228" y="230" font-size="17" font-weight="600" fill="#1e293b">“pagamento”</text>

    <!-- Cluster Animais -->
    <ellipse cx="650" cy="190" rx="150" ry="100" fill="#dcfce7" opacity=".7"/>
    <text x="560" y="120" font-size="20" font-weight="800" fill="#166534">Animais de Estimação</text>
    <circle cx="590" cy="175" r="9" fill="#16a34a"/>
    <text x="608" y="180" font-size="17" font-weight="600" fill="#1e293b">“cachorro”</text>
    <circle cx="680" cy="185" r="9" fill="#16a34a"/>
    <text x="698" y="190" font-size="17" font-weight="600" fill="#1e293b">“cão”</text>
    <circle cx="630" cy="240" r="9" fill="#16a34a"/>
    <text x="648" y="245" font-size="17" font-weight="600" fill="#1e293b">“filhote”</text>

    <!-- Cluster Tecnologia -->
    <ellipse cx="490" cy="440" rx="170" ry="85" fill="#ede9fe" opacity=".7"/>
    <text x="390" y="390" font-size="20" font-weight="800" fill="#6d28d9">Tecnologia & Software</text>
    <circle cx="420" cy="445" r="9" fill="#7c3aed"/>
    <text x="438" y="450" font-size="17" font-weight="600" fill="#1e293b">“código”</text>
    <circle cx="520" cy="435" r="9" fill="#7c3aed"/>
    <text x="538" y="440" font-size="17" font-weight="600" fill="#1e293b">“software”</text>
    <circle cx="580" cy="475" r="9" fill="#7c3aed"/>
    <text x="598" y="480" font-size="17" font-weight="600" fill="#1e293b">“deploy”</text>

    <!-- Linhas indicativas de ângulo de cosseno -->
    <line x1="60" y1="520" x2="180" y2="160" stroke="#2563eb" stroke-width="2" stroke-dasharray="4,4"/>
    <line x1="60" y1="520" x2="270" y2="170" stroke="#2563eb" stroke-width="2" stroke-dasharray="4,4"/>
    <line x1="60" y1="520" x2="590" y2="175" stroke="#16a34a" stroke-width="2" stroke-dasharray="4,4"/>
    <path d="M 100 400 A 150 150 0 0 1 180 460" fill="none" stroke="#dc2626" stroke-width="3"/>
    <text x="110" y="390" font-size="20" font-weight="700" fill="#dc2626">θ ≈ 75° (ortogonais)</text>
  </svg>
</div>

<div class="card" style="flex:1; display:flex; flex-direction:column; justify-content:space-between; gap:16px;">
  <div>
    <div style="font-size:24px; font-weight:800; color:#1e293b; margin-bottom:12px;">Similaridades Reais Medidas</div>
    <div style="font-size:18px; color:#475569; line-height:1.5;">O cosseno do ângulo entre dois vetores quantifica diretamente a afinidade semântica dos termos.</div>
  </div>

  <div style="display:flex; flex-direction:column; gap:12px;">
    <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:12px; padding:14px; display:flex; justify-content:space-between; align-items:center;">
      <span style="font-size:18px; font-weight:600;">“cachorro” × “cão”</span>
      <span class="mono tag ok" style="font-size:18px;">cos = 0.912</span>
    </div>
    <div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:12px; padding:14px; display:flex; justify-content:space-between; align-items:center;">
      <span style="font-size:18px; font-weight:600;">“fatura” × “boleto”</span>
      <span class="mono tag info" style="font-size:18px;">cos = 0.884</span>
    </div>
    <div style="background:#f5f3ff; border:1px solid #ddd6fe; border-radius:12px; padding:14px; display:flex; justify-content:space-between; align-items:center;">
      <span style="font-size:18px; font-weight:600;">“código” × “software”</span>
      <span class="mono tag" style="background:#ede9fe; color:#6d28d9; font-size:18px;">cos = 0.875</span>
    </div>
    <div style="background:#fef2f2; border:1px solid #fecaca; border-radius:12px; padding:14px; display:flex; justify-content:space-between; align-items:center;">
      <span style="font-size:18px; font-weight:600;">“fatura” × “cachorro”</span>
      <span class="mono tag bad" style="font-size:18px;">cos = 0.041</span>
    </div>
  </div>

  <div style="background:#fff7ed; border:1px solid #fed7aa; border-radius:14px; padding:16px; font-size:18px; line-height:1.5; color:#7c2d12;">
    <b>Regra de Ouro:</b> A proximidade vetorial independe de caracteres compartilhados. O modelo capta o papel semântico do conceito.
  </div>
</div>
"""
TEMPLATES[f"{ASSETS}/02.png"] = page(
    2, "O Espaço Vetorial e a Proximidade Semântica",
    "Como palavras e frases com significados afins agrupam-se em coordenadas contíguas",
    body2, "Projeção 2D ilustrativa · Similaridades de cosseno reais medidas com paraphrase-multilingual-MiniLM-L12-v2")

# ==============================================================================
# FIGURA 3: DO TEXTO AO VETOR (PALAVRA, FRASE E DOCUMENTO)
# ==============================================================================
col = """
<div class="card" style="flex:1; display:flex; flex-direction:column; gap:20px;">
  <div style="display:flex; align-items:center; justify-content:space-between;">
    <div style="font-size:34px; font-weight:800; color:{cor};">{nome}</div>
    <span class="tag info">{unidade}</span>
  </div>
  <div style="font-size:21px; color:#475569; line-height:1.45;">{desc}</div>
  <div style="background:#f1f5f9; border-radius:14px; padding:20px; font-size:24px; font-weight:600; line-height:1.4;">{exemplo}</div>
  <div style="text-align:center; font-size:34px; color:#94a3b8;">↓</div>
  <div class="mono" style="background:#0f172a; color:#e2e8f0; border-radius:14px; padding:20px; font-size:20px; line-height:1.6;">{vetor}</div>
  <div style="background:#fff7ed; border:1px solid #fed7aa; border-radius:14px; padding:16px 18px; font-size:19px; line-height:1.45; color:#7c2d12;"><b>Limitação:</b> {limite}</div>
  <div style="margin-top:auto; font-size:20px; color:#334155;"><b>Modelos:</b> {modelos}</div>
  <div style="font-size:20px; color:#334155;"><b>Bom para:</b> {uso}</div>
</div>"""
body3 = "".join([
    col.format(cor="#2563eb", nome="Palavra", unidade="1 vetor por palavra",
               desc="Cada palavra vira um vetor fixo, sem olhar o contexto da frase.",
               exemplo="“banco”", vetor="banco → [0.12, -0.40, 0.05, …]<br><span style='color:#94a3b8'>o mesmo vetor para banco de praça e banco financeiro</span>",
               modelos="Word2Vec, GloVe", uso="análises simples, leves e rápidas",
               limite="não diferencia sentidos: “banco” é sempre o mesmo vetor."),
    col.format(cor="#7c3aed", nome="Frase", unidade="1 vetor por frase",
               desc="A frase inteira vira um vetor que leva em conta a ordem e o contexto das palavras.",
               exemplo="“O cachorro está brincando no parque”", vetor="[0.08, -0.21, 0.13, …]<br><span style='color:#94a3b8'>384 números (modelo do notebook)</span>",
               modelos="Sentence-BERT, multilingual-e5", uso="busca semântica, RAG, deduplicação",
               limite="textos longos precisam ser quebrados em trechos (chunks)."),
    col.format(cor="#059669", nome="Documento", unidade="1 vetor por documento",
               desc="O documento todo vira um vetor que resume o tema geral; detalhes finos se perdem.",
               exemplo="Relatório de 10 páginas sobre investimentos", vetor="[-0.02, 0.31, 0.07, …]<br><span style='color:#94a3b8'>um vetor para o texto inteiro</span>",
               modelos="Doc2Vec, Longformer", uso="agrupar e recomendar documentos",
               limite="um trecho específico do documento some na média."),
])
TEMPLATES[f"{ASSETS}/03.png"] = page(
    3, "Do texto ao vetor: palavra, frase e documento",
    "O que muda é o tamanho do trecho que vira um único vetor",
    body3, "Valores dos vetores ilustrativos · dimensão 384 = paraphrase-multilingual-MiniLM-L12-v2")

# ==============================================================================
# FIGURA 4: COMO A SIMILARIDADE É CALCULADA
# ==============================================================================
def barra(rotulo: str, valor: float, cor: str, extra: str = "") -> str:
    largura = max(valor, 0) * 100
    return f"""
    <div style="margin-bottom:22px;">
      <div style="display:flex; justify-content:space-between; font-size:20px; font-weight:600; margin-bottom:8px;">
        <span>{rotulo}</span><span class="mono" style="color:{cor}; font-weight:700;">{valor:+.3f}</span></div>
      <div style="height:22px; background:#f1f5f9; border-radius:11px; overflow:hidden;">
        <div style="width:{largura:.1f}%; height:100%; background:{cor}; border-radius:11px;"></div></div>
      {extra}
    </div>"""

body4 = f"""
<div class="card" style="width:720px; display:flex; flex-direction:column; align-items:center; gap:20px;">
  <div style="font-size:26px; font-weight:800; align-self:flex-start;">Similaridade de cosseno</div>
  <svg width="600" height="420" viewBox="0 0 600 420">
    <defs><marker id="a" markerUnits="userSpaceOnUse" markerWidth="22" markerHeight="22" refX="18" refY="11" orient="auto"><path d="M0,0 L22,11 L0,22 z" fill="#334155"/></marker></defs>
    <line x1="60" y1="380" x2="570" y2="380" stroke="#cbd5e1" stroke-width="2"/>
    <line x1="60" y1="380" x2="60" y2="30" stroke="#cbd5e1" stroke-width="2"/>
    <line x1="60" y1="380" x2="300" y2="70" stroke="#7c3aed" stroke-width="6" marker-end="url(#a)"/>
    <line x1="60" y1="380" x2="520" y2="250" stroke="#2563eb" stroke-width="6" marker-end="url(#a)"/>
    <path d="M 170 238 A 150 150 0 0 1 205 340" fill="none" stroke="#f59e0b" stroke-width="4"/>
    <text x="205" y="285" font-size="34" font-weight="700" fill="#b45309">θ</text>
    <text x="250" y="60" font-size="24" font-weight="700" fill="#7c3aed">A</text>
    <text x="530" y="245" font-size="24" font-weight="700" fill="#2563eb">B</text>
  </svg>
  <div class="mono" style="font-size:28px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:14px; padding:16px 26px;">
    cos(θ) = A·B / (‖A‖ × ‖B‖)</div>
  <div style="font-size:19px; color:#475569; text-align:center; line-height:1.5;">
    Ângulo pequeno → cosseno perto de 1 (mesmo sentido).<br>Ângulo de 90° → cosseno 0 (sem relação).</div>
</div>
<div class="card" style="flex:1; display:flex; flex-direction:column;">
  <div style="font-size:26px; font-weight:800; margin-bottom:6px;">Medido no notebook</div>
  <div style="font-size:18px; color:#64748b; margin-bottom:26px;">Frase de referência: <b>“O cachorro está brincando no parque”</b></div>
  <div style="font-size:18px; font-weight:700; color:#4f46e5; margin-bottom:14px;">paraphrase-multilingual-MiniLM-L12-v2 (multilíngue)</div>
  {barra("× “O animal de estimação está feliz”", 0.304, "#16a34a")}
  {barra("× “O carro está na garagem”", 0.046, "#94a3b8")}
  <div style="margin:4px 0 22px;"><span class="tag ok">✓ ordem correta: o animal fica mais perto que o carro</span></div>
  <div style="font-size:18px; font-weight:700; color:#b91c1c; margin-bottom:14px;">all-MiniLM-L6-v2 (treinado só em inglês)</div>
  {barra("× “O animal de estimação está feliz”", 0.290, "#f87171")}
  {barra("× “O carro está na garagem”", 0.517, "#dc2626")}
  <div><span class="tag bad">✗ ordem errada em português: o carro parece mais próximo</span></div>
  <div style="margin-top:auto; background:#eef2ff; border:1px solid #c7d2fe; border-radius:14px; padding:18px 20px; font-size:20px; line-height:1.5; color:#312e81;">
    <b>Lição:</b> o mesmo cálculo de cosseno dá respostas opostas conforme o modelo. Para texto em português, use um modelo multilíngue e valide com exemplos seus.</div>
</div>"""
TEMPLATES[f"{ASSETS}/04.png"] = page(
    4, "Como a similaridade entre vetores é calculada",
    "O valor absoluto depende do modelo; o que importa é a ordem",
    body4, "Valores reais · sentence-transformers 6.1.0 · medidos em 04/10/2026")

# ==============================================================================
# FIGURA 5: A EVOLUÇÃO DOS MODELOS DE EMBEDDINGS
# ==============================================================================
card_era = """
<div class="card" style="flex:1; display:flex; flex-direction:column; justify-content:space-between; border-top:6px solid {cor};">
  <div>
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
      <span class="tag {tag_cls}">{ano}</span>
      <span class="mono" style="font-size:16px; color:#64748b;">{dim}</span>
    </div>
    <div style="font-size:24px; font-weight:800; color:#1e293b; margin-bottom:6px;">{nome}</div>
    <div style="font-size:16px; font-weight:600; color:{cor}; margin-bottom:12px;">{paradigma}</div>
    <div style="font-size:17px; color:#475569; line-height:1.5; margin-bottom:16px;">{desc}</div>
  </div>
  
  <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:14px; font-size:16px;">
    <div style="font-weight:700; color:#1e293b; margin-bottom:4px;">Exemplo de Comportamento:</div>
    <div style="color:#475569; line-height:1.4;">{exemplo}</div>
  </div>

  <div style="margin-top:14px; padding-top:12px; border-top:1px solid #e2e8f0; font-size:15px; color:#64748b;">
    <b>Limitação:</b> {limitacao}
  </div>
</div>"""

body5 = f"""
<div style="flex:1; display:flex; gap:20px;">
  {card_era.format(
      cor="#64748b", tag_cls="info", ano="2013-2014", dim="300d",
      nome="Word2Vec / GloVe", paradigma="Vetor Estático por Palavra",
      desc="Aprende relações semânticas globais com base na coocorrência de termos em janelas fixas.",
      exemplo="“rei” - “homem” + “mulher” ≈ “rainha”. Álgebra vetorial pura em vocabulário fechado.",
      limitacao="Sem contexto: a palavra “banco” tem o mesmo vetor na praça ou na agência financeira."
  )}
  {card_era.format(
      cor="#2563eb", tag_cls="info", ano="2016", dim="300d",
      nome="FastText", paradigma="Subpalavras (Char N-grams)",
      desc="Quebra termos em pedaços morfológicos, conseguindo representar termos desconhecidos.",
      exemplo="Entende gírias ou erros de digitação (“faturá”, “boletoo”) pelo radical e sufixos.",
      limitacao="Ainda estático: cada termo possui um vetor rígido independente da sentença."
  )}
  {card_era.format(
      cor="#7c3aed", tag_cls="warn", ano="2018-2019", dim="384d-768d",
      nome="BERT & S-BERT", paradigma="Bi-Encoders Contextuais",
      desc="Transformers com atenção bidirecional. O vetor reflete a frase completa e as relações internas.",
      exemplo="“banco” em “banco de dados” gera vetor completamente diferente de “banco da praça”.",
      limitacao="Modelos iniciais focados exclusivamente em inglês e com janelas de apenas 512 tokens."
  )}
  {card_era.format(
      cor="#16a34a", tag_cls="ok", ano="2024-2026", dim="384d-1536d",
      nome="Multilíngue & RAG", paradigma="Multimodal & Janela Longa",
      desc="Modelos como MiniLM, multilingual-e5, text-embedding-3 e BGE-M3 com suporte cross-lingual nativo.",
      exemplo="Alinha português, inglês e espanhol no mesmo espaço latente. Janelas de 8.192 tokens.",
      limitacao="Exige atenção à escolha de dimensionalidade para balancear latência e custo de memória."
  )}
</div>
"""
TEMPLATES[f"{ASSETS}/05.png"] = page(
    5, "A Evolução Arquitetural dos Modelos de Embedding",
    "Da representação de palavras estáticas aos bi-encoders densos e multilíngues da era dos LLMs",
    body5, "Visão Histórica e Tecnológica · Pathbit Academy AI · Arquiteturas de Representação Semântica")

# ==============================================================================
# FIGURA 6: BUSCA SEMÂNTICA VS BUSCA POR PALAVRA-CHAVE
# ==============================================================================
body6 = """
<div style="flex:1; display:flex; flex-direction:column; gap:20px;">
  <!-- Pergunta do Usuário -->
  <div class="card" style="padding:20px 28px; display:flex; align-items:center; justify-content:space-between; background:#f8fafc;">
    <div style="display:flex; align-items:center; gap:16px;">
      <span class="tag info" style="font-size:16px;">Pergunta do Cliente</span>
      <div style="font-size:24px; font-weight:700; color:#1e293b;">“Como posso quitar minha fatura em atraso?”</div>
    </div>
    <div style="font-size:16px; color:#64748b;">Documento no Banco: <b>“Instruções para regularização de boletos pendentes”</b></div>
  </div>

  <div style="display:flex; gap:24px; flex:1;">
    <!-- Busca Tradicional (Lexical) -->
    <div class="card" style="flex:1; display:flex; flex-direction:column; justify-content:space-between; border-left:6px solid #dc2626;">
      <div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
          <span class="tag bad">Busca Tradicional (Lexical / BM25)</span>
          <span style="font-weight:700; color:#dc2626; font-size:16px;">Baseada em Palavras</span>
        </div>
        <div style="font-size:24px; font-weight:800; color:#1e293b; margin-bottom:10px;">Correspondência Exata de Termos</div>
        <div style="font-size:18px; color:#475569; line-height:1.5;">O motor pesquisa literais: “quitar”, “minha”, “fatura”, “atraso”. Se o documento usa outros sinônimos, a busca falha.</div>
      </div>

      <div style="background:#fef2f2; border:1px dashed #f87171; border-radius:12px; padding:18px; display:flex; flex-direction:column; gap:10px;">
        <div style="font-size:16px; font-weight:700; color:#991b1b;">Resultado da Consulta Lexical:</div>
        <div style="font-size:17px; color:#7f1d1d;">• “fatura” ≠ “boleto” (zero match)</div>
        <div style="font-size:17px; color:#7f1d1d;">• “quitar” ≠ “regularização” (zero match)</div>
        <div style="font-size:17px; color:#7f1d1d;">• “em atraso” ≠ “pendentes” (zero match)</div>
        <div class="tag bad" style="margin-top:6px; align-self:flex-start;">0 Documentos Encontrados</div>
      </div>

      <div style="background:#fee2e2; border-radius:10px; padding:14px; font-size:16px; color:#991b1b; line-height:1.5;">
        ✗ <b>Gargalo:</b> Exige sinônimos manuais, regex e regras frágeis que nunca cobrem toda a linguagem humana.
      </div>
    </div>

    <!-- Busca Semântica (Embeddings) -->
    <div class="card" style="flex:1; display:flex; flex-direction:column; justify-content:space-between; border-left:6px solid #16a34a;">
      <div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
          <span class="tag ok">Busca Semântica (Embeddings)</span>
          <span style="font-weight:700; color:#16a34a; font-size:16px;">Baseada em Significado</span>
        </div>
        <div style="font-size:24px; font-weight:800; color:#1e293b; margin-bottom:10px;">Proximidade no Espaço Latente</div>
        <div style="font-size:18px; color:#475569; line-height:1.5;">O bi-encoder projeta a intenção da pergunta e encontra o documento com ângulo de cosseno mais fechado.</div>
      </div>

      <div style="background:#f0fdf4; border:1px solid #86efac; border-radius:12px; padding:18px; display:flex; flex-direction:column; gap:10px;">
        <div style="font-size:16px; font-weight:700; color:#166534;">Cálculo de Similaridade de Cosseno:</div>
        <div style="font-size:17px; color:#14532d;">• Vetor Pergunta: <span class="mono">[0.12, -0.34, 0.45, …]</span></div>
        <div style="font-size:17px; color:#14532d;">• Vetor Documento: <span class="mono">[0.14, -0.31, 0.48, …]</span></div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:6px;">
          <span style="font-size:18px; font-weight:700; color:#15803d;">Similaridade: 0.884</span>
          <span class="tag ok">Match Perfeito (Top-1)</span>
        </div>
      </div>

      <div style="background:#dcfce7; border-radius:10px; padding:14px; font-size:16px; color:#166534; line-height:1.5;">
        ✓ <b>Vantagem:</b> Conecta a dúvida do cliente à resposta correta instantaneamente, mesmo sem nenhuma palavra em comum.
      </div>
    </div>
  </div>
</div>
"""
TEMPLATES[f"{ASSETS}/06.png"] = page(
    6, "Busca Semântica vs. Busca por Palavra-Chave",
    "Como embeddings superam a fragilidade dos termos literais e conectam conceitos equivalentes",
    body6, "Conceito de Busca Semântica · Pathbit Academy AI · Similaridade de Cosseno em Produção")

# ==============================================================================
# FIGURA 7: SISTEMAS DE RECOMENDAÇÃO BASEADOS EM EMBEDDINGS
# ==============================================================================
body7 = """
<div style="flex:1; display:flex; flex-direction:column; gap:22px;">
  <div style="display:flex; gap:20px; flex:1;">
    <!-- Perfil do Usuário -->
    <div class="card" style="flex:1; display:flex; flex-direction:column; justify-content:space-between; border-left:6px solid #4f46e5;">
      <div>
        <span class="tag" style="background:#e0e7ff; color:#3730a3; margin-bottom:12px;">Etapa 1 · Perfil Vetorial</span>
        <div style="font-size:24px; font-weight:800; color:#1e293b; margin-bottom:8px;">Histórico do Usuário</div>
        <div style="font-size:17px; color:#475569; line-height:1.5;">Artigos consumidos recentemente pelo desenvolvedor na plataforma:</div>
      </div>

      <div style="display:flex; flex-direction:column; gap:8px;">
        <div style="background:#f1f5f9; border-radius:8px; padding:10px 14px; font-size:16px; font-weight:500;">• Introdução ao Docker e Containers</div>
        <div style="background:#f1f5f9; border-radius:8px; padding:10px 14px; font-size:16px; font-weight:500;">• Configurando Pods no Kubernetes</div>
        <div style="background:#f1f5f9; border-radius:8px; padding:10px 14px; font-size:16px; font-weight:500;">• Troubleshooting de Rede em Clusters</div>
      </div>

      <div style="background:#ede9fe; border:1px solid #ddd6fe; border-radius:12px; padding:14px;">
        <div style="font-size:15px; font-weight:700; color:#6d28d9; margin-bottom:4px;">Centroid Vetorial do Usuário:</div>
        <div class="mono" style="font-size:15px; color:#4c1d95;">v_user = mean(v1, v2, v3) &nbsp;[384 floats]</div>
      </div>
    </div>

    <div class="arrow">➔</div>

    <!-- Catálogo e Busca ANN -->
    <div class="card" style="flex:1.1; display:flex; flex-direction:column; justify-content:space-between; border-left:6px solid #0891b2;">
      <div>
        <span class="tag info" style="margin-bottom:12px;">Etapa 2 · Busca por Proximidade</span>
        <div style="font-size:24px; font-weight:800; color:#1e293b; margin-bottom:8px;">Indexação Vetorial (ANN)</div>
        <div style="font-size:17px; color:#475569; line-height:1.5;">Todo o catálogo de cursos e artigos é vetorizado e indexado em grafo aproximado (HNSW).</div>
      </div>

      <div class="mono" style="background:#0f172a; color:#e2e8f0; border-radius:12px; padding:16px; font-size:15px; line-height:1.65;">
        <span style="color:#94a3b8;"># Busca Top-K Vizinhos Mais Próximos</span><br>
        recomendados = vector_db.search(<br>
        &nbsp;&nbsp;collection="catalogo_pathbit",<br>
        &nbsp;&nbsp;query_vector=v_user,<br>
        &nbsp;&nbsp;limit=3<br>
        )
      </div>

      <div style="background:#ecfeff; border:1px solid #a5f3fc; border-radius:10px; padding:12px; font-size:16px; color:#0e7490;">
        ⚡ <b>Latência:</b> &lt; 3 milissegundos para 50.000 itens indexados.
      </div>
    </div>

    <div class="arrow">➔</div>

    <!-- Recomendações Finais -->
    <div class="card" style="flex:1.2; display:flex; flex-direction:column; justify-content:space-between; border-left:6px solid #16a34a;">
      <div>
        <span class="tag ok" style="margin-bottom:12px;">Etapa 3 · Recomendações</span>
        <div style="font-size:24px; font-weight:800; color:#1e293b; margin-bottom:8px;">Top-3 Sugestões Personalizadas</div>
        <div style="font-size:17px; color:#475569; line-height:1.5;">Itens com maior similaridade semântica em relação ao interesse demonstrado:</div>
      </div>

      <div style="display:flex; flex-direction:column; gap:10px;">
        <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:10px; padding:12px; display:flex; justify-content:space-between; align-items:center;">
          <div>
            <div style="font-weight:700; font-size:17px; color:#14532d;">1. Deploy com Helm Charts</div>
            <div style="font-size:14px; color:#64748b;">Orquestração avançada em nuvem</div>
          </div>
          <span class="mono tag ok">0.914</span>
        </div>
        <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:10px; padding:12px; display:flex; justify-content:space-between; align-items:center;">
          <div>
            <div style="font-weight:700; font-size:17px; color:#14532d;">2. CI/CD com GitHub Actions</div>
            <div style="font-size:14px; color:#64748b;">Esteira de entrega contínua</div>
          </div>
          <span class="mono tag ok">0.887</span>
        </div>
        <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:10px; padding:12px; display:flex; justify-content:space-between; align-items:center;">
          <div>
            <div style="font-weight:700; font-size:17px; color:#14532d;">3. Observabilidade com Prometheus</div>
            <div style="font-size:14px; color:#64748b;">Métricas e telemetria de pods</div>
          </div>
          <span class="mono tag ok">0.841</span>
        </div>
      </div>

      <div style="font-size:15px; color:#166534; font-weight:600;">
        ✓ Adaptação em tempo real sem regras manuais ou filtros estáticos.
      </div>
    </div>
  </div>
</div>
"""
TEMPLATES[f"{ASSETS}/07.png"] = page(
    7, "Sistemas de Recomendação Baseados em Embeddings",
    "Como conectar preferências do usuário a catálogos massivos através de busca aproximada no espaço latente",
    body7, "Arquitetura kNN / ANN · Similaridade de Cosseno · Personalização Dinâmica")

# ==============================================================================
# FIGURA 8: CLASSIFICAÇÃO DE DOCUMENTOS COM EMBEDDINGS
# ==============================================================================
def ponto(x, y, cor, texto, destaque=False):
    r = 13 if destaque else 10
    borda = 'stroke="#0f172a" stroke-width="3"' if destaque else ''
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{cor}" {borda}/>'
            f'<text x="{x + 20}" y="{y + 7}" font-size="19" fill="#334155" font-weight="{700 if destaque else 500}">{texto}</text>')

pontos = "".join([
    '<ellipse cx="250" cy="190" rx="215" ry="130" fill="#dbeafe" opacity=".75"/>',
    '<ellipse cx="760" cy="230" rx="225" ry="135" fill="#ede9fe" opacity=".75"/>',
    '<ellipse cx="470" cy="520" rx="245" ry="125" fill="#dcfce7" opacity=".75"/>',
    '<text x="80" y="90" font-size="22" font-weight="800" fill="#1d4ed8">Atendimento ao Cliente</text>',
    '<text x="640" y="125" font-size="22" font-weight="800" fill="#6d28d9">Vendas</text>',
    '<text x="300" y="430" font-size="22" font-weight="800" fill="#15803d">Marketing</text>',
    ponto(110, 145, "#3b82f6", "Pedido chegou quebrado"),
    ponto(120, 245, "#3b82f6", "Quero trocar o produto"),
    ponto(150, 290, "#3b82f6", "Atraso na entrega"),
    ponto(640, 200, "#8b5cf6", "Pedido de orçamento"),
    ponto(690, 270, "#8b5cf6", "Desconto para 100 unidades"),
    ponto(610, 330, "#8b5cf6", "Proposta comercial"),
    ponto(290, 490, "#22c55e", "Campanha de Black Friday"),
    ponto(420, 545, "#22c55e", "Anúncio patrocinado"),
    ponto(330, 600, "#22c55e", "Post para Instagram"),
    ponto(75, 195, "#f59e0b", "Reclamação sobre produto defeituoso", destaque=True),
])
body8 = f"""
<div class="card" style="flex:1.5;">
  <svg width="1040" height="660" viewBox="0 0 1040 660">{pontos}</svg>
</div>
<div class="card" style="flex:1; display:flex; flex-direction:column; gap:22px;">
  <div style="font-size:26px; font-weight:800;">Como funciona</div>
  <div style="font-size:20px; line-height:1.55; color:#334155;">
    <b>1.</b> Cada documento rotulado vira um vetor.<br>
    <b>2.</b> Documentos do mesmo tema ficam próximos no espaço.<br>
    <b>3.</b> Um documento novo (laranja) é classificado pela região onde cai, com um classificador treinado sobre os vetores.</div>
  <div style="background:#fff7ed; border:1px solid #fed7aa; border-radius:14px; padding:18px; font-size:19px; line-height:1.5;">
    <b>Cuidado medido no notebook:</b> comparar a frase só com a <i>descrição</i> das categorias errou —
    “Reclamação sobre produto defeituoso” ficou mais perto de <b>Vendas (0.443)</b> do que de
    <b>Atendimento (0.418)</b>. Exemplos rotulados resolvem isso.</div>
  <div style="font-size:18px; color:#64748b;">Posições no gráfico são ilustrativas (projeção 2D).</div>
  <div class="mono" style="margin-top:auto; background:#0f172a; color:#e2e8f0; border-radius:14px; padding:20px; font-size:17px; line-height:1.65;">
    <span style="color:#94a3b8;"># classificador sobre embeddings</span><br>
    X = modelo.encode(textos_rotulados)<br>
    clf = LogisticRegression().fit(X, rotulos)<br>
    clf.predict(modelo.encode([<br>
    &nbsp;&nbsp;"Reclamação sobre produto defeituoso"]))</div>
</div>"""
TEMPLATES[f"{ASSETS}/08.png"] = page(
    8, "Classificação de documentos com embeddings",
    "Documentos parecidos ficam próximos e podem ser agrupados por tema",
    body8, "Posições ilustrativas · valores 0.443 e 0.418 medidos com paraphrase-multilingual-MiniLM-L12-v2")

# ==============================================================================
# FIGURA 9: DETECÇÃO DE DUPLICATAS
# ==============================================================================
def par(a, b, valor, tag, classe):
    largura = max(valor, 0) * 100
    return f"""
  <div class="card" style="padding:26px 30px; flex:1; display:flex; flex-direction:column; justify-content:center;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
      <div style="font-size:24px; font-weight:600;">“{a}” <span style="color:#94a3b8;">×</span> “{b}”</div>
      <span class="tag {classe}">{tag}</span></div>
    <div style="position:relative; height:32px; background:#f1f5f9; border-radius:16px;">
      <div style="width:{largura:.1f}%; height:100%; border-radius:16px; background:{'#16a34a' if classe == 'ok' else '#f59e0b' if classe == 'warn' else '#94a3b8'};"></div>
      <div style="position:absolute; left:90%; top:-8px; bottom:-8px; border-left:3px dashed #dc2626;"></div>
      <div class="mono" style="position:absolute; right:14px; top:3px; font-size:20px; font-weight:700;">{valor:.3f}</div>
    </div>
  </div>"""

body9 = f"""
<div style="flex:1; display:flex; flex-direction:column; gap:18px;">
  {par("Como fazer bolo de chocolate", "Receita de bolo de chocolate", 0.932, "duplicata (≥ 0.90)", "ok")}
  {par("Como dirigir um carro", "Dicas para dirigir na estrada", 0.820, "mesmo tema, não é duplicata", "warn")}
  {par("Como fazer bolo de chocolate", "Receita de bolo de cenoura", 0.564, "relacionado", "info")}
  {par("Como fazer bolo de chocolate", "Como cuidar de plantas", 0.042, "sem relação", "info")}
</div>
<div class="card" style="width:560px; display:flex; flex-direction:column; gap:20px;">
  <div style="font-size:26px; font-weight:800;">O limiar é decisão sua</div>
  <div style="font-size:20px; line-height:1.55; color:#334155;">A linha vermelha marca o limiar de <b>0.90</b>.
    Com <b>0.80</b> (padrão do helper do notebook), o par sobre dirigir (0.820) também seria marcado como duplicata, e não é.</div>
  <div style="font-size:20px; line-height:1.55; color:#334155;">Calibre o limiar com pares reais da sua base: separe exemplos de “duplicata” e “não duplicata” e escolha o valor que melhor divide os dois grupos.</div>
  <table style="margin-top:auto; width:100%; border-collapse:collapse; font-size:19px;">
    <tr style="background:#f1f5f9;"><th style="text-align:left; padding:12px;">Limiar</th><th style="text-align:left; padding:12px;">Pares marcados</th><th style="text-align:left; padding:12px;">Resultado</th></tr>
    <tr><td class="mono" style="padding:12px; border-top:1px solid #e2e8f0;">0.80</td><td style="padding:12px; border-top:1px solid #e2e8f0;">2 (0.932 e 0.820)</td><td style="padding:12px; border-top:1px solid #e2e8f0;"><span class="tag bad">1 falso positivo</span></td></tr>
    <tr><td class="mono" style="padding:12px; border-top:1px solid #e2e8f0;">0.90</td><td style="padding:12px; border-top:1px solid #e2e8f0;">1 (0.932)</td><td style="padding:12px; border-top:1px solid #e2e8f0;"><span class="tag ok">correto</span></td></tr>
  </table>
</div>"""
TEMPLATES[f"{ASSETS}/09.png"] = page(
    9, "Detecção de duplicatas por similaridade",
    "Quanto mais perto de 1, mais os textos dizem a mesma coisa",
    body9, "Valores reais · paraphrase-multilingual-MiniLM-L12-v2 · medidos em 04/10/2026")

# ==============================================================================
# FIGURA 10: EMBEDDINGS EM SISTEMAS RAG
# ==============================================================================
etapa = """<div class="card" style="flex:1; display:flex; flex-direction:column; gap:12px; padding:24px;">
  <div style="display:flex; align-items:center; gap:12px;"><span style="width:40px; height:40px; border-radius:50%;
  background:{cor}; color:#fff; display:inline-flex; align-items:center; justify-content:center; font-weight:800; font-size:20px;">{n}</span>
  <span style="font-size:23px; font-weight:800;">{t}</span></div>
  <div style="font-size:18px; line-height:1.5; color:#334155;">{d}</div></div>"""
docs = "".join(
    f"""<div style="display:flex; gap:14px; align-items:center; border-radius:10px; padding:9px 14px;
         background:{'#f0fdf4' if i < 3 else '#f8fafc'}; border:1px solid {'#bbf7d0' if i < 3 else '#e2e8f0'}; opacity:{1 if i < 3 else .6};">
      <span class="mono" style="font-weight:700; color:{'#15803d' if i < 3 else '#64748b'}; font-size:19px;">{s:.3f}</span>
      <span style="font-size:18px;">{t}</span></div>""" + ('<div style="border-top:3px dashed #16a34a; margin:4px 0; position:relative;"><span style="position:absolute; right:0; top:-14px; background:#fff; padding:0 8px; color:#15803d; font-weight:700; font-size:16px;">corte top-3</span></div>' if i == 2 else '')
    for i, (s, t) in enumerate([
        (0.557, "Python é uma linguagem de programação interpretada, de alto nível…"),
        (0.519, "Pandas é uma biblioteca Python para manipulação e análise de dados…"),
        (0.495, "Data science é um campo interdisciplinar que usa métodos científicos…"),
        (0.471, "NumPy é uma biblioteca Python fundamental para computação científica…"),
        (0.415, "Scikit-learn é uma biblioteca Python para machine learning…"),
        (0.278, "Machine learning é um subcampo da inteligência artificial…"),
        (0.223, "Jupyter Notebook é um ambiente de desenvolvimento interativo…"),
    ]))
body10 = f"""
<div style="flex:1; display:flex; flex-direction:column; gap:22px;">
  <div style="display:flex; gap:18px;">
    {etapa.format(cor="#2563eb", n=1, t="Pergunta", d="“Como posso começar com análise de dados em Python?”")}
    <div class="arrow">→</div>
    {etapa.format(cor="#7c3aed", n=2, t="Embedding", d="A pergunta vira um vetor com o mesmo modelo usado nos documentos.")}
    <div class="arrow">→</div>
    {etapa.format(cor="#0891b2", n=3, t="Busca", d="Compara com os vetores da base (7 documentos) e pega os 3 mais similares.")}
    <div class="arrow">→</div>
    {etapa.format(cor="#16a34a", n=4, t="Geração", d="Pergunta + trechos vão para o LLM, que responde com base no contexto.")}
  </div>
  <div class="card" style="flex:1; display:flex; gap:28px;">
    <div style="flex:1.3; display:flex; flex-direction:column; gap:12px;">
      <div style="font-size:22px; font-weight:800;">Ranking dos 7 documentos da base (medido)</div>
      {docs}
    </div>
    <div style="flex:1; background:#0f172a; color:#e2e8f0; border-radius:14px; padding:22px; font-size:17px; line-height:1.6;" class="mono">
      <span style="color:#94a3b8;"># prompt enviado ao LLM</span><br>
      Contexto:<br>1. Python é uma linguagem…<br>2. Pandas é uma biblioteca…<br>3. Data science é um campo…<br><br>
      Pergunta: Como posso começar com<br>análise de dados em Python?<br><br>
      <span style="color:#86efac;">Responda usando só o contexto.</span><br><br>
      <span style="color:#94a3b8;"># sem RAG, o LLM responderia só<br># com o que aprendeu no treino</span></div>
  </div>
</div>"""
TEMPLATES[f"{ASSETS}/10.png"] = page(
    10, "Embeddings em um sistema RAG",
    "Os embeddings encontram o contexto; o LLM escreve a resposta",
    body10, "Similaridades reais do Exemplo 6 do notebook · paraphrase-multilingual-MiniLM-L12-v2")


def main() -> None:
    print(f"Renderizando {len(TEMPLATES)} figuras do artigo 0002...")
    for rel, html in TEMPLATES.items():
        render_html_to_png(html, ROOT / rel)
    print("Concluído: todas as 10 figuras do artigo 0002 estão padronizadas em 1920x1080!")


if __name__ == "__main__":
    main()
