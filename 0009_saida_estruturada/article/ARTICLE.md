# Saída Estruturada com LLMs Locais — Do Prompt Otimista ao Contrato Validado

Grande parte dos desenvolvedores que começam a integrar Modelos de Linguagem (LLMs) em sistemas de produção passa pelo mesmo ritual: escreve um prompt detalhado pedindo *"Responda apenas em formato JSON, sem preâmbulos, sem markdown e sem explicações"*, testa três vezes no playground, comemora que funcionou e coloca o serviço em deploy.

Três dias depois, o primeiro incidente em produção acontece: o modelo decidiu responder ```json no início, incluiu uma saudação cortês antes das chaves, trocou o nome de uma chave de `tool` para `ferramenta` ou alucinou um valor fora do `enum` esperado. O backend executa `json.loads()`, estoura uma exceção de sintaxe (`JSONDecodeError`) ou um `KeyError`, e a esteira inteira é interrompida.

No [artigo 0008 da Pathbit Academy](https://github.com/pathbit/pathbit-academy-ai/blob/master/0008_llms_locais_ollama/article/ARTICLE.md), provamos que um stack completo de IA roda 100% local em Docker via Ollama, eliminando custos por token e dependência de nuvem. No entanto, ter o modelo rodando localmente não resolve por si só a fragilidade da interface de saída.

Este artigo aprofunda exatamente essa fronteira: **como transformar a inferência probabilística de um LLM em uma chamada de função determinística e tipada**, comparando empiricamente três níveis de contrato em modelos locais compactos (`Qwen 2.5 0.5B`, `Qwen 2.5 1.5B` e `Llama 3.2 1B`).

---

## 1. Os Três Níveis de Contrato com Modelos de Linguagem

A relação entre código corporativo e LLMs evoluiu em três etapas bem definidas de acoplamento:

![Os Três Níveis de Contrato com LLMs](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0009_saida_estruturada/assets/01.png)

> **Figura 1:** Da incerteza do texto livre à garantia estrita imposta pelo motor de inferência.

### Nível 1: Prompt Otimista (Modo Livre)
O desenvolvedor não utiliza nenhuma restrição nativa da engine de inferência. Todo o peso do contrato recai sobre o prompt textual:
```python
prompt = """Você é um classificador.
Responda EXATAMENTE um JSON com as chaves "produto" e "prazo_dias".
Não use blocos de markdown.
Texto: 'quero devolver um televisor comprado ha 10 dias'"""
```

**O que acontece sob estresse:**
- O modelo envolve a resposta em blocos de código markdown (` ```json ... ``` `).
- Preâmbulos de polidez (*"Aqui está o JSON solicitado:"*) contaminam o payload.
- O parser quebra ou exige regexes e heurísticas frágeis de limpeza manual no backend.

### Nível 2: Modo JSON Sintático (`format: "json"`)
O motor de inferência (como o Ollama ou `llama.cpp`) impõe que a saída seja um JSON sintaticamente válido. O modelo não consegue fechar a requisição sem balancear aspas, chaves e colchetes.

```json
// O motor garante que isso parseia:
{
  "nome_produto": "televisor",
  "prazo": "10 dias"
}
```

**A armadilha oculta:**
O `json.loads()` passa sem erros, mas o schema interno permanece desgovernado. Chaves obrigatórias podem faltar, tipos numéricos podem ser emitidos como strings e, em modelos menores (como demonstrado nos testes com o `llama3.2:1b`), o modelo pode simplesmente devolver `{}` (um objeto JSON válido, porém completamente vazio).

### Nível 3: Contrato Estrito com JSON Schema (`format: <json_schema>`)
O motor recebe uma especificação JSON Schema formal que dita rigorosamente as propriedades permitidas, quais são obrigatórias (`required`), os tipos primitivos estritos (`integer`, `number`, `string`, `boolean`) e os valores finitos permitidos (`enum`).

```python
PLANNER_SCHEMA = {
    "type": "object",
    "properties": {
        "tool": {
            "type": "string",
            "enum": ["buscar_politica", "criar_ticket", "resposta_direta"],
        },
        "confianca": {"type": "number"},
    },
    "required": ["tool", "confianca"],
}
```

Qualquer token que gere uma chave inexistente ou viole a tipagem é matematicamente eliminado da amostragem.

---

## 2. Sob o Capô: Como Funciona o Grammar-Guided Sampling

Para entender por que o **Nível 3** oferece 100% de garantia, é fundamental examinar o ciclo autoregressivo de inferência de um LLM:

![Mecanismo de Decodificação Constrangida](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0009_saida_estruturada/assets/02.png)

> **Figura 2:** Máscara dinâmica de logits via Autômato de Estados Finitos (FSM) a cada token gerado.

1. **Geração dos Logits Não Normalizados:**
   A cada passo $t$, o modelo processa o contexto e calcula um vetor de *logits* $\mathbf{z}_t \in \mathbb{R}^{V}$, onde $V$ é o tamanho do vocabulário (geralmente entre 32.000 e 152.000 tokens). Cada entrada $z_{t, i}$ representa a afinidade estatística do token $i$ ser o próximo.

2. **Compilação do Schema em FSM:**
   Antes de iniciar a geração, a biblioteca de inferência (`llama.cpp` no Ollama) converte a especificação do JSON Schema em uma gramática livre de contexto (Context-Free Grammar / BNF) ou em um Autômato de Estados Finitos (FSM).

3. **Aplicação da Máscara de Logits (Logits Masking):**
   No estado atual do autômato, apenas um subconjunto $S_t \subset V$ de tokens preserva a legalidade da gramática. Os tokens proibidos têm seus logits forçados para $-\infty$:
   $$\tilde{z}_{t, i} = \begin{cases} z_{t, i} & \text{se } i \in S_t \\ -\infty & \text{se } i \notin S_t \end{cases}$$

4. **Amostragem Segura (Softmax):**
   Ao aplicar a função Softmax sobre os logits mascarados, a probabilidade dos tokens inválidos torna-se exatamente zero:
   $$P(\text{token}_i) = \frac{e^{\tilde{z}_{t, i}}}{\sum_{j \in S_t} e^{\tilde{z}_{t, j}}}$$

Dessa forma, o modelo é **estruturalmente incapaz** de gerar um caractere que quebre as aspas de fechamento antes do valor, de emitir uma propriedade não declarada ou de violar um enum.

---

## 3. O Experimento e Evidências Empíricas

Construímos um laboratório automatizado (`src/structured_lab.py`) testando 3 tarefas reais de engenharia corporativa:

| ID da Tarefa | Descrição do Caso de Uso | Contrato Esperado | Critério Semântico |
| :--- | :--- | :--- | :--- |
| `planner` | Escolha de tool para segunda via de fatura | `tool` (enum), `confianca` (float) | `tool == 'buscar_politica'` |
| `extracao` | Extração de devolução de televisor em 10 dias | `produto` (string), `prazo_dias` (integer) | `prazo_dias == 10` e televisor |
| `roteamento` | Triagem de erro 500 em app de cliente | `rota` (enum), `urgencia` (enum) | `rota == 'criar_ticket'` e `urgencia == 'alta'` |

Testamos 3 modelos em CPU, com 54 chamadas distribuídas uniformemente:
- `qwen2.5:0.5b` (ultraleve, 494M parâmetros)
- `qwen2.5:1.5b` (balanceado, 1.5B parâmetros)
- `llama3.2:1b` (1.2B parâmetros)

![Resultados Comparativos Medidos](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0009_saida_estruturada/assets/03.png)

> **Figura 3:** Taxa de parse direto, conformidade formal com schema e assertividade semântica medida.

### Resultados Consolidados por Modo

| Modo de Execução | Parse OK (%) | Schema Valid (%) | Acerto Semântico (%) | Latência Média (ms) |
| :--- | :---: | :---: | :---: | :---: |
| **Livre (Prompt Only)** | 72.2% | 55.6% | 44.4% | ~1.150 ms |
| **JSON (`format: "json"`)** | 100.0% | 66.7% | 55.6% | ~1.210 ms |
| **Schema (`format: <schema>`)** | **100.0%** | **100.0%** | **94.4%** | ~1.380 ms |

### Conclusões Críticas do Experimento:
1. **O modo livre quebra em quase 30% das chamadas:** O modelo 0.5B frequentemente insere marcações de markdown e texto explicativo antes ou depois do JSON.
2. **O modo JSON resolve a sintaxe, mas não o negócio:** Em 33.3% das vezes, as propriedades vieram com nomes incorretos ou em formato incompatível.
3. **Impor Schema aumenta a assertividade semântica:** Quando o modelo não precisa gastar parâmetros decidindo *como formatar*, toda a capacidade neural é focada em *qual dado escolher*. O acerto semântico subiu de 44.4% para 94.4%!

---

## 4. O Mito do Retry Compensatório e o Trade-off de Latência

Uma prática frequente em pipelines frágeis é o loop de retry baseado em prompt: quando o backend falha ao parsear o JSON, ele monta um segundo prompt contendo a mensagem de erro do parser e reenvia ao LLM:

![Trade-off de Latência e Retry](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0009_saida_estruturada/assets/04.png)

> **Figura 4:** O custo real do retry em relação ao overhead da gramática.

### Por que o retry reativo é prejudicial:
- **Duplicação de Latência:** Uma chamada que falha na primeira tentativa e tem sucesso no retry consome no mínimo o dobro do tempo total de resposta (~2.400 ms vs ~1.300 ms).
- **Incerteza Cumulativa:** Se o modelo não conseguiu seguir o formato na primeira vez, a chance de reincidir no erro na segunda chamada com o mesmo contexto permanece alta.
- **Sobrecarga Computacional:** Em cenários de alta concorrência local, dobrar o número de requisições satura os núcleos de CPU da máquina.

### A Abordagem Correta de Engenharia:
- **Primeira Chamada Determinística:** Sempre use `temperature = 0.0` com JSON Schema estrito. O overhead de mascaramento de logits adiciona menos de 200 ms, garantindo 100% de parseabilidade no primeiro disparo.
- **Retry Exclusivo para Semântica:** O retry deve existir apenas para cenários onde o JSON é matematicamente válido, mas uma regra de negócio externa rejeitou o valor (por exemplo, um ID inexistente no banco de dados).

---

## 5. Padrão Arquitetural de Integração em Produção

Para aplicar saída estruturada em arquiteturas corporativas modernas, estruturamos o pipeline em 4 etapas desacopladas:

![Arquitetura de Integração em Produção](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0009_saida_estruturada/assets/05.png)

> **Figura 5:** Integração limpa e tipada entre LLMs locais e serviços de backend.

### Exemplo de Implementação com Python e Pydantic:

```python
import json
import urllib.request
from pydantic import BaseModel, Field
from typing import Literal

