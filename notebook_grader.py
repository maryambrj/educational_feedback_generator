import nbformat
import sys
import os
import csv

def calculate_answered_percentage(notebook_path):
    """
    Calculates the percentage of answered code cells and markdown cells in a Jupyter notebook.
    
    Parameters:
    notebook_path (str): The path to the Jupyter notebook to be graded.
    
    Returns:
    tuple: A tuple containing the percentages of answered code cells, answered markdown cells, 
           the total percentage of answered cells, and a list of missing answers.
    """
    
    # Load the notebook
    with open(notebook_path, 'r', encoding='utf-8') as file:
        notebook = nbformat.read(file, as_version=4)
    
    # Initialize counters and tracking for missing answers
    total_code_cells = 0
    answered_code_cells = 0
    total_markdown_cells = 0
    answered_markdown_cells = 0
    missing_answers = []
    
    # Iterate through the cells to count the tagged answer cells and detect answers by content
    for i, cell in enumerate(notebook['cells']):
        if cell['cell_type'] == 'code':
            total_code_cells += 1
            # Consider a cell answered if it's tagged or contains code beyond comments
            if 'code answer' in cell.get('metadata', {}).get('tags', []) or \
               any(line.strip() for line in cell['source'].splitlines() if not line.strip().startswith('#')):
                answered_code_cells += 1
        
        elif cell['cell_type'] == 'markdown':
            total_markdown_cells += 1
            # Consider a markdown cell answered if:
            # 1. It's tagged as 'text answer'.
            # 2. It contains non-empty text after '✏️ **Answer:**' that is different from '*Put your answers here!*'.
            content_after_answer = cell['source'].split('✏️ **Answer:**', 1)[-1].strip() if '✏️ **Answer:**' in cell['source'] else cell['source'].strip()
            if 'text answer' in cell.get('metadata', {}).get('tags', []) and \
               content_after_answer and content_after_answer != "*Put your answers here!*":
                answered_markdown_cells += 1

        # Check for missing answers after a "task" cell
        if 'task' in cell.get('metadata', {}).get('tags', []):
            if i + 1 < len(notebook['cells']):
                next_cell = notebook['cells'][i + 1]
                if not ('code answer' in next_cell.get('metadata', {}).get('tags', []) or
                        'text answer' in next_cell.get('metadata', {}).get('tags', [])):
                    # Record the missing answer information with cell numbers
                    missing_answers.append({
                        'task_cell_number': i + 1,
                        'task_content': cell['source'].strip(),
                        'following_cell_number': i + 2,
                        'following_cell_content': next_cell['source'].strip(),
                        'following_cell_type': next_cell['cell_type']
                    })

    # Calculate percentages
    code_answered_percentage = (answered_code_cells / total_code_cells * 100) if total_code_cells > 0 else 0
    markdown_answered_percentage = (answered_markdown_cells / total_markdown_cells * 100) if total_markdown_cells > 0 else 0
    total_answered_percentage = ((answered_code_cells + answered_markdown_cells) / (total_code_cells + total_markdown_cells) * 100) if (total_code_cells + total_markdown_cells) > 0 else 0
    
    return code_answered_percentage, markdown_answered_percentage, total_answered_percentage, missing_answers

def grade_assignment(code_answered_percentage, markdown_answered_percentage):
    """
    Grades the assignment based on the answered percentages.
    
    Parameters:
    code_answered_percentage (float): The percentage of answered code cells.
    markdown_answered_percentage (float): The percentage of answered markdown cells.
    
    Returns:
    int: The final grade out of 4.
    """
    grade = 0
    if markdown_answered_percentage > 80:
        grade += 1
    if code_answered_percentage > 80:
        grade += 2
    if markdown_answered_percentage > 0 or code_answered_percentage > 0:
        grade += 1
    return grade

