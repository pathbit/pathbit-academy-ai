#!/usr/bin/env python3
"""Laboratorio de LLMs locais com Ollama em Docker.

Objetivos deste runner:
1. provar que um stack de IA roda 100% local, sem chave de API e sem custo por token
2. medir latencia, TTFT e vazao de tokens de modelos pequenos na propria maquina
3. gerar artefatos comparaveis entre modelos para decidir qual modelo usar em producao local
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

import matplotlib.pyplot as plt

DEFAULT_BASE_URL = "http://localhost:11434"
DEFAULT_CHAT_MODELS = "qwen2.5:0.5b,qwen2.5:1.5b,llama3.2:1b"
DEFAULT_EMBEDDING_MODEL = "nomic-embed-text"

BENCHMARK_PROMPTS: list[dict[str, str]] = [
    {
        "id": "resumo_curto",
        "categoria": "geracao",
        "prompt": "Responda em uma frase: o que e um LLM?",
    },
    {
        "id": "resumo_politica",
        "categoria": "geracao",
        "prompt": "Resuma em uma linha: devolucao permitida em ate 30 dias para produtos sem uso.",
    },
    {
        "id": "classificacao_intencao",
        "categoria": "roteamento",
        "prompt": (
            "Classifique a intencao do cliente: 'quero a segunda via da fatura deste mes'. "
            "Responda apenas com uma das opcoes: buscar_politica, criar_ticket, resposta_direta."
        ),
    },
    {
        "id": "classificacao_incidente",
        "categoria": "roteamento",
        "prompt": (
            "Classifique a intencao do cliente: 'meu app esta com erro 500 desde ontem'. "
            "Responda apenas com uma das opcoes: buscar_politica, criar_ticket, resposta_direta."
        ),
    },
    {
        "id": "extracao_campos",
        "categoria": "extracao",
        "prompt": (
            "Extraia o produto e o prazo da frase: 'quero devolver um televisor comprado ha 10 dias'. "
            "Responda no formato: produto=<valor>; prazo_dias=<numero>."
        ),
    },
    {
        "id": "explicacao_tecnica",
        "categoria": "geracao",
        "prompt": "Explique em no maximo duas frases para que serve um embedding.",
    },
]

CLASSIFICATION_PROMPT_IDS = {"classificacao_intencao", "classificacao_incidente"}
CLASSIFICATION_EXPECTED = {
    "classificacao_intencao": "buscar_politica",
    "classificacao_incidente": "criar_ticket",
}

RETRIEVAL_DOCS: list[dict[str, str]] = [
    {"id": "politica_devolucao", "conteudo": "A politica de devolucao permite estorno em ate 30 dias corridos para produtos sem uso e com embalagem preservada."},
    {"id": "politica_cancelamento", "conteudo": "O cancelamento sem multa pode ser solicitado em ate 7 dias corridos apos a contratacao."},
    {"id": "segunda_via_fatura", "conteudo": "Para emitir a segunda via da fatura, acesse o portal do cliente, aba Financeiro, opcao Segunda Via."},
    {"id": "suporte_aplicacao", "conteudo": "Falhas tecnicas, erros HTTP 500 e indisponibilidade devem gerar ticket com prioridade alta."},
    {"id": "capacidade_assistente", "conteudo": "O assistente responde sobre politicas, localiza documentos, resume textos e encaminha incidentes."},
    {"id": "prazo_resposta", "conteudo": "O prazo de resposta do suporte e de um dia util para chamados de prioridade media."},
    {"id": "seguranca_conta", "conteudo": "Nunca compartilhe senha, token ou dados de cartao com o atendente ou com o assistente."},
    {"id": "status_plataforma", "conteudo": "Indisponibilidade planejada e comunicada com 48 horas de antecedencia no painel de status."},
]

RETRIEVAL_QUERIES: list[dict[str, str]] = [
    {"id": "q_devolucao", "consulta": "posso devolver um produto sem uso?", "esperado": "politica_devolucao"},
    {"id": "q_fatura", "consulta": "como pego a segunda via do boleto?", "esperado": "segunda_via_fatura"},
    {"id": "q_incidente", "consulta": "o sistema esta fora do ar com erro 500", "esperado": "suporte_aplicacao"},
    {"id": "q_senha", "consulta": "posso passar minha senha no chat?", "esperado": "seguranca_conta"},
]


def http_post_json(base_url: str, path: str, payload: dict, timeout: float = 600.0, retries: int = 3):
    """POST com retry e backoff: um stall do container nao pode invalidar o benchmark."""
    last_error: Exception | None = None
    for attempt in range(retries):
        request = urllib.request.Request(
            f"{base_url}{path}",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = exc
            if attempt + 1 < retries:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"Falha ao chamar {path} apos {retries} tentativas: {last_error}")


def http_get_json(base_url: str, path: str, timeout: float = 30.0, retries: int = 3):
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(f"{base_url}{path}", timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = exc
            if attempt + 1 < retries:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"Falha ao chamar {path} apos {retries} tentativas: {last_error}")


def check_server(base_url: str) -> dict:
    """Verifica o servidor Ollama e devolve versao, modelos e healthy."""
    version = http_get_json(base_url, "/api/version")
    tags = http_get_json(base_url, "/api/tags")
    models = [
        {
            "name": entry["name"],
            "size_bytes": entry.get("size", 0),
        }
        for entry in tags.get("models", [])
    ]
    return {"version": version.get("version", "desconhecida"), "models": models}


def warmup_model(base_url: str, model: str) -> float:
    """Aquece o modelo no container e devolve o tempo de carga observado."""
    start = time.perf_counter()
    http_post_json(
        base_url,
        "/api/chat",
        {
            "model": model,
            "messages": [{"role": "user", "content": "Diga OK"}],
            "stream": False,
            "options": {"temperature": 0, "num_predict": 8},
        },
    )
    return time.perf_counter() - start


def chat_with_metrics(base_url: str, model: str, prompt: str, timeout: float = 300.0) -> dict:
    """Executa um chat em streaming e mede TTFT, tokens e vazao."""
    payload = json.dumps(
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True,
            "options": {"temperature": 0, "num_predict": 128, "num_thread": 4},
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        f"{base_url}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    start = time.perf_counter()
    ttft_ms: float | None = None
    content_parts: list[str] = []
    final: dict = {}

    with urllib.request.urlopen(request, timeout=timeout) as response:
        for raw_line in response:
            chunk = json.loads(raw_line.decode("utf-8"))
            piece = chunk.get("message", {}).get("content", "")
            if piece and ttft_ms is None:
                ttft_ms = (time.perf_counter() - start) * 1000
            content_parts.append(piece)
            if chunk.get("done", False):
                final = chunk
                break

    total_s = time.perf_counter() - start
    eval_count = int(final.get("eval_count", 0))
    eval_duration = float(final.get("eval_duration", 0))
    tokens_per_second = eval_count / (eval_duration / 1e9) if eval_duration > 0 else 0.0

    return {
        "resposta": "".join(content_parts).strip(),
        "ttft_ms": round(ttft_ms, 1) if ttft_ms is not None else round(total_s * 1000, 1),
        "total_ms": round(total_s * 1000, 1),
        "tokens_gerados": eval_count,
        "tokens_por_segundo": round(tokens_per_second, 1),
        "tokens_prompt": int(final.get("prompt_eval_count", 0)),
        "load_ms": round(float(final.get("load_duration", 0)) / 1e6, 1),
    }


def chat_structured(base_url: str, model: str, prompt: str, timeout: float = 300.0) -> tuple[bool, str | None, str]:
    """Chat com saida forcada em JSON: valida a resposta completa e devolve snippet para log."""
    response = http_post_json(
        base_url,
        "/api/generate",
        {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {"temperature": 0, "num_predict": 120},
        },
        timeout=timeout,
    )
    raw = response.get("response", "")
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return False, None, raw[:120]
    valid = isinstance(parsed, dict) and all(key in parsed for key in ("tool", "reason"))
    tool = parsed.get("tool") if isinstance(parsed, dict) else None
    return valid, (str(tool) if tool is not None else None), raw[:120]


def run_chat_benchmark(base_url: str, models: list[str], repeat: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Benchmark de chat: repete os prompts por modelo e consolida metricas."""
    rows: list[dict[str, object]] = []
    for model in models:
        cold_start = warmup_model(base_url, model)
        for repeat_index in range(repeat):
            for case in BENCHMARK_PROMPTS:
                metrics = chat_with_metrics(base_url, model, case["prompt"])
                resposta = metrics["resposta"]
                if case["id"] in CLASSIFICATION_EXPECTED:
                    esperado = CLASSIFICATION_EXPECTED[case["id"]]
                    acertou = esperado in resposta.lower().replace("-", "_")
                else:
                    esperado = ""
                    acertou = len(resposta) > 0
                rows.append(
                    {
                        "modelo": model,
                        "prompt_id": case["id"],
                        "categoria": case["categoria"],
                        "repeticao": repeat_index,
                        "ttft_ms": metrics["ttft_ms"],
                        "total_ms": metrics["total_ms"],
                        "tokens_gerados": metrics["tokens_gerados"],
                        "tokens_prompt": metrics["tokens_prompt"],
                        "tokens_por_segundo": metrics["tokens_por_segundo"],
                        "resposta": resposta,
                        "esperado": esperado,
                        "acertou": acertou,
                    }
                )
    results = pd.DataFrame(rows)

    summary = (
        results.groupby("modelo", as_index=False)
        .agg(
            ttft_medio_ms=("ttft_ms", "mean"),
            total_medio_ms=("total_ms", "mean"),
            tokens_por_segundo=("tokens_por_segundo", "mean"),
            tokens_gerados_medios=("tokens_gerados", "mean"),
            chamadas=("total_ms", "count"),
        )
        .round(1)
        .sort_values("tokens_por_segundo", ascending=False)
    )
    return results, summary


