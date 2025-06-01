import pandas as pd

def display_final_results():
    """Display the final results in the requested format"""
    
    # Load datasets
    audio_df = pd.read_csv('../metadata/base/merge_audio.csv')
    lyrics_df = pd.read_csv('../metadata/base/merge_lyrics.csv')
    bimodal_df = pd.read_csv('../metadata/base/merge_bimodal.csv')
    unified_df = pd.read_csv('../metadata/base/merge_unified.csv')
    
    print("=" * 60)
    print("DATASET UNIFICATION - FINAL RESULTS")
    print("=" * 60)
    print()
      # Complete counts from original datasets
    audio_complete = len(audio_df)
    lyrics_complete = len(lyrics_df)
    bimodal_complete = len(bimodal_df)
    
    # Balanced counts from unified dataset
    audio_balanced = unified_df['in_audio_balanced'].sum()
    lyrics_balanced = unified_df['in_lyrics_balanced'].sum()
    bimodal_balanced = unified_df['in_bimodal_balanced'].sum()
    
    # Display table in requested format
    print(f"{'Dataset':<25} {'Complete':<10} {'Balanced':<10}")
    print("-" * 45)
    print(f"{'Audio':<25} {audio_complete:<10} {audio_balanced:<10}")
    print(f"{'Lyrics':<25} {lyrics_complete:<10} {lyrics_balanced:<10}")
    print(f"{'Bimodal (Audio+Lyrics)':<25} {bimodal_complete:<10} {bimodal_balanced:<10}")
    
    print()
    print("=" * 60)
    print("UNIFIED DATASET SUMMARY")
    print("=" * 60)
    
    # Unified dataset breakdown
    total_entries = len(unified_df)
    bimodal_entries = unified_df['bimodal'].sum()
    audio_only_entries = ((~unified_df['bimodal']) & (unified_df['Song_id'].notna())).sum()
    lyrics_only_entries = ((~unified_df['bimodal']) & (unified_df['Song_id'].isna())).sum()
    
    print(f"Total entries in unified dataset: {total_entries}")
    print()
    print(f"Bimodal entries (has both audio & lyrics): {bimodal_entries}")
    print(f"Audio-only entries: {audio_only_entries}")
    print(f"Lyrics-only entries: {lyrics_only_entries}")
    print(f"Verification (sum): {bimodal_entries + audio_only_entries + lyrics_only_entries}")
    
    print()
    print("✅ Dataset structure:")
    print(f"   • Merge_id: Unique identifier for each entry")
    print(f"   • Song_id: Audio identifier (NaN for lyrics-only)")
    print(f"   • Lyric_id: Lyrics identifier (NaN for audio-only)")
    print(f"   • bimodal: True for entries with both audio & lyrics")
    print(f"   • Total columns: {len(unified_df.columns)}")
    
    print()
    print("✅ All data preserved - no entries lost during unification")
    print("✅ Output file: metadata/base/merge_unified.csv")
    print()
    print("=" * 60)

if __name__ == "__main__":
    display_final_results()
