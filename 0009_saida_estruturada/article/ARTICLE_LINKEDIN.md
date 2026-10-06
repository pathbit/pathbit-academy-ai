# Saída Estruturada com LLMs Locais — Do Prompt Otimista ao Contrato Formal e a Fronteira dos Modelos System 1

Grande parte dos desenvolvedores que começam a integrar Modelos de Linguagem (LLMs) em sistemas de produção corporativos passa pelo mesmo ritual: escreve um prompt detalhado pedindo:
> *"Você é um assistente de triagem. Responda APENAS em formato JSON, sem preâmbulos, sem markdown, sem explicações e com aspas duplas válidas."*

O desenvolvedor testa três vezes no terminal, comemora que o resultado veio em formato de dicionário e coloca o serviço em deploy na sexta-feira à tarde.

Na segunda-feira de manhã, o primeiro incidente de severidade alta acontece: o modelo decidiu prefixar a resposta com ```json na primeira linha, inseriu uma saudação cortês antes das chaves, trocou o nome da chave `status` por `situacao`, formatou um valor monetário como string `"$ 1.500,00"` em vez de float `1500.0` ou alucinou uma opção inexistente fora do `enum` esperado. O backend executa `json.loads()`, estoura uma exceção fatal de sintaxe (`JSONDecodeError`) ou um `KeyError`, e a esteira inteira de atendimento é interrompida.

No [Artigo 0008 da Pathbit Academy](https://github.com/pathbit/pathbit-academy-ai/blob/master/0008_llms_locais_ollama/article/ARTICLE.md), provamos como rodar uma stack completa de IA 100% local em Docker via Ollama, eliminando custos por token e dependências de nuvem. No entanto, ter o modelo rodando localmente não resolve por si só a fragilidade da interface de saída.

Este artigo aprofunda exatamente essa fronteira crítica de engenharia: **como transformar a inferência probabilística de um LLM em uma chamada de função determinística e fortemente tipada**, comparando empiricamente três níveis de contrato em modelos locais compactos (`Qwen 2.5 0.5B`, `Qwen 2.5 1.5B` e `Llama 3.2 1B`), e apresentando a nova fronteira da indústria de IA: os **Modelos System 1 (Jev vs Laya)** para decisões instantâneas em passada única.

---

## 1. Os Três Níveis de Contrato entre LLMs e Software Corporativo

A relação entre código de engenharia e modelos de linguagem evoluiu através de três paradigmas bem definidos de acoplamento:

![Os Três Níveis de Contrato com LLMs](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0009_saida_estruturada/assets/01.png)

> **Figura 1:** Da incerteza do texto livre à garantia matemática estrita imposta pelo motor de inferência.

### Nível 1: Prompt Otimista (Modo Livre)
Neste modelo inicial, o desenvolvedor não utiliza nenhuma restrição nativa do motor de inferência. Todo o peso do contrato recai sobre o prompt textual:

```python
prompt = """Você é um assistente de suporte.
Responda EXATAMENTE um JSON com as chaves "produto" e "prazo_dias".
Não inclua explicações nem blocos markdown.
Entrada: 'Quero devolver uma televisão comprada há 10 dias.'"""
```

**Por que o Nível 1 quebra em produção:**
- **Markdown Fences:** O modelo foi treinado em corpus massivo do GitHub e StackOverflow. Quando ele "vê" um JSON, a probabilidade estatística do próximo token ser ` ```json ` é altíssima.
- **Preâmbulos e Epílogos de Cortesia:** Frases como *"Com certeza! Aqui está o JSON que você pediu:"* ou *"Espero ter ajudado!"* poluem a resposta antes e depois das chaves.
- **Manutenção Frágil via Regex:** O time de backend cria heurísticas artesanais para encontrar a primeira `{` e a última `}`, mas qualquer caractere de chave desbalanceada dentro de uma string quebra a regex.
- **Nos nossos testes medidos:** Quase **30% das chamadas** sequer passam no `json.loads()`, e a assertividade de negócio desaba para **44.4%**.

### Nível 2: Modo JSON Sintático (`format: "json"`)
O motor de inferência (como o Ollama ou `llama.cpp`) restringe a decodificação para forçar que a sequência de tokens gerada seja um documento JSON sintaticamente válido. O modelo não consegue concluir a geração sem fechar aspas, vírgulas e chaves.

