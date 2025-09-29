# 🔧 Soluções para Erros do Google Colab

## ❌ Erros Encontrados

### **Erro 1: Módulo Google não encontrado**

```bash
ModuleNotFoundError: No module named 'google'
```

### **Erro 2: Conflito de dependências do tqdm**

```bash
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
datasets 4.0.0 requires tqdm>=4.66.3, but you have tqdm 4.66.1 which is incompatible.
dataproc-spark-connect 0.8.3 requires tqdm>=4.67, but you have tqdm 4.66.1 which is incompatible.
```

## ✅ Soluções

### **🔧 Solução para Erro 1: Módulo Google não encontrado**

#### **Opção 1: Substituir a célula problemática**

Na célula que está dando erro, substitua todo o código por:

```python
# ✅ API Key já configurada na primeira célula
# Esta célula não é mais necessária
print("✅ Configuração já realizada na primeira célula")
```

#### **Opção 2: Executar apenas as células necessárias**

1. **Execute a primeira célula** (que foi adicionada) - ela configura tudo automaticamente
2. **Pule a célula problemática** (que contém `from google.colab import userdata`)
3. **Continue com as próximas células** normalmente

#### **Opção 3: Configurar API Key manualmente**

Se preferir, adicione esta célula antes de executar o resto:

```python
import os
import getpass

# Configurar API Key do Groq
GROQ_API_KEY_NAME = "GROQ_API_KEY"

if GROQ_API_KEY_NAME not in os.environ:
    print("⚠️  GROQ_API_KEY não definida.")
    print("Opções:")
    print("1. Definir como variável de ambiente: export GROQ_API_KEY='sua_chave'")
    print("2. Ou digitar agora:")

    api_key = getpass.getpass("Digite sua API Key do Groq: ").strip()
    if api_key:
        os.environ[GROQ_API_KEY_NAME] = api_key
        print(f"✅ {GROQ_API_KEY_NAME} configurada")
    else:
        print("❌ API Key não fornecida")
else:
    print(f"✅ {GROQ_API_KEY_NAME}: {os.environ[GROQ_API_KEY_NAME][:6]}******")
```

### **🔧 Solução para Erro 2: Conflito de dependências do tqdm**

#### **Método 1: Atualizar tqdm (Recomendado)**

Execute esta célula **ANTES** de instalar outras dependências:

```python
# 🔧 Correção para conflito de dependências do tqdm
!pip install --upgrade tqdm>=4.67 --force-reinstall
```

#### **Método 2: Instalação forçada com --force-reinstall**

Se o Método 1 não funcionar, use:

```python
# 🔧 Forçar reinstalação do tqdm
!pip install tqdm>=4.67 --force-reinstall --no-deps
```

#### **Método 3: Limpar cache e reinstalar**

```python
# 🔧 Limpar cache e reinstalar
!pip cache purge
!pip uninstall tqdm -y
!pip install tqdm>=4.67
```

#### **Método 4: Instalação completa com dependências atualizadas**

```python
# 🔧 Instalação completa com versões compatíveis
!pip install --upgrade pip
!pip install tqdm>=4.67 datasets>=4.0.0 --force-reinstall
```

### **🚀 Instalação Correta das Dependências**

Para evitar conflitos, execute as dependências nesta ordem:

```python
# 1️⃣ Primeiro: Atualizar tqdm
!pip install --upgrade tqdm>=4.67

# 2️⃣ Depois: Instalar outras dependências
!pip install groq==0.32.0
!pip install sentence-transformers==3.1.1
!pip install numpy==1.26.4
!pip install scikit-learn==1.4.2
!pip install matplotlib==3.9.0
!pip install seaborn==0.13.2
!pip install pandas==2.2.2
!pip install plotly==5.22.0
!pip install jupyter==1.1.1
!pip install ipython==9.5.0
```

### **💡 Nota Importante**

**Os arquivos `requirements_colab.txt` foram removidos** porque não fazem sentido no contexto do Google Colab. O Colab roda na nuvem e não acessa arquivos locais do projeto. As dependências são instaladas diretamente nas células dos notebooks usando `%pip install` ou `!pip install`.

## 🚀 Próximos Passos

1. **Para Erro 1**: Execute a primeira célula (configuração automática) e pule ou substitua a célula problemática
2. **Para Erro 2**: Execute a correção do tqdm **ANTES** de instalar outras dependências
3. Continue executando o resto do notebook normalmente

Os notebooks agora funcionam tanto no **Google Colab** quanto **localmente**! 🎉
