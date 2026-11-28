# pathbit-academy-ai

## 0010_mcp_local

**Ano:** 2026  
**ID do Artigo:** 0010  
**Autor:** Eliel Sousa  
**Categoria:** Inteligência Artificial / Model Context Protocol (MCP) e Agentes Locais

---

### Resumo

Abra uma sessão **Model Context Protocol (MCP)** via `stdio` e, em seguida, deixe os modelos locais `qwen2.5:0.5b`, `qwen2.5:1.5b` e `llama3.2:1b` proporem chamadas por meio de Ollama.

- O servidor de ferramentas se comunica com o cliente por `stdin` e `stdout`. A consulta a Ollama usa HTTP em um caminho separado.
- O cliente descobre três ferramentas de demonstração com `session.list_tools()`.
- Ollama propõe o plano. O cliente valida o formato e, quando aplicável, chama a ferramenta via `session.call_tool()`.
- A série de 50 chamadas isoladas de uma ferramenta já inicializada registrou p50 de 0,99 ms e p95 de 1,53 ms. O teste com planner tem outro recorte.
- Consulte o CSV para acompanhar decisões, resultados e tempo por etapa.

---

### Tecnologias e Modelos Utilizados

- **Protocolo de Contexto:** `mcp` (Python SDK oficial da Anthropic)
- **Servidor de inferência:** `Ollama` em Docker (`ollama/ollama:latest`)
- **Modelos de linguagem:** `qwen2.5:0.5b`, `qwen2.5:1.5b`, `llama3.2:1b`
- **Validação de contratos:** `jsonschema`
- **Análise e visualização:** `pandas`, `matplotlib`
- **Ambiente:** Python 3.14+ (compatível com 3.10+) em ambiente virtual isolado (.venv)

---

### Estrutura do Artigo

- `article/ARTICLE.md` - Conteúdo técnico completo com diagramas e explicações aprofundadas.
- `article/ARTICLE_LINKEDIN.md` - Versão formatada para publicação no LinkedIn Pulse.
- `article/POST_LINKEDIN.md` - Post conciso para o feed do LinkedIn.
- `assets/` e `highlight/` - Figuras técnicas e [destaques em PDF](highlight/highlights_0010.pdf).
- `data/` - Catálogo de tools descobertas, métricas de protocolo e auditoria de chamadas agênticas.
- `notebooks/` - Notebook interativo passo a passo.
- `src/` - Servidor MCP (`mcp_server.py`), laboratório (`mcp_lab.py`) e launcher (`main.py`).

---

### Início rápido

Para inspecionar o servidor antes de instalar Ollama, prepare o ambiente Python e execute [a sessão MCP sem modelo](article/ARTICLE.md#3-faça-a-primeira-chamada-sem-ollama) do artigo.

#### Pré-requisitos do laboratório com modelo

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

Defina `OLLAMA_BASE_URL` antes de iniciar o Jupyter para usar o mesmo
endpoint alternativo no notebook.

#### Abrir o notebook interativo pelo launcher

```bash
python src/main.py
```

---

### Artefatos gerados

Ao executar o laboratório, você terá:

- `data/catalogo_tools.json` - catálogo de ferramentas descobertas dinamicamente em runtime via `session.list_tools()`
- `data/mcp_latencia_protocolo.json` - medição isolada de 50 chamadas de transporte stdio (p50 de 0,99 ms)
- `data/mcp_resultados.csv` - escolha, gabarito, indicadores de validação e tempos por consulta
- `data/mcp_resumo.csv` - consolidação de conformidade, acerto de ferramenta e latência por modelo
- `data/mcp_relatorio.md` - relatório técnico executivo consolidado
- `data/mcp_comparativo.png` - gráfico de latência de planejamento e das chamadas de ferramenta

---

### Versão para LinkedIn

- `article/ARTICLE_LINKEDIN.md` - artigo para LinkedIn Pulse com análise aprofundada.
- `article/POST_LINKEDIN.md` - post conciso pronto para publicar no feed do LinkedIn.

---

### Links úteis

- Artigo completo: [ARTICLE.md](./article/ARTICLE.md)
- Repositório: [pathbit-academy-ai](https://github.com/pathbit/pathbit-academy-ai)
- Artigo anterior 1: [0008 - LLMs Locais com Ollama](https://github.com/pathbit/pathbit-academy-ai/blob/master/0008_llms_locais_ollama/article/ARTICLE.md)
- Artigo anterior 2: [0009 - Saída Estruturada](https://github.com/pathbit/pathbit-academy-ai/blob/master/0009_saida_estruturada/article/ARTICLE.md)
- Próximo laboratório: [0011 - Aprovação humana e idempotência](../0011_aprovacao_idempotencia/article/ARTICLE.md)

---

### Licença e Créditos

Código e artigos sob a [licença MIT](../LICENSE).

Developed with ❤️ by [Pathbit](https://www.pathbit.com.br/)