```json
// O parser garante que isto é sintaticamente válido:
{
  "item_retornado": "televisão",
  "dias_passados": "10 dias"
}
```

**A armadilha oculta do Nível 2:**
O `json.loads()` executa com sucesso sem lançar exceções de sintaxe. No entanto, **o schema interno permanece desgovernado**:
1. **Chaves Alucinadas:** O modelo trocou `produto` por `item_retornado`, provocando um `KeyError` no backend downstream.
2. **Tipos Incompatíveis:** O campo `prazo_dias` veio como string formatada (`"10 dias"`) em vez de inteiro (`10`).
3. **O Fenômeno do Objeto Vazio `{}`:** Em nossos experimentos com o `llama3.2:1b`, sob `format: "json"` genérico, o modelo descobriu que devolver `{}` cumpria 100% da restrição sintática de ser um JSON válido — devolvendo um objeto vazio em todas as tentativas!

### Nível 3: Contrato Formal com JSON Schema (`format: <json_schema>`)
O motor de inferência recebe uma especificação JSON Schema formal (Draft 7 / Draft 2020-12) que dita rigorosamente:
- Os nomes exatos das propriedades permitidas;
- A lista de propriedades estritamente obrigatórias (`required`);
- Os tipos primitivos estritos (`string`, `integer`, `number`, `boolean`, `array`);
- O conjunto fechado de valores permitidos para categorias (`enum`).

```python
PLANNER_SCHEMA = {
    "type": "object",
    "properties": {
        "tool": {
            "type": "string",
            "enum": ["buscar_politica", "criar_ticket", "resposta_direta"],
        },
        "confianca": {"type": "number", "minimum": 0.0, "maximum": 1.0},
    },
    "required": ["tool", "confianca"],
    "additionalProperties": False,
}
```

Qualquer token do vocabulário que gere uma chave inexistente, viole a tipagem ou escape do enum é matematicamente eliminado da amostragem em tempo real.

---

## 2. Sob o Capô: A Matemática do Grammar-Guided Sampling

Para compreender por que o **Nível 3** oferece 100% de garantia estrutural sem quebras de parse, é indispensável analisar o ciclo de geração autoregressiva de um LLM:

![Mecanismo de Decodificação Constrangida](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0009_saida_estruturada/assets/02.png)

> **Figura 2:** Máscara dinâmica de logits guiada por Autômato de Estados Finitos (FSM) a cada token gerado.

### 2.1. O Ciclo Autoregressivo Padrão
A cada passo de tempo $t$, o modelo processa o contexto acumulado e calcula um vetor de *logits* não normalizados:
$$\mathbf{z}_t = [z_{t, 1}, z_{t, 2}, \dots, z_{t, V}] \in \mathbb{R}^V$$
onde $V$ é o tamanho do vocabulário do tokenizer (ex: 152.064 tokens no Qwen 2.5 ou 128.256 tokens no Llama 3.2).

Em amostragem livre com temperatura $T$, a probabilidade de escolher o token $i$ é calculada via Softmax:
$$P(\text{token}_i) = \frac{e^{z_{t, i} / T}}{\sum_{j=1}^V e^{z_{t, j} / T}}$$

### 2.2. Da Especificação JSON Schema à Máquina de Estados Finitos (FSM)
Antes de iniciar a geração do primeiro token, o motor de inferência (`llama.cpp` no Ollama) compila a especificação JSON Schema em uma Gramática Livre de Contexto (CFG / EBNF) e a converte em um **Autômato de Estados Finitos (FSM)**:
- **Estado 0:** Início. O único caractere permitido pela gramática é `{`.
- **Estado 1:** Chave obrigatória. O autômato só permite tokens que comecem com `"tool"` ou `"confianca"`.
- **Estado 2:** Dois-pontos `:`.
- **Estado 3:** Valor do enum. Se a chave foi `"tool"`, os únicos tokens permitidos são `"buscar_politica"`, `"criar_ticket"` ou `"resposta_direta"`.

### 2.3. A Aplicação Física da Máscara de Logits (Logits Masking)
No estado atual da FSM $S_t$, calcula-se o conjunto de tokens válidos $V_{\text{válidos}}(S_t) \subset V$. Para todos os tokens ilegais, o valor do logit é sobrescrito para $-\infty$:

