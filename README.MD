# MERGE Dataset: ETL, Exploration & Redesign
**Big Data Processing in Python - Project 1**

> **Student ID:** 23155  
> **Course:** Big Data Processing in Python  
> **Professor:** Renato Panda  
> **Date:** June 2025


## 📋 Project Overview

This project focuses on the **MERGE Dataset**, a public multimodal dataset for Music Emotion Recognition (MER) containing audio, lyrics, and emotion labels. The original dataset presents challenges for usability, reproducibility, and integration with modern data science tools.

**Goal:** Critically analyze, refactor, and enhance the dataset's structure and usability—mirroring a real-world data engineering task.

## 🎯 Objectives

- ✅ Explore and understand the current MERGE dataset structure and content
- ✅ Identify and document issues in organization, naming, splits, and usability  
- ✅ Implement improvements for unified schema and naming conventions
- ✅ Develop centralized metadata and split management
- ✅ Create ETL scripts for downloading, validating, and loading the dataset
- ✅ Develop loader scripts for easy access (Python)
- ✅ Demonstrate data exploration and visualization 
- 📝 Document process and rationale for each design decision

## 📊 Dataset at a Glance

The MERGE dataset consists of several modality-specific and bimodal subsets:

| Subset | Complete | Balanced |
|--------|----------|----------|
| Audio | 3554 | 3232 |
| Lyrics | 2568 | 2400 |
| Bimodal (Audio+Lyrics) | 2216 | 2000 |

