"""Percursos do artigo 0011 com processos separados e um banco real."""

from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest


CLI = Path(__file__).resolve().parents[1] / "0011_aprovacao_idempotencia" / "src/main.py"


class ApprovalLab(unittest.TestCase):
    def setUp(self):
        ambiente = tempfile.TemporaryDirectory()
        self.addCleanup(ambiente.cleanup)
        self.base = Path(ambiente.name) / "lab.sqlite"

    def executar_cli(self, *args, sucesso=True):
        retorno = subprocess.run(
            [sys.executable, str(CLI), "--base", str(self.base), *args],
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(retorno.returncode, 0 if sucesso else 1, retorno.stderr)
        return json.loads(retorno.stdout) if sucesso else retorno.stderr

    def test_proposta_aprovada_e_repeticao_concorrente(self):
        self.executar_cli("propor", " chave-1 ", "--titulo", "Problema de entrega")
        self.assertIn("exige uma proposta aprovada", self.executar_cli("executar", "chave-1", sucesso=False))
        self.assertEqual(self.executar_cli("consultar", "chave-1")["estado"], "pendente")
        comando = ("decidir", " chave-1 ", "aprovar", "--operador", "plantao")
        self.assertEqual(self.executar_cli(*comando), self.executar_cli(*comando))

        with ThreadPoolExecutor(max_workers=6) as pool:
            respostas = list(pool.map(lambda _: self.executar_cli("executar", " chave-1 "), range(6)))

        self.assertEqual(respostas, [respostas[0]] * len(respostas))
        self.assertEqual(respostas[0]["estado"], "executada")
        self.assertIsInstance(respostas[0]["chamado"], int)
        with closing(sqlite3.connect(self.base)) as banco:
            self.assertEqual(banco.execute("SELECT COUNT(*) FROM chamados").fetchone(), (1,))
        self.assertEqual(respostas[0], self.executar_cli("consultar", "chave-1"))

    def test_recusa_decisao_conflitante_e_reuso_da_chave(self):
        self.executar_cli("propor", "chave-2", "--titulo", "Solicitação original")
        self.executar_cli("decidir", "chave-2", "rejeitar", "--operador", "plantao")
        self.assertIn(
            "decisão registrada",
            self.executar_cli("decidir", "chave-2", "aprovar", "--operador", "plantao", sucesso=False),
        )
        self.assertIn(
            "proposta diferente",
            self.executar_cli("propor", "chave-2", "--titulo", "Outra solicitação", sucesso=False),
        )
        self.assertIn("exige uma proposta aprovada", self.executar_cli("executar", "chave-2", sucesso=False))
        proposta = self.executar_cli("consultar", "chave-2")
        self.assertEqual(proposta["titulo"], "Solicitação original")
        self.assertEqual(proposta["estado"], "rejeitada")
        self.assertIsNone(proposta["chamado"])