# 1. Definição do Contrato via Pydantic
class ClassificacaoSuporte(BaseModel):
    tool: Literal["buscar_politica", "criar_ticket", "resposta_direta"]
    confianca: float = Field(ge=0.0, le=1.0)
    motivo: str

# 2. Extração do JSON Schema do Modelo
SCHEMA_CONTRATO = ClassificacaoSuporte.model_json_schema()

# 3. Invocação do Ollama com o Schema Embutido
def invocar_llm_estruturado(prompt: str) -> ClassificacaoSuporte:
    payload = json.dumps({
        "model": "qwen2.5:0.5b",
        "prompt": prompt,
        "stream": False,
        "format": SCHEMA_CONTRATO,
        "options": {"temperature": 0.0}
    }).encode("utf-8")

    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        dados = json.loads(res.read().decode("utf-8"))

    # 4. Deserialização Determinística Direta (Sem risco de KeyError ou JSONDecodeError)
    return ClassificacaoSuporte.model_validate_json(dados["response"])
```

---

## 6. Como Executar o Laboratório Localmente

### Opção 1: Execução do Benchmark Automatizado pelo Terminal
Suba o servidor Ollama (conforme o artigo 0008) e execute o benchmark:

```bash
# Subir o Ollama se ainda não estiver em execução
cd pathbit-academy-ai/0008_llms_locais_ollama
docker compose up -d