$$\tilde{z}_{t, i} = \begin{cases} z_{t, i}, & \text{se } i \in V_{\text{válidos}}(S_t) \\ -\infty, & \text{se } i \notin V_{\text{válidos}}(S_t) \end{cases}$$

Ao aplicar a função Softmax sobre o vetor mascarado $\mathbf{\tilde{z}}_t$:
$$e^{-\infty} = 0 \implies P(\text{token inválido}) \equiv 0.00000\%$$

### 2.4. O Efeito de Redistribuição de Massa de Probabilidade
Aqui reside uma das maiores surpresas de engenharia dos nossos benchmarks: **o modelo não fica apenas sintaticamente correto; ele fica mais inteligente!**

Em geração livre, o modelo gasta parte considerável de sua capacidade probabilística tentando balancear vírgulas, fechar aspas e adivinhar sinônimos de chaves. Ao zerar os logits de tudo que não faz parte do schema, a massa total de probabilidade é redistribuída exclusivamente entre as opções válidas. A capacidade neural do modelo é direcionada 100% para o problema semântico: escolher o melhor valor para o campo.

---

## 3. O Experimento e Evidências Empíricas

Construímos um laboratório automatizado (`src/structured_lab.py`) testando 3 casos de uso corporativos reais:
1. **Planner de Suporte:** Decidir entre `buscar_politica`, `criar_ticket` ou `resposta_direta` com score de confiança float.
2. **Extração de Entidades:** Extrair nome do produto (string) e prazo de devolução (inteiro estrito) a partir de mensagem informal de cliente.
3. **Triagem de Incidentes:** Classificar rota operacional e nível de urgência (`baixa`, `media`, `alta`).

Avaliamos 3 modelos locais em CPU, com 54 execuções distribuídas uniformemente:
- `qwen2.5:0.5b` (494M parâmetros);
- `qwen2.5:1.5b` (1.5B parâmetros);
- `llama3.2:1b` (1.2B parâmetros).

![Resultados Comparativos Medidos](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0009_saida_estruturada/assets/03.png)

> **Figura 3:** Taxa de parse direto, conformidade formal com schema e assertividade semântica medida na máquina.

### Resultados Consolidados por Modo de Contrato:

| Modo de Contrato | Parse OK (%) | Conformidade de Schema (%) | Acurácia Semântica de Negócio (%) | Latência Média por Chamada |
| :--- | :---: | :---: | :---: | :---: |
| **Livre (Prompt Only)** | 72.2% | 55.6% | 44.4% | ~1.150 ms |
| **JSON Sintático (`format: "json"`)** | 100.0% | 66.7% | 55.6% | ~1.210 ms |
| **JSON Schema Estrito (`format: <schema>`)** | **100.0%** | **100.0%** | **94.4%** | **~1.380 ms** |

### Conclusões Críticas do Experimento:
1. **O modo livre é inaceitável em produção:** Quase um terço das requisições gerou exceções de parse no backend. Pior ainda: mais da metade das respostas válidas errou a semântica do negócio.
2. **O modo `format: "json"` é uma falsa sensação de segurança:** Embora o `json.loads` passe em 100% das vezes, 33.3% das respostas continham schemas corrompidos, chaves ausentes ou objetos vazios.
3. **JSON Schema impõe qualidade de negócio:** A acurácia semântica saltou de 44.4% para incríveis **94.4%**. O overhead computacional de mascarar logits adicionou em média apenas **170 ms** — um custo ínfimo em troca de 100% de confiabilidade contratual.

---

## 4. O Mito do Retry Compensatório e o Custo Real de Latência

Uma prática amplamente difundida (e prejudicial) na comunidade é o loop de retry reativo: quando o backend falha ao parsear a saída do LLM, ele monta um segundo prompt contendo a mensagem de erro da exceção e reenvia para o modelo tentar se corrigir:

![Trade-off de Latência e Retry](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0009_saida_estruturada/assets/04.png)

> **Figura 4:** O custo real do retry reativo em comparação ao overhead desprezível da máscara de gramática.

### Por que o retry reativo é um anti-padrão de engenharia:
1. **Duplicação de Latência:** Uma requisição que falha e precisa de retry consome o dobro do tempo total de resposta (~2.400 ms vs ~1.380 ms). Em agentes encadeados, essa latência se multiplica exponencialmente.
2. **Incerteza Cumulativa:** Se o modelo já demonstrou fraqueza estatística para seguir o formato no primeiro disparo, a probabilidade de reincidir em erros sutis no segundo disparo com o mesmo contexto permanece alta.
3. **Consumo de Concorrência Local:** Em servidores on-premise com CPU compartilhada, disparar retries duplica a saturação dos núcleos, penalizando outros usuários simultâneos.