def create_individual_report(student_name, missing_answers, reports_directory):
    """
    Creates an individual missing answers report for a student.
    
    Parameters:
    student_name (str): Name of the student
    missing_answers (list): List of missing answer dictionaries
    reports_directory (str): Directory to save individual reports
    
    Returns:
    str: Path to the created report file
    """
    if not missing_answers:
        return None
    
    # Create a safe filename
    safe_filename = "".join(c for c in student_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    report_filename = f"{safe_filename}_missing_answers_report.txt"
    report_path = os.path.join(reports_directory, report_filename)
    
    with open(report_path, 'w', encoding='utf-8') as report_file:
        report_file.write("=" * 60 + "\n")
        report_file.write(f"MISSING ANSWERS REPORT FOR: {student_name}\n")
        report_file.write("=" * 60 + "\n\n")
        
        report_file.write(f"Total Missing Answers: {len(missing_answers)}\n")
        report_file.write(f"Report Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for idx, missing in enumerate(missing_answers, 1):
            report_file.write(f"MISSING ANSWER #{idx}\n")
            report_file.write("-" * 40 + "\n")
            report_file.write(f"Task Cell Number: {missing['task_cell_number']}\n")
            report_file.write(f"Expected Answer Cell Number: {missing['following_cell_number']}\n")
            report_file.write(f"Following Cell Type: {missing['following_cell_type']}\n\n")
            
            report_file.write("TASK CONTENT:\n")
            report_file.write("-" * 20 + "\n")
            report_file.write(f"{missing['task_content']}\n\n")
            
            report_file.write("CURRENT CONTENT IN FOLLOWING CELL:\n")
            report_file.write("-" * 20 + "\n")
            if missing['following_cell_content']:
                report_file.write(f"{missing['following_cell_content']}\n")
            else:
                report_file.write("[EMPTY CELL]\n")
            
            report_file.write("\n" + "=" * 60 + "\n\n")
        
        report_file.write("RECOMMENDATIONS:\n")
        report_file.write("-" * 20 + "\n")
        report_file.write("1. Review each task above and provide appropriate answers\n")
        report_file.write("2. Make sure answer cells are properly tagged with 'code answer' or 'text answer'\n")
        report_file.write("3. For text answers, use the format: ✏️ **Answer:** followed by your response\n")
        report_file.write("4. For code answers, write actual code (not just comments)\n")
    
    return report_path

def process_student_notebooks(directory_path, output_csv):
    """
    Processes all student notebooks in a directory and writes the grading results to a CSV file.
    Creates individual missing answers reports for each student.
    All output files are saved in the same directory as the notebooks.
    
    Parameters:
    directory_path (str): The path to the directory containing the student notebooks.
    output_csv (str): The path to the output CSV file.
    
    Returns:
    None
    """
    results = []
    reports_created = []
    
    # Save all output files in the same directory as the notebooks
    output_csv = os.path.join(directory_path, os.path.basename(output_csv))
    
    # Create reports directory within the notebooks directory
    reports_directory = os.path.join(directory_path, 'individual_reports')
    if not os.path.exists(reports_directory):
        os.makedirs(reports_directory)
        print(f"Created reports directory: {reports_directory}")
    
    # Get list of notebook files
    notebook_files = [f for f in os.listdir(directory_path) if f.endswith(".ipynb")]
    
    if not notebook_files:
        print(f"No Jupyter notebooks found in '{directory_path}'")
        return
    
    print(f"Processing {len(notebook_files)} notebook(s)...")
    print("-" * 50)
    
    for filename in notebook_files:
        print(f"Processing notebook: {filename}")
        
        notebook_path = os.path.join(directory_path, filename)
        student_name = filename.replace('.ipynb', '').replace('_', ' ')
        
        try:
            code_percentage, markdown_percentage, total_percentage, missing_answers = calculate_answered_percentage(notebook_path)
            grade = grade_assignment(code_percentage, markdown_percentage)
            
            # Add results to the main list
            results.append([
                student_name, 
                f"{code_percentage:.1f}", 
                f"{markdown_percentage:.1f}", 
                f"{total_percentage:.1f}", 
                grade,
                len(missing_answers)
            ])
            
            # Create individual report if there are missing answers
            if missing_answers:
                report_path = create_individual_report(student_name, missing_answers, reports_directory)
                if report_path:
                    reports_created.append((student_name, report_path))
                    print(f"  ✓ Created missing answers report: {os.path.basename(report_path)}")
                else:
                    print(f"  ! No missing answers report created for {student_name}")
            else:
                print(f"  ✓ No missing answers found")
            
            print(f"  → Grade: {grade}/4 (Code: {code_percentage:.1f}%, Text: {markdown_percentage:.1f}%)")
            
        except Exception as e:
            print(f"  ✗ Error processing {filename}: {e}")
            results.append([student_name, "ERROR", "ERROR", "ERROR", "ERROR", "ERROR"])
        
        print()
    
    # Write the main results to a CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([
            'Student Name', 
            'Code Cells Answered (%)', 
            'Markdown Cells Answered (%)', 
            'Total Answered (%)', 
            'Final Grade',
            'Missing Answers Count'
        ])
        csvwriter.writerows(results)
    
    # Create a summary report in the same directory
    summary_path = output_csv.replace('.csv', '_summary.txt')
    with open(summary_path, 'w', encoding='utf-8') as summary_file:
        summary_file.write("GRADING SUMMARY REPORT\n")
        summary_file.write("=" * 50 + "\n\n")
        summary_file.write(f"Total students processed: {len(results)}\n")
        summary_file.write(f"Individual reports created: {len(reports_created)}\n")
        summary_file.write(f"Main grades file: {output_csv}\n")
        summary_file.write(f"Reports directory: {reports_directory}\n\n")
        
        if reports_created:
            summary_file.write("INDIVIDUAL REPORTS CREATED:\n")
            summary_file.write("-" * 30 + "\n")
            for student_name, report_path in reports_created:
                summary_file.write(f"• {student_name}: {os.path.basename(report_path)}\n")
        else:
            summary_file.write("No individual reports were needed (all students completed their work perfectly!)\n")
    
    print("=" * 60)
    print("GRADING COMPLETE!")
    print("=" * 60)
    print(f"📊 Main results saved to: {output_csv}")
    print(f"📋 Summary report saved to: {summary_path}")
    print(f"📁 Individual reports directory: {reports_directory}")
    print(f"📈 Students processed: {len(results)}")
    print(f"📝 Individual reports created: {len(reports_created)}")
    
    if reports_created:
        print(f"\nStudents with missing answers:")
        for student_name, _ in reports_created:
            print(f"  • {student_name}")

if __name__ == "__main__":
    """
    This script processes all Jupyter notebooks in a directory, calculates the percentage of answered cells,
    assigns a grade based on the completion of code and markdown cells, and outputs the results to a CSV file.
    It also creates individual missing answers reports for each student who has incomplete work.

    Usage:
    python notebook_grader.py <directory_path> <output_csv>
    
    Arguments:
    <directory_path>: Path to the directory containing the student notebooks.
    <output_csv>: Path to the output CSV file where results will be saved.
    
    Example:
    python notebook_grader.py /path/to/student_notebooks/ results.csv
    
    Output:
    - results.csv: Main grading results
    - results_summary.txt: Summary of grading process
    - individual_reports/: Directory containing individual student reports
    """
    if len(sys.argv) != 3:
        print("Usage: python notebook_grader.py <directory_path> <output_csv>")
        print("\nExample: python notebook_grader.py Homework/HW01_renamed grades.csv")
        sys.exit(1)
    
    directory_path = sys.argv[1]
    output_csv = sys.argv[2]
    
    # Validate directory exists
    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' does not exist.")
        sys.exit(1)
    
    # Process the student notebooks and save results to CSV
    process_student_notebooks(directory_path, output_csv)