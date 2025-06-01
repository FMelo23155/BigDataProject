#!/usr/bin/env python3
"""
Script para fazer merge das colunas Arousal e Valence do ficheiro merge_lyrics_complete_av_values.csv
para o ficheiro merge_lyrics.csv baseado no Song_id.
"""

import pandas as pd
import os
import sys
from pathlib import Path

def main():
    """Função principal para executar o merge dos dados de lyrics."""
    
    # Caminhos dos ficheiros
    base_dir = Path(__file__).parent.parent
    target_file = base_dir / "metadata" / "base" / "merge_lyrics.csv"
    source_file = base_dir / "metadata" / "last" / "lastbase" / "merge_lyrics_complete_av_values.csv"
    
    print("=== Script de Merge - Lyrics Arousal e Valence ===")
    print(f"Ficheiro de destino: {target_file}")
    print(f"Ficheiro de origem: {source_file}")
    
    # Verificar se os ficheiros existem
    if not target_file.exists():
        print(f"ERRO: Ficheiro de destino não encontrado: {target_file}")
        sys.exit(1)
        
    if not source_file.exists():
        print(f"ERRO: Ficheiro de origem não encontrado: {source_file}")
        sys.exit(1)
    
    try:
        # Carregar os dados
        print("\n1. A carregar ficheiros...")
        target_df = pd.read_csv(target_file)
        source_df = pd.read_csv(source_file)
        
        print(f"   - Ficheiro de destino: {len(target_df)} registos")
        print(f"   - Ficheiro de origem: {len(source_df)} registos")
        
        # Verificar se as colunas necessárias existem
        if 'Song_id' not in target_df.columns:
            print("ERRO: Coluna 'Song_id' não encontrada no ficheiro de destino")
            sys.exit(1)
            
        if 'Song' not in source_df.columns:
            print("ERRO: Coluna 'Song' não encontrada no ficheiro de origem")
            sys.exit(1)
            
        if 'Arousal' not in source_df.columns or 'Valence' not in source_df.columns:
            print("ERRO: Colunas 'Arousal' ou 'Valence' não encontradas no ficheiro de origem")
            sys.exit(1)
        
        # Verificar se as colunas Arousal e Valence já existem no ficheiro de destino
        if 'Arousal' in target_df.columns or 'Valence' in target_df.columns:
            print("AVISO: Colunas Arousal e/ou Valence já existem no ficheiro de destino")
            response = input("Deseja sobrescrever os valores existentes? (s/n): ")
            if response.lower() not in ['s', 'sim', 'y', 'yes']:
                print("Operação cancelada pelo utilizador")
                sys.exit(0)
        
        # Fazer o merge dos dados
        print("\n2. A fazer merge dos dados...")
        
        # Renomear a coluna 'Song' para 'Song_id' no dataframe de origem para facilitar o merge
        source_df_renamed = source_df.rename(columns={'Song': 'Song_id'})
        
        # Fazer o merge baseado no Song_id
        merged_df = target_df.merge(
            source_df_renamed[['Song_id', 'Arousal', 'Valence']], 
            on='Song_id', 
            how='left',
            suffixes=('', '_new')
        )
        
        # Se as colunas já existiam, substituir pelos novos valores
        if 'Arousal_new' in merged_df.columns:
            merged_df['Arousal'] = merged_df['Arousal_new']
            merged_df.drop('Arousal_new', axis=1, inplace=True)
            
        if 'Valence_new' in merged_df.columns:
            merged_df['Valence'] = merged_df['Valence_new']
            merged_df.drop('Valence_new', axis=1, inplace=True)
        
        # Validações
        print("\n3. A validar resultados...")
        
        # Verificar se o número de registos é o mesmo
        if len(merged_df) != len(target_df):
            print(f"AVISO: Número de registos alterado de {len(target_df)} para {len(merged_df)}")
        
        # Verificar quantos registos têm valores de Arousal e Valence
        arousal_count = merged_df['Arousal'].notna().sum()
        valence_count = merged_df['Valence'].notna().sum()
        
        print(f"   - Registos com Arousal: {arousal_count}/{len(merged_df)} ({arousal_count/len(merged_df)*100:.1f}%)")
        print(f"   - Registos com Valence: {valence_count}/{len(merged_df)} ({valence_count/len(merged_df)*100:.1f}%)")
        
        # Verificar se há registos no ficheiro de origem que não foram encontrados no destino
        target_song_ids = set(target_df['Song_id'].values)
        source_song_ids = set(source_df_renamed['Song_id'].values)
        
        missing_in_target = source_song_ids - target_song_ids
        missing_in_source = target_song_ids - source_song_ids
        
        if missing_in_target:
            print(f"   - Song_ids na origem mas não no destino: {len(missing_in_target)}")
            if len(missing_in_target) <= 5:
                print(f"     Exemplos: {list(missing_in_target)}")
        
        if missing_in_source:
            print(f"   - Song_ids no destino mas não na origem: {len(missing_in_source)}")
            if len(missing_in_source) <= 5:
                print(f"     Exemplos: {list(missing_in_source)}")
        
        # Mostrar alguns exemplos dos dados merged
        print("\n4. Exemplos de dados merged:")
        sample_data = merged_df[['Song_id', 'Artist', 'Title', 'Arousal', 'Valence']].head(3)
        for _, row in sample_data.iterrows():
            print(f"   - {row['Song_id']}: {row['Artist']} - {row['Title']} | Arousal: {row['Arousal']}, Valence: {row['Valence']}")
        
        # Guardar o ficheiro atualizado
        print(f"\n5. A guardar ficheiro atualizado: {target_file}")
        merged_df.to_csv(target_file, index=False)
        
        print("\n✅ MERGE CONCLUÍDO COM SUCESSO!")
        print(f"   - Total de registos: {len(merged_df)}")
        print(f"   - Registos com Arousal e Valence: {min(arousal_count, valence_count)}")
        
        # Estatísticas finais
        if arousal_count > 0:
            print(f"\n6. Estatísticas dos valores:")
            print(f"   - Arousal: min={merged_df['Arousal'].min():.4f}, max={merged_df['Arousal'].max():.4f}, média={merged_df['Arousal'].mean():.4f}")
            print(f"   - Valence: min={merged_df['Valence'].min():.4f}, max={merged_df['Valence'].max():.4f}, média={merged_df['Valence'].mean():.4f}")
        
    except Exception as e:
        print(f"ERRO durante o processamento: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
