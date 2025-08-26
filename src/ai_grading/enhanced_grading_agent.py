# enhanced_grading_agent.py
"""
Enhanced AI Grading Agent that incorporates reference solutions for better grading
"""

import os
from typing import List, Dict, Optional
from ..config.data_structures import GradingResult
from ..core.notebook_parser import NotebookParser
from ..reports.rubric_manager import RubricManager
from llm_grader import LLMGrader
from report_generator import ReportGenerator
from solution_generator import SolutionGenerator, ProblemSolution
from .llm_interface import LLMInterface

class EnhancedAIGradingAgent:
    """Enhanced grading agent that uses reference solutions for improved assessment"""
    
    def __init__(self, llm_interface: LLMInterface, rubrics_directory: str = "rubrics",
                 use_reference_solutions: bool = True):
        self.parser = NotebookParser()
        self.rubric_manager = RubricManager(rubrics_directory)
        self.grader = LLMGrader(llm_interface)
        self.solution_generator = SolutionGenerator(llm_interface, temperature=0.7) if use_reference_solutions else None
        self.report_generator = None
        self.results = []
        self.reference_solutions = {}
        self.use_reference_solutions = use_reference_solutions
    
    def generate_reference_solutions(self, assignment_id: str) -> Dict[str, ProblemSolution]:
        """Generate reference solutions for the assignment"""
        
        if not self.use_reference_solutions or not self.solution_generator:
            print("Reference solution generation is disabled")
            return {}
        
        print(f"🧠 Generating reference solutions for {assignment_id}...")
        
        solutions = self.solution_generator.generate_assignment_solutions(assignment_id)
        self.reference_solutions[assignment_id] = solutions
        
        # Export solutions for instructor review
        solutions_dir = os.path.join("reference_solutions", assignment_id)
        self.solution_generator.export_solutions(solutions, solutions_dir)
        
        # Evaluate solution quality
        print("\n📊 Evaluating solution quality:")
        for problem_id, solution in solutions.items():
            quality = self.solution_generator.evaluate_solution_quality(solution)
            print(f"  {problem_id}: Overall quality {quality.overall_score:.2f}")
            if quality.overall_score < 0.7:
                print(f"    ⚠️  Consider manual review - {quality.notes}")
        
        return solutions
    
    def grade_notebook_with_reference(self, notebook_path: str, assignment_id: str) -> List[GradingResult]:
        """Grade a notebook using reference solutions for enhanced assessment"""
        
        print(f"📚 Grading notebook: {notebook_path}")
        
        # Parse notebook
        parsed_content = self.parser.parse_notebook(notebook_path)
        student_name = parsed_content['student_name']
        
        # Load rubric
        assignment_rubric = self.rubric_manager.load_assignment_rubric(assignment_id)
        
        # Ensure reference solutions exist
        if self.use_reference_solutions and assignment_id not in self.reference_solutions:
            print(f"🔄 Generating reference solutions for {assignment_id}...")
            self.generate_reference_solutions(assignment_id)
        
        # Grade each response
        notebook_results = []
        
        for response in parsed_content['responses']:
            if response.problem_id in assignment_rubric:
                rubric = assignment_rubric[response.problem_id]
                
                # Enhanced grading with reference solution
                result = self._grade_with_reference(response, rubric, assignment_id, student_name)
                notebook_results.append(result)
                
                print(f"  ✅ Graded {response.problem_id}: {result.total_score}/{result.max_possible} ({result.percentage:.1f}%)")
            else:
                print(f"  ⚠️  Warning: No rubric found for {response.problem_id}")
        
        self.results.extend(notebook_results)
        return notebook_results
    
    def _grade_with_reference(self, response, rubric, assignment_id: str, student_name: str) -> GradingResult:
        """Grade a response using reference solution for enhanced assessment"""
        
        # Basic context
        context = f"Assignment: {assignment_id}"
        
        # Enhanced context with reference solution
        if (self.use_reference_solutions and 
            assignment_id in self.reference_solutions and 
            response.problem_id in self.reference_solutions[assignment_id]):
            
            reference_solution = self.reference_solutions[assignment_id][response.problem_id]
            
            # Compare student response with reference
            comparison = self.solution_generator.compare_student_solution(
                response.content, reference_solution
            )
            
            # Enhanced context for grading
            enhanced_context = f"""{context}

REFERENCE SOLUTION CONTEXT:
- Key concepts: {', '.join(reference_solution.key_concepts)}
- Expected outputs: {reference_solution.expected_outputs}
- Common approaches: {', '.join(reference_solution.common_approaches)}
- Grading notes: {reference_solution.grading_notes}

STUDENT COMPARISON ANALYSIS:
- Concept coverage: {comparison.get('concept_coverage', 0):.2f}
- Approach similarity: {comparison.get('approach_similarity', 0):.2f}
- Missing concepts: {', '.join(comparison.get('missing_concepts', []))}
- Strengths: {', '.join(comparison.get('strengths', []))}
- Areas for improvement: {', '.join(comparison.get('improvement_areas', []))}"""
            
            context = enhanced_context
        
        # Grade using enhanced context
        result = self.grader.grade_response(response, rubric, context)
        result.student_name = student_name
        
        return result
    
    def grade_directory(self, directory_path: str, assignment_id: str, 
                       generate_solutions: bool = True) -> Dict[str, List[GradingResult]]:
        """Grade all notebooks in a directory with reference solutions"""
        
        print(f"🚀 Starting enhanced AI grading for assignment: {assignment_id}")
        print(f"📁 Directory: {directory_path}")
        print(f"🧠 Reference solutions: {'Enabled' if self.use_reference_solutions else 'Disabled'}")
        
        # Generate reference solutions first if enabled
        if generate_solutions and self.use_reference_solutions:
            self.generate_reference_solutions(assignment_id)
        
        # Validate directory
        directory_path = os.path.normpath(directory_path)
        if not os.path.isdir(directory_path):
            print(f"❌ Error: {directory_path} is not a valid directory")
            return {}
        
        # Find notebook files
        notebook_files = [f for f in os.listdir(directory_path) if f.endswith('.ipynb')]
        
        if not notebook_files:
            print("❌ No notebook files found!")
            return {}
        
        print(f"📊 Found {len(notebook_files)} notebooks to grade")
        
        all_results = {}
        
        for notebook_file in notebook_files:
            notebook_path = os.path.join(directory_path, notebook_file)
            
            if not os.path.isfile(notebook_path):
                print(f"⏭️  Skipping {notebook_path} - not a file")
                continue
                
            try:
                if self.use_reference_solutions:
                    results = self.grade_notebook_with_reference(notebook_path, assignment_id)
                else:
                    # Fallback to basic grading
                    results = self._grade_notebook_basic(notebook_path, assignment_id)
                
                all_results[notebook_file] = results
            except Exception as e:
                print(f"❌ Error grading {notebook_file}: {e}")
                all_results[notebook_file] = []
        
        return all_results
    
    def _grade_notebook_basic(self, notebook_path: str, assignment_id: str) -> List[GradingResult]:
        """Basic grading without reference solutions (fallback)"""
        
        parsed_content = self.parser.parse_notebook(notebook_path)
        student_name = parsed_content['student_name']
        assignment_rubric = self.rubric_manager.load_assignment_rubric(assignment_id)
        
        notebook_results = []
        
        for response in parsed_content['responses']:
            if response.problem_id in assignment_rubric:
                rubric = assignment_rubric[response.problem_id]
                context = f"Assignment: {assignment_id}\nStudent: {student_name}"
                
                result = self.grader.grade_response(response, rubric, context)
                result.student_name = student_name
                notebook_results.append(result)
        
        self.results.extend(notebook_results)
        return notebook_results
    
    def export_results(self, output_directory: str):
        """Export grading results with enhanced reporting"""
        
        if not self.report_generator:
            self.report_generator = ReportGenerator(self.results)
        
        # Export standard reports
        self.report_generator.export_results(output_directory)
        
        # Export reference solutions analysis if available
        if self.reference_solutions:
            self._export_solution_analysis(output_directory)
    
    def _export_solution_analysis(self, output_directory: str):
        """Export analysis of how students compared to reference solutions"""
        
        analysis_dir = os.path.join(output_directory, 'solution_analysis')
        os.makedirs(analysis_dir, exist_ok=True)
        
        # Create summary of student performance vs reference
        summary_path = os.path.join(analysis_dir, 'reference_comparison_summary.txt')
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("REFERENCE SOLUTION COMPARISON SUMMARY\n")
            f.write("=" * 50 + "\n\n")
            
            for assignment_id, solutions in self.reference_solutions.items():
                f.write(f"Assignment: {assignment_id}\n")
                f.write("-" * 30 + "\n")
                
                for problem_id, solution in solutions.items():
                    f.write(f"\nProblem: {problem_id}\n")
                    f.write(f"Key Concepts: {', '.join(solution.key_concepts)}\n")
                    f.write(f"Difficulty: {solution.difficulty_level}\n")
                    f.write(f"Est. Time: {solution.estimated_time_minutes} min\n")
                
                f.write("\n" + "=" * 50 + "\n\n")
        
        print(f"📊 Solution analysis exported to: {analysis_dir}")
    
    def get_grading_summary(self) -> Dict:
        """Get enhanced summary with reference solution insights"""
        
        basic_summary = super().get_grading_summary() if hasattr(super(), 'get_grading_summary') else {}
        
        # Add reference solution insights
        enhanced_summary = {
            'total_graded': len(self.results),
            'reference_solutions_used': bool(self.reference_solutions),
            'assignments_with_solutions': list(self.reference_solutions.keys()),
            'solution_count': sum(len(sols) for sols in self.reference_solutions.values())
        }
        
        # Merge with basic summary
        enhanced_summary.update(basic_summary)
        
        return enhanced_summary