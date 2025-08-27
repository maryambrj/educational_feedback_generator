# AI-Enhanced Notebook Grading System

An intelligent grading system that supports two grading modes:
- **ICA Mode**: Simple completion-based grading (did student write something?)
- **Homework Mode**: Full AI-powered content analysis with rubrics

Features student anonymization, modular LLM configuration, and comprehensive feedback generation.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure API keys (create .env file)
echo "OPENAI_API_KEY=your_key_here" > .env

# 3. Initialize system
python src/setup.py

# 4. Test installation
python examples/toy_example/run_toy_example.py
```

## 📝 Usage

**Important**: Run all commands from the project root directory.

### ICA Grading (Completion Only)
```bash
python grade_notebooks.py "Homework/ICA01" ica01 --mode ica
```
- No rubric required
- Fast completion-based scoring

### Homework Grading (AI Analysis)
```bash
python grade_notebooks.py "Homework/HW01" hw1_assignment --mode homework
```
- Requires rubric file: `rubrics/hw1_assignment.yaml`
- AI-powered content analysis
- **Note**: If AI grading fails, no partial completion grades are generated

### With Anonymization
```bash
# 1. Create anonymous session
python src/utils/student_id_cli.py create hw1_assignment Homework/HW01/

# 2. Grade with anonymous IDs
python grade_notebooks.py "Homework/HW01" hw1_assignment --mode homework

# 3. Reveal names after grading
python src/utils/student_id_cli.py reveal hw1_assignment --results traditional_grades.csv --output final_grades.csv
```

## 🔄 Multi-Run Grading (Advanced)

For research or reliability purposes, you can run the same grading task 5 times with different models and compare results.

### Quick Start
```bash
# Run grading 5 times with different models
python multi_run_grader.py "Homework/HW01" hw1_assignment
```

### 🎯 Configure Models (One File Only)
Edit `config/multi_run_config.yaml` to change all 5 models:

```yaml
multi_run_grading:
  enabled: true
  runs:
    - name: "GPT-4"
      provider: "openai"
      model: "gpt-4"
      temperature: 0.3
      
    - name: "GPT-4-Turbo"
      provider: "openai"
      model: "gpt-4-turbo-preview"
      temperature: 0.3
      
    - name: "GPT-3.5-Turbo"
      provider: "openai"
      model: "gpt-3.5-turbo"
      temperature: 0.3
      
    - name: "Claude-3-Sonnet"
      provider: "anthropic"
      model: "claude-3-sonnet-20240229"
      temperature: 0.3
      
    - name: "GPT-4-Creative"
      provider: "openai"
      model: "gpt-4"
      temperature: 0.7

# Analysis settings
aggregation:
  flag_high_variance: true
  variance_threshold: 15  # Flag if scores vary by >15 points
```

### 📊 What You Get

**Single Final Result**: One consolidated output with averaged scores and merged feedback

```
Homework/HW01/ai_grading_results/
├── ai_grading_results.csv          # Final grades (averaged from 5 models)
├── detailed_feedback/               # Merged feedback files
│   ├── student1_ai_feedback.txt    # Combined feedback from all models
│   └── student2_ai_feedback.txt
├── flagged_for_review.csv           # High-variance problems
└── combined_grading_report.html     # Standard HTML report
```

**Averaged Results**: 
- **Scores**: Average of all 5 model scores for each problem
- **Confidence**: Average confidence across all models
- **Feedback**: Merged and summarized from all model responses
- **Suggestions**: Unique suggestions from all models combined
- **Variance Flagging**: Problems where models disagree significantly

### 🔍 Example Final Output

**ai_grading_results.csv:**
| Student | Problem | Total Score | Percentage | Confidence | Flagged |
|---------|---------|-------------|------------|------------|---------|
| John    | part_1  | 8.2         | 82.0%      | 0.87       | No      |
| John    | part_2  | 6.8         | 68.0%      | 0.73       | Yes*    |

*Flagged due to high variance between models (>15 points difference)

### 🎯 Use Cases

- **Research**: Compare model performance and consistency
- **Quality Assurance**: Identify problematic submissions where models disagree  
- **Model Selection**: Determine which models work best for your assignment types
- **Reliability**: Get more robust grading through multiple model consensus

### 📝 Tips

1. **Model Selection**: Mix different model families (GPT vs Claude) for diversity
2. **Temperature Variation**: Use different temperatures (0.1-0.7) for the same model
3. **High Variance**: Problems with >15 point variance typically need manual review
4. **Cost Management**: Multi-run uses 5x API calls - monitor usage

### Option A: Anonymous Grading (Recommended)

#### For Homework Assignments
**Step 1: Create Assignment Structure**
```bash
# Ensure you're in the project root directory
cd /path/to/your/AI-Grader

