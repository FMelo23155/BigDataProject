#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir as colunas balanced no dataset unificado
para atingir os targets: Audio=3232, Lyrics=2400, Bimodal=2000
"""

import pandas as pd
import numpy as np

def update_balanced_columns():
    """
    Atualiza as colunas balanced no dataset unificado para atingir os targets.
    """
    
    # Carregar dataset unificado
    df = pd.read_csv('../metadata/base/merge_unified.csv')
    print(f"📁 Dataset carregado: {len(df)} entradas")
    
    # Targets balanced
    target_audio_balanced = 3232
    target_lyrics_balanced = 2400
    target_bimodal_balanced = 2000
    
    print(f"\n🎯 Targets Balanced:")
    print(f"   Audio: {target_audio_balanced}")
    print(f"   Lyrics: {target_lyrics_balanced}")
    print(f"   Bimodal: {target_bimodal_balanced}")
    
    # Identificar entradas por tipo
    has_audio = ~df['Song_id'].isnull()
    has_lyrics = ~df['Lyric_id'].isnull()
    is_bimodal = df['bimodal'] == True
    
    print(f"\n📊 Contagens atuais:")
    print(f"   Total com audio: {has_audio.sum()}")
    print(f"   Total com lyrics: {has_lyrics.sum()}")
    print(f"   Total bimodal: {is_bimodal.sum()}")
    
    # Resetar colunas balanced
    df['in_audio_balanced'] = False
    df['in_lyrics_balanced'] = False
    df['in_bimodal_balanced'] = False
    
    # 1. Selecionar entradas bimodal balanced (2000 de 2216)
    bimodal_indices = df[is_bimodal].index
    selected_bimodal = np.random.choice(bimodal_indices, size=target_bimodal_balanced, replace=False)
    df.loc[selected_bimodal, 'in_bimodal_balanced'] = True
    
    print(f"\n✅ Bimodal balanced: {target_bimodal_balanced} selecionadas")
    
    # 2. Selecionar entradas audio balanced (3232 total)
    # Incluir todas as bimodal balanced (2000) + mais entradas com audio
    audio_indices = df[has_audio].index
    # Primeiro incluir todas as bimodal balanced
    df.loc[selected_bimodal, 'in_audio_balanced'] = True
    
    # Depois selecionar mais entradas audio para completar 3232
    remaining_audio_needed = target_audio_balanced - target_bimodal_balanced  # 1232
    audio_not_bimodal_balanced = df[has_audio & ~df['in_audio_balanced']].index
    
    if len(audio_not_bimodal_balanced) >= remaining_audio_needed:
        selected_audio_additional = np.random.choice(audio_not_bimodal_balanced, 
                                                   size=remaining_audio_needed, replace=False)
        df.loc[selected_audio_additional, 'in_audio_balanced'] = True
        print(f"✅ Audio balanced: {target_audio_balanced} selecionadas (2000 bimodal + 1232 adicionais)")
    else:
        print(f"⚠️ Não há entradas suficientes para audio balanced")
    
    # 3. Selecionar entradas lyrics balanced (2400 total)
    # Incluir todas as bimodal balanced (2000) + mais entradas com lyrics
    lyrics_indices = df[has_lyrics].index
    # Primeiro incluir todas as bimodal balanced
    df.loc[selected_bimodal, 'in_lyrics_balanced'] = True
    
    # Depois selecionar mais entradas lyrics para completar 2400
    remaining_lyrics_needed = target_lyrics_balanced - target_bimodal_balanced  # 400
    lyrics_not_bimodal_balanced = df[has_lyrics & ~df['in_lyrics_balanced']].index
    
    if len(lyrics_not_bimodal_balanced) >= remaining_lyrics_needed:
        selected_lyrics_additional = np.random.choice(lyrics_not_bimodal_balanced, 
                                                    size=remaining_lyrics_needed, replace=False)
        df.loc[selected_lyrics_additional, 'in_lyrics_balanced'] = True
        print(f"✅ Lyrics balanced: {target_lyrics_balanced} selecionadas (2000 bimodal + 400 adicionais)")
    else:
        print(f"⚠️ Não há entradas suficientes para lyrics balanced")
    
    # Verificar resultados finais
    final_audio_balanced = df['in_audio_balanced'].sum()
    final_lyrics_balanced = df['in_lyrics_balanced'].sum()
    final_bimodal_balanced = df['in_bimodal_balanced'].sum()
    
    print(f"\n📈 Resultados finais:")
    print(f"   Audio balanced: {final_audio_balanced}/{target_audio_balanced}")
    print(f"   Lyrics balanced: {final_lyrics_balanced}/{target_lyrics_balanced}")
    print(f"   Bimodal balanced: {final_bimodal_balanced}/{target_bimodal_balanced}")
    
    # Salvar dataset atualizado
    output_path = '../metadata/base/merge_unified.csv'
    df.to_csv(output_path, index=False)
    print(f"\n💾 Dataset atualizado salvo em: {output_path}")
    
    return df

if __name__ == "__main__":
    print("🔧 ATUALIZANDO COLUNAS BALANCED NO DATASET UNIFICADO")
    print("=" * 60)
    
    # Definir seed para reprodutibilidade
    np.random.seed(42)
    
    updated_df = update_balanced_columns()
    
    print("\n" + "=" * 60)
    print("✅ ATUALIZAÇÃO CONCLUÍDA!")
