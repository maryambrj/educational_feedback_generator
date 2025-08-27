# rubric_manager.py
"""
Rubric management system for handling grading criteria and scoring
"""

import os
import yaml
from typing import Dict
from ..config.data_structures import GradingCriterion, ProblemRubric

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
        
        rubric_path = os.path.join(self.rubrics_directory, f"{assignment_id}.txt")
        
        if not os.path.exists(rubric_path):
            # Create default rubric if none exists
            self._create_default_rubric(assignment_id)
        
        with open(rubric_path, 'r', encoding='utf-8') as file:
            rubric_content = file.read().strip()
        
        # Parse txt rubric format - for now, create a simple structure
        rubric_data = self._parse_txt_rubric(rubric_content, assignment_id)
        
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
        
        rubric_path = os.path.join(self.rubrics_directory, f"{assignment_id}.txt")
        with open(rubric_path, 'w', encoding='utf-8') as file:
            # Convert default rubric to txt format
            txt_content = self._convert_to_txt_format(default_rubric)
            file.write(txt_content)
    
    def save_rubric(self, assignment_id: str, rubric_data: Dict):
        """Save rubric data to file"""
        rubric_path = os.path.join(self.rubrics_directory, f"{assignment_id}.txt")
        with open(rubric_path, 'w', encoding='utf-8') as file:
            txt_content = self._convert_to_txt_format(rubric_data)
            file.write(txt_content)
    
    def _parse_txt_rubric(self, content: str, assignment_id: str) -> Dict:
        """Parse txt rubric format and return structured data"""
        # For now, create a simple default structure based on your current txt file
        # This assumes a simple format like yours with points, description, guidelines
        return {
            'part_1': {
                'total_points': 30,
                'problem_statement': 'General homework problem',
                'expected_response_type': 'mixed',
                'context': 'Student should provide thoughtful analysis',
                'criteria': {
                    'content_quality': {
                        'points': 15,
                        'description': 'Quality and depth of response',
                        'guidelines': 'Clear reasoning and understanding demonstrated'
                    },
                    'implementation': {
                        'points': 10,
                        'description': 'Code quality and correctness',
                        'guidelines': 'Working code with proper structure'
                    },
                    'presentation': {
                        'points': 5,
                        'description': 'Clear presentation and communication',
                        'guidelines': 'Well-organized and clearly written'
                    }
                }
            }
        }
    
    def _convert_to_txt_format(self, rubric_data: Dict) -> str:
        """Convert structured rubric data to txt format"""
        lines = []
        for problem_id, problem_data in rubric_data.items():
            lines.append(f"Problem: {problem_id}")
            lines.append(f"Total Points: {problem_data['total_points']}")
            lines.append(f"Statement: {problem_data.get('problem_statement', '')}")
            lines.append("")
            
            for crit_name, crit_data in problem_data['criteria'].items():
                lines.append(f"  {crit_name}:")
                lines.append(f"    points: {crit_data['points']}")
                lines.append(f"    description: \"{crit_data['description']}\"")
                lines.append(f"    guidelines: \"{crit_data['guidelines']}\"")
                lines.append("")
        
        return "\n".join(lines)