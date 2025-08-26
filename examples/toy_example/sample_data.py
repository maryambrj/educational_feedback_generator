#!/usr/bin/env python3
"""
Generate sample data for the toy data analysis assignment
"""

import pandas as pd
import numpy as np
import os

def create_sample_dataset():
    """Create a sample dataset for testing"""
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Create sample data
    n_samples = 100
    
    data = {
        'student_id': range(1, n_samples + 1),
        'age': np.random.randint(18, 25, n_samples),
        'study_hours': np.random.normal(15, 5, n_samples),
        'gpa': np.random.normal(3.2, 0.5, n_samples),
        'attendance': np.random.randint(70, 101, n_samples),
        'assignment_score': np.random.normal(85, 10, n_samples)
    }
    
    # Ensure realistic constraints
    data['gpa'] = np.clip(data['gpa'], 1.0, 4.0)
    data['study_hours'] = np.clip(data['study_hours'], 0, 30)
    data['assignment_score'] = np.clip(data['assignment_score'], 0, 100)
    
    # Create correlations
    data['gpa'] = data['gpa'] + (data['study_hours'] - 15) * 0.02
    data['assignment_score'] = data['assignment_score'] + (data['study_hours'] - 15) * 0.5
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV (in current directory since we're already in examples/toy_example/)
    csv_path = 'student_data.csv'
    df.to_csv(csv_path, index=False)
    
    print(f"✅ Created sample dataset: {csv_path}")
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\nSample data:")
    print(df.head())
    
    return df

if __name__ == "__main__":
    create_sample_dataset()
