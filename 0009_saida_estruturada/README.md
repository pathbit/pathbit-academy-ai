# pathbit-academy-ai

## 0009_saida_estruturada

**Ano:** 2026  
**ID do Artigo:** 0009  
**Autor:** Eliel Sousa  
**Categoria:** Inteligência Artificial / Saída Estruturada e Grammar-Guided Sampling

---

### Resumo

Este módulo prova como validar sintaxe e contrato das respostas sem confundir isso com correção de negócio, comparando três níveis de contrato em modelos compactos (`qwen2.5:0.5b`, `qwen2.5:1.5b` e `llama3.2:1b`):

- **Modo Livre (Prompt Only):** apenas pede JSON no prompt textual (fragilidade de parse e fences).
- **Modo JSON (`format: "json"`):** garante sintaxe parseável, mas campos e enums permanecem desgovernados.
- **Modo Schema (`format: <json_schema>`):** impõe contrato estrito via decodificação constrangida (Grammar-Guided Sampling com máscara de logits).
- **Baseline não generativa:** roteador por embeddings `nomic-embed-text`; não executa Jev, Laya ou Kev e não oferece probabilidades calibradas.
- **Análise de Latência e Retry:** demonstra empiricamente por que retries via prompt duplicam o tempo de resposta, enquanto contratos formais resolvem na largada.

Tudo testado e medido em CPU local via Ollama.


---

### Tecnologias e Modelos Utilizados

- **Servidor de inferência:** `Ollama` em Docker (`ollama/ollama:latest`)
- **Modelos de linguagem:** `qwen2.5:0.5b`, `qwen2.5:1.5b`, `llama3.2:1b`
- **Validação de contratos:** `jsonschema`, Python `urllib` padrão
- **Análise e visualização:** `pandas`, `matplotlib`
- **Ambiente:** Python 3.14+ (compatível com 3.10+) em ambiente virtual isolado (.venv)

---

### Estrutura do Artigo

- `article/ARTICLE.md` - Conteúdo técnico completo com diagramas e explicações aprofundadas.
- `article/ARTICLE_LINKEDIN.md` - Versão formatada para publicação no LinkedIn Pulse.
- `article/POST_LINKEDIN.md` - Post conciso para o feed do LinkedIn.
- `assets/` e `highlight/` - Imagens técnicas em 1920x1080 e apresentação em PDF de alta resolução.
- `data/` - Artefatos medidos: CSVs linha a linha, tabela consolidada e relatório markdown.
- `notebooks/` - Notebook interativo passo a passo.
- `src/` - Launcher do notebook e laboratório automatizado de benchmarks.

---

### Como Executar

#### Pré-requisitos

1. **Ollama em Execução:**
   Certifique-se de que o container Ollama está ativo (conforme configurado no módulo 0008):
   ```bash
   cd ../0008_llms_locais_ollama
   docker compose up -d
   cd ../0009_saida_estruturada
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

#### Rodar o laboratório de benchmarks

```bash
python src/structured_lab.py
```

Opções úteis:
```bash
# Rodar 2 repetições para benchmark rápido
python src/structured_lab.py --repeat 2

# Testar apenas um modelo específico
python src/structured_lab.py --models qwen2.5:0.5b

# Endpoint customizado do Ollama
python src/structured_lab.py --base-url http://localhost:11434
```

#### Abrir o notebook interativo pelo launcher

```bash
python src/main.py
```

---

### Artefatos gerados

Ao executar o laboratório, você terá:

- `data/structured_resultados.csv` - linha a linha de cada chamada medida (parse, validação de schema, assertividade semântica, latência e tokens)
- `data/structured_resumo.csv` - consolidação por nível de contrato (Livre, JSON, Schema)
- `data/structured_resumo_modelo.csv` - consolidação individual por modelo e modo
- `data/system_one_comparativo.json` - métricas do roteador por embeddings; nome histórico preservado
- `data/structured_relatorio.md` - relatório técnico pronto para leitura
- `data/structured_comparativo.png` - gráfico comparativo de conformidade e latência
- `../tmp/evidencias_notebooks/0009_saida_estruturada/evidence_notebook.png` - comprovação visual de execução do notebook interativo

---

### Versão para LinkedIn

- `article/ARTICLE_LINKEDIN.md` - artigo para LinkedIn Pulse com análise aprofundada.
- `article/POST_LINKEDIN.md` - post conciso pronto para publicar no feed do LinkedIn.

---

### Links úteis

- Artigo completo: [ARTICLE.md](./article/ARTICLE.md)
- Repositório: [pathbit-academy-ai](https://github.com/pathbit/pathbit-academy-ai)
- Artigo anterior: [0008 - LLMs Locais com Ollama](https://github.com/pathbit/pathbit-academy-ai/blob/master/0008_llms_locais_ollama/article/ARTICLE.md)
- Próximo artigo: [0010 - MCP Local](https://github.com/pathbit/pathbit-academy-ai/blob/master/0010_mcp_local/article/ARTICLE.md)

---

### Licença e Créditos

Desenvolvido com dedicação pela equipe de engenharia da **[Pathbit](https://pathbit.com)**.
Código e artigos distribuídos sob a licença MIT.