> **Regra de Ouro da Pathbit:** Utilize decodificação constrangida com JSON Schema na **primeira chamada**. O retry deve existir exclusivamente para tratar regras de negócio semânticas externas (ex: uma chave primária que não existe no banco de dados relacional), e nunca para corrigir erros de sintaxe ou enumeração.

---

## 5. Implementação de Produção com Pydantic v2

Em sistemas enterprise em Python, o schema não deve ser escrito manualmente em dicionários JSON suscetíveis a erros de digitação. Utilizamos **Pydantic v2**, aproveitando sua integração nativa com JSON Schema e deserialização de alta velocidade em Rust:

![Arquitetura de Integração em Produção](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0009_saida_estruturada/assets/05.png)

> **Figura 5:** Pipeline limpo, desacoplado e tipado entre LLMs locais e serviços de backend.

```python
import json
import urllib.request
from typing import Literal
from pydantic import BaseModel, Field, field_validator

# 1. Definição do Contrato Tipado via Pydantic v2
class PlanoAtendimento(BaseModel):
    tool: Literal["buscar_politica", "criar_ticket", "resposta_direta"] = Field(
        description="Ferramenta operacional necessária para atender a solicitação."
    )
    confianca: float = Field(
        ge=0.0, le=1.0, description="Nível de certeza matemática da decisão entre 0 e 1."
    )
    justificativa: str = Field(
        description="Breve raciocínio que fundamentou a escolha da ferramenta."
    )

    @field_validator("justificativa")
    def validar_justificativa(cls, v: str) -> str:
        if len(v.strip()) < 5:
            raise ValueError("Justificativa muito curta.")
        return v

# 2. Extração Automática do JSON Schema
SCHEMA_PLANO = PlanoAtendimento.model_json_schema()

# 3. Invocação Constrangida do Ollama
def executar_triagem_estruturada(pergunta_cliente: str, base_url: str = "http://localhost:11434") -> PlanoAtendimento:
    prompt = f"Analise a solicitação do cliente e decida o plano de ação: '{pergunta_cliente}'"
    
    payload = json.dumps({
        "model": "qwen2.5:0.5b",
        "prompt": prompt,
        "stream": False,
        "format": SCHEMA_PLANO,
        "options": {"temperature": 0.0, "num_predict": 128}
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{base_url}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    
    with urllib.request.urlopen(req, timeout=30) as res:
        resposta_raw = json.loads(res.read().decode("utf-8"))

    # 4. Deserialização e Validação em Rust (Sem try/except de JSONDecodeError)
    plano_validado: PlanoAtendimento = PlanoAtendimento.model_validate_json(resposta_raw["response"])
    return plano_validado
```

Se o código acima for executado 10.000 vezes, **em nenhuma delas ocorrerá `JSONDecodeError` ou `ValidationError` de propriedades faltantes**. O contrato é fisicamente assegurado na amostragem de cada token.

---

## 6. A Nova Fronteira: Modelos "System 1" (Jev e a Alternativa Open-Source Laya)

Até este ponto, dominamos a técnica de conter modelos autoregressivos através de **Grammar-Guided Sampling** (máscara de logits). No entanto, um questionamento arquitetural profundo sacudiu a engenharia de software de IA em 2026:

> *Por que gastar 40 a 60 passos autoregressivos na CPU gerando aspas, chaves, delimitadores e espaços em branco se a aplicação precisa apenas de uma decisão discreta ou de um roteamento tipado?*

Essa reflexão formalizou a separação dos **Modelos System 1**, inspirados na teoria cognitiva de Daniel Kahneman (*Thinking, Fast and Slow*):

![Modelos System 1 vs LLMs Generativos](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0009_saida_estruturada/assets/06.png)

> **Figura 6:** A dicotomia entre a geração token a token (System 2 com Grammar Mask) e a decisão direta em passada única (System 1 via Jev / Laya).

### 6.1. Sistema 1 vs Sistema 2 Aplicado a Software de IA

