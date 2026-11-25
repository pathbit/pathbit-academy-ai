import argparse
from collections import Counter
import json
from pathlib import Path

DEFAULT_FIXTURE = Path(__file__).resolve().parents[1] / "data" / "context.json"


def encode_context(documents):
    return json.dumps({"documents": documents}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def fit_context(candidates, byte_budget, per_source):
    if byte_budget < len(encode_context([])):
        raise ValueError("The byte budget must fit the empty document envelope")
    if per_source < 1:
        raise ValueError("The per-source limit must be positive")
    identifiers = {candidate["id"] for candidate in candidates}
    if len(identifiers) != len(candidates):
        raise ValueError("Candidate IDs must be unique")

    selected = []
    skipped = []
    source_counts = Counter()
    payload = encode_context(selected)
    for candidate in sorted(candidates, key=lambda item: (-item["score"], item["id"])):
        source = candidate["source"]
        chunk = {key: candidate[key] for key in ("id", "source", "text")}
        if source_counts[source] >= per_source:
            skipped.append({"id": chunk["id"], "reason": "source_limit"})
            continue

        trial = encode_context([*selected, chunk])
        if len(trial) > byte_budget:
            skipped.append({"id": chunk["id"], "reason": "byte_budget"})
            continue

        selected.append(chunk)
        source_counts[source] += 1
        payload = trial

    return {"byte_budget": byte_budget, "bytes_used": len(payload), "context": payload.decode("utf-8"), "skipped": skipped}


def main():
    parser = argparse.ArgumentParser(description="Fit ranked context into a UTF-8 JSON byte budget.")
    parser.add_argument("--input", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--bytes", type=int, default=245)
    parser.add_argument("--per-source", type=int, default=1)
    parser.add_argument("--output", type=Path, help="Save the report as UTF-8 JSON.")
    args = parser.parse_args()
    try:
        candidates = json.loads(args.input.read_text(encoding="utf-8"))
        report = fit_context(candidates, args.bytes, args.per_source)
        result = json.dumps(report, ensure_ascii=False, indent=2)
        if args.output:
            args.output.write_text(result + "\n", encoding="utf-8")
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))
    if not args.output:
        print(result)


if __name__ == "__main__":
    main()
