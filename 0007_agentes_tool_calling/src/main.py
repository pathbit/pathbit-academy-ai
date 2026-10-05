#!/usr/bin/env python3
"""
Pathbit Academy AI - Artigo 0007: Agentes e Tool Calling.

Abre o notebook do artigo localmente.
"""

import subprocess
import sys
from pathlib import Path


def obter_comando_jupyter() -> list[str] | None:
    try:
        res = subprocess.run(
            [sys.executable, "-m", "jupyter", "--version"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        if res.returncode == 0:
            return [sys.executable, "-m", "jupyter"]
    except (subprocess.SubprocessError, OSError):
        pass

    try:
        res = subprocess.run(
            ["jupyter", "--version"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        if res.returncode == 0:
            return ["jupyter"]
    except (subprocess.SubprocessError, OSError):
        pass

    return None


def verificar_dependencias() -> bool:
    cmd = obter_comando_jupyter()
    if cmd is not None:
        print("OK: Jupyter encontrado")
        return True
    print("ERRO: Jupyter nao encontrado no ambiente atual nem no PATH")
    print("Dica: pip install -r requirements.txt")
    return False


def iniciar_notebook() -> bool:
    notebook_path = (
        Path(__file__).parent.parent / "notebooks" / "agentes_tool_calling.ipynb"
    )
    if not notebook_path.exists():
        print(f"ERRO: notebook nao encontrado: {notebook_path}")
        return False

    cmd = obter_comando_jupyter()
    if cmd is None:
        print("ERRO: Jupyter nao disponivel para iniciar o notebook")
        return False

    print(f"Iniciando notebook: {notebook_path}")
    try:
        subprocess.run([*cmd, "notebook", str(notebook_path)], check=True)
        return True
    except subprocess.CalledProcessError as exc:
        print(f"ERRO ao iniciar jupyter: {exc}")
        return False
    except KeyboardInterrupt:
        print("\nEncerrado pelo usuario")
        return True


def main() -> None:
    check_only = "--check" in sys.argv
    print("Pathbit Academy AI - Artigo 0007")
    print("=" * 45)
    if not verificar_dependencias():
        sys.exit(1)
    if check_only:
        notebook_path = (
            Path(__file__).parent.parent / "notebooks" / "agentes_tool_calling.ipynb"
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
