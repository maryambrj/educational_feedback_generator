# AI-Enhanced Notebook Grading System

An intelligent grading system that combines traditional completion-based grading with AI-powered content analysis for Jupyter notebooks. This system extends your existing grading pipeline to provide detailed feedback and content-quality assessment.

## 🚀 Quick Start

### 1. Setup the System
```bash
# First time setup - creates directories and configuration files
python integrated_grader.py --setup-ai

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure LLM (Optional)
Edit `config/config.yaml` to add your API keys:
```yaml
llm_settings:
  provider: 'openai'  # or 'anthropic' or 'mock'
  model: 'gpt-4'
  api_key: 'your_api_key_here'
```

### 3. Run Grading Pipeline
```bash
# Full pipeline: rename + traditional + AI grading
python integrated_grader.py "Homework/HW02" hw2_california_housing --rename-notebooks --ai-grading

# Traditional grading only
python integrated_grader.py "Homework/HW02_renamed" hw2_california_housing

# AI grading on pre-renamed notebooks
python integrated_grader.py "Homework/HW02_renamed" hw2_california_housing --ai-grading --no-rename
```

## 📁 System Architecture

### Core Components

1. **Notebook Parser**: Extracts structured content from student notebooks
2. **Rubric Manager**: Manages grading criteria and scoring systems
3. **LLM Grader**: Uses language models for content quality assessment
4. **Report Generator**: Creates comprehensive feedback reports

### File Structure
```
your_project/
├── ai_grader.py                    # Core AI grading system
├── integrated_grader.py            # Main pipeline script
├── setup_ai_grader.py             # Setup and configuration
├── rename_notebooks.py            # Your existing renaming script
├── notebook_grader.py    # Your existing grading script
├── config/
│   └── config.yaml                # System configuration
├── rubrics/
│   ├── hw2_california_housing.yaml # Assignment-specific rubrics
│   └── general_template.yaml      # Template for new assignments
├── ai_grading_results/            # AI grading outputs
│   ├── ai_grading_results.csv     # Summary scores
│   ├── detailed_feedback/         # Individual student reports
│   └── flagged_for_review.csv     # Items needing manual review
└── requirements.txt               # Python dependencies
```

## 🎯 Grading Workflow

### Phase 1: Notebook Preparation
- **Rename notebooks** to standard format (`LastName_FirstName.ipynb`)
- **Parse structure** to identify problems and responses
- **Validate format** and extract metadata

### Phase 2: Traditional Grading
- **Completion analysis** using your existing system
- **Missing answer detection** with detailed reports
- **Basic metrics** (code cells answered, text cells completed)

### Phase 3: AI Content Grading
- **Load assignment rubric** with specific criteria
- **Analyze student responses** using LLM
- **Generate detailed feedback** with suggestions
- **Flag uncertain grades** for manual review

### Phase 4: Report Generation
- **Combined HTML report** showing both grading methods
- **Individual feedback files** for each student
- **Summary statistics** and class performance analysis
- **Flagged items report** for instructor review

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

**1. No notebooks found**
- Check directory path is correct
- Ensure `.ipynb` files are present
- Verify file permissions

**2. AI grading fails**
- Check API key configuration
- Verify internet connection
- Review rate limits for your LLM provider

**3. Rubric not found**
- Ensure rubric file exists in `rubrics/` directory
- Check YAML syntax is valid
- Verify assignment_id matches filename

**4. Import errors**
- Install required packages: `pip install -r requirements.txt`
- Ensure all Python files are in the same directory
- Check Python version compatibility (3.7+)

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

## 📚 Examples

### Example 1: California Housing Assignment

```bash
# Setup (first time only)
python integrated_grader.py --setup-ai

# Configure for OpenAI GPT-4
# Edit config/config.yaml with your API key

# Grade homework submission
python integrated_grader.py \
    "Homework/HW02" \
    hw2_california_housing \
    --rename-notebooks \
    --ai-grading
```

**Expected Output:**
- `Homework/HW02_renamed/` with standardized notebook names
- `traditional_grades.csv` with completion scores
- `ai_grading_results/` with detailed AI feedback
- `combined_grading_report.html` with comprehensive analysis

### Example 2: Traditional Grading Only

```bash
# For instructors who want to try the system gradually
python integrated_grader.py \
    "Homework/HW02" \
    hw2_california_housing \
    --rename-notebooks

# This runs your existing grading pipeline with enhancements
```

### Example 3: AI Grading Existing Renamed Notebooks

```bash
# If you already have renamed notebooks
python integrated_grader.py \
    "Homework/HW02_renamed" \
    hw2_california_housing \
    --ai-grading \
    --no-rename
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

**Note**: This system is designed to assist, not replace, instructor judgment. Always review AI-generated feedback before sharing with students, especially for items flagged for manual review.