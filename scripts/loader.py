import pandas as pd
import os
from typing import Optional, Union, List, Dict
from pathlib import Path


class DatasetLoader:
    """
    Loader completo para datasets de música com funcionalidades de filtragem e seleção de parâmetros.
    
    Suporta carregar:
    - Datasets base: merge_audio, merge_bimodal, merge_lyrics, merge_unified
    - Splits TVT: 40_30_30 e 70_15_15 para audio, bimodal e lyrics
    - Filtragem por balanced/complete e train/validate/test
    """
    
    def __init__(self, base_path: str = "/workspace/BigDataProject/metadata"):
        """
        Inicializa o loader com o caminho base dos metadados.
        
        Args:
            base_path: Caminho base para a pasta metadata
        """
        self.base_path = Path(base_path)
        self.base_dir = self.base_path / "base"
        self.splits_dir = self.base_path / "splits"
        
        # Verificar se os diretórios existem
        if not self.base_dir.exists():
            raise FileNotFoundError(f"Diretório base não encontrado: {self.base_dir}")
        if not self.splits_dir.exists():
            raise FileNotFoundError(f"Diretório de splits não encontrado: {self.splits_dir}")
    
    def load_base_dataset(
        self, 
        dataset_type: str = "unified",
        balanced_only: bool = False
    ) -> pd.DataFrame:
        """
        Carrega um dataset base.
        
        Args:
            dataset_type: Tipo do dataset ("audio", "bimodal", "lyrics", "unified")
            balanced_only: Se True, filtra apenas dados balanceados
            
        Returns:
            DataFrame com os dados carregados
        """
        valid_types = ["audio", "bimodal", "lyrics", "unified"]
        if dataset_type not in valid_types:
            raise ValueError(f"dataset_type deve ser um de: {valid_types}")
        
        # Construir nome do arquivo
        filename = f"merge_{dataset_type}.csv"
        filepath = self.base_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
        
        # Carregar dados
        df = pd.read_csv(filepath)
        
        # Aplicar filtro de balanced se solicitado
        if balanced_only:
            if dataset_type == "unified":
                # Para unified, verificar se todas as modalidades são balanceadas
                if "in_bimodal_balanced" in df.columns:
                    df = df[df["in_bimodal_balanced"] == True]
                if "in_audio_balanced" in df.columns:
                    df = df[df["in_audio_balanced"] == True]
                if "in_lyrics_balanced" in df.columns:
                    df = df[df["in_lyrics_balanced"] == True]
            else:
                # Para outros tipos, usar a coluna específica
                balanced_col = f"in_{dataset_type}_balanced"
                if balanced_col in df.columns:
                    df = df[df[balanced_col] == True]
                else:
                    print(f"Aviso: Coluna {balanced_col} não encontrada. Retornando todos os dados.")
        
        return df
    
    def load_split_dataset(
        self,
        modality: Union[str, List[str]] = "all",
        split_ratio: str = "40_30_30",
        split_type: Union[str, List[str]] = "all",
        balanced_type: str = "balanced"
    ) -> Dict[str, Union[pd.DataFrame, Dict[str, pd.DataFrame]]]:
        """
        Carrega datasets de splits TVT.
        
        Args:
            modality: Modalidade(s) a carregar ("audio", "bimodal", "lyrics", "all")
            split_ratio: Proporção do split ("40_30_30", "70_15_15")
            split_type: Tipo(s) de split ("train", "validate", "test", "all")
            balanced_type: Tipo de balanceamento ("balanced", "complete")
            
        Returns:
            Dicionário com DataFrames organizados por modalidade e tipo de split
        """
        valid_modalities = ["audio", "bimodal", "lyrics"]
        valid_ratios = ["40_30_30", "70_15_15"]
        valid_splits = ["train", "validate", "test"]
        valid_balanced = ["balanced", "complete"]
        
        if split_ratio not in valid_ratios:
            raise ValueError(f"split_ratio deve ser um de: {valid_ratios}")
        
        if balanced_type not in valid_balanced:
            raise ValueError(f"balanced_type deve ser um de: {valid_balanced}")
        
        # Normalizar modalities para lista
        if modality == "all":
            modalities = valid_modalities
        elif isinstance(modality, str):
            if modality not in valid_modalities:
                raise ValueError(f"modality deve ser um de: {valid_modalities} ou 'all'")
            modalities = [modality]
        else:
            for mod in modality:
                if mod not in valid_modalities:
                    raise ValueError(f"modality deve conter apenas: {valid_modalities}")
            modalities = modality
        
        # Normalizar split_types para lista
        if split_type == "all":
            split_types = valid_splits
        elif isinstance(split_type, str):
            if split_type not in valid_splits:
                raise ValueError(f"split_type deve ser um de: {valid_splits} ou 'all'")
            split_types = [split_type]
        else:
            for split in split_type:
                if split not in valid_splits:
                    raise ValueError(f"split_type deve conter apenas: {valid_splits}")
            split_types = split_type
        
        results = {}
        
        for mod in modalities:
            # Carregar arquivo de split para esta modalidade
            filename = f"tvt_{split_ratio}.csv"
            filepath = self.splits_dir / mod / filename
            
            if not filepath.exists():
                print(f"Aviso: Arquivo não encontrado: {filepath}")
                continue
            
            df_split = pd.read_csv(filepath)
            
            # Carregar dataset base correspondente para fazer merge
            base_df = self.load_base_dataset(
                dataset_type=mod if mod != "bimodal" else "bimodal"
            )
            
            # Determinar colunas de ID para merge
            if mod == "lyrics":
                base_id_col = "Lyric_id"
                split_id_col = "Song_id"  # No split file, lyrics usa Song_id
            else:
                base_id_col = "Song_id"
                split_id_col = "Song_id"
            
            # Merge dos dados
            if base_id_col in base_df.columns and split_id_col in df_split.columns:
                if base_id_col != split_id_col:
                    # Para lyrics, renomear a coluna para fazer o merge
                    df_split_copy = df_split.copy()
                    df_split_copy = df_split_copy.rename(columns={split_id_col: base_id_col})
                    merged_df = pd.merge(base_df, df_split_copy, on=base_id_col, how="inner")
                else:
                    merged_df = pd.merge(base_df, df_split, on=base_id_col, how="inner")
            else:
                print(f"Aviso: Não foi possível fazer merge para {mod}. Colunas de ID não encontradas.")
                print(f"Base tem {base_id_col}: {base_id_col in base_df.columns}, Split tem {split_id_col}: {split_id_col in df_split.columns}")
                continue
            
            results[mod] = {}
            
            # Filtrar por tipo de split
            for split in split_types:
                col_name = f"in_{balanced_type}_{split}"
                
                if col_name in merged_df.columns:
                    filtered_df = merged_df[merged_df[col_name] == True].copy()
                    
                    if not filtered_df.empty:
                        results[mod][split] = filtered_df
                    else:
                        print(f"Aviso: Nenhum dado encontrado para {mod}/{split}/{balanced_type}")
                else:
                    print(f"Aviso: Coluna {col_name} não encontrada em {mod}")
        
        return results
    
    def load_default(self) -> pd.DataFrame:
        """
        Carrega o dataset padrão (merge_unified completo).
        
        Returns:
            DataFrame com o dataset merge_unified
        """
        return self.load_base_dataset("unified", balanced_only=False)
    
    def get_dataset_info(self, dataset_type: str = "unified") -> Dict:
        """
        Retorna informações sobre um dataset.
        
        Args:
            dataset_type: Tipo do dataset a analisar
            
        Returns:
            Dicionário com informações do dataset
        """
        df = self.load_base_dataset(dataset_type, balanced_only=False)
        
        info = {
            "shape": df.shape,
            "columns": list(df.columns),
            "quadrants": df["Quadrant"].value_counts().to_dict() if "Quadrant" in df.columns else None,
            "missing_values": df.isnull().sum().to_dict(),
            "data_types": df.dtypes.to_dict()
        }
        
        # Adicionar informações específicas sobre colunas balanced
        balanced_cols = [col for col in df.columns if "balanced" in col.lower()]
        if balanced_cols:
            info["balanced_columns"] = {}
            for col in balanced_cols:
                info["balanced_columns"][col] = df[col].value_counts().to_dict()
        
        return info
    
    def get_split_info(self, modality: str = "audio", split_ratio: str = "40_30_30") -> Dict:
        """
        Retorna informações sobre splits.
        
        Args:
            modality: Modalidade a analisar
            split_ratio: Proporção do split
            
        Returns:
            Dicionário com informações dos splits
        """
        filename = f"tvt_{split_ratio}.csv"
        filepath = self.splits_dir / modality / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
        
        df = pd.read_csv(filepath)
        
        info = {
            "shape": df.shape,
            "columns": list(df.columns),
            "quadrants": df["Quadrant"].value_counts().to_dict() if "Quadrant" in df.columns else None,
        }
        
        # Contar amostras por split type
        split_cols = [col for col in df.columns if col.startswith("in_")]
        for col in split_cols:
            info[col] = df[col].sum()
        
        return info


