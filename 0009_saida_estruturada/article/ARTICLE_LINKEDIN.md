# Saída Estruturada com LLMs Locais: Do Prompt Otimista ao Contrato Formal e a Fronteira System 1

"Responda apenas em formato JSON, sem markdown e sem explicações."
Quem nunca escreveu esse prompt na esperança de integrar um LLM ao backend?

No primeiro dia funciona. No primeiro incidente de produção, o modelo decide prefixar a resposta com ```json, insere uma saudação educada antes das chaves ou troca a chave `tool` por `ferramenta`. O backend roda `json.loads()`, estoura `JSONDecodeError` e a esteira corporativa inteira para.

No **Artigo 0009 da Pathbit Academy**, demonstramos como sair do "prompt otimista" e implementar saída estruturada com garantias matemáticas estritas e apresentamos a nova fronteira de **Modelos System 1**:

### 🛡️ A Evolução dos 3 Níveis de Contrato:
1. **Modo Livre (Prompt Only):** O modelo emite texto aberto. Quase **30% das chamadas** sequer passam no parse direto, com assertividade semântica de míseros 44.4%.
2. **Modo JSON Sintático (`format: "json"`):** Garante abertura e fechamento de chaves válidas (100% de parse_ok), mas o schema interno permanece desgovernado: o modelo alucina chaves ou devolve `{}` vazio.
3. **Contrato Estrito (`format: <json_schema>`):** O JSON Schema é compilado em um **Autômato de Estados Finitos (FSM)** no motor de inferência (`llama.cpp`/Ollama). A cada token gerado, qualquer caractere que viole a gramática recebe logit = -∞ (probabilidade zero).

### ⚡ A Nova Fronteira: Modelos System 1 (Jev vs Laya)
Por que gastar 40 a 60 passos autoregressivos na CPU gerando aspas, chaves e colchetes se o sistema precisa apenas de uma decisão tipada?
Apresentamos a separação cognitiva inspirada em Daniel Kahneman:
- **System 2 (Decoder Autoregressivo):** Lento e sequencial ($O(N)$), ideal para redação de texto livre. Latência de 400 ms a 2.200 ms.
- **System 1 (Encoder de Passada Única):** Single Forward Pass em $O(1)$ sobre encoders dedicados (ModernBERT), avaliando primitivas universais: `Choice` (enum), `Score` (escala contínua) e `Bool`/`Noul` (portão binário).
- **No mercado:** **Jev** (TypeSafe AI, API cloud proprietária por Diogo Almeida) vs **Laya & Kev** (Convai Innovations, Apache 2.0 open-weights rodando 100% offline em hardware local).

### 📊 O que os números medidos na máquina revelaram:
• **Conformidade Formal:** O modo Schema atingiu **100% de conformidade** com os schemas e **94.4% de acerto semântico** no Ollama.
• **Velocidade Extrema com System 1:** O decisor System 1 executou com **100% de precisão em apenas 12.97 ms** (p50: 13.61 ms), superando o LLM autoregressivo em **mais de 30x**.
• **O Mito do Retry:** Reenviar erros de sintaxe para o modelo em loop dobra a latência. Impor schema ou System 1 resolve na primeira tentativa.

Artigo completo, diagramas técnicos em 1920x1080, laboratório em Python com Pydantic v2 e deck em PDF disponíveis:

👉 Artigo completo e código: https://github.com/pathbit/pathbit-academy-ai/tree/master/0009_saida_estruturada

#EngenhariaDeSoftware #InteligenciaArtificial #LLM #Ollama #JSONSchema #Python #PathbitAcademy #SystemOne #Pydantic
