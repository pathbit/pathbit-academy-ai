"""Figuras com números lidos dos dados preservados, sem duplicar métricas no HTML."""
from pathlib import Path
from html import escape
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def measured_page(title, subtitle, sections):
    body = []
    for heading, content in sections:
        table = content.to_html(index=False, border=0, float_format=lambda value: f"{value:.3f}") if isinstance(content, pd.DataFrame) else f"<p>{escape(str(content))}</p>"
        body.append(f"<section><h2>{escape(heading)}</h2>{table}</section>")
    return f'''<!doctype html><html lang="pt-BR"><meta charset="utf-8">
<style>body{{width:1800px;height:980px;padding:50px;background:#070a13;color:#f1f5f9;
font:22px Arial,sans-serif;margin:0}}h1{{font-size:42px;color:#c3b6fd}}
h2{{font-size:28px;color:#67e8f9}}p{{line-height:1.5}}section{{margin:28px 0}}
table{{border-collapse:collapse;width:100%;font-size:20px}}th,td{{padding:14px;
border-bottom:1px solid #334155;text-align:left}}th{{color:#c3b6fd}}
footer{{color:#94a3b8;font-size:18px}}</style><h1>{escape(title)}</h1>
<p>{escape(subtitle)}</p>{''.join(body)}<footer>Pathbit Academy AI · dados preservados em data/ · recorte didático, não SLA</footer></html>'''


