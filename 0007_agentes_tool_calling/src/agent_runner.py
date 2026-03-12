#!/usr/bin/env python3
"""Agente local com planejamento, tools, retrieval e trilha de auditoria.

Objetivos deste runner:
1. mostrar um fluxo híbrido entre regra de negócio, planner e fallback
2. registrar evidências suficientes para auditoria de cada execução
3. gerar artefatos que permitam inspecionar decisão, retrieval e resposta final
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

DEFAULT_EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
DEFAULT_GENERATION_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"


def guardrail(texto: str) -> tuple[bool, str]:
    bloqueios = ["senha", "token", "cartao", "cpf completo", "pix", "segredo"]
    for bloqueio in bloqueios:
        if bloqueio in texto.lower():
            return False, f"Solicitacao bloqueada por seguranca: '{bloqueio}'"
    return True, "ok"


def business_rule_router(texto: str) -> tuple[str | None, str]:
    """Captura intenções óbvias antes de gastar inferência no planner."""
    texto_l = texto.lower()
    if any(keyword in texto_l for keyword in ["fatura", "segunda via", "boleto", "devolucao", "cancelamento"]):
        return "buscar_politica", "roteamento deterministico por regra de negocio"
    if any(keyword in texto_l for keyword in ["erro 500", "nao funciona", "indisponibilidade", "app"]):
        return "criar_ticket", "roteamento deterministico para incidente tecnico"
    return None, ""


def build_embedder(model_name: str) -> SentenceTransformer:
    """Cria o modelo de embeddings usado para retrieval e fallback."""
    return SentenceTransformer(model_name)


def build_generator(model_name: str):
    """Cria o modelo gerador/planner compatível com o backend atual."""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if "t5" in model_name.lower():
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        mode = "seq2seq"
    else:
        model = AutoModelForCausalLM.from_pretrained(model_name)
        mode = "chat"
    return {"tokenizer": tokenizer, "model": model, "mode": mode, "model_name": model_name}


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))


def retrieve_policy(query: str, embedder: SentenceTransformer, knowledge_base: list[dict[str, str]]) -> tuple[dict[str, str], float]:
    """Recupera o documento mais próximo semanticamente da consulta."""
    documents = [entry["conteudo"] for entry in knowledge_base]
    vectors = embedder.encode([query, *documents], normalize_embeddings=True)
    query_vector = vectors[0]
    document_vectors = vectors[1:]
    scores = [cosine_similarity(query_vector, vector) for vector in document_vectors]
    best_index = int(np.argmax(scores))
    return knowledge_base[best_index], float(scores[best_index])


def tool_criar_ticket(assunto: str) -> dict[str, str]:
    """Simula abertura de ticket e devolve um payload observável."""
    prioridade = "alta" if "erro 500" in assunto.lower() or "indisponibilidade" in assunto.lower() else "media"
    ticket_id = f"TCK-{abs(hash(assunto)) % 100000:05d}"
    return {
        "ticket_id": ticket_id,
        "prioridade": prioridade,
        "assunto": assunto,
    }


def route_with_embeddings(query: str, embedder: SentenceTransformer, tools: list[dict[str, str]]) -> tuple[str, float]:
    """Escolhe uma tool por similaridade entre a consulta e a descrição das ferramentas."""
    labels = [tool["name"] for tool in tools]
    descriptions = [tool["description"] for tool in tools]
    vectors = embedder.encode([query, *descriptions], normalize_embeddings=True)
    query_vector = vectors[0]
    tool_vectors = vectors[1:]
    scores = [cosine_similarity(query_vector, vector) for vector in tool_vectors]
    best_index = int(np.argmax(scores))
    return labels[best_index], float(scores[best_index])


def planner_prompt(entrada: str, tools: list[dict[str, str]]) -> list[dict[str, str]]:
    tool_lines = "\n".join(
        f"- {tool['name']}: {tool['description']} | argumento: {tool['argument_name']}"
        for tool in tools
    )
    return [
        {
            "role": "system",
            "content": "Voce e um planner de agente. Responda apenas com JSON valido.",
        },
        {
            "role": "user",
            "content": (
                "Escolha a melhor tool para a solicitacao abaixo.\n"
                "Tools disponiveis:\n"
                f"{tool_lines}\n\n"
                f"Solicitacao: {entrada}\n"
                'Retorne EXATAMENTE um JSON com as chaves "tool", "argument" e "reason".'
            ),
        },
    ]


def messages_to_plain_prompt(messages: list[dict[str, str]]) -> str:
    return "\n\n".join(f"{message['role'].upper()}: {message['content']}" for message in messages)


def generate_text(generator, messages: list[dict[str, str]], max_new_tokens: int = 120) -> str:
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


def parse_plan(raw_text: str) -> dict[str, str] | None:
    """Extrai o JSON do planner e valida o schema mínimo esperado."""
    match = re.search(r"\{.*\}", raw_text, flags=re.DOTALL)
    if not match:
        return None
    try:
        plan = json.loads(match.group(0))
        if {"tool", "argument", "reason"}.issubset(plan.keys()):
            return {
                "tool": str(plan["tool"]),
                "argument": str(plan["argument"]),
                "reason": str(plan["reason"]),
            }
    except json.JSONDecodeError:
        return None
    return None


def generate_user_answer(generator, entrada: str, action: str, tool_result: str) -> str:
    """Transforma o resultado bruto da ferramenta em resposta final ao usuário."""
    messages = [
        {
            "role": "system",
            "content": "Voce e um assistente de suporte da Pathbit. Responda sempre em portugues claro e objetivo.",
        },
        {
            "role": "user",
            "content": (
                f"Pergunta do usuario: {entrada}\n"
                f"Acao tomada: {action}\n"
                f"Resultado da ferramenta: {tool_result}\n"
                "Responda em no maximo 2 frases."
            ),
        },
    ]
    return generate_text(generator, messages, max_new_tokens=96)


def build_decision_summary(result: pd.DataFrame) -> pd.DataFrame:
    """Resume quantas vezes cada fonte de decisão foi usada."""
    return (
        result.groupby(["decision_source", "acao"], as_index=False)
        .agg(total=("acao", "count"), taxa_acerto=("acertou_roteamento", "mean"))
        .sort_values(["decision_source", "total"], ascending=[True, False])
    )


def build_retrieval_summary(result: pd.DataFrame) -> pd.DataFrame:
    """Extrai a parte de retrieval para análise separada."""
    retrieval = result[result["acao"] == "buscar_politica"].copy()
    if retrieval.empty:
        return retrieval
    return retrieval[
        [
            "entrada",
            "planned_tool",
            "acao",
            "documento",
            "knowledge_score",
            "decision_source",
            "resposta",
        ]
    ]


def run_agent(
    generation_model: str = DEFAULT_GENERATION_MODEL,
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    limit: int | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    base_dir = Path(__file__).parent.parent
    scenario_path = base_dir / "data" / "cenarios.json"
    kb_path = base_dir / "data" / "knowledge_base.json"
    tools_path = base_dir / "data" / "tool_registry.json"
    audit_path = base_dir / "data" / "agent_audit_log.jsonl"
    decision_summary_path = base_dir / "data" / "decision_summary.csv"
    retrieval_summary_path = base_dir / "data" / "retrieval_summary.csv"

    scenarios = json.loads(scenario_path.read_text(encoding="utf-8"))
    if limit is not None:
        scenarios = scenarios[:limit]
    knowledge_base = json.loads(kb_path.read_text(encoding="utf-8"))
    tools = json.loads(tools_path.read_text(encoding="utf-8"))

    embedder = build_embedder(embedding_model)
    generator = build_generator(generation_model)

    audit_lines: list[str] = []
    rows: list[dict[str, object]] = []
    for scenario in scenarios:
        entrada = scenario["entrada"]
        expected_action = scenario["expected_action"]
        audit = []

        allowed, reason = guardrail(entrada)
        audit.append({"step": "guardrail", "allowed": allowed, "detail": reason})
        if not allowed:
            row = {
                "entrada": entrada,
                "expected_action": expected_action,
                "planned_tool": "bloqueado",
                "acao": "bloqueado",
                "status": "bloqueado",
                "router_score": 1.0,
                "knowledge_score": 0.0,
                "documento": "",
                "used_fallback": False,
                "plan_reason": reason,
                "resposta": reason,
                "acertou_roteamento": expected_action == "bloqueado",
                "audit_steps": json.dumps(audit, ensure_ascii=False),
            }
            rows.append(row)
            audit_lines.append(json.dumps(row, ensure_ascii=False))
            continue

        rule_tool, rule_reason = business_rule_router(entrada)
        if rule_tool is not None:
            router_tool, router_score = route_with_embeddings(entrada, embedder, tools)
            parsed_plan = {
                "tool": rule_tool,
                "argument": entrada,
                "reason": rule_reason,
            }
            used_fallback = False
            decision_source = "business_rule"
            audit.append(
                {
                    "step": "business_rule",
                    "rule_tool": rule_tool,
                    "rule_reason": rule_reason,
                    "router_tool": router_tool,
                    "router_score": router_score,
                }
            )
        else:
            raw_plan = generate_text(generator, planner_prompt(entrada, tools), max_new_tokens=120)
            parsed_plan = parse_plan(raw_plan)
            router_tool, router_score = route_with_embeddings(entrada, embedder, tools)
            used_fallback = False
            decision_source = "planner"
            if parsed_plan is None:
                parsed_plan = {
                    "tool": router_tool,
                    "argument": entrada,
                    "reason": "fallback por embeddings",
                }
                used_fallback = True
                decision_source = "router_fallback"
            else:
                if parsed_plan["tool"] != router_tool and router_score >= 0.50:
                    parsed_plan = {
                        "tool": router_tool,
                        "argument": entrada,
                        "reason": f"router semantico sobrescreveu planner ({parsed_plan['tool']})",
                    }
                    used_fallback = True
                    decision_source = "router_override"

            audit.append(
                {
                    "step": "planner",
                    "raw_plan": raw_plan,
                    "parsed_tool": parsed_plan["tool"],
                    "parsed_argument": parsed_plan["argument"],
                    "used_fallback": used_fallback,
                    "router_tool": router_tool,
                    "router_score": router_score,
                    "decision_source": decision_source,
                }
            )

        action = parsed_plan["tool"]
        tool_result = ""
        knowledge_score = 0.0
        document_title = ""

        if action == "buscar_politica":
            document, knowledge_score = retrieve_policy(parsed_plan["argument"], embedder, knowledge_base)
            document_title = document["titulo"]
            tool_result = document["conteudo"]
            audit.append(
                {
                    "step": "tool_execution",
                    "tool": action,
                    "documento": document_title,
                    "knowledge_score": knowledge_score,
                }
            )
        elif action == "criar_ticket":
            ticket = tool_criar_ticket(parsed_plan["argument"])
            tool_result = (
                f"Ticket {ticket['ticket_id']} criado com prioridade {ticket['prioridade']} para o assunto: {ticket['assunto']}"
            )
            audit.append({"step": "tool_execution", "tool": action, "ticket_id": ticket["ticket_id"]})
        else:
            tool_result = knowledge_base[-1]["conteudo"]
            action = "resposta_direta"
            audit.append({"step": "tool_execution", "tool": action})

        resposta = generate_user_answer(generator, entrada, action, tool_result)
        audit.append({"step": "final_response", "response_preview": resposta[:160]})

        row = {
            "entrada": entrada,
            "expected_action": expected_action,
            "planned_tool": parsed_plan["tool"],
            "acao": action,
            "status": "ok",
            "router_score": router_score,
            "knowledge_score": knowledge_score,
            "documento": document_title,
            "used_fallback": used_fallback,
            "decision_source": decision_source,
            "plan_reason": parsed_plan["reason"],
            "resposta": resposta,
            "acertou_roteamento": expected_action == action,
            "audit_steps": json.dumps(audit, ensure_ascii=False),
        }
        rows.append(row)
        audit_lines.append(json.dumps(row, ensure_ascii=False))

    result = pd.DataFrame(rows)
    summary = result.groupby("acao", as_index=False).agg(
        total=("acao", "count"),
        router_score_medio=("router_score", "mean"),
        taxa_acerto=("acertou_roteamento", "mean"),
    )
    decision_summary = build_decision_summary(result)
    retrieval_summary = build_retrieval_summary(result)

    output_csv = base_dir / "data" / "agent_runs.csv"
    output_csv.write_text(result.to_csv(index=False), encoding="utf-8")
    audit_path.write_text("\n".join(audit_lines), encoding="utf-8")
    decision_summary.to_csv(decision_summary_path, index=False)
    retrieval_summary.to_csv(retrieval_summary_path, index=False)
    return result, summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Agente local com planejamento, retrieval e tools")
    parser.add_argument("--model", default=DEFAULT_GENERATION_MODEL, help="Modelo de geração do Hugging Face")
    parser.add_argument("--embedding-model", default=DEFAULT_EMBEDDING_MODEL, help="Modelo de embedding do Hugging Face")
    parser.add_argument("--limit", type=int, default=None, help="Limita os cenários executados")
    args = parser.parse_args()

    result, summary = run_agent(
        generation_model=args.model,
        embedding_model=args.embedding_model,
        limit=args.limit,
    )

    print("Modelos utilizados:")
    print(f"- Geracao e planejamento: {args.model}")
    print(f"- Embedding e retrieval: {args.embedding_model}")
    print("\nResumo por acao:")
    print(summary.to_string(index=False))
    print("\nCenarios executados:")
    print(
        result[
            [
                "entrada",
                "planned_tool",
                "acao",
                "used_fallback",
                "documento",
                "resposta",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