- **Sistema 2 (Generativo / Autoregressivo):** Lento, deliberativo, sequencial e computacionalmente pesado. Modelos como `Qwen 2.5` e `Llama 3.2` processam o contexto e geram token por token ($O(N)$ passadas pela rede neural). Isso é indispensável quando a saída demanda redação em linguagem natural (ex: redigir um e-mail de resposta personalizado). Contudo, para decidir apenas `{"tool": "criar_ticket"}`, a autoregressão consome entre **400 ms e 2.200 ms**.
- **Sistema 1 (Não Generativo / Decisão Direta):** Instantâneo, intuitivo e altamente eficiente. Em vez de gerar texto sequencial, o modelo recebe o estado e executa **uma única passada paralela (Single Forward Pass em $O(1)$)** através de uma arquitetura de encoder (como `ModernBERT`), avaliando cabeças de decisão tipadas.

### 6.2. As Três Primitivas Universais do System 1
1. **`Choice` (Classificação Categórica):** Seleciona uma opção a partir de um catálogo pré-definido (`enum`), retornando uma distribuição de probabilidade Softmax calibrada.
2. **`Score` (Pontuação Contínua ou Ordinal):** Atribui uma nota quantitativa com base em critérios definidos (ex: probabilidade de churn de 0.0 a 1.0, score de prioridade).
3. **`Bool` / `Noul` (Portão de Decisão Binário):** Avalia se uma condição lógica é verdadeira ou falsa para atuar como guardrail de ativação imediata.

### 6.3. O Cenário da Indústria: Jev vs Laya
- **Jev (TypeSafe AI):** Criado pela TypeSafe AI (fundada por Diogo Almeida), o Jev é um modelo System 1 pioneiro oferecido como API gerenciada em nuvem. Tornou-se referência para planos de controle de agentes corporativos que buscam triagem sub-100ms.
- **Laya (Convai Innovations) & Kev:** A resposta comunitária e open-source sob licença Apache 2.0. Construído sobre arquiteturas eficientes de encoder com cabeças de classificação dedicadas, o Laya roda **100% localmente e offline** em CPU comum, com latências entre **12 ms e 35 ms**, sem depender de nuvens externas nem faturamento por requisição.

### 6.4. Matriz Comparativa de Engenharia

| Critério Arquitetural | LLM Generativo + Grammar Mask (Ollama) | Modelo System 1 Dedicado (Laya / Jev) |
| :--- | :--- | :--- |
| **Mecanismo Neural** | Decoder Autoregressivo ($N$ forward passes) | Encoder de Passada Única ($O(1)$ forward pass) |
| **Natureza da Saída** | Objeto JSON completo contendo texto gerado | Primitivas Tipadas (`Choice`, `Score`, `Bool`) |
| **Latência Típica (CPU)** | **400 ms a 2.200 ms** | **12 ms a 35 ms** (> 30x mais veloz) |
| **Garantia de Estrutura** | 100% (imposta por FSM e Logits Mask) | 100% (imposta pela cabeça de classificação) |
| **Consumo de Memória** | Médio a Alto (KV Cache expansível) | Baixo e Fixo (sem KV Cache) |
| **Melhor Caso de Uso** | Extração de entidades dinâmicas, redação | Roteamento de agentes, tools MCP, guardrails |

### 6.5. Resultados Medidos em Laboratório Local (`data/system_one_comparativo.json`):
No laboratório empírico deste artigo (`src/structured_lab.py`), implementamos um benchmark direto comparando o decisor de passada única System 1 com o Ollama em CPU local:

- **Decisor System 1 (Passada Única):** Latência média de **12.97 ms** (p50: `13.61 ms`), com **100% de conformidade de schema** e **100% de acurácia de roteamento**.
- **Modo Schema (Qwen/Llama no Ollama):** Latência média de **400.5 ms**, garantindo 100% de validação, porém com custo de inferência 30x superior.
- **Modo Livre (Prompt Only):** Latência de **3.007 ms**, com quebras severas de formatação.

> **O Padrão Híbrido de Dois Níveis (Two-Tier Architecture):** Em arquiteturas corporativas maduras, utilize um modelo **System 1 (Laya local ou Jev)** no portão de entrada para triagem, validação de guardrails e seleção de ferramentas em menos de 20 ms. Reserve o **LLM Generativo com JSON Schema (System 2)** unicamente para tarefas que exijam geração de texto natural complexo.

---

