# AI-Enhanced Notebook Grading System

An intelligent grading system that combines traditional completion-based grading with AI-powered content analysis for Jupyter notebooks. Features comprehensive **student anonymization** for bias-free grading, modular LLM configuration, and detailed feedback generation.

## 🌟 Key Features

- **🔒 Student Anonymization**: Complete privacy protection during grading with secure ID mapping
- **🤖 AI-Powered Analysis**: Advanced content evaluation using GPT-4, Claude, or other LLMs
- **📊 Dual Grading Methods**: Traditional completion metrics + AI content analysis
- **📝 Rich Feedback**: Detailed, actionable feedback for student improvement
- **⚙️ Modular Design**: Easily configurable models, providers, and grading criteria
- **📈 Comprehensive Reports**: HTML dashboards, CSV exports, and individual feedback

## 🚀 Complete Grading Guide (End-to-End)

### Step 1: Initial Setup

**Important**: All commands must be run from the project root directory (`AI-Grader/`)

```bash
# Navigate to project root (adjust path as needed)
cd /path/to/your/AI-Grader

# 1. Install dependencies
pip install -r requirements.txt

# 2. First time setup - creates directories and configuration files
python src/setup.py

# 3. Test that everything works
python examples/test_setup.py
```

### Step 2: Configure API Keys

Create a `.env` file in the root directory:
```bash
# .env file (automatically ignored by git for security)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

**Note**: You can start with `provider: 'mock'` in config to test without API keys.

### Step 3: Prepare Your Student Notebooks

Organize your student notebooks in a directory structure like:
```
Homework/HW02/
├── Smith_John.ipynb
├── Doe_Jane.ipynb
├── Garcia_Maria.ipynb
└── ...
```

**File naming**: Use `LastName_FirstName.ipynb` format for best results.

### Step 4: Create Assignment Rubric

Create a rubric file in `rubrics/hw2_your_assignment.yaml`:
```yaml
part_1:
  total_points: 30
  problem_statement: "Data Analysis and Visualization"
  expected_response_type: "mixed"  # code, text, or mixed
  context: "Students should demonstrate data analysis skills"
  criteria:
    analysis_quality:
      points: 15
      description: "Quality of data analysis and insights"
      guidelines: "Look for clear findings, proper methodology"
    code_quality:
      points: 10
      description: "Code clarity and correctness"
      guidelines: "Clean, well-commented, error-free code"
    visualization:
      points: 5
      description: "Quality of visualizations"
      guidelines: "Clear, properly labeled plots"
```

### Step 5: Run Anonymous Grading Workflow

#### 5A. Initialize Anonymous Session
```bash
# Navigate to the utils directory
cd src/utils

# Create anonymous grading session
python student_id_cli.py create hw2_assignment ../../Homework/HW02/

# This will:
# - Generate anonymous IDs (STUDENT_1001, STUDENT_1002, etc.)
# - Create encrypted mapping file
# - Export anonymous roster for graders
# - Prompt for secure password
```

#### 5B. Grade with Anonymous IDs
```bash
# Return to project root
cd ../..

# Run the main grading pipeline (now uses anonymous IDs)
python main.py "Homework/HW02" hw2_your_assignment

# This processes notebooks with anonymous identifiers
```

#### 5C. Review Anonymous Results
The system generates:
- `traditional_grades.csv` - with anonymous IDs
- `ai_grading_results/` - detailed AI feedback (anonymous)
- `combined_grading_report.html` - interactive dashboard (anonymous)

### Step 6: Reveal Student Names (After Grading)

```bash
# Navigate back to utils
cd src/utils

# Reveal all mappings (requires password from Step 5A)
python student_id_cli.py reveal hw2_assignment

# Or reveal results in a specific file
python student_id_cli.py reveal hw2_assignment --results ../../traditional_grades.csv --output ../../final_grades_with_names.csv

# Or look up specific student
python student_id_cli.py reveal hw2_assignment --id STUDENT_1001
```

### Step 7: Final Grade Distribution

Your final output includes:
- **`final_grades_with_names.csv`** - Complete results with real names
- **`combined_grading_report.html`** - Can be updated to show real names
- **Individual feedback files** - Mapped back to real names
- **Anonymous versions** - Keep for grader training/calibration

## 🎯 Quick Start (Traditional Workflow)

For those who want to start without anonymization:

```bash
# 1. Setup (one time)
python src/setup.py

# 2. Configure API keys in .env file

# 3. Run grading directly
python main.py "Homework/HW02" hw2_assignment

