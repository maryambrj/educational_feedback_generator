#!/usr/bin/env python3
"""
Simple working demo of the toy example focusing on anonymization
"""

import os
import sys
import pandas as pd
from pathlib import Path

# Add src/utils to path for direct import
current_dir = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.join(current_dir, '..', '..', 'src', 'utils')
sys.path.insert(0, utils_dir)

from student_id_manager import StudentIDManager

def main():
    """Simple demonstration that works with the current setup"""
    print("🎯 Simple Toy Example Demo")
    print("=" * 50)
    
    # Step 1: Generate sample data
    print("\n1️⃣ Generating sample data...")
    from sample_data import create_sample_dataset
    df = create_sample_dataset()
    print(f"✅ Created dataset with {len(df)} rows")
    
    # Step 2: Simulate student notebooks
    print("\n2️⃣ Simulating student notebooks...")
    notebook_files = list(Path("notebooks").glob("*.ipynb"))
    
    if not notebook_files:
        print("⚠️  No notebook files found. Creating simulation...")
        notebook_files = [
            "Student_A_Good_Answers.ipynb",
            "Student_B_Incomplete_Answers.ipynb", 
            "Student_C_No_Answers.ipynb"
        ]
    else:
        notebook_files = [f.name for f in notebook_files]
    
    print(f"📚 Found {len(notebook_files)} notebooks:")
    for notebook in notebook_files:
        print(f"  • {notebook}")
    
    # Step 3: Demonstrate anonymization
    print("\n3️⃣ Demonstrating student anonymization...")
    id_manager = StudentIDManager("temp_mappings")
    
    student_mappings = {}
    for notebook in notebook_files:
        # Extract student name from filename
        student_name = notebook.replace('.ipynb', '').replace('_', ' ')
        
        # Generate anonymous ID
        anonymous_id = id_manager.generate_anonymous_id(student_name)
        student_mappings[student_name] = anonymous_id
        
        print(f"  👤 {student_name:<30} → {anonymous_id}")
    
    # Step 4: Save mappings
    print("\n4️⃣ Saving secure mappings...")
    assignment_id = "toy_demo"
    password = "demo123"
    
    mapping_file = id_manager.save_mapping(assignment_id, password)
    roster_file = id_manager.export_anonymous_roster(assignment_id)
    
    print(f"  💾 Mapping: {mapping_file}")
    print(f"  📋 Roster: {roster_file}")
    
    # Step 5: Mock grading results
    print("\n5️⃣ Creating mock grading results...")
    
    # Create a simple results CSV with anonymous IDs
    results_data = []
    for student_name, anon_id in student_mappings.items():
        # Mock some grades
        if "Good" in student_name:
            score = 85 + (hash(student_name) % 10)
        elif "Incomplete" in student_name:
            score = 65 + (hash(student_name) % 15)
        else:
            score = 45 + (hash(student_name) % 20)
        
        results_data.append({
            'Student_ID': anon_id,
            'Assignment': assignment_id,
            'Score': score,
            'Grade': 'A' if score >= 90 else 'B' if score >= 80 else 'C' if score >= 70 else 'D'
        })
    
    results_df = pd.DataFrame(results_data)
    results_file = "anonymous_results.csv"
    results_df.to_csv(results_file, index=False)
    
    print(f"  📊 Results saved to: {results_file}")
    print("\n📋 Anonymous results:")
    print(results_df.to_string(index=False))
    
    # Step 6: Demonstrate name revelation
    print("\n6️⃣ Demonstrating name revelation...")
    
    # Load mapping and reveal names
    id_manager_reveal = StudentIDManager("temp_mappings")
    success = id_manager_reveal.load_mapping(assignment_id, password)
    
    if success:
        print("✅ Mapping loaded successfully")
        print("\n🔓 Results with real names:")
        
        for _, row in results_df.iterrows():
            anon_id = row['Student_ID']
            real_name = id_manager_reveal.get_real_name(anon_id)
            print(f"  {real_name:<30} → {row['Score']} ({row['Grade']})")
    
    # Step 7: Summary
    print("\n7️⃣ Summary")
    print("=" * 50)
    print("✅ Completed workflow:")
    print("  1. Generated sample data")
    print("  2. Identified student notebooks") 
    print("  3. Created anonymous IDs")
    print("  4. Saved secure mappings")
    print("  5. Generated anonymous results")
    print("  6. Revealed real names")
    
    print(f"\n📁 Files created:")
    print(f"  • student_data.csv - Sample dataset")
    print(f"  • {results_file} - Anonymous grading results")
    print(f"  • {os.path.basename(mapping_file)} - Encrypted mappings")
    print(f"  • {os.path.basename(roster_file)} - Anonymous roster")
    
    print("\n🚀 Next steps:")
    print("  • Use the CLI tool: python ../../src/utils/student_id_cli.py")
    print("  • Try real grading with the main system")
    print("  • Set up API keys in .env for real LLM grading")

if __name__ == "__main__":
    main()
