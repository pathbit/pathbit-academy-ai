#!/usr/bin/env python3
"""Esteira de evals com comparação entre candidatos gratuitos do Hugging Face.

Este runner foi pensado como um harness de decisão:
1. gera respostas de múltiplos candidatos
2. calcula score simples e score ponderado por criticidade
3. detecta regressões por caso
4. escreve artefatos para análise fora do notebook
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer

DEFAULT_EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
DEFAULT_CANDIDATES = [
    "qwen_generico",
    "qwen_estruturado",
    "flan_estruturado",
]
CRITICALITY_WEIGHTS = {"alta": 1.5, "media": 1.0, "baixa": 0.8}


def normalize_tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9]+", text.lower()))


def build_generator(model_name: str):
    """Cria o gerador compatível com o tipo do modelo."""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if "t5" in model_name.lower():
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        mode = "seq2seq"
    else:
        model = AutoModelForCausalLM.from_pretrained(model_name)
        mode = "chat"
    return {"tokenizer": tokenizer, "model": model, "mode": mode, "model_name": model_name}


def build_embedder(model_name: str) -> SentenceTransformer:
    """Cria o modelo de embeddings usado no julgamento semântico."""
    return SentenceTransformer(model_name)


def qwen_generic_prompt(pergunta: str, contexto: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "Voce responde em portugues de forma objetiva para clientes da Pathbit.",
        },
        {
            "role": "user",
            "content": (
                f"Pergunta: {pergunta}\n"
                f"Contexto: {contexto}\n"
                "Responda de forma curta."
            ),
        },
    ]


def qwen_structured_prompt(pergunta: str, contexto: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "Voce e um analista de suporte da Pathbit. Responda sempre em portugues e use somente o contexto recebido.",
        },
        {
            "role": "user",
            "content": (
                f"Pergunta: {pergunta}\n"
                f"Contexto: {contexto}\n"
                "Responda em ate 2 frases, incluindo prazos, condicoes ou passos importantes. "
                "Se faltar informacao no contexto, diga isso claramente."
            ),
        },
    ]


def flan_structured_prompt(pergunta: str, contexto: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "You are a support analyst for Pathbit. Answer in Brazilian Portuguese using only the provided context.",
        },
        {
            "role": "user",
            "content": (
                f"Question: {pergunta}\n"
                f"Context: {contexto}\n"
                "Answer in Brazilian Portuguese in at most 2 sentences, preserving deadlines, conditions and key steps."
            ),
        },
    ]


def messages_to_plain_prompt(messages: list[dict[str, str]]) -> str:
    return "\n\n".join(f"{message['role'].upper()}: {message['content']}" for message in messages)


def generate_answer(generator, messages: list[dict[str, str]], max_new_tokens: int = 96) -> str:
    tokenizer = generator["tokenizer"]
    model = generator["model"]
    mode = generator["mode"]

    if mode == "chat":
        prompt_text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs = tokenizer(prompt_text, return_tensors="pt")
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
        )
        new_tokens = outputs[0][inputs["input_ids"].shape[-1] :]
        return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

    plain_prompt = messages_to_plain_prompt(messages)
    inputs = tokenizer(plain_prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=False,
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()


def semantic_similarity(embedder: SentenceTransformer, gold: str, pred: str) -> float:
    """Compara semanticamente a resposta com o gabarito ideal."""
    vectors = embedder.encode([gold, pred], normalize_embeddings=True)
    return float(np.dot(vectors[0], vectors[1]))


def keyword_recall(keywords: list[str], pred: str) -> float:
    pred_l = pred.lower()
    hits = sum(1 for keyword in keywords if keyword.lower() in pred_l)
    return hits / len(keywords)


def faithfulness(contexto: str, pred: str) -> float:
    contexto_tokens = {token for token in normalize_tokens(contexto) if len(token) > 4}
    pred_tokens = {token for token in normalize_tokens(pred) if len(token) > 4}
    if not pred_tokens:
        return 0.0
    return len(contexto_tokens.intersection(pred_tokens)) / len(pred_tokens)


def weighted_score(score: float, criticidade: str) -> float:
    return score * CRITICALITY_WEIGHTS.get(criticidade, 1.0)


def build_category_summary(results: pd.DataFrame) -> pd.DataFrame:
    """Resume performance por categoria e candidato."""
    return (
        results.groupby(["candidate", "categoria"], as_index=False)[
            ["score_final", "score_ponderado", "faithfulness"]
        ]
        .mean()
        .sort_values(["candidate", "score_ponderado"], ascending=[True, False])
    )


def build_critical_case_table(results: pd.DataFrame) -> pd.DataFrame:
    """Extrai apenas os casos críticos para inspeção rápida."""
    critical = results[results["criticidade"] == "alta"].copy()
    return critical[
        [
            "candidate",
            "modelo_geracao",
            "pergunta",
            "categoria",
            "score_final",
            "score_ponderado",
            "resposta",
        ]
    ]


def save_markdown_report(base_dir: Path, summary: pd.DataFrame, regressions: pd.DataFrame, report: str) -> None:
    """Salva uma versão mais rica do relatório em markdown."""
    lines = [report.strip(), "", "## Ranking de candidatos", ""]
    for _, row in summary.iterrows():
        lines.append(
            f"- `{row['candidate']}` ({row['modelo_geracao']}): score ponderado {row['score_ponderado']:.3f}"
        )
    lines.append("")
    lines.append("## Regressões detectadas")
    lines.append("")
    if regressions.empty:
        lines.append("- Nenhuma regressão relevante detectada.")
    else:
        for _, row in regressions.iterrows():
            lines.append(
                f"- `{row['candidate']}` piorou `{row['pergunta']}` em {row['delta_vs_baseline']:.3f} pontos."
            )
    (base_dir / "data" / "relatorio_evals.md").write_text("\n".join(lines), encoding="utf-8")


def build_candidate_registry():
    return {
        "qwen_generico": {
            "model": "Qwen/Qwen2.5-0.5B-Instruct",
            "prompt_builder": qwen_generic_prompt,
        },
        "qwen_estruturado": {
            "model": "Qwen/Qwen2.5-0.5B-Instruct",
            "prompt_builder": qwen_structured_prompt,
        },
        "flan_estruturado": {
            "model": "google/flan-t5-small",
            "prompt_builder": flan_structured_prompt,
        },
    }


def run_evals(
    candidate_names: list[str] | None = None,
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    limit: int | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, str]:
    base_dir = Path(__file__).parent.parent
    dataset_path = base_dir / "data" / "eval_dataset.csv"
    report_path = base_dir / "data" / "relatorio_evals.md"
    output_csv = base_dir / "data" / "geracoes_evals.csv"
    regressions_path = base_dir / "data" / "regressoes_detectadas.csv"
    summary_path = base_dir / "data" / "candidate_summary.csv"
    category_path = base_dir / "data" / "candidate_summary_by_category.csv"
    critical_path = base_dir / "data" / "critical_cases.csv"

    df = pd.read_csv(dataset_path)
    if limit is not None:
        df = df.head(limit)

    embedder = build_embedder(embedding_model)
    registry = build_candidate_registry()
    candidate_names = candidate_names or DEFAULT_CANDIDATES
    generators = {}
    for candidate_name in candidate_names:
        model_name = registry[candidate_name]["model"]
        if model_name not in generators:
            generators[model_name] = build_generator(model_name)

    rows: list[dict[str, object]] = []
    for _, row in df.iterrows():
        keywords = str(row["palavras_criticas"]).split("|")
        for candidate_name in candidate_names:
            candidate = registry[candidate_name]
            model_name = candidate["model"]
            generator = generators[model_name]
            messages = candidate["prompt_builder"](row["pergunta"], row["contexto"])
            pred = generate_answer(generator, messages)
            score_semantic = semantic_similarity(embedder, row["gold"], pred)
            score_keywords = keyword_recall(keywords, pred)
            score_faithfulness = faithfulness(row["contexto"], pred)
            score_final = float(np.mean([score_semantic, score_keywords, score_faithfulness]))
            score_weighted = weighted_score(score_final, row["criticidade"])
            rows.append(
                {
                    "candidate": candidate_name,
                    "modelo_geracao": model_name,
                    "pergunta": row["pergunta"],
                    "categoria": row["categoria"],
                    "criticidade": row["criticidade"],
                    "gold": row["gold"],
                    "resposta": pred,
                    "similaridade_semantica": score_semantic,
                    "keyword_recall": score_keywords,
                    "faithfulness": score_faithfulness,
                    "score_final": score_final,
                    "score_ponderado": score_weighted,
                }
            )

    results = pd.DataFrame(rows)
    summary = (
        results.groupby(["candidate", "modelo_geracao"], as_index=False)[
            [
                "similaridade_semantica",
                "keyword_recall",
                "faithfulness",
                "score_final",
                "score_ponderado",
            ]
        ]
        .mean()
        .sort_values("score_ponderado", ascending=False)
    )

    baseline_name = "qwen_generico"
    baseline_scores = results[results["candidate"] == baseline_name][
        ["pergunta", "score_ponderado", "criticidade"]
    ].rename(columns={"score_ponderado": "baseline_score"})
    comparison = results.merge(baseline_scores, on=["pergunta", "criticidade"], how="left")
    comparison["delta_vs_baseline"] = comparison["score_ponderado"] - comparison["baseline_score"]
    regressions = comparison[
        (comparison["candidate"] != baseline_name)
        & (comparison["delta_vs_baseline"] < -0.05)
    ].copy()
    category_summary = build_category_summary(results)
    critical_cases = build_critical_case_table(results)

    best_candidate = summary.iloc[0]
    baseline_summary = summary[summary["candidate"] == baseline_name].iloc[0]
    gain = float(best_candidate["score_ponderado"] - baseline_summary["score_ponderado"])
    critical_regressions = regressions[regressions["criticidade"] == "alta"]
    gate = "aprovado" if gain >= 0.05 and critical_regressions.empty else "reprovado"

    report = f"""# Relatório de Evals

