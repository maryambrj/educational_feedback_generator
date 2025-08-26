# AI-Grader Project Structure

This document describes the organized structure of the AI-Enhanced Notebook Grading System.

## 📁 Directory Organization

```
AI-Grader/
├── main.py                          # Main entry point
├── requirements.txt                 # Python dependencies
├── README.md                       # Project documentation
├── .gitignore                      # Git ignore rules
├── PROJECT_STRUCTURE.md            # This file
│
├── src/                            # Source code package
│   ├── __init__.py                # Package initialization
│   │
│   ├── core/                      # Core grading functionality
│   │   ├── __init__.py           # Core package exports
│   │   ├── main_ai_grader.py     # Main grading pipeline
│   │   ├── notebook_grader.py    # Traditional notebook grading
│   │   ├── notebook_parser.py    # Notebook structure parsing
│   │   └── notebook_to_markdown.py # Notebook conversion utilities
│   │
│   ├── ai_grading/               # AI-powered grading components
│   │   ├── __init__.py           # AI grading package exports
│   │   ├── ai_grading_agent.py   # Main AI grading agent
│   │   ├── enhanced_grading_agent.py # Enhanced grading capabilities
│   │   ├── llm_grader.py         # LLM integration for grading
│   │   └── llm_interface.py      # Abstract LLM interface
│   │
│   ├── config/                    # Configuration management
│   │   ├── __init__.py           # Config package exports
│   │   ├── config_manager.py     # Configuration loading/validation
│   │   └── data_structures.py    # Data models and structures
│   │
│   ├── reports/                   # Report generation and rubrics
│   │   ├── __init__.py           # Reports package exports
│   │   ├── report_generator.py   # HTML and CSV report generation
│   │   └── rubric_manager.py     # Rubric loading and management
│   │
│   ├── utils/                     # Utility functions and scripts
│   │   ├── __init__.py           # Utils package exports
│   │   ├── solution_cli.py       # Command-line solution tools
│   │   ├── solution_generator.py # Solution generation utilities
│   │   ├── file_checker.py       # File validation utilities
│   │   ├── rename_notebooks.py   # Notebook renaming utilities
│   │   └── debug_grader.py       # Debugging and testing tools
│   │
│   ├── notebooks/                 # Jupyter notebook examples
│   │   └── Testing.ipynb         # Testing and development notebook
│   │
│   └── setup.py                  # Setup and configuration script
│
├── tests/                         # Test suite (to be created)
├── docs/                          # Documentation
│   └── enhanced_usage_guide.md   # Detailed usage guide
├── examples/                      # Example configurations and data
└── .git/                         # Git repository
```

## 🔧 Package Dependencies

### Core Dependencies
- **nbformat**: Jupyter notebook parsing and manipulation
- **pyyaml**: YAML configuration file handling
- **jupyter**: Jupyter ecosystem support
- **pandas/numpy**: Data processing and analysis
- **matplotlib**: Plotting and visualization

### AI Integration Dependencies
- **openai**: OpenAI GPT API integration
- **anthropic**: Anthropic Claude API integration

## 🚀 Usage

### Running the System
```bash
# Main entry point
python main.py <directory> <assignment_id> [output_csv]

# Debug configuration
python main.py --debug-config

# Test LLM
python main.py --test-llm
```

### Importing in Code
```python
# Import core functionality
from src.core import process_student_notebooks, enhanced_grading_pipeline

# Import AI grading components
from src.ai_grading import AIGradingAgent, LLMFactory

# Import configuration
from src.config import ConfigManager

# Import reporting
from src.reports import create_combined_report, RubricManager

# Import utilities
from src.utils import rename_notebooks, debug_grading
```

## 📋 Key Components

### 1. Core Grading (`src/core/`)
- **main_ai_grader.py**: Orchestrates the entire grading pipeline
- **notebook_grader.py**: Traditional completion-based grading
- **notebook_parser.py**: Extracts structured content from notebooks
- **notebook_to_markdown.py**: Converts notebooks to markdown format

### 2. AI Grading (`src/ai_grading/`)
- **ai_grading_agent.py**: Main AI grading agent
- **enhanced_grading_agent.py**: Advanced grading capabilities
- **llm_grader.py**: LLM integration for content analysis
- **llm_interface.py**: Abstract interface for different LLM providers

### 3. Configuration (`src/config/`)
- **config_manager.py**: Loads and validates YAML configuration
- **data_structures.py**: Defines data models and structures

### 4. Reporting (`src/reports/`)
- **report_generator.py**: Creates HTML and CSV reports
- **rubric_manager.py**: Manages grading rubrics and criteria

### 5. Utilities (`src/utils/`)
- **solution_cli.py**: Command-line solution management
- **solution_generator.py**: Solution generation utilities
- **file_checker.py**: File validation and checking
- **rename_notebooks.py**: Notebook renaming utilities
- **debug_grader.py**: Debugging and testing tools

## 🔄 Migration Notes

### Import Updates Required
After reorganization, some import statements in the source files may need to be updated to reflect the new package structure. The main entry point (`main.py`) handles the path setup automatically.

### Configuration Files
The system expects configuration files in the following locations:
- `config/config.yaml`: Main configuration
- `rubrics/`: Rubric definitions
- `ai_grading_results/`: Output directory

## 🧪 Testing

The `tests/` directory is prepared for future test development. Consider adding:
- Unit tests for each module
- Integration tests for the grading pipeline
- Mock data for testing scenarios

## 📚 Documentation

- **README.md**: Project overview and quick start
- **PROJECT_STRUCTURE.md**: This file - detailed structure explanation
- **docs/enhanced_usage_guide.md**: Comprehensive usage guide
- **src/notebooks/Testing.ipynb**: Interactive testing and examples

## 🚀 Next Steps

1. **Update imports**: Review and update any relative imports in source files
2. **Add tests**: Create comprehensive test suite
3. **Configuration**: Set up proper configuration management
4. **Documentation**: Expand usage examples and API documentation
5. **CI/CD**: Set up automated testing and deployment
