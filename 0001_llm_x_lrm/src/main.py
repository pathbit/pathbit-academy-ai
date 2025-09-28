#!/usr/bin/env python3
"""
Pathbit Academy AI - Artigo 0001: LLM vs LRM
============================================

Este script inicia o Jupyter Notebook localmente para execução
do comparativo entre LLM e LRM.

Requisitos:
- GROQ_API_KEY definida como variável de ambiente
- Dependências instaladas via requirements.txt

Uso:
    python main.py
"""

import subprocess
import sys
import os

from pathlib import Path

def verificar_dependencias():
    """
    Verifica se as dependências necessárias estão instaladas.
    """
    try:
        # Verificar se jupyter notebook está disponível
        result = subprocess.run(
            ['jupyter', '--version'],
            capture_output=True,
            text=True,
            timeout=5,
            check=False
        )
        if result.returncode == 0:
            print("✅ Dependências encontradas")
            return True
        else:
            print("❌ Jupyter não encontrado no PATH")
            return False
    except ImportError as e:
        print(f"❌ Dependência não encontrada: {e}")
        print("Execute: pip install -r requirements.txt")
        return False
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError) as e:
        print(f"❌ Erro ao verificar dependências: {e}")
        print("Execute: pip install -r requirements.txt")
        return False


def verificar_api_key():
    """
    Verifica se a API Key do Groq está configurada.
    """
    if not os.getenv("GROQ_API_KEY"):
        print("⚠️  GROQ_API_KEY não definida")
        print("Defina a variável de ambiente:")
        print("  export GROQ_API_KEY='sua_chave_aqui'")
        return False
    else:
        print("✅ GROQ_API_KEY configurada")
        return True


def iniciar_notebook():
    """
    Inicia o Jupyter Notebook com o arquivo de comparação.
    """
    # Caminho para o notebook
    notebook_path = Path(__file__).parent.parent / "notebooks" / "comparacao_llm_lrm.ipynb"

    if not notebook_path.exists():
        print(f"❌ Notebook não encontrado: {notebook_path}")
        return False

    print(f"🚀 Iniciando Jupyter Notebook: {notebook_path}")

    try:
        # Inicia o Jupyter Notebook
        subprocess.run([
            "jupyter", "notebook", str(notebook_path)
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao iniciar Jupyter: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Jupyter Notebook encerrado pelo usuário")
        return True


def main():
    """
    Função principal que inicia o notebook de comparação.
    """
    print("🚀 Pathbit Academy AI - Artigo 0001: LLM vs LRM")
    print("=" * 50)

    # Verificações iniciais
    if not verificar_dependencias():
        sys.exit(1)

    if not verificar_api_key():
        print("\n⚠️  Continuando sem API Key (algumas funcionalidades podem não funcionar)")

    print("\n📓 Iniciando notebook de comparação...")

    # Inicia o notebook
    if iniciar_notebook():
        print("✅ Notebook executado com sucesso!")
    else:
        print("❌ Falha ao executar notebook")
        sys.exit(1)


if __name__ == "__main__":
    main()