# Organize notebooks in directory
mkdir -p Homework/HW01
# Place notebooks as: LastName_FirstName.ipynb
```

**Step 2: Create Rubric**
```bash
# Create rubric file: rubrics/hw1_assignment.yaml
```

**Step 3: Initialize Anonymous Session**
```bash
python src/utils/student_id_cli.py create hw1_assignment Homework/HW01/
# Enter secure password when prompted
```

**Step 4: Run Grading**
```bash
python grade_notebooks.py "Homework/HW01" hw1_assignment --mode homework
```

**Step 5: Reveal Names (After Grading)**
```bash
python src/utils/student_id_cli.py reveal hw1_assignment --results traditional_grades.csv --output final_grades.csv
```

#### For ICA Assignments
**Step 1: Create Assignment Structure**
```bash
# Organize ICA notebooks in directory
mkdir -p Homework/ICA01
# Place notebooks as: LastName_FirstName.ipynb
```

**Step 2: Initialize Anonymous Session**
```bash
python src/utils/student_id_cli.py create ica01 Homework/ICA01/
# Enter secure password when prompted
```

**Step 3: Run ICA Grading**
```bash
python grade_notebooks.py "Homework/ICA01" ica01 --mode ica
# No rubric needed - only checks completion
```

**Step 4: Reveal Names (After Grading)**
```bash
python src/utils/student_id_cli.py reveal ica01 --results traditional_grades.csv --output ica01_final.csv
```

### Option B: Direct Grading (No Anonymization)
```bash
# Homework grading with AI analysis
python grade_notebooks.py "Homework/HW01" hw1_assignment --mode homework

# ICA grading (completion-only)  
python grade_notebooks.py "Homework/ICA01" ica01 --mode ica
```

## 🎯 Command Reference

### Main Grading Command
```bash
python grade_notebooks.py <notebook_directory> <assignment_id> [--mode {ica|homework}] [--debug]
```
- `notebook_directory`: Path to student notebooks
- `assignment_id`: Identifier for the assignment
- `--mode`: Grading mode (default: homework)
  - `ica`: Completion-based grading only (no rubric needed)
  - `homework`: Full AI analysis with rubric (rubric required)
- `--debug`: Enable debug output

### Anonymization Commands
```bash
# Create anonymous session
python src/utils/student_id_cli.py create <assignment_id> <notebook_directory>

# Reveal all mappings
python src/utils/student_id_cli.py reveal <assignment_id>

# Reveal with specific results file
python src/utils/student_id_cli.py reveal <assignment_id> --results <csv_file> --output <output_file>

# Look up specific student
python src/utils/student_id_cli.py reveal <assignment_id> --id STUDENT_1001

# List all sessions
python src/utils/student_id_cli.py list
```

## 📊 Rubric Configuration

Create `rubrics/<assignment_id>.yaml`:
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

## ⚙️ Configuration

### LLM Providers
Edit `config/config.yaml`:
```yaml
llm_settings:
  provider: 'openai'        # openai, anthropic, or mock
  model: 'gpt-4'            # gpt-4, gpt-3.5-turbo, claude-3-sonnet
  max_tokens: 1500
  temperature: 0.3
  api_key: 'your_key_here'  # or use .env file

grading_settings:
  confidence_threshold: 0.7
  auto_flag_low_confidence: true
  enable_detailed_feedback: true
```

## 📁 Output Files

### After Grading
```
├── traditional_grades.csv              # ICA completion scores
├── ai_grading_results/                 # AI feedback and scores
│   ├── ai_grading_results.csv         # Detailed AI scores
│   ├── detailed_feedback/             # Individual feedback files
│   └── flagged_for_review.csv         # Items needing manual review
└── combined_grading_report.html        # Interactive dashboard
```

### After Name Revelation (Anonymous Mode)
```
├── final_grades.csv                    # Results with real names
└── student_mappings/                   # Anonymous session files
    ├── <assignment>_mapping.json      # Encrypted mappings
    ├── <assignment>_anonymous_roster.csv
    └── <assignment>_name_reveal.csv
