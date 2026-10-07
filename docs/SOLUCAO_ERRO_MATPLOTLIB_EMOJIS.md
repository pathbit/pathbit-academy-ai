# 🔧 Solução: Erros de Fonte do Matplotlib com Emojis

## 🎯 Problema

Ao usar matplotlib com emojis nos títulos ou textos dos gráficos, você pode encontrar warnings como:

```
UserWarning: Glyph 128202 (\N{BAR CHART}) missing from font(s) DejaVu Sans.
UserWarning: Glyph 128196 (\N{PAGE FACING UP}) missing from font(s) DejaVu Sans.
UserWarning: Glyph 127919 (\N{DIRECT HIT}) missing from font(s) DejaVu Sans.
```

## 🔍 Causa

O matplotlib usa a fonte DejaVu Sans por padrão, que não suporta todos os caracteres Unicode/emojis. Quando tenta renderizar emojis, gera warnings sobre glifos ausentes.

## ✅ Soluções

### **Solução 1: Remover Emojis dos Gráficos (Recomendado)**

Substitua emojis por texto simples nos títulos e labels dos gráficos:

```python
# ❌ Problema - com emojis
plt.title('📊 Distribuição do Tamanho dos Chunks')
plt.xlabel('📄 Documentos')

# ✅ Solução - sem emojis
plt.title('Distribuicao do Tamanho dos Chunks')
plt.xlabel('Documentos')
```

### **Solução 2: Configurar Fonte Compatível**

Configure uma fonte que suporte emojis:

```python
import matplotlib.pyplot as plt
import matplotlib

# Configurar fonte que suporte emojis (se disponível)
plt.rcParams['font.family'] = ['Apple Color Emoji', 'Segoe UI Emoji', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False
```

### **Solução 3: Suprimir Warnings**

Se quiser manter os emojis, suprima os warnings:

```python
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*Glyph.*missing from font.*")
```

## 🎨 Exemplo Prático

### Antes (com problemas):

```python
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

axes[0, 0].set_title('📊 Distribuição do Tamanho dos Chunks')
axes[0, 1].set_title('📄 Chunks por Documento')
axes[1, 0].set_title('🎯 Similaridade das Consultas')
axes[1, 1].set_title('📈 Resumo do Sistema')
```

### Depois (corrigido):

```python
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

axes[0, 0].set_title('Distribuicao do Tamanho dos Chunks')
axes[0, 1].set_title('Chunks por Documento')
axes[1, 0].set_title('Similaridade das Consultas')
axes[1, 1].set_title('Resumo do Sistema')
```

## 📋 Checklist de Correção

- [ ] Remover emojis dos títulos dos gráficos
- [ ] Remover emojis dos labels dos eixos
- [ ] Remover emojis dos textos dentro dos gráficos
- [ ] Configurar fonte apropriada se necessário
- [ ] Testar visualização sem warnings

## 💡 Dicas

1. **Mantenha emojis no console/prints** - eles funcionam bem no terminal
2. **Use texto simples nos gráficos** - mais compatível e profissional
3. **Configure fonte uma vez** - no início do notebook
4. **Teste em diferentes ambientes** - Colab, local, diferentes SOs

## 🔗 Referências

- [Documentação do Matplotlib - Fonts](https://matplotlib.org/stable/tutorials/text/text_props.html)
- [Unicode Support in Matplotlib](https://matplotlib.org/stable/users/explain/text/text_props.html)

---

**Última atualização:** 02/10/2025
**Versão:** 1.0.0
