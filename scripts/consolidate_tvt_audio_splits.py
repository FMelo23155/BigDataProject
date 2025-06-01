#!/usr/bin/env python3
"""
Script to consolidate audio TVT (Train/Validate/Test) split files into a single comprehensive file.

This script reads the following CSV files:
- tvt_40_30_30_test_audio_balanced.csv
- tvt_40_30_30_test_audio_complete.csv  
- tvt_40_30_30_train_audio_balanced.csv
- tvt_40_30_30_train_audio_complete.csv
- tvt_40_30_30_validate_audio_balanced.csv
- tvt_40_30_30_validate_audio_complete.csv

And creates a consolidated file with structure:
Song_id,Quadrant,in_balanced_train,in_balanced_validate,in_balanced_test,in_complete_train,in_complete_validate,in_complete_test
"""

import pandas as pd
import os
from pathlib import Path

def consolidate_audio_splits():
    """
    Consolidate all audio split CSV files into a single comprehensive file.
    """
    # Define paths
    base_path = Path(__file__).parent.parent
    metadata_path = base_path / "metadata" / "last" / "lastsplits"
    audio_path = base_path / "data" / "audio"
    
    # Define input CSV files
    csv_files = {
        'balanced_train': metadata_path / "tvt_40_30_30_train_audio_balanced.csv",
        'balanced_validate': metadata_path / "tvt_40_30_30_validate_audio_balanced.csv", 
        'balanced_test': metadata_path / "tvt_40_30_30_test_audio_balanced.csv",
        'complete_train': metadata_path / "tvt_40_30_30_train_audio_complete.csv",
        'complete_validate': metadata_path / "tvt_40_30_30_validate_audio_complete.csv",
        'complete_test': metadata_path / "tvt_40_30_30_test_audio_complete.csv"
    }
    
    # Check if all files exist
    missing_files = []
    for name, file_path in csv_files.items():
        if not file_path.exists():
            missing_files.append(str(file_path))
    
    if missing_files:
        print("ERROR: The following files are missing:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    
    print("Reading CSV files...")
    
    # Read all CSV files
    dataframes = {}
    for name, file_path in csv_files.items():
        try:
            df = pd.read_csv(file_path)
            print(f"  - {name}: {len(df)} records")
            dataframes[name] = df
        except Exception as e:
            print(f"ERROR reading {file_path}: {e}")
            return False
    
    # Get all unique songs from all files
    all_songs = set()
    for df in dataframes.values():
        all_songs.update(df['Song'].values)
    
    print(f"\nTotal unique songs found: {len(all_songs)}")
    
    # Create the consolidated dataframe
    consolidated_data = []
    
    for song in sorted(all_songs):
        # Initialize row data
        row_data = {
            'Song_id': song,
            'Quadrant': None,
            'in_balanced_train': 0,
            'in_balanced_validate': 0,
            'in_balanced_test': 0,
            'in_complete_train': 0,
            'in_complete_validate': 0,
            'in_complete_test': 0
        }
        
        # Check each dataset for this song
        for dataset_name, df in dataframes.items():
            song_rows = df[df['Song'] == song]
            if len(song_rows) > 0:
                # Set the quadrant (should be the same across all datasets for the same song)
                if row_data['Quadrant'] is None:
                    row_data['Quadrant'] = song_rows.iloc[0]['Quadrant']
                
                # Mark presence in this dataset
                if dataset_name == 'balanced_train':
                    row_data['in_balanced_train'] = 1
                elif dataset_name == 'balanced_validate':
                    row_data['in_balanced_validate'] = 1
                elif dataset_name == 'balanced_test':
                    row_data['in_balanced_test'] = 1
                elif dataset_name == 'complete_train':
                    row_data['in_complete_train'] = 1
                elif dataset_name == 'complete_validate':
                    row_data['in_complete_validate'] = 1
                elif dataset_name == 'complete_test':
                    row_data['in_complete_test'] = 1
        
        consolidated_data.append(row_data)
    
    # Create DataFrame
    consolidated_df = pd.DataFrame(consolidated_data)
    
    # Sort by Song_id for better organization
    consolidated_df = consolidated_df.sort_values('Song_id')
    
    # Save to output file
    output_file = audio_path / "tvt_40_30_30.csv"
    
    print(f"\nSaving consolidated file to: {output_file}")
    try:
        consolidated_df.to_csv(output_file, index=False)
        print(f"Successfully created {output_file}")
        print(f"Total records: {len(consolidated_df)}")
        
        # Print summary statistics
        print("\nSummary statistics:")
        print(f"  - Songs in balanced train: {consolidated_df['in_balanced_train'].sum()}")
        print(f"  - Songs in balanced validate: {consolidated_df['in_balanced_validate'].sum()}")
        print(f"  - Songs in balanced test: {consolidated_df['in_balanced_test'].sum()}")
        print(f"  - Songs in complete train: {consolidated_df['in_complete_train'].sum()}")
        print(f"  - Songs in complete validate: {consolidated_df['in_complete_validate'].sum()}")
        print(f"  - Songs in complete test: {consolidated_df['in_complete_test'].sum()}")
        
        # Print quadrant distribution
        quadrant_counts = consolidated_df['Quadrant'].value_counts().sort_index()
        print(f"\nQuadrant distribution:")
        for quadrant, count in quadrant_counts.items():
            print(f"  - {quadrant}: {count} songs")
        
        # Check for duplicates
        duplicates = consolidated_df[consolidated_df.duplicated('Song_id')]
        if len(duplicates) > 0:
            print(f"\nWARNING: Found {len(duplicates)} duplicate Song_id entries!")
        else:
            print("\n✓ No duplicate Song_id entries found.")
            
        return True
        
    except Exception as e:
        print(f"ERROR saving file: {e}")
        return False

def main():
    """Main function."""
    print("=== Audio TVT Split Consolidation Script ===")
    print("This script consolidates the audio train/validate/test split files")
    print("into a single comprehensive CSV file.\n")
    
    success = consolidate_audio_splits()
    
    if success:
        print("\n✓ Consolidation completed successfully!")
    else:
        print("\n✗ Consolidation failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
