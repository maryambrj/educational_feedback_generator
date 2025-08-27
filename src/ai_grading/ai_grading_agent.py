# ai_grading_agent.py
"""
Main AI Grading Agent that coordinates all components
"""

import os
from typing import List, Dict
from ..config.data_structures import GradingResult
from ..core.notebook_parser import NotebookParser
from ..reports.rubric_manager import RubricManager
from .llm_grader import LLMGrader
from ..reports.report_generator import ReportGenerator
from .llm_interface import LLMInterface

class AIGradingAgent:
    """Main coordinating class for the AI grading system"""
    
    def __init__(self, llm_interface: LLMInterface, rubrics_directory: str = "rubrics"):
        self.parser = NotebookParser()
        self.rubric_manager = RubricManager(rubrics_directory)
        self.grader = LLMGrader(llm_interface)
        self.results = []
    
    def grade_notebook(self, notebook_path: str, assignment_id: str) -> List[GradingResult]:
        """Grade a single notebook"""
        
        print(f"Grading notebook: {notebook_path}")
        
        # Parse notebook
        parsed_content = self.parser.parse_notebook(notebook_path)
        student_name = parsed_content['student_name']
        
        # Load rubric
        assignment_rubric = self.rubric_manager.load_assignment_rubric(assignment_id)
        
        # Grade each response
        notebook_results = []
        
        for response in parsed_content['responses']:
            if response.problem_id in assignment_rubric:
                rubric = assignment_rubric[response.problem_id]
                
                # Add assignment context
                context = f"Assignment: {assignment_id}"
                
                result = self.grader.grade_response(response, rubric, context)
                result.student_id = student_name
                
                notebook_results.append(result)
                print(f"  Graded {response.problem_id}: {result.total_score}/{result.max_possible} ({result.percentage:.1f}%)")
            else:
                print(f"  Warning: No rubric found for {response.problem_id}")
        
        self.results.extend(notebook_results)
        return notebook_results
    
    def grade_directory(self, directory_path: str, assignment_id: str) -> Dict[str, List[GradingResult]]:
        """Grade all notebooks in a directory"""
        
        print(f"Starting AI grading for assignment: {assignment_id}")
        print(f"Directory: {directory_path}")
        
        # Ensure directory_path is clean and valid
        directory_path = os.path.normpath(directory_path)
        if not os.path.isdir(directory_path):
            print(f"Error: {directory_path} is not a valid directory")
            return {}
        
        # Find all notebook files
        notebook_files = [f for f in os.listdir(directory_path) if f.endswith('.ipynb')]
        
        if not notebook_files:
            print("No notebook files found!")
            return {}
        
        print(f"Found {len(notebook_files)} notebooks to grade")
        
        all_results = {}
        
        for notebook_file in notebook_files:
            notebook_path = os.path.join(directory_path, notebook_file)
            
            # Double-check that this is actually a jupyter notebook
            if not notebook_path.endswith('.ipynb'):
                print(f"Skipping {notebook_path} - not a Jupyter notebook")
                continue

            try:
                results = self.grade_notebook(notebook_path, assignment_id)
                all_results[notebook_file] = results
            except Exception as e:
                print(f"Error grading {notebook_file}: {e}")
                all_results[notebook_file] = []
        
        return all_results
    
    def export_results(self, output_directory: str):
        """Export grading results using the report generator"""
        
        report_generator = ReportGenerator(self.results)
        report_generator.export_results(output_directory)
    
    def get_grading_summary(self) -> Dict:
        """Get summary statistics of grading results"""
        
        if not self.results:
            return {
                'total_graded': 0,
                'average_score': 0,
                'flagged_count': 0,
                'confidence_avg': 0
            }
        
        total_score = sum(r.total_score for r in self.results)
        total_possible = sum(r.max_possible for r in self.results)
        flagged_count = sum(1 for r in self.results if r.flagged_for_review)
        avg_confidence = sum(r.confidence for r in self.results) / len(self.results)
        
        return {
            'total_graded': len(self.results),
            'average_score': (total_score / total_possible * 100) if total_possible > 0 else 0,
            'flagged_count': flagged_count,
            'confidence_avg': avg_confidence,
            'total_score': total_score,
            'total_possible': total_possible
        }
    
    def clear_results(self):
        """Clear stored results (useful for grading multiple assignments)"""
        self.results = []
        self.grader.grading_history = []