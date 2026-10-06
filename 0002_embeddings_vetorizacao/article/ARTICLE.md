# Como embeddings e vetorização estruturam a representação matemática do texto em sistemas de IA

Grande parte da intuição popular sobre inteligência artificial imagina que grandes modelos de linguagem operam diretamente sobre palavras, conceitos ou ideias abstratas. Nos bastidores da arquitetura de software, porém, processadores e aceleradores gráficos são incapazes de processar texto bruto. Computadores operam exclusivamente sobre matrizes, tensores e álgebra linear.

A tecnologia que torna possível a transição entre o vocabulário humano e o cálculo numérico é o embedding vetorial. Longe de ser apenas uma palavra da moda ou um detalhe secundário de bibliotecas de machine learning, a vetorização semântica constitui a espinha dorsal de qualquer arquitetura moderna de busca inteligente, classificação de documentos, desduplicação de registros e recuperação contextual em pipelines de RAG.

Compreender a matemática, a geometria e os limites práticos dos embeddings permite que equipes de engenharia tomem decisões conscientes de modelagem. Este artigo desvenda o funcionamento interno dessa camada, analisa como frases são projetadas em espaços multidimensionais, avalia métricas de distância geométrica e demonstra como construir sistemas estáveis de busca semântica em português sem depender de serviços proprietários ou orçamentos proibitivos.

---

## Da correspondência léxica ao espaço vetorial contínuo

Para compreender o salto geracional dos embeddings, vale revisar como a engenharia de software tradicional lidava com recuperação de informação.

Durante décadas, a busca em bancos de dados dependeu de correspondência léxica direta baseada em palavras-chave, consultas booleanas com SQL ou algoritmos de relevância estatística como TF-IDF e BM25. Esses métodos avaliam a frequência exata dos termos em cada documento. Se um usuário pesquisa por automóvel e o documento corporativo utiliza a palavra carro ou veículo, o sistema léxico tradicional simplesmente falha em recuperar o registro, a menos que dicionários manuais de sinônimos tenham sido mantidos a custo de muito esforço humano.

![Conceito de Embeddings](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0002_embeddings_vetorizacao/assets/01.png)

> Figura 1. Projeção de palavras e conceitos em um espaço matemático onde proximidade espacial reflete afinidade semântica.

Os modelos de embeddings resolvem essa fragilidade projetando textos em um espaço vetorial contínuo de alta dimensionalidade. Em vez de tratar palavras como símbolos isolados e ortogonais, o modelo mapeia sentenças inteiras para coordenadas numéricas densas. Conceitos semanticamente semelhantes passam a ocupar regiões próximas dentro desse espaço geométrico, permitindo que o sistema reconheça afinidade entre termos distintos sem exigir regras manuais.

---

## O processo de vetorização sob o capô

A transformação de uma sequência textual em um vetor de números reais segue um pipeline computacional bem estruturado dentro da arquitetura Transformer.

Primeiramente, o texto de entrada é dividido em unidades menores chamadas subtokens por meio de tokenizadores estatísticos como WordPiece ou Byte-Pair Encoding. Cada subtoken é convertido em um identificador inteiro que aponta para uma tabela interna de pesos aprendidos durante o treinamento.

![Processo de Vetorização](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0002_embeddings_vetorizacao/assets/02.png)

> Figura 2. O pipeline de conversão de texto bruto em representação vetorial através das camadas do Transformer.

Em seguida, essa sequência passa pelas camadas de autoatenção do modelo, onde cada token recalcula seu significado em função de todas as outras palavras ao seu redor. Ao final da rede neural, o modelo gera uma matriz intermediária com vetores individuais para cada token. Para consolidar essa matriz em um único vetor representativo da sentença inteira, aplica-se uma etapa de agregação, conhecida na literatura como pooling.

A estratégia de mean pooling, por exemplo, calcula a média aritmética de todos os vetores de tokens ponderados pela máscara de atenção, resultando em um vetor único e denso, com centenas de dimensões, que sintetiza o significado semântico completo do trecho.

---

## A geometria da similaridade semântica

Uma vez que documentos e consultas são convertidos em vetores, a comparação entre textos deixa de ser uma comparação de strings e vira um cálculo trigonométrico em alta dimensionalidade.

![Transformação Texto para Números](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0002_embeddings_vetorizacao/assets/03.png)

> Figura 3. Representação de sentenças transformadas em coordenadas vetoriais densas de dimensão fixa.

A métrica mais consolidada para avaliar a proximidade entre dois vetores é a similaridade de cosseno. Essa medida calcula o cosseno do ângulo formado entre os dois vetores no espaço multidimensional, desconsiderando a magnitude absoluta ou o comprimento do texto para focar exclusivamente na orientação direcional:

$$\text{Similaridade}(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\|_2 \|\mathbf{v}\|_2} = \frac{\sum_{i=1}^d u_i v_i}{\sqrt{\sum_{i=1}^d u_i^2} \sqrt{\sum_{i=1}^d v_i^2}}$$

