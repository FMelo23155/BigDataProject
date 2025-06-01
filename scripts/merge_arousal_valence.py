#!/usr/bin/env python3
"""
Script to merge Arousal and Valence values from merge_audio_complete_av_values.csv
into merge_audio.csv (metadata/base) based on Song IDs.

Author: Generated for ProjetoBigData23155
Date: 2025-06-01
"""

import pandas as pd
import os
import sys
from pathlib import Path

def validate_files(base_path, av_path):
    """
    Validate that both input files exist and are readable.
    
    Args:
        base_path (str): Path to the base metadata file
        av_path (str): Path to the arousal/valence values file
    
    Returns:
        bool: True if both files are valid, False otherwise
    """
    if not os.path.exists(base_path):
        print(f"Error: Base metadata file not found: {base_path}")
        return False
    
    if not os.path.exists(av_path):
        print(f"Error: Arousal/Valence file not found: {av_path}")
        return False
    
    try:
        # Test if files are readable
        pd.read_csv(base_path, nrows=1)
        pd.read_csv(av_path, nrows=1)
        print("✓ Both input files are accessible and readable")
        return True
    except Exception as e:
        print(f"Error reading files: {e}")
        return False

def load_and_validate_data(base_path, av_path):
    """
    Load and validate the data from both CSV files.
    
    Args:
        base_path (str): Path to the base metadata file
        av_path (str): Path to the arousal/valence values file
    
    Returns:
        tuple: (base_df, av_df) if successful, (None, None) if failed
    """
    try:
        # Load the base metadata file
        print("Loading base metadata file...")
        base_df = pd.read_csv(base_path)
        print(f"✓ Loaded base metadata: {len(base_df)} rows, {len(base_df.columns)} columns")
        
        # Load the arousal/valence file
        print("Loading arousal/valence values file...")
        av_df = pd.read_csv(av_path)
        print(f"✓ Loaded arousal/valence data: {len(av_df)} rows, {len(av_df.columns)} columns")
        
        # Validate required columns
        if 'Song' not in base_df.columns:
            print("Error: 'Song' column not found in base metadata file")
            return None, None
        
        if 'Song' not in av_df.columns:
            print("Error: 'Song' column not found in arousal/valence file")
            return None, None
        
        if 'Arousal' not in av_df.columns:
            print("Error: 'Arousal' column not found in arousal/valence file")
            return None, None
        
        if 'Valence' not in av_df.columns:
            print("Error: 'Valence' column not found in arousal/valence file")
            return None, None
        
        print("✓ All required columns are present")
        return base_df, av_df
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None

def merge_arousal_valence(base_df, av_df):
    """
    Merge the arousal and valence data into the base dataframe.
    
    Args:
        base_df (pd.DataFrame): Base metadata dataframe
        av_df (pd.DataFrame): Arousal/valence dataframe
    
    Returns:
        pd.DataFrame: Merged dataframe with Arousal and Valence columns
    """
    print("\nStarting merge process...")
    
    # Check for existing Arousal/Valence columns
    if 'Arousal' in base_df.columns:
        print("Warning: 'Arousal' column already exists in base data - it will be overwritten")
    if 'Valence' in base_df.columns:
        print("Warning: 'Valence' column already exists in base data - it will be overwritten")
    
    # Perform the merge
    merged_df = base_df.merge(
        av_df[['Song', 'Arousal', 'Valence']], 
        on='Song', 
        how='left',
        suffixes=('', '_new')
    )
    
    # Handle conflicts if columns already existed
    if 'Arousal_new' in merged_df.columns:
        merged_df['Arousal'] = merged_df['Arousal_new']
        merged_df = merged_df.drop('Arousal_new', axis=1)
    
    if 'Valence_new' in merged_df.columns:
        merged_df['Valence'] = merged_df['Valence_new']
        merged_df = merged_df.drop('Valence_new', axis=1)
    
    print(f"✓ Merge completed: {len(merged_df)} rows")
    
    # Validation statistics
    total_songs = len(merged_df)
    songs_with_arousal = merged_df['Arousal'].notna().sum()
    songs_with_valence = merged_df['Valence'].notna().sum()
    songs_missing_arousal = total_songs - songs_with_arousal
    songs_missing_valence = total_songs - songs_with_valence
    
    print(f"\nMerge Statistics:")
    print(f"  Total songs in base file: {total_songs}")
    print(f"  Songs with Arousal values: {songs_with_arousal}")
    print(f"  Songs with Valence values: {songs_with_valence}")
    print(f"  Songs missing Arousal: {songs_missing_arousal}")
    print(f"  Songs missing Valence: {songs_missing_valence}")
    
    if songs_missing_arousal > 0 or songs_missing_valence > 0:
        missing_songs = merged_df[merged_df['Arousal'].isna() | merged_df['Valence'].isna()]['Song'].tolist()
        print(f"  Songs missing A/V data: {missing_songs[:10]}{'...' if len(missing_songs) > 10 else ''}")
    
    return merged_df

def save_merged_data(merged_df, output_path):
    """
    Save the merged dataframe to the output file.
    
    Args:
        merged_df (pd.DataFrame): Merged dataframe
        output_path (str): Path to save the output file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"\nSaving merged data to: {output_path}")
        merged_df.to_csv(output_path, index=False)
        print("✓ File saved successfully")
        
        # Verify the saved file
        verification_df = pd.read_csv(output_path)
        if len(verification_df) == len(merged_df):
            print("✓ File verification successful")
            return True
        else:
            print("Error: File verification failed - row count mismatch")
            return False
            
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

def main():
    """
    Main function to execute the merge process.
    """
    print("=" * 60)
    print("AROUSAL/VALENCE MERGE SCRIPT")
    print("=" * 60)
    print("Script started successfully!")
    
    # Define file paths
    base_dir = Path(__file__).parent.parent
    base_metadata_path = base_dir / "metadata" / "base" / "merge_audio.csv"
    av_values_path = base_dir / "metadata" / "last" / "lastbase" / "merge_audio_complete_av_values.csv"
    
    print(f"Base metadata file: {base_metadata_path}")
    print(f"Arousal/Valence file: {av_values_path}")
    
    # Step 1: Validate files
    if not validate_files(str(base_metadata_path), str(av_values_path)):
        print("\n❌ File validation failed. Exiting.")
        sys.exit(1)
    
    # Step 2: Load and validate data
    base_df, av_df = load_and_validate_data(str(base_metadata_path), str(av_values_path))
    if base_df is None or av_df is None:
        print("\n❌ Data loading failed. Exiting.")
        sys.exit(1)
    
    # Step 3: Merge data
    try:
        merged_df = merge_arousal_valence(base_df, av_df)
    except Exception as e:
        print(f"\n❌ Merge process failed: {e}")
        sys.exit(1)
    
    # Step 4: Save merged data
    if not save_merged_data(merged_df, str(base_metadata_path)):
        print("\n❌ Save operation failed. Exiting.")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ MERGE PROCESS COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print(f"Updated file: {base_metadata_path}")
    print(f"New columns added: Arousal, Valence")

if __name__ == "__main__":
    main()
