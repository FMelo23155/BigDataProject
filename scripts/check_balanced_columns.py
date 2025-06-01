import pandas as pd

# Load the dataset
df = pd.read_csv('../metadata/base/merge_unified.csv')

print("Dataset columns:")
for i, col in enumerate(df.columns):
    print(f"  {i+1:2d}. {col}")

print("\nBalanced columns analysis:")
balanced_cols = ['in_audio_balanced', 'in_lyrics_balanced', 'in_bimodal_balanced']
for col in balanced_cols:
    if col in df.columns:
        count = df[col].sum()
        print(f"  {col}: {count}")
        # Show some sample values
        print(f"    Sample values: {df[col].value_counts().to_dict()}")
    else:
        print(f"  {col}: Column not found")

print(f"\nTotal entries: {len(df)}")
