# 🔧 Solução: Captura de API Keys no Google Colab

## 🎯 Problema

No Google Colab, não é possível usar arquivos `.env` como no ambiente local. É necessário capturar a API key diretamente do usuário de forma segura.

## 🔍 Diferenças entre Ambientes

### **💻 Ambiente Local:**

- Usa arquivo `.env` com `load_dotenv()`
- API key armazenada de forma persistente
- Não requer interação do usuário

### **🌐 Google Colab:**

- Não tem acesso a arquivos `.env`
- Precisa capturar API key via input
- Requer interação do usuário a cada execução

## ✅ Solução Implementada

### **Função Inteligente de Detecção:**

```python
def verificar_groq_disponivel():
    """Verifica se a API do Groq está disponível"""
    try:
        # 1. Tentar arquivo .env (ambiente local)
        load_dotenv()
        groq_api_key = os.getenv('GROQ_API_KEY')

        if groq_api_key:
            print("✅ GROQ_API_KEY encontrada no arquivo .env!")
            return True, groq_api_key

        # 2. Se Colab, capturar do usuário
        if IN_COLAB:
            print("🌐 Detectado Google Colab - capturando API key do usuário...")
            try:
                from getpass import getpass
                print("🔑 Digite sua GROQ_API_KEY (será ocultada):")
                groq_api_key = getpass("GROQ_API_KEY: ").strip()

                if groq_api_key:
                    print("✅ GROQ_API_KEY capturada com sucesso!")
                    return True, groq_api_key
                else:
                    print("⚠️ GROQ_API_KEY não fornecida")
                    return False, None
            except Exception as e:
                print(f"❌ Erro ao capturar API key: {e}")
                return False, None
        else:
            print("⚠️ GROQ_API_KEY não encontrada no arquivo .env")
            print("💡 Para usar localmente, crie um arquivo .env com:")
            print("   GROQ_API_KEY=sua_chave_aqui")
            return False, None

    except Exception as e:
        print(f"❌ Erro ao verificar GROQ_API_KEY: {e}")
        return False, None
```

### **Instalação Automática no Colab:**

```python
def setup_groq_client(api_key):
    """Configura o cliente Groq"""
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        print("🤖 Cliente Groq configurado com sucesso!")
        return client
    except ImportError:
        print("❌ Biblioteca 'groq' não instalada.")
        if IN_COLAB:
            print("🔧 Instalando groq no Google Colab...")
            get_ipython().run_line_magic('pip', 'install groq --quiet')
            try:
                from groq import Groq
                client = Groq(api_key=api_key)
                print("✅ Groq instalado e configurado!")
                return client
            except Exception as e:
                print(f"❌ Erro após instalação: {e}")
                return None
        else:
            print("💡 Execute: pip install groq")
            return None
```

## 🎯 Vantagens da Solução

### **✅ Compatibilidade Total:**

- Funciona no ambiente local (arquivo `.env`)
- Funciona no Google Colab (captura segura)
- Detecção automática do ambiente

### **✅ Segurança:**

- Usa `getpass()` para ocultar a API key no Colab
- Não armazena a key em logs ou outputs
- Fallback seguro se a captura falhar

### **✅ Experiência do Usuário:**

- Instalação automática no Colab
- Mensagens claras sobre o que está acontecendo
- Instruções específicas para cada ambiente

## 📋 Como Usar

### **No Ambiente Local:**

1. Crie um arquivo `.env` na raiz do projeto
2. Adicione: `GROQ_API_KEY=sua_chave_aqui`
3. Execute o notebook normalmente

### **No Google Colab:**

1. Execute a célula de configuração
2. Digite sua API key quando solicitado (será ocultada)
3. O sistema instala e configura automaticamente

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
    print("💡 Para ativar Groq: Configure GROQ_API_KEY")
```

## 💡 Dicas Importantes

1. **Use `getpass()`** no Colab para ocultar a API key
2. **Detecte o ambiente** antes de tentar capturar
3. **Instale automaticamente** dependências no Colab
4. **Forneça fallbacks** para quando a API não estiver disponível
5. **Dê instruções claras** para cada ambiente

## 🔗 Recursos

- **Groq Console:** https://console.groq.com/keys
- **Documentação Groq:** https://console.groq.com/docs
- **getpass Python:** https://docs.python.org/3/library/getpass.html

---

**Última atualização:** 02/10/2025
**Versão:** 1.0.0
