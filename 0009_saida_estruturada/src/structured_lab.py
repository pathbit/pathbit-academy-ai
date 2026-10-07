#!/usr/bin/env python3
"""Laboratorio de saida estruturada com LLMs locais via Ollama.

Compara tres niveis de contrato sobre os mesmos modelos e prompts:
- livre:  sem constraint, o prompt apenas pede JSON
- json:   format="json" garante sintaxe parseavel
- schema: format=<json schema> garante o contrato completo (campos, tipos, enum)

Para cada chamada mede parse, validacao de schema, correcao semantica e latencia,
inclusive o efeito de uma unica tentativa de retry apos falha.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

import jsonschema
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

DEFAULT_BASE_URL = "http://localhost:11434"
DEFAULT_CHAT_MODELS = "qwen2.5:0.5b,qwen2.5:1.5b,llama3.2:1b"

PLANNER_SCHEMA = {
    "type": "object",
    "properties": {
        "tool": {"type": "string", "enum": ["buscar_politica", "criar_ticket", "resposta_direta"]},
        "confianca": {"type": "number"},
    },
    "required": ["tool", "confianca"],
}

EXTRACAO_SCHEMA = {
    "type": "object",
    "properties": {
        "produto": {"type": "string"},
        "prazo_dias": {"type": "integer"},
    },
    "required": ["produto", "prazo_dias"],
}

ROTAS_SCHEMA = {
    "type": "object",
    "properties": {
        "rota": {"type": "string", "enum": ["buscar_politica", "criar_ticket", "resposta_direta"]},
        "urgencia": {"type": "string", "enum": ["baixa", "media", "alta"]},
    },
    "required": ["rota", "urgencia"],
}

TASKS: list[dict] = [
    {
        "id": "planner",
        "prompt": "O cliente quer a segunda via da fatura deste mes. Escolha a tool e informe a confianca entre 0 e 1.",
        "schema": PLANNER_SCHEMA,
        "semantico": lambda r: r.get("tool") == "buscar_politica",
    },
    {
        "id": "extracao",
        "prompt": "Extraia o produto e o prazo da frase: 'quero devolver um televisor comprado ha 10 dias'.",
        "schema": EXTRACAO_SCHEMA,
        "semantico": lambda r: r.get("prazo_dias") == 10 and "televisor" in str(r.get("produto", "")).lower(),
    },
    {
        "id": "roteamento",
        "prompt": "Classifique a mensagem do cliente: 'meu app esta com erro 500 desde ontem'. Informe a rota e a urgencia.",
        "schema": ROTAS_SCHEMA,
        "semantico": lambda r: r.get("rota") == "criar_ticket" and r.get("urgencia") == "alta",
    },
]

MODOS = ("livre", "json", "schema")


def http_post_json(base_url: str, path: str, payload: dict, timeout: float = 300.0) -> dict:
    for attempt in range(3):
        try:
            request = urllib.request.Request(
                f"{base_url}{path}",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.HTTPError, urllib.error.URLError) as exc:
            if attempt < 2:
                time.sleep(1.5)
                continue
            raise exc
    raise RuntimeError("Falha apos retries HTTP")



def check_server(base_url: str) -> dict:
    with urllib.request.urlopen(f"{base_url}/api/version", timeout=30) as response:
        v = json.loads(response.read().decode("utf-8"))
    with urllib.request.urlopen(f"{base_url}/api/tags", timeout=30) as response:
        tags = json.loads(response.read().decode("utf-8"))
    return {"version": v.get("version", "?"), "models": [m["name"] for m in tags.get("models", [])]}


def gerar(base_url: str, model: str, prompt: str, modo: str, schema: dict | None, temperature: float) -> dict:
    """Uma chamada /api/generate no modo pedido, com metricas de tempo e tokens."""
    payload: dict = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature, "num_predict": 128, "num_thread": 4},
    }
    if modo == "json":
        payload["format"] = "json"
    elif modo == "schema":
        payload["format"] = schema


    start = time.perf_counter()
    response = http_post_json(base_url, "/api/generate", payload)
    total_ms = (time.perf_counter() - start) * 1000
    return {
        "resposta": response.get("response", ""),
        "total_ms": round(total_ms, 1),
        "tokens": int(response.get("eval_count", 0)),
    }


def limpar_fences(raw: str) -> str:
    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
    return text.strip()


def avaliar(raw: str, schema: dict) -> tuple[bool, bool, dict | None]:
    """Tenta parsear (direto e apos limpeza de fences) e valida contra o schema."""
    parsed = None
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        try:
            parsed = json.loads(limpar_fences(raw))
        except json.JSONDecodeError:
            return False, False, None
    parse_ok = True
    try:
        jsonschema.validate(instance=parsed, schema=schema)
        return parse_ok, True, parsed
    except jsonschema.ValidationError:
        return parse_ok, False, parsed


def run_task_case(base_url: str, model: str, task: dict, modo: str) -> dict:
    """Uma linha de resultado: primeira tentativa + retry unico quando falha."""
    schema = task["schema"] if modo == "schema" else task["schema"]

    tentativas: list[dict] = []
    for index, temperature in enumerate((0.0, 0.7)):
        call = gerar(base_url, model, task["prompt"], modo, schema, temperature)
        parse_ok, schema_ok, parsed = avaliar(call["resposta"], schema)
        semantico_ok = bool(schema_ok and parsed is not None and task["semantico"](parsed))
        tentativas.append(
            {
                "modelo": model,
                "tarefa": task["id"],
                "modo": modo,
                "tentativa": index + 1,
                "parse_ok": parse_ok,
                "schema_ok": schema_ok,
                "semantico_ok": semantico_ok,
                "total_ms": call["total_ms"],
                "tokens": call["tokens"],
                "resposta": call["resposta"][:160],
            }
        )
        if parse_ok and schema_ok:
            break
    if len(tentativas) == 1:
        tentativas[0]["recuperado"] = False
        return tentativas[0]
    return _linha_consolidada(tentativas)


def _linha_consolidada(tentativas: list[dict]) -> dict:
    final = dict(tentativas[-1])
    primeira = tentativas[0]
    falhou_primeira = not (primeira["parse_ok"] and primeira["schema_ok"])
    final["tentativa"] = len(tentativas)
    final["recuperado"] = falhou_primeira and (final["parse_ok"] and final["schema_ok"])
    final["total_ms"] = round(sum(t["total_ms"] for t in tentativas), 1)
    final["tokens"] = sum(t["tokens"] for t in tentativas)
    return final


def benchmark_system_one(base_url: str, repeat: int = 5) -> dict:
    """Mede roteamento por similaridade de embeddings, sem decoder autoregressivo.

    Não executa Jev, Laya ou outro modelo comercial de decisão. As pontuações
    softmax abaixo ordenam similaridades; não são probabilidades calibradas.
    """
    import math

    classes = {
        "buscar_politica": "buscar segunda via de fatura ou boleto de pagamento",
        "criar_ticket": "abrir chamado de suporte tecnico para erro ou incidente",
        "resposta_direta": "responder duvida geral diretamente sem ferramentas",
    }

    def get_emb(text: str) -> list[float]:
        payload = json.dumps({"model": "nomic-embed-text", "prompt": text}).encode()
        req = urllib.request.Request(
            f"{base_url}/api/embeddings", data=payload, headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=30) as res:
            return json.loads(res.read())["embedding"]

    def cosine(a: list[float], b: list[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(y * y for y in b))
        return dot / (na * nb) if (na * nb) > 0 else 0.0

    class_names = list(classes.keys())
    class_embs = [get_emb(desc) for desc in classes.values()]

    test_queries = [
        ("O cliente quer a segunda via da fatura deste mes.", "buscar_politica"),
        ("Meu aplicativo esta travando com erro 500.", "criar_ticket"),
        ("Qual o horario de atendimento da empresa?", "resposta_direta"),
    ]

    latencias: list[float] = []
    acertos = 0
    total_calls = 0

    for _ in range(repeat):
        for query, expected in test_queries:
            t0 = time.perf_counter()
            q_emb = get_emb(query)
            sims = [cosine(q_emb, ce) for ce in class_embs]
            exps = [math.exp(s * 10) for s in sims]
            s_exp = sum(exps)
            probs = [e / s_exp for e in exps]
            best_idx = probs.index(max(probs))
            chosen = class_names[best_idx]
            elapsed_ms = (time.perf_counter() - t0) * 1000

            latencias.append(elapsed_ms)
            if chosen == expected:
                acertos += 1
            total_calls += 1

    latencias_sorted = sorted(latencias)
    p50 = latencias_sorted[len(latencias_sorted) // 2]
    p95 = latencias_sorted[int(len(latencias_sorted) * 0.95)]
    media = sum(latencias) / len(latencias)

    return {
        "paradigma": "Roteador por embeddings nomic-embed-text e similaridade de cosseno",
        "frameworks_referencia": ["Ollama / nomic-embed-text"],
        "chamadas_avaliadas": total_calls,
        "acuracia_pct": round(100 * acertos / total_calls, 1),
        "latencia_media_ms": round(media, 2),
        "latencia_p50_ms": round(p50, 2),
        "latencia_p95_ms": round(p95, 2),
        "tokens_gerados": 0,
        "conformidade_schema_pct": 100.0,
    }


def run_lab(base_url: str, models: list[str], repeat: int, skip_plots: bool = False):
    """Executa a matriz models x tarefas x modos x repeticoes e persiste artefatos."""
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    server = check_server(base_url)
    missing = [m for m in models if m not in server["models"]]
    if missing:
        raise RuntimeError(f"Modelos ausentes no Ollama: {missing}. Rode 'ollama pull <modelo>'.")
    print(f"Ollama {server['version']} com {len(server['models'])} modelos locais")

    rows: list[dict] = []
    total = len(models) * len(TASKS) * len(MODOS) * repeat
    done = 0
    for model in models:
        for _ in range(repeat):
            for task in TASKS:
                for modo in MODOS:
                    rows.append(run_task_case(base_url, model, task, modo))
                    done += 1
                    print(f"[{done:3d}/{total}] {model} {task['id']:9s} {modo:6s}", flush=True)

    results = pd.DataFrame(rows)
    results["falha"] = ~(results["parse_ok"] & results["schema_ok"])
    results.to_csv(data_dir / "structured_resultados.csv", index=False, encoding="utf-8")

    resumo = (
        results.groupby("modo", as_index=False)
        .agg(
            parse_ok_pct=("parse_ok", lambda s: round(100 * s.mean(), 1)),
            schema_ok_pct=("schema_ok", lambda s: round(100 * s.mean(), 1)),
            semantico_ok_pct=("semantico_ok", lambda s: round(100 * s.mean(), 1)),
            recuperado_pct=("recuperado", lambda s: round(100 * s.mean(), 1)),
            total_medio_ms=("total_ms", "mean"),
            tokens_medios=("tokens", "mean"),
            chamadas=("total_ms", "count"),
        )
        .round(1)
    )
    resumo.to_csv(data_dir / "structured_resumo.csv", index=False, encoding="utf-8")

    por_modelo = (
        results.groupby(["modelo", "modo"], as_index=False)
        .agg(
            parse_ok_pct=("parse_ok", lambda s: round(100 * s.mean(), 1)),
            schema_ok_pct=("schema_ok", lambda s: round(100 * s.mean(), 1)),
            semantico_ok_pct=("semantico_ok", lambda s: round(100 * s.mean(), 1)),
            total_medio_ms=("total_ms", "mean"),
        )
        .round(1)
    )
    por_modelo.to_csv(data_dir / "structured_resumo_modelo.csv", index=False, encoding="utf-8")

    # Benchmark do Paradigma System 1 (Single Forward Pass)
    sys1_metrics = benchmark_system_one(base_url, repeat=max(2, repeat))
    with open(data_dir / "system_one_comparativo.json", "w", encoding="utf-8") as f:
        json.dump(sys1_metrics, f, indent=2)

    if not skip_plots:
        plot_resumo(resumo, por_modelo, data_dir / "structured_comparativo.png")

    (data_dir / "structured_relatorio.md").write_text(
        montar_relatorio(server, resumo, por_modelo, sys1_metrics), encoding="utf-8"
    )
    return results, resumo, por_modelo, sys1_metrics



def plot_resumo(resumo: pd.DataFrame, por_modelo: pd.DataFrame, output_png: Path) -> None:
    """Gera grafico comparativo: contratos atendidos por modo e latencia por modo."""
    fig, axes = plt.subplots(1, 3, figsize=(17, 4.6))
    ordem = ["livre", "json", "schema"]
    x = range(len(ordem))

    schema_pct = [float(resumo[resumo["modo"] == m]["schema_ok_pct"].iloc[0]) for m in ordem]
    semantico_pct = [float(resumo[resumo["modo"] == m]["semantico_ok_pct"].iloc[0]) for m in ordem]
    axes[0].bar([i - 0.18 for i in x], schema_pct, width=0.36, label="schema_ok %", color="#10b981")
    axes[0].bar([i + 0.18 for i in x], semantico_pct, width=0.36, label="semantico_ok %", color="#8b5cf6")
    axes[0].set_xticks(list(x))
    axes[0].set_xticklabels(ordem)
    axes[0].set_title("Contrato atendido por nivel")
    axes[0].set_ylim(0, 105)
    axes[0].legend()

    for modelo in por_modelo["modelo"].unique():
        sub = por_modelo[por_modelo["modelo"] == modelo].set_index("modo")
        axes[1].plot(ordem, [float(sub.loc[m, "total_medio_ms"]) for m in ordem], marker="o", label=modelo)
    axes[1].set_title("Latencia media por nivel (ms)")
    axes[1].legend(fontsize=8)
    axes[1].grid(alpha=0.3)

    axes[2].axis("off")
    tabela = resumo[["modo", "parse_ok_pct", "schema_ok_pct", "semantico_ok_pct", "total_medio_ms"]]
    axes[2].table(cellText=tabela.values, colLabels=tabela.columns, loc="center", cellLoc="center")
    axes[2].set_title("Resumo por nivel")

    fig.suptitle("Saida estruturada: do prompt otimista ao contrato validado", fontsize=13)
    fig.tight_layout()
    fig.savefig(output_png, dpi=150)
    plt.close(fig)


def montar_relatorio(server: dict, resumo: pd.DataFrame, por_modelo: pd.DataFrame, sys1: dict | None = None) -> str:
    linhas = [
        "# Relatorio do laboratorio de saida estruturada",
        "",
        f"- Servidor: Ollama `{server['version']}`",
        f"- Modelos: {', '.join(server['models'])}",
        "",
        "## Resumo por nivel de contrato",
        "",
        resumo.to_markdown(index=False),
        "",
        "## Resumo por modelo e nivel",
        "",
        por_modelo.to_markdown(index=False),
        "",
    ]
    if sys1:
        linhas.extend(
            [
                "## Baseline não generativa: roteamento por embeddings",
                "",
                f"- **Paradigma:** `{sys1['paradigma']}`",
                f"- **Referencias da Industria:** `{', '.join(sys1['frameworks_referencia'])}`",
                f"- **Latencia Mediana (p50):** `{sys1['latencia_p50_ms']} ms`",
                f"- **Latencia Percentil 95 (p95):** `{sys1['latencia_p95_ms']} ms`",
                f"- **Latencia Media:** `{sys1['latencia_media_ms']} ms`",
                f"- **Tokens gerados no decoder:** `{sys1['tokens_gerados']}` (sem loop autoregressivo)",
                f"- **Conformidade com schema:** `{sys1['conformidade_schema_pct']}%`",
                f"- **Acuracia de decisao:** `{sys1['acuracia_pct']}%`",
                "",
                "> **Limite:** esta baseline escolhe entre três rótulos fixos usando embeddings. Não mede Jev ou Laya, não extrai argumentos e não demonstra equivalência com um modelo generativo. Compare a latência com o resumo desta execução, sem extrapolar para outros produtos.",
                "",
            ]
        )
    linhas.extend(
        [
            "## Leitura",
            "",
            "- `parse_ok` aceita JSON direto ou apos limpeza de code fences (resgate basico).",
            "- `schema_ok` exige validacao jsonschema contra o contrato da tarefa.",
            "- `semantico_ok` exige o valor de negocio correto dentro do contrato.",
            "- Latencia do modo `schema` inclui o custo de decodificar sob a gramatica.",
            "",
        ]
    )
    return "\n".join(linhas)


def main() -> None:
    matplotlib.use("Agg")
    parser = argparse.ArgumentParser(description="Laboratorio de saida estruturada com Ollama")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--models", default=DEFAULT_CHAT_MODELS)
    parser.add_argument("--repeat", type=int, default=3)
    parser.add_argument("--skip-plots", action="store_true")
    args = parser.parse_args()

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    results, resumo, por_modelo, sys1 = run_lab(args.base_url, models, args.repeat, args.skip_plots)

    print("\nResumo por nivel de contrato:")
    print(resumo.to_string(index=False))
    print("\nResumo por modelo e nivel:")
    print(por_modelo.to_string(index=False))
    print("\nFronteira System 1 (Passada Unica sem Tokens de Decoder):")
    print(f"  Latencia media: {sys1['latencia_media_ms']} ms | p50: {sys1['latencia_p50_ms']} ms | Acuracia: {sys1['acuracia_pct']}%")
    print(f"\nArtefatos em: {(Path(__file__).parent.parent / 'data').resolve()}")


if __name__ == "__main__":
    main()

