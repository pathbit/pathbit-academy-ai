# Saída Estruturada com LLMs: Do Prompt Otimista ao Contrato Validado

Pedir JSON em texto livre é a maior armadilha da engenharia de IA moderna. O modelo responde ```json com preâmbulos, esquece vírgulas ou alucina nomes de propriedades. O backend executa `json.loads()`, estoura `JSONDecodeError` e a esteira inteira trava.

O artigo 0009 da série Pathbit Academy prova como transformar inferência probabilística em chamada de função determinística e tipada:

🎯 Três níveis de acoplamento comparados:
1. Livre (Prompt Only): "Responda apenas em JSON". Quase 30% de falha no parse direto.
2. Modo JSON (`format: "json"`): sintaxe parseável, mas campos e enums desgovernados (ou objeto vazio `{}`).
3. JSON Schema (`format: <schema>`): contrato estrito compilado em Autômato de Estados Finitos (FSM) no motor de inferência.

🔬 Como funciona o Grammar-Guided Sampling:
A cada passo autoregressivo, os logits dos tokens que violam a gramática recebem valor -∞ (probabilidade zero). O modelo é matematicamente incapaz de gerar caracteres fora do schema.

📊 O que os testes reais mediram no Ollama (54 execuções):
→ Modo Livre: 72.2% de parse_ok e apenas 44.4% de acerto semântico.
→ format: "json": 100% de parse_ok, mas 66.7% de conformidade com o schema esperado.
→ format: schema: 100% de conformidade com o schema e 94.4% de acerto semântico.
→ Quando o modelo não gasta probabilidade formatando, ele foca no conteúdo correto.

💡 O mito do retry compensatório:
Reenviar erros de sintaxe para o modelo em loop dobra a latência (~2.400 ms vs ~1.300 ms). Impor schema na primeira chamada custa menos de 200 ms e resolve na largada.

O laboratório entrega evidência completa: código em Python padrão, notebook interativo, CSVs medidos e relatório comparativo.

Artigo completo e código open-source:
👉 https://github.com/pathbit/pathbit-academy-ai/tree/master/0009_saida_estruturada

#InteligenciaArtificial #LLM #Ollama #SoftwareEngineering #Python #JSONSchema #OpenSource
