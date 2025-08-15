# solution_generator.py
"""
LLM-powered solution generator for assignment problems
Generates reference solutions to aid in grading and rubric development
"""

import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

from llm_interface import LLMInterface
from data_structures import ProblemRubric
from rubric_manager import RubricManager

@dataclass
class ProblemSolution:
    """Generated solution for a specific problem"""
    problem_id: str
    assignment_id: str
    solution_code: str
    solution_explanation: str
    key_concepts: List[str]
    expected_outputs: str
    common_approaches: List[str]
    grading_notes: str
    difficulty_level: str  # 'easy', 'medium', 'hard'
    estimated_time_minutes: int
    generated_timestamp: datetime

@dataclass
class SolutionQuality:
    """Assessment of solution quality and completeness"""
    completeness_score: float  # 0.0 to 1.0
    technical_accuracy: float  # 0.0 to 1.0
    explanation_clarity: float  # 0.0 to 1.0
    pedagogical_value: float  # 0.0 to 1.0
    overall_score: float  # 0.0 to 1.0
    notes: str

class SolutionGenerator:
    """Generates reference solutions for assignment problems using LLM"""
    
    def __init__(self, llm_interface: LLMInterface, temperature: float = 0.7):
        self.llm = llm_interface
        self.temperature = temperature  # Higher temperature for creative problem solving
        self.rubric_manager = RubricManager()
        self.solutions_cache = {}
    
    def generate_solution(self, problem_statement: str, rubric: ProblemRubric, 
                         assignment_context: str = "") -> ProblemSolution:
        """Generate a comprehensive solution for a given problem"""
        
        prompt = self._construct_solution_prompt(problem_statement, rubric, assignment_context)
        
        try:
            llm_response = self.llm.generate_response(prompt, max_tokens=2000)
            solution = self._parse_solution_response(llm_response, rubric.problem_id, assignment_context)
            
            # Cache the solution
            cache_key = f"{assignment_context}_{rubric.problem_id}"
            self.solutions_cache[cache_key] = solution
            
            return solution
            
        except Exception as e:
            print(f"Error generating solution for {rubric.problem_id}: {e}")
            return self._create_fallback_solution(rubric.problem_id, assignment_context, str(e))
    
    def generate_assignment_solutions(self, assignment_id: str) -> Dict[str, ProblemSolution]:
        """Generate solutions for all problems in an assignment"""
        
        print(f"Generating reference solutions for assignment: {assignment_id}")
        
        # Load assignment rubric
        assignment_rubric = self.rubric_manager.load_assignment_rubric(assignment_id)
        
        solutions = {}
        
        for problem_id, rubric in assignment_rubric.items():
            print(f"  Generating solution for {problem_id}...")
            
            solution = self.generate_solution(
                problem_statement=rubric.problem_statement,
                rubric=rubric,
                assignment_context=f"Assignment: {assignment_id}"
            )
            
            solutions[problem_id] = solution
            print(f"    ✓ Solution generated ({solution.difficulty_level} difficulty)")
        
        return solutions
    
    def _construct_solution_prompt(self, problem_statement: str, rubric: ProblemRubric, 
                                  context: str) -> str:
        """Construct prompt for generating problem solutions"""
        
        criteria_text = "\n".join([
            f"- {crit.name}: {crit.description} ({crit.max_points} points)"
            for crit in rubric.criteria
        ])
        
        prompt = f"""You are an expert machine learning instructor creating a comprehensive reference solution for a student assignment problem.

ASSIGNMENT CONTEXT:
{context}

PROBLEM STATEMENT:
{problem_statement}

GRADING CRITERIA (Total: {rubric.total_points} points):
{criteria_text}

EXPECTED RESPONSE TYPE: {rubric.expected_response_type}

TASK:
Create a complete, exemplary solution that would earn full points according to the grading criteria. Your solution should serve as a reference for grading student submissions.

REQUIREMENTS:
1. **Complete Implementation**: Provide working code that solves the problem
2. **Clear Explanations**: Include detailed explanations of concepts and decisions
3. **Best Practices**: Demonstrate proper coding style, documentation, and ML practices
4. **Educational Value**: Explain the 'why' behind each approach
5. **Multiple Approaches**: Mention alternative valid approaches when applicable

RESPONSE FORMAT:
Provide a comprehensive solution as a JSON object:

{{
  "solution_code": "Complete, well-documented code implementation...",
  "solution_explanation": "Detailed explanation of the approach, concepts, and implementation decisions...",
  "key_concepts": ["concept1", "concept2", "concept3"],
  "expected_outputs": "Description of what the code should produce when run...",
  "common_approaches": ["approach1", "approach2", "approach3"],
  "grading_notes": "Key points graders should look for when evaluating student responses...",
  "difficulty_level": "easy|medium|hard",
  "estimated_time_minutes": estimated_completion_time
}}

Focus on creating a solution that demonstrates mastery of the concepts while being accessible to students at this level."""
        
        return prompt
    
    def _parse_solution_response(self, llm_response: str, problem_id: str, 
                                assignment_context: str) -> ProblemSolution:
        """Parse LLM response into structured solution"""
        
        try:
            # Extract JSON from response
            json_start = llm_response.find('{')
            json_end = llm_response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in LLM response")
            
            json_str = llm_response[json_start:json_end]
            parsed = json.loads(json_str)
            
            return ProblemSolution(
                problem_id=problem_id,
                assignment_id=assignment_context,
                solution_code=parsed.get('solution_code', ''),
                solution_explanation=parsed.get('solution_explanation', ''),
                key_concepts=parsed.get('key_concepts', []),
                expected_outputs=parsed.get('expected_outputs', ''),
                common_approaches=parsed.get('common_approaches', []),
                grading_notes=parsed.get('grading_notes', ''),
                difficulty_level=parsed.get('difficulty_level', 'medium'),
                estimated_time_minutes=parsed.get('estimated_time_minutes', 60),
                generated_timestamp=datetime.now()
            )
            
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error parsing solution response: {e}")
            return self._create_fallback_solution(problem_id, assignment_context, f"Parse error: {e}")
    
    def _create_fallback_solution(self, problem_id: str, assignment_context: str, 
                                 error_msg: str) -> ProblemSolution:
        """Create fallback solution when generation fails"""
        return ProblemSolution(
            problem_id=problem_id,
            assignment_id=assignment_context,
            solution_code="# Solution generation failed - manual review required",
            solution_explanation=f"Error generating solution: {error_msg}",
            key_concepts=[],
            expected_outputs="Manual review required",
            common_approaches=[],
            grading_notes="Manual grading recommended due to solution generation failure",
            difficulty_level="unknown",
            estimated_time_minutes=0,
            generated_timestamp=datetime.now()
        )
    
    def evaluate_solution_quality(self, solution: ProblemSolution) -> SolutionQuality:
        """Evaluate the quality of a generated solution"""
        
        prompt = f"""Evaluate the quality of this generated solution for an assignment problem:

PROBLEM ID: {solution.problem_id}
SOLUTION CODE:
{solution.solution_code}

SOLUTION EXPLANATION:
{solution.solution_explanation}

GRADING NOTES:
{solution.grading_notes}

Assess the solution on these criteria (0.0 to 1.0 scale):
1. Completeness: Does it fully address the problem?
2. Technical Accuracy: Is the code correct and following best practices?
3. Explanation Clarity: Are the explanations clear and educational?
4. Pedagogical Value: Would this help students learn?

Respond with JSON:
{{
  "completeness_score": 0.0-1.0,
  "technical_accuracy": 0.0-1.0,
  "explanation_clarity": 0.0-1.0,
  "pedagogical_value": 0.0-1.0,
  "overall_score": 0.0-1.0,
  "notes": "Detailed assessment notes..."
}}"""
        
        try:
            response = self.llm.generate_response(prompt, max_tokens=500)
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            parsed = json.loads(response[json_start:json_end])
            
            return SolutionQuality(
                completeness_score=parsed.get('completeness_score', 0.5),
                technical_accuracy=parsed.get('technical_accuracy', 0.5),
                explanation_clarity=parsed.get('explanation_clarity', 0.5),
                pedagogical_value=parsed.get('pedagogical_value', 0.5),
                overall_score=parsed.get('overall_score', 0.5),
                notes=parsed.get('notes', 'Quality assessment completed')
            )
        except Exception as e:
            return SolutionQuality(
                completeness_score=0.0,
                technical_accuracy=0.0,
                explanation_clarity=0.0,
                pedagogical_value=0.0,
                overall_score=0.0,
                notes=f"Quality assessment failed: {e}"
            )
    
    def export_solutions(self, solutions: Dict[str, ProblemSolution], 
                        output_directory: str):
        """Export solutions to files for review and use"""
        
        os.makedirs(output_directory, exist_ok=True)
        
        # Export as JSON
        solutions_data = {}
        for problem_id, solution in solutions.items():
            solutions_data[problem_id] = {
                'problem_id': solution.problem_id,
                'assignment_id': solution.assignment_id,
                'solution_code': solution.solution_code,
                'solution_explanation': solution.solution_explanation,
                'key_concepts': solution.key_concepts,
                'expected_outputs': solution.expected_outputs,
                'common_approaches': solution.common_approaches,
                'grading_notes': solution.grading_notes,
                'difficulty_level': solution.difficulty_level,
                'estimated_time_minutes': solution.estimated_time_minutes,
                'generated_timestamp': solution.generated_timestamp.isoformat()
            }
        
        json_path = os.path.join(output_directory, 'reference_solutions.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(solutions_data, f, indent=2, ensure_ascii=False)
        
        # Export human-readable versions
        for problem_id, solution in solutions.items():
            readable_path = os.path.join(output_directory, f'{problem_id}_solution.md')
            with open(readable_path, 'w', encoding='utf-8') as f:
                f.write(f"# Reference Solution: {problem_id}\n\n")
                f.write(f"**Assignment:** {solution.assignment_id}\n")
                f.write(f"**Difficulty:** {solution.difficulty_level}\n")
                f.write(f"**Estimated Time:** {solution.estimated_time_minutes} minutes\n")
                f.write(f"**Generated:** {solution.generated_timestamp}\n\n")
                
                f.write(f"## Solution Code\n\n```python\n{solution.solution_code}\n```\n\n")
                
                f.write(f"## Explanation\n\n{solution.solution_explanation}\n\n")
                
                f.write(f"## Key Concepts\n\n")
                for concept in solution.key_concepts:
                    f.write(f"- {concept}\n")
                
                f.write(f"\n## Expected Outputs\n\n{solution.expected_outputs}\n\n")
                
                f.write(f"## Common Approaches\n\n")
                for approach in solution.common_approaches:
                    f.write(f"- {approach}\n")
                
                f.write(f"\n## Grading Notes\n\n{solution.grading_notes}\n")
        
        print(f"Solutions exported to: {output_directory}")
        print(f"  - JSON format: {json_path}")
        print(f"  - Markdown files: {len(solutions)} problem solutions")
    
    def compare_student_solution(self, student_response: str, reference_solution: ProblemSolution) -> Dict[str, Any]:
        """Compare student response against reference solution"""
        
        prompt = f"""Compare this student response against the reference solution:

REFERENCE SOLUTION:
{reference_solution.solution_explanation}

CODE:
{reference_solution.solution_code}

KEY CONCEPTS: {', '.join(reference_solution.key_concepts)}

STUDENT RESPONSE:
{student_response}

Provide comparison analysis in JSON format:
{{
  "concept_coverage": 0.0-1.0,
  "approach_similarity": 0.0-1.0,
  "code_quality_vs_reference": 0.0-1.0,
  "missing_concepts": ["concept1", "concept2"],
  "strengths": ["strength1", "strength2"],
  "improvement_areas": ["area1", "area2"],
  "overall_comparison": "Detailed comparison summary..."
}}"""
        
        try:
            response = self.llm.generate_response(prompt, max_tokens=800)
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            return json.loads(response[json_start:json_end])
        except Exception as e:
            return {
                "concept_coverage": 0.0,
                "approach_similarity": 0.0,
                "code_quality_vs_reference": 0.0,
                "missing_concepts": [],
                "strengths": [],
                "improvement_areas": [f"Comparison failed: {e}"],
                "overall_comparison": f"Could not compare due to error: {e}"
            }