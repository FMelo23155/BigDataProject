import pandas as pd

# Load the unified dataset
df = pd.read_csv('../metadata/base/merge_unified.csv')

print("=== BIMODAL EXAMPLE ===")
bimodal_example = df[df['bimodal'] == True].head(1)
print(bimodal_example[['Merge_id', 'Song_id', 'Lyric_id', 'bimodal', 'Artist', 'Title']])

print("\n=== AUDIO-ONLY EXAMPLE ===")
audio_only_example = df[(df['bimodal'] == False) & (df['Song_id'].notna())].head(1)
print(audio_only_example[['Merge_id', 'Song_id', 'Lyric_id', 'bimodal', 'Artist', 'Title']])

print("\n=== LYRICS-ONLY EXAMPLE ===")
lyrics_only_example = df[(df['bimodal'] == False) & (df['Song_id'].isna())].head(1)
print(lyrics_only_example[['Merge_id', 'Song_id', 'Lyric_id', 'bimodal', 'Artist', 'Title']])

print(f"\n=== SUMMARY ===")
print(f"Total rows: {len(df)}")
print(f"Bimodal (True): {df['bimodal'].sum()}")
print(f"Non-bimodal (False): {(~df['bimodal']).sum()}")
print(f"Audio-only: {((~df['bimodal']) & (df['Song_id'].notna())).sum()}")
print(f"Lyrics-only: {((~df['bimodal']) & (df['Song_id'].isna())).sum()}")

print(f"\n=== COLUMNS ===")
print(f"Total columns: {len(df.columns)}")
print("First 10 columns:", list(df.columns[:10]))
