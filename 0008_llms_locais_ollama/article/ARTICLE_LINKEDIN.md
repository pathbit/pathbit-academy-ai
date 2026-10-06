# LLMs Locais com Ollama: Como Provar uma Stack de IA 100% Offline sem Custos por Token

A maioria dos tutoriais de IA em produção começa com uma premissa perigosa: `client = OpenAI(api_key=...)`. Para protótipos de fim de semana, isso funciona. Mas em sistemas corporativos de missão crítica, operações de alta frequência ou ambientes com dados estritamente sensíveis (LGPD / HIPAA / Open Finance), essa dependência externa cobra um pedágio invisível:
❌ Você não controla a latência (ela oscila com a rede pública e filas de provedores).
❌ Você não controla a versão (o modelo de nuvem muda silenciosamente).
❌ O dado trafega fora do perímetro da sua infraestrutura.
❌ Cada loop de reflexão ou benchmark contínuo consome créditos de alguém.

No **Artigo 0008 da Pathbit Academy**, provamos o caminho da engenharia: montamos uma stack completa de IA rodando 100% local em container Docker via Ollama, consumida via HTTP puro em loopback, com medição cirúrgica de telemetria.

### 🐳 O que construímos na prática:
1. **Servidor Local em Docker com Volume Persistente:** O Ollama roda isolado, mantendo modelos congelados em disco via volume nomeado (`ollama-data`). Sem recarregar gigabytes a cada reinício de container.
2. **Quatro Modelos Abertos Coexistindo:** `qwen2.5:0.5b`, `qwen2.5:1.5b` e `llama3.2:1b` para chat e planejamento agêntico; `nomic-embed-text` para busca vetorial semântica.
3. **Decomposição Cirúrgica de Latência:** Medição em CPU de TTFT (Time to First Token), tempo de avaliação de prompt e vazão real (tokens/segundo). Sem a nuvem esconder os gargalos reais da máquina.
4. **Decodificação Constrangida (JSON Forçado):** Provamos como o parâmetro `format: "json"` garante sintaxe 100% parseável mesmo em modelos compactos de 500 milhões de parâmetros.
5. **Retrieval Vetorial na Mesma Instância:** Classificação semântica por similaridade de cosseno com embeddings gerados localmente (100% de acerto top-1 nos testes).

### 📊 O que os números medidos na máquina revelaram:
• **Vazão Brutal:** O Qwen 2.5 0.5B atingiu quase **80 tokens/segundo em CPU**, com 100% de precisão de tool calling sob JSON forçado.
• **A Armadilha do TTFT:** O Llama 3.2 1B entregou o menor TTFT (**256 ms**), mas decodificação sem schema devolveu JSON vazio: provando que decodificação constrangida sintática garante formato, não semântica de negócio.
• **Zero Custo Variável:** A latência de rede vira loopback (< 1 ms), o custo por token vira capacidade de hardware e os dados jamais saem do perímetro.

Todo o laboratório, docker-compose, scripts de benchmark, notebook interativo e deck de apresentação em PDF estão disponíveis no repositório open-source:

👉 Artigo completo e código: https://github.com/pathbit/pathbit-academy-ai/tree/master/0008_llms_locais_ollama

#InteligenciaArtificial #LLM #Ollama #Docker #OpenSource #Python #PathbitAcademy #LocalAI #SoftwareEngineering
