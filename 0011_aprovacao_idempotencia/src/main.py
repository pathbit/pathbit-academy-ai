#!/usr/bin/env python3
"""Laboratório de aprovação humana e idempotência com um banco SQLite local."""

import argparse
from contextlib import closing, contextmanager
import json
from pathlib import Path
import sqlite3
import sys


SCHEMA = """
CREATE TABLE IF NOT EXISTS propostas (
    pedido TEXT PRIMARY KEY NOT NULL,
    titulo TEXT NOT NULL,
    prioridade TEXT NOT NULL CHECK (prioridade IN ('baixa', 'media', 'alta')),
    decisao TEXT CHECK (decisao IN ('aprovar', 'rejeitar')),
    operador TEXT,
    CHECK ((decisao IS NULL AND operador IS NULL) OR
           (decisao IS NOT NULL AND operador IS NOT NULL))
);
CREATE TABLE IF NOT EXISTS chamados (
    id INTEGER PRIMARY KEY,
    pedido TEXT NOT NULL UNIQUE REFERENCES propostas(pedido)
);
"""


class ErroDoLaboratorio(ValueError):
    """Operação incompatível com o contrato do laboratório."""


def texto_obrigatorio(texto: str, campo: str) -> str:
    valor = texto.strip()
    if not valor:
        raise ErroDoLaboratorio(f"Informe {campo}.")
    return valor


@contextmanager
def transacao(base: Path):
    with closing(sqlite3.connect(base, timeout=10)) as banco:
        banco.row_factory = sqlite3.Row
        banco.execute("PRAGMA foreign_keys = ON")
        banco.executescript(SCHEMA)
        with banco:
            banco.execute("BEGIN IMMEDIATE")
            yield banco


def consultar(banco: sqlite3.Connection, pedido: str) -> dict:
    pedido = texto_obrigatorio(pedido, "o identificador do pedido")
    linha = banco.execute(
        """
        SELECT p.pedido, p.titulo, p.prioridade, p.decisao, p.operador, c.id AS chamado
        FROM propostas p LEFT JOIN chamados c ON c.pedido = p.pedido
        WHERE p.pedido = ?
        """,
        (pedido,),
    ).fetchone()
    if linha is None:
        raise ErroDoLaboratorio("Proposta não encontrada.")
    resultado = dict(linha)
    if resultado["chamado"] is not None:
        estado = "executada"
    else:
        estado = {"aprovar": "aprovada", "rejeitar": "rejeitada", None: "pendente"}[linha["decisao"]]
    return {**resultado, "estado": estado}


def propor(base: Path, pedido: str, titulo: str, prioridade: str) -> dict:
    pedido = texto_obrigatorio(pedido, "o identificador do pedido")
    titulo = texto_obrigatorio(titulo, "o título")
    if prioridade not in {"baixa", "media", "alta"}:
        raise ErroDoLaboratorio("Prioridade inválida.")
    with transacao(base) as banco:
        banco.execute(
            """
            INSERT INTO propostas (pedido, titulo, prioridade) VALUES (?, ?, ?)
            ON CONFLICT(pedido) DO NOTHING
            """,
            (pedido, titulo, prioridade),
        )
        resultado = consultar(banco, pedido)
        if (resultado["titulo"], resultado["prioridade"]) != (titulo, prioridade):
            raise ErroDoLaboratorio("O identificador já pertence a uma proposta diferente.")
        return resultado


def decidir(base: Path, pedido: str, decisao: str, operador: str) -> dict:
    operador = texto_obrigatorio(operador, "o operador")
    if decisao not in {"aprovar", "rejeitar"}:
        raise ErroDoLaboratorio("Decisão inválida.")
    with transacao(base) as banco:
        anterior = consultar(banco, pedido)
        if anterior["decisao"] is None:
            banco.execute(
                "UPDATE propostas SET decisao = ?, operador = ? WHERE pedido = ?",
                (decisao, operador, anterior["pedido"]),
            )
        elif (anterior["decisao"], anterior["operador"]) != (decisao, operador):
            raise ErroDoLaboratorio("A proposta já tem uma decisão registrada.")
        return consultar(banco, pedido)


def executar(base: Path, pedido: str) -> dict:
    with transacao(base) as banco:
        anterior = consultar(banco, pedido)
        if anterior["decisao"] != "aprovar":
            raise ErroDoLaboratorio("A execução exige uma proposta aprovada.")
        banco.execute(
            "INSERT INTO chamados (pedido) VALUES (?) ON CONFLICT(pedido) DO NOTHING",
            (anterior["pedido"],),
        )
        return consultar(banco, pedido)


def consultar_proposta(base: Path, pedido: str) -> dict:
    with transacao(base) as banco:
        return consultar(banco, pedido)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True, help="Arquivo SQLite do laboratório.")
    comandos = parser.add_subparsers(dest="comando", required=True)
    criar = comandos.add_parser("propor", help="Registra o efeito proposto.")
    criar.add_argument("pedido")
    criar.add_argument("--titulo", required=True)
    criar.add_argument("--prioridade", choices=("baixa", "media", "alta"), default="media")
    revisao = comandos.add_parser("decidir", help="Registra a decisão do operador.")
    revisao.add_argument("pedido")
    revisao.add_argument("decisao", choices=("aprovar", "rejeitar"))
    revisao.add_argument("--operador", required=True)
    comandos.add_parser("executar", help="Cria o chamado aprovado.").add_argument("pedido")
    comandos.add_parser("consultar", help="Consulta a proposta e o chamado.").add_argument("pedido")
    args = parser.parse_args()

    try:
        if args.comando == "propor":
            resultado = propor(args.base, args.pedido, args.titulo, args.prioridade)
        elif args.comando == "decidir":
            resultado = decidir(args.base, args.pedido, args.decisao, args.operador)
        elif args.comando == "executar":
            resultado = executar(args.base, args.pedido)
        else:
            resultado = consultar_proposta(args.base, args.pedido)
    except (ErroDoLaboratorio, sqlite3.Error) as erro:
        print(str(erro), file=sys.stderr)
        return 1
    print(json.dumps(resultado, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
