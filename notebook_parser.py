
# notebook_parser.py
"""
Notebook parsing functionality for extracting structured content from student notebooks
"""

import nbformat
import os
import re
from typing import Dict, List, Optional, Any
from data_structures import StudentResponse

class NotebookParser:
    """Enhanced parser that extracts structured content from student notebooks"""
    
    def __init__(self):
        self.problem_patterns = [
            r'##\s*Part\s*(\d+):\s*(.+)',
            r'##\s*Problem\s*(\d+):\s*(.+)',
            # r'____',
            # r'---'  # Separator pattern from your example
        ]
    
    def parse_notebook(self, notebook_path: str) -> Dict[str, Any]:
        """Parse notebook and extract structured problem-response pairs"""
        
        with open(notebook_path, 'r', encoding='utf-8') as file:
            notebook = nbformat.read(file, as_version=4)
        
        student_name = self._extract_student_name(notebook_path)
        problems = self._identify_problems(notebook)
        responses = self._extract_responses(notebook, problems)
        
        return {
            'student_name': student_name,
            'notebook_path': notebook_path,
            'problems': problems,
            'responses': responses,
            'total_cells': len(notebook['cells'])
        }
    
    def _extract_student_name(self, notebook_path: str) -> str:
        """Extract student name from filename"""
        filename = os.path.basename(notebook_path)
        # Remove .ipynb extension and replace underscores with spaces
        name = filename.replace('.ipynb', '').replace('_', ' ')
        return name
    
    def _identify_problems(self, notebook) -> List[Dict[str, Any]]:
        """Identify problem sections in the notebook"""
        problems = []
        
        for i, cell in enumerate(notebook['cells']):
            if cell['cell_type'] == 'markdown':
                content = cell['source']
                
                # Check for problem patterns
                for pattern in self.problem_patterns:
                    match = re.search(pattern, content, re.IGNORECASE)
                    if match:
                        problem_info = {
                            'cell_index': i,
                            'content': content,
                            'pattern_match': match.groups() if match.groups() else (content[:50],),
                            'problem_id': self._generate_problem_id(match, i)
                        }
                        problems.append(problem_info)
                        break
        
        return problems
    
    def _generate_problem_id(self, match, cell_index: int) -> str:
        """Generate consistent problem ID from pattern match"""
        if match and match.groups():
            # Try to extract part number or problem identifier
            groups = match.groups()
            if len(groups) >= 1 and groups[0].isdigit():
                return f"part_{groups[0]}"
            elif len(groups) >= 1:
                # Clean up text to create ID
                clean_text = re.sub(r'[^\w\s]', '', groups[0])
                clean_text = '_'.join(clean_text.lower().split()[:3])
                return clean_text
        
        return f"problem_{cell_index}"
    
    def _extract_responses(self, notebook, problems: List[Dict]) -> List[StudentResponse]:
        """Extract student responses following each problem"""
        responses = []
        
        for i, problem in enumerate(problems):
            problem_start = problem['cell_index']
            
            # Determine end of problem section
            if i + 1 < len(problems):
                problem_end = problems[i + 1]['cell_index']
            else:
                problem_end = len(notebook['cells'])
            
            # Extract and combine all response cells in this problem section
            combined_response = self._get_combined_response_in_range(
                notebook, problem_start + 1, problem_end, problem['problem_id']
            )
            
            if combined_response:
                responses.append(combined_response)
        
        return responses
    
    def _get_combined_response_in_range(self, notebook, start: int, end: int, problem_id: str) -> Optional[StudentResponse]:
        """Extract and combine all response cells between start and end cell indices into a single StudentResponse"""
        
        answer_cells = []
        combined_content = []
        combined_output = []
        has_errors = False
        first_cell_index = start
        
        for i in range(start, end):
            if i >= len(notebook['cells']):
                break
                
            cell = notebook['cells'][i]
            
            # Check if this is an answer cell
            if self._is_answer_cell(cell):
                answer_cells.append(cell)
                
                # Combine content with cell type indicators
                cell_type_indicator = f"[{cell['cell_type'].upper()} CELL]"
                combined_content.append(f"{cell_type_indicator}\n{cell['source']}")
                
                # Collect execution output if available
                output = self._get_execution_output(cell)
                if output:
                    combined_output.append(f"[OUTPUT from cell {i}]\n{output}")
                
                # Check for errors
                if self._check_for_errors(cell):
                    has_errors = True
                
                # Use the first answer cell's index as the reference
                if len(answer_cells) == 1:
                    first_cell_index = i
        
        # If no answer cells found, return None
        if not answer_cells:
            return None
        
        # Determine the dominant cell type (markdown vs code)
        cell_types = [cell['cell_type'] for cell in answer_cells]
        code_count = cell_types.count('code')
        markdown_count = cell_types.count('markdown')
        
        # Classify as mixed if both types present, otherwise use the majority
        if code_count > 0 and markdown_count > 0:
            dominant_type = 'mixed'
        elif code_count > markdown_count:
            dominant_type = 'code'
        else:
            dominant_type = 'markdown'
        
        # Create combined response
        return StudentResponse(
            problem_id=problem_id,
            part_id=None,
            content='\n\n'.join(combined_content),
            cell_type=dominant_type,
            cell_index=first_cell_index,
            execution_output='\n\n'.join(combined_output) if combined_output else None,
            has_errors=has_errors
        )
    
    def _is_answer_cell(self, cell) -> bool:
        """Determine if a cell contains a student answer"""
        # Check for answer tags
        tags = cell.get('metadata', {}).get('tags', [])
        if 'code answer' in tags or 'text answer' in tags:
            return True
        
        # Check for substantial content
        content = cell['source'].strip()
        if not content:
            return False
            
        # For code cells, check if there's actual code (not just comments)
        if cell['cell_type'] == 'code':
            non_comment_lines = [line for line in content.split('\n') 
                               if line.strip() and not line.strip().startswith('#')]
            return len(non_comment_lines) > 0
        
        # For markdown cells, check for answer indicators or substantial content
        if cell['cell_type'] == 'markdown':
            # Skip cells that are just problem statements (look for common problem indicators)
            problem_indicators = ['##', '(10)', '(20)', '(30)', '(40)', 'points)', '---']
            if any(indicator in content for indicator in problem_indicators):
                # This might be a problem statement, check if it's mainly that
                if len(content.split('\n')) <= 5 and any(indicator in content[:100] for indicator in problem_indicators):
                    return False
            
            # Look for answer indicators
            answer_indicators = ['answer:', '**answer:**', 'solution:', 'response:', '###', 'interpretation:', 'why these help:']
            content_lower = content.lower()
            if any(indicator in content_lower for indicator in answer_indicators):
                return True
            
            # Include substantial markdown content that's not obviously a problem statement
            return len(content) > 50
        
        return True  # Default to including non-empty cells
    
    def _get_execution_output(self, cell) -> Optional[str]:
        """Extract execution output from code cells, including images"""
        if cell['cell_type'] != 'code':
            return None
            
        outputs = cell.get('outputs', [])
        if not outputs:
            return None
        
        output_components = []
        
        for i, output in enumerate(outputs):
            output_type = output.get('output_type', 'unknown')
            
            # Handle text outputs
            if 'text' in output:
                text_data = output['text']
                if isinstance(text_data, list):
                    text_content = ''.join(text_data)
                else:
                    text_content = str(text_data)
                if text_content.strip():
                    output_components.append(f"[TEXT OUTPUT {i+1}]\n{text_content}")
            
            # Handle data outputs (including images)
            elif 'data' in output:
                data = output['data']
                
                # Text/plain data
                if 'text/plain' in data:
                    plain_data = data['text/plain']
                    if isinstance(plain_data, list):
                        text_content = ''.join(plain_data)
                    else:
                        text_content = str(plain_data)
                    if text_content.strip():
                        output_components.append(f"[PLAIN TEXT OUTPUT {i+1}]\n{text_content}")
                
                # Image data (PNG, JPEG, SVG)
                image_formats = ['image/png', 'image/jpeg', 'image/svg+xml']
                for img_format in image_formats:
                    if img_format in data:
                        # For images, we'll include metadata about the image
                        img_info = f"[IMAGE OUTPUT {i+1}]\nFormat: {img_format}\n"
                        
                        # Try to get image size if available
                        if img_format == 'image/svg+xml':
                            svg_data = data[img_format]
                            if isinstance(svg_data, list):
                                svg_content = ''.join(svg_data)
                            else:
                                svg_content = str(svg_data)
                            
                            # Extract SVG dimensions if present
                            import re
                            width_match = re.search(r'width=["\']?(\d+(?:\.\d+)?)', svg_content)
                            height_match = re.search(r'height=["\']?(\d+(?:\.\d+)?)', svg_content)
                            
                            if width_match and height_match:
                                img_info += f"Dimensions: {width_match.group(1)} x {height_match.group(1)}\n"
                            
                            # Include a snippet of the SVG for analysis
                            if len(svg_content) > 500:
                                img_info += f"SVG Content (first 500 chars): {svg_content[:500]}...\n"
                            else:
                                img_info += f"SVG Content: {svg_content}\n"
                        else:
                            # For PNG/JPEG, we can't easily extract dimensions without decoding
                            # But we can note the presence and format
                            img_data = data[img_format]
                            if isinstance(img_data, str):
                                data_size = len(img_data)
                                img_info += f"Data size: ~{data_size} characters (base64 encoded)\n"
                            
                            # Add a note about what this represents
                            img_info += "Image contains: Matplotlib plot/visualization\n"
                        
                        output_components.append(img_info)
                        break  # Only process the first image format found
                
                # HTML outputs (sometimes used for rich displays)
                if 'text/html' in data:
                    html_data = data['text/html']
                    if isinstance(html_data, list):
                        html_content = ''.join(html_data)
                    else:
                        html_content = str(html_data)
                    
                    # Include HTML but truncate if very long
                    if len(html_content) > 1000:
                        html_preview = html_content[:1000] + "...[truncated]"
                    else:
                        html_preview = html_content
                    
                    output_components.append(f"[HTML OUTPUT {i+1}]\n{html_preview}")
            
            # Handle execution results (like the last expression in a cell)
            elif output_type == 'execute_result' and 'data' in output:
                data = output['data']
                if 'text/plain' in data:
                    result_data = data['text/plain']
                    if isinstance(result_data, list):
                        result_content = ''.join(result_data)
                    else:
                        result_content = str(result_data)
                    output_components.append(f"[EXECUTION RESULT {i+1}]\n{result_content}")
        
        return '\n\n'.join(output_components) if output_components else None
    
    def _check_for_errors(self, cell) -> bool:
        """Check if cell execution resulted in errors"""
        if cell['cell_type'] != 'code':
            return False
            
        outputs = cell.get('outputs', [])
        for output in outputs:
            if output.get('output_type') == 'error':
                return True
        return False