- **Files:** Each subset distributed as ZIP file from [Zenodo](https://zenodo.org/records/13939205)
- **Splits:** Both 70-15-15 and 40-30-30 train/val/test splits provided
- **Metadata:** Includes Song, Quadrant, Artist, Title, Genres, Moods, Themes, ActualYear, and more

## 🏗️ Project Structure

```
ProjetoBigData23155/
├── data/                           # Raw audio and lyrics files
│   ├── audio/                      # Audio files (.mp3)
│   └── lyrics/                     # Lyrics files
├── metadata/                       # All metadata and split information
│   ├── base/                       # Consolidated base metadata files
│   ├── last/                       # Original dataset files from MERGE
│   └── splits/                     # Processed split files
│       ├── audio/                  # Audio-specific splits
│       ├── bimodal/                # Bimodal splits
│       └── lyrics/                 # Lyrics-specific splits
├── scripts/                        # ETL, processing, and utility scripts
│   ├── [merge_*_arousal_valence.py]# Arousal/Valence merging scripts
│   ├── [transform_to_tvt_*.py]     # Split transformation scripts  
│   ├── [consolidate_*.py]          # Data consolidation scripts
│   ├── [validate_*.py]             # Data validation scripts
│   ├── [verify_*.py]               # Split verification scripts
│   ├── loader.py                   # Main dataset loader 
│   └── test_loader.py              # Loader test suite 
├── notebooks/                      # Jupyter notebooks for analysis
│   ├── dashboard.py                # Dataset exploration and analysis using Streamlit
├── LOADER_GUIDE.md                 # Detailed loader documentation                   # 
└── README.md                       # This file
```

## 🔧 Implemented Solutions

### 1. Schema Redesign & Standardization ✅

**Issues Identified:**
- Inconsistent naming (Song, SongID, Song_id)
- Fragmented subsets across multiple files
- Poor documentation and usability

**Solutions Implemented:**
- Unified column naming (`Song_id` standardization)
- Centralized metadata consolidation
- Consistent split file structures
- **NEW:** Unified dataset combining all modalities

### 2. Dataset Unification ✅

**New Feature: Single Unified Dataset**
- `unify_datasets.py` - Combines audio, lyrics, and bimodal into one dataset
- `merge_unified.csv` - Single CSV with all 8,338 records
- Preserves all original data with clear modality indicators
- Uses `Merge_id` as unique identifier across all entries
- Flags: `is_bimodal`, `has_audio`, `has_lyrics` for easy filtering

**Unified Dataset Structure:**
- **Total Records:** 8,338 (Audio: 3,554 | Lyrics: 2,568 | Bimodal: 2,216)
- **Complete Coverage:** No data loss during unification
- **Balanced Subsets:** Audio: 3,232 | Lyrics: 2,400 | Bimodal: 2,000
- **Schema:** 36 columns with consistent naming across all modalities

**Key Features of `merge_unified.csv`:**
- **Merge_id:** Unique identifier for each entry across all modalities
- **Modality Flags:** `bimodal` boolean flag to distinguish entry types
- **Balanced Tracking:** `in_audio_balanced`, `in_lyrics_balanced`, `in_bimodal_balanced` columns
- **Complete Integration:** All original data preserved with no information loss
- **Easy Filtering:** Simple queries to extract specific modality subsets

### 3. ETL Scripts ✅

#### Arousal/Valence Integration
- `merge_arousal_valence.py` - Audio metadata enhancement
- `merge_bimodal_arousal_valence.py` - Bimodal metadata enhancement  
- `merge_lyrics_arousal_valence.py` - Lyrics metadata enhancement

#### Split Management
- `transform_to_tvt_70_15_15_audio.py` - 70-15-15 splits for audio
- `transform_to_tvt_70_15_15_bimodal.py` - 70-15-15 splits for bimodal
- `transform_to_tvt_70_15_15_lyrics.py` - 70-15-15 splits for lyrics
- `transform_to_tvt_40_30_30_*.py` - 40-30-30 split variants

#### Data Consolidation
- `consolidate_audio_splits.py` - Unified audio split management
- `consolidate_tvt_audio_splits.py` - TVT-specific consolidation

#### Validation & Verification
- `validate_*_balanced.py` - Balanced dataset validation
- `verify_audio_splits.py` - Split integrity verification
- `validar_resultados.py` - **Comprehensive dataset validation and results verification**

### 3. Consolidated Metadata Structure ✅

Each modality now has unified split files with structure:
```csv
Song_id,Quadrant,in_balanced_train,in_balanced_validate,in_balanced_test,in_complete_train,in_complete_validate,in_complete_test
```

This design allows:
- ✅ Easy filtering by split type (balanced vs complete)
- ✅ Easy filtering by split phase (train/validate/test)
- ✅ Clear tracking of song membership across different splits
- ✅ Unified schema across all modalities

### 4. Unified Dataset Implementation ✅

**File:** `metadata/base/merge_unified.csv`

The unified dataset represents a major improvement in data accessibility:

```csv
Merge_id,Song_id,Lyric_id,bimodal,Artist,Title,...,in_audio_balanced,in_lyrics_balanced,in_bimodal_balanced
A001_L001,A001,L001,True,Artist1,Song1,...,True,True,True
A002,A002,,False,Artist2,Song2,...,True,False,False
L002,,L002,False,Artist3,Song3,...,False,True,False
```

**Usage Examples:**
```python
import pandas as pd

# Load unified dataset
df = pd.read_csv('metadata/base/merge_unified.csv')

# Filter bimodal entries
bimodal_data = df[df['bimodal'] == True]

# Filter audio-only entries
audio_only = df[(df['bimodal'] == False) & (df['Song_id'].notna())]

# Filter lyrics-only entries  
lyrics_only = df[(df['bimodal'] == False) & (df['Song_id'].isna())]

# Get balanced audio subset
balanced_audio = df[df['in_audio_balanced'] == True]
```

### 6. DatasetLoader Implementation ✅

**Script:** `scripts/loader.py`

A comprehensive, production-ready loader for easy access to all dataset variants with filtering capabilities.

**Key Features:**
- **Default Loading:** Automatically loads `merge_unified.csv` when no parameters specified
- **Flexible Filtering:** Support for modality, balanced/complete, split types
- **Multiple Formats:** Base datasets and TVT splits with various proportions
- **Performance:** Efficient merging and filtering operations

**DatasetLoader Class:**
```python
from scripts.loader import DatasetLoader, load_dataset, load_splits

# Initialize loader
loader = DatasetLoader()

# Load default dataset (merge_unified.csv)
data = loader.load_default()  # 3,906 records

# Load specific base datasets
audio_balanced = loader.load_base_dataset("audio", balanced_only=True)
bimodal_all = loader.load_base_dataset("bimodal", balanced_only=False)  
lyrics_balanced = loader.load_base_dataset("lyrics", balanced_only=True)
unified_data = loader.load_base_dataset("unified", balanced_only=False)
```

**Split Loading Capabilities:**
```python
# Load specific splits
train_data = loader.load_split_dataset(
    modality="audio",           # "audio", "bimodal", "lyrics", "all"
    split_ratio="40_30_30",     # "40_30_30", "70_15_15"
    split_type="train",         # "train", "validate", "test", "all"
    balanced_type="balanced"    # "balanced", "complete"
)

# Load multiple splits at once
all_splits = loader.load_split_dataset(
    modality="all",             # All modalities
    split_type="all",           # All split types
    balanced_type="balanced"
)
```

**Convenience Functions:**
```python
# Quick access functions
audio_data = load_dataset("audio", balanced_only=True)
splits = load_splits(modality="bimodal", split_type=["train", "test"])
```

**Dataset Information & Analysis:**
```python
# Get dataset statistics
info = loader.get_dataset_info("unified")
print(f"Shape: {info['shape']}")
print(f"Quadrants: {info['quadrants']}")
print(f"Balanced columns: {info['balanced_columns']}")

# Get split statistics
split_info = loader.get_split_info("audio", "40_30_30")
print(f"Train samples: {split_info['in_balanced_train']}")
```

## 📚 DatasetLoader Complete Reference

### Supported Parameters

#### Base Dataset Loading
| Parameter | Options | Description |
|-----------|---------|-------------|
| `dataset_type` | `"audio"`, `"bimodal"`, `"lyrics"`, `"unified"` | Dataset modality |
| `balanced_only` | `True`, `False` | Filter only balanced data |

#### Split Dataset Loading  
| Parameter | Options | Description |
|-----------|---------|-------------|
| `modality` | `"audio"`, `"bimodal"`, `"lyrics"`, `"all"`, `["audio", "bimodal"]` | Modality selection |
| `split_ratio` | `"40_30_30"`, `"70_15_15"` | Train/Validate/Test proportions |
| `split_type` | `"train"`, `"validate"`, `"test"`, `"all"`, `["train", "test"]` | Split phase selection |
| `balanced_type` | `"balanced"`, `"complete"` | Dataset balancing type |

### Dataset Sizes & Distribution

**Base Datasets:**
- **Unified (all modalities):** 3,906 records
- **Audio (balanced):** 3,232 records
- **Audio (complete):** 3,554 records  
- **Bimodal (balanced):** 2,000 records
- **Bimodal (complete):** 2,216 records
- **Lyrics (balanced):** 2,400 records
- **Lyrics (complete):** 2,568 records

**Split Distribution (40-30-30, Balanced):**
| Modality | Train | Validate | Test | Total |
|----------|-------|----------|------|-------|
| Audio | 1,296 | 968 | 968 | 3,232 |
| Bimodal | 800 | 600 | 600 | 2,000 |
| Lyrics | 960 | 720 | 720 | 2,400 |

**Quadrant Distribution (Unified Dataset):**
- **Q1 (High Arousal, High Valence):** 950 songs (24.3%)
- **Q2 (High Arousal, Low Valence):** 952 songs (24.4%)  
- **Q3 (Low Arousal, Low Valence):** 929 songs (23.8%)
- **Q4 (Low Arousal, High Valence):** 1,075 songs (27.5%)

### Files Generated by Loader
- **Test Suite:** `scripts/test_loader.py` - Comprehensive test validation
- **Examples:** `exemplos_loader.py` - Practical usage examples
- **Documentation:** `LOADER_GUIDE.md` - Detailed usage guide
- **Status Report:** `LOADER_STATUS.md` - Implementation completion status

### 7. Comprehensive Validation System ✅

**Script:** `scripts/validar_resultados.py`

This validation script provides end-to-end verification of the dataset processing pipeline:

**Key Validation Features:**
- **Structure Validation:** Verifies required columns and data types
- **Count Validation:** Ensures target counts are met for all modalities
- **Consistency Validation:** Checks data integrity across the unified dataset
- **Target Verification:** Validates against expected balanced/complete counts

**Validation Results:**
```
=== VALIDATION RESULTS ===
✅ Dataset Structure: PASSED
✅ Target Counts: PASSED  
✅ Data Consistency: PASSED
✅ Balanced Subsets: PASSED

COMPLETE COUNTS:
Audio: 3,554 ✅
Lyrics: 2,568 ✅  
Bimodal: 2,216 ✅

BALANCED COUNTS:
Audio: 3,232 ✅
Lyrics: 2,400 ✅
Bimodal: 2,000 ✅
```

## 🚀 Quick Start

### Prerequisites
```bash
pip install pandas numpy
# Add other requirements as needed
```

### Using the DatasetLoader (Recommended)

**1. Basic Usage:**

```python
from scripts.loader import DatasetLoader, load_dataset, load_splits

# Initialize loader
loader = DatasetLoader()

# Load default dataset (merge_unified.csv) - 3,906 records
data = loader.load_default()
print(f"Total songs: {len(data)}")
print(f"Quadrants: {data['Quadrant'].value_counts().to_dict()}")

# Carregar datasets base com diferentes opções
audio_balanced = load_dataset("audio", balanced_only=True)      # 3,232 records
bimodal_complete = load_dataset("bimodal", balanced_only=False) # 2,216 records
lyrics_balanced = load_dataset("lyrics", balanced_only=True)    # 2,400 records
unified_data = load_dataset("unified", balanced_only=False)     # Dataset unificado completo
```

**2. Split Loading para Machine Learning:**

```python
# Carregamento de splits específicos
train_splits = loader.load_split_dataset(
    modality="audio",           # "audio", "bimodal", "lyrics", "all", ou lista ["audio", "bimodal"]
    split_ratio="70_15_15",     # "70_15_15" ou "40_30_30"
    split_type="all",           # "train", "validate", "test", "all", ou lista ["train", "test"] 
    balanced_type="balanced"    # "balanced" ou "complete"
)

# Preparação de dados para ML
X_train = train_splits["audio"]["train"][["Arousal", "Valence"]]
y_train = train_splits["audio"]["train"]["Quadrant"]
X_val = train_splits["audio"]["validate"][["Arousal", "Valence"]]
y_val = train_splits["audio"]["validate"]["Quadrant"]

print(f"Training samples: {len(X_train)}")
print(f"Validation samples: {len(X_val)}")

# Carregamento apenas de dados de treino para proporção 40-30-30
audio_train_40_30_30 = loader.load_split_dataset(
    modality="audio",
    split_ratio="40_30_30",
    split_type="train", 
    balanced_type="balanced"
)
```

**3. Análise Multimodal:**

```python
# Comparação de todas as modalidades
multimodal_data = loader.load_split_dataset(
    modality="all",             # Carrega dados de audio, bimodal, lyrics
    split_type="train",
    balanced_type="balanced"
)

for modality, data in multimodal_data.items():
    train_df = data["train"]
    print(f"{modality}: {train_df.shape[0]} samples")
    print(f"  Avg Arousal: {train_df['Arousal'].mean():.3f}")
    print(f"  Avg Valence: {train_df['Valence'].mean():.3f}")

# Carregar apenas dados de áudio e bimodal
audio_bimodal_splits = loader.load_split_dataset(
    modality=["audio", "bimodal"],  # Lista de modalidades específicas
    split_ratio="40_30_30",
    split_type=["validate", "test"], # Apenas splits de validação e teste
    balanced_type="balanced"
)
```

**4. Análise Rápida e Recuperação de Informações:**

```python
# Obter informações sobre datasets
info = loader.get_dataset_info("unified")
print(f"Dataset shape: {info['shape']}")
print(f"Missing values: {info['missing_values']}")
print(f"Balanced columns: {list(info['balanced_columns'].keys())}")
print(f"Quadrantes: {info['quadrants']}")

# Obter informações sobre splits
split_info = loader.get_split_info("audio", "40_30_30")
print(f"Split samples - Train: {split_info['in_balanced_train']}")
print(f"Split samples - Val: {split_info['in_balanced_validate']}")
print(f"Split samples - Test: {split_info['in_balanced_test']}")

# Verificação de distribuição de quadrantes
audio_data = load_dataset("audio")
quadrant_counts = audio_data["Quadrant"].value_counts()
print(f"Distribuição de quadrantes:\n{quadrant_counts}")
```

### Manual Dataset Access (Alternative)

**Using the Unified Dataset:**

```python
import pandas as pd

# Load the unified dataset
df = pd.read_csv('metadata/base/merge_unified.csv')

# Get all audio data (bimodal + audio-only)
audio_data = df[df['Song_id'].notna()]
print(f"Total audio entries: {len(audio_data)}")

# Get balanced bimodal training data
balanced_bimodal = df[
    (df['bimodal'] == True) & 
    (df['in_bimodal_balanced'] == True)
]

# Quick dataset overview
print(f"Total entries: {len(df)}")
print(f"Bimodal: {df['bimodal'].sum()}")
print(f"Audio-only: {((~df['bimodal']) & (df['Song_id'].notna())).sum()}")
print(f"Lyrics-only: {((~df['bimodal']) & (df['Song_id'].isna())).sum()}")
```

### Manual Script Execution

```bash
# Create unified dataset from all modalities
python scripts/unify_datasets.py

# Merge arousal/valence values
python scripts/merge_arousal_valence.py

# Transform to consolidated splits
python scripts/transform_to_tvt_70_15_15_audio.py

# Verify split integrity
python scripts/verify_audio_splits.py

# Comprehensive validation of final results
python scripts/validar_resultados.py
```



## 📈 Validation Results

The implemented scripts provide comprehensive validation:

- ✅ **Metadata Integrity:** All Song_id references validated
- ✅ **Split Consistency:** No overlapping songs between train/validate/test
- ✅ **Arousal/Valence Coverage:** Tracking of missing values per modality
- ✅ **File Existence:** Verification of audio/lyrics file availability
- ✅ **Unified Dataset Integrity:** Complete validation via `validar_resultados.py`
- ✅ **Target Count Verification:** All balanced/complete targets achieved
- ✅ **Cross-Modal Consistency:** Bimodal entries properly linked across modalities


## 🎓 Academic Context

This project demonstrates key concepts in:
- **Data Engineering:** ETL pipeline design and implementation
- **Data Quality:** Validation, verification, and integrity checking
- **Schema Design:** Unified data structure development
- **Documentation:** Comprehensive project documentation