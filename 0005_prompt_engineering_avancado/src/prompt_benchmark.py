#!/usr/bin/env python3
"""Laboratório de prompt engineering com comparação entre estratégias e modelos gratuitos.

Este script foi desenhado para ser mais do que uma simples execução de prompts.
Ele produz:
1. execuções brutas por caso, estratégia e modelo
2. resumo agregado por modelo/estratégia
3. delta contra a estratégia base
4. breakdown por caso com campos ausentes
5. relatório em markdown para leitura rápida
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer

DEFAULT_GENERATION_MODELS = [
    "Qwen/Qwen2.5-0.5B-Instruct",
    "google/flan-t5-small",
]
DEFAULT_EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
OUTPUT_FIELDS = ["resumo", "prioridade", "proxima_acao"]
FIELD_PATTERNS = {
    "resumo": r"^\s*resumo\s*:\s*(.+)$",
    "prioridade": r"^\s*prioridade\s*:\s*(.+)$",
    "proxima_acao": r"^\s*proxima[_\s]+a[cç][aã]o\s*:\s*(.+)$",
}

FEW_SHOT_EXAMPLE = """Exemplo 1
Mensagem: Cliente reportou erro 500 e pede retorno urgente.
Saida:
resumo: Cliente reportou erro 500 e pede retorno urgente.
prioridade: alta
proxima_acao: abrir ticket tecnico e responder em ate 1h
"""

CHECKLIST_EXAMPLE = """Checklist interno
1. identificar o problema central
2. inferir prioridade
3. sugerir a proxima acao mais segura
"""

STRATEGY_DESCRIPTIONS = {
    "base": "Instrução curta e pouco controlada.",
    "estruturado": "Contrato de saída rígido, sem few-shot.",
    "few_shot": "Contrato de saída com exemplo orientador.",
    "checklist": "Contrato com checklist operacional explícito.",
}


def load_dataset(base_dir: Path) -> pd.DataFrame:
    """Carrega o dataset principal do laboratório."""
    dataset_path = base_dir / "data" / "prompt_dataset.json"
    with dataset_path.open("r", encoding="utf-8") as file:
        dataset = json.load(file)
    return pd.DataFrame(dataset)


def build_generator(model_name: str):
    """Cria o modelo gerador.

    A implementação suporta dois modos:
    - seq2seq, como T5/FLAN
    - chat/causal, como Qwen instruct
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if "t5" in model_name.lower():
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        mode = "seq2seq"
    else:
        model = AutoModelForCausalLM.from_pretrained(model_name)
        mode = "chat"
    return {"tokenizer": tokenizer, "model": model, "mode": mode, "model_name": model_name}


def build_embedder(model_name: str) -> SentenceTransformer:
    """Cria o modelo de embeddings usado na avaliação semântica."""
    return SentenceTransformer(model_name)


def generic_prompt(texto: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "Voce e um analista de atendimento da Pathbit. Responda em portugues.",
        },
        {
            "role": "user",
            "content": (
                "Leia a mensagem abaixo e devolva um resumo curto em portugues. "
                f"Mensagem: {texto}"
            ),
        },
    ]


def structured_prompt(texto: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "Voce e um analista de atendimento da Pathbit. Responda sempre em portugues.",
        },
        {
            "role": "user",
            "content": (
                "Analise a mensagem e responda EXATAMENTE com 3 linhas.\n"
                "resumo: <uma frase>\n"
                "prioridade: <alta|media|baixa>\n"
                "proxima_acao: <uma frase objetiva>\n"
                f"Mensagem: {texto}"
            ),
        },
    ]


def few_shot_prompt(texto: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "Voce e um analista de atendimento da Pathbit. Responda sempre em portugues.",
        },
        {
            "role": "user",
            "content": (
                "Aprenda com o exemplo abaixo e use o mesmo formato.\n\n"
                f"{FEW_SHOT_EXAMPLE}\n\n"
                "Agora analise a nova mensagem e responda EXATAMENTE com 3 linhas.\n"
                "resumo: <uma frase>\n"
                "prioridade: <alta|media|baixa>\n"
                "proxima_acao: <uma frase objetiva>\n"
                f"Mensagem: {texto}"
            ),
        },
    ]


