# 🔧 Solução: Captura de API Keys no Google Colab

## 🎯 Problema

No Google Colab, não é possível usar arquivos `.env` como no ambiente local. É necessário usar o sistema de secrets do Colab ou capturar a API key diretamente do usuário de forma segura.

## 🔍 Diferenças entre Ambientes

### **💻 Ambiente Local:**

- Usa arquivo `.env` com `config_local.py`
- API key armazenada de forma persistente
- Não requer interação do usuário

### **🌐 Google Colab:**

- Usa sistema de secrets do Colab (`google.colab.userdata`)
- API key armazenada de forma segura no Colab
- Configuração uma única vez

## ✅ Solução Implementada

### **Configuração Elegante e Profissional:**

```python
# 🚀 Configuração para execução local e Colab
# ============================================

# Adicionar o diretório src ao path para importar módulos locais
import sys
import os
sys.path.append('../src')

# Constante com o nome da secret adicionada no Notebook
GROQ_API_KEY_NAME = "GROQ_API_KEY"

# Importar configuração local
try:
    from config_local import configurar_api_key, exibir_markdown, exibir_resposta_formatada
    print("✅ Configuração local carregada")
except ImportError:
    print("⚠️  Executando em modo Colab")

    # Funções para Colab
    def configurar_api_key():
        from google.colab import userdata
        try:
            groq_api_key = userdata.get(GROQ_API_KEY_NAME)
            os.environ[GROQ_API_KEY_NAME] = groq_api_key
            print(f"✅ {GROQ_API_KEY_NAME}: {os.environ[GROQ_API_KEY_NAME][:6]}******")
            return True
        except Exception as e:
            print(f"❌ Erro ao configurar API Key: {e}")
            return False

# Configurar API Key
configurar_api_key()
```

### **Arquivo config_local.py (Ambiente Local):**

```python
def configurar_api_key():
    """Configura a API key do Groq para execução local."""
    try:
        # Carregar variáveis de ambiente do arquivo .env
        load_dotenv()

        groq_api_key = os.getenv('GROQ_API_KEY')

        if groq_api_key:
            os.environ['GROQ_API_KEY'] = groq_api_key
            print(f"✅ GROQ_API_KEY: {groq_api_key[:6]}******")
            return True
        else:
            print("⚠️ GROQ_API_KEY não encontrada no arquivo .env")
            return False

    except Exception as e:
        print(f"❌ Erro ao configurar API Key: {e}")
        return False
```

## 🎯 Vantagens da Solução

### **✅ Compatibilidade Total:**

- Funciona no ambiente local (módulo `config_local.py`)
- Funciona no Google Colab (secrets do Colab)
- Detecção automática do ambiente

### **✅ Segurança:**

- Usa `google.colab.userdata` para secrets no Colab
- API key não aparece em logs ou outputs
- Mascaramento da chave na exibição

### **✅ Experiência do Usuário:**

- Configuração uma única vez no Colab
- Mensagens claras sobre o que está acontecendo
- Funções utilitárias para formatação

### **✅ Manutenibilidade:**

- Código limpo e organizado
- Separação clara entre ambiente local e Colab
- Fácil de estender para outras APIs

## 📋 Como Usar

### **No Ambiente Local:**

1. Crie um arquivo `.env` na raiz do projeto
2. Adicione: `GROQ_API_KEY=sua_chave_aqui`
3. O módulo `config_local.py` carrega automaticamente

### **No Google Colab:**

1. Vá em **Tools → Secrets**
2. Adicione uma secret com nome `GROQ_API_KEY`
3. Execute o notebook - a configuração é automática

## 🔧 Exemplo Prático

```python
# Verificar disponibilidade
groq_disponivel, groq_api_key = verificar_groq_disponivel()

if groq_disponivel:
    groq_client = setup_groq_client(groq_api_key)
    if groq_client:
        print("🎯 Sistema RAG completo pronto para uso!")
    else:
        groq_disponivel = False
        groq_client = None
else:
    groq_client = None
    print("ℹ️ Continuando apenas com busca semântica")
```

## 💡 Dicas Importantes

1. **Use secrets no Colab** para máxima segurança
2. **Detecte o ambiente** antes de tentar importar módulos
3. **Mascare a API key** na exibição (primeiros 6 caracteres)
4. **Forneça fallbacks** para quando a API não estiver disponível
5. **Organize o código** em módulos separados

## 🔗 Recursos

- **Groq Console:** https://console.groq.com/keys
- **Colab Secrets:** https://colab.research.google.com/
- **Documentação Groq:** https://console.groq.com/docs

---

**Última atualização:** 02/10/2025
**Versão:** 2.0.0
