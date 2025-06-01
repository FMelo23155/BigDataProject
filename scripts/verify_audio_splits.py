import pandas as pd

def verify_splits():
    """
    Verifies the consolidated audio splits file for data integrity.
    """
    file_path = r"c:\Users\aluno23155\Desktop\ProjetoBigData23155\metadata\splits\audio\tvt_40_30_30.csv"
    
    df = pd.read_csv(file_path)
    
    print("=== Audio Splits Verification ===")
    print(f"Total songs: {len(df)}")
    print(f"Unique songs: {df['Song_id'].nunique()}")
    print(f"Any duplicates: {df['Song_id'].duplicated().any()}")
    
    print("\n=== Split Distribution ===")
    print(f"Balanced train: {df['in_balanced_train'].sum()}")
    print(f"Balanced validate: {df['in_balanced_validate'].sum()}")
    print(f"Balanced test: {df['in_balanced_test'].sum()}")
    print(f"Complete train: {df['in_complete_train'].sum()}")
    print(f"Complete validate: {df['in_complete_validate'].sum()}")
    print(f"Complete test: {df['in_complete_test'].sum()}")
    
    print("\n=== Quadrant Distribution ===")
    print(df['Quadrant'].value_counts().sort_index())
    
    print("\n=== Sample Data ===")
    print(df.head(10))
    
    # Check for songs that appear in multiple splits (should be allowed)
    balanced_cols = ['in_balanced_train', 'in_balanced_validate', 'in_balanced_test']
    complete_cols = ['in_complete_train', 'in_complete_validate', 'in_complete_test']
    
    print("\n=== Cross-split Analysis ===")
    print("Songs in multiple balanced splits:")
    df['balanced_count'] = df[balanced_cols].sum(axis=1)
    print(df['balanced_count'].value_counts().sort_index())
    
    print("\nSongs in multiple complete splits:")
    df['complete_count'] = df[complete_cols].sum(axis=1)
    print(df['complete_count'].value_counts().sort_index())

if __name__ == "__main__":
    verify_splits()
