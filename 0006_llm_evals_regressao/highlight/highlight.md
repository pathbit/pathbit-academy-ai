**Slide 1**
LLM EVALS E REGRESSÃO
Como escolher o candidato certo antes do deploy.

**Slide 2**
O PROBLEMA REAL
Melhorar um caso não significa melhorar o sistema inteiro.
Sem esteira de avaliação, a regressão passa escondida.

**Slide 3**
O HARNESS DO ARTIGO
Comparação entre três candidatos:
- qwen_generico
- qwen_estruturado
- flan_estruturado

**Slide 4**
O QUE O DATASET TEM
- contexto oficial
- resposta ideal
- palavras críticas
- categoria
- criticidade

**Slide 5**
O QUE O SCORE CONSIDERA
- similaridade semântica
- keyword recall
- faithfulness
- peso por criticidade

**Slide 6**
O QUE MUDA DE VERDADE
O release não depende só do melhor score médio.
Também depende de não criar regressão em caso crítico.

**Slide 7**
O QUE A ESTEIRA GERA
- candidate_summary.csv
- regressoes_detectadas.csv
- relatorio_evals.md
- gerações completas por candidato

**Slide 8**
POR QUE ISSO ELEVA O PADRÃO
Comparar candidatos completos mostra onde o score médio engana
e onde a regressão crítica precisa barrar o release.

**Slide 9**
Link do artigo nos comentários.
Avaliar LLM direito é escolher melhor antes de publicar.