![Cálculo de Similaridade](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0002_embeddings_vetorizacao/assets/04.png)

> Figura 4. Demonstração geométrica da similaridade de cosseno avaliando o ângulo entre vetores no plano.

Quando os vetores são previamente normalizados pela norma euclidiana ($L_2 = 1$), a magnitude de cada vetor torna-se unitária. Isso gera uma vantagem prática imensa em engenharia de software: o cálculo do cosseno se reduz a um produto escalar simples, que pode ser executado em frações de milissegundo através de instruções SIMD no processador ou multiplicação de tensores em GPU.

Um ponto crítico comprovado em laboratório diz respeito ao suporte linguístico do modelo. Ao calcular a similaridade entre sentenças em português com o modelo multilíngue `paraphrase-multilingual-MiniLM-L12-v2`, a frase "O cachorro está brincando no parque" alcança similaridade de 0.304 com "O animal de estimação está feliz", enquanto sua similaridade com "O carro está na garagem" cai para 0.046. 

No entanto, se a mesma comparação for executada com o modelo `all-MiniLM-L6-v2`, treinado exclusivamente em inglês, os escores invertem de forma desastrosa: o modelo aponta 0.517 de afinidade para a frase do carro e apenas 0.290 para o animal de estimação. Em projetos operando no Brasil, a adoção de pesos multilíngues é um requisito inegociável de arquitetura.

---

## Panorama dos tipos de representação vetorial

A literatura de processamento de linguagem natural desenvolveu diferentes modalidades de representação para atender requisitos operacionais distintos.

![Comparação entre os modelos](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0002_embeddings_vetorizacao/assets/05.png)

> Figura 5. Arquiteturas clássicas e modernas de geração de representações numéricas.

Os embeddings de palavras, representados historicamente por Word2Vec e GloVe, atribuem um único vetor fixo para cada vocábulo. Embora sejam extremamente leves e velozes, eles sofrem de incapacidade contextual, tratando a palavra banco de uma instituição financeira exatamente com as mesmas coordenadas do assento de uma praça pública.

Os embeddings de sentenças, consolidados por arquiteturas siamesas como Sentence-BERT e modelos da família E5, capturam o contexto completo da frase e do parágrafo. Eles representam o padrão dominante para recuperação contextual, busca semântica corporativa e classificação de intenções.

Para necessidades de agregação macroscópica, os embeddings de documentos utilizam janelas ampliadas de atenção para capturar o tema geral de laudos e contratos extensos, sendo muito aplicados em tarefas de clustering e organização de repositórios.

Por fim, os embeddings multimodais, exemplificados por arquiteturas como CLIP e SigLIP, projetam textos e imagens em um espaço compartilhado de representação, permitindo que uma busca textual recupere fotografias ou diagramas técnicos diretamente com base em seu conteúdo visual.

---

## Casos de uso consolidados na engenharia corporativa

A aplicação de embeddings vai muito além da simples substituição do campo de busca de um portal.

![Busca Semântica](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0002_embeddings_vetorizacao/assets/06.png)

> Figura 6. Busca semântica mapeando termos coloquiais de usuários para documentação técnica de investimentos.

Na busca semântica, o usuário pode digitar termos coloquiais como "como guardar dinheiro para render todo mês" e o sistema recupera com precisão artigos sobre "aplicação em CDB com liquidez diária e renda fixa", superando barreiras de vocabulário formal.

![Sistema de Recomendação](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0002_embeddings_vetorizacao/assets/07.png)

> Figura 7. Mecanismos de recomendação de conteúdo baseados na distância entre perfis de consumo e catálogo de itens.

Em motores de recomendação, o histórico de consumo de um profissional em materiais sobre data science e aprendizado de máquina posiciona seu perfil vetorial próximo a cursos práticos de bibliotecas analíticas, gerando sugestões contextuais sem necessidade de regras manuais exaustivas.

![Classificação de Documentos](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0002_embeddings_vetorizacao/assets/08.png)

> Figura 8. Agrupamento e roteamento de documentos por meio de proximidade espacial em clusters temáticos.

Na triagem e classificação de chamados de atendimento, documentos similares formam agrupamentos densos. É importante notar um aprendizado prático de engenharia: comparar o texto diretamente contra descrições curtas de categorias pode induzir a erros de fronteira. A abordagem robusta consiste em treinar um classificador linear leve, como regressão logística, alimentado pelos embeddings de centenas de exemplos históricos já validados pela equipe humana.

![Detecção de Duplicatas](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0002_embeddings_vetorizacao/assets/09.png)

> Figura 9. Identificação de perguntas redundantes em bases de conhecimento aplicando limiares de corte angular.