# Results will use real names throughout
```

## 📁 System Architecture

### Project Organization

The project is organized into logical packages for better maintainability:

- **`src/core/`**: Core grading functionality and main pipeline
- **`src/ai_grading/`**: AI-powered grading components and LLM integration
- **`src/config/`**: Configuration management and data structures
- **`src/reports/`**: Report generation, rubrics, and feedback
- **`src/utils/`**: Utility functions, CLI tools, and helper scripts
- **`src/notebooks/`**: Example notebooks and testing files

See `PROJECT_STRUCTURE.md` for detailed organization information.

### Core Components

1. **Notebook Parser**: Extracts structured content from student notebooks
2. **Rubric Manager**: Manages grading criteria and scoring systems
3. **LLM Grader**: Uses language models for content quality assessment
4. **Report Generator**: Creates comprehensive feedback reports

### File Structure
```
AI-Grader/
├── main.py                          # Main entry point
├── requirements.txt                 # Python dependencies
├── .env                            # Environment variables (API keys)
├── README.md                       # This documentation
├── PROJECT_STRUCTURE.md            # Detailed structure guide
│
├── src/                            # Source code package
│   ├── core/                      # Core grading functionality
│   │   ├── main_ai_grader.py     # Main grading pipeline
│   │   ├── notebook_grader.py    # Traditional notebook grading
│   │   ├── notebook_parser.py    # Notebook structure parsing
│   │   └── notebook_to_markdown.py # Notebook conversion utilities
│   │
│   ├── ai_grading/               # AI-powered grading components
│   │   ├── ai_grading_agent.py   # Main AI grading agent
│   │   ├── enhanced_grading_agent.py # Enhanced grading capabilities
│   │   ├── llm_grader.py         # LLM integration for grading
│   │   └── llm_interface.py      # Abstract LLM interface
│   │
│   ├── config/                    # Configuration management
│   │   ├── config_manager.py     # Configuration loading/validation
│   │   └── data_structures.py    # Data models and structures
│   │
│   ├── reports/                   # Report generation and rubrics
│   │   ├── report_generator.py   # HTML and CSV report generation
│   │   └── rubric_manager.py     # Rubric loading and management
│   │
│   ├── utils/                     # Utility functions and scripts
│   │   ├── solution_cli.py       # Command-line solution tools
│   │   ├── solution_generator.py # Solution generation utilities
│   │   ├── file_checker.py       # File validation utilities
│   │   ├── rename_notebooks.py   # Notebook renaming utilities
│   │   └── debug_grader.py       # Debugging and testing tools
│   │
│   ├── notebooks/                 # Jupyter notebook examples
│   └── setup.py                  # Setup and configuration script
│
├── config/                         # Configuration files
│   └── config.yaml                # System configuration
├── rubrics/                       # Assignment rubrics
├── ai_grading_results/            # AI grading outputs
├── tests/                         # Test suite
├── docs/                          # Documentation
└── examples/                      # Example configurations
```

## 🔒 Student Anonymization System

### Why Use Anonymization?

- **🎯 Bias-Free Grading**: Remove unconscious bias based on student names
- **🔐 Privacy Protection**: Secure student data during grading process
- **👥 Multiple Graders**: Enable blind grading by teaching assistants
- **📊 Fair Assessment**: Focus purely on content quality

### How It Works

```
Real Names → Anonymous IDs → Grading → Results → Name Revelation
Smith, John → STUDENT_1001 → 85% → STUDENT_1001: 85% → Smith, John: 85%
```

### Security Features

- **🔐 Encrypted Mappings**: All name mappings stored with password protection
- **📋 Anonymous Rosters**: Safe to share with graders (no real names)
- **🔓 Controlled Revelation**: Only instructors can reveal names after grading
- **🧹 Memory Management**: Sensitive data cleared after use

## 🎯 Grading Workflow Options

### Option A: Anonymous Grading (Recommended)

1. **📝 Notebook Preparation**: Standard format, structure parsing
2. **🔒 Anonymization**: Generate anonymous IDs, create secure mappings
3. **📊 Anonymous Grading**: Traditional + AI analysis with anonymous IDs
4. **📈 Anonymous Reports**: Review results without seeing real names
5. **🔓 Name Revelation**: Map results back to students after grading
6. **📤 Final Distribution**: Share results with real names

### Option B: Traditional Grading (Direct)

1. **📝 Notebook Preparation**: Standard format, structure parsing
2. **📊 Direct Grading**: Traditional + AI analysis with real names
3. **📈 Report Generation**: Immediate results with student names
4. **📤 Distribution**: Share results directly

### Workflow Components

#### Phase 1: Notebook Preparation
- **Rename notebooks** to standard format (`LastName_FirstName.ipynb`)
- **Parse structure** to identify problems and responses
- **Validate format** and extract metadata

#### Phase 2: Anonymization (Optional)
- **Generate anonymous IDs** (STUDENT_1001, STUDENT_1002, etc.)
- **Create encrypted mappings** with password protection
- **Export anonymous roster** for grader distribution

#### Phase 3: Traditional Grading
- **Completion analysis** using existing metrics
- **Missing answer detection** with detailed reports
- **Basic metrics** (code cells answered, text cells completed)

#### Phase 4: AI Content Grading  
- **Load assignment rubric** with specific criteria
- **Analyze student responses** using LLM
- **Generate detailed feedback** with suggestions
- **Flag uncertain grades** for manual review

#### Phase 5: Report Generation
- **Combined HTML report** showing both grading methods
- **Individual feedback files** for each student
- **Summary statistics** and class performance analysis
- **Flagged items report** for instructor review

#### Phase 6: Name Revelation (If Using Anonymization)
- **Secure mapping reload** with password verification
- **Results file processing** to add real names
- **Final report generation** with complete student information

## 📋 Rubric Configuration

### Creating Assignment Rubrics

Rubrics are defined in YAML format in the `rubrics/` directory. Here's an example:

```yaml
part_1:
  total_points: 30
  problem_statement: "From Exploration to Engineering"
  expected_response_type: "mixed"  # code, text, or mixed
  context: "Student should demonstrate understanding of IDA, EDA, and feature engineering"
  criteria:
    insight_quality:
      points: 15
      description: "Quality and depth of insights from IDA/EDA"
      guidelines: "Look for specific observations about data patterns, identification of problems"
    code_quality:
      points: 10
      description: "Quality of code implementation"
      guidelines: "Clean, well-commented code that runs without errors"
    visualization:
      points: 5
      description: "Quality and appropriateness of visualizations"
      guidelines: "Clear, properly labeled plots that support the analysis"
