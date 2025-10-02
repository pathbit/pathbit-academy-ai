# 📚 Documentação Técnica

Esta pasta contém toda a documentação técnica do projeto **Pathbit Academy AI**.

## 📋 Índice de Documentos

### 🔧 Soluções para Problemas

| Documento                                                                        | Descrição                                                                                     | Quando Usar                                                         |
| -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **[SOLUCAO_ERRO_COLAB.md](./SOLUCAO_ERRO_COLAB.md)**                             | Resolução de erros do Google Colab (módulo google e conflitos de tqdm)                        | Ao executar notebooks no Colab e encontrar erros de compatibilidade |
| **[SOLUCAO_ERRO_GROQ.md](./SOLUCAO_ERRO_GROQ.md)**                               | Resolução do erro `TypeError: Client.__init__() got an unexpected keyword argument 'proxies'` | Ao encontrar erro de compatibilidade com a API do Groq              |
| **[SOLUCAO_ERRO_CHROMADB_TELEMETRIA.md](./SOLUCAO_ERRO_CHROMADB_TELEMETRIA.md)** | Resolução dos erros de telemetria do ChromaDB (`capture() takes 1 positional argument`)       | Ao ver mensagens de erro sobre telemetria ao usar ChromaDB          |
| **[SOLUCAO_ERRO_MATPLOTLIB_EMOJIS.md](./SOLUCAO_ERRO_MATPLOTLIB_EMOJIS.md)**     | Resolução de warnings de fonte do matplotlib com emojis (`Glyph missing from font`)           | Ao ver warnings sobre glifos ausentes nos gráficos                  |
| **[SOLUCAO_CAPTURA_API_KEY_COLAB.md](./SOLUCAO_CAPTURA_API_KEY_COLAB.md)**       | Como capturar API keys no Google Colab usando getpass vs arquivo .env local                   | Ao configurar APIs no Colab que precisam de captura de chaves       |

### 🚀 Guias de Uso

| Documento                                                          | Descrição                                                                       | Quando Usar                                      |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------- | ------------------------------------------------ |
| **[COMO_USAR_NOTEBOOKS_COLAB.md](./COMO_USAR_NOTEBOOKS_COLAB.md)** | Guia completo de como usar os notebooks no Google Colab com correção automática | Ao executar notebooks no Colab pela primeira vez |
| **[REQUIREMENTS_COLAB.md](./REQUIREMENTS_COLAB.md)**               | Guia de instalação específico para Google Colab com requirements otimizados     | Para resolver conflitos de dependências no Colab |

### 📦 Gerenciamento de Dependências

| Documento                                                | Descrição                                    | Quando Usar                                       |
| -------------------------------------------------------- | -------------------------------------------- | ------------------------------------------------- |
| **[ATUALIZACOES_VERSOES.md](./ATUALIZACOES_VERSOES.md)** | Histórico de atualizações dos pacotes Python | Para entender as mudanças nas versões dos pacotes |

### 📋 Documentação do Projeto

| Documento                                            | Descrição                                    | Quando Usar                                  |
| ---------------------------------------------------- | -------------------------------------------- | -------------------------------------------- |
| **[RESUMO_ORGANIZACAO.md](./RESUMO_ORGANIZACAO.md)** | Resumo da estrutura e organização do projeto | Para entender a organização geral do projeto |

## 🚀 Como Usar Esta Documentação

1. **Identifique o problema** que está enfrentando
2. **Consulte a tabela acima** para encontrar o documento relevante
3. **Siga as instruções** passo a passo
4. **Se o problema persistir**, verifique se há atualizações mais recentes

## 📝 Convenções

- **🔧** = Soluções técnicas
- **🚀** = Guias de uso e instruções
- **📦** = Gerenciamento de dependências
- **📋** = Documentação do projeto
- **⚠️** = Avisos importantes
- **✅** = Confirmação de sucesso
- **❌** = Indicação de erro

## 🤝 Contribuindo com a Documentação

Se você encontrar um novo problema ou tiver uma solução melhor:

1. **Documente o problema** seguindo o padrão dos arquivos existentes
2. **Teste a solução** antes de documentar
3. **Inclua exemplos práticos** sempre que possível
4. **Atualize este índice** se necessário

---

**Última atualização:** 02/10/2025
**Versão da documentação:** 1.3.0
