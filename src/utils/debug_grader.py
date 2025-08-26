#!/usr/bin/env python3
"""
Debug script for AI Grader
Helps identify and fix common path and directory issues
"""

import os
import sys
from pathlib import Path

def debug_directory_structure(directory_path: str):
    """Debug the directory structure and file paths"""
    
    print("=" * 60)
    print("DEBUGGING DIRECTORY STRUCTURE")
    print("=" * 60)
    
    # Check if path exists
    print(f"Input path: {directory_path}")
    print(f"Absolute path: {os.path.abspath(directory_path)}")
    print(f"Normalized path: {os.path.normpath(directory_path)}")
    print(f"Path exists: {os.path.exists(directory_path)}")
    print(f"Is directory: {os.path.isdir(directory_path)}")
    print(f"Is file: {os.path.isfile(directory_path)}")
    
    if not os.path.exists(directory_path):
        print("❌ ERROR: Path does not exist!")
        return False
    
    if not os.path.isdir(directory_path):
        print("❌ ERROR: Path is not a directory!")
        return False
    
    # List contents
    print(f"\nDirectory contents:")
    try:
        contents = os.listdir(directory_path)
        print(f"Total items: {len(contents)}")
        
        notebooks = [f for f in contents if f.endswith('.ipynb')]
        other_files = [f for f in contents if not f.endswith('.ipynb') and os.path.isfile(os.path.join(directory_path, f))]
        directories = [f for f in contents if os.path.isdir(os.path.join(directory_path, f))]
        
        print(f"Notebook files: {len(notebooks)}")
        for nb in notebooks[:5]:  # Show first 5
            nb_path = os.path.join(directory_path, nb)
            print(f"  ✓ {nb} (size: {os.path.getsize(nb_path)} bytes)")
        
        if len(notebooks) > 5:
            print(f"  ... and {len(notebooks) - 5} more notebooks")
        
        if other_files:
            print(f"Other files: {len(other_files)}")
            for f in other_files[:3]:
                print(f"  • {f}")
        
        if directories:
            print(f"Subdirectories: {len(directories)}")
            for d in directories[:3]:
                print(f"  📁 {d}")
        
    except PermissionError:
        print("❌ ERROR: Permission denied reading directory!")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False
    
    return True

def test_ai_grader_basic(directory_path: str):
    """Test basic AI grader functionality"""
    
    print("\n" + "=" * 60)
    print("TESTING AI GRADER BASIC FUNCTIONALITY")
    print("=" * 60)
    
    try:
        # Import the AI grader
        from ai_grader import NotebookParser, MockLLM, AIGradingAgent
        
        print("✅ AI grader modules imported successfully")
        
        # Test notebook parser
        parser = NotebookParser()
        print("✅ Notebook parser created")
        
        # Find first notebook
        notebooks = [f for f in os.listdir(directory_path) if f.endswith('.ipynb')]
        if not notebooks:
            print("❌ No notebooks found for testing")
            return False
        
        test_notebook = os.path.join(directory_path, notebooks[0])
        print(f"Testing with: {test_notebook}")
        
        # Test parsing
        try:
            parsed = parser.parse_notebook(test_notebook)
            print(f"✅ Notebook parsed successfully")
            print(f"   Student: {parsed['student_name']}")
            print(f"   Problems found: {len(parsed['problems'])}")
            print(f"   Responses found: {len(parsed['responses'])}")
            
            for i, problem in enumerate(parsed['problems'][:3]):
                print(f"   Problem {i+1}: {problem['problem_id']}")
                
        except Exception as e:
            print(f"❌ Error parsing notebook: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Test AI grader creation
        try:
            llm = MockLLM()
            ai_grader = AIGradingAgent(llm)
            print("✅ AI grader created successfully")
            
            # Test path construction for output
            test_output_dir = os.path.join(directory_path, 'test_output')
            print(f"Test output directory: {test_output_dir}")
            
            # Create and remove test directory
            os.makedirs(test_output_dir, exist_ok=True)
            print("✅ Test output directory created")
            
            # Clean up
            import shutil
            shutil.rmtree(test_output_dir)
            print("✅ Test output directory cleaned up")
            
        except Exception as e:
            print(f"❌ Error with AI grader: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure ai_grader.py is in the same directory")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_path_construction(directory_path: str):
    """Test path construction logic"""
    
    print("\n" + "=" * 60)
    print("TESTING PATH CONSTRUCTION")
    print("=" * 60)
    
    # Test various path constructions
    test_paths = [
        os.path.join(directory_path, 'ai_grading_results'),
        os.path.join(directory_path, 'ai_grading_results', 'detailed_feedback'),
        os.path.join(directory_path, 'ai_grading_results', 'flagged_for_review.csv'),
    ]
    
    for path in test_paths:
        print(f"Testing path: {path}")
        print(f"  Absolute: {os.path.abspath(path)}")
        print(f"  Directory part: {os.path.dirname(path)}")
        print(f"  File part: {os.path.basename(path)}")
        
        # Test directory creation
        if path.endswith('.csv'):
            dir_part = os.path.dirname(path)
            try:
                os.makedirs(dir_part, exist_ok=True)
                print(f"  ✅ Directory created successfully: {dir_part}")
                
                # Test file creation
                with open(path, 'w') as f:
                    f.write("test")
                print(f"  ✅ File created successfully: {path}")
                
                # Clean up
                os.remove(path)
                print(f"  ✅ File removed")
                
            except Exception as e:
                print(f"  ❌ Error with file path: {e}")
        else:
            try:
                os.makedirs(path, exist_ok=True)
                print(f"  ✅ Directory created successfully")
                
                # Clean up
                os.rmdir(path)
                print(f"  ✅ Directory removed")
                
            except Exception as e:
                print(f"  ❌ Error with directory path: {e}")
        
        print()

def main():
    """Main debug function"""
    
    if len(sys.argv) != 2:
        print("Usage: python debug_grader.py <directory_path>")
        print("\nExample:")
        print("python debug_grader.py HW02")
        print("python debug_grader.py 'Homework/HW02_renamed'")
        sys.exit(1)
    
    directory_path = sys.argv[1]
    
    print(f"Debugging AI Grader with directory: {directory_path}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Step 1: Debug directory structure
    if not debug_directory_structure(directory_path):
        print("\n❌ Directory structure check failed!")
        sys.exit(1)
    
    # Step 2: Test path construction
    test_path_construction(directory_path)
    
    # Step 3: Test AI grader basics
    if not test_ai_grader_basic(directory_path):
        print("\n❌ AI grader basic test failed!")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED!")
    print("=" * 60)
    print("The AI grader should work with this directory.")
    print("\nTo run the full grading pipeline:")
    print(f"python integrated_grader.py '{directory_path}' hw2_california_housing --ai-grading")

if __name__ == "__main__":
    main()