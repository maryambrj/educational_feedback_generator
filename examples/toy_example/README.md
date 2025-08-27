# 🎯 AI Grader Toy Example

This directory contains a complete toy example that demonstrates the entire AI grading workflow using sample notebooks and mock data.

## 📁 What's Included

### 📊 Sample Data
- **`sample_data.py`**: Script to generate realistic student dataset
- **`student_data.csv`**: Sample dataset with 100 student records
- **Columns**: student_id, age, study_hours, gpa, attendance, assignment_score

### 📓 Sample Notebooks
- **`Student_A_Good_Answers.ipynb`**: Complete, high-quality submission
- **`Student_B_Incomplete_Answers.ipynb`**: Partial submission with some missing work
- **`Student_C_No_Answers.ipynb`**: Minimal submission with mostly missing work

### 🎯 Rubric
- **`toy_data_analysis.yaml`**: Comprehensive grading rubric with 3 parts
- **Total Points**: 100 (40 + 35 + 25)
- **Criteria**: Data loading, exploration, visualization, analysis, and summary

### 🚀 Test Runner
- **`run_toy_example.py`**: Complete workflow demonstration
- **`run_toy_example.py`**: Simple runner from root directory

## 🎮 How to Run

### Option 1: From Root Directory (Recommended)
```bash
# From the AI-Grader root directory
python tests/run_toy_example.py
```

### Option 2: From Toy Example Directory
```bash
# Navigate to toy example directory
cd tests/toy_example

# Run the example
python run_toy_example.py
```

## 🔄 What Happens

1. **📊 Data Generation**: Creates realistic student dataset
2. **📝 ICAs**: Runs completion-based grading
3. **🤖 AI Grading**: Uses mock LLM for content analysis
4. **📊 Combined Report**: Generates comprehensive HTML report
5. **📁 Output Files**: Saves all results for inspection

## 📊 Expected Results

### ICAs
- **Student A**: High completion rate, good grade
- **Student B**: Medium completion rate, moderate grade
- **Student C**: Low completion rate, poor grade

### AI Grading (Mock)
- **Student A**: 85/100 - Excellent comprehensive analysis
- **Student B**: 45/100 - Good start but incomplete
- **Student C**: 10/100 - Minimal work completed

### Missing Answer Detection
The system will automatically detect:
- Missing code cells after task cells
- Incomplete text answers
- Unanswered questions

## 🎯 Learning Objectives

This toy example demonstrates:
- ✅ **ICAs**: Completion-based assessment
- ✅ **AI Grading**: Content quality analysis
- ✅ **Rubric Management**: Structured grading criteria
- ✅ **Report Generation**: Comprehensive feedback
- ✅ **Missing Answer Detection**: Automatic problem identification
- ✅ **Different Performance Levels**: Various student submission qualities

## 🔧 Customization

### Modify the Rubric
Edit `toy_data_analysis.yaml` to:
- Change point allocations
- Add new criteria
- Modify grading guidelines

### Add More Students
Create additional notebooks in the `notebooks/` directory:
- Follow the same naming convention
- Include proper cell tags (`task`, `code answer`, `text answer`)
- Vary the quality and completeness

### Use Real LLM
Replace mock LLM with real API:
1. Update `.env` file with your API keys
2. Modify `run_toy_example.py` to use real LLM
3. Experience actual AI-powered grading

## 🚨 Troubleshooting

### Common Issues
1. **Import Errors**: Ensure you're running from the correct directory
2. **Missing Dependencies**: Install requirements with `pip install -r requirements.txt`
3. **File Permissions**: Check that you can write to the output directories

### Debug Mode
The system includes comprehensive error handling and will show:
- Detailed error messages
- Stack traces for debugging
- Step-by-step progress updates

## 📚 Next Steps

After running the toy example:
1. **Examine Outputs**: Review generated reports and CSV files
2. **Understand Workflow**: See how traditional and AI grading complement each other
3. **Customize**: Modify rubrics and criteria for your own assignments
4. **Scale Up**: Apply to real student submissions
5. **Real LLM**: Replace mock responses with actual AI analysis

## 🎉 Success Indicators

You'll know the toy example worked when you see:
- ✅ Sample dataset generated
- ✅ ICAs completed with results
- ✅ AI grading completed (mock responses)
- ✅ Combined report generated
- ✅ All output files created successfully
- ✅ Summary displayed with next steps

---

**Happy Testing! 🚀**

This toy example gives you a complete understanding of the AI grading system's capabilities and workflow.