def run_structured_benchmark(base_url: str, models: list[str], attempts: int) -> pd.DataFrame:
    """Mede a taxa de JSON valido e a acuracia de um planner minimalista."""
    prompt = (
        "Voce e um planner de agente. Escolha a tool para: 'quero a segunda via da fatura'. "
        "Tools: buscar_politica, criar_ticket. "
        'Retorne EXATAMENTE um JSON com as chaves "tool" e "reason".'
    )
    rows: list[dict[str, object]] = []
    for model in models:
        validos = 0
        corretos = 0
        for _ in range(attempts):
            valid, tool, raw = chat_structured(base_url, model, prompt)
            if valid:
                validos += 1
                if tool == "buscar_politica":
                    corretos += 1
        rows.append(
            {
                "modelo": model,
                "tentativas": attempts,
                "json_valido": validos,
                "json_valido_pct": round(100 * validos / attempts, 1),
                "tool_correta": corretos,
                "tool_correta_pct": round(100 * corretos / attempts, 1),
            }
        )
    return pd.DataFrame(rows)


def embed_texts(base_url: str, model: str, texts: list[str]) -> tuple[np.ndarray, float]:
    """Gera embeddings em lote e devolve matriz normalizada e latencia."""
    start = time.perf_counter()
    response = http_post_json(base_url, "/api/embed", {"model": model, "input": texts})
    elapsed = time.perf_counter() - start
    vectors = np.array(response["embeddings"], dtype=np.float64)
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return vectors / norms, elapsed


