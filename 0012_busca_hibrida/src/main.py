import argparse
import json
import math
from pathlib import Path
import re

DEFAULT_DATASET = Path(__file__).resolve().parents[1] / "data" / "search.json"


def terms(text):
    return set(re.findall(r"\w+", text.casefold()))


def cosine_similarity(left, right):
    numerator = sum(a * b for a, b in zip(left, right, strict=True))
    denominator = math.hypot(*left) * math.hypot(*right)
    return numerator / denominator if denominator else 0.0


def top_matches(scores, limit):
    ranked = sorted(scores, key=lambda match: (-match[1], match[0]))
    return [document_id for document_id, score in ranked if score > 0][:limit]


def reciprocal_rank_fusion(rankings, constant=60):
    scores = {}
    for ranking in rankings:
        for position, document_id in enumerate(ranking, start=1):
            scores[document_id] = scores.get(document_id, 0.0) + 1 / (constant + position)
    return sorted(scores, key=lambda document_id: (-scores[document_id], document_id))


def assess(ranking, relevant, top):
    selected = ranking[:top]
    hits = set(selected) & relevant
    first_hit = next((position for position, item in enumerate(selected, start=1) if item in relevant), None)
    return {
        "results": selected,
        "recall_at_k": len(hits) / len(relevant),
        "reciprocal_rank_at_k": 1 / first_hit if first_hit else 0.0,
    }


def run_search(dataset, top):
    documents = dataset["documents"]
    depth = dataset["candidate_depth"]
    if depth < top:
        raise ValueError("Candidate depth must be at least the requested top K")
    document_ids = {document["id"] for document in documents}
    if len(document_ids) != len(documents):
        raise ValueError("Document IDs must be unique")

    reports = []
    for query in dataset["queries"]:
        relevant = set(query["relevant"])
        if not relevant or not relevant <= document_ids:
            raise ValueError("Each query needs at least one known relevant document")
        query_terms = terms(query["text"])
        lexical = top_matches(
            ((document["id"], len(terms(document["text"]) & query_terms)) for document in documents),
            depth,
        )
        vector = top_matches(
            ((document["id"], cosine_similarity(document["vector"], query["vector"])) for document in documents),
            depth,
        )
        fused = reciprocal_rank_fusion((lexical, vector))
        reports.append({
            "query": query["text"],
            "lexical": assess(lexical, relevant, top),
            "vector": assess(vector, relevant, top),
            "hybrid": assess(fused, relevant, top),
        })
    return reports


def main():
    parser = argparse.ArgumentParser(description="Compare lexical, vector and fused rankings.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--top", type=int, default=2)
    args = parser.parse_args()
    if args.top < 1:
        parser.error("--top must be positive")
    try:
        dataset = json.loads(args.dataset.read_text(encoding="utf-8"))
        reports = run_search(dataset, args.top)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))
    print(json.dumps(reports, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