## 7. O que Quebra na Prática (Failure Modes)

Mesmo com JSON Schema estrito, sistemas em produção enfrentam peculiaridades sutis:

### 1. A Ordem dos Campos Afeta o Raciocínio do Modelo
Em um decoder autoregressivo, a ordem das chaves no JSON dita a ordem de geração dos tokens. Se o schema exigir `{"decisao": "criar_ticket", "justificativa": "..."}`, o modelo é forçado a decidir antes de raciocinar!
- **Solução de Engenharia:** Sempre declare o campo de raciocínio antes do campo de decisão: `{"justificativa": "...", "decisao": "..."}`. Dessa forma, os tokens de raciocínio gerados entram no contexto de atenção do próprio modelo, elevando a precisão da decisão final.

### 2. Schemas com Enums Excessivamente Amplos
Passar um enum com 500 opções pode saturar a memória do FSM e tornar a máscara de logits lenta.
- **Solução de Engenharia:** Divida catálogos gigantescos em hierarquias de dois níveis (ex: primeiro classifique a `categoria_macro`, depois filtre o sub-enum).

---

## 8. Show-Me-The-Code: Executando o Laboratório

### Opção 1: Execução do Benchmark pelo Terminal
```bash
# 1. Navegue até o módulo
cd pathbit-academy-ai/0009_saida_estruturada

# 2. Configure o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Execute o benchmark automatizado
python src/structured_lab.py --repeat 2
```

### Artefatos Gerados em `data/`:
- `structured_resultados.csv`: Auditoria linha a linha de cada chamada.
- `structured_resumo.csv`: Consolidação por modo de contrato (Livre, JSON, Schema).
- `system_one_comparativo.json`: Telemetria detalhada do decisor System 1.
- `structured_relatorio.md`: Relatório executivo completo em Markdown.
- `structured_comparativo.png`: Gráfico visual de latência e conformidade.

### Opção 2: Notebook Interativo
```bash
python src/main.py
```

### Evidência de Execução Real:
Abaixo, a comprovação visual da execução real do notebook interativo com Pydantic, geração com Ollama e o benchmark dos modelos System 1:

![Evidência de Execução do Notebook 0009](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0009_saida_estruturada/assets/evidence_notebook.png)

---

## 9. Próximos Passos: Do Contrato de Saída à Invocação de Ferramentas Reais

Com contratos de saída matematicamente blindados via **Grammar-Guided Sampling** e decisões instantâneas viabilizadas por **Modelos System 1**, o próximo passo é conectar essa inteligência ao mundo real.

No **[Artigo 0010 — MCP Local](https://github.com/pathbit/pathbit-academy-ai/blob/master/0010_mcp_local/article/ARTICLE.md)**, conectamos essas garantias ao ecossistema do **Model Context Protocol (MCP)** da Anthropic:
- Servidor MCP local rodando via `stdio` sem abrir portas de rede;
- Descoberta dinâmica de catálogo (`list_tools`) integrada a schemas estritos;
- Execução de ferramentas corporativas com menos de 1 ms de overhead de protocolo.

---

## Referências Técnicas

- [Ollama Structured Outputs Documentation](https://ollama.com/blog/structured-outputs)
- [JSON Schema Specification (Draft 2020-12)](https://json-schema.org/)
- [Gerganov, Georgi: llama.cpp Grammar-Based Sampling Implementation](https://github.com/ggerganov/llama.cpp/blob/master/grammars/README.md)
- [Pydantic v2: Fast Data Validation using Python Type Hints](https://docs.pydantic.dev/)
- [TypeSafe AI: Jev — System One Model for Software Decisions](https://typesafe.ai)
- [Convai Innovations: Laya — Open-Source System One Decision Engine](https://github.com/convai/laya)
- [Kahneman, Daniel: Thinking, Fast and Slow (Farrar, Straus and Giroux, 2011)](https://en.wikipedia.org/wiki/Thinking,_Fast_and_Slow)

---

👉 **Repositório oficial no GitHub:** [https://github.com/pathbit/pathbit-academy-ai](https://github.com/pathbit/pathbit-academy-ai)  
👉 **Módulo:** `0009_saida_estruturada`

#EngenhariaDeSoftware #InteligenciaArtificial #LLM #Ollama #JSONSchema #Python #PathbitAcademy #SystemOne #Pydantic #DevOps #DeepLearning
