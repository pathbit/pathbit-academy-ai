# 🔧 Solução: Erros de Telemetria do ChromaDB

> Nota de versão: patches em APIs privadas abaixo são históricos e podem não
> existir em Chroma atual. Prefira `Settings(anonymized_telemetry=False)` e
> teste a versão instalada; não faça downgrade automático para 0.5.23.

## 🎯 Problema

Ao usar o ChromaDB, você pode encontrar os seguintes erros:

```
Failed to send telemetry event ClientStartEvent: capture() takes 1 positional argument but 3 were given
Failed to send telemetry event ClientCreateCollectionEvent: capture() takes 1 positional argument but 3 were given
Failed to send telemetry event CollectionAddEvent: capture() takes 1 positional argument but 3 were given
Failed to send telemetry event CollectionQueryEvent: capture() takes 1 positional argument but 3 were given
```

## 🔍 Causa

Esses erros são causados por uma incompatibilidade na biblioteca de telemetria do ChromaDB em versões antigas (< 0.5.0). Embora não impeçam o funcionamento, eles poluem a saída e podem confundir usuários.

## ✅ Solução

### 1. Atualizar o ChromaDB

Atualize para a versão `0.5.23` ou superior:

```bash
python -m pip install --upgrade chromadb
```

Ou atualize seu `requirements.txt`:

```txt
chromadb==0.5.23
```

### 2. Configurar corretamente o ambiente

Antes de criar o cliente ChromaDB, configure as variáveis de ambiente e logging:

```python
import os
import warnings
import logging

# Desabilitar telemetria do ChromaDB completamente
os.environ['CHROMA_TELEMETRY'] = 'false'
os.environ['CHROMA_DISABLE_TELEMETRY'] = '1'
os.environ['ANONYMIZED_TELEMETRY'] = 'False'

# Suprimir todos os warnings e erros relacionados à telemetria
warnings.filterwarnings("ignore", message=".*telemetry.*")
warnings.filterwarnings("ignore", message=".*Failed to send telemetry.*")
warnings.filterwarnings("ignore", message=".*capture.*")

# Desabilitar logs do ChromaDB relacionados à telemetria
logging.getLogger('chromadb.telemetry').setLevel(logging.CRITICAL)
logging.getLogger('chromadb').setLevel(logging.WARNING)
```

### 3. Criar o cliente com configurações corretas

```python
import chromadb
from chromadb.config import Settings

client = chromadb.Client(
    settings=Settings(
        allow_reset=True,
        anonymized_telemetry=False,
        is_persistent=False
    )
)
```

## 📋 Ordem de Execução no Notebook

Se estiver usando Jupyter Notebook:

1. ✅ Execute as células de importação
2. ✅ Execute a célula de configuração de telemetria (célula 8)
3. ✅ Execute a célula de criação do cliente ChromaDB (célula 14)

## 🧪 Teste

Para verificar se a solução funcionou, execute:

```python
# Criar coleção de teste
collection = client.create_collection(name="test")

# Se não houver mensagens de erro de telemetria, está funcionando!
print("✅ ChromaDB configurado corretamente!")
```

## 💡 Notas

- Esses erros **NÃO impedem** o funcionamento do ChromaDB
- São apenas mensagens de log do sistema de telemetria
- A solução completa elimina todas as mensagens
- Versões do ChromaDB >= 0.5.0 têm melhor suporte para desabilitar telemetria

## 🔗 Referências

- [Documentação do ChromaDB](https://docs.trychroma.com/)
- [Configurações do ChromaDB](https://docs.trychroma.com/)
- [GitHub do ChromaDB](https://github.com/chroma-core/chroma)

---

**Última atualização:** 02/10/2025
**Versão do ChromaDB testada:** 0.5.23
