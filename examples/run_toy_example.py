#!/usr/bin/env python3
"""
Simple Toy Example Runner

Run this from the root directory to test the complete AI grading workflow.
"""

import os
import sys

def main():
    """Run the toy example from the root directory"""
    print("🎯 Running AI Grader Toy Example...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("src"):
        print("❌ Error: Please run this from the root directory of the AI-Grader project")
        print("Current directory:", os.getcwd())
        sys.exit(1)
    
    # Change to toy example directory and run
    toy_example_dir = "examples/toy_example"
    if not os.path.exists(toy_example_dir):
        print("❌ Error: Toy example directory not found")
        sys.exit(1)
    
    # Run the toy example
    os.chdir(toy_example_dir)
    
    try:
        from run_toy_example import main as run_toy
        run_toy()
    except Exception as e:
        print(f"❌ Error running toy example: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
