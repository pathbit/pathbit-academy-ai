# LLMs Locais com Ollama — Como Montar, Medir e Operar uma Stack de IA 100% Offline sem Custo por Token

Grande parte do material sobre Inteligência Artificial em produção assume uma premissa silenciosa logo na terceira linha de código:
```python
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
```

O exemplo funciona, o dashboard fica elegante, a demonstração encanta a diretoria e cada chamada consome centavos de dólar no cartão corporativo. Para protótipos de fim de semana, isso é conveniente. Mas para sistemas corporativos de missão crítica, ambientes regulados, laboratórios acadêmicos ou operações de alta volumetria, essa dependência externa cobra um pedágio invisível e perigoso.

Não se trata apenas de economizar na fatura da nuvem. Trata-se de responder a três perguntas fundamentais de engenharia de software que uma API de terceiros impede que você responda:
1. **Soberania e Privacidade:** Seus dados confidenciais, prontuários de clientes ou segredos industriais podem cruzar a internet pública e repousar em servidores de terceiros sob jurisdições estrangeiras?
2. **Determinismo e Estabilidade:** O que acontece quando o provedor de nuvem atualiza o modelo silenciosamente na virada do mês, alterando o comportamento de um agente em produção?
3. **Previsibilidade de Latência e Custo Marginal Zero:** Como viabilizar um loop de agente que executa 50 chamadas de reflexão e autoavaliação por minuto se cada chamada adiciona 800 ms de latência de rede mundial e gera custo variável contínuo?

