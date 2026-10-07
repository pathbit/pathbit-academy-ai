"""
Configuração para execução local do notebook
==========================================

Este arquivo substitui as funcionalidades específicas do Google Colab
para permitir execução local do notebook.
"""
import os
import getpass
import sys

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
    if os.getenv("LAB_PROVIDER") == "ollama":
        print("Modo local explícito: Qwen 0.5B/1.5B, não um benchmark de LRM nem de Groq.")
        return True
    if os.getenv(GROQ_API_KEY_NAME):
        print(f"✅ {GROQ_API_KEY_NAME} configurada (valor não exibido)")
        return True

    # Solicita a API Key do usuário
    print(f"⚠️  {GROQ_API_KEY_NAME} não definida.")
    print("Você pode:")
    print("1. Definir como variável de ambiente: export GROQ_API_KEY='sua_chave'")
    print("2. Ou digitar agora (será salva apenas para esta sessão):")

    if not sys.stdin.isatty():
        raise RuntimeError("Defina GROQ_API_KEY ou LAB_PROVIDER=ollama; execução automática não solicita segredos.")
    api_key = getpass.getpass("Digite sua API Key do Groq: ").strip()

    if api_key:
        os.environ[GROQ_API_KEY_NAME] = api_key
        print(f"✅ {GROQ_API_KEY_NAME} configurada para esta sessão")
        return True
    else:
        print("❌ API Key não fornecida")
        return False


def criar_cliente_groq():
    """Groq real ou baseline Ollama explicitamente selecionada pelo usuário."""
    from groq import Groq
    if os.getenv("LAB_PROVIDER") != "ollama":
        return Groq(api_key=os.environ[GROQ_API_KEY_NAME])
    import httpx
    import json

    class TransporteLocal(httpx.HTTPTransport):
        def handle_request(self, request):
            payload = json.loads(request.content)
            payload["model"] = "qwen2.5:1.5b" if "120b" in payload["model"] else "qwen2.5:0.5b"
            payload["max_tokens"] = min(payload.pop("max_completion_tokens", 128), 128)
            payload["options"] = {"num_thread": 4}
            for key in ("reasoning_effort", "reasoning_format", "include_reasoning", "max_reasoning_tokens"):
                payload.pop(key, None)
            adapted = httpx.Request(request.method, request.url.copy_with(path="/v1/chat/completions"),
                                    json=payload, extensions=request.extensions)
            return super().handle_request(adapted)

    return Groq(api_key="ollama-local", base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
                http_client=httpx.Client(transport=TransporteLocal(), timeout=300))


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
