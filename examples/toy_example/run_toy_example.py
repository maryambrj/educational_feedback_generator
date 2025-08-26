#!/usr/bin/env python3
"""
Toy Example Runner for AI Grader System

This script demonstrates the complete workflow of the AI grading system
using sample notebooks and data.
"""

import os
import sys
import subprocess
import pandas as pd
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def setup_toy_example():
    """Set up the toy example environment"""
    print("🚀 Setting up Toy Example...")
    
    # Create sample dataset
    print("📊 Generating sample dataset...")
    try:
        from sample_data import create_sample_dataset
        create_sample_dataset()
        print("✅ Sample dataset created successfully")
    except Exception as e:
        print(f"❌ Error creating sample dataset: {e}")
        return False
    
    # Copy data to notebooks directory
    import shutil
    src_data = "tests/toy_example/student_data.csv"
    dst_data = "tests/toy_example/notebooks/student_data.csv"
    shutil.copy2(src_data, dst_data)
    print("✅ Dataset copied to notebooks directory")
    
    return True

def run_traditional_grading():
    """Run traditional completion-based grading"""
    print("\n📝 Running Traditional Grading...")
    
    try:
        from core.notebook_grader import process_student_notebooks
        
        notebooks_dir = "tests/toy_example/notebooks"
        output_csv = "tests/toy_example/traditional_grades.csv"
        
        # Run traditional grading
        process_student_notebooks(notebooks_dir, output_csv)
        
        # Display results
        if os.path.exists(output_csv):
            df = pd.read_csv(output_csv)
            print("✅ Traditional grading completed!")
            print("\nTraditional Grading Results:")
            print("=" * 50)
            print(df.to_string(index=False))
            return True
        else:
            print("❌ Traditional grading output not found")
            return False
            
    except Exception as e:
        print(f"❌ Error in traditional grading: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_ai_grading():
    """Run AI-powered grading"""
    print("\n🤖 Running AI Grading...")
    
    try:
        from config.config_manager import ConfigManager
        from ai_grading.ai_grading_agent import AIGradingAgent
        
        # Use mock LLM for testing
        config = ConfigManager()
        config.config['llm_settings']['provider'] = 'mock'
        
        # Create AI grading agent
        from ai_grading.llm_interface import MockLLM
        llm = MockLLM()
        ai_grader = AIGradingAgent(llm)
        
        # Grade notebooks
        notebooks_dir = "tests/toy_example/notebooks"
        assignment_id = "toy_data_analysis"
        
        ai_results = ai_grader.grade_directory(notebooks_dir, assignment_id)
        
        print("✅ AI grading completed!")
        print(f"Graded {len(ai_results)} notebooks")
        
        # Export results
        output_dir = "tests/toy_example/ai_grading_results"
        ai_grader.export_results(output_dir)
        
        return True
        
    except Exception as e:
        print(f"❌ Error in AI grading: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_combined_report():
    """Generate combined grading report"""
    print("\n📊 Generating Combined Report...")
    
    try:
        from reports.report_generator import create_combined_report
        
        notebooks_dir = "tests/toy_example/notebooks"
        traditional_csv = "tests/toy_example/traditional_grades.csv"
        
        # Mock AI results for demonstration
        ai_results = {
            "Student_A_Good_Answers": {
                "overall_score": 85,
                "confidence": 0.9,
                "feedback": "Excellent work with comprehensive analysis"
            },
            "Student_B_Incomplete_Answers": {
                "overall_score": 45,
                "confidence": 0.8,
                "feedback": "Good start but incomplete analysis"
            },
            "Student_C_No_Answers": {
                "overall_score": 10,
                "confidence": 0.9,
                "feedback": "Minimal work completed"
            }
        }
        
        create_combined_report(notebooks_dir, traditional_csv, ai_results, "toy_data_analysis")
        
        print("✅ Combined report generated!")
        return True
        
    except Exception as e:
        print(f"❌ Error generating combined report: {e}")
        import traceback
        traceback.print_exc()
        return False

def display_summary():
    """Display a summary of the toy example"""
    print("\n" + "=" * 60)
    print("🎉 TOY EXAMPLE COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
    print("\n📁 Generated Files:")
    print("├── tests/toy_example/student_data.csv")
    print("├── tests/toy_example/traditional_grades.csv")
    print("├── tests/toy_example/ai_grading_results/")
    print("└── tests/toy_example/combined_grading_report.html")
    
    print("\n📊 What You Can Test:")
    print("1. Traditional grading (completion-based)")
    print("2. AI grading (content analysis)")
    print("3. Combined reporting")
    print("4. Missing answer detection")
    print("5. Different student performance levels")
    
    print("\n🚀 Next Steps:")
    print("1. Open combined_grading_report.html in your browser")
    print("2. Examine the traditional_grades.csv file")
    print("3. Check ai_grading_results/ for detailed feedback")
    print("4. Try running with real LLM by updating .env file")
    
    print("\n💡 Tips:")
    print("- The system automatically detected missing answers")
    print("- AI grading used mock responses for demonstration")
    print("- You can replace mock LLM with real OpenAI/Anthropic API")
    print("- All outputs are saved for inspection")

def main():
    """Main function to run the toy example"""
    print("🎯 AI Grader Toy Example")
    print("=" * 50)
    print("This will demonstrate the complete grading workflow")
    print("using sample notebooks and mock AI responses.\n")
    
    # Change to toy example directory
    os.chdir("tests/toy_example")
    
    # Run the complete workflow
    success = True
    
    if not setup_toy_example():
        success = False
    
    if success and not run_traditional_grading():
        success = False
    
    if success and not run_ai_grading():
        success = False
    
    if success and not run_combined_report():
        success = False
    
    if success:
        display_summary()
    else:
        print("\n❌ Toy example encountered errors. Check the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
