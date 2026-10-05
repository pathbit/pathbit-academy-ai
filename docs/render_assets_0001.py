#!/usr/bin/env python3
"""Gera a figura conceitual de arquitetura para o artigo 0001 (LLM vs LRM).

Renderiza em 1920x1080 com tema dark glassmorphism e tipografia premium.
Uso: python docs/render_assets_0001.py
"""

from __future__ import annotations

from pathlib import Path
from render_assets import ROOT, render_html_to_png

ASSETS = "0001_llm_x_lrm/assets"

HTML_0001 = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  width: 1920px; height: 1080px; overflow: hidden;
  background: #070a13;
  background-image: 
    radial-gradient(circle at 10% 15%, rgba(37, 99, 235, 0.18) 0%, transparent 42%),
    radial-gradient(circle at 90% 85%, rgba(139, 92, 246, 0.16) 0%, transparent 42%),
    radial-gradient(circle at 50% 50%, rgba(16, 185, 129, 0.08) 0%, transparent 55%);
  font-family: 'Inter', -apple-system, sans-serif; color: #f1f5f9;
  padding: 44px 56px; display: flex; flex-direction: column; justify-content: space-between;
}
.header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
.brand-pill {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(37, 99, 235, 0.15); border: 1px solid rgba(59, 130, 246, 0.35);
  padding: 6px 14px; border-radius: 9999px; font-size: 13px; font-weight: 700;
  letter-spacing: 0.08em; color: #60a5fa; text-transform: uppercase;
}
.brand-pill .dot { width: 8px; height: 8px; border-radius: 50%; background: #3b82f6; box-shadow: 0 0 10px #3b82f6; }
.title { font-size: 38px; font-weight: 800; letter-spacing: -0.02em; color: #ffffff; line-height: 1.15; margin-top: 8px; }
.subtitle { font-size: 18px; color: #94a3b8; font-weight: 500; margin-top: 4px; }
.figure-badge {
  background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.12);
  padding: 8px 18px; border-radius: 12px; font-size: 15px; font-weight: 700; color: #cbd5e1;
}
.main { flex: 1; display: flex; flex-direction: column; gap: 24px; min-height: 0; }
.card {
  background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px; padding: 28px; backdrop-filter: blur(12px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.28); display: flex; flex-direction: column;
}
.mono { font-family: 'JetBrains Mono', monospace; }
.badge {
  display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; border-radius: 6px;
  font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;
}
.badge-blue { background: rgba(37, 99, 235, 0.2); color: #60a5fa; border: 1px solid rgba(37, 99, 235, 0.4); }
.badge-purple { background: rgba(139, 92, 246, 0.2); color: #c084fc; border: 1px solid rgba(139, 92, 246, 0.4); }
.badge-emerald { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }
.footer {
  display: flex; justify-content: space-between; align-items: center; padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.08); font-size: 14px; color: #64748b; font-weight: 500;
}
</style>
</head>
<body>
  <div class="header">
    <div>
      <div class="brand-pill"><span class="dot"></span> Artigo 0001 • Fundamentos de IA</div>
      <div class="title">LLM vs. LRM: Duas Ferramentas, Dois Paradigmas Cognitivos</div>
      <div class="subtitle">Previsão estatística de próximo token vs. Raciocínio estruturado com computação em tempo de inferência</div>
    </div>
    <div class="figure-badge">Figura Conceitual</div>
  </div>

  <div class="main">
    <div style="display: flex; gap: 28px; flex: 1;">
      <!-- Lado LLM -->
      <div class="card" style="flex: 1; border-color: rgba(59, 130, 246, 0.35); background: rgba(37, 99, 235, 0.04); justify-content: space-between;">
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
            <span class="badge badge-blue">Geração Causal</span>
            <span class="mono" style="font-size: 14px; color: #60a5fa; font-weight: 700;">LATÊNCIA: 100ms - 500ms</span>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #ffffff; margin-bottom: 8px;">LLM (Large Language Model)</div>
          <div style="font-size: 16px; color: #94a3b8; line-height: 1.5; margin-bottom: 20px;">
            Treinado sobre trilhões de tokens para prever a próxima palavra com máxima plausibilidade estatística.
          </div>

          <div style="background: rgba(0, 0, 0, 0.35); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 16px; margin-bottom: 18px;">
            <div style="font-size: 14px; font-weight: 700; color: #60a5fa; text-transform: uppercase; margin-bottom: 8px;">Mecanismo Operacional:</div>
            <div class="mono" style="font-size: 14px; color: #cbd5e1; line-height: 1.6;">
              Input ➔ [Atenção Transformer] ➔ P(w_t | w_1...w_{t-1}) ➔ Token<br>
              <span style="color: #94a3b8;"># Resposta gerada de forma contínua e sem auto-crítica</span>
            </div>
          </div>

          <div style="display: flex; flex-direction: column; gap: 10px;">
            <div style="background: rgba(59, 130, 246, 0.1); border-radius: 8px; padding: 12px; font-size: 15px; color: #e2e8f0;">
              ✓ <b>Ideal Para:</b> Resumos, redação fluida, tradução, extração de entidades, suporte FAQ rápido.
            </div>
            <div style="background: rgba(239, 68, 68, 0.1); border-radius: 8px; padding: 12px; font-size: 15px; color: #fca5a5;">
              ✗ <b>Risco Crítico:</b> Alucina lógica com confiança; falha em problemas matemáticos e deduções multi-variáveis.
            </div>
          </div>
        </div>

        <div style="border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 14px; font-size: 14px; color: #94a3b8;">
          <b>Modelos de Referência:</b> GPT-4o-mini, Llama 3.1 8B, Qwen 2.5 7B Instruct
        </div>
      </div>

      <!-- Lado LRM -->
      <div class="card" style="flex: 1; border-color: rgba(139, 92, 246, 0.35); background: rgba(139, 92, 246, 0.04); justify-content: space-between;">
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
            <span class="badge badge-purple">Test-Time Compute</span>
            <span class="mono" style="font-size: 14px; color: #c084fc; font-weight: 700;">REFLEXÃO: 2s - 25s</span>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #ffffff; margin-bottom: 8px;">LRM (Large Reasoning Model)</div>
          <div style="font-size: 16px; color: #94a3b8; line-height: 1.5; margin-bottom: 20px;">
            Treinado via reforço (RL) para gerar cadeia oculta de pensamento (CoT), validar hipóteses e auto-corrigir erros antes da saída.
          </div>

          <div style="background: rgba(0, 0, 0, 0.35); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 16px; margin-bottom: 18px;">
            <div style="font-size: 14px; font-weight: 700; color: #c084fc; text-transform: uppercase; margin-bottom: 8px;">Mecanismo Operacional:</div>
            <div class="mono" style="font-size: 14px; color: #cbd5e1; line-height: 1.6;">
              Input ➔ [Decomposição em Subproblemas] ➔ [Backtracking & Provas] ➔ Output<br>
              <span style="color: #a78bfa;">&lt;think&gt; ... reflete 1.500 tokens internamente ... &lt;/think&gt;</span>
            </div>
          </div>

          <div style="display: flex; flex-direction: column; gap: 10px;">
            <div style="background: rgba(139, 92, 246, 0.1); border-radius: 8px; padding: 12px; font-size: 15px; color: #e2e8f0;">
              ✓ <b>Ideal Para:</b> Análise de risco de crédito, auditoria de código, planejamento de múltiplos passos, deduções complexas.
            </div>
            <div style="background: rgba(245, 158, 11, 0.1); border-radius: 8px; padding: 12px; font-size: 15px; color: #fde68a;">
              ✗ <b>Risco / Custo:</b> Latência proibitiva para chat síncrono simples; overkill e custo elevado para tarefas triviais.
            </div>
          </div>
        </div>

        <div style="border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 14px; font-size: 14px; color: #94a3b8;">
          <b>Modelos de Referência:</b> DeepSeek R1, OpenAI o1 / o3, QwQ-32B, Gemini 2.0 Flash Thinking
        </div>
      </div>
    </div>

    <!-- Barra de Conclusão / Arquitetura -->
    <div class="card" style="padding: 18px 28px; background: rgba(16, 185, 129, 0.06); border-color: rgba(16, 185, 129, 0.3); flex-direction: row; align-items: center; justify-content: space-between;">
      <div style="display: flex; align-items: center; gap: 16px;">
        <span class="badge badge-emerald">Decisão Estratégica</span>
        <div style="font-size: 16px; color: #e2e8f0;">
          Não existe rivalidade: use <strong>LLM para a interface rápida e redação</strong> e <strong>LRM como oráculo de raciocínio profundo e validação de regras de negócio</strong>.
        </div>
      </div>
      <div style="font-size: 14px; color: #34d399; font-weight: 700; white-space: nowrap;">
        Engenharia de Soluções Inteligentes
      </div>
    </div>
  </div>

  <div class="footer">
    <div><strong>Pathbit Academy AI</strong> • Engenharia de Inteligência Artificial para Produção</div>
    <div>Figura: Matriz Conceitual e Arquitetural — Large Language Models vs. Large Reasoning Models</div>
  </div>
</body>
</html>
"""

def main() -> None:
    output_png = ROOT / f"{ASSETS}/05_arquitetura_llm_vs_lrm.png"
    print(f"Renderizando figura de arquitetura de 0001: {output_png}...")
    render_html_to_png(HTML_0001, output_png)
    print("Concluído!")

if __name__ == "__main__":
    main()
