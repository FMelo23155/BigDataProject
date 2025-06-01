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
- 🔄 Develop loader scripts for easy access (Python) - **[TO BE COMPLETED]**
- 🔄 Demonstrate data exploration and visualization - **[TO BE COMPLETED]**
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
│       ├── bimodal/               # Bimodal splits
│       └── lyrics/                # Lyrics-specific splits
├── scripts/                        # ETL, processing, and utility scripts
│   ├── [merge_*_arousal_valence.py] # Arousal/Valence merging scripts
│   ├── [transform_to_tvt_*.py]     # Split transformation scripts  
│   ├── [consolidate_*.py]          # Data consolidation scripts
│   ├── [validate_*.py]             # Data validation scripts
│   ├── [verify_*.py]               # Split verification scripts
│   └── loader.py                   # Main dataset loader **[TO BE COMPLETED]**
├── notebooks/                      # Jupyter notebooks for analysis
│   └── relatorio.ipynb            # Main project report **[TO BE COMPLETED]**
├── README.md                       # This file
└── p1.txt                         # Project assignment specifications
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

### 5. Comprehensive Validation System ✅

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

### Basic Usage

**Using the Unified Dataset (Recommended):**

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

**[TO BE COMPLETED - Requires implementation of loader.py]**

```python
from scripts.loader import load_merge_dataset

# Load balanced audio training set with 70-15-15 split
df = load_merge_dataset(
    version='v1.1',          # Dataset version
    split='train',           # train/validate/test
    strategy='70_15_15',     # Split strategy  
    balanced=True,           # Balanced vs complete
    mode='audio',            # audio/lyrics/bimodal
    return_format='pandas'   # Return format
)

print(df.head())
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

## 🔍 Data Exploration & Analysis

**[TO BE COMPLETED - Planned implementations]**

- 📊 Label distribution analysis
- 📈 Modality coverage statistics  
- 🎵 Audio feature exploration
- 📝 Lyrics sentiment analysis
- 🔄 Cross-modal correlation analysis

## 📈 Validation Results

The implemented scripts provide comprehensive validation:

- ✅ **Metadata Integrity:** All Song_id references validated
- ✅ **Split Consistency:** No overlapping songs between train/validate/test
- ✅ **Arousal/Valence Coverage:** Tracking of missing values per modality
- ✅ **File Existence:** Verification of audio/lyrics file availability
- ✅ **Unified Dataset Integrity:** Complete validation via `validar_resultados.py`
- ✅ **Target Count Verification:** All balanced/complete targets achieved
- ✅ **Cross-Modal Consistency:** Bimodal entries properly linked across modalities

## 🐛 Known Issues & Limitations

### Identified Issues
1. **Poor Documentation:** Original dataset lacks clear usage instructions
2. **Inconsistent Naming:** Multiple variations of Song identifiers  
3. **Fragmented Subsets:** Data scattered across multiple files
4. **Manual Preprocessing:** Significant cleaning required before analysis
5. **Too Many Variants:** Multiple split strategies distributed separately
6. **Versioning Issues:** No clear mechanism to track changes

### Current Limitations
- ⚠️ **Loader API:** Main loader script needs implementation
- ⚠️ **Visualization:** Data exploration notebooks incomplete
- ⚠️ **Documentation:** Data dictionary needs completion
- ⚠️ **Testing:** Automated testing suite missing

## 🔮 Future Improvements

### Planned Enhancements
- [ ] **Complete Loader API:** Implement `loader.py` with version-aware loading
- [ ] **Data Visualization:** Interactive dashboard with Plotly
- [ ] **Schema Documentation:** Complete data dictionary with field descriptions
- [ ] **Version Management:** Implement version-specific patch files
- [ ] **PyTorch Integration:** Add PyTorch Dataset loaders
- [ ] **Automated Testing:** Unit tests for all ETL scripts
- [ ] **Documentation:** Complete user guide and API documentation

### Integration Possibilities
- [ ] **Hugging Face Datasets:** Package for easy distribution
- [ ] **mirdata:** Integration with music information retrieval framework
- [ ] **Python Package:** Distribute as installable library

## 📝 Technical Implementation Notes

### Script Dependencies
```python
import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
```

### File Path Conventions
- All scripts use relative paths from project root
- `Path(__file__).parent.parent` pattern for cross-platform compatibility
- Consistent directory structure maintained across scripts

### Error Handling
- Comprehensive file existence checking
- Clear error messages with suggested solutions
- Graceful handling of missing data

## 📊 Project Statistics

### Files Processed
- **Audio Files:** 200+ MP3 files
- **Metadata Files:** 15+ CSV files across modalities
- **Split Files:** 18+ consolidated split configurations
- **Scripts:** 15+ ETL and validation scripts

### Data Quality Metrics
- **Song ID Consistency:** 100% standardized to `Song_id`
- **Split Coverage:** All songs tracked across split strategies
- **Arousal/Valence Integration:** **[PERCENTAGE TO BE CALCULATED]**%
- **File Integrity:** **[TO BE VALIDATED]**% of referenced files exist

## 🎓 Academic Context

This project demonstrates key concepts in:
- **Data Engineering:** ETL pipeline design and implementation
- **Data Quality:** Validation, verification, and integrity checking
- **Schema Design:** Unified data structure development
- **Reproducibility:** Version-aware data management
- **Documentation:** Comprehensive project documentation