def overrides():
    result = {}
    prompt = pd.read_csv(ROOT/'0005_prompt_engineering_avancado/data/benchmark_resumo.csv')
    result['0005_prompt_engineering_avancado/assets/05.png'] = measured_page(
        'Estratégia e modelo: score não é acurácia', 'Fonte: benchmark_resumo.csv. Recorte pequeno; compare estrutura, prioridade e semântica.',
        [('Resumo medido', prompt[['modelo_geracao','estrategia','score_estrutura','score_prioridade','score_total']])])
    summary = pd.read_csv(ROOT/'0006_llm_evals_regressao/data/candidate_summary.csv')
    regressions = pd.read_csv(ROOT/'0006_llm_evals_regressao/data/regressoes_detectadas.csv')
    result['0006_llm_evals_regressao/assets/04.png'] = measured_page(
        'Gate de release: compare o candidato escolhido', '0,05 é um limiar em pontos de score ponderado, não pontos percentuais de acurácia.',
        [('Ranking preservado',summary[['candidate','score_final','score_ponderado']]),
         ('Regressões históricas',f'{len(regressions)} registros. O gate corrigido considera somente regressões críticas do vencedor; relatórios antigos não foram alterados.'),
         ('Limite', 'Faithfulness neste runner é sobreposição de tokens, não prova de verdade. Acrescente pisos absolutos e casos adversos.')])
    ollama = pd.read_csv(ROOT/'0008_llms_locais_ollama/data/benchmark_resumo.csv')
    result['0008_llms_locais_ollama/assets/04.png'] = measured_page(
        'Ollama: tempos e vazão observados', 'Fonte: benchmark_resumo.csv. Respostas têm comprimentos diferentes; tamanho em disco não é RAM.',
        [('Resumo medido',ollama),('Limite','Sem cobrança de API por token; energia, hardware e operação continuam tendo custo.')])
    structured = pd.read_csv(ROOT/'0009_saida_estruturada/data/structured_resumo.csv')
    result['0009_saida_estruturada/assets/03.png'] = measured_page(
        'Sintaxe, schema e acerto de negócio', '18 linhas consolidadas por modo; o tempo pode incluir uma tentativa extra.',
        [('Resumo preservado',structured[['modo','parse_ok_pct','schema_ok_pct','semantico_ok_pct','total_medio_ms']]),
         ('Interpretação','100% de conformidade no recorte não significa decisão correta: schema teve 44,4% de acerto semântico.')])
    result['0009_saida_estruturada/assets/04.png'] = measured_page(
        'Retry: custo acumulado, não overhead constante', 'Fonte: structured_resumo.csv; o runner consolida até duas tentativas por tarefa.',
        [('Latência consolidada',structured[['modo','total_medio_ms','tokens_medios','chamadas']]),
         ('Política','Retry ocorre após falha de parse/schema. Uma saída semanticamente errada que passa no schema não é corrigida por essa política.'),
         ('Limite','Compare recuperação, latência e tokens de todas as tentativas. Não afirme que retry sempre dobra o tempo ou que schema tem overhead fixo.')])
    baseline = json.loads((ROOT/'0009_saida_estruturada/data/system_one_comparativo.json').read_text())
    result['0009_saida_estruturada/assets/06.png'] = measured_page(
        'Roteamento sem geração: baseline por embeddings', 'O nome histórico system_one_comparativo.json foi preservado; não mede Jev, Laya ou Kev.',
        [('Métricas observadas',pd.DataFrame([{k:baseline[k] for k in ['chamadas_avaliadas','latencia_media_ms','latencia_p50_ms','latencia_p95_ms','acuracia_pct']} ])),
         ('Implementação','nomic-embed-text → similaridade de cosseno → maior score entre três rotas. Similaridade/softmax não é confiança calibrada.'),
         ('Limite','Escolher rótulo não extrai parâmetros nem equivale às tarefas do LLM com schema. Complexidade varia com o texto.')])
    protocol = json.loads((ROOT/'0010_mcp_local/data/mcp_latencia_protocolo.json').read_text())
    mcp = pd.read_csv(ROOT/'0010_mcp_local/data/mcp_resumo.csv')
    result['0010_mcp_local/assets/04.png'] = measured_page(
        'MCP: protocolo isolado e ciclo completo', 'São medições diferentes, não garantia de overhead inferior a 1 ms.',
        [('50 chamadas isoladas',pd.DataFrame([protocol])),
         ('Planner e chamada por modelo',mcp[['modelo','tool_certa_pct','plan_medio_ms','mcp_medio_ms']]),
         ('Segurança','Stdio não é sandbox. Valide argumentos, permissões, timeouts e encerramento de processos.')])

    eval_module = '0006_llm_evals_regressao'
    finance = pd.read_csv(ROOT / eval_module / 'data/eval_dataset.csv').query("categoria == 'financeiro'").iloc[0]
    result[f'{eval_module}/assets/01.png'] = measured_page(
        'O ranking não encerra a avaliação', 'Média ponderada e perdas por caso nos dados preservados.',
        [('Ranking', summary[['candidate', 'score_ponderado']]),
         ('Regressões', regressions[['candidate', 'categoria', 'criticidade', 'delta_vs_baseline']])])
    result[f'{eval_module}/assets/02.png'] = measured_page(
        'Anatomia de um caso de avaliação', finance['pergunta'],
        [('Contexto', finance['contexto']), ('Gabarito', finance['gold']),
         ('Termos e criticidade', f"{finance['palavras_criticas']} · {finance['criticidade']}")])
    result[f'{eval_module}/assets/03.png'] = measured_page(
        'Três componentes, uma média', 'A média recebe o multiplicador de criticidade.',
        [('Similaridade', 'Compara os embeddings da resposta e do gabarito.'),
         ('Termos críticos', 'Conta expressões do gabarito presentes na resposta.'),
         ('Sobreposição', 'Conta tokens da resposta presentes no contexto. A medida não verifica suporte lógico.')])
    result[f'{eval_module}/assets/05.png'] = measured_page(
        'Abra a evidência por trás do ranking', 'Cada arquivo ajuda a localizar uma decisão da avaliação.',
        [('Gerações', 'geracoes_evals.csv registra a resposta e os componentes do escore por pergunta.'),
         ('Ranking e regressões', 'candidate_summary.csv agrega os escores; regressoes_detectadas.csv registra quedas por caso.'),
         ('Decisão', 'relatorio_evals.md resume as métricas e a regra usada na execução.')])

    agent_module = '0007_agentes_tool_calling'
    audit_file = ROOT / agent_module / 'data/agent_audit_log.jsonl'
    audit = [json.loads(line) for line in audit_file.read_text(encoding='utf-8').splitlines()]
    first_actions = {}
    for row in audit:
        first_actions.setdefault(row['acao'], row)
    no_example = 'Nenhum caso correspondente no recorte.'
    blocked = first_actions.get('bloqueado', {})
    policy = first_actions.get('buscar_politica', {})
    ticket = first_actions.get('criar_ticket', {})
    ticket_steps = json.loads(ticket.get('audit_steps', '[]'))
    ticket_step = next((step for step in ticket_steps if step['step'] == 'tool_execution'), {})
    result[f'{agent_module}/assets/01.png'] = measured_page(
        'Onde a aplicação escolhe o caminho', 'O runner separa entrada, decisão e ação.',
        [('Entrada', 'A aplicação verifica a mensagem antes do roteamento.'),
         ('Decisão', 'A regra conhecida vem primeiro. O planner cobre casos sem regra aplicável.'),
         ('Ação', 'A aplicação consulta políticas, simula um chamado ou responde diretamente.')])
    result[f'{agent_module}/assets/02.png'] = measured_page(
        'Uma recusa antes do roteamento', 'O registro da execução preservada mostra uma única etapa.',
        [('Registro', pd.DataFrame(json.loads(blocked['audit_steps'])) if blocked else no_example),
         ('Limite', 'O filtro didático procura palavras. A entrada recusada não chega ao planejador.')])
    result[f'{agent_module}/assets/03.png'] = measured_page(
        'De onde veio a decisão', 'Um plano parseável ainda pode ser substituído.',
        [('Regras', 'business_rule escolhe antes do planner.'),
         ('Plano', 'planner identifica a ação proposta pelo modelo quando o aplicativo a mantém.'),
         ('Roteador', 'router_fallback trata falha de parse. router_override trata divergência com similaridade de pelo menos 0,50.')])
    result[f'{agent_module}/assets/04.png'] = measured_page(
        'Da rota ao documento e à resposta', 'A ação e a síntese são avaliadas em etapas.',
        [('Ação', policy.get('planned_tool', no_example)), ('Documento recuperado', policy.get('documento', '—')),
         ('Síntese', policy.get('resposta', '—'))])
    result[f'{agent_module}/assets/05.png'] = measured_page(
        'O log aponta a decisão e a execução', 'O incidente por erro 500 gerou um chamado simulado.',
        [('Origem da decisão', ticket.get('decision_source', no_example)), ('Ação executada', ticket.get('acao', '—')),
         ('ID da simulação registrada', ticket_step.get('ticket_id', '—'))])

    mcp_module = '0010_mcp_local'
    mcp_data = ROOT / mcp_module / 'data'
    catalog = json.loads((mcp_data / 'catalogo_tools.json').read_text(encoding='utf-8'))
    tools = [{'ferramenta': tool['nome'], 'obrigatórios': ', '.join(tool['input_schema']['required'])}
             for tool in catalog]
    mcp_runs = pd.read_csv(mcp_data / 'mcp_resultados.csv')
    incidents = mcp_runs[(mcp_runs['consulta_id'] == 'q_incidente') & mcp_runs['acertou'].eq(False)].head(1)
    incident = next(iter(incidents.to_dict(orient='records')), {})
    incident_summary = f"Consulta {incident['consulta_id']} com {incident['modelo']}." if incident else no_example
    incident_details = [
        ('Escolha', f"{incident['tool_escolhida']} no plano. O gabarito indicou {incident['tool_esperada']}."),
        ('Validação', f"schema_ok={incident['schema_ok']} · acertou={incident['acertou']}"),
        ('Resultado', incident['resposta_mcp']),
    ] if incident else []
    result[f'{mcp_module}/assets/01.png'] = measured_page(
        'MCP e Ollama usam canais separados', 'O cliente Python coordena os dois caminhos.',
        [('Servidor de ferramentas', 'O cliente lança o subprocesso MCP.'),
         ('Caminho MCP', 'O protocolo usa stdin e stdout. Diagnósticos ficam em stderr.'),
         ('Caminho Ollama', 'O cliente solicita o plano por HTTP. As permissões do subprocesso vêm do ambiente.')])
    result[f'{mcp_module}/assets/02.png'] = measured_page(
        'O catálogo documenta a entrada', 'Os campos vêm do registro de list_tools().',
        [('Catálogo de ferramentas', pd.DataFrame(tools)),
         ('Campo opcional', 'criar_ticket também aceita prioridade em forma de string.')])
    result[f'{mcp_module}/assets/03.png'] = measured_page(
        'Um plano válido pode escolher mal', incident_summary, incident_details)
    result[f'{mcp_module}/assets/05.png'] = measured_page(
        'O CSV ajuda a explicar a chamada', 'O log preservado permite investigar escolha, validação e latência.',
        [('Campos', incidents[['consulta_id', 'tool_escolhida', 'tool_esperada', 'schema_ok', 'plan_ms', 'mcp_ms']]
          if incident else no_example),
         ('Limite', 'O CSV pode ser regravado, e seus campos não registram aprovação do usuário.')])
    return result