```

### Rubric Guidelines

- **Problem Statement**: Clear description of what students should accomplish
- **Expected Response Type**: Helps the AI understand what to look for
- **Context**: Additional background for the grading AI
- **Criteria**: Specific aspects to evaluate with point allocations
- **Guidelines**: Detailed instructions for consistent grading

## 🤖 LLM Integration

### Environment Variables (Recommended)

Create a `.env` file in the root directory for your API keys:
```bash
# .env file
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

**Note**: The `.env` file is automatically ignored by git for security.

### Supported Providers

1. **OpenAI GPT** (`provider: 'openai'`)
   - Models: gpt-4, gpt-3.5-turbo
   - Excellent for reasoning and code understanding
   - Requires OpenAI API key

2. **Anthropic Claude** (`provider: 'anthropic'`)
   - Models: claude-3-sonnet, claude-3-haiku
   - Strong analytical capabilities
   - Requires Anthropic API key

3. **Mock LLM** (`provider: 'mock'`)
   - For testing and development
   - No API key required
   - Generates realistic sample responses

### Configuration Example

```yaml
llm_settings:
  provider: 'openai'
  model: 'gpt-4'
  max_tokens: 1500
  temperature: 0.3
  api_key: 'sk-your-key-here'

grading_settings:
  confidence_threshold: 0.7
  auto_flag_low_confidence: true
  enable_detailed_feedback: true
  max_suggestions: 5
```

## 📊 Output Reports

### 1. Traditional Grading CSV
Basic completion metrics from your existing system:
- Student names and completion percentages
- Missing answer counts
- Final grades (0-4 scale)

### 2. AI Grading Results CSV
Detailed content-based scores:
- Problem-by-problem scores
- Confidence levels
- Flagged items indicator

### 3. Combined HTML Report
Interactive dashboard showing:
- Side-by-side comparison of both grading methods
- Expandable student sections
- Summary statistics
- Flagged items highlighting

### 4. Individual Feedback Files
Detailed reports for each student:
- Problem-by-problem breakdown
- Specific feedback and suggestions
- Areas for improvement
- Overall performance summary

### 5. Flagged Items Report
Items requiring manual review:
- Low confidence scores
- Validation issues
- Recommendations for instructor action

## 🛠️ Advanced Usage

### Custom Rubric Creation

1. **Copy the template**: Start with `rubrics/general_template.yaml`
2. **Modify criteria**: Adjust points and descriptions for your assignment
3. **Test with sample**: Run on a few notebooks to validate
4. **Refine guidelines**: Update based on AI grading results

