# setup.py
"""
Simple setup script for the modular AI grading system
"""

import os
import yaml

def create_config_file():
    """Create a basic configuration file"""
    
    config = {
        'llm_settings': {
            'provider': 'mock',  # Change to 'openai' or 'anthropic' when ready
            'model': 'gpt-4',
            'api_key': 'your_api_key_here',
            'max_tokens': 1500,
            'temperature': 0.3
        },
        'grading_settings': {
            'confidence_threshold': 0.7,
            'auto_flag_low_confidence': True,
            'enable_detailed_feedback': True,
            'max_suggestions': 5
        },
        'output_settings': {
            'generate_html_report': True,
            'export_detailed_feedback': True,
            'create_flagged_report': True,
            'save_grading_history': True
        },
        'system_settings': {
            'rubrics_directory': 'rubrics',
            'output_directory': 'ai_grading_results',
            'log_level': 'INFO'
        }
    }
    
    os.makedirs('config', exist_ok=True)
    config_path = 'config/config.yaml'
    
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, indent=2)
    
    print(f"✓ Created configuration file: {config_path}")

def create_directories():
    """Create necessary directories"""
    
    directories = [
        'config',
        'rubrics', 
        'ai_grading_results',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def create_requirements_file():
    """Create requirements.txt file"""
    
    requirements = [
        "nbformat>=5.0.0",
        "pyyaml>=6.0",
        "openai>=1.0.0  # For OpenAI GPT integration",
        "anthropic>=0.8.0  # For Claude integration", 
        "jupyter>=1.0.0",
        "matplotlib>=3.5.0",
        "pandas>=1.3.0",
        "numpy>=1.21.0"
    ]
    
    with open('requirements.txt', 'w') as f:
        f.write('\n'.join(requirements))
    
    print("✓ Created requirements.txt")

def main():
    """Main setup function"""
    
    print("Setting up Modular AI Grading System...")
    print("=" * 50)
    
    # create_directories()
    # create_config_file()
    # create_requirements_file()
    
    print("\n" + "=" * 50)
    print("Setup Complete!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Install requirements: pip install -r requirements.txt")
    print("2. Edit config/config.yaml to add your API keys")
    print("3. Test the system: python main_ai_grader.py --debug-config")
    print("4. Run grading: python main_ai_grader.py <directory> <assignment_id>")
    
    print("\nFile structure:")
    print("├── config/config.yaml          # Configuration settings")
    print("├── rubrics/                    # Assignment rubrics")
    print("├── data_structures.py          # Core data classes")
    print("├── notebook_parser.py          # Notebook parsing")
    print("├── rubric_manager.py           # Rubric management") 
    print("├── llm_interface.py            # LLM implementations")
    print("├── config_manager.py           # Configuration management")
    print("├── llm_grader.py               # LLM grading engine")
    print("├── report_generator.py         # Report generation")
    print("├── ai_grading_agent.py         # Main coordinator")
    print("└── main_ai_grader.py           # Entry point")

if __name__ == "__main__":
    main()