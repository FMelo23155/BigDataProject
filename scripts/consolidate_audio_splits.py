import pandas as pd
import os

def consolidate_audio_splits():
    """
    Consolidates audio split CSV files into a single file with proper structure.
    
    Reads from tvt_40_30_30_*_audio_*.csv files and creates a consolidated file
    with columns: Song_id, Quadrant, in_balanced_train, in_balanced_validate, 
    in_balanced_test, in_complete_train, in_complete_validate, in_complete_test
    """
    
    # Base directory paths
    base_dir = r"c:\Users\aluno23155\Desktop\ProjetoBigData23155"
    splits_dir = os.path.join(base_dir, "metadata", "last", "lastsplits")
    output_dir = os.path.join(base_dir, "metadata", "splits", "audio")
    
    # Define file mappings
    files_to_process = {
        'train_balanced': 'tvt_40_30_30_train_audio_balanced.csv',
        'train_complete': 'tvt_40_30_30_train_audio_complete.csv',
        'validate_balanced': 'tvt_40_30_30_validate_audio_balanced.csv',
        'validate_complete': 'tvt_40_30_30_validate_audio_complete.csv',
        'test_balanced': 'tvt_40_30_30_test_audio_balanced.csv',
        'test_complete': 'tvt_40_30_30_test_audio_complete.csv'
    }
    
    # Dictionary to store all songs and their information
    all_songs = {}
    
    # Process each file
    for split_type, filename in files_to_process.items():
        file_path = os.path.join(splits_dir, filename)
        
        if not os.path.exists(file_path):
            print(f"Warning: File {filename} not found at {file_path}")
            continue
            
        print(f"Processing {filename}...")
        
        # Read CSV file
        try:
            df = pd.read_csv(file_path)
            
            # Process each song in the file
            for _, row in df.iterrows():
                song_id = row['Song']
                quadrant = row['Quadrant']
                
                # Initialize song entry if it doesn't exist
                if song_id not in all_songs:
                    all_songs[song_id] = {
                        'Song_id': song_id,
                        'Quadrant': quadrant,
                        'in_balanced_train': False,
                        'in_balanced_validate': False,
                        'in_balanced_test': False,
                        'in_complete_train': False,
                        'in_complete_validate': False,
                        'in_complete_test': False
                    }
                
                # Mark the appropriate split as True
                if split_type == 'train_balanced':
                    all_songs[song_id]['in_balanced_train'] = True
                elif split_type == 'train_complete':
                    all_songs[song_id]['in_complete_train'] = True
                elif split_type == 'validate_balanced':
                    all_songs[song_id]['in_balanced_validate'] = True
                elif split_type == 'validate_complete':
                    all_songs[song_id]['in_complete_validate'] = True
                elif split_type == 'test_balanced':
                    all_songs[song_id]['in_balanced_test'] = True
                elif split_type == 'test_complete':
                    all_songs[song_id]['in_complete_test'] = True
                    
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            continue
    
    # Convert to DataFrame
    consolidated_df = pd.DataFrame(list(all_songs.values()))
    
    # Sort by Song_id for consistency
    consolidated_df = consolidated_df.sort_values('Song_id')
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to output file
    output_file = os.path.join(output_dir, "tvt_40_30_30.csv")
    consolidated_df.to_csv(output_file, index=False)
    
    print(f"\nConsolidation complete!")
    print(f"Total songs processed: {len(consolidated_df)}")
    print(f"Output saved to: {output_file}")
    
    # Print summary statistics
    print("\nSummary:")
    print(f"Songs in balanced train: {consolidated_df['in_balanced_train'].sum()}")
    print(f"Songs in balanced validate: {consolidated_df['in_balanced_validate'].sum()}")
    print(f"Songs in balanced test: {consolidated_df['in_balanced_test'].sum()}")
    print(f"Songs in complete train: {consolidated_df['in_complete_train'].sum()}")
    print(f"Songs in complete validate: {consolidated_df['in_complete_validate'].sum()}")
    print(f"Songs in complete test: {consolidated_df['in_complete_test'].sum()}")
    
    # Check for any quadrant distribution
    print(f"\nQuadrant distribution:")
    print(consolidated_df['Quadrant'].value_counts().sort_index())
    
    return consolidated_df

if __name__ == "__main__":
    print("Starting consolidation process...")
    try:
        result = consolidate_audio_splits()
        print("Script completed successfully!")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
