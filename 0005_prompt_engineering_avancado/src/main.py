#!/usr/bin/env python3
"""
Pathbit Academy AI - Artigo 0005: Prompt Engineering Avançado.

Abre o notebook do artigo localmente.
"""

import subprocess
import sys
from pathlib import Path


def verificar_dependencias() -> bool:
    try:
        result = subprocess.run(
            ["jupyter", "--version"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        if result.returncode == 0:
            print("OK: Jupyter encontrado")
            return True
        print("ERRO: Jupyter nao encontrado no PATH")
        print("Dica: pip install -r requirements.txt")
        return False
    except subprocess.TimeoutExpired:
        print("AVISO: verificacao do Jupyter demorou, continuando")
        return True
    except (subprocess.SubprocessError, OSError) as exc:
        print(f"ERRO ao verificar dependencias: {exc}")
        return False


def iniciar_notebook() -> bool:
    notebook_path = (
        Path(__file__).parent.parent
        / "notebooks"
        / "prompt_engineering_avancado.ipynb"
    )
    if not notebook_path.exists():
        print(f"ERRO: notebook nao encontrado: {notebook_path}")
        return False

    print(f"Iniciando notebook: {notebook_path}")
    try:
        subprocess.run(["jupyter", "notebook", str(notebook_path)], check=True)
        return True
    except subprocess.CalledProcessError as exc:
        print(f"ERRO ao iniciar jupyter: {exc}")
        return False
    except KeyboardInterrupt:
        print("\nEncerrado pelo usuario")
        return True


def main() -> None:
    check_only = "--check" in sys.argv
    print("Pathbit Academy AI - Artigo 0005")
    print("=" * 45)
    if not verificar_dependencias():
        sys.exit(1)
    if check_only:
        notebook_path = (
            Path(__file__).parent.parent
            / "notebooks"
            / "prompt_engineering_avancado.ipynb"
        )
        if notebook_path.exists():
            print("OK: verificacao concluida")
            return
        print("ERRO: notebook nao encontrado")
        sys.exit(1)
    if not iniciar_notebook():
        sys.exit(1)


if __name__ == "__main__":
    main()
