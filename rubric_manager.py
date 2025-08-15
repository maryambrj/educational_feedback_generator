# rubric_manager.py
"""
Rubric management system for handling grading criteria and scoring
"""

import os
import yaml
from typing import Dict
from data_structures import GradingCriterion, ProblemRubric

class RubricManager:
    """Manages grading criteria and scoring systems"""
    
    def __init__(self, rubrics_directory: str = "rubrics"):
        self.rubrics_directory = rubrics_directory
        self.loaded_rubrics = {}
        
        # Create rubrics directory if it doesn't exist
        os.makedirs(rubrics_directory, exist_ok=True)
    
    def load_assignment_rubric(self, assignment_id: str) -> Dict[str, ProblemRubric]:
        """Load rubric for an entire assignment"""
        
        if assignment_id in self.loaded_rubrics:
            return self.loaded_rubrics[assignment_id]
        
        rubric_path = os.path.join(self.rubrics_directory, f"{assignment_id}.yaml")
        
        if not os.path.exists(rubric_path):
            # Create default rubric if none exists
            self._create_default_rubric(assignment_id)
        
        with open(rubric_path, 'r', encoding='utf-8') as file:
            rubric_data = yaml.safe_load(file)
        
        # Convert to ProblemRubric objects
        problem_rubrics = {}
        for problem_id, problem_data in rubric_data.items():
            criteria = [
                GradingCriterion(
                    name=crit_name,
                    max_points=crit_data['points'],
                    description=crit_data.get('description', ''),
                    guidelines=crit_data.get('guidelines', '')
                )
                for crit_name, crit_data in problem_data['criteria'].items()
            ]
            
            problem_rubrics[problem_id] = ProblemRubric(
                problem_id=problem_id,
                total_points=problem_data['total_points'],
                criteria=criteria,
                problem_statement=problem_data.get('problem_statement', ''),
                expected_response_type=problem_data.get('expected_response_type', 'mixed'),
                context=problem_data.get('context', '')
            )
        
        self.loaded_rubrics[assignment_id] = problem_rubrics
        return problem_rubrics
    
    def _create_default_rubric(self, assignment_id: str):
        """Create a default rubric template"""
        default_rubric = {
            'part_1': {
                'total_points': 30,
                'problem_statement': 'From Exploration to Engineering',
                'expected_response_type': 'mixed',
                'context': 'Student should demonstrate understanding of IDA, EDA, and feature engineering',
                'criteria': {
                    'insight_quality': {
                        'points': 15,
                        'description': 'Quality and depth of insights from IDA/EDA',
                        'guidelines': 'Look for specific observations about data patterns, identification of problems, and proposed solutions'
                    },
                    'code_quality': {
                        'points': 10,
                        'description': 'Quality of code implementation',
                        'guidelines': 'Clean, well-commented code that runs without errors'
                    },
                    'visualization': {
                        'points': 5,
                        'description': 'Quality and appropriateness of visualizations',
                        'guidelines': 'Clear, properly labeled plots that support the analysis'
                    }
                }
            },
            'part_2': {
                'total_points': 30,
                'problem_statement': 'Train-Test Splits',
                'expected_response_type': 'mixed',
                'criteria': {
                    'conceptual_understanding': {
                        'points': 15,
                        'description': 'Understanding of why train-test splits are needed',
                        'guidelines': 'Clear explanation of overfitting, generalization, and validation concepts'
                    },
                    'implementation': {
                        'points': 10,
                        'description': 'Correct implementation using sklearn',
                        'guidelines': 'Proper use of train_test_split, appropriate analysis of results'
                    },
                    'analysis': {
                        'points': 5,
                        'description': 'Analysis of split properties and stratification',
                        'guidelines': 'Understanding of stratified splits and their importance'
                    }
                }
            },
            'part_3': {
                'total_points': 40,
                'problem_statement': 'Scikit-Learn API',
                'expected_response_type': 'mixed',
                'criteria': {
                    'api_understanding': {
                        'points': 20,
                        'description': 'Understanding of sklearn API concepts',
                        'guidelines': 'Clear definitions of estimator, transformer, predictor and their methods'
                    },
                    'implementation': {
                        'points': 10,
                        'description': 'Correct implementation of LinearRegression example',
                        'guidelines': 'Working code with proper fit, predict, and visualization'
                    },
                    'pipeline_understanding': {
                        'points': 10,
                        'description': 'Understanding of ML pipelines',
                        'guidelines': 'Clear explanation of pipeline benefits and setup'
                    }
                }
            }
        }
        
        rubric_path = os.path.join(self.rubrics_directory, f"{assignment_id}.yaml")
        with open(rubric_path, 'w', encoding='utf-8') as file:
            yaml.dump(default_rubric, file, default_flow_style=False, indent=2)
    
    def save_rubric(self, assignment_id: str, rubric_data: Dict):
        """Save rubric data to file"""
        rubric_path = os.path.join(self.rubrics_directory, f"{assignment_id}.yaml")
        with open(rubric_path, 'w', encoding='utf-8') as file:
            yaml.dump(rubric_data, file, default_flow_style=False, indent=2)