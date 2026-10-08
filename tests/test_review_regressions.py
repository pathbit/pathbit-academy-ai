"""Regressões do gate, recuperação de JSON e imports em notebook."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


_MODULE_CACHE = {}


def load(module, path):
    if path in _MODULE_CACHE:
        return _MODULE_CACHE[path]
    spec = importlib.util.spec_from_file_location(module, ROOT / path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    _MODULE_CACHE[path] = result
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

    def test_mcp_tools_and_validation(self):
        mcp_module = load("mcp_server_review", "0010_mcp_local/src/mcp_server.py")
        self.assertIn("devolucao", mcp_module.POLITICAS)
        self.assertIn("Devolucao permitida", mcp_module.buscar_politica("devolucao"))
        self.assertIn("nao encontrada", mcp_module.buscar_politica("inexistente"))
        self.assertIn("prioridade invalida", mcp_module.criar_ticket("Ajuda", prioridade="urgente"))
        self.assertIn("ticket#2041 criado", mcp_module.criar_ticket("Problema no login", prioridade="alta"))
        self.assertIn("Cliente Maria", mcp_module.resumo_atendimento("Maria"))

    def test_agent_guardrail_blocking_sensitive_patterns(self):
        agent = load("agent_guardrail_review", "0007_agentes_tool_calling/src/agent_runner.py")
        ok, msg = agent.guardrail("minha senha de acesso é secreta")
        self.assertFalse(ok)
        self.assertIn("senha", msg)

        ok, msg = agent.guardrail("informe o token da api")
        self.assertFalse(ok)
        self.assertIn("token", msg)

        ok, msg = agent.guardrail("como consultar o status do meu servico?")
        self.assertTrue(ok)
        self.assertEqual(msg, "ok")

    def test_agent_business_rule_router_and_ticket_creation(self):
        agent = load("agent_router_review", "0007_agentes_tool_calling/src/agent_runner.py")
        route, reason = agent.business_rule_router("Gostaria de solicitar a segunda via do boleto")
        self.assertEqual(route, "buscar_politica")

        route, reason = agent.business_rule_router("Sistema apresentando erro 500 no checkout")
        self.assertEqual(route, "criar_ticket")

        route, reason = agent.business_rule_router("Qual a distancia entre a Terra e Marte?")
        self.assertIsNone(route)

        ticket_critico = agent.tool_criar_ticket("Erro 500 fatal")
        self.assertEqual(ticket_critico["prioridade"], "alta")
        self.assertIn("TCK-", ticket_critico["ticket_id"])
        self.assertEqual(ticket_critico["assunto"], "Erro 500 fatal")

        ticket_normal = agent.tool_criar_ticket("Duvida comercial")
        self.assertEqual(ticket_normal["prioridade"], "media")


if __name__ == "__main__":
    unittest.main()