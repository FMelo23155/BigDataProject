#!/usr/bin/env python3
"""
Script para análise rápida do dataset unificado.
Mostra estatísticas e exemplos de cada modalidade.

Author: Generated for ProjetoBigData23155
Date: 2025-06-01
"""
import pandas as pd
import numpy as np
from pathlib import Path

def main():
    """Função principal para análise do dataset unificado."""
    
    print("=" * 80)
    print("📊 ANÁLISE DO DATASET UNIFICADO - MERGE PROJECT")
    print("=" * 80)
    
    # Carregar dataset unificado
    base_dir = Path(__file__).parent.parent
    unified_path = base_dir / "metadata" / "base" / "merge_unified.csv"
    
    try:
        df = pd.read_csv(unified_path)
        print(f"✅ Dataset carregado: {len(df)} registos, {len(df.columns)} colunas")
    except Exception as e:
        print(f"❌ Erro ao carregar dataset: {e}")
        return
    
    print("\n" + "=" * 60)
    print("📈 ESTATÍSTICAS GERAIS")
    print("=" * 60)
    
    # Estatísticas básicas
    total = len(df)
    audio_only = len(df[df['has_audio'] & ~df['has_lyrics']])
    lyrics_only = len(df[df['has_lyrics'] & ~df['has_audio']])
    bimodal = len(df[df['is_bimodal']])
    
    print(f"📊 Distribuição por modalidade:")
    print(f"   • Total de registos: {total}")
    print(f"   • Só Audio: {audio_only} ({audio_only/total*100:.1f}%)")
    print(f"   • Só Lyrics: {lyrics_only} ({lyrics_only/total*100:.1f}%)")
    print(f"   • Bimodal: {bimodal} ({bimodal/total*100:.1f}%)")
    
    print(f"\n🎯 Preenchimento de dados:")
    print(f"   • Song_id: {df['Song_id'].notna().sum()}/{total} ({df['Song_id'].notna().sum()/total*100:.1f}%)")
    print(f"   • Lyric_id: {df['Lyric_id'].notna().sum()}/{total} ({df['Lyric_id'].notna().sum()/total*100:.1f}%)")
    print(f"   • Artist: {df['Artist'].notna().sum()}/{total} ({df['Artist'].notna().sum()/total*100:.1f}%)")
    print(f"   • Title: {df['Title'].notna().sum()}/{total} ({df['Title'].notna().sum()/total*100:.1f}%)")
    print(f"   • Arousal: {df['Arousal'].notna().sum()}/{total} ({df['Arousal'].notna().sum()/total*100:.1f}%)")
    print(f"   • Valence: {df['Valence'].notna().sum()}/{total} ({df['Valence'].notna().sum()/total*100:.1f}%)")
    
    # Estatísticas dos conjuntos balanceados
    print(f"\n⚖️  Conjuntos balanceados:")
    audio_balanced = df[df['in_audio_balanced'] == 1.0]
    lyrics_balanced = df[df['in_lyrics_balanced'] == 1.0]
    bimodal_balanced = df[df['in_bimodal_balanced'] == 1.0]
    
    print(f"   • Audio balanceado: {len(audio_balanced)}")
    print(f"   • Lyrics balanceado: {len(lyrics_balanced)}")
    print(f"   • Bimodal balanceado: {len(bimodal_balanced)}")
    
    print("\n" + "=" * 60)
    print("🔍 EXEMPLOS DE CADA MODALIDADE")
    print("=" * 60)
    
    # Exemplo Audio only
    audio_example = df[df['has_audio'] & ~df['has_lyrics']].iloc[0]
    print(f"\n🎵 EXEMPLO - AUDIO ONLY:")
    print(f"   Merge_id: {audio_example['Merge_id']}")
    print(f"   Song_id: {audio_example['Song_id']}")
    print(f"   Lyric_id: {audio_example['Lyric_id']}")
    print(f"   Artist: {audio_example['Artist']}")
    print(f"   Title: {audio_example['Title']}")
    print(f"   Quadrant: {audio_example['Quadrant']}")
    print(f"   Arousal: {audio_example['Arousal']}")
    print(f"   Valence: {audio_example['Valence']}")
    print(f"   is_bimodal: {audio_example['is_bimodal']}")
    print(f"   has_audio: {audio_example['has_audio']}")
    print(f"   has_lyrics: {audio_example['has_lyrics']}")
    
    # Exemplo Lyrics only
    lyrics_example = df[df['has_lyrics'] & ~df['has_audio']].iloc[0]
    print(f"\n📝 EXEMPLO - LYRICS ONLY:")
    print(f"   Merge_id: {lyrics_example['Merge_id']}")
    print(f"   Song_id: {lyrics_example['Song_id']}")
    print(f"   Lyric_id: {lyrics_example['Lyric_id']}")
    print(f"   Artist: {lyrics_example['Artist']}")
    print(f"   Title: {lyrics_example['Title']}")
    print(f"   Quadrant: {lyrics_example['Quadrant']}")
    print(f"   Arousal: {lyrics_example['Arousal']}")
    print(f"   Valence: {lyrics_example['Valence']}")
    print(f"   is_bimodal: {lyrics_example['is_bimodal']}")
    print(f"   has_audio: {lyrics_example['has_audio']}")
    print(f"   has_lyrics: {lyrics_example['has_lyrics']}")
    
    # Exemplo Bimodal
    bimodal_example = df[df['is_bimodal']].iloc[0]
    print(f"\n🎭 EXEMPLO - BIMODAL:")
    print(f"   Merge_id: {bimodal_example['Merge_id']}")
    print(f"   Song_id: {bimodal_example['Song_id']}")
    print(f"   Lyric_id: {bimodal_example['Lyric_id']}")
    print(f"   Artist: {bimodal_example['Artist']}")
    print(f"   Title: {bimodal_example['Title']}")
    print(f"   Quadrant: {bimodal_example['Quadrant']}")
    print(f"   Arousal: {bimodal_example['Arousal']}")
    print(f"   Valence: {bimodal_example['Valence']}")
    print(f"   is_bimodal: {bimodal_example['is_bimodal']}")
    print(f"   has_audio: {bimodal_example['has_audio']}")
    print(f"   has_lyrics: {bimodal_example['has_lyrics']}")
    
    print("\n" + "=" * 60)
    print("🎯 VALIDAÇÃO DE INTEGRIDADE")
    print("=" * 60)
    
    # Validações
    print(f"✓ Merge_id único: {df['Merge_id'].nunique() == len(df)}")
    print(f"✓ Todos os bimodais têm Song_id e Lyric_id: {df[df['is_bimodal']]['Song_id'].notna().all() and df[df['is_bimodal']]['Lyric_id'].notna().all()}")
    print(f"✓ Audio only não tem Lyric_id: {df[df['has_audio'] & ~df['has_lyrics']]['Lyric_id'].isna().all()}")
    print(f"✓ Lyrics only não tem Song_id: {df[df['has_lyrics'] & ~df['has_audio']]['Song_id'].isna().all()}")
    print(f"✓ Todos têm Arousal e Valence: {df['Arousal'].notna().all() and df['Valence'].notna().all()}")
    
    print("\n" + "=" * 80)
    print("✅ ANÁLISE CONCLUÍDA!")
    print("=" * 80)
    print(f"📁 Dataset analisado: {unified_path}")
    print(f"📊 Resumo: {total} registos totais")
    print(f"   🎵 Audio: {audio_only} | 📝 Lyrics: {lyrics_only} | 🎭 Bimodal: {bimodal}")

if __name__ == "__main__":
    main()
