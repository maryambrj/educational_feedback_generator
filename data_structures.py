# data_structures.py
"""
Core data structures for the AI grading system
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any

@dataclass
class StudentResponse:
    """Represents a student's response to a problem or part"""
    problem_id: str
    part_id: Optional[str]
    content: str
    cell_type: str  # 'code', 'markdown'
    cell_index: int
    execution_output: Optional[str] = None
    has_errors: bool = False

@dataclass
class GradingCriterion:
    """Individual grading criterion with points and description"""
    name: str
    max_points: int
    description: str
    guidelines: str

@dataclass
class ProblemRubric:
    """Rubric for a specific problem or part"""
    problem_id: str
    total_points: int
    criteria: List[GradingCriterion]
    problem_statement: str
    expected_response_type: str  # 'code', 'text', 'mixed'
    context: Optional[str] = None

@dataclass
class GradingResult:
    """Result of grading a single response"""
    problem_id: str
    student_name: str
    scores: Dict[str, float]  # criterion_name -> score
    total_score: float
    max_possible: int
    percentage: float
    feedback: str
    suggestions: List[str]
    confidence: float
    flagged_for_review: bool = False