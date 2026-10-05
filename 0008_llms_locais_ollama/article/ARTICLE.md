# LLMs locais com Ollama - como provar um stack de IA sem nuvem, sem chave e sem custo por token

Grande parte do material sobre IA em produção assume uma coisa discreta no meio do caminho: uma chave de API. O exemplo funciona, o dashboard fica bonito, e cada chamada consome crédito de alguém. Para aprender, demonstrar em aula ou rodar um piloto sensível, essa dependência é incômoda. Não pelo custo em si, mas pelo que ela impede: você não controla latência, não controla versão do modelo e não consegue provar nada sem internet.

Este artigo parte do ponto em que o agente local do artigo anterior deixou implícito. O agente do 0007 rodava um planner e um retrieval na máquina, mas usava bibliotecas de Hugging Face carregadas em processo. Aqui o passo seguinte é separar o servidor do modelo do código que o consome: um Ollama em container Docker servindo uma API HTTP local, com benchmark medido na própria máquina, sem chave de API e sem custo por token.

> Se você vier do artigo anterior de [Agentes e Tool Calling](https://github.com/pathbit/pathbit-academy-ai/blob/master/0007_agentes_tool_calling/article/ARTICLE.md), vai reconhecer a continuidade. Depois de dar autonomia com controle, o próximo passo natural é perguntar onde o modelo desses agentes roda quando a nuvem não é opção.

## O que muda quando o modelo mora na sua máquina

![Nuvem versus local](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0008_llms_locais_ollama/assets/01.png)

> Figura 1: Na nuvem, cada chamada cruza internet, chave e faturamento. No local, o caminho inteiro cabe no seu hardware.

Rodar local não é só economizar. São quatro mudanças concretas:

- a latência de rede vira latência de loopback, e a métrica que passa a dominar é a geração do modelo;
- o custo por token desaparece, e o limite passa a ser a memória da máquina;
- o dado nunca sai do ambiente, o que destrava pilotos com informação sensível;
- a versão do modelo fica congelada no container, e o benchmark deixa de comparar alvos móveis.

O contrário também é verdade, e o artigo não esconde: modelos locais de 0.5B a 1.5B parâmetros são menos capazes que os modelos de fronteira. A pergunta que este artigo responde não é "qual é o melhor modelo do mundo", e sim "o que um modelo que cabe na minha máquina consegue sustentar".

## O stack gratuito que sustenta o experimento

![Stack Ollama no Docker](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0008_llms_locais_ollama/assets/02.png)

> Figura 2: Container, volume de modelos e porta local formam todo o infraestrutura necessária.

São três blocos, todos sem conta e sem cartão:

- `Ollama` em container Docker, servindo a API em `http://localhost:11434`;
- modelos abertos puxados para dentro de um volume: `qwen2.5:0.5b`, `qwen2.5:1.5b`, `llama3.2:1b` e `nomic-embed-text`;
- um cliente Python que fala HTTP puro com a biblioteca padrão, sem SDK.

O `docker-compose.yml` do módulo sobe o servidor e persiste os modelos em volume nomeado. Isso importa porque container descartável com modelo embutido baixaria gigabytes toda execução. Com volume, o `pull` acontece uma vez e o container pode morrer e voltar sem custo.

```yaml
services:
  ollama:
    image: ollama/ollama:latest
    container_name: pathbit-ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama
    restart: unless-stopped

volumes:
  ollama-data:
```

Os modelos são puxados de dentro do container:

```bash
docker exec pathbit-ollama ollama pull qwen2.5:0.5b
docker exec pathbit-ollama ollama pull qwen2.5:1.5b
docker exec pathbit-ollama ollama pull llama3.2:1b
docker exec pathbit-ollama ollama pull nomic-embed-text
```

## A anatomia de uma chamada local

![Anatomia da requisição](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0008_llms_locais_ollama/assets/03.png)

> Figura 3: TTFT, tokens de avaliação e vazão decompõem o tempo que a nuvem costuma esconder em uma única latência.

A API do Ollama tem dois modos que interessam para medição. O modo simples devolve a resposta inteira quando termina. O modo em streaming devolve um JSON por token, e é nele que mora a métrica mais honesta de experiência: o tempo até o primeiro token.

```python
def chat_with_metrics(base_url: str, model: str, prompt: str, timeout: float = 300.0) -> dict:
    payload = json.dumps(
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True,
            "options": {"temperature": 0},
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        f"{base_url}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    start = time.perf_counter()
    ttft_ms = None
    content_parts: list[str] = []
    final: dict = {}

    with urllib.request.urlopen(request, timeout=timeout) as response:
        for raw_line in response:
            chunk = json.loads(raw_line.decode("utf-8"))
            piece = chunk.get("message", {}).get("content", "")
            if piece and ttft_ms is None:
                ttft_ms = (time.perf_counter() - start) * 1000
            content_parts.append(piece)
            if chunk.get("done", False):
                final = chunk
                break
    ...
```

Cada chunk em streaming vem sem custo de rede relevante, e o último traz o balanço da chamada: `eval_count` para tokens gerados, `prompt_eval_count` para tokens de entrada e `eval_duration` para o tempo de geração. A vazão em tokens por segundo sai daí, sem estimativa:

```python
tokens_per_second = eval_count / (eval_duration / 1e9)
```

Essa decomposição é o que o laboratório registra em cada linha do CSV. Quando alguém pergunta "por que a resposta demorou", o artefato responde com carga de modelo, tempo até primeiro token e geração, separados.

## O benchmark medido na prática

![Benchmark comparativo](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0008_llms_locais_ollama/assets/04.png)

> Figura 4: Três modelos pequenos, mesmos prompts, mesma máquina: a comparação vira decisão de engenharia.

O runner executa seis prompts de três categorias diferentes: geração de texto, roteamento por classificação e extração de campos. Cada modelo recebe um aquecimento para carregar os pesos na memória antes das medições, e cada prompt roda mais de uma vez.

Os números abaixo foram medidos na máquina de execução deste artigo, em CPU, com o Ollama em container. Numa máquina diferente os valores mudam, e essa é justamente a razão de existir um runner em vez de uma tabela pronta.

| Modelo | TTFT médio | Latência total média | Vazão | JSON válido | Tool correta |
| --- | --- | --- | --- | --- | --- |
| `qwen2.5:0.5b` | 559 ms | 5,49 s | 79,8 tokens/s | 100% | 100% |
| `llama3.2:1b` | 256 ms | 4,33 s | 25,3 tokens/s | 0% | 0% |
| `qwen2.5:1.5b` | 1.022 ms | 6,33 s | 19,4 tokens/s | 100% | 100% |

Médias de seis prompts por modelo em duas repetições, na máquina deste artigo. A primeira chamada de cada bloco carrega o resíduo de carregamento do modelo, e o CSV mantém as duas medições de propósito: esse custo existe em produção também.

O padrão observado derruba o palpite ingênuo de que "modelo maior é sempre melhor":

- o `0.5B` tem a maior vazão e foi o único a combinar vazão com planner perfeito, mas errou todas as classificações zero-shot: respondeu `resposta_direta` para tudo, ignorando a instrução de responder apenas o rótulo;
- o `llama3.2:1b` tem o menor TTFT e a melhor acurácia de classificação (50%), e foi o único a quebrar o JSON: com `format: "json"`, devolveu objeto vazio nas cinco tentativas;
- o `1.5B` é o mais lento e empatou na classificação, com JSON e tool 100%.

Duas lições saem daí. A primeira: decodificação constrangida garante sintaxe, não conteúdo — o JSON vazio do `llama3.2:1b` parseia, e ainda assim não serve para nada. A segunda: prompt zero-shot não basta para roteamento com modelos pequenos. O roteamento híbrido do artigo 0007 existe exatamente por isso, e o teste de JSON do laboratório mostra o caminho: com o formato forçado, o mesmo `0.5B` que errava o rótulo livre escolhe a tool certa em 100% das tentativas.

A coluna que mais diz se o modelo serve para agente não é latência, é a taxa de acerto: se o planner erra a tool, o agente do artigo 0007 executa a ação errada rápido. Velocidade em cima de decisão errada só torna o erro mais frequente.

## Saída estruturada sem depender de sorte

O artigo 0007 mostrou o custo de um plano que não parseia. O Ollama ataca esse problema com o parâmetro `format: "json"`, que restringe a decodificação para produzir JSON válido:

```python
response = http_post_json(
    base_url,
    "/api/generate",
    {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0, "num_predict": 120},
    },
)
```

O laboratório submete cada modelo a tentativas repetidas do mesmo prompt de planner e registra duas taxas: JSON válido e tool correta. A diferença entre os modelos nesse teste é o argumento mais forte para escolher modelo por função, e não por fama.

## Embeddings na mesma instância

![Matriz de decisão](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0008_llms_locais_ollama/assets/05.png)

> Figura 5: A decisão de rodar local depende do caso de uso, e a matriz deixa os critérios explícitos.

O mesmo servidor entrega embeddings com `nomic-embed-text`, no endpoint `/api/embed`. O laboratório roda um retrieval top-1 sobre uma base de oito documentos de suporte com quatro consultas de teste, as mesmas famílias de pergunta dos artigos anteriores.

O resultado relevante: o roteamento semântico que sustentava o fallback do agente do 0007 roda na mesma instância que serve o chat. Um único container cobre o stack completo dos artigos 0002, 0003 e 0007, sem nenhuma chamada externa.

## O que os artefatos atuais mostram de fato

Os arquivos gerados nesta pasta na execução que alimentou este artigo:

- `data/benchmark_resultados.csv` registra cada chamada com modelo, prompt, TTFT, latência total, tokens e vazão;
- `data/benchmark_resumo.csv` consolida por modelo e ordena por vazão;
- `data/structured_output.csv` registra as taxas de JSON válido e tool correta por modelo;
- `data/embedding_routes.csv` registra o retrieval top-1 de cada consulta com o score;
- `data/modelos_disponiveis.json` preserva o snapshot do servidor, versão e modelos, do momento da medição.

Isso significa que os artefatos versionados demonstram com clareza:

- healthcheck do servidor local com versão e lista de modelos;
- benchmark de chat com decomposição de latência;
- saída estruturada com taxa de sucesso por modelo;
- retrieval semântico local com acerto top-1.

E o que o artigo não faz: treinar modelo, afirmar qualidade de raciocínio de longo alcance ou comparar com modelos de fronteira. O escopo é o stack local e a medição honesta dele.

## Show-Me-The-Code

O artigo entrega um laboratório local que:

- sobe Ollama em Docker com volume persistente de modelos;
- verifica o servidor e os modelos antes de medir;
- roda benchmark de chat com TTFT, latência e vazão por modelo;
- testa saída estruturada em JSON com taxa de acerto de tool;
- valida retrieval semântico com embeddings locais;
- gera CSVs, relatório markdown e gráfico comparativo como evidência.

**Opção 1** Suba o Ollama, rode o laboratório e compare os modelos no terminal.

[**Abrir README.md com instruções locais**](https://github.com/pathbit/pathbit-academy-ai/blob/master/0008_llms_locais_ollama/README.md)

**Opção 2** Abra o notebook e acompanhe healthcheck, benchmark, saída estruturada e retrieval passo a passo.

[**Abrir notebook de testes**](https://github.com/pathbit/pathbit-academy-ai/blob/master/0008_llms_locais_ollama/notebooks/llms_locais_ollama.ipynb)

### Pré-requisitos para Execução Local

Antes de executar o laboratório de LLMs locais, configure o ambiente:

1. **Docker:**
   - Verifique com `docker --version`. Se necessário, instale o Docker Desktop em [docker.com](https://www.docker.com/products/docker-desktop/).
   - Não é necessária conta em serviço de registry: a imagem `ollama/ollama` é pública.
2. **Python 3.10 ou superior:**
   - Verifique com `python3 --version`. Se necessário, instale:
     - **macOS:** `brew install python` ou `pyenv install 3.12`
     - **Linux (Ubuntu/Debian):** `sudo apt update && sudo apt install -y python3 python3-venv python3-pip`
     - **Windows:** `winget install Python.Python.3.12`
   - Crie e ative um ambiente virtual dedicado:
     ```bash
     # macOS e Linux
     python3 -m venv .venv
     source .venv/bin/activate

     # Windows (PowerShell)
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - Instale as bibliotecas necessárias:
     ```bash
     pip install --upgrade pip
     pip install -r requirements.txt
     ```
3. **Modelos 100% Locais e Gratuitos:**
   - Não requer chave de API, autenticação ou contas de terceiros.
   - A conexão com a internet é usada apenas para baixar a imagem do Ollama e os modelos abertos na primeira execução.
4. **Execução Local:**
   - Suba o servidor e puxe os modelos:
     ```bash
     docker compose up -d
     docker exec pathbit-ollama ollama pull qwen2.5:0.5b
     docker exec pathbit-ollama ollama pull qwen2.5:1.5b
     docker exec pathbit-ollama ollama pull llama3.2:1b
     docker exec pathbit-ollama ollama pull nomic-embed-text
     ```
   - Rode o laboratório de benchmarks pelo terminal ou abra o notebook:
     ```bash
     # Benchmark completo com artefatos em data/
     python src/ollama_lab.py

     # Ou abrir o launcher do notebook
     python src/main.py
     ```

## Próximos passos

Se você quiser endurecer essa base sem sair do stack gratuito:

1. adicione ao benchmark o modelo que você pretende usar em produção local e compare com os três daqui;
2. conecte o modelo vencedor no agente do artigo 0007 e rode os evals do artigo 0006 em cima dele;
3. experimente `keep_alive` e quantização diferente para medir o impacto no TTFT;
4. em máquinas com GPU, repetir o benchmark e comparar a vazão com esta execução em CPU.

A diferença entre prometer "IA local" e provar "IA local" está nesse detalhe: modelo pequeno, servidor próprio e números medidos na sua máquina.

## Referências

- [Ollama - Documentação e downloads](https://ollama.com)
- [Ollama - Imagem oficial no Docker Hub](https://hub.docker.com/r/ollama/ollama)
- [Qwen 2.5 - Modelo aberto da Alibaba](https://qwenlm.github.io/)
- [Llama 3.2 - Modelo aberto da Meta](https://www.llama.com/)
- [Nomic Embed Text - Modelo aberto de embeddings](https://ollama.com/library/nomic-embed-text)
