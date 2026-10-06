# Saída estruturada com LLMs locais, contratos formais e a fronteira dos modelos System 1

Grande parte dos desenvolvedores que começam a integrar Modelos de Linguagem em sistemas de produção corporativos passa pelo mesmo ritual ao redigir um prompt detalhado pedindo que o modelo responda apenas em formato JSON, sem preâmbulos, sem markdown e com aspas duplas estritas.

O desenvolvedor testa três vezes no terminal, comemora que o resultado veio em formato de dicionário e coloca o serviço em deploy na sexta-feira à tarde.

Na segunda-feira de manhã, o primeiro incidente de severidade alta acontece. O modelo decidiu prefixar a resposta com blocos de markdown na primeira linha, inseriu uma saudação cortês antes das chaves, trocou o nome da chave `status` por `situacao`, formatou um valor monetário como texto em vez de número decimal ou alucinou uma opção inexistente fora do enum esperado. O backend executa o parser JSON, estoura uma exceção fatal de sintaxe ou de chave ausente, e a esteira inteira de atendimento é interrompida.

No [Artigo 0008 da Pathbit Academy](https://github.com/pathbit/pathbit-academy-ai/blob/master/0008_llms_locais_ollama/article/ARTICLE.md), provamos como rodar uma stack completa de IA 100% local em Docker via Ollama, eliminando custos por token e dependências de nuvem. No entanto, ter o modelo rodando localmente não resolve por si só a fragilidade da interface de saída.

Este artigo aprofunda exatamente essa fronteira crítica de engenharia sobre como transformar a inferência probabilística de um LLM em uma chamada de função determinística e fortemente tipada. Comparamos na prática três níveis de contrato em modelos locais compactos (Qwen 2.5 0.5B, Qwen 2.5 1.5B e Llama 3.2 1B) e apresentamos a nova fronteira da indústria de IA, que são os modelos System 1 para decisões instantâneas em passada única.

---

## Os três níveis de contrato entre LLMs e software corporativo

A relação entre código de engenharia e modelos de linguagem evoluiu através de três paradigmas bem definidos de acoplamento.

![Os Três Níveis de Contrato com LLMs](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0009_saida_estruturada/assets/01.png)

> Figura 1. Da incerteza do texto livre à garantia matemática estrita imposta pelo motor de inferência.

### O prompt otimista em modo livre

Neste modelo inicial, o desenvolvedor não utiliza nenhuma restrição nativa do motor de inferência. Todo o peso do contrato recai sobre o prompt textual.

```python
prompt = """Você é um assistente de suporte.
Responda EXATAMENTE um JSON com as chaves "produto" e "prazo_dias".
Não inclua explicações nem blocos markdown.
Entrada: 'Quero devolver uma televisão comprada há 10 dias.'"""
```

O problema desse nível é que ele falha sob qualquer variação de contexto. Como os modelos são treinados em bases massivas de código com tutoriais, a probabilidade estatística de envolver o JSON em blocos markdown com crases triplas é altíssima. Além disso, saudações de cortesia poluem o início e o fim da mensagem. 

Muitas equipes tentam contornar isso com expressões regulares artesanais para localizar chaves de abertura e fechamento, mas qualquer aspa desbalanceada no meio do texto quebra o parser. Nos nossos testes medidos, quase 30% das chamadas sequer passaram na leitura inicial do JSON, e a assertividade de negócio caiu para 44.4%.

### O modo JSON sintático

O motor de inferência, como o Ollama ou o llama.cpp, restringe a decodificação para forçar que a sequência de tokens gerada seja um documento JSON sintaticamente válido. O modelo não consegue concluir a geração sem fechar aspas, vírgulas e colchetes.

```json
{
  "item_retornado": "televisão",
  "dias_passados": "10 dias"
}
```

O parser tradicional executa com sucesso sem lançar exceções de sintaxe. Contudo, o esquema interno de dados permanece desgovernado. O modelo pode inventar nomes de propriedades diferentes dos esperados pelo backend, converter números em strings ou, pior ainda, devolver um objeto vazio `{}`. Em nossos experimentos com o Llama 3.2 1B sob essa opção genérica, o modelo descobriu que devolver chaves vazias cumpria a exigência de sintaxe válida, entregando um objeto inútil em todas as tentativas.

### O contrato formal com JSON Schema

O motor de inferência recebe uma especificação JSON Schema formal que dita rigorosamente as propriedades permitidas, a lista de campos obrigatórios, os tipos primitivos estritos e os valores aceitos em enumerações fechadas.

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

Qualquer token do vocabulário que gere uma chave inexistente, viole a tipagem numérica ou fuja das opções do enum é matematicamente eliminado da amostragem em tempo real durante a geração de cada caractere.

---

## A matemática do Grammar-Guided Sampling sob o capô

Para compreender por que o Nível 3 oferece garantia estrutural total sem quebras de parse, é preciso examinar o ciclo autoregressivo de geração de um modelo.

![Mecanismo de Decodificação Constrangida](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0009_saida_estruturada/assets/02.png)

> Figura 2. Máscara dinâmica de logits guiada por Autômato de Estados Finitos a cada token gerado.

A cada passo de tempo $t$, o modelo processa o contexto acumulado e calcula um vetor de afinidade estatística, chamado de logits não normalizados.

$$\mathbf{z}_t = [z_{t, 1}, z_{t, 2}, \dots, z_{t, V}] \in \mathbb{R}^V$$

onde $V$ representa o tamanho total do vocabulário do tokenizer, que gira entre 128 mil e 152 mil tokens nos modelos modernos.

Em amostragem livre com temperatura $T$, a probabilidade de selecionar determinado token é calculada pela função Softmax.

$$P(\text{token}_i) = \frac{e^{z_{t, i} / T}}{\sum_{j=1}^V e^{z_{t, j} / T}}$$

Antes de iniciar a geração, a biblioteca llama.cpp no Ollama compila a especificação JSON Schema em uma Gramática Livre de Contexto (CFG / EBNF) e constrói um Autômato de Estados Finitos (FSM). 

No estado inicial, o único caractere permitido pela gramática é a chave de abertura `{`. Uma vez aberta a chave, o autômato passa para o estado que exige o nome de uma propriedade declarada. Se o modelo tentar emitir qualquer letra que não inicie uma chave válida, essa transição é considerada proibida.

Para aplicar essa regra fisicamente, o motor calcula o conjunto de tokens válidos no estado atual da máquina de estados. Todos os tokens ilegais têm seus valores de logits sobrescritos para menos infinito.

$$\tilde{z}_{t, i} = \begin{cases} z_{t, i}, & \text{se } i \in V_{\text{válidos}} \\ -\infty, & \text{se } i \notin V_{\text{válidos}} \end{cases}$$

Como a exponencial de menos infinito é exatamente zero, a probabilidade de qualquer token fora da gramática torna-se absolutamente nula na equação da Softmax.

Esse mecanismo traz um efeito colateral valioso observado em laboratório. O modelo não apenas respeita a sintaxe, mas torna-se semanticamente mais preciso. Em geração livre, o modelo dispersa atenção tentando equilibrar pontuação e aspas. Quando os tokens proibidos são descartados, toda a massa de probabilidade se redistribui exclusivamente entre as escolhas válidas de negócio.

---

## O experimento e as evidências empíricas

Para avaliar esse comportamento na prática, construímos um laboratório automatizado cobrindo três casos reais de uso corporativo. O primeiro foi um planejador de suporte técnico encarregado de escolher entre buscar políticas ou abrir tickets. O segundo foi um extrator de entidades para identificar produtos e prazos de devolução em linguagem informal. E o terceiro foi um classificador de incidentes operacionais para atribuir rotas e níveis de urgência.

Avaliamos três modelos compactos em CPU com 54 chamadas distribuídas uniformemente, cobrindo o Qwen 2.5 0.5B, o Qwen 2.5 1.5B e o Llama 3.2 1B.

![Resultados Comparativos Medidos](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0009_saida_estruturada/assets/03.png)

> Figura 3. Taxa de parse direto, conformidade formal com schema e assertividade semântica medida na máquina.

Os resultados consolidados por nível de contrato demonstram com clareza o salto de maturidade.

| Modo de Contrato | Parse OK (%) | Conformidade de Schema (%) | Acurácia Semântica de Negócio (%) | Latência Média por Chamada |
| :--- | :---: | :---: | :---: | :---: |
| Livre (Prompt Only) | 72.2% | 55.6% | 44.4% | ~1.150 ms |
| JSON Sintático (`format: "json"`) | 100.0% | 66.7% | 55.6% | ~1.210 ms |
| JSON Schema Estrito (`format: <schema>`) | 100.0% | 100.0% | 94.4% | ~1.380 ms |

O teste deixa três lições práticas para arquitetura. O modo livre é inviável em produção porque quase um terço das respostas quebra o parser e mais da metade falha nas regras de negócio. O modo JSON sintático cria uma falsa sensação de segurança, pois passa no parser mas entrega dados corrompidos ou incompletos em um terço das tentativas. Por fim, a restrição com JSON Schema elevou o acerto de negócio para 94.4%, adicionando apenas 170 milissegundos de sobrecarga de amostragem.

---

## O mito do retry compensatório e o custo real de latência

Um padrão comum em pipelines frágeis é o loop de retry reativo. Quando o backend falha ao ler o JSON gerado, ele captura a mensagem de erro do parser, monta um novo prompt e reenvia para o modelo tentar consertar a saída.

![Trade-off de Latência e Retry](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0009_saida_estruturada/assets/04.png)

> Figura 4. O custo real do retry reativo em comparação ao overhead desprezível da máscara de gramática.

Esse padrão é prejudicial por três motivos. Primeiro, dobra a latência total observada pelo usuário, saltando de cerca de 1.380 ms para mais de 2.400 ms em cada ocorrência de erro. Segundo, se o modelo já errou o formato na primeira tentativa sob determinado contexto, a chance de reincidir em erros sutis na segunda chamada é elevada. Terceiro, em ambientes locais com recursos compartilhados de CPU, disparar chamadas repetidas satura os núcleos do servidor e prejudica os demais processos.

A abordagem de engenharia correta é garantir o formato na primeira chamada com decodificação constrangida. Loops de retry devem ser reservados exclusivamente para validações externas de negócio, como verificar se um número de pedido existe no banco relacional, e nunca para tratar vírgulas ausentes ou nomes de campos trocados.

---

## Implementação de produção com Pydantic v2

Em sistemas empresariais em Python, os contratos de dados devem ser mantidos como modelos tipados com Pydantic, aproveitando a extração automática de JSON Schema e a validação ultrarrápida compilada em Rust.

![Arquitetura de Integração em Produção](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0009_saida_estruturada/assets/05.png)

> Figura 5. Pipeline desacoplado e tipado entre LLMs locais e serviços de backend.

```python
import json
import urllib.request
from typing import Literal
from pydantic import BaseModel, Field, field_validator

class PlanoAtendimento(BaseModel):
    tool: Literal["buscar_politica", "criar_ticket", "resposta_direta"] = Field(
        description="Ferramenta operacional necessária para atender a solicitação."
    )
    confianca: float = Field(
        ge=0.0, le=1.0, description="Nível de certeza da decisão entre 0 e 1."
    )
    justificativa: str = Field(
        description="Breve raciocínio que fundamentou a escolha da ferramenta."
    )

    @field_validator("justificativa")
    def validar_justificativa(cls, v: str) -> str:
        if len(v.strip()) < 5:
            raise ValueError("Justificativa muito curta.")
        return v

SCHEMA_PLANO = PlanoAtendimento.model_json_schema()

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

    return PlanoAtendimento.model_validate_json(resposta_raw["response"])
```

Esse fluxo garante que a resposta do Ollama seja deserializada diretamente na classe tipada sem risco de quebras de contrato ou chaves inexistentes.

---

## A nova fronteira dos modelos System 1 com Laya e Jev

Com o Grammar-Guided Sampling, aprendemos a conter um modelo autoregressivo para gerar JSON válido. Porém, uma reflexão arquitetural importante surgiu na comunidade técnica sobre a real necessidade de gastar dezenas de passos sequenciais gerando chaves e espaços quando a aplicação precisa apenas de uma decisão discreta ou de um enum.

Essa distinção resgata a teoria cognitiva de Daniel Kahneman sobre dois modos de pensamento.

![Modelos System 1 vs LLMs Generativos](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0009_saida_estruturada/assets/06.png)

> Figura 6. A dicotomia entre a geração sequencial token a token e a decisão direta em passada única.

O modo System 2 corresponde aos modelos generativos tradicionais, como Qwen e Llama. Eles são lentos, deliberativos e computam uma passada completa pela rede neural para cada novo token emitido. Esse comportamento é indispensável quando a tarefa exige redigir respostas livres em texto natural. No entanto, para decidir qual ferramenta acionar em um catálogo fixo, esse processo consome entre 400 e 2.200 milissegundos.

O modo System 1 reúne modelos focados em decisão direta em vez de geração de texto. Utilizando arquiteturas de encoder como ModernBERT, o modelo processa todo o contexto em uma única passada paralela em ordem $O(1)$, avaliando cabeças de classificação dedicadas para responder em cerca de 13 a 35 milissegundos.

Os modelos System 1 operam sobre três primitivas universais bem definidas. A primitiva Choice é voltada para seleções categóricas sobre enums fechados com distribuição de probabilidade calibrada. A primitiva Score lida com a atribuição de notas contínuas ou ordinais, a exemplo de risco de cancelamento ou nível de prioridade de chamados. Por fim, a primitiva Bool executa validações binárias de regras lógicas, atuando como guardrail instantâneo de ativação de sistemas.

No cenário da indústria, duas iniciativas se destacam. O Jev, criado pela TypeSafe AI sob liderança de Diogo Almeida, oferece essa capacidade como uma API gerenciada em nuvem para roteamento rápido em pipelines corporativos. Em contrapartida, projetos open-source e com pesos abertos como Laya e Kev, desenvolvidos pela Convai Innovations sob licença Apache 2.0, permitem rodar essa mesma arquitetura de decisão em hardware local comum, sem tráfego de dados externo nem custos por requisição.

| Critério Arquitetural | LLM Generativo com Grammar Mask (Ollama) | Modelo System 1 Dedicado (Laya / Jev) |
| :--- | :--- | :--- |
| Mecanismo Neural | Decoder Autoregressivo ($N$ passadas sequenciais) | Encoder de Passada Única ($O(1)$ passada paralela) |
| Natureza da Saída | Objeto JSON completo com texto gerado | Primitivas Tipadas (Choice, Score, Bool) |
| Latência Típica em CPU | 400 ms a 2.200 ms | 12 ms a 35 ms (mais de 30x mais veloz) |
| Garantia de Estrutura | 100% imposta por FSM e máscara de logits | 100% imposta pela cabeça de classificação |
| Consumo de Memória | Médio a alto com KV Cache expansível | Baixo e fixo sem necessidade de KV Cache |
| Cenário Recomendado | Extração dinâmica de texto e síntese livre | Roteamento de agentes, tools MCP e guardrails |

No laboratório deste módulo, o decisor System 1 alcançou latência média de 12.97 ms com 100% de acerto de roteamento, comparado a 400.5 ms no modo schema do LLM e mais de 3.000 ms em modo livre.

A recomendação para arquiteturas maduras é combinar os dois mundos em um padrão de dois níveis. O modelo System 1 atua no portão de entrada para triagem, guardrails e roteamento em menos de 20 milissegundos. Quando a requisição demanda redação complexa ou síntese de texto, o fluxo encaminha a tarefa para o LLM generativo sob contrato formal de JSON Schema.

---

## O que quebra na prática

Mesmo operando com JSON Schema formal, existem sutilezas que afetam a estabilidade em produção.

A primeira é que a ordem dos campos no JSON influencia o raciocínio do modelo. Em decoders autoregressivos, os tokens são gerados na sequência em que as chaves aparecem na gramática. Se o schema exigir o campo de decisão antes do campo de justificativa, o modelo precisará cravar a resposta antes de ponderar os fatos. Sempre que possível, declare o campo de raciocínio antes da decisão final, permitindo que a própria geração prévia sirva de contexto para a atenção neural.

A segunda é que esquemas com listas de opções excessivamente extensas tornam a compilação da gramática pesada. Quando o catálogo de opções ultrapassa centenas de itens, o ideal é decompor a escolha em duas etapas, primeiro identificando uma categoria macro e em seguida filtrando o subconjunto correspondente.

---

## Execução prática do laboratório passo a passo

Os códigos completos do laboratório de saída estruturada e dos benchmarks de System 1 estão versionados no repositório.

### Execução pelo terminal

```bash
cd pathbit-academy-ai/0009_saida_estruturada

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python src/structured_lab.py --repeat 2
```

A execução gera todos os dados brutos e relatórios consolidados diretamente na pasta `data`. O arquivo `structured_resultados.csv` contém o registro individual de cada chamada e seus respectivos tempos, enquanto `structured_resumo.csv` compila as taxas de parse e conformidade por modelo. Os tempos do decisor em passada única ficam registrados em `system_one_comparativo.json`, o relatório analítico formatado pode ser conferido em `structured_relatorio.md`, e a visualização gráfica dos resultados está salva em `structured_comparativo.png`.

### Execução pelo notebook

O fluxo também pode ser acompanhado passo a passo no notebook.

```bash
python src/main.py
```

A imagem abaixo ilustra a execução interativa do laboratório com a validação estrita dos contratos Pydantic e as respostas geradas pelo Ollama.

![Evidência de Execução do Notebook 0009](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0009_saida_estruturada/assets/evidence_notebook.png)

---

## Próximos passos

Com as garantias matemáticas de saída estruturada estabelecidas e o ganho de velocidade proporcionado pelos modelos System 1, o próximo passo da trilogia conecta essas decisões à execução prática de tarefas corporativas.

No [Artigo 0010 (MCP Local via Stdio)](https://github.com/pathbit/pathbit-academy-ai/blob/master/0010_mcp_local/article/ARTICLE.md), conectamos modelos locais ao Model Context Protocol da Anthropic por canais seguros do sistema operacional, permitindo descobrir ferramentas dinamicamente e executá-las com menos de 1 milissegundo de sobrecarga de protocolo.

---

## Referências

- [Documentação oficial de saídas estruturadas do Ollama](https://ollama.com/blog/structured-outputs)
- [Especificação formal do JSON Schema Draft 2020-12](https://json-schema.org/)
- [Documentação técnica sobre amostragem guiada por gramática no llama.cpp](https://github.com/ggerganov/llama.cpp/blob/master/grammars/README.md)
- [Documentação oficial do framework de validação tipada Pydantic](https://docs.pydantic.dev/)
- [Documentação e especificações do modelo Jev pela TypeSafe AI](https://typesafe.ai)
- [Repositório do projeto open source Laya da Convai Innovations](https://github.com/convai/laya)
- [Obra Thinking Fast and Slow de Daniel Kahneman](https://en.wikipedia.org/wiki/Thinking,_Fast_and_Slow)

---

Repositório oficial no GitHub no endereço https://github.com/pathbit/pathbit-academy-ai no módulo 0009_saida_estruturada.

#EngenhariaDeSoftware #InteligenciaArtificial #LLM #Ollama #JSONSchema #Python #PathbitAcademy #SystemOne #Pydantic
