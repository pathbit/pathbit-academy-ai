Você não precisa de chave de API, cartão corporativo nem internet aberta para rodar uma stack de IA séria em produção.

A maioria esmagadora dos tutoriais de inteligência artificial parte de uma premissa conveniente: uma chamada para uma API externa com cobrança por token. Isso funciona para protótipos de fim de semana, mas em sistemas corporativos sensíveis essa dependência cobra um preço alto em soberania de dados, instabilidade de versões e latência imprevisível.

No módulo 0008 da Pathbit Academy, mostramos como rodar uma stack completa de IA 100% offline dentro de containers Docker, consumida via Python padrão e sem gastar um centavo em tokens.

Montamos um servidor com Ollama gerenciando quatro modelos abertos em paralelo, cobrindo raciocínio conversacional, saídas estruturadas e embeddings locais para busca semântica na mesma máquina. Medimos o tempo até o primeiro token, a taxa de avaliação de prompt e a vazão real em CPU pura.

Os dados medidos desmistificam ideias comuns. O modelo Qwen 2.5 0.5B, com menos de 400 MB de memória, entregou quase 80 tokens por segundo em CPU e acertou todas as ferramentas sob decodificação constrangida. Já o Llama 3.2 1B foi muito rápido no primeiro token, mas sob JSON genérico sem schema devolveu um objeto vazio, provando que decodificação sintática garante chaves válidas, mas não garante o conteúdo exigido pelo negócio.

O laboratório completo, com scripts de benchmark, docker-compose, notebook interativo e deck de slides, está disponível no nosso repositório de código aberto.

Repositório no GitHub: https://github.com/pathbit/pathbit-academy-ai
Módulo: 0008_llms_locais_ollama

#InteligenciaArtificial #LLM #Ollama #Docker #OpenSource #Python #PathbitAcademy #LocalAI #SoftwareEngineering
