#!/usr/bin/env python3
"""
Test Setup Verification

This script verifies that the toy example is properly set up and ready to run.
"""

import os
import sys
from pathlib import Path

def check_structure():
    """Check if the toy example structure is correct"""
    print("🔍 Checking Toy Example Structure...")
    
    base_dir = Path("tests/toy_example")
    required_files = [
        "sample_data.py",
        "run_toy_example.py", 
        "README.md",
        "test_config.yaml"
    ]
    
    required_dirs = [
        "notebooks",
        "rubrics",
        "expected_output"
    ]
    
    required_notebooks = [
        "notebooks/Student_A_Good_Answers.ipynb",
        "notebooks/Student_B_Incomplete_Answers.ipynb", 
        "notebooks/Student_C_No_Answers.ipynb"
    ]
    
    required_rubrics = [
        "rubrics/toy_data_analysis.yaml"
    ]
    
    all_good = True
    
    # Check directories
    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            print(f"✅ Directory: {dir_name}")
        else:
            print(f"❌ Missing directory: {dir_name}")
            all_good = False
    
    # Check files
    for file_name in required_files:
        file_path = base_dir / file_name
        if file_path.exists():
            print(f"✅ File: {file_name}")
        else:
            print(f"❌ Missing file: {file_name}")
            all_good = False
    
    # Check notebooks
    for notebook in required_notebooks:
        notebook_path = base_dir / notebook
        if notebook_path.exists():
            print(f"✅ Notebook: {notebook}")
        else:
            print(f"❌ Missing notebook: {notebook}")
            all_good = False
    
    # Check rubrics
    for rubric in required_rubrics:
        rubric_path = base_dir / rubric
        if rubric_path.exists():
            print(f"✅ Rubric: {rubric}")
        else:
            print(f"❌ Missing rubric: {rubric}")
            all_good = False
    
    return all_good

def check_dependencies():
    """Check if required Python packages are available"""
    print("\n📦 Checking Dependencies...")
    
    required_packages = [
        'pandas',
        'numpy', 
        'matplotlib',
        'seaborn',
        'nbformat',
        'pyyaml'
    ]
    
    all_good = True
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ Package: {package}")
        except ImportError:
            print(f"❌ Missing package: {package}")
            all_good = False
    
    return all_good

def check_src_structure():
    """Check if the src directory structure is correct"""
    print("\n🏗️ Checking Source Code Structure...")
    
    src_dir = Path("src")
    required_packages = [
        "core",
        "ai_grading", 
        "config",
        "reports",
        "utils"
    ]
    
    all_good = True
    
    if not src_dir.exists():
        print("❌ Missing src directory")
        return False
    
    for package in required_packages:
        package_path = src_dir / package
        if package_path.exists() and (package_path / "__init__.py").exists():
            print(f"✅ Package: {package}")
        else:
            print(f"❌ Missing package: {package}")
            all_good = False
    
    return all_good

def main():
    """Main verification function"""
    print("🎯 AI Grader Toy Example Setup Verification")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("src"):
        print("❌ Error: Please run this from the root directory of the AI-Grader project")
        print("Current directory:", os.getcwd())
        sys.exit(1)
    
    all_good = True
    
    # Run all checks
    if not check_structure():
        all_good = False
    
    if not check_dependencies():
        all_good = False
    
    if not check_src_structure():
        all_good = False
    
    # Summary
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 All checks passed! Toy example is ready to run.")
        print("\n🚀 Next steps:")
        print("1. Run: python tests/run_toy_example.py")
        print("2. Or run: python tests/toy_example/run_toy_example.py")
        print("\n📚 See tests/toy_example/README.md for detailed instructions")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\n💡 Common fixes:")
        print("- Install missing packages: pip install -r requirements.txt")
        print("- Ensure you're in the root directory")
        print("- Check file permissions")
        sys.exit(1)

if __name__ == "__main__":
    main()
