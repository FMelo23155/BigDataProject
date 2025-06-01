import pandas as pd
import numpy as np

# Define file paths
audio_file = r'c:\Users\aluno23155\Desktop\ProjetoBigData23155\metadata\base\merge_audio.csv'
lyrics_file = r'c:\Users\aluno23155\Desktop\ProjetoBigData23155\metadata\base\merge_lyrics.csv'
bimodal_file = r'c:\Users\aluno23155\Desktop\ProjetoBigData23155\metadata\base\merge_bimodal.csv'
output_file = r'c:\Users\aluno23155\Desktop\ProjetoBigData23155\metadata\base\merge_unified.csv'

# Read the datasets
print("Reading datasets...")
audio_df = pd.read_csv(audio_file)
lyrics_df = pd.read_csv(lyrics_file)
bimodal_df = pd.read_csv(bimodal_file)

print(f"Audio dataset shape: {audio_df.shape}")
print(f"Lyrics dataset shape: {lyrics_df.shape}")
print(f"Bimodal dataset shape: {bimodal_df.shape}")

# Create unified dataset by properly joining the datasets
print("Creating unified dataset...")

# Start with bimodal data as base (these have both Song_id and Lyric_id)
unified_df = bimodal_df.copy()
unified_df['Merge_id'] = unified_df['Song_id'] + '_' + unified_df['Lyric_id']
unified_df['bimodal'] = True

print(f"Starting with {len(unified_df)} bimodal entries")

# Find audio-only entries (not in bimodal)
audio_only = audio_df[~audio_df['Song_id'].isin(bimodal_df['Song_id'])].copy()
if len(audio_only) > 0:
    audio_only['Merge_id'] = audio_only['Song_id']
    audio_only['Lyric_id'] = np.nan
    audio_only['bimodal'] = False
    
    print(f"Found {len(audio_only)} audio-only entries")
    
    # Append audio-only entries
    unified_df = pd.concat([unified_df, audio_only], ignore_index=True, sort=False)

# Find lyrics-only entries (not in bimodal)
lyrics_only = lyrics_df[~lyrics_df['Lyric_id'].isin(bimodal_df['Lyric_id'])].copy()
if len(lyrics_only) > 0:
    lyrics_only['Merge_id'] = lyrics_only['Lyric_id']
    lyrics_only['Song_id'] = np.nan
    lyrics_only['bimodal'] = False
    
    print(f"Found {len(lyrics_only)} lyrics-only entries")
    
    # Append lyrics-only entries
    unified_df = pd.concat([unified_df, lyrics_only], ignore_index=True, sort=False)

# Reorder columns to have Merge_id, Song_id, Lyric_id, bimodal first
cols = ['Merge_id', 'Song_id', 'Lyric_id', 'bimodal']
remaining_cols = [col for col in unified_df.columns if col not in cols]
unified_df = unified_df[cols + remaining_cols]

print(f"Unified dataset shape: {unified_df.shape}")
print(f"Bimodal entries: {unified_df['bimodal'].sum()}")
print(f"Audio-only entries: {(~unified_df['bimodal'] & unified_df['Song_id'].notna()).sum()}")
print(f"Lyrics-only entries: {(~unified_df['bimodal'] & unified_df['Lyric_id'].notna() & unified_df['Song_id'].isna()).sum()}")

# Save to CSV
print(f"Saving unified dataset to {output_file}...")
unified_df.to_csv(output_file, index=False)

print("Dataset unification completed successfully!")
print(f"Final dataset saved with {len(unified_df)} rows and {len(unified_df.columns)} columns")

# Display sample data for verification
print("\nSample entries:")
print("Bimodal entry:")
print(unified_df[unified_df['bimodal'] == True].head(1)[['Merge_id', 'Song_id', 'Lyric_id', 'bimodal', 'Artist', 'Title']])

if len(audio_only) > 0:
    print("\nAudio-only entry:")
    print(unified_df[(~unified_df['bimodal']) & (unified_df['Song_id'].notna())].head(1)[['Merge_id', 'Song_id', 'Lyric_id', 'bimodal', 'Artist', 'Title']])

if len(lyrics_only) > 0:
    print("\nLyrics-only entry:")
    print(unified_df[(~unified_df['bimodal']) & (unified_df['Song_id'].isna())].head(1)[['Merge_id', 'Song_id', 'Lyric_id', 'bimodal', 'Artist', 'Title']])
