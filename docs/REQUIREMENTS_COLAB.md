# 🔧 Guia de Instalação para Google Colab

> Clone o repo antes dos comandos com `/content/pathbit-academy-ai`.
> `requirements_colab.txt` não existe mais; use o requirements do módulo ou
> a célula de instalação do notebook.

## 🚨 Problema de Compatibilidade do tqdm

Se você está enfrentando este erro no Google Colab:

```bash
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
datasets 4.0.0 requires tqdm>=4.66.3, but you have tqdm 4.66.1 which is incompatible.
dataproc-spark-connect 0.8.3 requires tqdm>=4.67, but you have tqdm 4.66.1 which is incompatible.
```

## ✅ Solução Rápida

### **Opção 1: Usar o requirements do módulo**

`requirements_colab.txt` foi removido. Use as células de setup do notebook ou clone o repo e instale o requirements do módulo:

```python
# No Google Colab, execute:
!git clone https://github.com/pathbit/pathbit-academy-ai.git /content/pathbit-academy-ai
%pip install -r /content/pathbit-academy-ai/0004_rag_vs_finetuning/requirements.txt
```

### **Opção 2: Correção Manual**

Execute esta célula **ANTES** de instalar outras dependências:

```python
# 🔧 Correção para conflito de dependências do tqdm
!pip install --upgrade tqdm>=4.67 --force-reinstall
```

## 📁 Arquivos Disponíveis

### **0001_llm_x_lrm/**

- `requirements.txt` - Para instalação local
- Células de setup do notebook - Para Google Colab

### **0002_embeddings_vetorizacao/**

- `requirements.txt` - Para instalação local
- Células de setup do notebook - Para Google Colab

## 🚀 Instalação Passo a Passo no Colab

1. **Abra o notebook no Google Colab**
2. **Execute esta célula primeiro:**
   ```python
   # 🔧 Correção para conflito de dependências
   !pip install --upgrade tqdm>=4.67 --force-reinstall
   ```
3. **Depois execute:**
   ```python
   # Instalar dependências do projeto
   %pip install -r /content/pathbit-academy-ai/0004_rag_vs_finetuning/requirements.txt
   ```

## 🔍 Verificação

Para verificar se a instalação foi bem-sucedida:

```python
import tqdm
print(f"✅ tqdm versão: {tqdm.__version__}")
# Confira também imports e python -m pip check; uma versão não valida todas as dependências.
```

## 📚 Documentação Completa

Para mais detalhes e outras soluções, consulte:

- **[SOLUCAO_ERRO_COLAB.md](./SOLUCAO_ERRO_COLAB.md)**

---

**💡 Dica:** Sempre execute a correção do `tqdm` **ANTES** de instalar outras dependências para evitar conflitos!