### Batch Processing Multiple Assignments

```bash
# Process multiple assignments
for assignment in hw1 hw2 hw3; do
    python integrated_grader.py "Homework/${assignment}_renamed" $assignment --ai-grading
done
```

### Integration with Learning Management Systems

The CSV outputs can be imported into most LMS platforms:
- **Canvas**: Use the grade export format
- **Blackboard**: Compatible with grade center
- **Moodle**: Direct CSV import support

## 🔧 Troubleshooting

### Common Issues

**1. Setup and Installation**
```bash
# Test system setup
python examples/test_setup.py

# If import errors:
pip install -r requirements.txt

# If path issues:
python src/setup.py
```

**2. No notebooks found**
- Check directory path is correct: `ls Homework/HW02/`
- Ensure `.ipynb` files are present
- Verify file permissions
- Use absolute paths if relative paths fail

**3. Anonymization Issues**
```bash
# Check if anonymous session exists
cd src/utils
python student_id_cli.py list

# If mapping file not found:
python student_id_cli.py create your_assignment ../../your_notebook_dir/

# If password issues:
# Re-create session with new password
# Or check for typos in assignment_id
```

**4. AI grading fails**
- Check API key configuration in `.env` file
- Test with mock LLM first: set `provider: 'mock'` in config
- Verify internet connection
- Review rate limits for your LLM provider
- Check model availability (e.g., GPT-4 access)

**5. Rubric not found**
- Ensure rubric file exists: `ls rubrics/your_assignment.yaml`
- Check YAML syntax: `python -c "import yaml; yaml.safe_load(open('rubrics/your_assignment.yaml'))"`
- Verify assignment_id matches filename exactly
- Check file permissions

**6. Import/Module errors**
- Install required packages: `pip install -r requirements.txt`
- Check Python version: `python --version` (requires 3.8+)
- If relative import issues, run from project root directory
- For complex import errors, try the toy example first

**7. Permission/File Access Issues**
```bash
# Check file permissions
ls -la Homework/HW02/

# If permission denied:
chmod +r Homework/HW02/*.ipynb

# If directory doesn't exist:
mkdir -p student_mappings
mkdir -p ai_grading_results
```

**8. Anonymous ID Lookup Failures**
```bash
# Verify anonymous ID format
python student_id_cli.py reveal assignment_id --id STUDENT_1001

# If ID not found, check:
python student_id_cli.py reveal assignment_id  # Show all mappings

# If mapping corrupted, regenerate:
python student_id_cli.py create assignment_id notebook_dir/
```

### Debugging Tips

**Enable verbose logging**:
```yaml
system_settings:
  log_level: 'DEBUG'
```

**Test with mock LLM first**:
```yaml
llm_settings:
  provider: 'mock'
```

**Start with small batch**:
- Test with 2-3 notebooks initially
- Verify rubric configuration
- Check output quality before full batch

## 📈 Performance Optimization

### Cost Management (for paid LLMs)

1. **Batch similar problems** together
2. **Use appropriate models** (GPT-3.5 for simple tasks, GPT-4 for complex)
3. **Set reasonable token limits**
4. **Cache common responses** (future enhancement)

### Quality Assurance

1. **Regular calibration** with manual grading samples
2. **Monitor confidence scores** and adjust thresholds
3. **Review flagged items** to improve rubrics
4. **Student feedback** on AI-generated comments

## 🔮 Future Enhancements

### Planned Features

- **Interactive feedback**: Students can ask follow-up questions
- **Plagiarism detection**: Code similarity analysis
- **Adaptive rubrics**: Learning from grading patterns
- **Real-time grading**: As students work on assignments
- **Integration with IDEs**: Direct notebook feedback

### Extension Points

- **Custom LLM providers**: Add support for local models
- **Enhanced visualization analysis**: Image recognition for plots
- **Code execution sandbox**: Run and test student code
- **Peer comparison**: Anonymous benchmarking

## 📚 Complete Examples

### Example 1: Full Anonymous Grading Workflow

