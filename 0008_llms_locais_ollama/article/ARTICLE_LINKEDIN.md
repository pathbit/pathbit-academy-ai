# LLMs locais com Ollama: stack de IA sem nuvem, sem chave e sem custo por token

Grande parte do material sobre IA em produção assume uma chave de API no meio do caminho. Para aprender, demonstrar ou rodar um piloto sensível, essa dependência atrapalha: você não controla latência, versão nem o dado.

O artigo 0008 da série Pathbit Academy prova o caminho contrário:

🐳 Ollama em Docker, com volume persistente de modelos
🧠 Modelos abertos: qwen2.5:0.5b, qwen2.5:1.5b, llama3.2:1b e nomic-embed-text
📡 API local em http://localhost:11434, consumida com Python padrão, sem SDK
📊 Benchmark medido na própria máquina: TTFT, latência total e vazão em tokens/s

O que os números da execução mostraram:

→ O 0.5B tem a maior vazão (79,8 tokens/s) e acertou 100% da tool com JSON forçado
→ O llama3.2:1b tem o menor TTFT (256 ms) — e devolveu JSON vazio nas 5 tentativas
→ Sem constraint, o 0.5B errou 100% da classificação zero-shot: decodificação constrangida muda o jogo
→ Retrieval top-1 com nomic-embed-text: 4/4 de acerto na mesma instância

Rodar local não é só economizar: a latência de rede vira loopback, o custo por token vira memória da máquina, o dado nunca sai do ambiente e a versão do modelo fica congelada no container.

O laboratório entrega evidência completa: CSV linha a linha, gráfico comparativo e relatório markdown gerados em um comando.

Artigo completo, código, notebook e artefatos medidos:
👉 https://github.com/pathbit/pathbit-academy-ai/tree/master/0008_llms_locais_ollama


#InteligenciaArtificial #LLM #Ollama #Docker #OpenSource