def checklist_prompt(texto: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "Voce e um analista senior da Pathbit. Responda sempre em portugues.",
        },
        {
            "role": "user",
            "content": (
                f"{CHECKLIST_EXAMPLE}\n\n"
                "Use o checklist acima antes de responder.\n"
                "Retorne EXATAMENTE com 3 linhas.\n"
                "resumo: <uma frase>\n"
                "prioridade: <alta|media|baixa>\n"
                "proxima_acao: <uma frase objetiva>\n"
                f"Mensagem: {texto}"
            ),
        },
    ]


def messages_to_plain_prompt(messages: list[dict[str, str]]) -> str:
    return "\n\n".join(f"{message['role'].upper()}: {message['content']}" for message in messages)


def run_generation(generator, messages: list[dict[str, str]], max_new_tokens: int = 96) -> str:
    """Executa a geração respeitando o tipo de modelo.

    Alguns modelos gratuitos trabalham melhor com chat template.
    Outros exigem um prompt linear em estilo seq2seq.
    """
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


def extract_field(output: str, field_name: str) -> str:
    pattern = FIELD_PATTERNS[field_name]
    match = re.search(pattern, output, flags=re.MULTILINE | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def structure_score(output: str) -> float:
    found = sum(
        1
        for field in OUTPUT_FIELDS
        if re.search(FIELD_PATTERNS[field], output, flags=re.MULTILINE | re.IGNORECASE)
    )
    return found / len(OUTPUT_FIELDS)


def keyword_score(output: str, required_keywords: list[str]) -> float:
    output_l = output.lower()
    hits = sum(1 for keyword in required_keywords if keyword.lower() in output_l)
    return hits / len(required_keywords)


def priority_score(output: str, expected_priority: str) -> float:
    prioridade = re.sub(r"[^a-z]", "", extract_field(output, "prioridade").lower())
    return 1.0 if prioridade == expected_priority.lower() else 0.0


def semantic_score(embedder: SentenceTransformer, output: str, expected_summary: str) -> float:
    """Compara a semântica do resumo gerado com o resumo ideal."""
    resumo = extract_field(output, "resumo") or output
    vectors = embedder.encode([resumo, expected_summary], normalize_embeddings=True)
    return float(np.dot(vectors[0], vectors[1]))


def evaluate_output(
    output: str,
    row: pd.Series,
    embedder: SentenceTransformer,
) -> dict[str, float]:
    score_structure = structure_score(output)
    score_keywords = keyword_score(output, row["required_keywords"])
    score_priority = priority_score(output, row["expected_priority"])
    score_semantic = semantic_score(embedder, output, row["expected_summary"])
    score_total = float(
        np.mean([score_structure, score_keywords, score_priority, score_semantic])
    )
    return {
        "score_estrutura": score_structure,
        "score_keywords": score_keywords,
        "score_prioridade": score_priority,
        "score_semantico": score_semantic,
        "score_total": score_total,
    }


def list_missing_fields(output: str) -> str:
    """Lista quais campos obrigatórios não apareceram na resposta."""
    missing = [field for field in OUTPUT_FIELDS if not extract_field(output, field)]
    return ",".join(missing) if missing else ""


def build_delta_summary(summary: pd.DataFrame) -> pd.DataFrame:
    """Calcula o delta de cada estratégia contra a baseline dentro do mesmo modelo."""
    baselines = (
        summary[summary["estrategia"] == "base"][["modelo_geracao", "score_total"]]
        .rename(columns={"score_total": "base_score_total"})
    )
    delta = summary.merge(baselines, on="modelo_geracao", how="left")
    delta["delta_vs_base"] = delta["score_total"] - delta["base_score_total"]
    delta["delta_vs_base_pct"] = np.where(
        delta["base_score_total"] > 0,
        (delta["delta_vs_base"] / delta["base_score_total"]) * 100,
        0.0,
    )
    return delta.sort_values(["modelo_geracao", "score_total"], ascending=[True, False])


def build_case_breakdown(result: pd.DataFrame) -> pd.DataFrame:
    """Produz uma visão por caso para entender onde cada estratégia ainda erra."""
    breakdown = result.copy()
    breakdown["missing_fields"] = breakdown["saida"].apply(list_missing_fields)
    breakdown["strategy_description"] = breakdown["estrategia"].map(STRATEGY_DESCRIPTIONS)
    return breakdown[
        [
            "modelo_geracao",
            "caso",
            "estrategia",
            "strategy_description",
            "score_estrutura",
            "score_keywords",
            "score_prioridade",
            "score_semantico",
            "score_total",
            "missing_fields",
            "saida",
        ]
    ]


def save_markdown_report(base_dir: Path, delta_summary: pd.DataFrame) -> None:
    """Escreve um relatório executivo curto para leitura fora do notebook."""
    lines = ["# Relatório do Laboratório de Prompt Engineering", ""]
    for model_name in delta_summary["modelo_geracao"].drop_duplicates():
        block = delta_summary[delta_summary["modelo_geracao"] == model_name]
        winner = block.iloc[0]
        lines.append(f"## {model_name}")
        lines.append(f"- Melhor estratégia: `{winner['estrategia']}`")
        lines.append(f"- Score total: {winner['score_total']:.3f}")
        lines.append(f"- Delta vs base: {winner['delta_vs_base']:+.3f} pontos ({winner['delta_vs_base_pct']:+.1f}%)")
        lines.append("")
    (base_dir / "data" / "benchmark_relatorio.md").write_text("\n".join(lines), encoding="utf-8")


def run_benchmark(
    generation_models: list[str] | None = None,
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    limit: int | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    base_dir = Path(__file__).parent.parent
    df = load_dataset(base_dir)
    if limit is not None:
        df = df.head(limit)

    embedder = build_embedder(embedding_model)
    generation_models = generation_models or DEFAULT_GENERATION_MODELS

    strategies = {
        "base": generic_prompt,
        "estruturado": structured_prompt,
        "few_shot": few_shot_prompt,
        "checklist": checklist_prompt,
    }

    rows: list[dict[str, object]] = []
    generators = {model_name: build_generator(model_name) for model_name in generation_models}
    for model_name, generator in generators.items():
        for _, row in df.iterrows():
            for strategy_name, prompt_builder in strategies.items():
                messages = prompt_builder(row["input"])
                output = run_generation(generator, messages)
                scores = evaluate_output(output, row, embedder)
                rows.append(
                    {
                        "caso": row["id"],
                        "estrategia": strategy_name,
                        "modelo_geracao": model_name,
                        "modelo_embedding": embedding_model,
                        "input": row["input"],
                        "saida": output,
                        **scores,
                    }
                )

    result = pd.DataFrame(rows)
    summary = (
        result.groupby(["modelo_geracao", "estrategia"], as_index=False)[
            [
                "score_estrutura",
                "score_keywords",
                "score_prioridade",
                "score_semantico",
                "score_total",
            ]
        ]
        .mean()
        .sort_values("score_total", ascending=False)
    )
    delta_summary = build_delta_summary(summary)
    case_breakdown = build_case_breakdown(result)

    output_path = base_dir / "data" / "benchmark_resultados.csv"
    summary_path = base_dir / "data" / "benchmark_resumo.csv"
    delta_path = base_dir / "data" / "benchmark_deltas.csv"
    breakdown_path = base_dir / "data" / "benchmark_case_breakdown.csv"
    result.to_csv(output_path, index=False)
    summary.to_csv(summary_path, index=False)
    delta_summary.to_csv(delta_path, index=False)
    case_breakdown.to_csv(breakdown_path, index=False)
    save_markdown_report(base_dir, delta_summary)
    return result, summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Laboratorio de prompt engineering com modelos gratuitos")
    parser.add_argument(
        "--models",
        default=",".join(DEFAULT_GENERATION_MODELS),
        help="Lista de modelos gratuitos separados por virgula",
    )
    parser.add_argument("--embedding-model", default=DEFAULT_EMBEDDING_MODEL, help="Modelo gratuito de embedding do Hugging Face")
    parser.add_argument("--limit", type=int, default=None, help="Limita a quantidade de casos para testes rapidos")
    args = parser.parse_args()
    generation_models = [model.strip() for model in args.models.split(",") if model.strip()]

    result, summary = run_benchmark(
        generation_models=generation_models,
        embedding_model=args.embedding_model,
        limit=args.limit,
    )

    print("Modelos utilizados:")
    print(f"- Geracao: {', '.join(generation_models)}")
    print(f"- Embedding: {args.embedding_model}")
    print("\nResumo agregado:")
    print(summary.to_string(index=False))
    print("\nExemplo de saida:")
    preview = result[["modelo_geracao", "caso", "estrategia", "score_total", "saida"]].head(8)
    print(preview.to_string(index=False))


if __name__ == "__main__":
    main()
