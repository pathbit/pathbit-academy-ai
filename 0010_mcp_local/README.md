# pathbit-academy-ai

## 0010_mcp_local

**Ano:** 2026  
**ID do Artigo:** 0010  
**Autor:** Eliel Sousa  
**Categoria:** Inteligência Artificial / Model Context Protocol (MCP) e Agentes Locais

---

### Resumo

Este módulo demonstra a implementação prática e isolada do **Model Context Protocol (MCP)** da Anthropic, conectando um servidor MCP local via transporte `stdio` a modelos locais de inferência no Ollama (`qwen2.5:0.5b`, `qwen2.5:1.5b` e `llama3.2:1b`):

- **Transporte Stdio Seguro:** Comunicação IPC via `stdin`/`stdout` sem abrir portas de rede locais nem depender de tráfego externo.
- **Descoberta Dinâmica de Ferramentas:** Uso de `session.list_tools()` para desacoplar o agente do catálogo de funções corporativas.
- **Loop Agêntico Completo:** O Ollama atua como planner sob JSON Schema constrangido (módulo 0009), chamando a ferramenta MCP correspondente via `session.call_tool()`.
- **Medição Cirúrgica de Overhead:** 50 chamadas de protocolo isoladas provam que a camada MCP adiciona apenas ~0.99 ms de mediana (< 0.25% do tempo total).
- **Trilha de Auditoria Forense:** Registro estruturado de decisões em CSV/JSONL para governança em ambientes regulados.

---

### Tecnologias e Modelos Utilizados

- **Protocolo de Contexto:** `mcp` (Python SDK oficial da Anthropic)
- **Servidor de inferência:** `Ollama` em Docker (`ollama/ollama:latest`)
- **Modelos de linguagem:** `qwen2.5:0.5b`, `qwen2.5:1.5b`, `llama3.2:1b`
- **Validação de contratos:** `jsonschema`
- **Análise e visualização:** `pandas`, `matplotlib`
- **Ambiente:** Python 3.10+

---

### Estrutura do Artigo

- `article/ARTICLE.md` - Conteúdo técnico completo com diagramas e explicações aprofundadas.
- `article/ARTICLE_LINKEDIN.md` - Versão formatada para publicação no LinkedIn Pulse.
- `article/POST_LINKEDIN.md` - Post conciso para o feed do LinkedIn.
- `assets/` e `highlight/` - Imagens técnicas em 1920x1080 e apresentação em PDF de alta resolução.
- `data/` - Catálogo de tools descobertas, métricas de protocolo e auditoria de chamadas agênticas.
- `notebooks/` - Notebook interativo passo a passo.
- `src/` - Servidor MCP (`mcp_server.py`), laboratório (`mcp_lab.py`) e launcher (`main.py`).

---

### Como Executar

#### Pré-requisitos

1. **Ollama em Execução:**
   ```bash
   cd ../0008_llms_locais_ollama
   docker compose up -d
   cd ../0010_mcp_local
   ```

2. **Modelos Locais:**
   ```bash
   docker exec pathbit-ollama ollama pull qwen2.5:0.5b
   docker exec pathbit-ollama ollama pull qwen2.5:1.5b
   docker exec pathbit-ollama ollama pull llama3.2:1b
   ```

3. **Ambiente Virtual Python:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

#### Rodar o laboratório automatizado MCP

```bash
python src/mcp_lab.py
```

Opções úteis:
```bash
# Rodar 2 repetições
python src/mcp_lab.py --repeat 2

# Testar apenas um modelo específico
python src/mcp_lab.py --models qwen2.5:0.5b

# Endpoint customizado do Ollama
python src/mcp_lab.py --base-url http://localhost:11434
```

#### Abrir o notebook interativo pelo launcher

```bash
python src/main.py
```

---

### Licença e Créditos

Desenvolvido com dedicação pela equipe de engenharia da **[Pathbit](https://pathbit.com)**.
Código e artigos distribuídos sob a licença MIT.
