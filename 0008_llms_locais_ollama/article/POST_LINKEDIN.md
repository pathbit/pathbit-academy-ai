Você não precisa de chave de API, cartão corporativo nem internet para rodar IA de verdade.

A maioria esmagadora dos tutoriais e projetos de IA começa com uma dependência silenciosa: `api_key = os.getenv("OPENAI_API_KEY")`.

Isso funciona para protótipos, mas em ambientes corporativos sensíveis, laboratórios de engenharia ou sistemas offline, essa dependência trava tudo:
❌ Você não controla a latência (ela varia com a rede mundial e filas do provedor).
❌ Você não controla a versão (o modelo de nuvem muda silenciosamente).
❌ O dado sai da sua infraestrutura.
❌ Cada teste, loop de agente ou benchmark consome créditos de alguém.

No módulo 0008 do Pathbit Academy AI, provamos que uma stack completa de IA roda 100% local, dentro do Docker, consumida via Python padrão:

🐳 O que montamos na prática:
1. Servidor de Inferência Local:
Ollama rodando em container Docker com volume persistente de modelos (`ollama-data`). Sem recarregar gigabytes a cada reinício.

2. Quatro Modelos Abertos Coexistindo:
`qwen2.5:0.5b`, `qwen2.5:1.5b`, `llama3.2:1b` para raciocínio/chat e `nomic-embed-text` para busca vetorial semântica.

3. Decomposição Honesta de Latência:
Medição precisa em CPU de TTFT (Time to First Token), tempo de avaliação e vazão real (tokens/segundo). Sem a nuvem esconder o gargalo.

4. Decodificação Constrangida (JSON Forçado):
Provamos como o `format: "json"` garante sintaxe 100% parseável mesmo em modelos ultraleves de 0.5B parâmetros.

5. Retrieval Semântico na Mesma Instância:
Classificação e busca vetorial por similaridade de cosseno com embeddings gerados localmente (4/4 de acerto nos testes).

📊 O que os números medidos na máquina revelaram:
• O Qwen 2.5 0.5B atingiu quase 80 tokens/s em CPU, com 100% de precisão de tool calling sob JSON forçado.
• O Llama 3.2 1B entregou menor TTFT (~250 ms), mas decodificação sem schema devolveu JSON vazio: provando que decodificação constrangida garante sintaxe, não semântica.
• Sem chave, sem cadastro, sem faturamento por token.

Todo o laboratório, scripts executáveis, docker-compose, notebook e deck em PDF estão disponíveis no repositório open-source:

🔗 Repositório oficial: https://github.com/pathbit/pathbit-academy-ai
📖 Módulo: 0008_llms_locais_ollama

#InteligenciaArtificial #LLM #Ollama #Docker #OpenSource #Python #PathbitAcademy #LocalAI
