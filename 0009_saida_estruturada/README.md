# pathbit-academy-ai

## 0009_saida_estruturada

**Ano:** 2026  
**ID do Artigo:** 0009  
**Autor:** Eliel Sousa  
**Categoria:** Inteligência Artificial / Saída Estruturada e Grammar-Guided Sampling

---

### Resumo

Este módulo prova como transformar a inferência probabilística de LLMs locais em chamadas de função determinísticas e tipadas, comparando três níveis de contrato em modelos compactos (`qwen2.5:0.5b`, `qwen2.5:1.5b` e `llama3.2:1b`):

- **Modo Livre (Prompt Only):** apenas pede JSON no prompt textual (fragilidade de parse e fences).
- **Modo JSON (`format: "json"`):** garante sintaxe parseável, mas campos e enums permanecem desgovernados.
- **Modo Schema (`format: <json_schema>`):** impõe contrato estrito via decodificação constrangida (Grammar-Guided Sampling com máscara de logits).
- **Análise de Latência e Retry:** demonstra empiricamente por que retries via prompt duplicam o tempo de resposta, enquanto o schema estrito resolve na primeira chamada.

Tudo testado e medido em CPU local via Ollama.

---

### Tecnologias e Modelos Utilizados

- **Servidor de inferência:** `Ollama` em Docker (`ollama/ollama:latest`)
- **Modelos de linguagem:** `qwen2.5:0.5b`, `qwen2.5:1.5b`, `llama3.2:1b`
- **Validação de contratos:** `jsonschema`, Python `urllib` padrão
- **Análise e visualização:** `pandas`, `matplotlib`
- **Ambiente:** Python 3.10+

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

### Licença e Créditos

Desenvolvido com dedicação pela equipe de engenharia da **[Pathbit](https://pathbit.com)**.
Código e artigos distribuídos sob a licença MIT.
