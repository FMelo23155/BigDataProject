# DatasetLoader - Guia de Utilização

O `DatasetLoader` é uma classe completa para carregar e filtrar os datasets de música do projeto BigData. Suporta carregamento de datasets base e splits com múltiplos parâmetros de filtragem.

## Estrutura de Dados Suportada

### Datasets Base (`/metadata/base/`)
- `merge_audio.csv` - Dados apenas de áudio
- `merge_bimodal.csv` - Dados bimodais (áudio + lyrics)
- `merge_lyrics.csv` - Dados apenas de letras
- `merge_unified.csv` - Dataset unificado (padrão)

### Splits TVT (`/metadata/splits/`)
- `audio/tvt_40_30_30.csv` e `audio/tvt_70_15_15.csv`
- `bimodal/tvt_40_30_30.csv` e `bimodal/tvt_70_15_15.csv`
- `lyrics/tvt_40_30_30.csv` e `lyrics/tvt_70_15_15.csv`

## Utilização Básica

### 1. Inicialização

```python
from scripts.loader import DatasetLoader

# Usar caminho padrão
loader = DatasetLoader()

# Ou especificar caminho personalizado
loader = DatasetLoader(base_path="/caminho/para/metadata")
```

### 2. Carregar Dataset Padrão (merge_unified)

```python
# Carrega merge_unified completo
data = loader.load_default()

# Ou usando a função de conveniência
from scripts.loader import load_dataset
data = load_dataset()  # carrega unified por padrão
```

### 3. Carregar Datasets Base Específicos

```python
# Carregar dataset de áudio (todos os dados)
audio_data = loader.load_base_dataset("audio", balanced_only=False)

# Carregar dataset bimodal (apenas balanceados)
bimodal_balanced = loader.load_base_dataset("bimodal", balanced_only=True)

# Carregar dataset de lyrics (apenas balanceados)
lyrics_balanced = loader.load_base_dataset("lyrics", balanced_only=True)

# Carregar dataset unificado (todos os dados)
unified_data = loader.load_base_dataset("unified", balanced_only=False)
```

### 4. Carregar Splits TVT

#### Carregar um split específico
```python
# Carregar dados de treino de áudio (balanceados, 40_30_30)
train_data = loader.load_split_dataset(
    modality="audio",
    split_ratio="40_30_30",
    split_type="train", 
    balanced_type="balanced"
)
# Resultado: {"audio": {"train": DataFrame}}
```

#### Carregar múltiplos splits
```python
# Carregar treino e validação para todas as modalidades
train_val_data = loader.load_split_dataset(
    modality="all",  # audio, bimodal, lyrics
    split_ratio="40_30_30",
    split_type=["train", "validate"],
    balanced_type="balanced"
)
# Resultado: {"audio": {"train": DF, "validate": DF}, "bimodal": {...}, "lyrics": {...}}
```

#### Carregar todos os splits
```python
# Carregar todos os splits para bimodal (70_15_15, completos)
all_bimodal = loader.load_split_dataset(
    modality="bimodal",
    split_ratio="70_15_15", 
    split_type="all",  # train, validate, test
    balanced_type="complete"
)
# Resultado: {"bimodal": {"train": DF, "validate": DF, "test": DF}}
```

### 5. Funções de Conveniência

```python
from scripts.loader import load_dataset, load_splits

# Carregar dataset base rapidamente
audio_data = load_dataset("audio", balanced_only=True)

# Carregar splits rapidamente
splits = load_splits(
    modality="all",
    split_ratio="40_30_30",
    split_type="train",
    balanced_type="balanced"
)
```

## Parâmetros Disponíveis

### Datasets Base

| Parâmetro | Valores | Descrição |
|-----------|---------|-----------|
| `dataset_type` | `"audio"`, `"bimodal"`, `"lyrics"`, `"unified"` | Tipo de dataset |
| `balanced_only` | `True`, `False` | Filtrar apenas dados balanceados |

### Splits TVT

| Parâmetro | Valores | Descrição |
|-----------|---------|-----------|
| `modality` | `"audio"`, `"bimodal"`, `"lyrics"`, `"all"`, `["audio", "bimodal"]` | Modalidade(s) |
| `split_ratio` | `"40_30_30"`, `"70_15_15"` | Proporção do split |
| `split_type` | `"train"`, `"validate"`, `"test"`, `"all"`, `["train", "test"]` | Tipo(s) de split |
| `balanced_type` | `"balanced"`, `"complete"` | Tipo de balanceamento |

## Informações sobre Datasets

### Obter informações de um dataset base
```python
info = loader.get_dataset_info("unified")
print(f"Shape: {info['shape']}")
print(f"Quadrantes: {info['quadrants']}")
print(f"Colunas balanceadas: {info['balanced_columns']}")
```

### Obter informações de splits
```python
split_info = loader.get_split_info("audio", "40_30_30")
print(f"Amostras de treino: {split_info['in_balanced_train']}")
print(f"Amostras de validação: {split_info['in_balanced_validate']}")
print(f"Amostras de teste: {split_info['in_balanced_test']}")
```

## Exemplos Práticos

### Exemplo 1: Análise básica
```python
# Carregar dataset padrão
data = loader.load_default()
print(f"Total de músicas: {len(data)}")
print(f"Distribuição por quadrantes: {data['Quadrant'].value_counts()}")
```

### Exemplo 2: Treinar modelo com splits
```python
# Carregar dados de treino e teste
splits = loader.load_split_dataset(
    modality="audio",
    split_ratio="70_15_15",
    split_type=["train", "test"],
    balanced_type="balanced"
)

train_data = splits["audio"]["train"]
test_data = splits["audio"]["test"]

print(f"Treino: {train_data.shape}, Teste: {test_data.shape}")
```

### Exemplo 3: Comparar modalidades
```python
# Carregar treino para todas as modalidades
train_splits = loader.load_split_dataset(
    modality="all",
    split_type="train",
    balanced_type="balanced"
)

for modality, data in train_splits.items():
    train_df = data["train"]
    print(f"{modality}: {train_df.shape}")
```

## Tratamento de Erros

O loader inclui validação de parâmetros e tratamento de erros:

- Valida se os tipos de dataset/modalidade são válidos
- Verifica se os arquivos existem antes de carregá-los
- Apresenta avisos quando filtros não retornam dados
- Propaga erros informativos quando há problemas de carregamento

## Performance e Cache

Para melhor performance em projetos que carregam os mesmos dados repetidamente, considere:

```python
# Carregar uma vez e reutilizar
loader = DatasetLoader()
unified_data = loader.load_default()

# Usar o DataFrame carregado múltiplas vezes
analysis1 = unified_data[unified_data['Quadrant'] == 'Q1']
analysis2 = unified_data[unified_data['Quadrant'] == 'Q2']
```
