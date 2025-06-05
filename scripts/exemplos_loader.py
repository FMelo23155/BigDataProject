#!/usr/bin/env python3
"""
Exemplos práticos de utilização do DatasetLoader
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from loader import DatasetLoader, load_dataset, load_splits
import pandas as pd

def exemplo_basico():
    """Exemplo 1: Uso básico do loader"""
    print("=" * 60)
    print("EXEMPLO 1: USO BÁSICO")
    print("=" * 60)
    
    # Carregar dataset padrão (merge_unified)
    print("🔄 Carregando dataset padrão...")
    data = load_dataset()  # Carrega merge_unified por padrão
    print(f"📊 Dataset padrão: {data.shape}")
    print(f"🎯 Quadrantes: {data['Quadrant'].value_counts().to_dict()}")
    
    # Carregar dataset específico
    print("\n🔄 Carregando audio balanceado...")  
    audio_balanced = load_dataset("audio", balanced_only=True)
    print(f"📊 Audio balanceado: {audio_balanced.shape}")
    
    return data, audio_balanced

def exemplo_splits_treinamento():
    """Exemplo 2: Preparação de dados para treinamento"""
    print("\n" + "=" * 60)
    print("EXEMPLO 2: PREPARAÇÃO PARA TREINAMENTO")
    print("=" * 60)
    
    loader = DatasetLoader()
    
    # Carregar dados de treino, validação e teste para audio
    print("🔄 Carregando splits de audio (40-30-30, balanceado)...")
    audio_splits = loader.load_split_dataset(
        modality="audio",
        split_ratio="40_30_30",
        split_type="all",  # train, validate, test
        balanced_type="balanced"
    )
    
    if "audio" in audio_splits:
        print("📊 Splits de Audio:")
        for split_name, split_data in audio_splits["audio"].items():
            print(f"   {split_name}: {split_data.shape}")
            
        # Exemplo de uso para ML
        train_data = audio_splits["audio"]["train"]
        val_data = audio_splits["audio"]["validate"] 
        test_data = audio_splits["audio"]["test"]
        
        # Extrair features e targets
        X_train = train_data[["Arousal", "Valence"]]
        y_train = train_data["Quadrant"]
        
        print(f"🎯 Features de treino: {X_train.shape}")
        print(f"🎯 Labels de treino: {y_train.shape}")
        print(f"🎯 Distribuição de classes: {y_train.value_counts().to_dict()}")
    
    return audio_splits

def exemplo_multimodal():
    """Exemplo 3: Análise multimodal"""
    print("\n" + "=" * 60)
    print("EXEMPLO 3: ANÁLISE MULTIMODAL")
    print("=" * 60)
    
    # Carregar dados de treino para todas as modalidades
    print("🔄 Carregando treino para todas as modalidades...")
    train_splits = load_splits(
        modality="all",
        split_ratio="70_15_15",
        split_type="train",
        balanced_type="balanced"
    )
    
    print("📊 Comparação entre modalidades (treino):")
    modalidades_stats = {}
    
    for modality, data in train_splits.items():
        if "train" in data:
            train_df = data["train"]
            modalidades_stats[modality] = {
                "total_samples": len(train_df),
                "quadrants": train_df["Quadrant"].value_counts().to_dict(),
                "arousal_mean": train_df["Arousal"].mean(),
                "valence_mean": train_df["Valence"].mean()
            }
            
            print(f"\n🎵 {modality.upper()}:")
            print(f"   Amostras: {modalidades_stats[modality]['total_samples']}")
            print(f"   Arousal médio: {modalidades_stats[modality]['arousal_mean']:.3f}")
            print(f"   Valence médio: {modalidades_stats[modality]['valence_mean']:.3f}")
            print(f"   Quadrantes: {modalidades_stats[modality]['quadrants']}")
    
    return modalidades_stats

def exemplo_analise_exploratoria():
    """Exemplo 4: Análise exploratória"""
    print("\n" + "=" * 60)
    print("EXEMPLO 4: ANÁLISE EXPLORATÓRIA")
    print("=" * 60)
    
    loader = DatasetLoader()
    
    # Obter informações detalhadas
    print("🔄 Analisando dataset unificado...")
    info = loader.get_dataset_info("unified")
    
    print(f"📊 Informações do Dataset Unificado:")
    print(f"   Shape: {info['shape']}")
    print(f"   Colunas: {len(info['columns'])}")
    print(f"   Quadrantes: {info['quadrants']}")
    
    # Analisar valores faltantes
    missing_cols = {k: v for k, v in info['missing_values'].items() if v > 0}
    if missing_cols:
        print(f"   ⚠️  Valores faltantes: {missing_cols}")
    else:
        print(f"   ✅ Sem valores faltantes!")
    
    # Analisar colunas balanceadas
    if "balanced_columns" in info:
        print(f"   🎯 Colunas balanceadas:")
        for col, counts in info["balanced_columns"].items():
            print(f"      {col}: {counts}")
    
    # Analisar splits
    print(f"\n🔄 Analisando splits de audio...")
    split_info = loader.get_split_info("audio", "40_30_30")
    print(f"📊 Informações do Split Audio (40-30-30):")
    print(f"   Shape: {split_info['shape']}")
    print(f"   Train (balanced): {split_info.get('in_balanced_train', 'N/A')}")
    print(f"   Validate (balanced): {split_info.get('in_balanced_validate', 'N/A')}")
    print(f"   Test (balanced): {split_info.get('in_balanced_test', 'N/A')}")
    
    return info, split_info

def exemplo_casos_especificos():
    """Exemplo 5: Casos de uso específicos"""
    print("\n" + "=" * 60)
    print("EXEMPLO 5: CASOS DE USO ESPECÍFICOS")
    print("=" * 60)
    
    loader = DatasetLoader()
    
    # Caso 1: Apenas dados bimodais completos para teste
    print("🔄 Caso 1: Dados bimodais completos para teste...")
    bimodal_test = loader.load_split_dataset(
        modality="bimodal",
        split_type="test",
        balanced_type="complete"
    )
    
    if "bimodal" in bimodal_test and "test" in bimodal_test["bimodal"]:
        test_data = bimodal_test["bimodal"]["test"]
        print(f"   ✅ Bimodal test completo: {test_data.shape}")
        
        # Analisar músicas por década
        if "ActualYear" in test_data.columns:
            test_data_clean = test_data.dropna(subset=["ActualYear"])
            decades = (test_data_clean["ActualYear"] // 10) * 10
            decade_counts = decades.value_counts().sort_index()
            print(f"   📅 Distribuição por década: {decade_counts.to_dict()}")
    
    # Caso 2: Comparar proporções 40-30-30 vs 70-15-15
    print(f"\n🔄 Caso 2: Comparando proporções de split...")
    
    for ratio in ["40_30_30", "70_15_15"]:
        lyrics_splits = loader.load_split_dataset(
            modality="lyrics",
            split_ratio=ratio,
            split_type="all",
            balanced_type="balanced"
        )
        
        if "lyrics" in lyrics_splits:
            sizes = {k: v.shape[0] for k, v in lyrics_splits["lyrics"].items()}
            total = sum(sizes.values())
            percentages = {k: round(v/total*100, 1) for k, v in sizes.items()}
            print(f"   📊 Lyrics {ratio}: {percentages}")

def main():
    """Executar todos os exemplos"""
    print("🎵 EXEMPLOS PRÁTICOS DO DATASETLOADER")
    print("🎵" * 30)
    
    try:
        # Executar todos os exemplos
        data, audio_balanced = exemplo_basico()
        audio_splits = exemplo_splits_treinamento()
        modalidades_stats = exemplo_multimodal()
        info, split_info = exemplo_analise_exploratoria()
        exemplo_casos_especificos()
        
        print("\n" + "🎉" * 30)
        print("TODOS OS EXEMPLOS EXECUTADOS COM SUCESSO!")
        print("🎉" * 30)
        
        # Resumo final
        print(f"\n📋 RESUMO:")
        print(f"   • Dataset padrão: {data.shape}")
        print(f"   • Audio balanceado: {audio_balanced.shape}")
        print(f"   • Modalidades analisadas: {len(modalidades_stats)}")
        print(f"   • Total de colunas no unified: {len(info['columns'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante execução: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
