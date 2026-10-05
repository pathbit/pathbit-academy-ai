#!/usr/bin/env python3
"""Recria as figuras 03, 04, 08, 09 e 10 do artigo 0002 (embeddings).

As originais tinham erros de digitação ("EMBEDINGS", "Clustring", "SIMILIARITY",
"Uncoser") e três delas não correspondiam à seção onde estavam no artigo.

Todos os números exibidos foram medidos com o modelo usado no notebook
(paraphrase-multilingual-MiniLM-L12-v2, sentence-transformers 6.1.0) em
04/10/2026; os valores ilustrativos estão marcados como tal na própria figura.

Tema claro para combinar com as demais figuras do artigo 0002.
Uso:  python docs/render_assets_0002.py
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');
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

# ---------------------------------------------------------------- Figura 3
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

# ---------------------------------------------------------------- Figura 4
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

# ---------------------------------------------------------------- Figura 8
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

# ---------------------------------------------------------------- Figura 9
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

# ---------------------------------------------------------------- Figura 10
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
    print("Concluído.")


if __name__ == "__main__":
    main()
