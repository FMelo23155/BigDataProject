#!/usr/bin/env python3
"""
Script para validar se os Song IDs do ficheiro merge_lyrics.csv estão presentes no ficheiro 
merge_lyrics_balanced_metadata.csv e adicionar uma coluna 'in_lyrics_balanced' com True/False.
"""

import pandas as pd
import os
import sys
from pathlib import Path

def main():
    """Função principal para executar a validação e adicionar a coluna."""
    
    # Caminhos dos ficheiros
    base_dir = Path(__file__).parent.parent
    target_file = base_dir / "metadata" / "base" / "merge_lyrics.csv"
    reference_file = base_dir / "metadata" / "last" / "lastbase" / "merge_lyrics_balanced_metadata.csv"
    
    print("=== Script de Validação - Lyrics Balanced ===")
    print(f"Ficheiro principal: {target_file}")
    print(f"Ficheiro de referência: {reference_file}")
    
    # Verificar se os ficheiros existem
    if not target_file.exists():
        print(f"ERRO: Ficheiro principal não encontrado: {target_file}")
        sys.exit(1)
        
    if not reference_file.exists():
        print(f"ERRO: Ficheiro de referência não encontrado: {reference_file}")
        sys.exit(1)
    
    try:
        # Carregar os dados
        print("\n1. A carregar ficheiros...")
        target_df = pd.read_csv(target_file)
        reference_df = pd.read_csv(reference_file)
        
        print(f"   - Ficheiro principal: {len(target_df)} registos")
        print(f"   - Ficheiro de referência: {len(reference_df)} registos")
        
        # Verificar se as colunas necessárias existem
        if 'Song_id' not in target_df.columns:
            print("ERRO: Coluna 'Song_id' não encontrada no ficheiro principal")
            sys.exit(1)
            
        if 'Song' not in reference_df.columns:
            print("ERRO: Coluna 'Song' não encontrada no ficheiro de referência")
            sys.exit(1)
        
        # Verificar se a coluna in_lyrics_balanced já existe
        if 'in_lyrics_balanced' in target_df.columns:
            print("AVISO: Coluna 'in_lyrics_balanced' já existe no ficheiro principal")
            response = input("Deseja sobrescrever os valores existentes? (s/n): ")
            if response.lower() not in ['s', 'sim', 'y', 'yes']:
                print("Operação cancelada pelo utilizador")
                sys.exit(0)
        
        # Criar conjunto de Song IDs do ficheiro de referência para lookup rápido
        print("\n2. A processar dados...")
        reference_songs = set(reference_df['Song'].values)
        
        # Criar a coluna in_lyrics_balanced
        target_df['in_lyrics_balanced'] = target_df['Song_id'].isin(reference_songs)
        
        # Validações e estatísticas
        print("\n3. A validar resultados...")
        
        total_songs = len(target_df)
        songs_in_balanced = target_df['in_lyrics_balanced'].sum()
        songs_not_in_balanced = total_songs - songs_in_balanced
        
        print(f"   - Total de registos: {total_songs}")
        print(f"   - Songs presentes no balanced: {songs_in_balanced} ({songs_in_balanced/total_songs*100:.1f}%)")
        print(f"   - Songs NÃO presentes no balanced: {songs_not_in_balanced} ({songs_not_in_balanced/total_songs*100:.1f}%)")
        
        # Mostrar alguns exemplos de songs que estão e não estão no balanced
        print("\n4. Exemplos de dados:")
        
        # Songs que estão no balanced
        songs_present = target_df[target_df['in_lyrics_balanced'] == True][['Song_id', 'Artist', 'Title']].head(3)
        if len(songs_present) > 0:
            print("   Songs presentes no balanced:")
            for _, row in songs_present.iterrows():
                print(f"     ✓ {row['Song_id']}: {row['Artist']} - {row['Title']}")
        
        # Songs que não estão no balanced
        songs_absent = target_df[target_df['in_lyrics_balanced'] == False][['Song_id', 'Artist', 'Title']].head(3)
        if len(songs_absent) > 0:
            print("   Songs NÃO presentes no balanced:")
            for _, row in songs_absent.iterrows():
                print(f"     ✗ {row['Song_id']}: {row['Artist']} - {row['Title']}")
        
        # Verificar se há songs no balanced que não estão no principal
        target_songs = set(target_df['Song_id'].values)
        only_in_balanced = reference_songs - target_songs
        
        if only_in_balanced:
            print(f"\n   - Songs apenas no balanced (não no principal): {len(only_in_balanced)}")
            if len(only_in_balanced) <= 5:
                print(f"     Exemplos: {list(only_in_balanced)}")
        
        # Guardar o ficheiro atualizado
        print(f"\n5. A guardar ficheiro atualizado: {target_file}")
        target_df.to_csv(target_file, index=False)
        
        print("\n✅ VALIDAÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"   - Coluna 'in_lyrics_balanced' adicionada")
        print(f"   - {songs_in_balanced}/{total_songs} songs estão presentes no balanced")
        
        # Estatísticas por quadrante (se disponível)
        if 'Quadrant' in target_df.columns:
            print(f"\n6. Estatísticas por quadrante:")
            quadrant_stats = target_df.groupby('Quadrant')['in_lyrics_balanced'].agg(['count', 'sum']).reset_index()
            quadrant_stats['percentage'] = (quadrant_stats['sum'] / quadrant_stats['count'] * 100).round(1)
            
            for _, row in quadrant_stats.iterrows():
                print(f"   - {row['Quadrant']}: {row['sum']}/{row['count']} ({row['percentage']}%)")
        
    except Exception as e:
        print(f"ERRO durante o processamento: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