- Modelo de embedding: {embedding_model}
- Baseline: {baseline_name}
- Melhor candidato: {best_candidate['candidate']} ({best_candidate['modelo_geracao']})
- Score ponderado baseline: {baseline_summary['score_ponderado']:.3f}
- Score ponderado vencedor: {best_candidate['score_ponderado']:.3f}
- Ganho ponderado: {gain:.3f}
- Regressões críticas detectadas: {len(critical_regressions)}
- Gate de release: {gate}
"""

    results.to_csv(output_csv, index=False)
    summary.to_csv(summary_path, index=False)
    regressions.to_csv(regressions_path, index=False)
    category_summary.to_csv(category_path, index=False)
    critical_cases.to_csv(critical_path, index=False)
    save_markdown_report(base_dir, summary, regressions, report)
    return results, summary, report


def main() -> None:
    parser = argparse.ArgumentParser(description="Esteira de evals comparando candidatos gratuitos")
    parser.add_argument(
        "--candidates",
        default=",".join(DEFAULT_CANDIDATES),
        help="Lista de candidatos separados por virgula",
    )
    parser.add_argument("--embedding-model", default=DEFAULT_EMBEDDING_MODEL, help="Modelo de embedding do Hugging Face")
    parser.add_argument("--limit", type=int, default=None, help="Limita o número de casos para testes rápidos")
    args = parser.parse_args()
    candidate_names = [candidate.strip() for candidate in args.candidates.split(",") if candidate.strip()]

    results, summary, report = run_evals(
        candidate_names=candidate_names,
        embedding_model=args.embedding_model,
        limit=args.limit,
    )

    print(report)
    print("Resumo agregado:")
    print(summary.to_string(index=False))
    print("\nAmostra de respostas:")
    print(results[["candidate", "modelo_geracao", "pergunta", "score_ponderado", "resposta"]].head(9).to_string(index=False))


if __name__ == "__main__":
    main()
