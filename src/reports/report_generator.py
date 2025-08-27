# report_generator.py
"""
Report generation functionality for AI grading results
"""

import os
import csv
from datetime import datetime
from typing import List, Dict, Tuple
from ..config.data_structures import GradingResult

class ReportGenerator:
    """Generates various reports from grading results"""
    
    def __init__(self, results: List[GradingResult]):
        self.results = results
    
    def export_results(self, output_directory: str):
        """Export grading results to CSV and detailed reports"""
        
        # Ensure output directory exists and is properly constructed
        os.makedirs(output_directory, exist_ok=True)
        
        # Export summary CSV
        csv_path = os.path.join(output_directory, 'ai_grading_results.csv')
        self.export_csv_summary(csv_path)
        
        # Export detailed feedback
        feedback_dir = os.path.join(output_directory, 'detailed_feedback')
        self.export_detailed_feedback(feedback_dir)
        
        # Export flagged items
        flagged_path = os.path.join(output_directory, 'flagged_for_review.csv')
        self.export_flagged_items(flagged_path)
        
        print(f"Results exported to: {output_directory}")
    
    def export_csv_summary(self, csv_path: str):
        """Export summary results to CSV"""
        
        # Ensure the directory for the CSV file exists
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Student Name', 'Problem ID', 'Total Score', 'Max Possible', 
                         'Percentage', 'Confidence', 'Flagged for Review']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in self.results:
                writer.writerow({
                    'Student Name': result.student_name,
                    'Problem ID': result.problem_id,
                    'Total Score': result.total_score,
                    'Max Possible': result.max_possible,
                    'Percentage': f"{result.percentage:.1f}%",
                    'Confidence': f"{result.confidence:.2f}",
                    'Flagged for Review': 'Yes' if result.flagged_for_review else 'No'
                })
    
    def export_detailed_feedback(self, feedback_directory: str):
        """Export detailed feedback for each student"""
        
        # Ensure the feedback directory exists
        os.makedirs(feedback_directory, exist_ok=True)
        
        # Group results by student
        student_results = {}
        for result in self.results:
            if result.student_name not in student_results:
                student_results[result.student_name] = []
            student_results[result.student_name].append(result)
        
        # Create feedback file for each student
        for student_name, results in student_results.items():
            safe_name = "".join(c for c in student_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            feedback_path = os.path.join(feedback_directory, f"{safe_name}_ai_feedback.txt")
            
            with open(feedback_path, 'w', encoding='utf-8') as f:
                f.write(f"AI Grading Feedback for: {student_name}\n")
                f.write("=" * 60 + "\n\n")
                
                total_score = sum(r.total_score for r in results)
                total_possible = sum(r.max_possible for r in results)
                overall_percentage = (total_score / total_possible * 100) if total_possible > 0 else 0
                
                f.write(f"Overall Score: {total_score}/{total_possible} ({overall_percentage:.1f}%)\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for result in results:
                    f.write(f"PROBLEM: {result.problem_id}\n")
                    f.write("-" * 30 + "\n")
                    f.write(f"Score: {result.total_score}/{result.max_possible} ({result.percentage:.1f}%)\n")
                    f.write(f"Confidence: {result.confidence:.2f}\n\n")
                    
                    f.write("DETAILED SCORES:\n")
                    for criterion, score in result.scores.items():
                        f.write(f"  {criterion}: {score}\n")
                    f.write("\n")
                    
                    f.write("FEEDBACK:\n")
                    f.write(f"{result.feedback}\n\n")
                    
                    if result.suggestions:
                        f.write("SUGGESTIONS FOR IMPROVEMENT:\n")
                        for i, suggestion in enumerate(result.suggestions, 1):
                            f.write(f"{i}. {suggestion}\n")
                        f.write("\n")
                    
                    if result.flagged_for_review:
                        f.write("⚠️  FLAGGED FOR INSTRUCTOR REVIEW\n")
                    
                    f.write("=" * 60 + "\n\n")
    
    def export_flagged_items(self, csv_path: str):
        """Export items flagged for review"""
        
        flagged_results = [r for r in self.results if r.flagged_for_review]
        
        if not flagged_results:
            return
        
        # Ensure the directory for the CSV file exists
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Student Name', 'Problem ID', 'Confidence', 'Reason', 'Feedback']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in flagged_results:
                reason = "Low confidence" if result.confidence < 0.7 else "Score validation issue"
                writer.writerow({
                    'Student Name': result.student_name,
                    'Problem ID': result.problem_id,
                    'Confidence': f"{result.confidence:.2f}",
                    'Reason': reason,
                    'Feedback': result.feedback[:100] + "..." if len(result.feedback) > 100 else result.feedback
                })

def create_combined_report(directory_path: str, traditional_csv: str, 
                         ai_results: Dict, assignment_id: str, mode: str = "homework"):
    """Create a combined HTML report showing both traditional and AI grading"""
    
    # Load ICAs results
    traditional_results = {}
    traditional_csv_path = os.path.join(directory_path, os.path.basename(traditional_csv))
    
    if os.path.exists(traditional_csv_path):
        with open(traditional_csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                traditional_results[row['Student Name']] = row
    
    # Create HTML report
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Combined Grading Report - {assignment_id}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .card h3 {{
            margin-top: 0;
            color: #2c3e50;
        }}
        .student-section {{
            background: white;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .student-header {{
            background-color: #34495e;
            color: white;
            padding: 15px 20px;
            border-radius: 8px 8px 0 0;
            cursor: pointer;
        }}
        .student-content {{
            padding: 20px;
            display: none;
        }}
        .student-content.active {{
            display: block;
        }}
        .grade-comparison {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}
        .traditional-grade, .ai-grade {{
            padding: 15px;
            border-radius: 8px;
        }}
        .traditional-grade {{
            background-color: #e8f4f8;
            border-left: 4px solid #3498db;
        }}
        .ai-grade {{
            background-color: #e8f6e8;
            border-left: 4px solid #27ae60;
        }}
        .flagged {{
            background-color: #fdf2e9;
            border-left: 4px solid #e67e22;
            padding: 10px;
            margin: 10px 0;
            border-radius: 4px;
        }}
        .feedback {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
        }}
        .suggestions {{
            background-color: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            margin-top: 10px;
        }}
        .metric {{
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        }}
        .metric-label {{
            font-size: 14px;
            color: #7f8c8d;
            margin-top: 5px;
        }}
        .toggle-btn {{
            float: right;
            background: none;
            border: none;
            color: white;
            font-size: 18px;
        }}
    </style>
    <script>
        function toggleStudent(studentId) {{
            const content = document.getElementById('content-' + studentId);
            const btn = document.getElementById('btn-' + studentId);
            
            if (content.classList.contains('active')) {{
                content.classList.remove('active');
                btn.textContent = '+';
            }} else {{
                content.classList.add('active');
                btn.textContent = '-';
            }}
        }}
    </script>
</head>
<body>
    <div class="header">
        <h1>Combined Grading Report</h1>
        <p>Assignment: {assignment_id}</p>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
"""
    
    # Calculate summary statistics
    total_students = len(ai_results)
    flagged_students = sum(1 for results in ai_results.values() 
                          for result in results if result.flagged_for_review)
    
    # Add summary cards
    html_content += f"""
    <div class="summary-cards">
        <div class="card">
            <h3>Total Students</h3>
            <div class="metric">{total_students}</div>
            <div class="metric-label">Notebooks Processed</div>
        </div>
        <div class="card">
            <h3>AI Grading Complete</h3>
            <div class="metric">{len([r for r in ai_results.values() if r])}</div>
            <div class="metric-label">Successfully Graded</div>
        </div>
        <div class="card">
            <h3>Flagged for Review</h3>
            <div class="metric">{flagged_students}</div>
            <div class="metric-label">Need Manual Check</div>
        </div>
        <div class="card">
            <h3>Grading Methods</h3>"""
    
    # Add grading method info based on mode
    if mode == 'ica':
        html_content += f"""
            <div class="metric-label">Traditional: Completion-based</div>
            <div class="metric-label">AI: Content-based</div>"""
    else:  # homework mode
        html_content += f"""
            <div class="metric-label">AI: Content-based with rubric</div>"""
    
    html_content += f"""
        </div>
    </div>
"""
    
    # Add student sections
    student_id = 0
    for notebook_file, ai_student_results in ai_results.items():
        if not ai_student_results:
            continue
            
        student_name = ai_student_results[0].student_id
        student_id += 1
        
        # Get ICAs data
        traditional_data = traditional_results.get(student_name, {})
        
        html_content += f"""
    <div class="student-section">
        <div class="student-header" onclick="toggleStudent({student_id})">
            <h3>{student_name}
                <button class="toggle-btn" id="btn-{student_id}">+</button>
            </h3>
        </div>
        <div class="student-content" id="content-{student_id}">
            <div class="grade-comparison">"""
        
        # Add traditional grade section only for ICA mode
        if mode == 'ica':
            html_content += f"""
                <div class="traditional-grade">
                    <h4>ICAs (Completion)</h4>
                    <p><strong>Final Grade:</strong> {traditional_data.get('Final Grade', 'N/A')}/4</p>
                    <p><strong>Code Cells:</strong> {traditional_data.get('Code Cells Answered (%)', 'N/A')}</p>
                    <p><strong>Text Cells:</strong> {traditional_data.get('Markdown Cells Answered (%)', 'N/A')}</p>
                    <p><strong>Total Answered:</strong> {traditional_data.get('Total Answered (%)', 'N/A')}</p>
                    <p><strong>Missing Answers:</strong> {traditional_data.get('Missing Answers Count', 'N/A')}</p>
                </div>"""
        
        html_content += f"""
                <div class="ai-grade">
                    <h4>AI Grading (Content Quality)</h4>
"""
        
        # Calculate AI totals
        total_ai_score = sum(result.total_score for result in ai_student_results)
        total_ai_possible = sum(result.max_possible for result in ai_student_results)
        avg_confidence = sum(result.confidence for result in ai_student_results) / len(ai_student_results)
        
        html_content += f"""
                    <p><strong>Total Score:</strong> {total_ai_score:.1f}/{total_ai_possible} ({(total_ai_score/total_ai_possible*100):.1f}%)</p>
                    <p><strong>Average Confidence:</strong> {avg_confidence:.2f}</p>
                    <p><strong>Problems Graded:</strong> {len(ai_student_results)}</p>
                </div>
            </div>
"""
        
        # Show flagged items
        flagged_items = [r for r in ai_student_results if r.flagged_for_review]
        if flagged_items:
            html_content += f"""
            <div class="flagged">
                <strong>⚠️ Flagged for Review:</strong> {len(flagged_items)} problem(s) need manual verification
            </div>
"""
        
        # Add detailed AI results for each problem
        for result in ai_student_results:
            html_content += f"""
            <h4>Problem: {result.problem_id}</h4>
            <p><strong>Score:</strong> {result.total_score}/{result.max_possible} ({result.percentage:.1f}%) | 
               <strong>Confidence:</strong> {result.confidence:.2f}</p>
            
            <div class="feedback">
                <strong>AI Feedback:</strong><br>
                {result.feedback}
            </div>
"""
            
            if result.suggestions:
                html_content += f"""
            <div class="suggestions">
                <strong>Suggestions for Improvement:</strong>
                <ul>
"""
                for suggestion in result.suggestions:
                    html_content += f"<li>{suggestion}</li>"
                html_content += """
                </ul>
            </div>
"""
        
        html_content += """
        </div>
    </div>
"""
    
    html_content += """
</body>
</html>
"""
    
    # Save HTML report
    report_path = os.path.join(directory_path, 'combined_grading_report.html')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)