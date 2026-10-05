#!/usr/bin/env python3
"""
Pathbit Academy AI - Artigo 0010: MCP Local (Model Context Protocol).

Abre o notebook do artigo localmente ou executa o laboratório do protocolo MCP.
"""

import asyncio
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
        Path(__file__).parent.parent / "notebooks" / "mcp_local.ipynb"
    )
    if not notebook_path.exists():
        print(f"ERRO: notebook nao encontrado: {notebook_path}")
        return False

    cmd = obter_comando_jupyter()
    if cmd is None:
        print("ERRO: jupyter nao encontrado para abrir o notebook")
        return False

    full_cmd = cmd + ["notebook", str(notebook_path)]
    print(f"Iniciando: {' '.join(full_cmd)}")
    try:
        subprocess.run(full_cmd, check=True)
        return True
    except KeyboardInterrupt:
        print("\nNotebook finalizado pelo usuario")
        return True
    except subprocess.SubprocessError as exc:
        print(f"ERRO ao iniciar notebook: {exc}")
        return False


def main() -> None:
    print("=" * 60)
    print("  Pathbit Academy AI - Artigo 0010: MCP Local")
    print("=" * 60)

    if any(arg in sys.argv for arg in ("-h", "--help")):
        print("Uso:")
        print("  python src/main.py          # Abre o notebook interativo no Jupyter")
        print("  python src/main.py --check  # Apenas valida dependências e arquivos")
        print("  python src/main.py --lab    # Executa o laboratório do protocolo MCP")
        return

    if "--check" in sys.argv:
        if not verificar_dependencias():
            sys.exit(1)
        notebook_path = (
            Path(__file__).parent.parent / "notebooks" / "mcp_local.ipynb"
        )
        if notebook_path.exists():
            print("OK: verificacao concluida")
            return
        print(f"ERRO: notebook nao encontrado: {notebook_path}")
        sys.exit(1)

    if len(sys.argv) > 1 and sys.argv[1] == "--lab":
        lab_script = Path(__file__).parent / "mcp_lab.py"
        subprocess.run([sys.executable, str(lab_script)] + sys.argv[2:])
        return

    if not verificar_dependencias():
        sys.exit(1)

    print("\nAbrindo notebook interativo...")
    if not iniciar_notebook():
        sys.exit(1)


if __name__ == "__main__":
    main()

