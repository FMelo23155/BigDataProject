#!/usr/bin/env python3
"""
Test script to demonstrate the DatasetLoader functionality.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from loader import DatasetLoader, load_dataset, load_splits

def main():
    print("🔄 Testing DatasetLoader Functionality")
    print("=" * 50)
    
    try:
        # Initialize loader
        print("1. Initializing DatasetLoader...")
        loader = DatasetLoader()
        print("   ✅ DatasetLoader initialized successfully!")
        
        # Test 1: Default loading (merge_unified)
        print("\n2. Testing default dataset loading...")
        default_data = loader.load_default()
        print(f"   ✅ Default dataset shape: {default_data.shape}")
        print(f"   📊 Quadrants distribution: {default_data['Quadrant'].value_counts().to_dict()}")
        
        # Test 2: Load specific base dataset
        print("\n3. Testing specific base dataset loading...")
        
        # Load audio dataset (balanced only)
        audio_balanced = loader.load_base_dataset("audio", balanced_only=True)
        print(f"   ✅ Audio balanced shape: {audio_balanced.shape}")
        
        # Load bimodal dataset (all data)
        bimodal_all = loader.load_base_dataset("bimodal", balanced_only=False)
        print(f"   ✅ Bimodal all shape: {bimodal_all.shape}")
        
        # Test 3: Load split datasets
        print("\n4. Testing split dataset loading...")
        
        # Load train data for all modalities (balanced, 40_30_30)
        train_splits = loader.load_split_dataset(
            modality="all",
            split_ratio="40_30_30", 
            split_type="train",
            balanced_type="balanced"
        )
        
        print("   ✅ Train splits loaded:")
        for modality, data in train_splits.items():
            if "train" in data:
                shape = data["train"].shape
                print(f"      - {modality}: {shape}")
        
        # Load specific split (lyrics, test, complete, 70_15_15)
        lyrics_test = loader.load_split_dataset(
            modality="lyrics",
            split_ratio="70_15_15",
            split_type="test", 
            balanced_type="complete"
        )
        
        if "lyrics" in lyrics_test and "test" in lyrics_test["lyrics"]:
            print(f"   ✅ Lyrics test (complete, 70_15_15): {lyrics_test['lyrics']['test'].shape}")
        
        # Test 4: Convenience functions
        print("\n5. Testing convenience functions...")
        
        # Quick dataset loading
        quick_unified = load_dataset("unified", balanced_only=False)
        print(f"   ✅ Quick unified load: {quick_unified.shape}")
        
        # Quick split loading
        quick_splits = load_splits(
            modality="audio",
            split_ratio="40_30_30",
            split_type=["train", "validate"],
            balanced_type="balanced"
        )
        
        print("   ✅ Quick splits loaded:")
        for modality, splits in quick_splits.items():
            for split_name, split_data in splits.items():
                print(f"      - {modality} {split_name}: {split_data.shape}")
        
        # Test 5: Dataset information
        print("\n6. Testing dataset information methods...")
        
        info = loader.get_dataset_info("unified")
        print(f"   ✅ Unified dataset info:")
        print(f"      - Shape: {info['shape']}")
        print(f"      - Columns: {len(info['columns'])}")
        print(f"      - Quadrants: {info['quadrants']}")
        
        # Test balanced columns info
        if "balanced_columns" in info:
            print(f"      - Balanced columns: {list(info['balanced_columns'].keys())}")
        
        split_info = loader.get_split_info("audio", "40_30_30")
        print(f"   ✅ Audio split info (40_30_30):")
        print(f"      - Shape: {split_info['shape']}")
        print(f"      - Train samples: {split_info.get('in_balanced_train', 'N/A')}")
        print(f"      - Validate samples: {split_info.get('in_balanced_validate', 'N/A')}")
        print(f"      - Test samples: {split_info.get('in_balanced_test', 'N/A')}")
        
        print("\n🎉 All tests completed successfully!")
        print("📋 DatasetLoader is fully functional and ready to use!")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
