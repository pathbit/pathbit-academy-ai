# 🔧 Guia de Instalação para Google Colab

## 🚨 Problema de Compatibilidade do tqdm

Se você está enfrentando este erro no Google Colab:

```bash
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
datasets 4.0.0 requires tqdm>=4.66.3, but you have tqdm 4.66.1 which is incompatible.
dataproc-spark-connect 0.8.3 requires tqdm>=4.67, but you have tqdm 4.66.1 which is incompatible.
```

## ✅ Solução Rápida

### **Opção 1: Usar requirements_colab.txt (Recomendado)**

Cada projeto agora tem um arquivo `requirements_colab.txt` otimizado para o Google Colab:

```python
# No Google Colab, execute:
!pip install -r requirements_colab.txt
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
- `requirements_colab.txt` - Para Google Colab (com correção do tqdm)

### **0002_embeddings_vetorizacao/**

- `requirements.txt` - Para instalação local
- `requirements_colab.txt` - Para Google Colab (com correção do tqdm)

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
   !pip install -r requirements_colab.txt
   ```

## 🔍 Verificação

Para verificar se a instalação foi bem-sucedida:

```python
import tqdm
print(f"✅ tqdm versão: {tqdm.__version__}")
print("✅ Todas as dependências instaladas com sucesso!")
```

## 📚 Documentação Completa

Para mais detalhes e outras soluções, consulte:

- **[SOLUCAO_ERRO_COLAB.md](./SOLUCAO_ERRO_COLAB.md)**

---

**💡 Dica:** Sempre execute a correção do `tqdm` **ANTES** de instalar outras dependências para evitar conflitos!
