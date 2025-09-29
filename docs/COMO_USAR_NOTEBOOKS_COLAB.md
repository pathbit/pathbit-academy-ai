# 📚 Como Usar os Notebooks no Google Colab

## 🎯 **Guia Completo de Instalação**

Os notebooks agora possuem **correção automática** para problemas de compatibilidade do `tqdm` no Google Colab.

## 🔧 **Estrutura dos Notebooks Atualizados**

### **1. Célula de Correção Automática**

```
🔧 CORREÇÃO AUTOMÁTICA PARA GOOGLE COLAB
==========================================
```

- **Detecta automaticamente** se está rodando no Google Colab
- **Aplica correção** do `tqdm` antes de instalar outras dependências
- **Resolve conflitos** com `datasets` e `dataproc-spark-connect`

### **2. Célula de Instalação de Dependências**

```
📦 INSTALAÇÃO DAS DEPENDÊNCIAS
===============================
```

- **Instala as bibliotecas** necessárias para o projeto
- **Usa versões compatíveis** do `tqdm` (>=4.67)
- **Funciona tanto no Colab** quanto localmente

## 🚀 **Como Executar no Google Colab**

### **Passo 1: Abrir o Notebook**

1. Clique no botão **"Open In Colab"** no notebook
2. O notebook será aberto no Google Colab

### **Passo 2: Executar as Células de Instalação**

1. **Execute a primeira célula** (correção automática)
2. **Execute a segunda célula** (instalação de dependências)
3. **Continue com o resto** do notebook normalmente

### **Passo 3: Configurar API Key (se necessário)**

- Para notebooks que usam Groq: configure sua API Key nas secrets do Colab
- Para notebooks de embeddings: não precisa de configuração adicional

## ✅ **O que Foi Corrigido**

### **Problema Original:**

```bash
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
datasets 4.0.0 requires tqdm>=4.66.3, but you have tqdm 4.66.1 which is incompatible.
dataproc-spark-connect 0.8.3 requires tqdm>=4.67, but you have tqdm 4.66.1 which is incompatible.
```

### **Solução Implementada:**

```python
# Detectar se estamos no Google Colab
try:
    import google.colab
    IN_COLAB = True
    print("🌐 Detectado: Google Colab")
    print("🔧 Aplicando correção para conflito de tqdm...")

    # CORREÇÃO: Atualizar tqdm para resolver conflitos
    get_ipython().run_line_magic('pip', 'install --upgrade tqdm>=4.67 --force-reinstall --quiet')
    print("✅ tqdm atualizado com sucesso!")

except ImportError:
    IN_COLAB = False
    print("💻 Detectado: Ambiente Local")
```

## 📋 **Notebooks Atualizados**

### **0001_llm_x_lrm/notebooks/comparacao_llm_lrm.ipynb**

- ✅ Célula de correção automática do `tqdm`
- ✅ Célula de instalação do `groq`
- ✅ Configuração automática para Colab e local

### **0002_embeddings_vetorizacao/notebooks/embeddings_vetorizacao.ipynb**

- ✅ Célula de correção automática do `tqdm`
- ✅ Célula de instalação de todas as dependências
- ✅ Configuração automática para Colab e local

## 🎯 **Vantagens da Nova Implementação**

1. **✅ Correção Automática:** Não precisa mais executar comandos manuais
2. **✅ Detecção Inteligente:** Funciona tanto no Colab quanto localmente
3. **✅ Organização Clara:** Células separadas para cada função
4. **✅ Mensagens Informativas:** Feedback claro sobre o que está acontecendo
5. **✅ Compatibilidade Total:** Resolve todos os conflitos de dependências

## 🚨 **Importante**

- **Sempre execute as células na ordem:** correção primeiro, depois instalação
- **Aguarde a conclusão** de cada célula antes de continuar
- **Se houver erro:** verifique se está executando no Google Colab (não localmente)
- **Para ambiente local:** as correções não são aplicadas (não são necessárias)

## 🎉 **Resultado Final**

Agora você pode executar os notebooks no Google Colab **sem problemas de compatibilidade**!

O sistema detecta automaticamente o ambiente e aplica as correções necessárias, garantindo que tudo funcione perfeitamente.

---

**💡 Dica:** Se você encontrar algum problema, verifique se executou as células de instalação na ordem correta!
