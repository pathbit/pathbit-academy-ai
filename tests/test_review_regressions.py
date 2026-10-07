"""Regressões do gate, recuperação de JSON e imports em notebook."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def load(module, path):
    spec = importlib.util.spec_from_file_location(module, ROOT / path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class ReviewRegressions(unittest.TestCase):
    def test_gate_ignores_regression_of_rejected_candidate(self):
        runner = load("eval_review", "0006_llm_evals_regressao/src/eval_runner.py")
        summary = pd.DataFrame([{"candidate": "vencedor", "score_ponderado": 1.0},
                                {"candidate": "qwen_generico", "score_ponderado": 0.7}])
        regressions = pd.DataFrame([{"candidate": "outro", "criticidade": "alta"}])
        gain, critical, gate = runner.evaluate_release_gate(summary, regressions)
        self.assertAlmostEqual(gain, 0.3)
        self.assertTrue(critical.empty)
        self.assertEqual(gate, "aprovado")
        regressions.loc[0, "candidate"] = "vencedor"
        self.assertEqual(runner.evaluate_release_gate(summary, regressions)[2], "reprovado")

    def test_success_without_retry_has_recovery_false(self):
        runner = load("structured_review", "0009_saida_estruturada/src/structured_lab.py")
        task = {"id": "test", "prompt": "test", "schema": {"type": "object"}, "semantico": lambda value: True}
        with patch.object(runner, "gerar", return_value={"resposta": "{}", "total_ms": 1, "tokens": 2}):
            row = runner.run_task_case("http://localhost", "model", task, "schema")
        self.assertIs(row["recuperado"], False)
        self.assertEqual(row["tentativa"], 1)

    def test_notebook_import_does_not_force_agg(self):
        import matplotlib
        matplotlib.use("module://matplotlib_inline.backend_inline")
        for name, path in [("ollama_review", "0008_llms_locais_ollama/src/ollama_lab.py"),
                           ("mcp_review", "0010_mcp_local/src/mcp_lab.py")]:
            load(name, path)
            self.assertIn("matplotlib_inline", matplotlib.get_backend())

    def test_retry_accumulates_tokens_and_latency(self):
        runner = load("retry_review", "0009_saida_estruturada/src/structured_lab.py")
        rows = [dict(parse_ok=False, schema_ok=False, total_ms=3, tokens=4),
                dict(parse_ok=True, schema_ok=True, total_ms=5, tokens=6)]
        result = runner._linha_consolidada(rows)
        self.assertEqual(result["tokens"], 10)
        self.assertEqual(result["total_ms"], 8)
        self.assertTrue(result["recuperado"])

    def test_planner_rejects_non_string_arguments(self):
        runner = load("agent_review", "0007_agentes_tool_calling/src/agent_runner.py")
        self.assertIsNone(runner.parse_plan('{"tool":"x","argument":{},"reason":"x"}'))
        self.assertEqual(runner.parse_plan('{"tool":"x","argument":"ok","reason":"x"}')["argument"], "ok")


if __name__ == "__main__":
    unittest.main()