# Executar o laboratório de saída estruturada
cd ../0009_saida_estruturada
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Rodar a matriz comparativa completa
python3 src/structured_lab.py --repeat 2
```

Os artefatos gerados (CSVs, gráfico comparativo e relatório markdown) serão salvos automaticamente na pasta `data/`.

### Opção 2: Notebook Interativo
Execute o launcher para abrir o Jupyter Notebook passo a passo:

```bash
python3 src/main.py
```

---

## 7. Próximos Passos e Continuidade

A garantia de saída estruturada fecha o elo que faltava entre o **modelo local (0008)** e a **capacidade de ação no mundo real**.

No próximo artigo, **[0010 - MCP Local](https://github.com/pathbit/pathbit-academy-ai/blob/master/0010_mcp_local/article/ARTICLE.md)**, conectamos a saída estruturada ao protocolo aberto **Model Context Protocol (MCP)** da Anthropic:
- Servidor MCP rodando localmente via `stdio` (sem rede e sem chaves).
- Descoberta dinâmica de ferramentas com conversão automática de schemas.
- Planejamento, invocação e trilha de auditoria para agentes corporativos locais.

---

## Referências

- [Ollama Structured Outputs Documentation](https://ollama.com/blog/structured-outputs)
- [JSON Schema Specification (Draft 2020-12)](https://json-schema.org/)
- [llama.cpp Grammar-Based Sampling Implementation](https://github.com/ggerganov/llama.cpp/blob/master/grammars/README.md)
- [Pydantic: Data validation using Python type hints](https://docs.pydantic.dev/)
