import pandas as pd

# Load all datasets to get the complete picture
audio_df = pd.read_csv('../metadata/base/merge_audio.csv')
lyrics_df = pd.read_csv('../metadata/base/merge_lyrics.csv')
bimodal_df = pd.read_csv('../metadata/base/merge_bimodal.csv')
unified_df = pd.read_csv('../metadata/base/merge_unified.csv')

print("=== DATASET SUMMARY TABLE ===")
print()
print(f"{'Dataset':<20} {'Complete':<10} {'Balanced':<10}")
print("-" * 40)

# Audio statistics
audio_complete = len(audio_df)
audio_balanced = audio_df['in_audio_balanced'].sum() if 'in_audio_balanced' in audio_df.columns else 0

print(f"{'Audio':<20} {audio_complete:<10} {audio_balanced:<10}")

# Lyrics statistics  
lyrics_complete = len(lyrics_df)
lyrics_balanced = lyrics_df['in_lyrics_balanced'].sum() if 'in_lyrics_balanced' in lyrics_df.columns else 0

print(f"{'Lyrics':<20} {lyrics_complete:<10} {lyrics_balanced:<10}")

# Bimodal statistics
bimodal_complete = len(bimodal_df)
bimodal_balanced = bimodal_df['in_bimodal_balanced'].sum() if 'in_bimodal_balanced' in bimodal_df.columns else 0

print(f"{'Bimodal (Audio+Lyrics)':<20} {bimodal_complete:<10} {bimodal_balanced:<10}")

print()
print("=== UNIFIED DATASET BREAKDOWN ===")
print(f"Total entries in unified dataset: {len(unified_df)}")
print()

# Check what's actually in the unified dataset
bimodal_entries = unified_df['bimodal'].sum()
audio_only_entries = ((~unified_df['bimodal']) & (unified_df['Song_id'].notna())).sum()
lyrics_only_entries = ((~unified_df['bimodal']) & (unified_df['Song_id'].isna())).sum()

print(f"Bimodal entries: {bimodal_entries}")
print(f"Audio-only entries: {audio_only_entries}")  
print(f"Lyrics-only entries: {lyrics_only_entries}")
print(f"Total: {bimodal_entries + audio_only_entries + lyrics_only_entries}")

print()
print("=== EXPECTED vs ACTUAL ===")
print("Expected numbers based on your request:")
print("Complete: Audio=3554, Lyrics=2568, Bimodal=2216")
print("Balanced: Audio=3232, Lyrics=2400, Bimodal=2000")
print()
print("Current numbers:")
print(f"Complete: Audio={audio_complete}, Lyrics={lyrics_complete}, Bimodal={bimodal_complete}")
print(f"Balanced: Audio={audio_balanced}, Lyrics={lyrics_balanced}, Bimodal={bimodal_balanced}")

# Check balanced columns in unified dataset
print()
print("=== BALANCED COLUMNS IN UNIFIED DATASET ===")
balanced_cols = [col for col in unified_df.columns if 'balanced' in col.lower()]
print(f"Balanced columns found: {balanced_cols}")

for col in balanced_cols:
    if col in unified_df.columns:
        count = unified_df[col].sum()
        print(f"{col}: {count} True values")
