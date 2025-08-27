# llm_grader.py
"""
LLM-based grading engine for evaluating student responses
"""

import json
from datetime import datetime
from typing import List
from ..config.data_structures import StudentResponse, ProblemRubric, GradingResult
from .llm_interface import LLMInterface

class LLMGrader:
    """Core grading logic using language models"""
    
    def __init__(self, llm_interface: LLMInterface):
        self.llm = llm_interface
        self.grading_history = []
    
    def grade_response(self, response: StudentResponse, rubric: ProblemRubric, 
                      assignment_context: str = "") -> GradingResult:
        """Grade a single student response using LLM"""
        
        prompt = self._construct_grading_prompt(response, rubric, assignment_context)
        
        try:
            llm_response = self.llm.generate_response(prompt, max_tokens=1500)
            result = self._parse_llm_response(llm_response, response, rubric)
            
            # Store grading history
            self.grading_history.append({
                'timestamp': datetime.now(),
                'student': response.problem_id,
                'prompt': prompt,
                'llm_response': llm_response,
                'result': result
            })
            
            return result
            
        except Exception as e:
            print(f"Error grading response: {e}")
            return self._create_error_result(response, rubric, str(e))
    
    def _construct_grading_prompt(self, response: StudentResponse, rubric: ProblemRubric, 
                                context: str) -> str:
        """Construct detailed grading prompt for the LLM"""
        
        criteria_text = "\n".join([
            f"- {crit.name} ({crit.max_points} points): {crit.description}\n  Guidelines: {crit.guidelines}"
            for crit in rubric.criteria
        ])
        
        # Analyze the response structure
        cell_type_info = f"Response Type: {response.cell_type}"
        if response.cell_type == 'mixed':
            cell_type_info += " (contains both code and markdown cells)"
        elif response.cell_type == 'code':
            cell_type_info += " (primarily code implementation)"
        elif response.cell_type == 'markdown':
            cell_type_info += " (primarily text/explanation)"
        
        # Check for outputs and images
        output_info = ""
        if response.execution_output:
            output_info = "\n\nEXECUTION OUTPUTS AND RESULTS:"
            output_info += f"\n{response.execution_output}"
            
            # Analyze output types for the AI
            if "IMAGE OUTPUT" in response.execution_output:
                image_count = response.execution_output.count("IMAGE OUTPUT")
                output_info += f"\n\n[ANALYSIS NOTE: This response generated {image_count} visualization(s)]"
            
            if "ERROR" in response.execution_output.upper() or "TRACEBACK" in response.execution_output.upper():
                output_info += "\n\n[ANALYSIS NOTE: Execution errors detected in output]"
        
        prompt = f"""You are an expert machine learning instructor grading student homework. You are evaluating a student's complete response to a problem that may contain multiple cells (markdown explanations, code implementations, and outputs).

ASSIGNMENT CONTEXT:
{context}

PROBLEM STATEMENT:
{rubric.problem_statement}

TOTAL POINTS POSSIBLE: {rubric.total_points}

GRADING CRITERIA:
{criteria_text}

STUDENT RESPONSE ANALYSIS:
{cell_type_info}

STUDENT RESPONSE CONTENT:
{response.content}
{output_info}

{"IMPORTANT: This response contains execution errors that may affect the grade." if response.has_errors else ""}

GRADING INSTRUCTIONS:
1. **Holistic Evaluation**: Consider the complete response including explanations, code, and outputs together
2. **Cell Type Analysis**: 
   - [MARKDOWN CELL] sections contain explanations, reasoning, and text responses
   - [CODE CELL] sections contain implementation and technical work
   - Evaluate how well these components work together
3. **Output Assessment**: 
   - Check if code execution was successful
   - Verify that visualizations/outputs align with the code
   - Consider whether outputs demonstrate correct implementation
4. **Technical Quality**: Assess code correctness, style, and documentation
5. **Conceptual Understanding**: Evaluate explanations and reasoning quality
6. **Integration**: Consider how well code and explanations support each other

SCORING GUIDELINES:
- Assign points for each criterion (0 to maximum specified)
- Consider both technical execution AND conceptual understanding
- Deduct points for errors, missing components, or poor explanations
- Reward clear integration between code and explanations
- Account for visualization quality when images are present

RESPONSE FORMAT:
Provide your assessment as a JSON object with detailed, constructive feedback:

{{
  "scores": {{"criterion_name": points_awarded, ...}},
  "total_score": total_points_awarded,
  "percentage": percentage_score,
  "feedback": "Comprehensive feedback addressing both technical and conceptual aspects. Comment on code quality, explanation clarity, output correctness, and integration between components...",
  "suggestions": ["Specific improvement suggestion 1", "Specific improvement suggestion 2", ...],
  "confidence": confidence_score_0_to_1
}}

Focus on providing actionable feedback that helps the student improve both their technical skills and their ability to explain their work clearly."""
        
        return prompt
    
    def _parse_llm_response(self, llm_response: str, response: StudentResponse, 
                           rubric: ProblemRubric) -> GradingResult:
        """Parse structured response from LLM"""
        
        try:
            # Extract JSON from response
            json_start = llm_response.find('{')
            json_end = llm_response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in LLM response")
            
            json_str = llm_response[json_start:json_end]
            parsed = json.loads(json_str)
            
            # Validate and clean the response
            scores = parsed.get('scores', {})
            total_score = parsed.get('total_score', sum(scores.values()))
            confidence = parsed.get('confidence', 0.5)
            
            # Flag for review if confidence is low or scores seem off
            flagged = confidence < 0.7 or total_score > rubric.total_points
            
            return GradingResult(
                problem_id=response.problem_id,
                student_id="",  # Will be filled in by calling function
                scores=scores,
                total_score=total_score,
                max_possible=rubric.total_points,
                percentage=parsed.get('percentage', (total_score / rubric.total_points) * 100),
                feedback=parsed.get('feedback', 'No feedback provided'),
                suggestions=parsed.get('suggestions', []),
                confidence=confidence,
                flagged_for_review=flagged
            )
            
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error parsing LLM response: {e}")
            print(f"Raw response: {llm_response}")
            return self._create_error_result(response, rubric, f"Parse error: {e}")
    
    def _create_error_result(self, response: StudentResponse, rubric: ProblemRubric, 
                           error_msg: str) -> GradingResult:
        """Create error result when grading fails"""
        return GradingResult(
            problem_id=response.problem_id,
            student_id="",
            scores={crit.name: 0 for crit in rubric.criteria},
            total_score=0,
            max_possible=rubric.total_points,
            percentage=0.0,
            feedback=f"Grading error occurred: {error_msg}",
            suggestions=["Please review this submission manually"],
            confidence=0.0,
            flagged_for_review=True
        )