#!/usr/bin/env python3
"""
Pathbit Academy AI - Artigo 0004: RAG vs Fine-Tuning
====================================================

Este script inicia o Jupyter Notebook localmente para execução
dos exemplos de RAG vs Fine-Tuning.

NOTA: Este notebook foi otimizado para Google Colab e contém
tudo que você precisa - sem arquivos externos!

Requisitos:
- GROQ_API_KEY definida como variável de ambiente (opcional)
- Dependências instaladas via requirements.txt

Uso:
    python main.py

DICA: Para usar no Google Colab, acesse:
    https://colab.research.google.com/github/pathbit/pathbit-academy-ai/blob/master/0004_rag_vs_finetuning/notebooks/rag_vs_finetuning.ipynb
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
        # Aumentado timeout para evitar problemas em sistemas mais lentos
        result = subprocess.run(
            ["jupyter", "--version"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        if result.returncode == 0:
            print("✅ Jupyter Notebook encontrado")
            return True
        else:
            print("❌ Jupyter não encontrado no PATH")
            print("💡 Execute: pip install -r requirements.txt")
            return False
    except subprocess.TimeoutExpired:
        print("⚠️  Verificação de Jupyter demorou muito, mas continuando...")
        print("💡 Se der erro, execute: pip install -r requirements.txt")
        return True  # Continuar mesmo assim
    except ImportError as e:
        print(f"❌ Dependência não encontrada: {e}")
        print("💡 Execute: pip install -r requirements.txt")
        return False
    except (subprocess.SubprocessError, OSError, FileNotFoundError) as e:
        print(f"❌ Erro ao verificar dependências: {e}")
        print("💡 Execute: pip install -r requirements.txt")
        return False


def verificar_api_keys():
    """
    Verifica se as API Keys estão configuradas.
    """
    groq_key = os.getenv("GROQ_API_KEY")

    if not groq_key:
        print(
            "⚠️  GROQ_API_KEY não definida (opcional - alguns exemplos funcionam sem ela)"
        )
    else:
        print("✅ GROQ_API_KEY configurada")

    print("✅ Hugging Face funciona sem API Key para modelos públicos")
    return True


def iniciar_notebook():
    """
    Inicia o Jupyter Notebook com o arquivo de RAG vs Fine-Tuning.
    """
    # Caminho para o notebook
    notebook_path = (
        Path(__file__).parent.parent / "notebooks" / "rag_vs_finetuning.ipynb"
    )

    if not notebook_path.exists():
        print(f"❌ Notebook não encontrado: {notebook_path}")
        return False

    print(f"🚀 Iniciando Jupyter Notebook: {notebook_path}")
    print(
        "💡 O kernel será selecionado automaticamente baseado nos metadados do notebook"
    )

    try:
        # Método mais simples - apenas inicia o notebook
        # O kernel já está configurado no notebook via metadados
        subprocess.run(["jupyter", "notebook", str(notebook_path)], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao iniciar Jupyter: {e}")
        print("💡 Verifique se o Jupyter está instalado: pip install jupyter")
        return False
    except KeyboardInterrupt:
        print("\n👋 Jupyter Notebook encerrado pelo usuário")
        return True


def main():
    """
    Função principal que inicia o notebook de RAG vs Fine-Tuning.
    """
    print("🚀 Pathbit Academy AI - Artigo 0004: RAG vs Fine-Tuning")
    print("=" * 60)

    # Verificações iniciais
    if not verificar_dependencias():
        sys.exit(1)

    verificar_api_keys()

    print("\n📓 Iniciando notebook de RAG vs Fine-Tuning...")

    # Inicia o notebook
    if iniciar_notebook():
        print("✅ Notebook executado com sucesso!")
    else:
        print("❌ Falha ao executar notebook")
        sys.exit(1)


if __name__ == "__main__":
    main()