Este artigo parte exatamente de onde o [Artigo 0007 (Agentes e Tool Calling)](https://github.com/pathbit/pathbit-academy-ai/blob/master/0007_agentes_tool_calling/article/ARTICLE.md) parou. No 0007, construímos um agente autônomo com guardrails, planner e retrieval semântico rodando em memória de processo com Hugging Face. Aqui, damos o salto de engenharia: **desacoplamos o motor de inferência em um servidor dedicado via Ollama em container Docker**, consumido via HTTP puro em loopback, com medição cirúrgica de latência, vazão, memória e saída estruturada — sem chave de API, sem autenticação externa e sem pagar um centavo por token gerado.

---

## 1. O que Muda Quando o Modelo Mora na Sua Máquina

A transição da inferência gerenciada na nuvem para a inferência local altera radicalmente a física e a economia do seu software:

![Nuvem versus local](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0008_llms_locais_ollama/assets/01.png)

> **Figura 1:** Na nuvem, cada chamada cruza internet, chaves e faturamento dinâmico. No local, o ciclo inteiro opera dentro dos limites físicos do seu hardware.

### As Quatro Transformações Concretas:

1. **A Latência de Rede Vira Latência de Loopback (`localhost`):**
   Em chamadas de nuvem, a latência observada pelo cliente é a soma de:
   $$\text{Latência}_{\text{total}} = \text{DNS} + \text{Handshake TLS} + \text{Trânsito WAN} + \text{Fila do Provedor} + \text{Inferência}$$
   Em conexões corporativas transatlânticas, o overhead de rede raramente fica abaixo de 150 ms a 400 ms antes que o modelo gere o primeiro byte. No local, o transporte é um socket de loopback em memória interprocessos (`127.0.0.1`), onde o overhead de transporte é inferior a **1 ms**. A métrica que domina passa a ser unicamente a velocidade do hardware.

2. **O Custo Marginal por Token Torna-se Zero:**
   Na nuvem, cada token de entrada e saída é tarifado. Isso induz equipes de engenharia a adotar atalhos perigosos: encurtar prompts de sistema, omitir exemplos *few-shot*, limitar o histórico de conversa e evitar loops agênticos de reflexão. No ambiente local, o investimento é de capital fixo (o hardware já adquirido). Você pode gerar um milhão de tokens por dia sem que isso altere a conta bancária da sua empresa.

3. **Isolamento Absoluto de Dados (Compliance LGPD / GDPR / HIPAA):**
   Ao desligar o cabo de rede da máquina, o sistema continua funcionando com 100% de capacidade. Para instituições financeiras, hospitais, escritórios jurídicos e órgãos governamentais, essa garantia elimina auditorias exaustivas de conformidade sobre vazamento de PII (*Personally Identifiable Information*).

4. **Congelamento Estrito de Versão:**
   Provedores de nuvem frequentemente deprecam versões de modelos (*snapshots*) com aviso prévio curto ou aplicam alinhamentos invisíveis via *system prompts* que alteram a distribuição de probabilidade das saídas. No Docker local, o modelo é um arquivo de pesos imutável (`.gguf`) armazenado em volume. O mesmo teste executado hoje produzirá a mesma distribuição matemática daqui a três anos.

> **A advertência honesta da Pathbit:** Rodar local não é uma bala de prata. Modelos compactos (de 0.5B a 1.5B parâmetros) não possuem o raciocínio enciclopédico de um modelo de fronteira de 400B rodando em clusters de H100 na nuvem. A pergunta que este artigo responde com dados reais não é *"qual é o modelo mais inteligente do planeta"*, mas sim: **o que um modelo compacto de 1 bilhão de parâmetros é capaz de sustentar com precisão determinística dentro da sua infraestrutura?**

---

## 2. Sob o Capô: Como a Inferência Local Realmente Funciona

Para operar modelos locais em produção sem surpresas, o desenvolvedor precisa entender o que acontece na memória do sistema operacional entre o envio do prompt e o retorno da resposta.

### 2.1. Do `llama.cpp` ao Ollama
O Ollama não é um modelo de IA; ele é um servidor de gerenciamento e empacotamento construído em Go que encapsula o projeto **`llama.cpp`** (desenvolvido por Georgi Gerganov). O `llama.cpp` é uma implementação em C/C++ puro da arquitetura Transformer, otimizada cirurgicamente para executar tensores sem dependências externas (como PyTorch ou CUDA runtime pesada).

O Ollama atua como uma camada de orquestração moderna:
- Gerencia o download e armazenamento de modelos em blobs imutáveis;
- Expõe uma API REST compatível com HTTP/1.1 e streaming JSON;
- Aloca dinamicamente camadas neurais entre CPU e GPU (*offloading* via flag `ngl` ou `--num-gpu`);
- Otimiza as instruções da CPU utilizando registradores vetoriais modernos: **AVX2 / AVX-512** em arquiteturas x86 e **ARM NEON / Apple Silicon Metal** em arquiteturas ARM (M1/M2/M3/M4).

### 2.2. A Matemática da Quantização e o Formato GGUF
Um modelo como o Llama 3.2 em ponto flutuante de precisão total (FP16 ou BF16) armazena cada parâmetro em 16 bits (2 bytes). Para um modelo de 1 bilhão de parâmetros, seriam necessários no mínimo 2 GB apenas para os pesos na memória, sem contar o estado de contexto.

O formato **GGUF** (*GPT-Generated Unified Format*) viabiliza a execução local através de **Quantização Pós-Treinamento (PTQ)**:

| Tipo de Quantização | Bits por Peso | Tamanho Llama 3.2 1B | Queda de Perplexidade (PPL) | Recomendação de Uso |
| :--- | :---: | :---: | :---: | :--- |
| **FP16** | 16 bits | ~2.5 GB | Baseline (0.00) | Treinamento e geração de alta fidelidade |
| **Q8_0** | 8 bits | ~1.3 GB | Quase nula (< 0.01) | Servidores com GPU e memória abundante |
| **Q4_K_M** *(Padrão Ollama)* | 4.5 bits | ~800 MB | Mínima (~0.05) | **Padrão Ouro:** Melhor equilíbrio CPU / RAM |
| **Q2_K** | 2.5 bits | ~500 MB | Severa (> 0.50) | Dispositivos embarcados e IoT extremos |

Na quantização `Q4_K_M`, os tensores são divididos em blocos (geralmente de 32 ou 256 parâmetros), onde os pesos são mapeados para inteiros de 4 bits acompanhados de fatores de escala de ponto flutuante. O consumo de memória RAM cai em até 70%, permitindo que o modelo caiba com folga no cache e na memória principal de laptops convencionais.

### 2.3. O Gargalo Real: Largura de Banda de Memória (*Memory Bandwidth*)
Em inferência de LLMs autoregressivos, o cálculo de cada novo token exige que **todos os pesos do modelo sejam lidos da memória uma vez**. Isso significa que a vazão máxima teórica em tokens por segundo é limitada pela largura de banda da memória RAM:

$$\text{Vazão Máxima (tokens/s)} \approx \frac{\text{Largura de Banda de Memória (GB/s)}}{\text{Tamanho dos Pesos do Modelo (GB)}}$$

Se o seu computador possui memória DDR5 operando a 64 GB/s e o modelo ocupa 1.3 GB de RAM, a velocidade teórica máxima de geração sequencial em CPU será de aproximadamente $\frac{64}{1.3} \approx 49 \text{ tokens/s}$. Esse é o motivo pelo qual placas de vídeo com memórias ultrarrápidas (GDDR6 a 500+ GB/s) ou processadores Apple Silicon com memória unificada (200 a 800 GB/s) geram texto em velocidades vertiginosas.

### 2.4. A Gestão do KV Cache (*Key-Value Cache*)
A cada token gerado, a camada de atenção recalcula matrizes de chave ($K$) e valor ($V$). Para não recomputar o passado a cada novo token gerado, o Ollama armazena o histórico em um **KV Cache**. A memória consumida pelo KV Cache cresce linearmente com a janela de contexto:

$$\text{Memória}_{\text{KV}} = 2 \times n_{\text{camadas}} \times n_{\text{heads}} \times d_{\text{head}} \times n_{\text{tokens\_contexto}} \times \text{bytes\_por\_elemento}$$

Por isso, definir o parâmetro de contexto (`num_ctx`) no Ollama é essencial para evitar estouros de memória (*Out of Memory - OOM*) em máquinas com 8 GB ou 16 GB de RAM.

---

## 3. O Stack Mínimo e Gratuito em Docker

Para garantir reprodutibilidade corporativa, empacotamos o servidor em um único arquivo `docker-compose.yml`:

![Stack Ollama no Docker](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0008_llms_locais_ollama/assets/02.png)

> **Figura 2:** Container, volume persistente nomeado e porta HTTP local compõem toda a infraestrutura necessária.

```yaml
services:
  ollama:
    image: ollama/ollama:latest
    container_name: pathbit-ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama
    environment:
      - OLLAMA_KEEP_ALIVE=24h
      - OLLAMA_NUM_PARALLEL=2
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 8G

volumes:
  ollama-data:
```

### Por que essa configuração importa:
- **Volume Persistente `ollama-data`:** Baixar gigabytes de modelos a cada reinício de container destruiria a produtividade. O volume nomeado preserva as camadas de pesos no host permanentemente.
- **`OLLAMA_KEEP_ALIVE=24h`:** Por padrão, o Ollama descarrega o modelo da memória após 5 minutos de inatividade para economizar RAM. Em servidores de produção, descarregar pesos gera um "cold start" de 2 a 4 segundos na requisição seguinte. O `keep_alive` mantém os tensores aquecidos na memória.
- **Porta `11434`:** A porta canônica do Ollama, acessível localmente via `http://localhost:11434`.

Com o container ativo, baixamos os modelos abertos selecionados para a nossa bancada de testes:

```bash
docker compose up -d
docker exec pathbit-ollama ollama pull qwen2.5:0.5b
docker exec pathbit-ollama ollama pull qwen2.5:1.5b
docker exec pathbit-ollama ollama pull llama3.2:1b
docker exec pathbit-ollama ollama pull nomic-embed-text
```

---

## 4. A Anatomia Cirúrgica de uma Chamada Local

Quando o seu código faz uma requisição HTTP para a API do Ollama, o endpoint `/api/chat` ou `/api/generate` suporta dois modos:
1. **Modo Monolítico (`stream: False`):** O servidor aguarda a geração completa de todos os tokens e devolve um único objeto JSON final.
2. **Modo Streaming (`stream: True`):** O servidor devolve um fluxo contínuo de objetos JSON separados por quebras de linha (`\n`), onde cada linha representa um token emitido.

![Anatomia da requisição](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0008_llms_locais_ollama/assets/03.png)

> **Figura 3:** TTFT, tempo de avaliação de prompt e vazão de geração decompõem o que a nuvem costuma esconder em uma única métrica opaca.

### O Cliente de Medição sem Dependências Externas:

Para medir com rigor absoluto sem a sobrecarga ou variáveis de SDKs pesados de terceiros, construímos um cliente HTTP utilizando apenas a biblioteca padrão do Python (`urllib.request` e `json`):

```python
import json
import time
import urllib.request

def chat_com_metricas(base_url: str, model: str, prompt: str, timeout: float = 300.0) -> dict:
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
        "options": {"temperature": 0.0, "num_predict": 128}
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{base_url}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    start_time = time.perf_counter()
    ttft_ms = None
    chunks_recebidos = []
    final_payload = {}

    with urllib.request.urlopen(req, timeout=timeout) as response:
        for line in response:
            if not line.strip():
                continue
            chunk = json.loads(line.decode("utf-8"))
            texto_token = chunk.get("message", {}).get("content", "")
            
            # Registra exatamente o momento em que o primeiro caractere útil chegou
            if texto_token and ttft_ms is None:
                ttft_ms = (time.perf_counter() - start_time) * 1000.0
                
            chunks_recebidos.append(texto_token)
            if chunk.get("done", False):
                final_payload = chunk
                break

    latencia_total_ms = (time.perf_counter() - start_time) * 1000.0
    resposta_completa = "".join(chunks_recebidos)

    # Extrai métricas de telemetria emitidas diretamente pelo motor C++ do Ollama
    eval_count = final_payload.get("eval_count", len(chunks_recebidos))
    eval_duration_ns = final_payload.get("eval_duration", 1)
    prompt_eval_count = final_payload.get("prompt_eval_count", 0)
    prompt_eval_duration_ns = final_payload.get("prompt_eval_duration", 1)

    vazao_tokens_seg = (eval_count / (eval_duration_ns / 1e9)) if eval_duration_ns > 0 else 0.0

    return {
        "modelo": model,
        "resposta": resposta_completa,
        "ttft_ms": round(ttft_ms, 2) if ttft_ms else round(latencia_total_ms, 2),
        "latencia_total_ms": round(latencia_total_ms, 2),
        "tokens_prompt": prompt_eval_count,
        "tokens_gerados": eval_count,
        "vazao_tok_s": round(vazao_tokens_seg, 2),
    }
```

---

## 5. O Benchmark Empírico Medido na Prática

Submetemos os três modelos locais a uma bateria idêntica de testes de engenharia em CPU local:
1. **Geração Livre:** Redação técnica e respostas a perguntas de suporte.
2. **Roteamento e Classificação Zero-Shot:** Classificar chamados em tópicos (`segunda_via`, `devolucao`, `cancelamento`).
3. **Extração de Entidades:** Extrair produto e prazo numérico a partir de texto desestruturado.
4. **Planejamento de Agente sob JSON Forçado (`format: "json"`):** Emitir a ferramenta correta para executar uma ação de negócio.

![Benchmark comparativo](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0008_llms_locais_ollama/assets/04.png)

> **Figura 4:** Três modelos compactos, mesmos prompts, mesma máquina: a comparação deixa de ser opinião e vira decisão de engenharia.

### Resultados Consolidados Medidos em Laboratório (CPU Intel / Apple Silicon Local):

| Modelo | Parâmetros | Tamanho em RAM | TTFT Médio | Latência Total Média | Vazão de Geração | Validade do JSON | Acurácia de Tool Calling |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`qwen2.5:0.5b`** | 494M | ~398 MB | 559 ms | 5.49 s | **79.8 tokens/s** | **100%** | **100%** |
| **`llama3.2:1b`** | 1.2B | ~1.3 GB | **256 ms** | **4.33 s** | 25.3 tokens/s | 0% *(vazio)* | 0% |
| **`qwen2.5:1.5b`** | 1.5B | ~986 MB | 1.022 ms | 6.33 s | 19.4 tokens/s | **100%** | **100%** |

### Três Revelações Críticas Que Derrubam o Senso Comum:

1. **Maior Nem Sempre Significa Melhor em Tarefas Específicas:**
   O `qwen2.5:0.5b`, com menos de 500 milhões de parâmetros e consumindo menos de 400 MB de RAM, gerou quase **80 tokens por segundo** em CPU, superando em mais de 3x a velocidade do modelo 1.5B. Quando o formato foi forçado via decodificação sintática, o 0.5B acertou 100% dos planejamentos de ferramenta.

2. **A Armadilha do TTFT Rápido com JSON Vazio:**
   O `llama3.2:1b` foi o campeão indiscutível de responsividade de primeiro token (TTFT de apenas **256 ms**). No entanto, quando submetido a tarefas de extração sob a flag `format: "json"` genérica, o modelo devolveu `{}` vazio nas 5 tentativas. Ele gerou um JSON sintaticamente perfeito em tempo recorde — que não servia para rigorosamente nada.
   > **Lição:** Decodificação constrangida sintática garante formato, não conteúdo de negócio. Para garantir propriedades obrigatórias, é necessário avançar para JSON Schema formal (tema aprofundado no Artigo 0009).

3. **Prompt Zero-Shot sem Restrição Quebra Modelos Pequenos:**
   Sem restrição estruturada de saída, o modelo 0.5B falhou em todas as classificações zero-shot: em vez de devolver unicamente o rótulo da classe solicitado nas instruções, ele insistiu em inventar justificativas e saudações corteses. Modelos compactos não possuem capacidade de manter fidelidade estrita a prompts complexos em texto livre; eles **exigem restrições formais na camada de inferência**.

---

## 6. Embeddings e Retrieval Vetorial na Mesma Instância

Um sistema de IA corporativo raramente vive apenas de geração de texto. Ele precisa de busca semântica, recuperação de documentos (RAG) e classificação vetorial.

No Ollama, a mesma instância que serve o chat local expõe o endpoint `/api/embed`, permitindo rodar o modelo aberto **`nomic-embed-text`**:

![Matriz de decisão](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0008_llms_locais_ollama/assets/05.png)

> **Figura 5:** A matriz de decisão objetiva para saber exatamente quando migrar do modelo de nuvem para o modelo local.

### 6.1. Características do `nomic-embed-text`:
- **Parâmetros:** 137M parâmetros;
- **Dimensionalidade:** Vetores densos de 768 dimensões;
- **Janela de Contexto:** Suporta até 8.192 tokens por documento;
- **Consumo de Memória:** ~274 MB em RAM;
- **Latência de Codificação Local:** ~14 ms por sentença curta em CPU.

### 6.2. Implementação do Retrieval Semântico Top-1:
No laboratório (`src/ollama_lab.py`), indexamos oito documentos internos de suporte da empresa e submetemos quatro consultas desafiadoras de usuários:

```python
def gerar_embedding(base_url: str, text: str, model: str = "nomic-embed-text") -> list[float]:
    payload = json.dumps({"model": model, "input": text}).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url}/api/embed",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as res:
        dados = json.loads(res.read().decode("utf-8"))
        return dados["embeddings"][0]

def similaridade_cosseno(v1: list[float], v2: list[float]) -> float:
    dot = sum(a * b for a, b in zip(v1, v2))
    norm_a = sum(a * a for a in v1) ** 0.5
    norm_b = sum(b * b for b in v2) ** 0.5
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0
```

**Resultado Medido:** O retrieval local atingiu **4 de 4 acertos (100% de precisão top-1)**, com scores de similaridade superiores a 0.78 nas rotas corretas. Isso prova que um único container Docker de ~3 GB é capaz de substituir com louvor toda a esteira dos Artigos 0002, 0003 e 0007 da Pathbit Academy, com zero conexões com o mundo exterior.

---

## 7. O que Quebra na Prática (Failure Modes em Produção)

Operar modelos locais em escala corporativa envolve lidar com restrições físicas de hardware. Em nossos testes de estresse, mapeamos as quatro falhas mais frequentes:

### 1. O Efeito Bola de Neve do OOM e Swap Thrashing
Se duas requisições concorrentes solicitarem contextos longos (ex: 8.000 tokens cada), o KV Cache consumirá toda a memória RAM livre. Quando o sistema operacional começa a transferir páginas de memória para o disco SSD (*Swap*), a velocidade do modelo desaba de 80 tokens/s para menos de **0.2 tokens/s**.
- **Defesa:** No Docker Compose, defina limites rígidos de memória (`limits: memory: 8G`) e restrinja a janela no prompt (`options: {"num_ctx": 2048}`).

### 2. O Loop Infinito de Alucinação (*Babbling*)
Modelos pequenos sem restrição de parada podem entrar em loops repetitivos de preenchimento até atingir o limite máximo de tokens padrão (4.096).
- **Defesa:** Sempre envie `num_predict: 128` (ou o teto estrito do seu caso de uso) e configure *stop tokens* explícitos (ex: `["\n\n", "Usuário:"]`).

### 3. Aquecimento e Throttling Térmico em CPU
Ao executar benchmarks prolongados em servidores ou laptops sem refrigeração ativa adequada, a CPU atinge 95°C e o governador do sistema operacional reduz os clocks de 4.5 GHz para 1.8 GHz. A vazão cai pela metade ao longo de 10 minutos de teste.
- **Defesa:** Sempre monitore a telemetria térmica da máquina antes de tomar decisões de capacidade de hardware.

---

## 8. Show-Me-The-Code: Executando o Laboratório

Todo o código, scripts de medição, docker-compose e notebook executável estão prontos no repositório oficial da Pathbit Academy:

### Opção 1: Execução Automatizada pelo Terminal
Suba o ambiente e dispare a esteira de benchmark completa:

```bash
# 1. Navegue até o módulo
cd pathbit-academy-ai/0008_llms_locais_ollama

# 2. Suba o servidor e puxe os modelos
docker compose up -d
docker exec pathbit-ollama ollama pull qwen2.5:0.5b
docker exec pathbit-ollama ollama pull qwen2.5:1.5b
docker exec pathbit-ollama ollama pull llama3.2:1b
docker exec pathbit-ollama ollama pull nomic-embed-text

# 3. Configure o ambiente Python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 4. Execute a suíte de benchmarks completa
python src/ollama_lab.py
```

### Artefatos Gerados Automaticamente na Pasta `data/`:
- `benchmark_resultados.csv`: Auditoria detalhada chamada a chamada com TTFT, latência, tokens e vazão.
- `benchmark_resumo.csv`: Consolidação por modelo ordenada por vazão.
- `structured_output.csv`: Taxas de sucesso de JSON válido e acerto de tool calling.
- `embedding_routes.csv`: Classificação semântica top-1 das consultas com score vetorial.
- `benchmark_relatorio.md`: Relatório executivo completo em Markdown.
- `benchmark_comparativo.png`: Gráfico visual de latência e vazão.

### Opção 2: Notebook Interativo
Execute o launcher para abrir o Jupyter Notebook passo a passo:

```bash
python src/main.py
```

### Evidência de Execução Real:
Abaixo, a captura de tela comprovando a execução real do notebook interativo com métricas de telemetria coletadas em tempo de execução:

![Evidência de Execução do Notebook 0008](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0008_llms_locais_ollama/assets/evidence_notebook.png)

---

## 9. Próximos Passos na Trilogia de IA Local

Com o motor de inferência local estabelecido, estável e auditado, os próximos dois artigos fecham as lacunas para viabilizar sistemas de produção reais:

1. **[Artigo 0009 — Saída Estruturada e Modelos System 1](https://github.com/pathbit/pathbit-academy-ai/blob/master/0009_saida_estruturada/article/ARTICLE.md):**
   Como sair da fragilidade do JSON forçado genérico e implementar **Grammar-Guided Sampling com JSON Schema estrito** via Autômatos de Estados Finitos (FSM), e como a fronteira de **Modelos System 1 (Jev vs Laya)** permite decisões tipadas em ~13 ms em passada única ($O(1)$).
2. **[Artigo 0010 — MCP Local via Stdio](https://github.com/pathbit/pathbit-academy-ai/blob/master/0010_mcp_local/article/ARTICLE.md):**
   Como plugar ferramentas corporativas reais ao seu modelo local através do **Model Context Protocol (MCP)** da Anthropic, utilizando pipes do sistema operacional com isolamento de processos e menos de 1 ms de overhead de protocolo.

---

## Referências Técnicas

- [Ollama: Get up and running with large language models locally](https://ollama.com)
- [Gerganov, Georgi: llama.cpp — Port of Facebook's LLaMA model in C/C++](https://github.com/ggerganov/llama.cpp)
- [GGUF Specification: The unified model file format for quantized LLM inference](https://github.com/ggerganov/ggml/blob/master/docs/gguf.md)
- [Qwen 2.5: A Comprehensive Foundation Model Family by Alibaba Cloud](https://qwenlm.github.io/)
- [Llama 3.2: Open Source Multimodal and Lightweight Language Models by Meta](https://www.llama.com/)
- [Nomic Embed: High-Performance Open-Weights Text Embeddings](https://www.nomic.ai/blog/posts/nomic-embed-text-v1)
- [Frantar, Elias et al.: GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers (arXiv:2210.17323)](https://arxiv.org/abs/2210.17323)

---

👉 **Repositório oficial no GitHub:** [https://github.com/pathbit/pathbit-academy-ai](https://github.com/pathbit/pathbit-academy-ai)  
👉 **Módulo:** `0008_llms_locais_ollama`

#InteligenciaArtificial #LLM #Ollama #Docker #OpenSource #Python #PathbitAcademy #LocalAI #SoftwareEngineering #DevOps #DeepLearning
