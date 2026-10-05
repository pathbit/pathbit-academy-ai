#!/usr/bin/env python3
"""Laboratorio MCP local: Ollama como planner sobre tools de um servidor MCP.

O loop provado aqui:
1. o cliente MCP inicia o servidor local via stdio e descobre as tools (list_tools)
2. o catalogo descoberto entra no prompt do planner, e o Ollama escolhe a tool
   com saida forçada por JSON Schema (artigo 0009)
3. o cliente executa a tool escolhida via MCP (call_tool) e mede o custo do pulo
4. toda decisao vira linha de auditoria em CSV

Nada sai da maquina: sem chave de API, sem conta, sem rede externa.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import statistics
import sys
import time
import urllib.request
from pathlib import Path

import jsonschema
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

DEFAULT_BASE_URL = "http://localhost:11434"
DEFAULT_CHAT_MODELS = "qwen2.5:0.5b,qwen2.5:1.5b,llama3.2:1b"
PROTOCOL_CALLS = 50

PLANNER_SCHEMA = {
    "type": "object",
    "properties": {
        "tool": {"type": "string", "enum": ["buscar_politica", "criar_ticket", "resumo_atendimento", "responder_direto"]},
        "argumentos": {
            "type": "object",
            "properties": {
                "topico": {"type": "string"},
                "titulo": {"type": "string"},
                "prioridade": {"type": "string"},
                "nome_cliente": {"type": "string"},
            },
        },
    },
    "required": ["tool", "argumentos"],
}

QUERIES: list[dict[str, str]] = [
    {"id": "q_fatura", "consulta": "quero a segunda via da fatura deste mes", "esperado": "buscar_politica", "argumento": "segunda_via"},
    {"id": "q_devolucao", "consulta": "posso devolver um produto sem uso?", "esperado": "buscar_politica", "argumento": "devolucao"},
    {"id": "q_incidente", "consulta": "meu app esta com erro 500 desde ontem", "esperado": "criar_ticket", "argumento": ""},
    {"id": "q_cancelamento", "consulta": "quero cancelar minha assinatura sem pagar multa", "esperado": "buscar_politica", "argumento": "cancelamento"},
    {"id": "q_capacidade", "consulta": "o que voce consegue fazer por mim?", "esperado": "responder_direto", "argumento": ""},
    {"id": "q_ticket", "consulta": "nao consigo emitir o boleto, preciso abrir um chamado urgente", "esperado": "criar_ticket", "argumento": ""},
]

ARGUMENTO_CHAVE = {
    "buscar_politica": "topico",
    "criar_ticket": "titulo",
    "resumo_atendimento": "nome_cliente",
    "responder_direto": None,
}


def http_get_json(url: str, timeout: float = 30.0) -> dict:
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def montar_prompt_planner(catalogo: list[dict], consulta: str) -> str:
    linhas = [
        "Voce e o planner de um agente de suporte. Escolha a tool para a pergunta do cliente.",
        "Tools disponiveis (catalogo descoberto via MCP):",
    ]
    for tool in catalogo:
        linhas.append(f"- {tool['nome']}: {tool['descricao']}")
    linhas.append("- responder_direto: use quando nenhuma tool se aplica (pergunta sobre o proprio assistente).")
    linhas.append("Argumentos: buscar_politica(topico); criar_ticket(titulo, prioridade); resumo_atendimento(nome_cliente).")
    linhas.append(f"Pergunta do cliente: '{consulta}'")
    linhas.append('Responda EXATAMENTE um JSON com "tool" e "argumentos".')
    return "\n".join(linhas)


async def plano_do_modelo(base_url: str, model: str, prompt: str) -> tuple[dict | None, float, int]:
    """Chama o Ollama com schema forçado e devolve plano parseado, latencia e tokens."""
    payload = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "format": PLANNER_SCHEMA,
            "options": {"temperature": 0},
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        f"{base_url}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    start = time.perf_counter()
    with urllib.request.urlopen(request, timeout=300) as response:
        out = json.loads(response.read().decode("utf-8"))
    total_ms = (time.perf_counter() - start) * 1000
    try:
        plano = json.loads(out.get("response", ""))
    except json.JSONDecodeError:
        plano = None
    return plano, round(total_ms, 1), int(out.get("eval_count", 0))


async def run_lab(base_url: str, models: list[str], repeat: int, skip_plots: bool = False):
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    version = http_get_json(f"{base_url}/api/version").get("version", "?")
    tags = http_get_json(f"{base_url}/api/tags")
    disponiveis = [m["name"] for m in tags.get("models", [])]
    missing = [m for m in models if m not in disponiveis]
    if missing:
        raise RuntimeError(f"Modelos ausentes no Ollama: {missing}. Rode 'ollama pull <modelo>'.")
    print(f"Ollama {version} com {len(disponiveis)} modelos locais")

    server_path = Path(__file__).parent / "mcp_server.py"
    params = StdioServerParameters(command=sys.executable, args=[str(server_path)])

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()

            catalogo = [
                {
                    "nome": tool.name,
                    "descricao": tool.description,
                    "input_schema": tool.input_schema,
                }
                for tool in tools.tools
            ]
            (data_dir / "catalogo_tools.json").write_text(
                json.dumps(catalogo, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            print(f"MCP: servidor 'pathbit-suporte' com {len(catalogo)} tools descobertas")

            # Benchmark do pulo de protocolo sem modelo no caminho.
            latencias_ms: list[float] = []
            for _ in range(PROTOCOL_CALLS):
                start = time.perf_counter()
                await session.call_tool("buscar_politica", {"topico": "devolucao"})
                latencias_ms.append((time.perf_counter() - start) * 1000)
            protocolo = {
                "chamadas": PROTOCOL_CALLS,
                "p50_ms": round(statistics.median(latencias_ms), 2),
                "p95_ms": round(sorted(latencias_ms)[int(0.95 * len(latencias_ms)) - 1], 2),
                "media_ms": round(statistics.fmean(latencias_ms), 2),
            }
            (data_dir / "mcp_latencia_protocolo.json").write_text(
                json.dumps(protocolo, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            print(f"MCP: call_tool x{PROTOCOL_CALLS} -> p50 {protocolo['p50_ms']} ms / p95 {protocolo['p95_ms']} ms")

            rows: list[dict] = []
            total = len(models) * len(QUERIES) * repeat
            done = 0
            for model in models:
                await plano_do_modelo(base_url, model, montar_prompt_planner(catalogo, "aquecimento"))
                for _ in range(repeat):
                    for q in QUERIES:
                        prompt = montar_prompt_planner(catalogo, q["consulta"])
                        plano, plan_ms, tokens = await plano_do_modelo(base_url, model, prompt)

                        tool_escolhida = (plano or {}).get("tool", "invalido")
                        argumentos = (plano or {}).get("argumentos", {}) if isinstance(plano, dict) else {}
                        try:
                            jsonschema.validate(instance=plano, schema=PLANNER_SCHEMA)
                            schema_ok = True
                        except jsonschema.ValidationError:
                            schema_ok = False

                        mcp_ms = 0.0
                        resposta_mcp = ""
                        if schema_ok and tool_escolhida in {t["nome"] for t in catalogo}:
                            start = time.perf_counter()
                            result = await session.call_tool(tool_escolhida, argumentos)
                            mcp_ms = round((time.perf_counter() - start) * 1000, 2)
                            resposta_mcp = result.content[0].text[:200]

                        chave = ARGUMENTO_CHAVE.get(tool_escolhida)
                        argumento_ok = bool(chave is None or str(argumentos.get(chave, "")))
                        rows.append(
                            {
                                "modelo": model,
                                "consulta_id": q["id"],
                                "repeticao": _,
                                "tool_escolhida": tool_escolhida,
                                "tool_esperada": q["esperado"],
                                "acertou": tool_escolhida == q["esperado"],
                                "argumento_ok": argumento_ok,
                                "schema_ok": schema_ok,
                                "plan_ms": plan_ms,
                                "mcp_ms": mcp_ms,
                                "tokens": tokens,
                                "resposta_mcp": resposta_mcp,
                            }
                        )
                        done += 1
                        print(f"[{done:3d}/{total}] {model} {q['id']:13s} -> {tool_escolhida}", flush=True)

    results = pd.DataFrame(rows)
    results.to_csv(data_dir / "mcp_resultados.csv", index=False, encoding="utf-8")

    resumo = (
        results.groupby("modelo", as_index=False)
        .agg(
            plano_valido_pct=("schema_ok", lambda s: round(100 * s.mean(), 1)),
            tool_certa_pct=("acertou", lambda s: round(100 * s.mean(), 1)),
            argumento_ok_pct=("argumento_ok", lambda s: round(100 * s.mean(), 1)),
            plan_medio_ms=("plan_ms", "mean"),
            mcp_medio_ms=("mcp_ms", "mean"),
            tokens_medios=("tokens", "mean"),
        )
        .round(1)
        .sort_values("tool_certa_pct", ascending=False)
    )
    resumo.to_csv(data_dir / "mcp_resumo.csv", index=False, encoding="utf-8")

    if not skip_plots:
        plot_lab(results, resumo, protocolo, data_dir / "mcp_comparativo.png")

    relatorio = [
        "# Relatorio do laboratorio MCP local",
        "",
        f"- Servidor de modelos: Ollama `{version}` | Servidor de tools: MCP stdio `pathbit-suporte`",
        f"- Tools descobertas: {', '.join(t['nome'] for t in catalogo)}",
        f"- Custo do pulo de protocolo (call_tool): p50 {protocolo['p50_ms']} ms / p95 {protocolo['p95_ms']} ms em {PROTOCOL_CALLS} chamadas",
        "",
        "## Planner por modelo",
        "",
        resumo.to_markdown(index=False),
        "",
        "## Leitura",
        "",
        "- `plan_ms` domina: o modelo em CPU custa ordens de magnitude mais que o protocolo.",
        "- O pulo MCP (`mcp_ms`) e milissegundos; o gargalo segue sendo a geracao do plano.",
        "- A decisao correta depende do modelo, nao do protocolo - o MCP garante o contrato.",
        "",
    ]
    (data_dir / "mcp_relatorio.md").write_text("\n".join(relatorio), encoding="utf-8")
    return results, resumo


def plot_lab(results: pd.DataFrame, resumo: pd.DataFrame, protocolo: dict, output_png: Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(17, 4.6))

    axes[0].barh(resumo["modelo"], resumo["tool_certa_pct"], color="#f59e0b")
    axes[0].set_xlim(0, 105)
    axes[0].set_title("Tool correta por modelo (%)")

    por_modelo = results.groupby("modelo", as_index=False).agg(plan=("plan_ms", "mean"), mcp=("mcp_ms", "mean"))
    axes[1].bar(por_modelo["modelo"], por_modelo["plan"], color="#8b5cf6", label="plano (Ollama)")
    axes[1].bar(por_modelo["modelo"], por_modelo["mcp"], color="#10b981", label="call_tool (MCP)")
    axes[1].set_yscale("log")
    axes[1].set_title("Onde o tempo e gasto (ms, escala log)")
    axes[1].legend(fontsize=8)

    axes[2].axis("off")
    linhas = [
        ["chamadas", protocolo["chamadas"]],
        ["p50 (ms)", protocolo["p50_ms"]],
        ["p95 (ms)", protocolo["p95_ms"]],
        ["media (ms)", protocolo["media_ms"]],
    ]
    axes[2].table(cellText=linhas, colLabels=["call_tool MCP", "valor"], loc="center", cellLoc="center")
    axes[2].set_title("Custo do pulo de protocolo")

    fig.suptitle("MCP local: planner Ollama sobre tools padronizadas", fontsize=13)
    fig.tight_layout()
    fig.savefig(output_png, dpi=150)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Laboratorio MCP local com Ollama")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--models", default=DEFAULT_CHAT_MODELS)
    parser.add_argument("--repeat", type=int, default=2)
    parser.add_argument("--skip-plots", action="store_true")
    args = parser.parse_args()

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    results, resumo = asyncio.run(run_lab(args.base_url, models, args.repeat, args.skip_plots))

    print("\nResumo por modelo:")
    print(resumo.to_string(index=False))
    print(f"\nArtefatos em: {(Path(__file__).parent.parent / 'data').resolve()}")


if __name__ == "__main__":
    main()