# Função de conveniência para uso rápido
def load_dataset(
    dataset_type: str = "unified",
    balanced_only: bool = False,
    base_path: str = "/workspace/BigDataProject/metadata"
) -> pd.DataFrame:
    """
    Função de conveniência para carregar rapidamente um dataset base.
    
    Args:
        dataset_type: Tipo do dataset ("audio", "bimodal", "lyrics", "unified")
        balanced_only: Se True, filtra apenas dados balanceados
        base_path: Caminho base para a pasta metadata
        
    Returns:
        DataFrame com os dados carregados
    """
    loader = DatasetLoader(base_path)
    return loader.load_base_dataset(dataset_type, balanced_only)


def load_splits(
    modality: Union[str, List[str]] = "all",
    split_ratio: str = "40_30_30",
    split_type: Union[str, List[str]] = "all",
    balanced_type: str = "balanced",
    base_path: str = "/workspace/BigDataProject/metadata"
) -> Dict[str, pd.DataFrame]:
    """
    Função de conveniência para carregar rapidamente splits.
    
    Args:
        modality: Modalidade(s) a carregar ("audio", "bimodal", "lyrics", "all")
        split_ratio: Proporção do split ("40_30_30", "70_15_15")
        split_type: Tipo(s) de split ("train", "validate", "test", "all")
        balanced_type: Tipo de balanceamento ("balanced", "complete")
        base_path: Caminho base para a pasta metadata
        
    Returns:
        Dicionário com DataFrames organizados por modalidade e tipo de split
    """
    loader = DatasetLoader(base_path)
    return loader.load_split_dataset(modality, split_ratio, split_type, balanced_type)


# Exemplo de uso
if __name__ == "__main__":
    # Criar instância do loader
    loader = DatasetLoader()
    
    # Carregar dataset padrão
    print("Carregando dataset padrão (merge_unified)...")
    default_data = loader.load_default()
    print(f"Shape: {default_data.shape}")
    print(f"Colunas: {list(default_data.columns)}")
    
    # Carregar dataset específico
    print("\nCarregando dataset bimodal balanceado...")
    bimodal_balanced = loader.load_base_dataset("bimodal", balanced_only=True)
    print(f"Shape: {bimodal_balanced.shape}")
    
    # Carregar splits
    print("\nCarregando splits de treino para todas as modalidades...")
    train_splits = loader.load_split_dataset(
        modality="all",
        split_ratio="40_30_30",
        split_type="train",
        balanced_type="balanced"
    )
    
    for modality, data in train_splits.items():
        if "train" in data:
            print(f"{modality} train shape: {data['train'].shape}")
    
    # Informações do dataset
    print("\nInformações do dataset unified:")
    info = loader.get_dataset_info("unified")
    print(f"Shape: {info['shape']}")
    print(f"Quadrantes: {info['quadrants']}")