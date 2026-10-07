# pathbit-academy-ai

## 0008_llms_locais_ollama

**Ano:** 2026  
**ID do Artigo:** 0008  
**Autor:** Eliel Sousa  
**Categoria:** Inteligência Artificial / LLMs Locais com Ollama

---

### Resumo

Este módulo prova que um stack de IA roda 100% local, sem chave de API, sem conta externa e sem custo por token:

- Ollama em container Docker com volume persistente de modelos
- benchmark de chat com TTFT, latência total e vazão (tokens/s) por modelo
- saída estruturada em JSON forçado (`format: "json"`) com taxa de acerto de tool
- retrieval semântico com `nomic-embed-text` na mesma instância
- relatório markdown, CSVs e gráfico comparativo como evidência da execução

Tudo medido na própria máquina, em CPU.

---

### Tecnologias e Modelos Utilizados

- **Servidor de modelos:** `Ollama` em Docker (`ollama/ollama:latest`)
- **Modelos de chat:** `qwen2.5:0.5b`, `qwen2.5:1.5b`, `llama3.2:1b`
- **Modelo de embeddings:** `nomic-embed-text`
- **Cliente:** Python padrão (`urllib`), sem SDK
- **Ambiente:** Python 3.14+ (compatível com 3.10+) em ambiente virtual isolado (.venv), Pandas, Matplotlib

---

### Estrutura do Artigo

- `article/ARTICLE.md` - Conteúdo completo.
- `article/ARTICLE_LINKEDIN.md` - Versão resumida para publicação em artigo no LinkedIn Pulse.
- `article/POST_LINKEDIN.md` - Post direto e conciso para o feed do LinkedIn.
- `assets/` e `highlight/` - Imagens técnicas e material de apoio visual.
- `data/` - Artefatos medidos: CSVs, relatório e snapshot do servidor.
- `notebooks/` - Notebook interativo.
- `src/` - Launcher do notebook e laboratório de benchmarks.
- `docker-compose.yml` - Sobe o Ollama local com volume de modelos.

---

### Como Executar

#### Pré-requisitos

- Docker Desktop ou Docker Engine (sem conta no registry: a imagem `ollama/ollama` é pública)
- Python 3.14+ (compatível com 3.10+) executando em ambiente virtual isolado (.venv)
- Sem cobrança de API por token após baixar modelos; hardware e energia têm custo
- Conexão de internet apenas para baixar a imagem e os modelos abertos na primeira execução

#### Subir o Ollama e puxar os modelos

```bash
cd 0008_llms_locais_ollama

docker compose up -d
docker exec pathbit-ollama ollama pull qwen2.5:0.5b
docker exec pathbit-ollama ollama pull qwen2.5:1.5b
docker exec pathbit-ollama ollama pull llama3.2:1b
docker exec pathbit-ollama ollama pull nomic-embed-text
```

> Em máquina sem Docker Compose v2, o comando `docker compose up -d` vira `docker-compose up -d`.

#### Preparar o ambiente Python

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### Rodar o laboratório de benchmarks

```bash
python src/ollama_lab.py
```

Opções úteis:

```bash
# Menos repetições para uma primeira prova rápida
python src/ollama_lab.py --repeat 1 --attempts 3

# Benchmark de um modelo específico
python src/ollama_lab.py --models qwen2.5:0.5b

# Endpoint do Ollama em outra porta ou host
python src/ollama_lab.py --base-url http://localhost:11434
```

#### Abrir o notebook pelo launcher

```bash
python src/main.py
```

#### Executar notebook diretamente

```bash
jupyter notebook notebooks/llms_locais_ollama.ipynb
```

---

### O que você vai aprender

1. Como subir um servidor de modelos local com Docker e volume persistente.
2. Como medir TTFT, latência total e vazão de tokens de modelos locais sem SDK.
3. Como forçar saída JSON com `format: "json"` e medir a taxa de acerto de um planner.
4. Como rodar retrieval semântico na mesma instância que serve o chat.
5. Como transformar a escolha de modelo em decisão baseada em artefatos, e não em opinião.

---

### Artefatos gerados

Ao executar o laboratório, você terá:

- `data/benchmark_resultados.csv` - linha a linha de cada chamada medida
- `data/benchmark_resumo.csv` - consolidação por modelo, ordenada por vazão
- `data/structured_output.csv` - taxa de JSON válido e tool correta por modelo
- `data/embedding_routes.csv` - retrieval top-1 de cada consulta de teste
- `data/embedding_summary.csv` - latência e dimensão dos embeddings locais
- `data/benchmark_relatorio.md` - relatório pronto para leitura
- `data/benchmark_comparativo.png` - gráfico comparativo de latência e vazão
- `data/modelos_disponiveis.json` - snapshot do servidor no momento da execução

---

### Versão para LinkedIn

- `article/ARTICLE_LINKEDIN.md` - post pronto para publicar, dentro do limite de caracteres do LinkedIn (3.000).

---

### Links úteis

- Artigo completo: [ARTICLE.md](./article/ARTICLE.md)
- Repositório: [pathbit-academy-ai](https://github.com/pathbit/pathbit-academy-ai)
- Artigo anterior: [0007 - Agentes e Tool Calling](https://github.com/pathbit/pathbit-academy-ai/blob/master/0007_agentes_tool_calling/article/ARTICLE.md)
- Próximo artigo: [0009 - Saída Estruturada](https://github.com/pathbit/pathbit-academy-ai/blob/master/0009_saida_estruturada/article/ARTICLE.md)
- Conclusão da trilogia: [0010 - MCP Local](https://github.com/pathbit/pathbit-academy-ai/blob/master/0010_mcp_local/article/ARTICLE.md)

