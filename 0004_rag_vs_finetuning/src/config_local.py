"""Conexão opcional ao Ollama para executar a comparação sem credencial cloud.

LAB_PROVIDER=ollama seleciona explicitamente uma baseline Qwen local. Isso não
valida desempenho, preços ou disponibilidade dos modelos da Groq.
"""
import json
import os

import httpx
from groq import Groq


class TransporteLocal(httpx.HTTPTransport):
    def handle_request(self, request):
        payload = json.loads(request.content)
        payload["model"] = "qwen2.5:1.5b"
        payload["max_tokens"] = min(payload.pop("max_completion_tokens", payload.get("max_tokens", 128)), 128)
        payload["options"] = {"num_thread": 4}
        for key in ("reasoning_effort", "reasoning_format", "include_reasoning"):
            payload.pop(key, None)
        adapted = httpx.Request(request.method, request.url.copy_with(path="/v1/chat/completions"),
                                json=payload, extensions=request.extensions)
        return super().handle_request(adapted)


def criar_cliente():
    if os.getenv("LAB_PROVIDER") != "ollama":
        return Groq(api_key=os.environ["GROQ_API_KEY"])
    return Groq(api_key="ollama-local", base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
                http_client=httpx.Client(transport=TransporteLocal(), timeout=300))