```bash
# === INITIAL SETUP (One Time) ===
pip install -r requirements.txt
python src/setup.py
python examples/test_setup.py

# Create .env file with your API keys
echo "OPENAI_API_KEY=your_key_here" > .env

# === ASSIGNMENT SETUP ===
# 1. Organize student notebooks in Homework/HW02/
# 2. Create rubric file: rubrics/hw2_data_analysis.yaml

# === ANONYMOUS GRADING WORKFLOW ===
# Step 1: Initialize anonymous session
cd src/utils
python student_id_cli.py create hw2_data_analysis ../../Homework/HW02/
# Enter secure password when prompted

# Step 2: Run grading with anonymous IDs
cd ../..
python main.py "Homework/HW02" hw2_data_analysis

# Step 3: Review anonymous results
# Files created: traditional_grades.csv, ai_grading_results/, combined_grading_report.html

# Step 4: Reveal names after grading complete
cd src/utils
python student_id_cli.py reveal hw2_data_analysis --results ../../traditional_grades.csv --output ../../final_grades.csv

# Step 5: Distribute final grades with real names
```

### Example 2: Quick Start (No Anonymization)

```bash
# Setup (first time only)
python src/setup.py

# Configure API keys in .env file
echo "OPENAI_API_KEY=your_key_here" > .env

# Grade homework directly with real names
python main.py "Homework/HW02" hw2_data_analysis
```

### Example 3: Testing and Development

```bash
# Test system setup
python examples/test_setup.py

# Try the toy example first
cd examples/toy_example
python simple_demo.py

# Test with mock LLM (no API key needed)
# Edit config/config.yaml: provider: 'mock'
python main.py "examples/toy_example/notebooks" toy_data_analysis

# Debug configuration
python main.py --debug-config

# Test LLM connection
python main.py --test-llm
```

### Example 4: Batch Processing Multiple Assignments

```bash
# Process multiple assignments with anonymization
for assignment in hw1_intro hw2_analysis hw3_modeling; do
    echo "Processing $assignment..."
    
    # Create anonymous session
    cd src/utils
    python student_id_cli.py create $assignment ../../Homework/${assignment}/
    
    # Grade anonymously
    cd ../..
    python main.py "Homework/${assignment}" $assignment
    
    # Reveal names
    cd src/utils
    python student_id_cli.py reveal $assignment --results ../../traditional_grades.csv --output ../../${assignment}_final.csv
    cd ../..
done
```

### Example 5: Working with Teaching Assistants

```bash
# === INSTRUCTOR SETUP ===
# 1. Create anonymous session
cd src/utils
python student_id_cli.py create midterm_exam ../../Exams/Midterm/

# 2. Share anonymous roster with TAs
# File: student_mappings/midterm_exam_anonymous_roster.csv

# === TA GRADING ===
# TAs grade using anonymous IDs (STUDENT_1001, STUDENT_1002, etc.)
# All grading results contain only anonymous identifiers

# === INSTRUCTOR FINAL STEP ===
# 3. After grading complete, instructor reveals names
python student_id_cli.py reveal midterm_exam --results ../../exam_grades.csv --output ../../final_exam_grades.csv
```

## 🤝 Contributing

### Adding New LLM Providers

1. **Inherit from `LLMInterface`**
2. **Implement required methods**
3. **Add to `LLMFactory`**
4. **Update configuration options**

### Improving Rubrics

1. **Test with diverse student responses**
2. **Collect instructor feedback**
3. **Iterate on guidelines and criteria**
4. **Share successful rubric patterns**

## 📄 License

This system extends your existing grading infrastructure. Please ensure compliance with your institution's policies regarding AI-assisted grading and student data privacy.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review generated log files
3. Test with mock LLM to isolate issues
4. Verify rubric configuration syntax

---

## 🎯 Summary: Complete Notebook Grading Solution

This system provides a comprehensive end-to-end solution for grading Jupyter notebooks:

### ✅ **What You Get**
- **🔒 Privacy-First**: Complete student anonymization with secure mapping
- **🤖 AI-Enhanced**: Intelligent content analysis with detailed feedback  
- **📊 Dual Assessment**: Traditional completion + AI content evaluation
- **📈 Rich Reports**: Interactive dashboards and detailed analytics
- **⚙️ Flexible Setup**: Works with or without API keys, multiple LLM providers
- **🔧 Production Ready**: Handles real classroom workflows and edge cases

### 🚀 **Getting Started**
1. **`python examples/test_setup.py`** - Verify installation
2. **`cd examples/toy_example && python simple_demo.py`** - Try the demo
3. **Follow the step-by-step guide above** for your real assignments

### 🔐 **Privacy & Security**
- Anonymous grading protects against bias
- Encrypted mappings secure student data  
- Teaching assistant support with blind grading
- Institutional compliance for educational use

---

**Important**: This system is designed to assist, not replace, instructor judgment. Always review AI-generated feedback before sharing with students, especially for items flagged for manual review. The anonymization features help ensure fair and unbiased assessment while maintaining complete privacy protection.