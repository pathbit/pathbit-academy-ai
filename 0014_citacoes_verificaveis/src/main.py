import argparse
import json
from pathlib import Path

DEFAULT_FIXTURE = Path(__file__).resolve().parents[1] / "data" / "evidence.json"


def check_evidence(context, claims):
    evidence = {document["id"]: document["text"] for document in context}
    if len(evidence) != len(context):
        raise ValueError("Context document IDs must be unique")

    errors = []
    if not claims:
        errors.append({"reason": "no_claims"})
    for position, claim in enumerate(claims, start=1):
        if not claim["text"].strip():
            errors.append({"claim": position, "reason": "empty_claim"})
        if not claim["citations"]:
            errors.append({"claim": position, "reason": "missing_citation"})
        for citation in claim["citations"]:
            source_id = citation["source_id"]
            quote = citation["quote"]
            if source_id not in evidence:
                errors.append({"claim": position, "source_id": source_id, "reason": "unknown_source"})
            elif not quote.strip() or quote not in evidence[source_id]:
                errors.append({"claim": position, "source_id": source_id, "reason": "quote_not_found"})

    if errors:
        return {"status": "abstained", "claims": [], "errors": errors}
    return {"status": "citations_verified", "claims": claims, "errors": []}


def main():
    parser = argparse.ArgumentParser(description="Verify citations against the supplied context.")
    parser.add_argument("--input", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--context-report", type=Path, help="Read the document envelope from lab 0013.")
    parser.add_argument("--case", default="valid")
    args = parser.parse_args()
    try:
        fixture = json.loads(args.input.read_text(encoding="utf-8"))
        context = fixture["context"]
        if args.context_report:
            packed = json.loads(args.context_report.read_text(encoding="utf-8"))
            context = json.loads(packed["context"])
        report = check_evidence(context["documents"], fixture["cases"][args.case])
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
