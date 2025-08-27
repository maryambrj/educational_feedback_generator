#!/usr/bin/env python3
"""
Working AI Grader Entry Point
This bypasses the relative import issues in main.py
"""

import sys
import os
import argparse
from pathlib import Path

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

# Add individual module directories to avoid relative import issues
sys.path.insert(0, os.path.join(src_dir, 'core'))
sys.path.insert(0, os.path.join(src_dir, 'config'))
sys.path.insert(0, os.path.join(src_dir, 'ai_grading'))
sys.path.insert(0, os.path.join(src_dir, 'reports'))
sys.path.insert(0, os.path.join(src_dir, 'utils'))

def main():
    """Main grading function that works around import issues"""
    parser = argparse.ArgumentParser(description='AI-Enhanced Notebook Grading System')
    parser.add_argument('notebook_dir', help='Directory containing student notebooks')
    parser.add_argument('assignment_id', help='Assignment ID (matches rubric filename for homework mode)')
    parser.add_argument('--mode', choices=['ica', 'homework'], default='homework', 
                        help='Grading mode: "ica" for completion-only, "homework" for rubric-based (default: homework)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    print("🎯 AI-Enhanced Notebook Grading System")
    print("=" * 50)
    print(f"📚 Notebooks: {args.notebook_dir}")
    print(f"📋 Assignment: {args.assignment_id}")
    print(f"🎯 Grading Mode: {args.mode.upper()}")
    print(f"🔧 Debug mode: {args.debug}")
    print()
    
    # Check if notebook directory exists
    notebook_path = Path(args.notebook_dir)
    if not notebook_path.exists():
        print(f"❌ Directory not found: {args.notebook_dir}")
        print("💡 Make sure the path is correct and run from project root")
        return 1
    
    # Find notebooks
    notebooks = list(notebook_path.glob("*.ipynb"))
    if not notebooks:
        print(f"❌ No notebooks found in: {args.notebook_dir}")
        print("💡 Make sure the directory contains .ipynb files")
        return 1
    
    print(f"📓 Found {len(notebooks)} notebook(s):")
    for nb in notebooks:
        print(f"  • {nb.name}")
    print()
    
    # Check for rubric (only required for homework mode)
    if args.mode == 'homework':
        rubric_path = Path(f"rubrics/{args.assignment_id}.yaml")
        if not rubric_path.exists():
            print(f"❌ Rubric not found: {rubric_path}")
            print(f"💡 Create a rubric file at: rubrics/{args.assignment_id}.yaml")
            print("📚 See README.md for rubric format")
            return 1
        
        print(f"✅ Rubric found: {rubric_path}")
    else:
        print("📝 ICA Mode: Completion-based grading (no rubric required)")
    print()
    
    # Run grading based on mode
    try:
        print("🔄 Loading grading system...")
        output_csv = "traditional_grades.csv"
        
        if args.mode == 'ica':
            # ICA mode: Only completion-based grading
            print("📝 Running ICA completion-based grading...")
            from notebook_grader import process_student_notebooks
            process_student_notebooks(str(notebook_path), output_csv)
            print(f"✅ ICA grading completed: {output_csv}")
            
        else:
            # Homework mode: Only run AI grading (no completion fallback)
            print("📚 Running homework grading with rubric analysis...")
            
            # Run AI grading only
            print("🤖 Running AI content analysis...")
            try:
                import subprocess
                result = subprocess.run([
                    sys.executable, 
                    'ai_grading_wrapper.py', 
                    str(notebook_path), 
                    args.assignment_id, 
                    output_csv
                ], capture_output=True, text=True, cwd=os.getcwd())
                
                print(result.stdout)
                if result.stderr:
                    print("Warnings:", result.stderr)
                
                if result.returncode == 0:
                    print("✅ AI grading completed successfully!")
                else:
                    print("❌ AI grading failed. No grades generated.")
                    print("💡 Fix the AI grading issues or use --mode ica for completion-based grading")
                    return 1
                    
            except Exception as e:
                print(f"❌ Could not run AI grading: {e}")
                print("💡 Fix the AI grading issues or use --mode ica for completion-based grading")
                return 1
        
        print("\n🎉 Grading completed!")
        print(f"📊 Results saved to: {output_csv}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error loading grading system: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        
        print("\n🔧 Troubleshooting suggestions:")
        print("1. Try ICA mode for simpler grading:")
        print(f"   python grade_notebooks.py \"{args.notebook_dir}\" {args.assignment_id} --mode ica")
        print("2. Check that all dependencies are installed:")
        print("   pip install -r requirements.txt")
        print("3. Make sure you're in the project root directory")
        print("4. For homework mode, ensure rubric exists:")
        print(f"   ls rubrics/{args.assignment_id}.yaml")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