def run_embedding_lab(base_url: str, embedding_model: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Valida retrieval semantico local e mede latencia do embedding."""
    documents = [doc["conteudo"] for doc in RETRIEVAL_DOCS]
    doc_vectors, doc_latency = embed_texts(base_url, embedding_model, documents)
    _, query_latency = embed_texts(base_url, embedding_model, [q["consulta"] for q in RETRIEVAL_QUERIES])

    rows: list[dict[str, object]] = []
    for query in RETRIEVAL_QUERIES:
        query_vector, _ = embed_texts(base_url, embedding_model, [query["consulta"]])
        scores = doc_vectors @ query_vector[0]
        best_index = int(np.argmax(scores))
        rows.append(
            {
                "consulta_id": query["id"],
                "consulta": query["consulta"],
                "documento_top1": RETRIEVAL_DOCS[best_index]["id"],
                "score_top1": round(float(scores[best_index]), 4),
                "esperado": query["esperado"],
                "acertou": RETRIEVAL_DOCS[best_index]["id"] == query["esperado"],
            }
        )
    routes = pd.DataFrame(rows)

    summary = pd.DataFrame(
        [
            {
                "modelo_embedding": embedding_model,
                "dimensao": int(doc_vectors.shape[1]),
                "documentos": len(documents),
                "latencia_batch_docs_ms": round(doc_latency * 1000, 1),
                "latencia_batch_queries_ms": round(query_latency * 1000, 1),
                "taxa_acerto_top1": round(routes["acertou"].mean(), 2),
            }
        ]
    )
    return routes, summary


def plot_benchmark(results: pd.DataFrame, output_png: Path) -> None:
    """Gera grafico comparativo de latencia e vazao por modelo."""
    summary = (
        results.groupby("modelo", as_index=False)
        .agg(total_medio_ms=("total_ms", "mean"), tokens_por_segundo=("tokens_por_segundo", "mean"))
        .sort_values("tokens_por_segundo")
    )
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.2))
    axes[0].barh(summary["modelo"], summary["total_medio_ms"], color="#f59e0b")
    axes[0].set_title("Latencia media total por chamada (ms)")
    axes[0].set_xlabel("ms")
    axes[1].barh(summary["modelo"], summary["tokens_por_segundo"], color="#10b981")
    axes[1].set_title("Vazao media (tokens/s)")
    axes[1].set_xlabel("tokens/s")
    fig.suptitle("LLMs locais via Ollama - benchmark na propria maquina", fontsize=13)
    fig.tight_layout()
    fig.savefig(output_png, dpi=150)
    plt.close(fig)


def df_to_markdown(df: pd.DataFrame) -> str:
    """Formata um DataFrame como tabela markdown sem depender de tabulate."""
    colunas = [str(coluna) for coluna in df.columns]
    linhas = [f"| {' | '.join(colunas)} |", f"| {' | '.join('---' for _ in colunas)} |"]
    for _, row in df.iterrows():
        linhas.append(f"| {' | '.join(str(valor) for valor in row.tolist())} |")
    return "\n".join(linhas)


def build_relatorio(
    server: dict,
    summary: pd.DataFrame,
    structured: pd.DataFrame,
    embedding_summary: pd.DataFrame,
    results: pd.DataFrame,
) -> str:
    """Monta o relatorio markdown com os numeros observados na execucao."""
    linhas: list[str] = [
        "# Relatorio do laboratorio local de LLMs",
        "",
        f"- Servidor: Ollama `{server['version']}` em `http://localhost:11434`",
        f"- Modelos no container: {', '.join(model['name'] for model in server['models'])}",
        f"- Execucao: {len(results)} chamadas de chat, sem chave de API, sem custo por token",
        "",
        "## Chat: latencia e vazao por modelo",
        "",
        df_to_markdown(summary),
        "",
        "## Saida estruturada: JSON valido e tool correta",
        "",
        df_to_markdown(structured),
        "",
        "## Embeddings locais (nomic-embed-text)",
        "",
        df_to_markdown(embedding_summary),
        "",
        "## Interpretacao",
        "",
        "- TTFT e total medem a experiencia real de quem usa o sistema local.",
        "- Tokens/s mostra o tamanho pratico de resposta possivel dentro do SLA.",
        "- JSON valido e tool correta mostram se o modelo sustenta um planner de agente.",
        "- Retrieval top-1 prova que a mesma maquina resolve roteamento semantico sem nuvem.",
        "",
    ]
    return "\n".join(linhas)


def run_lab(
    base_url: str = DEFAULT_BASE_URL,
    chat_models: list[str] | None = None,
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    repeat: int = 2,
    attempts: int = 5,
    skip_plots: bool = False,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Executa o laboratorio completo e persiste os artefatos em data/."""
    models = chat_models if chat_models else DEFAULT_CHAT_MODELS.split(",")
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    print("1/5 Verificando servidor Ollama...")
    server = check_server(base_url)
    available = {model["name"] for model in server["models"]}
    missing = [model for model in models if model not in available]
    if missing:
        raise RuntimeError(
            f"Modelos ausentes no Ollama: {missing}. Execute 'ollama pull <modelo>' dentro do container."
        )
    (data_dir / "modelos_disponiveis.json").write_text(
        json.dumps(server, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"   Ollama {server['version']} com {len(server['models'])} modelos locais")

    print(f"2/5 Benchmark de chat ({len(models)} modelos x {len(BENCHMARK_PROMPTS)} prompts x {repeat} repeticoes)...")
    results, summary = run_chat_benchmark(base_url, models, repeat)
    results.to_csv(data_dir / "benchmark_resultados.csv", index=False, encoding="utf-8")
    summary.to_csv(data_dir / "benchmark_resumo.csv", index=False, encoding="utf-8")

    print("3/5 Benchmark de saida estruturada (JSON)...")
    structured = run_structured_benchmark(base_url, models, attempts)
    structured.to_csv(data_dir / "structured_output.csv", index=False, encoding="utf-8")

    print("4/5 Laboratorio de embeddings e retrieval...")
    routes, embedding_summary = run_embedding_lab(base_url, embedding_model)
    routes.to_csv(data_dir / "embedding_routes.csv", index=False, encoding="utf-8")
    embedding_summary.to_csv(data_dir / "embedding_summary.csv", index=False, encoding="utf-8")

    print("5/5 Persistindo relatorio e grafico...")
    (data_dir / "benchmark_relatorio.md").write_text(
        build_relatorio(server, summary, structured, embedding_summary, results), encoding="utf-8"
    )
    if not skip_plots:
        plot_benchmark(results, data_dir / "benchmark_comparativo.png")

    return results, summary, structured, embedding_summary


def main() -> None:
    matplotlib.use("Agg")
    parser = argparse.ArgumentParser(description="Laboratorio local de LLMs com Ollama em Docker")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Endpoint do Ollama")
    parser.add_argument("--models", default=DEFAULT_CHAT_MODELS, help="Modelos de chat separados por virgula")
    parser.add_argument("--embedding-model", default=DEFAULT_EMBEDDING_MODEL, help="Modelo de embedding local")
    parser.add_argument("--repeat", type=int, default=2, help="Repeticoes por prompt no benchmark de chat")
    parser.add_argument("--attempts", type=int, default=5, help="Tentativas por modelo no teste de JSON")
    parser.add_argument("--skip-plots", action="store_true", help="Nao gera o grafico comparativo")
    args = parser.parse_args()

    models = [model.strip() for model in args.models.split(",") if model.strip()]
    results, summary, structured, embedding_summary = run_lab(
        base_url=args.base_url,
        chat_models=models,
        embedding_model=args.embedding_model,
        repeat=args.repeat,
        attempts=args.attempts,
        skip_plots=args.skip_plots,
    )

    print("\nResumo por modelo:")
    print(summary.to_string(index=False))
    print("\nSaida estruturada:")
    print(structured.to_string(index=False))
    print("\nEmbeddings locais:")
    print(embedding_summary.to_string(index=False))
    print(f"\nArtefatos em: {(Path(__file__).parent.parent / 'data').resolve()}")


if __name__ == "__main__":
    main()
