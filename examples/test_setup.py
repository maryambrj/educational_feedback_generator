#!/usr/bin/env python3
"""
Test Setup Verification

This script verifies that the toy example is properly set up and ready to run.
"""

import os
import sys
from pathlib import Path

def check_examples_structure():
    """Check if the examples directory structure is correct"""
    print("🔍 Checking Examples Structure...")
    
    base_dir = Path("examples/toy_example")
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
    
    # Check for at least some notebooks (flexible - any notebooks are fine)
    notebooks_dir = base_dir / "notebooks"
    existing_notebooks = []
    if notebooks_dir.exists():
        existing_notebooks = list(notebooks_dir.glob("*.ipynb"))
    
    required_rubrics = [
        "rubrics/toy_data_analysis.yaml"
    ]
    
    all_good = True
    
    # Check directories
    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            print(f"✅ Directory: examples/toy_example/{dir_name}")
        else:
            print(f"❌ Missing directory: examples/toy_example/{dir_name}")
            all_good = False
    
    # Check files
    for file_name in required_files:
        file_path = base_dir / file_name
        if file_path.exists():
            print(f"✅ File: examples/toy_example/{file_name}")
        else:
            print(f"❌ Missing file: examples/toy_example/{file_name}")
            all_good = False
    
    # Check notebooks (flexible - just need at least one)
    if existing_notebooks:
        print(f"✅ Found {len(existing_notebooks)} notebook(s):")
        for notebook in existing_notebooks:
            print(f"  📓 {notebook.name}")
    else:
        print("⚠️  No notebooks found in examples/toy_example/notebooks/")
        print("   This is optional - you can still test with simple_demo.py")
    
    # Check rubrics
    for rubric in required_rubrics:
        rubric_path = base_dir / rubric
        if rubric_path.exists():
            print(f"✅ Rubric: examples/toy_example/{rubric}")
        else:
            print(f"❌ Missing rubric: examples/toy_example/{rubric}")
            all_good = False
    
    return all_good

def check_modular_system():
    """Check if the modular system files are present"""
    print("\n🔍 Checking Modular System Structure...")
    
    required_files = [
        "main.py",
        ".env",
        "requirements.txt",
        "README.md"
    ]
    
    # Optional files (nice to have but not required)
    optional_files = [
        "simple_model_demo.py"  # This was a demo file we intentionally removed
    ]
    
    required_src_files = [
        "src/config/model_config.py",
        "src/config/model_factory.py", 
        "src/config/config_loader.py",
        "src/config/model_cli.py",
        "src/config/README.md"
    ]
    
    all_good = True
    
    # Check required root files
    for file_name in required_files:
        file_path = Path(file_name)
        if file_path.exists():
            print(f"✅ File: {file_name}")
        else:
            print(f"❌ Missing file: {file_name}")
            all_good = False
    
    # Check optional files (informational only)
    for file_name in optional_files:
        file_path = Path(file_name)
        if file_path.exists():
            print(f"✅ Optional file: {file_name}")
        else:
            print(f"ℹ️  Optional file not present: {file_name} (this is fine)")
    
    # Check src files
    for file_name in required_src_files:
        file_path = Path(file_name)
        if file_path.exists():
            print(f"✅ Src file: {file_name}")
        else:
            print(f"❌ Missing src file: {file_name}")
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
        'yaml'  # pyyaml imports as 'yaml'
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
    print("🎯 AI Grader Modular System Verification")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("src"):
        print("❌ Error: Please run this from the root directory of the AI-Grader project")
        print("Current directory:", os.getcwd())
        sys.exit(1)
    
    all_good = True
    
    # Run all checks
    if not check_examples_structure():
        all_good = False
    
    if not check_modular_system():
        all_good = False
    
    if not check_dependencies():
        all_good = False
    
    if not check_src_structure():
        all_good = False
    
    # Summary
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 All essential checks passed! The system is ready to use.")
        print("\n🚀 Next steps:")
        print("1. Try the toy example: cd examples/toy_example && python simple_demo.py")
        print("2. Set up your API keys in .env file")
        print("3. Create your rubric and run: python main.py <notebook_dir> <assignment_id>")
        print("4. For anonymization: cd src/utils && python student_id_cli.py create <assignment> <notebooks>/")
        print("\n📚 See README.md for complete instructions")
    else:
        print("❌ Some essential checks failed. Please fix the issues above.")
        print("\n💡 Common fixes:")
        print("- Install missing packages: pip install -r requirements.txt")
        print("- Ensure you're in the project root directory (where README.md is)")
        print("- Check file permissions")
        print("- Run: python src/setup.py")
        sys.exit(1)

if __name__ == "__main__":
    main()
