"""
Configuração para execução local do notebook
==========================================

Este arquivo substitui as funcionalidades específicas do Google Colab
para permitir execução local do notebook.
"""
import os
import getpass

GROQ_API_KEY_NAME = "GROQ_API_KEY"


try:
    from IPython.display import Markdown, display
except ImportError:
    def display(x):
        """Fallback display function for environments without IPython."""
        print(x)
    class Markdown(str):
        """Fallback Markdown class for environments without IPython."""


def configurar_api_key():
    """
    Configura a API Key do Groq para execução local.
    """
    # Verifica se já está definida
    if GROQ_API_KEY_NAME in os.environ:
        print(f"✅ {GROQ_API_KEY_NAME}: {os.environ[GROQ_API_KEY_NAME][:6]}******")
        return True

    # Solicita a API Key do usuário
    print(f"⚠️  {GROQ_API_KEY_NAME} não definida.")
    print("Você pode:")
    print("1. Definir como variável de ambiente: export GROQ_API_KEY='sua_chave'")
    print("2. Ou digitar agora (será salva apenas para esta sessão):")

    api_key = getpass.getpass("Digite sua API Key do Groq: ").strip()

    if api_key:
        os.environ[GROQ_API_KEY_NAME] = api_key
        print(f"✅ {GROQ_API_KEY_NAME} configurada para esta sessão")
        return True
    else:
        print("❌ API Key não fornecida")
        return False


def exibir_markdown(texto):
    """
    Exibe texto formatado em Markdown (compatível com Colab e Jupyter local).
    """
    display(Markdown(texto))


def exibir_resposta_formatada(modelo, pergunta, resposta, raciocinio=None, tempo=0.0):
    """
    Exibe resposta formatada similar ao Colab.
    """
    texto_raciocinio = ""
    if raciocinio:
        texto_raciocinio = f"""

## 🧐 Raciocínio
================================================

{raciocinio.strip()}
"""

    texto_md = f"""
## 🧠 Modelo: `{modelo}`
**⏱ Tempo de execução:** {tempo:.2f}s{texto_raciocinio}

### 📥 Pergunta

{pergunta.strip()}

### 📤 Resposta

{resposta.strip()}
    """

    exibir_markdown(texto_md)