Na desduplicação de bases de suporte, perguntas redigidas de formas distintas, como "como redefinir minha senha" e "esqueci meu login e preciso resetar o acesso", geram pontuação de similaridade angular superior a 0.90, viabilizando a unificação automática de artigos redundantes.

![RAG com Embeddings](https://raw.githubusercontent.com/pathbit/pathbit-academy-ai/refs/heads/master/0002_embeddings_vetorizacao/assets/10.png)

> Figura 10. A recuperação vetorial alimentando o contexto do modelo gerativo em arquiteturas de RAG.

Em arquiteturas de RAG, o embedding atua como o filtro cirúrgico que vasculha milhões de fragmentos de documentação para injetar no prompt do modelo apenas os dois ou três parágrafos estritamente necessários para embasar a resposta.

---

## Critérios objetivos para escolha de modelos em produção

A tabela abaixo compila as principais opções de mercado, seus custos computacionais e suas indicações de uso:

| Modelo | Dimensões | Contexto | Idiomas | Hospedagem | Custo | Indicação Principal |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `paraphrase-multilingual-MiniLM-L12-v2` | 384 | 128 tokens | Multilíngue | Local (CPU) | Gratuito | Microsserviços ultrarrápidos e tarefas de baixa latência |
| `multilingual-e5-base` | 768 | 512 tokens | Multilíngue | Local (CPU/GPU) | Gratuito | Equilíbrio perfeito entre precisão e custo em servidores próprios |
| `nomic-embed-text-v1.5` | 768 | 8.192 tokens | Multilíngue | Local (Ollama) | Gratuito | Documentos extensos e RAG corporativo 100% offline |
| `text-embedding-3-small` | 1.536 | 8.191 tokens | Multilíngue | Cloud API | Pago | Protótipos rápidos sem gestão de servidores locais |
| `text-embedding-3-large` | 3.072 | 8.191 tokens | Multilíngue | Cloud API | Pago | Casos de altíssima exigência em nuvem gerenciada |

Para bases com até dez mil documentos, modelos compactos de 384 dimensões em CPU costumam ser mais do que suficientes, entregando tempos de resposta inferiores a dez milissegundos. Quando a base atinge centenas de milhares de trechos ou lida com terminologias técnicas complexas, modelos de 768 dimensões com índices vetoriais especializados representam a melhor arquitetura de produção.

---

## Execução prática do laboratório passo a passo

O repositório fornece um laboratório completo em Python para testar a geração de embeddings, cálculo de similaridades e desduplicação de textos diretamente no seu computador ou via nuvem no Google Colab.

A preparação do ambiente local requer apenas a criação do ambiente virtual e a instalação das dependências:

```bash
cd pathbit-academy-ai/0002_embeddings_vetorizacao

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python src/main.py --check
```

O download dos pesos de modelos abertos como `paraphrase-multilingual-MiniLM-L12-v2` é gerenciado automaticamente pela biblioteca `sentence-transformers` na primeira execução, sem necessidade de chaves de API nem autenticação externa.

Para explorar as matrizes de similaridade e a visualização gráfica de agrupamentos semânticos passo a passo, inicie o Jupyter Notebook interativo:

```bash
jupyter notebook notebooks/embeddings_vetorizacao.ipynb
```

---

## Próximos passos na jornada de IA da Pathbit Academy

Compreender o cálculo de similaridade e a estrutura dos espaços vetoriais prepara o terreno para a próxima fronteira da engenharia de inteligência artificial. Quando o volume de vetores cresce de algumas centenas para milhões de registros, realizar comparações exaustivas torna-se inviável.

No [Artigo 0003 (RAG e Vector Database)](https://github.com/pathbit/pathbit-academy-ai/blob/master/0003_rag_vector_database/article/ARTICLE.md), mostramos como bancos de dados vetoriais utilizam estruturas de índices aproximados para encontrar os fragmentos mais relevantes em frações de segundo, alimentando LLMs com conhecimento verificado em tempo real.

---

## Referências

- [Reimers, Nils e Gurevych, Iryna: Sentence-BERT (Sentence Embeddings using Siamese BERT-Networks)](https://arxiv.org/abs/1908.10084)
- [Wang, Liang et al.: Text Embeddings by Weakly-Supervised Pre-Training (E5)](https://arxiv.org/abs/2212.03533)
- [Nussbaum, Zach et al.: Nomic Embed (Training a Reproducible Long Context Text Embedder)](https://arxiv.org/abs/2402.01613)
- [Documentação oficial da biblioteca Sentence Transformers](https://sbert.net/)
- [Manning, Christopher et al.: Introduction to Information Retrieval (Cambridge University Press)](https://nlp.stanford.edu/IR-book/)

---

Repositório oficial no GitHub no endereço https://github.com/pathbit/pathbit-academy-ai no módulo 0002_embeddings_vetorizacao.

#InteligenciaArtificial #Embeddings #BuscaSemantica #Vetorizacao #Python #SentenceBERT #EngenhariaDeSoftware #PathbitAcademy
