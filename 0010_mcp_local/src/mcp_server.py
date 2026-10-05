#!/usr/bin/env python3
"""Servidor MCP local que expoe as tools de suporte do artigo 0007.

Transporte stdio: o cliente inicia este processo e conversa por stdin/stdout.
Nenhuma rede, nenhuma conta, nenhuma chave - o protocolo inteiro roda na maquina.
"""

from __future__ import annotations

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("pathbit-suporte")

POLITICAS: dict[str, str] = {
    "devolucao": "Devolucao permitida em ate 30 dias corridos para produtos sem uso e com embalagem preservada.",
    "cancelamento": "Cancelamento sem multa pode ser solicitado em ate 7 dias corridos apos a contratacao.",
    "segunda_via": "A segunda via da fatura e emitida no portal do cliente, aba Financeiro, opcao Segunda Via.",
    "prazos": "Prazo de resposta do suporte: 1 dia util para prioridade media e 4 horas para prioridade alta.",
    "seguranca": "Nunca compartilhe senha, token ou dados de cartao com atendentes ou com o assistente.",
}


@mcp.tool()
def buscar_politica(topico: str) -> str:
    """Busca uma politica interna da empresa pelo topico (devolucao, cancelamento, segunda_via, prazos, seguranca)."""
    return POLITICAS.get(topico.lower().replace(" ", "_"), f"Politica '{topico}' nao encontrada.")


@mcp.tool()
def criar_ticket(titulo: str, prioridade: str = "media") -> str:
    """Abre um ticket de suporte tecnico. Prioridades aceitas: baixa, media, alta."""
    if prioridade not in ("baixa", "media", "alta"):
        return f"ticket nao criado: prioridade invalida '{prioridade}'"
    return f"ticket#2041 criado com sucesso: '{titulo}' (prioridade {prioridade})"


@mcp.tool()
def resumo_atendimento(nome_cliente: str) -> str:
    """Resume o historico de atendimento de um cliente pelo nome."""
    return f"Cliente {nome_cliente}: 2 atendimentos anteriores, nenhum incidente aberto, plano ativo."


if __name__ == "__main__":
    mcp.run()
