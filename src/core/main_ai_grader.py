# main_ai_grader.py
"""
Main entry point for the AI grading system
"""

import sys
import os
from ..config.config_manager import ConfigManager, LLMFactory
from ..ai_grading.ai_grading_agent import AIGradingAgent
from ..reports.report_generator import create_combined_report

def debug_configuration(config_path: str = "config/config.yaml"):
    """Debug function to check configuration setup"""
    
    print("=" * 60)
    print("CONFIGURATION DEBUG")
    print("=" * 60)
    
    # Check if config file exists
    print(f"Config file path: {config_path}")
    print(f"Config file exists: {os.path.exists(config_path)}")
    print(f"Current working directory: {os.getcwd()}")
    
    if os.path.exists(config_path):
        try:
            config_manager = ConfigManager(config_path)
            print(f"✅ Configuration loaded successfully")
            
            # Show all LLM settings
            llm_settings = config_manager.config.get('llm_settings', {})
            print(f"\nLLM Settings:")
            for key, value in llm_settings.items():
                if key == 'api_key':
                    # Mask API key for security
                    display_value = f"{'*' * (len(str(value)) - 4)}{str(value)[-4:]}" if value else "Not set"
                else:
                    display_value = value
                print(f"  {key}: {display_value}")
            
            # Test LLM creation
            print(f"\nTesting LLM creation:")
            llm = LLMFactory.create_llm(config_manager)
            print(f"  Created LLM: {llm.get_model_name()}")
            
            # Test LLM response
            from ..ai_grading.llm_interface import MockLLM
            if isinstance(llm, MockLLM):
                print(f"  Status: Using Mock LLM (no real API calls)")
            else:
                print(f"  Status: Real LLM configured")
                print(f"  Note: API calls will be made when grading")
            
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"❌ Configuration file not found")
        print(f"To create a config file:")
        print(f"  1. Run: python integrated_grader.py --setup-ai")
        print(f"  2. Or manually create {config_path}")
    
    print("=" * 60)

def enhanced_grading_pipeline(directory_path: str, assignment_id: str, output_csv: str = "grades.csv"):
    """Enhanced grading pipeline that combines traditional and AI grading"""
    
    print("=" * 60)
    print("ENHANCED GRADING PIPELINE")
    print("=" * 60)
    
    # Step 1: ICAs (using existing system)
    print("Step 1: Running ICAs completion-based grading...")
    
    # Import and use existing grading functions
    try:
        from notebook_grader import process_student_notebooks
        process_student_notebooks(directory_path, output_csv)
    except ImportError:
        print("Warning: notebook_grader not found. Skipping ICAs.")
    
    # Step 2: AI-based grading
    print("\nStep 2: Running AI-based content grading...")
    
    # Initialize AI grading system with configured LLM
    try:
        # Load configuration
        config = ConfigManager()
        llm = LLMFactory.create_llm(config)
        print(f"Using LLM: {llm.get_model_name()}")
        
        # Debug: Show configuration details
        provider = config.get('llm_settings.provider', 'not_set')
        model = config.get('llm_settings.model', 'not_set')
        has_api_key = bool(config.get('llm_settings.api_key', ''))
        
        print(f"Configuration details:")
        print(f"  Provider: {provider}")
        print(f"  Model: {model}")
        print(f"  Has API key: {has_api_key}")
        
        if provider == 'mock':
            print("Warning: Using mock provider. To use real LLM:")
            print("  1. Edit config/config.yaml")
            print("  2. Set provider to 'openai' or 'anthropic'")
            print("  3. Add your API key")
        
    except Exception as e:
        print(f"Warning: Could not load configuration: {e}")
        print("Using MockLLM as fallback.")
        from ..ai_grading.llm_interface import MockLLM
        llm = MockLLM()
    
    ai_grader = AIGradingAgent(llm)
    
    # Grade all notebooks with AI
    ai_results = ai_grader.grade_directory(directory_path, assignment_id)
    
    # Step 3: Export AI grading results
    print("\nStep 3: Exporting AI grading results...")
    ai_output_dir = os.path.join(directory_path, 'ai_grading_results')
    ai_grader.export_results(ai_output_dir)
    
    # Step 4: Create combined report
    print("\nStep 4: Creating combined grading report...")
    create_combined_report(directory_path, output_csv, ai_results, assignment_id, "homework")
    
    print("\n" + "=" * 60)
    print("GRADING PIPELINE COMPLETE!")
    print("=" * 60)
    print(f"Traditional grades: {output_csv}")
    print(f"AI grades and feedback: {ai_output_dir}")
    print(f"Combined report: {os.path.join(directory_path, 'combined_grading_report.html')}")

def main():
    """Main function for command line usage"""
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main_ai_grader.py <directory_path> <assignment_id> [output_csv]")
        print("  python main_ai_grader.py --debug-config")
        print("  python main_ai_grader.py --test-llm")
        print("\nExample:")
        print("  python main_ai_grader.py HW02 hw2_california_housing grades.csv")
        sys.exit(1)
    
    if sys.argv[1] == "--debug-config":
        # Debug configuration
        debug_configuration()
        return
    
    elif sys.argv[1] == "--test-llm":
        # Test LLM configuration
        print("Testing LLM Configuration...")
        try:
            config = ConfigManager()
            llm = LLMFactory.create_llm(config)
            print(f"LLM: {llm.get_model_name()}")
            
            # Test a simple response
            response = llm.generate_response("Test prompt: What is 2+2?", max_tokens=100)
            print(f"Test response: {response[:200]}...")
            
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        return
    
    # Normal grading pipeline
    directory_path = sys.argv[1]
    assignment_id = sys.argv[2] if len(sys.argv) > 2 else "default_assignment"
    output_csv = sys.argv[3] if len(sys.argv) > 3 else "grades.csv"
    
    # Validate directory exists
    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' does not exist.")
        sys.exit(1)
    
    # Run enhanced grading pipeline
    enhanced_grading_pipeline(directory_path, assignment_id, output_csv)

if __name__ == "__main__":
    main()