```

## 🔧 Common Workflows

### Batch Processing
```bash
# Homework assignments
for assignment in hw1 hw2 hw3; do
    python src/utils/student_id_cli.py create $assignment Homework/$assignment/
    python grade_notebooks.py "Homework/$assignment" $assignment --mode homework
    python src/utils/student_id_cli.py reveal $assignment --results traditional_grades.csv --output ${assignment}_final.csv
done

# ICA assignments
for ica in ica1 ica2 ica3; do
    python src/utils/student_id_cli.py create $ica Homework/$ica/
    python grade_notebooks.py "Homework/$ica" $ica --mode ica
    python src/utils/student_id_cli.py reveal $ica --results traditional_grades.csv --output ${ica}_final.csv
done
```

### Teaching Assistant Workflow
```bash
# Instructor: Create anonymous session
python src/utils/student_id_cli.py create midterm Exams/Midterm/

# Share anonymous roster with TAs: student_mappings/midterm_anonymous_roster.csv
# TAs grade using anonymous IDs

# Instructor: Reveal names after grading
python src/utils/student_id_cli.py reveal midterm --results exam_grades.csv --output final_exam_grades.csv
```

## 🚨 Troubleshooting

### Common Issues
```bash
# Wrong directory error (double src path)
pwd  # Should show /path/to/AI-Grader, not /path/to/AI-Grader/src
cd /path/to/your/AI-Grader  # Navigate to project root

# No notebooks found
ls "Homework/HW01/"  # Verify .ipynb files exist

# Rubric not found (homework mode only)
ls rubrics/hw1_assignment.yaml  # Check filename matches assignment_id

# AI grading issues - try debug mode:
python grade_notebooks.py "Homework/HW01" hw1 --mode homework --debug
python examples/toy_example/run_toy_example.py  # Test AI functionality

# Import errors
python src/setup.py  # Reinitialize system
```

### Debug Commands
```bash
# Test system configuration
python examples/test_setup.py

# Debug AI configuration
python src/core/main_ai_grader.py --debug-config

# Verify anonymization
python src/utils/student_id_cli.py list
```

## 🎯 Key Features

- **🎯 Two Grading Modes**: ICA (completion-based) vs Homework (AI analysis)
- **🔒 Student Anonymization**: Complete privacy protection with encrypted mappings
- **🤖 AI Content Analysis**: Intelligent feedback using GPT-4, Claude, or other LLMs  
- **📊 Flexible Assessment**: Simple completion checks or detailed rubric analysis
- **📈 Rich Reports**: Interactive HTML dashboards and detailed CSV exports
- **⚙️ Flexible Setup**: Works with/without API keys, multiple LLM providers
- **👥 Multi-Grader Support**: Anonymous grading for teaching assistants

## 📚 Examples

### Complete Anonymous Homework Workflow
```bash
# 1. Setup
pip install -r requirements.txt
python src/setup.py

# 2. Create rubric: rubrics/hw2_analysis.yaml

# 3. Initialize anonymous grading
python src/utils/student_id_cli.py create hw2_analysis Homework/HW02/

# 4. Grade anonymously
python grade_notebooks.py "Homework/HW02" hw2_analysis --mode homework

# 5. Review results (anonymous)
open combined_grading_report.html

# 6. Reveal names
python src/utils/student_id_cli.py reveal hw2_analysis --results traditional_grades.csv --output final_grades.csv
```

### Complete Anonymous ICA Workflow
```bash
# 1. Setup (same as above)
pip install -r requirements.txt
python src/setup.py

# 2. No rubric needed for ICAs

# 3. Initialize anonymous grading
python src/utils/student_id_cli.py create ica03 Homework/ICA03/

# 4. Grade anonymously (completion-only)
python grade_notebooks.py "Homework/ICA03" ica03 --mode ica

# 5. Review results (anonymous)
cat traditional_grades.csv

# 6. Reveal names
python src/utils/student_id_cli.py reveal ica03 --results traditional_grades.csv --output ica03_final.csv
```

### Quick Direct Grading
```bash
# Setup and grade immediately (no anonymization)

# For homework (detailed analysis)
python grade_notebooks.py "Homework/HW02" hw2_analysis --mode homework
open combined_grading_report.html

# For ICA (completion check only)
python grade_notebooks.py "Homework/ICA02" ica02 --mode ica
```

---

**Important**: Always review AI-generated feedback before sharing with students, especially items flagged for manual review. The anonymization features ensure fair and unbiased assessment while maintaining privacy protection.