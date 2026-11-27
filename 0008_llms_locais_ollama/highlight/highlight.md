**Slide 1**
[layout: cover]
[eyebrow: Série 0008 · LLMs locais]
[image: ../assets/02.png]
[caption: Ollama em Docker, porta publicada em loopback e volume de modelos.]

Do primeiro chat ao benchmark local

Suba um modelo pequeno, leia os tempos da resposta e investigue o que muda da primeira chamada para a seguinte.

**Slide 2**
[layout: split]
[eyebrow: Servidor local]
[image: ../assets/02.png]
[caption: O container pode ser recriado e reaproveitar os pesos no volume.]

O que está instalado e o que está em memória

- /api/version identifica a versão que responde.
- /api/tags lista os modelos instalados.
- /api/ps mostra os modelos carregados.

**Slide 3**
[layout: split]
[eyebrow: Duas chamadas ao mesmo modelo]
[image: ../assets/06_streaming_terminal.png]
[caption: Exemplo de execução com o mesmo prompt e dois estados do modelo.]

A espera antes do primeiro fragmento

Rode o exemplo uma vez com o modelo fora de /api/ps e outra com o modelo carregado. Compare primeiro conteúdo e duração da carga.

**Slide 4**
[layout: split]
[eyebrow: Como medir]
[image: ../assets/03.png]
[caption: O cliente cronometra a entrega e o servidor informa suas métricas na linha final.]

Conte três medidas

- Primeiro conteúdo no cliente.
- Tempo até a conclusão.
- Taxa de geração calculada com eval_count e eval_duration.

**Slide 5**
[layout: split]
[eyebrow: Dados históricos • Ollama 0.35.1]
[image: ../assets/04.png]
[caption: Benchmark de três modelos em CPU, com 12 chamadas por modelo.]

Maior vazão pode acompanhar uma resposta mais longa

O Qwen 0.5B produziu mais tokens por segundo em média. O Qwen 1.5B produziu menos tokens e apresentou menor tempo total médio naquele conjunto.

**Slide 6**
[layout: cta]
[eyebrow: Experimento]
[gallery: ../assets/06_streaming_terminal.png, ../assets/04.png]

Repita o caso com seu próprio prompt

Compare a primeira chamada e a chamada aquecida com a mesma versão, o mesmo modelo e as mesmas opções. Junto com os tempos, registre o número de tokens e confira se o resultado atende à tarefa.

> github.com/pathbit/pathbit-academy-ai
