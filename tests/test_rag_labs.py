import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
SEARCH = "0012_busca_hibrida"
CONTEXT = "0013_orcamento_contexto"
CITATIONS = "0014_citacoes_verificaveis"


def invoke(lab, *options):
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(ROOT / lab / "src" / "main.py"), *options],
        capture_output=True, text=True, encoding="utf-8", check=False,
    )


class RagLabsTest(unittest.TestCase):
    def read_report(self, lab, *options):
        completed = invoke(lab, *options)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return json.loads(completed.stdout)

    def test_rank_fusion_improves_one_lexical_result_and_loses_one_vector_result(self):
        password, reservation = self.read_report(SEARCH, "--top", "2")
        self.assertEqual(password["lexical"]["results"], ["reset-password"])
        self.assertEqual(password["hybrid"]["results"], ["reset-password", "access-code"])
        self.assertEqual(reservation["vector"]["results"], ["rain-policy", "weather-alert"])
        self.assertEqual(reservation["hybrid"]["recall_at_k"], 0.5)
        self.assertEqual(reservation["hybrid"]["reciprocal_rank_at_k"], 1.0)
        self.assertEqual(self.read_report(SEARCH, "--top", "3")[1]["hybrid"]["recall_at_k"], 1.0)

    def test_invalid_cutoff_is_rejected(self):
        completed = invoke(SEARCH, "--top", "4")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("Candidate depth", completed.stderr)

    def test_context_budget_accounts_for_utf8_and_continues_after_a_skip(self):
        packed = self.read_report(CONTEXT, "--bytes", "214")
        payload = packed["context"]
        self.assertGreater(len(payload.encode("utf-8")), len(payload))
        self.assertEqual(len(payload.encode("utf-8")), packed["bytes_used"])
        self.assertEqual(packed["bytes_used"], packed["byte_budget"])
        self.assertEqual(
            [item["id"] for item in json.loads(payload)["documents"]],
            ["refund-summary", "refund-window"],
        )
        self.assertEqual(packed["skipped"], [
            {"id": "refund-history", "reason": "source_limit"},
            {"id": "policy-appendix", "reason": "byte_budget"},
        ])
        smaller = self.read_report(CONTEXT, "--bytes", "213")
        self.assertEqual(
            [item["id"] for item in json.loads(smaller["context"])["documents"]],
            ["refund-summary"],
        )

    def test_context_budget_below_empty_envelope_is_rejected(self):
        completed = invoke(CONTEXT, "--bytes", "15")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("empty document envelope", completed.stderr)

    def test_bad_citations_are_withheld_and_semantic_entailment_is_outside_the_check(self):
        for fixture, reason in [
            ("altered-quote", "quote_not_found"),
            ("unknown-source", "unknown_source"),
        ]:
            with self.subTest(fixture=fixture):
                report = self.read_report(CITATIONS, "--case", fixture)
                self.assertEqual(report["status"], "abstained")
                self.assertEqual(report["claims"], [])
                self.assertEqual(report["errors"][0]["reason"], reason)
        for fixture in ("valid", "unsupported-claim"):
            with self.subTest(fixture=fixture):
                report = self.read_report(CITATIONS, "--case", fixture)
                self.assertEqual(report["status"], "citations_verified")

    def test_citations_only_use_actual_packed_context(self):
        with TemporaryDirectory() as directory:
            report_path = str(Path(directory) / "context-report.json")
            packed = invoke(CONTEXT, "--bytes", "245", "--output", report_path)
            self.assertEqual(packed.returncode, 0, packed.stderr)
            self.assertEqual(packed.stdout, "")
            accepted = self.read_report(CITATIONS, "--context-report", report_path)
            self.assertEqual(accepted["status"], "citations_verified")

            packed = invoke(CONTEXT, "--bytes", "16", "--output", report_path)
            self.assertEqual(packed.returncode, 0, packed.stderr)
            rejected = self.read_report(CITATIONS, "--context-report", report_path)
            self.assertEqual(rejected["status"], "abstained")
            self.assertEqual(rejected["errors"][0]["reason"], "unknown_source")
